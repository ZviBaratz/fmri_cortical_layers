import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import glob
import os
from sklearn import preprocessing


## s = fixed ts
## x = normalized ts


class CalcMeanTS:
    def __init__(self, path: str = r'C:/Users/Owner/Desktop/Cortical_Layers_fMRI'):
        self.path = '{0}/derivatives/tsplots/mean_ts'.format(path)

    def calc_ts_properties(self,path: str):
        ts_files = glob.glob('{0}/*/*all_ts.txt'.format(path))
        for f in ts_files:
            ts = pd.read_csv(f, header=0, sep=',')
            new_f = f.replace('all_ts','fixed_ts')
            all_subjects_norm_bold = f.replace('all_ts','subjects_norm_BOLD_response')
            norm_f = f.replace('all_ts','normalized_ts')
            mean_f = f.replace('all_ts','mean_normalized_ts')
            mean_r_f = f.replace('all_ts','mean_ts')
            mean_b_f = f.replace('all_ts','mean_norm_bold_response')
            mean_real_b = f.replace('all_ts','mean_bold_response')
            if 'Gre' in f:
                s12 = pd.concat([ts['sub-01'], ts['sub-04']],axis=1)
                s12 = s12[7:90]
                s12 = s12.reset_index(drop=True)
                s34 = pd.concat([ts['sub-02'], ts['sub-03']],axis=1)
                s34 = s34[0:83]
                s34 = s34.reset_index(drop=True)
                s = pd.concat([s12,s34],axis=1)
                headers = list(s.columns.values)
                x = s.values
                min_max_scaler = preprocessing.MinMaxScaler()
                x_scaled = min_max_scaler.fit_transform(x)
                x = pd.DataFrame(x_scaled)
            elif 'IREPITI' in f:
                if 'sub-01' in ts.keys() and 'sub-04' in ts.keys():
                    s12 = pd.concat([ts['sub-01'], ts['sub-04']], axis=1)
                    s34 = pd.concat([ts['sub-02'], ts['sub-03']], axis=1)
                elif 'sub-01' not in ts.keys() and 'sub-04' in ts.keys():
                    s12 = ts['sub-04']
                    s34 = ts['sub-03']
                s12 = s12[3:45]
                s12 = s12.reset_index(drop=True)
                s34 = s34[0:42]
                s34 = s34.reset_index(drop=True)
                s = pd.concat([s12, s34], axis=1)
                headers = list(s.columns.values)
                x = s.values
                min_max_scaler = preprocessing.MinMaxScaler()
                x_scaled = min_max_scaler.fit_transform(x)
                x = pd.DataFrame(x_scaled)
            x_mean = x.mean(axis=1)
            h = f.split('_')[-4]
            s.mean(axis=1).to_csv(mean_r_f,header=[h],mode='w',index=False,line_terminator=os.linesep)
            s.to_csv(new_f, header=True, mode='w', index=False, line_terminator=os.linesep)
            x.to_csv(norm_f,header = headers,mode ='w',index=False,line_terminator=os.linesep)
            x_mean.to_csv(mean_f,header = [h],mode ='w',index=False,line_terminator=os.linesep)
            if 'Gre' in f:
                rel_mean = x_mean[1:81]
                non_norm_m = s.mean(axis=1)[1:81]
                skip = 20
            else:
                rel_mean = x_mean[1:41]
                non_norm_m = s.mean(axis=1)[1:41]
                skip = 10
            m_l = list()
            n_m_l = list()
            j = 0
            for i in range(4):
                m_l.append(rel_mean[j:j+skip])
                n_m_l.append(non_norm_m[j:j+skip])
                j+=skip
            real_mb = np.array(n_m_l)
            real_mb = pd.DataFrame(real_mb.mean(axis=0))
            real_mb.to_csv(mean_real_b,header=[h], mode='w',index=False,line_terminator=os.linesep)
            mean_bold = np.array(m_l)
            pd.DataFrame(mean_bold).to_csv(all_subjects_norm_bold,mode='w',index=False,line_terminator=os.linesep)
            mean_bold = pd.DataFrame(mean_bold.mean(axis=0))
            mean_bold.to_csv(mean_b_f,header=[h], mode='w',index=False,line_terminator=os.linesep)

    def calculate_subjects_mean_bold(self, path: str):
        ts_files = glob.glob('{0}/*/*bold_normalized_ts.txt'.format(path))
        for f in ts_files:
            df = pd.read_csv(f)
            if 'Gre' in f:
                relevant = df[1:81]
                BOLD_duration = 20
            else:
                relevant = df[1:41]
                BOLD_duration = 10
            iterables = [['First','Second','Third','Fourth'],np.arange(BOLD_duration).tolist()]
            index = pd.MultiIndex.from_product(iterables,names=['Action','Time'])
            mean_bold_df = pd.DataFrame(relevant.values,index = index,columns= relevant.columns)
            mean_bold_df = mean_bold_df.mean(level = 'Time')
            mean_bold_df.to_csv(f.replace('normalized_ts','subjects_norm_BOLD_response'),mode='w',index =False,line_terminator=os.linesep)

    def run(self):
        self.calc_ts_properties(path=self.path)
        self.calculate_subjects_mean_bold(path=self.path)
