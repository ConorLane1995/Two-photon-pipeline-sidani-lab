"""
Script to take the 2P output from recordings that were processed together, and split them into separate files.
INPUT: set every variable in ALL CAPS before the main method
OUTPUT: split files in separate folders defined in R1_FOLDER and R2_FOLDER
AUTHOR: Veronica Tarka, August 2022, veronica.tarka@mail.mcgill.ca
"""
import numpy as np
import shutil
import os 

COMBINED_FOLDER = "/media/vtarka/USB DISK/Lab/2P/244__246_247_248/" # folder where the Suite2P output for the combined recordings are

S1_FOLDER = "/media/vtarka/USB DISK/Lab/2P/Vid_244/"

E1_FOLDER = "/media/vtarka/USB DISK/Lab/2P/Vid_246/" # folder to save the split files for the first recording in
E1_TRIGGER_FILE = "TSeries-08192022-1257-246_Cycle00001_VoltageRecording_001.csv" # file name for the trigger CSV (should be within COMBINED_FOLDER)
E1_CONDITION_FILE = "ID112_190822_EvokedPreSal.mat" # file name for the .mat file with the condition labeling for every trial (should be within COMBINED_FOLDER)

E2_FOLDER = "/media/vtarka/USB DISK/Lab/2P/Vid_247/" # folder to save the split files for the second recording
E2_TRIGGER_FILE = "TSeries-08192022-1257-247_Cycle00001_VoltageRecording_001.csv" # file name for the trigger CSV (should be within COMBINED_FOLDER)
E2_CONDITION_FILE = "ID112_190822_EvokedPostSal.mat" # file name for the .mat file with the condition labeling for every trial (should be within COMBINED_FOLDER)

S2_FOLDER = "/media/vtarka/USB DISK/Lab/2P/Vid_248/"

JUNCTURE_FRAMES = [0,9001,16715,24400,33399]# frames where recording 1 stops and recording 2 begins
# JUNCTURE_FRAME is included in recording 2, JUNCTURE_FRAME-1 is included in recording 1

def main():
    # load our files that were generated by Suite2P and the stim files
    fluorescence_trace = np.load(COMBINED_FOLDER + "F.npy",allow_pickle=True) # uncorrected trace of dF/F
    neuropil_trace = np.load(COMBINED_FOLDER + "Fneu.npy",allow_pickle=True) # estimation of background fluorescence
    spks_trace = np.load(COMBINED_FOLDER+"spks.npy",allow_pickle=True)

    for folder in [S1_FOLDER,E1_FOLDER,E2_FOLDER,S2_FOLDER]:
        if not os.path.exists(folder):
            os.makedirs(folder)

    for frame_idx,folder in zip(range(len(JUNCTURE_FRAMES)-1),[S1_FOLDER,E1_FOLDER,E2_FOLDER,S2_FOLDER]):
        np.save(folder + "F.npy",fluorescence_trace[:,JUNCTURE_FRAMES[frame_idx]:JUNCTURE_FRAMES[frame_idx+1]])
        np.save(folder + "Fneu.npy",neuropil_trace[:,JUNCTURE_FRAMES[frame_idx]:JUNCTURE_FRAMES[frame_idx+1]])  
        np.save(folder + "spks.npy",spks_trace[:,JUNCTURE_FRAMES[frame_idx]:JUNCTURE_FRAMES[frame_idx+1]]) 

    # copy some of the shared files into the R1_FOLDER so you don't have to manually move them
    folders = [E1_FOLDER,E2_FOLDER]
    triggers = [E1_TRIGGER_FILE,E2_TRIGGER_FILE]
    conds = [E1_CONDITION_FILE,E2_CONDITION_FILE]

    for f,t,c in zip(folders,triggers,conds):
    
        shutil.copy(COMBINED_FOLDER+t,f+t) # copying the trigger file
        shutil.copy(COMBINED_FOLDER+c,f+c) # copying the trial labeling

        # copy the Suite2P files that don't need to be split
        shutil.copy(COMBINED_FOLDER+"ops.npy",f+"ops.npy")
        shutil.copy(COMBINED_FOLDER+"stat.npy",f+"stat.npy")
        shutil.copy(COMBINED_FOLDER+"iscell.npy",f+"iscell.npy")


if __name__=="__main__":
    main()