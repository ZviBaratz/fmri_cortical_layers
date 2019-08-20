# This script will generate each subjects design.fsf, but does not run it.
# It depends on your system how will launch feat

import os
import glob
import platform

is32bit = platform.architecture()[0] == "32bit"
system32 = os.path.join(
os.environ["SystemRoot"], "SysNative" if is32bit else "System32")
bash = os.path.join(system32, "bash.exe")


class FsfsFirstLevel:
    def __init__(self, path: str = r"C:/Users/Owner/Desktop/Cortical_Layers_fMRI"):
        self.path = r'{0}/Nifti'.format(path)
        self.output_path = r"{0}/derivatives/feats".format(path)
        # Set this to the directory all of the sub### directories live in

        # Set this to the directory where you'll dump all the fsf files
        # May want to make it a separate directory, because you can delete them all o
        #   once Feat runs
        self.fsfdir = r"{0}/scripts/fsfs".format(os.path.dirname(self.output_path))
        self.subdirs = glob.glob(r"{0}/*/func/sub*.nii".format(self.path))

    def create_fsfdir(self, fsfdir: str):
        if os.path.isdir(fsfdir) == False:
            os.mkdir(fsfdir)

    # Get all the paths!  Note, this won't do anything special to omit bad subjects

    def create_fsfs(self, subdirs: list,path: str, output_path: str, fsfdir: str):
        for dir in list(subdirs):
            splitdir = dir.split(os.sep)
            # YOU WILL NEED TO EDIT THIS TO GRAB sub001
            splitdir_sub = splitdir[-3]
            if os.path.isdir("{0}/{1}".format(output_path, splitdir_sub)) == False:
                os.makedirs(r"{0}/{1}".format(output_path, splitdir_sub))
            prot_title = splitdir[-1]
            outdir = r"{0}/{1}/{2}".format(output_path, splitdir_sub, prot_title[:-4])
            outdir = outdir.replace("C:", "/mnt/c")
            outdir = outdir.replace(os.sep, "/")
            if "Gre" in prot_title:
                TE = "30"
                DOF = "BBR"
                stand_DOF = "12"
                TR = "1.5"
                IMG_size = "18311040"
            elif "IR" in prot_title:
                TE = "28"
                DOF = "7"
                stand_DOF = "12"
                TR = "3"
                IMG_size = "4577760"
            if "Motor" in prot_title:
                Action = "Motor"
            elif "Sensory" in prot_title:
                Action = "Sensory"

            struct_file = os.path.join(
                path, splitdir_sub, "anat", "{0}_T1w_brain.nii.gz".format(splitdir_sub)
            )
            struct_file = struct_file.replace("C:", "/mnt/c")
            struct_file = struct_file.replace(os.sep, "/")
            FEAT_dir = dir[:-4]
            FEAT_dir = FEAT_dir.replace("C:", "/mnt/c")
            FEAT_dir = FEAT_dir.replace(os.sep, "/")
            con_file = os.path.join(
                path,
                splitdir_sub,
                "func",
                "motion_assess",
                "{0}_motion_assess".format(prot_title[:-4]),
            )
            con_file = os.path.join(con_file, "confound.txt")
            con_file = con_file.replace("C:", "/mnt/c")
            con_file = con_file.replace(os.sep, "/")
            events = "{0}{1}{2}{1}events.txt".format(output_path, os.sep, splitdir_sub)
            f = open(events, "w")
            if "sub-02" in splitdir_sub or "sub-03" in splitdir_sub:
                L = ["7 15 1\n", "37 15 1\n", "67 15 1\n", "97 15 1\n"]
            else:
                L = ["15 15 1\n", "45 15 1\n", "75 15 1\n", "105 15 1\n"]
            f.writelines(L)
            f.close()
            events = events.replace("C:", "/mnt/c")
            events = events.replace(os.sep, "/")
            #  YOU WILL ALSO NEED TO EDIT THIS TO GRAB THE PART WITH THE RUNNUM
            tdir = dir.replace("C:", "/mnt/c")
            tdir = tdir.replace(os.sep, "/")
            ntime = os.popen('%s -lc "fslnvols %s"' % (bash, tdir)).read().rstrip()
            replacements = {
                "NTPTS": ntime,
                "outdir": outdir,
                "cur_TE": TE,
                "cur_TR": TR,
                "FEAT_dir": FEAT_dir,
                "cur_con": con_file,
                "IMG_size": IMG_size,
                "struct_file": struct_file,
                "cur_DOF": DOF,
                "cur_Action": Action,
                "cur_stand_DOF": stand_DOF,
                "events_txt": events,
            }  # , 'RUNNUM':runnum
            if os.path.isdir("{0}/lev1".format(fsfdir)) == False:
                os.mkdir("{0}/lev1".format(fsfdir))
            with open("{0}/template_lev1.fsf".format(fsfdir)) as infile:
                with open(
                        "{0}/lev1/design_{1}.fsf".format(fsfdir, prot_title[:-4]), "w"
                ) as outfile:  # runnum
                    for line in infile:
                        for src, target in replacements.items():
                            line = line.replace(src, target)
                        outfile.write(line)
            print('create fsf for {0}'.format(prot_title[:-4]))

    def run(self):
        self.create_fsfdir(fsfdir=self.fsfdir)
        self.create_fsfs(subdirs=self.subdirs,path = self.path,output_path=self.output_path,fsfdir=self.fsfdir)