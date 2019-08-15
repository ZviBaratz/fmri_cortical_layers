import os
import glob
import subprocess
from Bash_cmd import bash_get


class run_all_fsfs:
    def __init__(self,path: str = r'C:/Users/Owner/Desktop/Cortical_Layers_fMRI'):
        self.path = r'{0}/Nifti'.format(path)
    def declare_paths(self, path: str):
        fsfdir=r'{0}/derivatives/scripts/fsfs'.format(os.path.dirname(path))
        feat_dir ='{0}/derivatives/feats'.format(os.path.dirname(path))
        all_fsfs = glob.glob('{0}/lev1/*'.format(fsfdir))
        return feat_dir,all_fsfs

    def run_fsfs(self, feat_dir: str, all_fsfs: list):
        for fsf in all_fsfs:
            cur_hdr = fsf.split(os.sep)[-1][:-4]
            cur_hdr = cur_hdr.replace('design_','')
            print(cur_hdr)
            sub = cur_hdr.split('_')[0]
            cur_feat = '{0}/{1}/{2}.feat'.format(feat_dir,sub,cur_hdr)
            flag = '{0}/stats/smoothness'.format(cur_feat)
            if os.path.isfile(flag) == False:
                cmd = bash_get('-lc "feat {0}"'.format(fsf))
                subprocess.run(cmd)
                while os.path.isfile(flag) == False:
                    if os.path.isfile(flag) == True:
                        break

    def run(self):
        feat_dir, all_fsfs = self.declare_paths(path=self.path)
        self.run_fsfs(feat_dir=feat_dir, all_fsfs=all_fsfs)

