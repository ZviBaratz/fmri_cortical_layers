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

        :param subnum: an
        :param crf_dir:
        :return:
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
        if not path:
            path = self.path
        brain_extract = fix_flip_run_bet_anatomical.BetBrainExtract(path=path)
        brain_extract.run()

    def motion_assess(self, path: str = None):
        if not path:
            path = self.path
        bold_create = prep_bold.RunPrepBold(path=path)
        bold_create.run()

    def prep_bold_spm(self, path: str = None):
        if not path:
            path = self.path
        bold_prep = run_spm_preproc.SpmPrep(path=path)
        bold_prep.run()

    def make_fsfs_files(self, path: str = None):
        if not path:
            path = self.path
        fsfs_make = make_fsf_lev1.FsfsFirstLevel(path=path)
        fsfs_make.run()

    def run_fsfs(self, path: str = None):
        if not path:
            path = self.path
        fsfs_run = run_fsfs.run_all_fsfs(path=path)
        fsfs_run.run()

    def qa_lev1(self, path: str = None):
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
        if not path:
            path = self.path
        query = run_featquery.Featquery(path=path)
        query.run()

    def ts_gather(self, path: str = None):
        if not path:
            path = self.path
        gather = gather_ts.Get_TS(path=path)
        gather.run()

    def calc_ts_features(self, path: str = None):
        if not path:
            path = self.path
        features_calc = calc_mean_ts.CalcMeanTS(path=path)
        features_calc.run()

    def run(self):
        self.bids(subjects_number=self.subjects_number, path=self.path)
        self.brain_extraction(path=self.path)
        self.prep_bold_spm(path=self.path)
        self.motion_assess(path=self.path)
        self.make_fsfs_files(path=self.path)
        self.run_fsfs(path=self.path)
        self.qa_lev1(path=self.path)
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
