#!/usr/bin/env python


import glob
import os

 
path = '/Users/jeanettemumford/Documents/Research/Talks/MumfordBrainStats/ds008/'

boldfiles = glob.glob('%s/sub0[0-9][0-9]/BOLD/task00[0-9]_run00[0-9]/bold.nii.gz'%(path))

for file in boldfiles:  
    print file
    os.system("fslnvols %s"%(file))



    
