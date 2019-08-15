Python (FSL) pipeline:
1.Change original name of subject folder to 'sub-XX'
2.BIDS_Create.py

option 1: FSL pipeline
3.prep_bold.py
4.Make the first fsf using feat_gui and use it as a template
5.make_fsf_lev1.py
6.run_fsfs.py
7.QA_all_lev1s.py
8.create_roi.py
9.calculate_mean_TS.py

option 2: Matlab (SPM) pipeline
3.create a loop that runs over all decompressed .nii files using spm_cortical_fMRI.m (+gunzip_files.py)
4.create_roi_spm.py
5.calculate_mean_TS_spm.m


10/6. all_TCs = gather_ts(path(path to all subs directory),subnum(number of subjects))
11/7. mean_ROI_table = calc_mean_roi(all_TCs)


