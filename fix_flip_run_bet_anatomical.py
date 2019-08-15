import glob
import os
from pathlib import Path
import subprocess

class BetBrainExtract:
    def __init__(self, path: str = r'C:/Users/Owner/Desktop/Cortical_Layers_fMRI'):
        self.path = '{0}/Nifti'.format(path)
    def fix_flip_run_anatomical(self, path: str):
        subdirs = glob.glob('%s/*/anat/*T1w.nii'%(path))

        for this_dir in subdirs:
            this_dir = this_dir.replace('C:','/mnt/c')
            this_dir = str(Path(this_dir))
            sub = os.path.dirname(this_dir).split(os.sep)[-2]
            print(sub)
            out_brain = this_dir[:-4]+'_brain'
        # Only run the following if your orientation was mixed up
        # BUT directional labels must be accurate in fslview
        # Make sure you verify that it worked
        #os.system("fslreorient2std  %s/anatomy/highres001  %s/anatomy/highres001"%(dir,dir))
        # bet call edit to use the flags you found worked well on your data
            cmd = 'bash -lc "bet {0} {1} -R -m"'.format(this_dir[:-4], out_brain)
            cmd = cmd.replace(os.sep,'/')
            os.system(cmd)

    def run(self):
        self.fix_flip_run_anatomical(path=self.path)


# If you want to try out freesurfer, here's the command line code that
# you can adapt to the loop via os.system.  Mostly, you'll need to put actual paths in.

# I think it needs unzipped files (double check this)
# gunzip path/to/anatomy/highres001.nii.gz

# This takes a while (~15 minutes?)
#recon-all -autorecon1 -i path/to/anatomy/highres001.nii -subjid autorecon   -sd /path/to/anatomy/
# This will actually create the skull stripped brain (you won't get a mask)

#mri_convert  /path/to/anatomy/autorecon/mri/brainmask.mgz  --reslice_like /path/to/anatomy/highres001.nii /path/to/anatomy/highres001_brain.nii

# I'm deleting the files it created
#rm -rf /path/to/anatomy/autorecon/

# zipping up the skull stripped image and original image
#gzip /path/to/anatomy/*.nii
