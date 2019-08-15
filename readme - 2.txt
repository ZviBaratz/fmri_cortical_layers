Python (FSL) pipeline with examples:

1.Change original name of subject folder to 'sub-XX'

2.from BIDS_Create import BIDS_run ------ >
BIDS_run(subnum = '01', age = '26', hand = 'right', sex = 'm', toplvl = r'C:/Users/Owner/Desktop/Cortical_Layers_fMRI')

option 1: FSL pipeline

3.from prep_bold import run_prep_bold ----->
run_prep_bold(path = Path("C:/Users/Owner/Desktop/Cortical_Layers_fMRI/Nifti"),
	      outhtml = Path("C:/Users/Owner/Desktop/Cortical_Layers_fMRI/derivatives/scripts/bold_motion_QA.html"),
              out_bad_bold_list = Path("C:/Users/Owner/Desktop/Cortical_Layers_fMRI/derivatives/scripts/subs_lose_gt_45_vol_scrub.txt")

4.Make the first fsf using feat_gui and use it as a template

5.from make_fsf_lev1 import make_fsfs_first ---->
make_fsfs_first(path=r"C:/Users/Owner/Desktop/Cortical_Layers_fMRI/Nifti")

6.from run_fsfs import run_all_fsfs ---->
run_all_fsfs(path = r'C:/Users/Owner/Desktop/Cortical_Layers_fMRI/Nifti')

7.from QA_all_lev1s import QA_lev1(outfile = r'C:/Users/Owner/Desktop/Cortical_Layers_fMRI/derivatives/scripts/lev1_QA.html',
				   all_feats = glob.glob(r'C:/Users/Owner/Desktop/Cortical_Layers_fMRI/derivatives/feats/*/sub*.feat'))

8.from create_roi import run_create_roi(path=r'C:/Users/Owner/Desktop/Cortical_Layers_fMRI/derivatives/feats',mx='47',my='27',mz='35',sx='45',sy='25',sz='36')
(m for Motor, s for Sensory)

9.from calculate_mean_TS import calc_ts_properties(path = r'C:/Users/Owner/Desktop/Cortical_Layers_fMRI/derivatives/tsplots/mean_ts')

10.from plot_TIs import plot_TIs (Action = 'Motor',
				  path=r"C:/Users/Owner/Desktop/Cortical_Layers_fMRI/derivatives/tsplots/mean_ts",
				  filetype="mean_norm_bold_response",
				  sig_change=True,
				  ax = None)

option 2: Matlab (SPM) pipeline
3.create a loop that runs over all decompressed .nii files using spm_cortical_fMRI.m (+gunzip_files.py)
4.create_roi_spm.py
5.calculate_mean_TS_spm.m


10/6. all_TCs = gather_ts(path(path to all subs directory),subnum(number of subjects))
11/7. mean_ROI_table = calc_mean_roi(all_TCs)


