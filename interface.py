"""
This file allow to connect this program with different type of data classification system.
You can edit it in order to allow the program to treat your data.

This file must contain at leat the following functions:
- connectData : allow to create objects with basic informations (id, path to data)
- getBlock, getTriplet, getShot, getCCD : allow to fill all the informations of the object using the basic information already available in these objects

All the data cannot be stored entirely in the RAM, so each object will load data when needed by using these get functions.
"""

##################################################
DATA_ROOT = "D:/Lab_Project/OSSOS/dbimages/Triplets"
DATA_LIST = "rsrc/All_triplets"
OUTPUT = "D:/Lab_Project/results/"
##################################################

from classes.block import Block
from classes.triplet import Triplet
from classes.shot import Shot
from classes.ccd import CCD
from classes.rate import Rate
import os
from astropy.io import fits
from numpy import *
from utils.term import *
import re
from scipy.optimize import curve_fit

#    _____      _      ____  _     _           _         _      _     _   
#   / ____|    | |    / __ \| |   (_)         | |       | |    (_)   | |  
#  | |  __  ___| |_  | |  | | |__  _  ___  ___| |_ ___  | |     _ ___| |_ 
#  | | |_ |/ _ \ __| | |  | | '_ \| |/ _ \/ __| __/ __| | |    | / __| __|
#  | |__| |  __/ |_  | |__| | |_) | |  __/ (__| |_\__ \ | |____| \__ \ |_ 
#   \_____|\___|\__|  \____/|_.__/| |\___|\___|\__|___/ |______|_|___/\__|
#                                _/ |                                     
#                               |__/                                     
                                       
def connectData(verbose=False):
    """This function allow to create instances of all objects that will be used by the program. These informations can be incomplete (only containing the name/id of each object)"""
    reading = ""

    # Reading All_triplets file
    with open(DATA_LIST) as file:

        if verbose == True: print("Scanning data...",end="\r")
        if verbose == 2:    print("Scanning data...")

        for line in file:
            if line == "\n":
                continue

            #__________________________________________________
            # Reading headers (blocks and triplets)

            if "#" in line:

                if line[1:-5] not in Block.all:
                    currentBlock = Block(id=line[1:-5])

                    if verbose == 2: print(f"   Block {line[1:-5]}")

                else: currentBlock = Block.all[line[1:-5]] # Just to be sure to have the correct block

                currentTriplet = Triplet(id=line[1:-1], block=currentBlock)
                currentBlock.tripletList.append(currentTriplet)

                if verbose == 2: print(f"      Triplet {line[1:-1]}")
            
            # __________________________________________________
            # Reading all shots and associated CCDs

            else:
                currentShot = Shot(id=line[:-1].replace(" ",""),triplet=currentTriplet,block=currentBlock, dataPath=os.path.join(DATA_ROOT,str(int(line[:-1]))))

                for i in os.listdir(currentShot.dataPath):
                    path = os.path.join(currentShot.dataPath,i)

                    if os.path.isdir(path) and i[:3] == "ccd":
                        currentShot.ccdList.append(CCD(id=i[3:], dataPath=path, shot=currentShot, triplet=currentShot.triplet, block=currentShot.block))

                currentTriplet.shotList.append(currentShot)

                if verbose == 2: print(f"         Shot {line[:-1]} with {len(currentShot.ccdList)} CCDs")
    
    if verbose == True: print("Scanning data... Done")
    if verbose: print(f"-> Found {len(Block.all)} blocks, {len(Triplet.all)} triplets, {len(Shot.all)} shots and {len(CCD.all)} CCDs")

    

#    _____                      _      _          ____  _     _           _       
#   / ____|                    | |    | |        / __ \| |   (_)         | |      
#  | |     ___  _ __ ___  _ __ | | ___| |_ ___  | |  | | |__  _  ___  ___| |_ ___ 
#  | |    / _ \| '_ ` _ \| '_ \| |/ _ \ __/ _ \ | |  | | '_ \| |/ _ \/ __| __/ __|
#  | |___| (_) | | | | | | |_) | |  __/ ||  __/ | |__| | |_) | |  __/ (__| |_\__ \
#   \_____\___/|_| |_| |_| .__/|_|\___|\__\___|  \____/|_.__/| |\___|\___|\__|___/
#                        | |                                _/ |                  
#                        |_|                               |__/                                                                                                                                                                                                                        

