import glob
import os
import pandas as pd


class Get_TS:
    def __init__(self, path: str=r'C:/Users/Owner/Desktop/Cortical_Layers_fMRI'):
        self.path = r'{0}/derivatives/tsplots'.format(path)
        self.subjects = glob.glob('{0}/sub*'.format(self.path))
        self.tsplots = glob.glob('{0}/*/*bold'.format(self.path))

    def gather(self, path: str, subjects: list, tsplots: list):
        prots = []
        for tsplot in tsplots:
            prots.append(tsplot.split(os.sep)[-1])
        prots = list(set(prots))
        for prot in prots:
            if os.path.isdir('{0}/mean_ts/{1}'.format(path,prot)) == False:
                os.makedirs('{0}/mean_ts/{1}'.format(path,prot))
        for prot in prots:
            header = list()
            for subj in subjects:
                subject = subj.split(os.sep)[-1]
                if os.path.isdir('{0}/{1}'.format(subj,prot)):
                    infile = pd.read_csv('{0}/{1}/tsplot/tsplotc_zstat1.txt'.format(subj, prot), header=None, sep=' ')
                    col = infile.iloc[:,0]
                    header.append(subject)
                    if os.path.isfile('{0}/mean_ts/{1}/{1}_all_ts.txt'.format(path,prot)):
                        outfile = pd.read_csv('{0}/mean_ts/{1}/{1}_all_ts.txt'.format(path,prot),header=0,sep=',')
                        new_outfile = outfile.join(col)
                    else:
                        new_outfile = col
                    new_outfile.to_csv('{0}/mean_ts/{1}/{1}_all_ts.txt'.format(path,prot),header=header,mode='w',index = False,line_terminator=os.linesep)

    def run(self):
        self.gather(path=self.path, subjects=self.subjects, tsplots=self.tsplots)

