#!/usr/bin/env python

import glob
import os

path = r'C:/Users/Owner/Desktop/Cortical_Layers_fMRI/derivatives/nii_SPM'
source_path = r'C:/Users/Owner/Desktop/Cortical_Layers_fMRI/Nifti'
func_files = glob.glob('{0}/*/func/*rsub-0*'.format(source_path))
for f in func_files:
    f_name = f.split(os.sep)[-1]
    subj = f.split(os.sep)[-3]
    dits = f.split('-')
    prot = dits[-1].split('_')[0]
    task = dits[-2].split('_')[0]
    new_f_dir = '{0}/{1}/{2}_{3}/func_files'.format(path,subj,task,prot)
    if os.path.isdir(new_f_dir) == False:
        os.mkdir(new_f_dir)
    os.rename(f,'{0}/{1}'.format(new_f_dir,f_name))
subdirs = glob.glob('{0}/sub-*/[Motor|Sensory]*_stats'.format(path))
for dir in subdirs:
    stats_dir = dir.split(os.sep)[-1]
    new_dir = dir.rstrip('_stats')
    print(new_dir)
    if os.path.isdir(new_dir) == False:
        os.mkdir(new_dir)
    os.rename(dir,'{0}/{1}'.format(new_dir,stats_dir))