# OPTIONAL
def loadBlock(block):
    """This function use the informations contained in the block object to find the corresponding data and fill the missing parts"""
    return block

# OPTIONAL
def loadTriplet(triplet):
    """This function use the informations contained in the triplet object to find the corresponding data and fill the missing parts"""
    path = "H:/Lab_Project/Triplets/Split_triplets"
    for shot in triplet.shotList:
        for file in os.listdir(path):
            if shot.id in file:
                ft, fs = get_params_from_fake_objects(f"{path}/{file}")
                triplet.rates.append(Rate(parent=triplet, func = "tan", a=ft[0], b=ft[1], c=ft[2], d=ft[3]))
                triplet.rates.append(Rate(parent=triplet, func = "square", a=fs[0], b=fs[1], c=fs[2], d=fs[3]))
                return triplet
    return triplet

# CUSTOM
def get_params_from_fake_objects(file):
    detected = []
    undetected = []
    with open(file,"r") as f:
        cpt = 0
        for line in f:
            cpt += 1
            if line.startswith("#"): continue
            data = line.split()
            if data[2] == "mag": continue
            try:
                if data[7] in ["--","0.000"]: 
                    undetected.append(float(data[2]))
                else: detected.append(float(data[2]))
            except:
                print("Error in file",file,"line",cpt)
                print(line)
                raise

    detected = array(detected)
    undetected = array(undetected)

    m,step = linspace(21,25.5,50, retstep=True)

    eff = empty_like(m)

    for i,x in enumerate(m):
        numDetected = sum((x - step/2 <= detected) * (detected < x + step/2))
        numUndetected = sum((x - step/2 <= undetected) * (undetected < x + step/2))
        if numDetected + numUndetected == 0: eff[i] = 0
        else: eff[i] = numDetected / (numDetected + numUndetected)

    def ft(m,a,b,c,d):
        return a/4 * (1-tanh((m-b)/c)) * (1-tanh((m-b)/d))

    def fs(m,a,b,c,d):
        return (a-b*(m-21)**2) / (1+exp((m-c)/d))

    param = [0.5,21,0.5,0.5]
    paramft = curve_fit(ft,m,eff,param)

    param = [0.5,0.5,21,0.5]
    paramfs = curve_fit(fs,m,eff,param)

    return paramft[0], paramfs[0]


# OPTIONAL
def loadShot(shot, verbose=False, prefix=""):
    """This function use the informations contained in the shot object to find the corresponding data and fill the missing parts"""
    try: hdul = fits.open(os.path.join(shot.dataPath,f"{shot.id}p.fits.fz"))
    except FileNotFoundError: hdul = fits.open(os.path.join(shot.dataPath,f"{shot.id}p.fits"))

    if verbose: print(f"{prefix}Getting data for shot {shot.id}...")    
    for i in range(len(hdul)-1):
        if verbose: progressbar(i/(len(hdul)-2),prefix=f"{prefix}   ")
        for ccd in shot.ccdList:
            if i == int(ccd.id):
                ccd.data = hdul[i+1].data
    for ccd in shot.ccdList:
        try: loadCCD(ccd)
        except TypeError as e:
            print("CCD :",ccd.id)
            raise e
    return shot

# OPTIONAL
def loadCCD(ccd):
    """This function use the informations contained in the CCD object to find the corresponding data and fill the missing parts"""

    if ccd.data is None:
        try: hdul = fits.open(os.path.join(ccd.shot.dataPath,f"{ccd.shot.id}p.fits.fz"))
        except FileNotFoundError: hdul = fits.open(os.path.join(ccd.shot.dataPath,f"{ccd.shot.id}p.fits"))
        for i in range(len(hdul)-1):
            if i == int(ccd.id):
                ccd.data = hdul[i].data

    ccd.fwhm = float(loadtxt(os.path.join(ccd.dataPath,f"{ccd.uid}.fwhm")))
    # print("fwhm:",ccd.fwhm,type(ccd.fwhm))
    apcor = loadtxt(os.path.join(ccd.dataPath,f"{ccd.uid}.apcor"))
    ccd.apcor_inner_radius = float(apcor[0])
    ccd.apcor_outer_radius = float(apcor[1])
    ccd.apcor_factor       = float(apcor[2])
    ccd.apcor_uncertainty  = float(apcor[3])
    # print("apcor:", ccd.apcor_inner_radius, ccd.apcor_outer_radius, ccd.apcor_factor, ccd.apcor_uncertainty,type(ccd.apcor_inner_radius))
    ccd.zeropoint = float(loadtxt(os.path.join(ccd.dataPath,f"{ccd.uid}.zeropoint.used")))
    # print("zeropoint:",ccd.zeropoint,type(ccd.zeropoint))
    ccd.trans_mat = loadtxt(os.path.join(ccd.dataPath,f"{ccd.uid}.trans.jmp"))
    # print("trans_mat:",ccd.trans_mat,type(ccd.trans_mat))
    return ccd

