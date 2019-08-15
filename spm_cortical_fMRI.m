%%
% Processing a task-based single-subject fMRI dataset.
% 
% Prerequisites:
% - Matlab recent version (developed using 2016b on Mac OS Sierra)
% - SPM12 neuroimage processing toolbox: https://www.fil.ion.ucl.ac.uk/spm/software/spm12/
% - Task fMRI data: https://openneuro.org/datasets/ds000157/versions/00001
% - A basic understanding of the processing steps involved in analysing
% task fMRI
% 
% Dependencies:
% - spm_standardPreproc_jsh
% - spm_specify1stlevel_jsh
% - spm_estimateModel_jsh
% - spm_setupTaskContrast_jsh
% - spm_runResults_jsh
% 
% See online tutorial for full details: https://www.fmrwhy.com/2018/06/28/spm12-matlab-scripting-tutorial-1/
%__________________________________________________________________________
% Copyright (C) Stephan Heunis 2018
% 


% ATTENTION!!!
% PLEASE MAKE SURE TO CHANGE:
% 1. FILES DIRECTORY (f_fn)
% 2. STATS DIRECTORY (stats_dir)
% 3. DESIGN PROPERTIES
% BEFORE RUNNING THE SPM ANALYSIS PIPELINE!
function spm_cortical_fMRI(active,acq,subj,data_dir)
%% INITIALIZATION
% Initialize file locations, image file names and other variables
%data_dir = 'C:\Users\Owner\Desktop\Cortical_Layers_fMRI\Nifti';
spm_dir = 'C:\Users\Owner\Desktop\FSL_pipeline\spm12';
addpath(spm_dir);
%% Change the following:
% TR = 3;
% active = 'Motor';
% acq = 'IREPITI750';
% subj = 'sub-02';
if strcmp(acq,'Gre')
    TR=1.5;
else
    TR=3;
end
if strcmp(subj,'sub-02') || strcmp(subj,'sub-03')
    t_onsets = [7; 37; 67; 97];
else
    t_onsets = [15; 45; 75; 105];
end

%%
s_fn = [data_dir filesep subj filesep 'anat' filesep subj '_T1w.nii']; %Enter functional 4D image.
f_fn = [data_dir filesep subj filesep 'func' filesep subj '_task-' active '_acq-' acq '_bold.nii'];%Enter structural 4D image.
fwhm = 5;  % mm

%% PREPROCESSING
disp('PREPROCESSING')
% Preprocess structural and functional images (if not already)
[d, f, e] = fileparts(s_fn);
[d1, f1, e1] = fileparts(f_fn);
if exist([d1 filesep 'swr' f1 e1], 'file')
    disp('...preproc already done, saving variables...')
    preproc_data = struct;
    % Structural filenames
    preproc_data.forward_transformation = [d filesep 'y_' f e];
    preproc_data.inverse_transformation = [d filesep 'iy_' f e];
    preproc_data.gm_fn = [d filesep 'c1' f e];
    preproc_data.wm_fn = [d filesep 'c2' f e];
    preproc_data.csf_fn = [d filesep 'c3' f e];
    preproc_data.bone_fn = [d filesep 'c4' f e];
    preproc_data.soft_fn = [d filesep 'c5' f e];
    preproc_data.air_fn = [d filesep 'c6' f e];
%     preproc_data.rstructural_fn = [d filesep 'r' f e];
%     preproc_data.rgm_fn = [d filesep 'rc1' f e];
%     preproc_data.rwm_fn = [d filesep 'rc2' f e];
%     preproc_data.rcsf_fn = [d filesep 'rc3' f e];
%     preproc_data.rbone_fn = [d filesep 'rc4' f e];
%     preproc_data.rsoft_fn = [d filesep 'rc5' f e];
%     preproc_data.rair_fn = [d filesep 'rc6' f e];
    % Functional filenames
    preproc_data.rfunctional_fn = [d1 filesep 'r' f1 e1];
    preproc_data.wrfunctional_fn = [d1 filesep 'wr' f1 e1];
    preproc_data.swrfunctional_fn = [d1 filesep 'swr' f1 e1];
    preproc_data.mp_fn = [d1 filesep 'rp_' f1 '.txt'];
    preproc_data.MP = load(preproc_data.mp_fn);
else
    disp('...running preprocessing batch jobs...')
    preproc_data = spm_standardPreproc_jsh(f_fn, s_fn, fwhm, spm_dir);
    preproc_data = struct;
    % Structural filenames
    preproc_data.forward_transformation = [d filesep 'y_' f e];
    preproc_data.inverse_transformation = [d filesep 'iy_' f e];
    preproc_data.gm_fn = [d filesep 'c1' f e];
    preproc_data.wm_fn = [d filesep 'c2' f e];
    preproc_data.csf_fn = [d filesep 'c3' f e];
    preproc_data.bone_fn = [d filesep 'c4' f e];
    preproc_data.soft_fn = [d filesep 'c5' f e];
    preproc_data.air_fn = [d filesep 'c6' f e];
%     preproc_data.rstructural_fn = [d filesep 'r' f e];
%     preproc_data.rgm_fn = [d filesep 'rc1' f e];
%     preproc_data.rwm_fn = [d filesep 'rc2' f e];
%     preproc_data.rcsf_fn = [d filesep 'rc3' f e];
%     preproc_data.rbone_fn = [d filesep 'rc4' f e];
%     preproc_data.rsoft_fn = [d filesep 'rc5' f e];
%     preproc_data.rair_fn = [d filesep 'rc6' f e];
    % Functional filenames
    preproc_data.rfunctional_fn = [d1 filesep 'r' f1 e1];
    preproc_data.wrfunctional_fn = [d1 filesep 'wr' f1 e1];
    preproc_data.swrfunctional_fn = [d1 filesep 'swr' f1 e1];
    preproc_data.mp_fn = [d1 filesep 'rp_' f1 '.txt'];
    preproc_data.MP = load(preproc_data.mp_fn);
end
% Check coregistration and segmentation
spm_check_registration(s_fn, [preproc_data.wrfunctional_fn ',1'], preproc_data.gm_fn, preproc_data.wm_fn, preproc_data.csf_fn)
disp('Preprocessing done!')
end