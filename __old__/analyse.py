from numpy import *
from astropy.io import fits
import os
from utils import *
from multiprocessing import Pool

##################################
input_path = 'H:/Lab_Project/OSSOS/dbimages/Triplets'
save_results_in = "./results/"
##################################

if __name__ == '__main__':

    # Getting input files
    if os.path.isfile(input_path):
        triplets = [input_path]
    elif os.path.isdir(input_path):
        triplets = []
        for path, currentDirectory, files in os.walk(input_path):
            for file in files:
                if file[-9:] == "p.fits.fz" and file[-10].isdigit():
                    triplets.append(os.path.join(path, file))
    else:
        print("Unable to find the input file or directory")
        exit()

    # Treatment of each file
    lenTriplets = len(triplets)
    for j,triplet in enumerate(triplets):
        numTriplet = os.path.split(triplet)[-1].replace("p.fits.fz","")
        print(f"Analyzing triplet {numTriplet}, {j+1}/{lenTriplets}")

        # Reading data from fits.fz file
        hdul = fits.open(triplet)
        #print(hdul.info())
        sizeX, sizeY = hdul[1].data.shape

        ccds = empty([len(hdul)-1,sizeX,sizeY])
        ccds_background = empty([len(hdul)-1,sizeX,sizeY])

        args = []
        for i in range(len(hdul)-1):
            ccds[i] = hdul[i+1].data
            args.append((i, ccds[i], len(ccds), False, "   "))

        print("   Computing sky background...")
        print(f"   [{' '*(term_size-10)}]",end="\r")
        cores = min(len(ccds),CPUcount)
        with Pool(cores) as p: ccds_background = p.starmap(mp_sky_backgroud,args) # Computing all ccd's sky background and put hem in the good order
        if stop == True: exit()
        print(f"   [{'='*(term_size-10)}]100%")
        ccds_background.sort(key=lambda x: x[0])
        ccds_background = array([bg[1] for bg in ccds_background])                                         # Removing th indexes

        args = []
        path = f"{save_results_in}/Triplets/{numTriplet}"
        save_ccd_as_png(ccds[0],"test.png")
        save_ccd_as_png(ccds_background[0],"test_background.png")
        for i in range(len(ccds)):
            args.append((path,i,ccds[i],ccds_background[i],len(ccds)))
        print("   Saving results...")
        print(f"   [{' '*(term_size-10)}]",end="\r")
        with Pool(cores) as p: p.starmap(mp_save_ccd,args)
        if stop == True: exit()
        print(f"   [{'='*(term_size-10)}]100%")

        


    
