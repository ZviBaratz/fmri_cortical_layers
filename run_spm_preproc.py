import os
import glob


class SpmPrep:
    def __init__(self, path: str = r"C:/Users/Owner/Desktop/Cortical_Layers_fMRI"):
        self.path = "{0}/Nifti".format(path)

    def get_subjects(self, path: str = None):
        if not path:
            path = self.path
        subjects = glob.glob(r"{0}/sub-*".format(path))
        subjects_to_return = list()
        for subj in subjects:
            subj = subj.split(os.sep)[-1]
            subjects_to_return.append(subj)
        return subjects_to_return

    def get_subj_protocols(self, subj: str, path: str = None):
        if not path:
            path = self.path
        sub_path = r"{0}/{1}".format(path, subj)
        protocols = glob.glob(r"{0}/func/*.json".format(sub_path))
        protocols_to_return = list()
        for prot in protocols:
            protocols_to_return.append(prot.split("_")[-2].split("-")[-1])
        protocols_to_return = set(protocols_to_return)
        return protocols_to_return

    def spm_prep(self, subj: str, prot: str, path: str = None):
        acqs = ["Motor", "Sensory"]
        for acq in acqs:
            os.system(
                r"matlab -noFigureWindows -nosplash -nodesktop -wait -r "
                r"spm_cortical_fMRI('{0}','{1}','{2}','{3}');exit".format(
                    acq, prot, subj, path
                )
            )

    def move_new_files(self, subj: str, path: str = None):
        if not path:
            path = self.path
        files = glob.glob(r"{0}/{1}/func/[!s]*".format(path, subj))
        if not os.path.isdir(r"{0}/{1}/func/spm_prep".format(path, subj)):
            os.mkdir(r"{0}/{1}/func/spm_prep".format(path, subj))
        for f in files:
            file_name = f.split(os.sep)[-1]
            os.rename(f, r"{0}/{1}/func/spm_prep/{2}".format(path, subj, file_name))

    def run(self):
        subjects = self.get_subjects(path=self.path)
        for subj in subjects:
            protocols = self.get_subj_protocols(subj=subj, path=self.path)
            for prot in protocols:
                self.spm_prep(subj=subj, prot=prot, path=self.path)
            self.move_new_files(subj=subj, path=self.path)
