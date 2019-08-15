#!/usr/bin/python

# This follows the level 1 QA script (4_QA...py)

import os
import glob

# We will start with the registration png files
outfile = "/Users/jeanettemumford/Documents/Research/Talks/MumfordBrainStats/ds008_R1.1.0_raw/QA/lev2_QA.html"
os.system("rm %s"%(outfile))

all_feats = glob.glob('/Users/jeanettemumford/Documents/Research/Talks/MumfordBrainStats/ds008_R1.1.0_raw/sub*/model/lev2.gfeat/')

f = open(outfile, "w")
for file in list(all_feats):
  f.write("<p>============================================")
  f.write("<p>%s"%(file))
  f.write("<IMG SRC=\"%s/inputreg/masksum_overlay.png\">"%(file))
  f.write("<IMG SRC=\"%s/inputreg/maskunique_overlay.png\">"%(file))
f.close()
