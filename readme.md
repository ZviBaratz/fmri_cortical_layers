Python (FSL-based) pipeline for analyzing Cortical-Layers fMRI data
----------------------
Prerequisites:

1. In order to work with the pipeline attached, you need to change the  original name of subject folder to 'sub-XX (subject's number)'
2. A CRF.xlsx file containing data regarding the subjects: subject number, age, sex, and dominant hand.

Once the prerequisites are met, you can use the fsl_pipeline.py class (see it's notes) to analyze your data.

the pipeline contains the following classes/functions:
* **_get_subjects_data:_**
 
        Returns subject data.
        :param subnum: an integer describing the number of the subject to which the function extracts data.
        :param crf_dir: a string variable contains the path to the CRF excel file.
        :return: strings describing the subject number, age, dominant hand, and sex, as in the CRF file.

* **_bids:_**

        Converting Dicom files to Niftis, and organizes the data in BIDS format,
        :param subjects_number: an integer describing the number of subjects to analyze
        :param path: a string containing the path to the mother directory of all files
        
* **_brain_extracion:_**

        FSL's BET-based brain extraction (skull stripping)
        :param path: a string containing the path to the mother directory of all files
      
* **_motion_assess:_**

        FSL's motion assessment
        :param path: a string containing the path to the mother directory of all files
        :return: motion-assess directory in "func" for each subject and for each scan
        
* **_prep_bold_spm:_** *NOT CURRENTLY USED

        MATLAB-based preproccessing pipeline based on spm batch script
        :param path: a string containing the path to the mother directory of all files
        :return: swr (smoothed, warped, realigned) nifti files for each scan + preproccessing derviatives

* **_make_fsfs_files:_**

        FEAT design files creation, based on functional nifti scans
        :param path: a string containing the path to the mother directory of all files
        :return: "scripts" folder, under which will be all the .fsf files for the FEAT analysis

* **_run_fsfs:_**

        Running the design.fsf files through FEAT
        :param path: a string containing the path to the mother directory of all files
        :return: FEAT directories as created after FEAT analysis

* **_qa_lev1:_**

        QA for the first-level analysis of FEAT.
        :param path: a string containing the path to the mother directory of all files
        :return: HTML file containing several features from the FEAT directories

* **_roi_create:_**

        Create ROI for each FEAT directory, for further analysis
        :param path: a string containing the path to the mother directory of all files
        :param mx: motor X value
        :param my: motor Y value
        :param mz: motor Z value
        :param sx: sensory X value
        :param sy: sensory Y value
        :param sz: sensory Z value
        :return: binary ROI spheres for motor and sensory paradigm, centered in voxel-based coordinates

* **_featquery:_**

        ROI analysis based on featquery for each scan for which there is a ROI image in it's feat directory
        :param path: a string containing the path to the mother directory of all files
        :return: time series directory, containing the averaged time course in the relevant ROI

* **_ts_gather:_**

        Move all relevant averaged time courses and gather them in a specific time series directory
        :param path: a string containing the path to the mother directory of all files
        :return: time series directory, containing all averaged time courses, as extracted from featquery

* **_calc_ts_features:_**

        Calculation of several features regarding the averaged time courses, creating the following files:

        all_ts = all raw-data time series from all subjects.
        fixed_ts = since an error occured while scanning 2 subjects (02 and 03), a realigned time series across all subjects.
        mean_bold_response = non-normalized, raw averaged bold response, across all subjects
        mean_norm_bold_response = after intra-subject normalization, a calculated mean normalized bold response.
        mean_ts = non-normalized, raw averaged time course, across all subjects
        mean_normalized_ts = a normalized time series across all subjects.
        normalized_ts = normalized time series for each subject.
        subjects_norm_BOLD_response = non-averaged, normalized BOLD response, for each subject.

        :param path: a string containing the path to the mother directory of all files
        :return: files mentioned above

* **_native2standard:_**

        FSL's FLIRT-based registrating of standard MNI template to each subject's scan native space.
        :param path: a string containing the path to the mother directory of all files
        :return: _standard filtered nifti file, of standard template in native space.

* **_run:_**

        Running all FSL-based pipeline for analyzing Cortical-Layers fMRI data