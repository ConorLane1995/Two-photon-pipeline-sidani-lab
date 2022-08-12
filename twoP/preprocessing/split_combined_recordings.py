"""
Script to take the 2P output from recordings that were processed together, and split them into separate files.
INPUT: TODO
OUTPUT: TODO
AUTHOR: Veronica Tarka, August 2022, veronica.tarka@mail.mcgill.ca
"""

import numpy as np

BASE_PATH = "/media/vtarka/USB DISK/Lab/2P/217_220_combined/"

def main():
    # load our files that were generated by Suite2P and the stim files
    fluorescence_trace = np.load(BASE_PATH + "F.npy",allow_pickle=True) # uncorrected trace of dF/F
    neuropil_trace = np.load(BASE_PATH + "Fneu.npy",allow_pickle=True) # estimation of background fluorescence
    stimulus = np.genfromtxt(BASE_PATH + "TSeries-07052022-1312-217_Cycle00001_VoltageRecording_001.csv",delimiter=',',skip_header=True) # voltage values of the trigger software over the recording
    
    juncture_frame = round(len(stimulus)/100*10)

    Fluo222 = fluorescence_trace[:,:juncture_frame]
    Fluo226 = fluorescence_trace[:,juncture_frame:]

    Fneu222 = neuropil_trace[:,:juncture_frame]
    Fneu226 = neuropil_trace[:,juncture_frame:]

    np.save(BASE_PATH + "Vid_217s/F.npy",Fluo222)
    np.save(BASE_PATH + "Vid_217s/Fneu.npy",Fneu222)

    np.save(BASE_PATH + "Vid_220s/F.npy",Fluo226)
    np.save(BASE_PATH + "Vid_220s/Fneu.npy",Fneu226)

if __name__=="__main__":
    main()