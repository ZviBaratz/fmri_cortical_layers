import glob
import subprocess
import Bash_cmd
import os


class Prep_Fsl:
    def __init__(self, path: str = r"C:/Users/Owner/Desktop/Cortical_Layers_fMRI"):
        self.path = r"{0}/derivatives/feats".format(path)

    def prep_filtered_func(self, path: str = None):
        if not path:
            path = self.path
        func_data = glob.glob(r"{0}/*/*.feat".format(path))
        for func in func_data:
            filtered_func = r"{0}/filtered_func_data.nii.gz".format(func)
            output_filtered_func = r"{0}/filtered_func_data_standard.nii.gz".format(
                func
            )
            standard2example = r"{0}/reg/standard2example_func.mat".format(func)
            cmd = Bash_cmd.bash_get(
                '-lc "flirt -in /usr/local/fsl/data/standard/MNI152_T1_2mm_brain -ref {0} -applyxfm -init {1} -out {2}"'.format(
                    filtered_func, standard2example, output_filtered_func
                )
            )
            subprocess.run(cmd)
            print(r"Finished standardizing {0}".format(func.split(os.sep)[-1]))

    def run(self):
        self.prep_filtered_func(path=self.path)
