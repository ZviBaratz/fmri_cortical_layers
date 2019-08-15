import os
import glob
import subprocess
from Bash_cmd import bash_get
###


class CreateROI:
    def __init__(self, path: str = r'C:/Users/Owner/Desktop/Cortical_Layers_fMRI',
                 mx: int = 47, my: int = 27, mz: int = 35, sx: int = 45, sy: int = 25, sz: int = 36):
        self.path = r'{0}/derivatives/feats'.format(path)
        self.mx = str(mx)
        self.my = str(my)
        self.mz = str(mz)
        self.sx = str(sx)
        self.sy = str(sy)
        self.sz = str(sz)

    def run_create_roi(self,path: str, mx: str,my: str,mz: str,sx: str,sy: str,sz: str):
        #path = r'C:/Users/Owner/Desktop/Cortical_Layers_fMRI/derivatives/feats'
        ###Define ROI
        func_files = glob.glob(r'{0}/*/*.feat/filtered_func_data.nii.gz'.format(path))
        for func_data in func_files:
            if 'Motor' in func_data:
                x=mx
                y=my
                z=mz
                out_point = '{0}/Motor_ROI_point'.format(os.path.dirname(func_data))
                out_sphere = '{0}/Motor_ROI_sphere'.format(os.path.dirname(func_data))
            elif 'Sensory' in func_data:
                x = sx
                y = sy
                z = sz
                out_point = '{0}/Sensory_ROI_point'.format(os.path.dirname(func_data))
                out_sphere = '{0}/Sensory_ROI_sphere'.format(os.path.dirname(func_data))
            print(os.path.dirname(func_data))
            sphere_size = '8'
            if os.path.isfile('{0}.nii.gz'.format(out_point)) == True:
                os.remove('{0}.nii.gz'.format(out_point))
            if 'IREPI' in func_data:
                z = str(float(z)-21)
            cmd = bash_get('-lc "fslmaths {0} -mul 0 -add 1 -roi {1} 1 {2} 1 {3} 1 0 1 {4} -odt float"'.format(func_data, x, y, z,out_point))
            subprocess.run(cmd)
            while os.path.isfile('{0}.nii.gz'.format(out_point)) == False:
                print('Waiting on point')
                if os.path.isfile('{0}.nii.gz'.format(out_point)) == True:
                    break
            if os.path.isfile('{0}.nii.gz'.format(out_sphere)) == True:
                os.remove('{0}.nii.gz'.format(out_sphere))
            cmd = bash_get('-lc "fslmaths {0} -kernel sphere {1} -fmean {2} -odt float"'.format(out_point, sphere_size, out_sphere))
            subprocess.run(cmd)
            while os.path.isfile('{0}.nii.gz'.format(out_sphere)) == False:
                print('Waiting on Spehere')
                if os.path.isfile('{0}.nii.gz'.format(out_sphere)) == True:
                    break
            if os.path.isfile('{0}_bin.nii.gz'.format(out_sphere)) == True:
                os.remove('{0}_bin.nii.gz'.format(out_sphere))
            cmd = bash_get('-lc "fslmaths {0}.nii.gz -bin {0}_bin.nii.gz"'.format(out_sphere))
            subprocess.run(cmd)

    def run(self):
        self.run_create_roi(path=self.path, mx=self.mx, my=self.my, mz=self.mz, sx=self.sx, sy=self.sy, sz=self.sz)