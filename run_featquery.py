import glob
import os
import subprocess
from Bash_cmd import bash_get
###


class Featquery:
    def __init__(self, path: str = r'C:/Users/Owner/Desktop/Cortical_Layers_fMRI'):
        self.path = r'{0}/derivatives/feats'.format(path)
        self.subjects = glob.glob('{0}/*'.format(self.path))

    def query(self, path: str, subjects: list):
        for subj in subjects:
            subnum = subj.split(os.sep)[-1]
            if not os.path.isdir('{0}/tsplots/{1}'.format(os.path.dirname(path), subnum)):
                os.makedirs('{0}/tsplots/{1}'.format(os.path.dirname(path), subnum))
            feats = glob.glob('{0}/*.feat'.format(subj))
            for feat in feats:
                prot = feat.split(os.sep)[-1].split('.')[0].replace('{0}_'.format(subnum), '')
                mask = glob.glob('{0}/*_bin.nii.gz'.format(feat))[0]
                output = '{0}/tsplots/{1}/{2}'.format(os.path.dirname(path), subnum, prot)
                cmd = bash_get('-lc "featquery 1 {0} 1 stats/cope1 {1} -p -s -b {2}"'.format(feat, prot, mask))
                subprocess.run(cmd)
                if os.path.isdir(output):
                    os.remove(output)
                os.rename('{0}/{1}'.format(feat, prot), output)

    def run(self):
        self.query(path=self.path, subjects=self.subjects)
