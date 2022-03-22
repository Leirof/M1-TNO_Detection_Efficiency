
"""
This file allow to connect this program with different type of data classification system.
You can edit it in order to allow the program to treat your data.
"""

DATA_ROOTS = ["D:/Lab Project/OSSOS/dbimages/Triplets","D:/Lab Project/data/dbimages/Triplets_2","D:/Lab Project/data/dbimages/Missing"]

from block import Block
from triplet import Triplet
from shot import Shot
from ccd import CCD
import os

def connectData(verbose=False):
    """This function allow to create instances of all objects that will be used by the program. These informations can be incomplete (only containing the name/id of each object)"""
    reading = ""

    # Reading All_triplets file
    with open("rsrc/All_triplets") as file:
        for line in file:
            if line == "\n":
                continue

            # Reading headers
            if "#" in line:
                
                # If all the shots are not organized by triplet
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
            
            # Reading all shots ID and making them correspond to their parent triplet and/or block
            if reading == "triplet":
                currentShot = Shot(id=int(line[:-1]),triplet=currentTriplet,block=currentBlock)
                currentTriplet.shots.append(currentShot)
                if verbose: print(f"      Shot {line[:-1]}")
            
            if reading == "messy_block":
                currentShot = Shot(id=line[:-1],block=currentBlock)
                currentBlock.orphanShots.append(currentShot)
                if verbose: print(f"   Orphan shot {line[:-1]}")

    associatePath(verbose=False)


def associatePath(verbose=False):
    """This function allow to associate data path to each object"""

    associatedShots = 0
    additionalFolder = 0
    duplicatedFolder = 0

    for root in DATA_ROOTS:
        for folder in os.listdir(root):
            if folder in Shot.all:
                if Shot.all[folder].dataPath is not None:
                    duplicatedFolder +=1
                    print(f"Duplicated folder:\n   {Shot.all[folder].dataPath}\n      {os.listdir(Shot.all[folder].dataPath)}\n   {os.path.join(root,folder)}\n      {os.listdir(os.path.join(root,folder))}")
                else:
                    Shot.all[folder].dataPath = os.path.join(root,folder)
                    associatedShots += 1
                    if verbose: print(f"Shot {folder} path: {Shot.all[folder].dataPath}")
            elif folder.isdigit():
                additionalFolder += 1
                if verbose: print(f"Shot {folder} belong to no block and/or triplet")

    if verbose:
        for shot in Shot.all.values():
            if shot.dataPath is None: print(f"Shot {shot.id} have no associated folder")
    
    print(f"Associated path to {associatedShots} over {len(Shot.all)}. {additionalFolder} folders found without associated shot. {duplicatedFolder} duplicated folders")

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
    connectData(verbose=True)
    print(f"Readed {len(Block.all)} blocks, {len(Triplet.all)} triplets, {len(Shot.all)} shots, {len(CCD.all)} CCDs, ")