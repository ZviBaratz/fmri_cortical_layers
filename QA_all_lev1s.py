# Basically, I'm using python to create a text file with a huge command in it and then we run it.

import os
import glob


# We will start with the registration png files
class qa_lev1_analysis:
  def __init__(self,path: str = r'C:/Users/Owner/Desktop/Cortical_Layers_fMRI'):
    self.outfile = r'{0}/derivatives/scripts/lev1_QA.html'.format(path)
    self.all_feats = glob.glob(r'{0}/derivatives/feats/*/sub*.feat'.format(path))

  def QA_lev1(self,outfile: str, all_feats: list):
    if os.path.isfile(outfile):
      os.remove(outfile)

    f = open(outfile, "w")
    for file in list(all_feats):
      f.write("<p>============================================")
      f.write("<p>%s"%(file))
      f.write("<IMG SRC=\"%s/design.png\">"%(file))
      f.write("<IMG SRC=\"%s/design_cov.png\" >"%(file))
      f.write("<IMG SRC=\"%s/mc/disp.png\">"%(file))
      f.write("<IMG SRC=\"%s/mc/trans.png\" >"%(file))
      f.write("<p><IMG SRC=\"%s/reg/example_func2highres.png\" WIDTH=1200>"%(file))
      f.write("<p><IMG SRC=\"%s/reg/example_func2standard.png\" WIDTH=1200>"%(file))
      f.write("<p><IMG SRC=\"%s/reg/highres2standard.png\" WIDTH=1200>"%(file))
    f.close()

  def run(self):
    self.QA_lev1(outfile=self.outfile, all_feats=self.all_feats)