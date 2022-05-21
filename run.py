import interface
from block import Block
from triplet import Triplet
from shot import Shot
from ccd import CCD
import os
from astropy.io import fits
from numpy import *
from utils.multithread import *
from ccd import *
import time
from utils.term import *
import yaml
import threading

if __name__ == "__main__":

    interface.connectData(verbose=True)

    print("Treating Data...")
    data = {}
    for j, block in enumerate(Block.all.values()):
        if os.path.isfile(os.path.join(interface.OUTPUT,f"{block.id}.yml")): continue
        print(f"Block {block.id} ({j+1}/{len(Block.all.values())})")
        for k,triplet in enumerate(block.tripletList):
            # if i > 0: break
            print(f"|  Triplet {triplet.id} ({k+1}/{len(block.tripletList)})")
            for l, shot in enumerate(triplet.shotList):
                # if i > 0: break
                # else: i+=1
                print(f"|  |  Shot {shot.id} ({l+1}/{len(triplet.shotList)})")

                print("|  |  Loading shot...",end="\r")
                interface.loadShot(shot)

                #------ MonoThread

                # for m, ccd in enumerate(shot.ccdList):

                #     #print(f"|  |  |   CCD {ccd.id}")
                #     progressbar(int(ccd.id)/(len(shot.ccdList)-1),prefix=f"|  |  Treating CCD {ccd.id} ({m+1}/{len(shot.ccdList)}) ")
                #     ccd.compute_sky_background()

                #------ Multithread

                m=0
                while m < len(shot.ccdList):                            # Loop over the CCDs
                    joinThreads()                                       # Wait for existing threads
                    for _ in range(min(CPUcount,len(shot.ccdList)-m)):  # Associating a computation to a thread
                        thread = threading.Thread(target=CCD.mp_compute_sky_background, args=(shot.ccdList[m], len(shot.ccdList), True, f"|  |  Treating CCD {shot.ccdList[m].id} ({m+1}/{len(shot.ccdList)}) "))
                        thread.start()
                        m+=1
                joinThreads()

                #------
         
                shot.unload() # Free memory space

                
                shot.unload()
        with open(os.path.join(interface.OUTPUT,f'{block.id}.json'), 'w') as fp:
            yaml.dump({f"block {block.id}":block.to_dict()}, fp)
