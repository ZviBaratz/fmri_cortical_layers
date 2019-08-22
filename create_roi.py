import os
import glob
import subprocess
from Bash_cmd import bash_get

PATH = os.path.abspath("C:/Users/Owner/Desktop/Cortical_Layers_fMRI/derivatives/feats")


class CreateROI:
    def __init__(self, coordinates: dict, path: str = PATH):
        self.path = path
        self.coordinates = coordinates

    def get_coordinates(self, file_path: str):
        if "Motor" in file_path:
            return self.coordinates["motor"]
        return self.coordinates["sensory"]

    def run(self):
        func_files = glob.glob(
            r"{0}/*/*.feat/filtered_file_path.nii.gz".format(self.path)
        )
        for file_path in func_files:
            if "Motor" in file_path:
                out_point = "{0}/Motor_ROI_point".format(os.path.dirname(file_path))
                out_sphere = "{0}/Motor_ROI_sphere".format(os.path.dirname(file_path))
            elif "Sensory" in file_path:
                out_point = "{0}/Sensory_ROI_point".format(os.path.dirname(file_path))
                out_sphere = "{0}/Sensory_ROI_sphere".format(os.path.dirname(file_path))
            print(os.path.dirname(file_path))
            sphere_size = "8"
            if os.path.isfile("{0}.nii.gz".format(out_point)):
                os.remove("{0}.nii.gz".format(out_point))
            coords = self.get_coordinates(file_path)
            if "IREPI" in file_path:
                coords["z"] = str(float(coords["z"]) - 21)
            cmd = bash_get(
                '-lc "fslmaths {0} -mul 0 -add 1 -roi {1} 1 {2} 1 {3} 1 0 1 {4} -odt float"'.format(
                    file_path, coords["x"], coords["y"], coords["z"], out_point
                )
            )
            subprocess.run(cmd)
            while os.path.isfile("{0}.nii.gz".format(out_point)) == False:
                print("Waiting on point")
                if os.path.isfile("{0}.nii.gz".format(out_point)) == True:
                    break
            if os.path.isfile("{0}.nii.gz".format(out_sphere)) == True:
                os.remove("{0}.nii.gz".format(out_sphere))
            cmd = bash_get(
                '-lc "fslmaths {0} -kernel sphere {1} -fmean {2} -odt float"'.format(
                    out_point, sphere_size, out_sphere
                )
            )
            subprocess.run(cmd)
            while os.path.isfile("{0}.nii.gz".format(out_sphere)) == False:
                print("Waiting on Spehere")
                if os.path.isfile("{0}.nii.gz".format(out_sphere)) == True:
                    break
            if os.path.isfile("{0}_bin.nii.gz".format(out_sphere)) == True:
                os.remove("{0}_bin.nii.gz".format(out_sphere))
            cmd = bash_get(
                '-lc "fslmaths {0}.nii.gz -bin {0}_bin.nii.gz"'.format(out_sphere)
            )
            subprocess.run(cmd)

