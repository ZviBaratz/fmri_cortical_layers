import subject_bids
import pandas as pd
import prep_bold
import make_fsf_lev1
import run_fsfs
import QA_all_lev1s
import create_roi
import calc_mean_ts
import run_featquery
import gather_ts
import fix_flip_run_bet_anatomical
import run_spm_preproc
import fsl_standarize

CRF_DIR = r"C:\Users\Owner\Desktop"
PATH = r"C:/Users/Owner/Desktop/Cortical_Layers_fMRI"


class FSL_Pipe:
    def __init__(
        self,
        subjects_number: int,
        crf_dir: str = CRF_DIR,
        path: str = None,
        mx: int = 47,
        my: int = 27,
        mz: int = 35,
        sx: int = 45,
        sy: int = 25,
        sz: int = 36,
    ):
        self.subjects_number = subjects_number
        self.crf_dir = r"{0}/CRF.xlsx".format(crf_dir)
        self.mx = mx
        self.my = my
        self.mz = mz
        self.sx = sx
        self.sy = sy
        self.sz = sz
        if not path:
            self.path = PATH
        else:
            self.path = path

    def get_subjects_data(self, subnum: int, crf_dir: str = None):
        """
        Returns subject data.
        :param subnum: an integer describing the number of the subject to which the function extracts data.
        :param crf_dir: a string variable contains the path to the CRF excel file.
        :return: strings describing the subject number, age, dominant hand, and sex, as in the CRF file.
        """
        if not crf_dir:
            crf_dir = self.crf_dir
        crf = pd.read_excel(crf_dir, header=0)
        subject_num = crf.subnum[subnum]
        age = crf.Age[subnum]
        hand = crf.Hand[subnum]
        sex = crf.Gender[subnum]
        return subject_num, str(age), hand, sex

    def bids(self, subjects_number: int = None, path: str = None):
        """
        Converting Dicom files to Niftis, and organizes the data in BIDS format,
        :param subjects_number: an integer describing the number of subjects to analyze
        :param path: a string containing the path to the mother directory of all files
        """
        if not subjects_number:
            subjects_number = self.subjects_number
        if not path:
            path = self.path
        for i in range(subjects_number):
            subnum, age, hand, sex = self.get_subjects_data(subnum=i)
            num = subnum.split("-")[-1]
            bids = subject_bids.RunBids(
                subnum=num, age=age, hand=hand, sex=sex, toplvl=path
            )
            bids.run()

    def brain_extraction(self, path: str = None):
        """
        FSL's BET-based brain extraction (skull stripping)
        :param path: a string containing the path to the mother directory of all files
        """
        if not path:
            path = self.path
        brain_extract = fix_flip_run_bet_anatomical.BetBrainExtract(path=path)
        brain_extract.run()

    def motion_assess(self, path: str = None):
        """
        FSL's motion assessment
        :param path: a string containing the path to the mother directory of all files
        :return: motion-assess directory in "func" for each subject and for each scan
        """
        if not path:
            path = self.path
        bold_create = prep_bold.RunPrepBold(path=path)
        bold_create.run()

    def prep_bold_spm(self, path: str = None):
        """
        MATLAB-based preproccessing pipeline based on spm batch script
        :param path: a string containing the path to the mother directory of all files
        :return: swr (smoothed, warped, realigned) nifti files for each scan + preproccessing derviatives
        """
        if not path:
            path = self.path
        bold_prep = run_spm_preproc.SpmPrep(path=path)
        bold_prep.run()

    def make_fsfs_files(self, path: str = None):
        """
        FEAT design files creation, based on functional nifti scans
        :param path: a string containing the path to the mother directory of all files
        :return: "scripts" folder, under which will be all the .fsf files for the FEAT analysis
        """
        if not path:
            path = self.path
        fsfs_make = make_fsf_lev1.FsfsFirstLevel(path=path)
        fsfs_make.run()

    def run_fsfs(self, path: str = None):
        """
        Running the design.fsf files through FEAT
        :param path: a string containing the path to the mother directory of all files
        :return: FEAT directories as created after FEAT analysis
        """
        if not path:
            path = self.path
        fsfs_run = run_fsfs.run_all_fsfs(path=path)
        fsfs_run.run()

    def qa_lev1(self, path: str = None):
        """
        QA for the first-level analysis of FEAT.
        :param path: a string containing the path to the mother directory of all files
        :return: HTML file containing several features from the FEAT directories
        """
        if not path:
            path = self.path
        lev1_qa = QA_all_lev1s.qa_lev1_analysis(path=path)
        lev1_qa.run()

    def roi_create(
        self,
        path: str = None,
        mx: int = None,
        my: int = None,
        mz: int = None,
        sx: int = None,
        sy: int = None,
        sz: int = None,
    ):
        """
        Create ROI for each FEAT directory, for further analysis
        :param path: a string containing the path to the mother directory of all files
        :param mx: motor X value
        :param my: motor Y value
        :param mz: motor Z value
        :param sx: sensory X value
        :param sy: sensory Y value
        :param sz: sensory Z value
        :return: binary ROI spheres for motor and sensory paradigm, centered in voxel-based coordinates
        """
        if not path:
            path = self.path
        if not mx or my or mz or sx or sy or sz:
            mx, my, mz, sx, sy, sz = (
                self.mx,
                self.my,
                self.mz,
                self.sx,
                self.sy,
                self.sz,
            )
        ROI = create_roi.CreateROI(path=path, mx=mx, my=my, mz=mz, sx=sx, sy=sy, sz=sz)
        ROI.run()

    def featquery(self, path: str = None):
        """
        ROI analysis based on featquery for each scan for which there is a ROI image in it's feat directory
        :param path: a string containing the path to the mother directory of all files
        :return: time series directory, containing the averaged time course in the relevant ROI
        """
        if not path:
            path = self.path
        query = run_featquery.Featquery(path=path)
        query.run()

    def ts_gather(self, path: str = None):
        """
        Move all relevant averaged time courses and gather them in a specific time series directory
        :param path: a string containing the path to the mother directory of all files
        :return: time series directory, containing all averaged time courses, as extracted from featquery
        """
        if not path:
            path = self.path
        gather = gather_ts.Get_TS(path=path)
        gather.run()

    def calc_ts_features(self, path: str = None):
        """
        Calculation of several features regarding the averaged time courses, creating the following files:

        all_ts = all raw-data time series from all subjects.
        fixed_ts = since an error occured while scanning 2 subjects (02 and 03), a realigned time series across all subjects.
        mean_bold_response = non-normalized, raw averaged bold response, across all subjects
        mean_norm_bold_response = after intra-subject normalization, a calculated mean normalized bold response.
        mean_ts = non-normalized, raw averaged time course, across all subjects
        mean_normalized_ts = a normalized time series across all subjects.
        normalized_ts = normalized time series for each subject.
        subjects_norm_BOLD_response = non-averaged, normalized BOLD response, for each subject.

        :param path: a string containing the path to the mother directory of all files
        :return: files mentioned above
        """
        if not path:
            path = self.path
        features_calc = calc_mean_ts.CalcMeanTS(path=path)
        features_calc.run()

    def native2standard(self, path: str = None):
        """
        FSL's FLIRT-based registrating of standard MNI template to each subject's scan native space.
        :param path: a string containing the path to the mother directory of all files
        :return: _standard filtered nifti file, of standard template in native space.
        """
        if not path:
            path = self.path
        to_standard = fsl_standarize.Prep_Fsl(path=path)
        to_standard.run()

    def run(self):
        """
        Running all FSL-based pipeline for analyzing Cortical-Layers fMRI data
        """
        self.bids(subjects_number=self.subjects_number, path=self.path)
        self.brain_extraction(path=self.path)
        # self.prep_bold_spm(path=self.path)
        self.motion_assess(path=self.path)
        self.make_fsfs_files(path=self.path)
        self.run_fsfs(path=self.path)
        self.qa_lev1(path=self.path)
        self.native2standard(path=self.path)
        self.roi_create(
            path=self.path,
            mx=self.mx,
            my=self.my,
            mz=self.mz,
            sx=self.sx,
            sy=self.sy,
            sz=self.sz,
        )
        self.featquery(path=self.path)
        self.ts_gather(path=self.path)
        self.calc_ts_features(path=self.path)
