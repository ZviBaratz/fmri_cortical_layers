###THis scripts converts Dicom files to niftis and arranging them according to BIDS guidelines.
###Top level Dicom folder should be saved under 'Project_name/sourcedata/sub-XX'.
import os
import json
import csv
import glob
import subprocess
import pandas as pd
import shutil


TOP_LEVEL = r'C:/Users/Owner/Desktop/Cortical_Layers_fMRI'
TEMPLATE_PARTICIPANTS = r'C:\Users\Owner\Desktop\FSL_pipeline\bids-starter-kit-master\templates\participants.tsv'

# def BIDS_run(subnum,age,hand,sex, ):
    # project's folder
    #   age = '25'
    #   hand = 'right'
    #  sex = 'm'

class RunBids:
    def __init__(self, subnum: str, age: str, hand: str, sex: str, toplvl: str = TOP_LEVEL, temp_participants: str = TEMPLATE_PARTICIPANTS):
        self.age = age
        self.hand = hand
        self.sex = sex
        self.toplvl = toplvl
        self.temp_participants = temp_participants
        self.subnum = subnum


    def set_directories(self, subnum: str, toplvl:str):
        sub = 'sub-'+subnum
        new_toplvl = r'{0}\Nifti\sub-{1}'.format(toplvl,subnum) #Folder containing niftis after conversion, in which there will be anat and func subfolders.
        if not os.path.isdir(new_toplvl):
            os.makedirs(new_toplvl)
        derivatives = r'{0}\derivatives'.format(toplvl)
        if not os.path.isdir(derivatives):
            os.makedirs(derivatives)
        dcmdir= r'{0}\sourcedata\sub-{1}'.format(toplvl,subnum)
        ds_description = 'C:/Users/Owner/Desktop/FSL_pipeline/bids-starter-kit-master/templates/dataset_description.json' ##Please make sure there is a template dataset description available. this is the path to it.
        participants_tsv = '{0}/participants.tsv'.format(os.path.dirname(new_toplvl)) #.tsv file containing participans data
        dcm2niidir= 'C:/Users/Owner/Desktop/FSL_pipeline/mricrogl_windows/mricrogl/' #Path to the folder containing dcm2niix (!!)
        return [dcmdir,ds_description,participants_tsv,dcm2niidir,sub,new_toplvl]


    #Create nifti directory

    #if os.path.isdir('{0}/Nifti'.format(new_toplvl)) == False:
    #    os.mkdir('{0}/Nifti'.format(new_toplvl))
    #niidir='{0}/Nifti'.format(new_toplvl)

    ###Create dataset_description.json
    def dataset_description(self, new_toplvl: str,ds_description: str):
        Proj_Name = '"Cortical_Layers_fMRI"' #Define project name as it will be in the .json file
        replacements = {'proj_name': Proj_Name}
        if os.path.isfile('{0}/dataset_description.json'.format(os.path.dirname(new_toplvl))):
            with open(ds_description) as infile:
                with open('{0}/dataset_description.json'.format(os.path.dirname(new_toplvl)), 'w') as outfile:
                    for line in infile:
                        for src, target in replacements.items():
                            line = line.replace(src, target)
                        outfile.write(line)
        print('Created dataset_description.json')

    ###Create participants.tsv
    ###Define parameters to be included in the .tsv file (participants.tsv)

    def participants(self,sub: str, age: str, hand: str, sex: str, participant_tsv: str, temp_participants:str):
        if os.path.isfile(participant_tsv) == False:
            df = pd.read_csv(temp_participants)
        else:
            df = pd.read_csv(participant_tsv,sep = '\t')
        loc = int(sub[-2:])
        newline = [sub,age,hand,sex]
        df.loc[loc-1] = newline
        df.to_csv(participant_tsv, sep='\t', index=False)
        print('Created participants.tsv')

    # Create anat and func folder

    def create_anat(self, new_toplvl: str,dcmdir: str,dcm2niidir: str, subnum: str):
        if os.path.isdir(r'{0}\func'.format(new_toplvl)) == False:
            os.mkdir(r'{0}\func'.format(new_toplvl))
        if os.path.isdir(r'{0}\anat'.format(new_toplvl)) == False:
            os.mkdir(r'{0}\anat'.format(new_toplvl))

        ###Convert Dicom anat files to nii using dicm2niix

        anat_dir = glob.glob('{0}/*MPRAGE*'.format(dcmdir)) ##find all relevent anatomical scans
        cmd = '{0}dcm2niix -o {1} -f {2}_%f_%p {3}'.format(dcm2niidir,r'{0}\anat'.format(new_toplvl),subnum,anat_dir[0]) #declare the bash command
        cmd = cmd.replace('/',os.sep)
        subprocess.run(cmd) #Run

        ###Rename nii anat files
        ##Renaming all anat nii according to BIDS guidelines

        MPRAGE_files = glob.glob('{0}/anat/*MPRAGE*'.format(new_toplvl))
        for file in MPRAGE_files:
            file_list = file.split('/')
            MP_hdr = file_list[-1].split('.')
            MP_hdr[0] = 'sub-{0}_T1w'.format(subnum)
            T1w_hdr = '.'.join(MP_hdr)
            shutil.move(file, '{0}/anat/{1}'.format(new_toplvl,T1w_hdr))
        print('Converted MPRAGE files from {0} to {1}'.format(anat_dir[0],r'{0}\anat'.format(new_toplvl)))
    ###Convert Dicom func files to nii using dicm2niix

    def create_func(self,dcmdir: str,dcm2niidir: str,new_toplvl: str,subnum: str):
        all_files= glob.glob('{0}/*'.format(dcmdir)) ##find all relevent functional scans
        func_files = list()
        for file in all_files: #remove SBref files
            if 'Motor' in file or 'Sensor' in file or 'Sensory' in file:
                func_files.append(file)
                if 'SBRef' in file:
                    func_files.remove(file)
        for file in func_files:
            cmd = '{0}dcm2niix -o {1} -f {2}_%f_%p {3}'.format(dcm2niidir, r'{0}\func'.format(new_toplvl), subnum, file) #declare the bash command
            cmd = cmd.replace('/',os.sep)
            subprocess.run(cmd) #Run

        ###Rename nii func files
        ##Renaming all func nii according to BIDS guidelines, ***please edit in order to match the template of your original dicom files***

    def rename_func_file(self, new_toplvl: str,subnum: str,dcmdir: str):
        func_files = glob.glob('{0}/func/*[Gre|IR|SE]*[Motor|Sensor|Sensory].*[!v]'.format(new_toplvl))
        for file in func_files: #remove SBref files
            if 'Sensor' in file and 'Sensory' not in file:
                fixed_f = file.replace('Sensor','Sensory')
                os.rename(file,fixed_f)
        func_files = glob.glob('{0}/func/*[Gre|IR|SE]*[Motor|Sensory].*[!v]'.format(new_toplvl))
        for file in func_files:
            file_list = file.split('/')
            file_no_path = file_list[-1]
            func_data = file_no_path.split('_')
            func_type = func_data[-1].split('.')
            if 'IR' in file:
                scan_type = func_data[2].replace('-','')
                new_func = 'sub-{0}_task-{1}_acq-{2}{3}_bold'.format(subnum,func_type[0],scan_type,func_data[-2])
                func_type[0] = new_func
                shutil.move(file, '{0}/func/{1}'.format(new_toplvl, ".".join(func_type)))
            if 'Gre' in file:
                new_func = 'sub-{0}_task-{1}_acq-{2}_bold'.format(subnum,func_type[0],func_data[2])
                func_type[0] = new_func
                shutil.move(file, '{0}/func/{1}'.format(new_toplvl, ".".join(func_type)))
        print('Converted functional Dicom files from {0} to {1}'.format(dcmdir,r'{0}\func'.format(new_toplvl)))

    def check_func_conversion(self,new_toplvl: str):
        func_files = glob.glob('{0}/func/*'.format(new_toplvl))
        for f in func_files:
            if 'FLAIR' in f:
                os.remove(f)

        ###Modify .json files
    ###Adding task names, as required by BIDS format


    def modify_json(self, new_toplvl: str):
        json_files = glob.glob('{0}/func/*.json'.format(new_toplvl))
        for file in json_files:
            with open(file, 'r+') as f:
                data = json.load(f)
                if 'Motor' in file:
                    data['TaskName'] = 'Motor'
                elif 'Sensory' in file or 'Sensor' in file:
                    data['TaskName'] = 'Sensory'
                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()

    ###Create .tsv events files
    ###Creating or adding to .tsv events file, describing the onsets of each task.

    def create_onsets(self, new_toplvl: str):
        onset_files = glob.glob('{0}/func/*.tsv'.format(new_toplvl))
        for file in onset_files:
            if os.path.isfile(file) == False:
                with open(file, 'wt') as tsvfile:
                    fieldnames = ['onset','duration','trial_type','response_time','stim_file','HED']
                    writer = csv.writer(tsvfile, delimiter = '\t')
                    writer.writerow(fieldnames)

            with open(file, 'r') as tsvfile:
                reader = csv.reader(tsvfile, delimiter = '\t')
                lines = list(reader)
                lines.append(['15','15','n/a','0','n/a','n/a'])
                lines.append(['45','15','n/a','0','n/a','n/a'])
                lines.append(['75','15','n/a','0','n/a','n/a'])
                lines.append(['105','15','n/a','0','n/a','n/a'])

            with open(file, 'w') as tsvfile:
                writer = csv.writer(tsvfile, delimiter = '\t')
                writer.writerows(lines)

    def run(self):

        [dcmdir, ds_description, participants_tsv, dcm2niidir, sub, new_toplvl] = self.set_directories(self.subnum,
                                                                                                 toplvl=self.toplvl)
        self.dataset_description(new_toplvl=new_toplvl, ds_description=ds_description)
        self.participants(sub=sub, age=self.age, hand=self.hand, sex=self.sex, participant_tsv=participants_tsv, temp_participants=self.temp_participants)
        self.create_anat(new_toplvl=new_toplvl, dcmdir=dcmdir, dcm2niidir=dcm2niidir, subnum=self.subnum)
        self.create_func(dcmdir=dcmdir, dcm2niidir=dcm2niidir, new_toplvl=new_toplvl, subnum=self.subnum)
        self.rename_func_file(new_toplvl=new_toplvl, subnum=self.subnum, dcmdir=dcmdir)
        self.check_func_conversion(new_toplvl=new_toplvl)
        self.modify_json(new_toplvl=new_toplvl)
        self.create_onsets(new_toplvl =new_toplvl)