#   _______        _     _____        _           _____                _     _                        
#  |__   __|      | |   |  __ \      | |         / ____|              (_)   | |                       
#     | | ___  ___| |_  | |  | | __ _| |_ __ _  | |     ___  _ __  ___ _ ___| |_ ___ _ __   ___ _   _ 
#     | |/ _ \/ __| __| | |  | |/ _` | __/ _` | | |    / _ \| '_ \/ __| / __| __/ _ \ '_ \ / __| | | |
#     | |  __/\__ \ |_  | |__| | (_| | || (_| | | |___| (_) | | | \__ \ \__ \ ||  __/ | | | (__| |_| |
#     |_|\___||___/\__| |_____/ \__,_|\__\__,_|  \_____\___/|_| |_|___/_|___/\__\___|_| |_|\___|\__, |
#                                                                                                __/ |
#                                                                                               |___/

if __name__ == "__main__":
    connectData(verbose=False)

    files_to_check = [
        "fwhm",
        "apcor",
        "zeropoint.used",
        "trans.jmp"
    ]
    list_dest = "D:/Lab_Project/incomplet/" # destination of the lists of incompelte ccds
    ccd_dest = "D:/Lab_Project/incomplet/ccds/" # new location for incomplet ccd
    ccd_dest2 = "D:/Lab_Project/incomplet/blockH/" # new location for incomplet ccd

    count = zeros(len(files_to_check))
    incomplet = []
    incomplet_triplet = []
    incomplet_block = []

    for ext in files_to_check:
        if os.path.isfile(os.path.join(list_dest,ext+"_list.txt")): os.remove(os.path.join(list_dest,ext+"_list.txt")) 

    for ccd in CCD.all.values():
        for i, ext in enumerate(files_to_check):
            if not os.path.isfile(os.path.join(ccd.dataPath,f"{ccd.shot.id}p{ccd.id}.{ext}")):
                if ccd not in incomplet: incomplet.append(ccd)
                if ccd.triplet not in incomplet_triplet: incomplet_triplet.append(ccd.triplet)
                if ccd.block not in incomplet_block: incomplet_block.append(ccd.block)
                with open(os.path.join(list_dest,ext+"_list.txt"),"a") as file: file.write(ccd.uid + "\n")
                print(f"{ccd.triplet.id}" + os.path.join(ccd.dataPath,f"{ccd.shot.id}p{ccd.id}.{ext}"))
                count[i] += 1

    for ccd in incomplet:
        print("Removed ccd",ccd.id)
        if ccd.block.id == "14BH":
            print(f"H : {ccd.block.id}")
            if not os.path.isdir(os.path.join(ccd_dest2,ccd.shot.id)): os.makedirs(os.path.join(ccd_dest2,ccd.shot.id))
            os.rename(ccd.dataPath, os.path.join(ccd_dest2,ccd.shot.id,"ccd" + ccd.id))
        else:
            print(f"NOT H : {ccd.block.id}")
            if not os.path.isdir(os.path.join(ccd_dest,ccd.shot.id)): os.makedirs(os.path.join(ccd_dest,ccd.shot.id))
            os.rename(ccd.dataPath, os.path.join(ccd_dest,ccd.shot.id,"ccd" + ccd.id))
        

    # for i, ext in enumerate(files_to_check):
    #     print(f"Found {count[i]} incomplet CCDs in {len(incomplet_triplet)} triplets in {len(incomplet_block)}")
    
    print(f"Found {count[i]} incomplet CCDs in {len(incomplet_triplet)} triplets in {len(incomplet_block)} blocks")