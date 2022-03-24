"""
This file allow to connect this program with different type of data classification system.
You can edit it in order to allow the program to treat your data.

This file must contain at leat the following functions:
- connectData : allow to create objects with basic informations (id, path to data)
- getBlock, getTriplet, getShot, getCCD : allow to fill all the informations of the object using the basic information already available in these objects

All the data cannot be stored entirely in the RAM, so each object will load data when needed by using these get functions.
"""

##################################################
DATA_ROOT = "D:/Lab Project/OSSOS/dbimages/Triplets"
DATA_LIST = "rsrc/All_triplets"
##################################################

from block import Block
from triplet import Triplet
from shot import Shot
from ccd import CCD
import os
from astropy.io import fits

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
        for line in file:
            if line == "\n":
                continue

            #__________________________________________________
            # Reading headers (blocks and triplets)

            if "#" in line:
                
                # If the block doesn't contain information about the triplets
                if "block" in line:
                    reading = "messy_block"
                    currentBlock = Block(id=line[1:-7])
                    if verbose: print(f"Messy block {line[1:-7]}")

                # If the shots are organised by triplets
                else:
                    reading = "triplet"
                    if line[1:-5] not in Block.all:
                        currentBlock = Block(id=line[1:-5])
                        if verbose: print(f"Block {line[1:-5]}")
                    else: currentBlock = Block.all[line[1:-5]] # Just to be sure to have the correct block

                    currentTriplet = Triplet(id=line[1:-1], block=currentBlock)
                    currentBlock.triplets.append(currentTriplet)
                    if verbose: print(f"   Triplet {line[1:-1]}")
                continue
            
            # __________________________________________________
            # Reading all shots
            # and making them correspond to their parent triplet and/or block

            if reading == "triplet":
                currentShot = Shot(id=line[:-1],triplet=currentTriplet,block=currentBlock, dataPath=os.path.join(DATA_ROOT,line[:-1]))
                get_ccdList(currentShot)
                currentTriplet.shots.append(currentShot)
                if verbose: print(f"      Shot {line[:-1]}")
            
            if reading == "messy_block":
                currentShot = Shot(id=line[:-1],block=currentBlock, dataPath=os.path.join(DATA_ROOT,line[:-1]))
                get_ccdList(currentShot)
                currentBlock.orphanShots.append(currentShot)
                if verbose: print(f"   Orphan shot {line[:-1]}")
    print(f"Readed {len(Block.all)} blocks, {len(Triplet.all)} triplets, {len(Shot.all)} shots, {len(CCD.all)} CCDs, ")

def get_ccdList(shot):
    for i in os.listdir(shot.dataPath):
        path = os.path.join(shot.dataPath,i)
        if os.path.isdir(path) and i[:3] == "ccd":
            newCCD = CCD(id=i[3:],dataPath=path,shot=shot,triplet=shot.triplet,block=shot.block)

#    _____                      _      _          ____  _     _           _       
#   / ____|                    | |    | |        / __ \| |   (_)         | |      
#  | |     ___  _ __ ___  _ __ | | ___| |_ ___  | |  | | |__  _  ___  ___| |_ ___ 
#  | |    / _ \| '_ ` _ \| '_ \| |/ _ \ __/ _ \ | |  | | '_ \| |/ _ \/ __| __/ __|
#  | |___| (_) | | | | | | |_) | |  __/ ||  __/ | |__| | |_) | |  __/ (__| |_\__ \
#   \_____\___/|_| |_| |_| .__/|_|\___|\__\___|  \____/|_.__/| |\___|\___|\__|___/
#                        | |                                _/ |                  
#                        |_|                               |__/                                                                                                                                                                                                                        

def getBlock(block):
    """This function use the informations contained in the block object to find the corresponding data and fill the missing parts"""
    return block

def getTriplet(triplet):
    """This function use the informations contained in the triplet object to find the corresponding data and fill the missing parts"""
    return triplet

def getShot(shot):
    """This function use the informations contained in the shot object to find the corresponding data and fill the missing parts"""
    return shot

def getCCD(ccd):
    """This function use the informations contained in the CCD object to find the corresponding data and fill the missing parts"""
    return ccd

if __name__ == "__main__":
    connectData(verbose=False)

    
#   __  __ _         _                   _       _        
#  |  \/  (_)       (_)                 | |     | |       
#  | \  / |_ ___ ___ _ _ __   __ _    __| | __ _| |_ __ _ 
#  | |\/| | / __/ __| | '_ \ / _` |  / _` |/ _` | __/ _` |
#  | |  | | \__ \__ \ | | | | (_| | | (_| | (_| | || (_| |
#  |_|  |_|_|___/___/_|_| |_|\__, |  \__,_|\__,_|\__\__,_|
#                             __/ |                       
#                            |___/                       


    with open("listFWHM","w+") as file, open("listAPCOR","w+") as file2, open("listZEROPOINT","w+") as file3:
        count = 0
        count2 = 0
        count3 = 0
        for ccd in CCD.all.values():
            if not os.path.isfile(os.path.join(ccd.dataPath,f"{ccd.shot.id}p{ccd.id}.fwhm")):
                file.write(ccd.uid + "\n")
                print(os.path.join(ccd.dataPath,f"{ccd.shot.id}p{ccd.id}.fwhm"))
                count += 1
            if not os.path.isfile(os.path.join(ccd.dataPath,f"{ccd.shot.id}p{ccd.id}.apcor")):
                file2.write(ccd.uid + "\n")
                print(os.path.join(ccd.dataPath,f"{ccd.shot.id}p{ccd.id}.apcor"))
                count2 += 1
        
            if not os.path.isfile(os.path.join(ccd.dataPath,f"{ccd.shot.id}p{ccd.id}.zeropoint.used")):
                file3.write(ccd.uid + "\n")
                print(os.path.join(ccd.dataPath,f"{ccd.shot.id}p{ccd.id}.zeropoint.used"))
                count3 += 1

    print(count)
    print(count2)
    print(count3)