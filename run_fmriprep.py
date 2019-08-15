import os
###set pathes to relevant tools
os.system('export ANTSPATH=${HOME}/bin/ants/bin/')
os.system('export PATH=${ANTSPATH}:$PATH')
os.system('export FREESURFER_HOME=/Applications/freesurfer')
os.system('source $FREESURFER_HOME/SetUpFreeSurfer.sh')
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8
###run command line
os.system('/Users/glhrsqwbyz/local/bin/fmriprep-docker /Users/glhrsqwbyz/Desktop/Projects/fMRI_Cortical_Layers/BIDS_Pilot2 /Users/glhrsqwbyz/Desktop/Projects/fMRI_Cortical_Layers/BIDS_Pilot2/derivatives participant --fs-license-file /Applications/freesurfer/license.txt')
