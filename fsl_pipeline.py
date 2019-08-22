import os
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

CRF_FILE = os.path.abspath("C:/Users/Owner/Desktop/CRF.xlsx")
PATH = os.path.abspath("C:/Users/Owner/Desktop/Cortical_Layers_fMRI")
DEFAULT_MOTOR = {'x': 47, 'y', 27, 'z': 35}
DEFAULY_SENSORY = {'x': 45, 'y': 25, 'z': 36}
COORDINATES = {'motor': DEFAULT_MOTOR, 'sensory': DEFAULY_SENSORY}


class FslPipeline:
    def __init__(
        self,
        n_subjects: int,
        crf_file: str = CRF_FILE,
        path: str = PATH,
        coordinates: dict = COORDINATES,
    ):
        self.n_subjects = n_subjects
        self.df = pd.read_excel(crf_file, header=0)
        self.path = path
        self.coordinates = coordinates

    def to_bids(self):
        """
        Converting Dicom files to Niftis, and organizes the data in BIDS format,
        :param n_subjects: an integer describing the number of subjects to analyze
        :param path: a string containing the path to the mother directory of all files
        """

        for i in range(self.n_subjects):
            data = self.df[i]
            identifier = int(data["subnum"].split("-")[-1])
            bids = subject_bids.RunBids(
                subnum=identifier,
                age=data.Age,
                hand=data.Hand,
                sex=data.Gender,
                toplvl=self.path,
            )
            bids.run()

    def brain_extraction(self):
        """
        FSL's BET-based brain extraction (skull stripping)
        :param path: a string containing the path to the mother directory of all files
        """

        brain_extract = fix_flip_run_bet_anatomical.BetBrainExtract(path=self.path)
        brain_extract.run()

    def motion_assess(self):
        """
        FSL's motion assessment
        :param path: a string containing the path to the mother directory of all files
        :return: motion-assess directory in "func" for each subject and for each scan
        """

        bold_create = prep_bold.RunPrepBold(path=self.path)
        bold_create.run()

    def prep_bold_spm(self):
        """
        MATLAB-based preproccessing pipeline based on spm batch script
        :param path: a string containing the path to the mother directory of all files
        :return: swr (smoothed, warped, realigned) nifti files for each scan + preproccessing derviatives
        """

        bold_prep = run_spm_preproc.SpmPrep(path=self.path)
        bold_prep.run()

    def make_fsfs_files(self):
        """
        FEAT design files creation, based on functional nifti scans
        :param path: a string containing the path to the mother directory of all files
        :return: "scripts" folder, under which will be all the .fsf files for the FEAT analysis
        """

        fsfs_make = make_fsf_lev1.FsfsFirstLevel(path=self.path)
        fsfs_make.run()

    def run_fsfs(self, path: str = None):
        """
        Running the design.fsf files through FEAT
        :param path: a string containing the path to the mother directory of all files
        :return: FEAT directories as created after FEAT analysis
        """

        fsfs_run = run_fsfs.run_all_fsfs(path=self.path)
        fsfs_run.run()

    def qa_lev1(self):
        """
        QA for the first-level analysis of FEAT.
        :param path: a string containing the path to the mother directory of all files
        :return: HTML file containing several features from the FEAT directories
        """

        lev1_qa = QA_all_lev1s.qa_lev1_analysis(path=self.path)
        lev1_qa.run()

    def create_roi(self):
        """
        Create ROI for each FEAT directory, for further analysis
        :return: binary ROI spheres for motor and sensory paradigm, centered in voxel-based coordinates
        """

        ROI = create_roi.CreateROI(path=self.path, coordinates=self.coordinates)
        ROI.run()

    def featquery(self):
        """
        ROI analysis based on featquery for each scan for which there is a ROI image in it's feat directory
        :param path: a string containing the path to the mother directory of all files
        :return: time series directory, containing the averaged time course in the relevant ROI
        """

        query = run_featquery.Featquery(path=path)
        query.run()

    def ts_gather(self, path: str = None):
        """
        Move all relevant averaged time courses and gather them in a specific time series directory
        :param path: a string containing the path to the mother directory of all files
        :return: time series directory, containing all averaged time courses, as extracted from featquery
        """

        gather = gather_ts.Get_TS(path=self.path)
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

        features_calc = calc_mean_ts.CalcMeanTS(path=self.path)
        features_calc.run()

    def native2standard(self, path: str = None):
        """
        FSL's FLIRT-based registrating of standard MNI template to each subject's scan native space.
        :param path: a string containing the path to the mother directory of all files
        :return: _standard filtered nifti file, of standard template in native space.
        """

        to_standard = fsl_standarize.Prep_Fsl(path=self.path)
        to_standard.run()

    def run(self):
        """
        Running all FSL-based pipeline for analyzing Cortical-Layers fMRI data
        """

        self.to_bids()
        self.brain_extraction()
        self.motion_assess()
        self.make_fsfs_files()
        self.run_fsfs()
        self.qa_lev1()
        self.native2standard()
        self.create_roi()
        self.featquery()
        self.ts_gather()
        self.calc_ts_features()
