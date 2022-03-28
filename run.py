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
import json
import threading

if __name__ == "__main__":

    interface.connectData(verbose=True)

    print("Treating Data...")
    # i=0
    data = {}
    for j, block in enumerate(Block.all.values()):
        # if i > 0: break
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

                for m, ccd in enumerate(shot.ccdList):
                    thread = threading.Thread(target=CCD.mp_compute_sky_background, args=(ccd, len(shot.ccdList), True, f"|  |  Treating CCD {ccd.id} ({m+1}/{len(shot.ccdList)}) "))
                    thread.start()
                                
                for thread in threading.enumerate():
                    try:
                        thread.join()
                        del thread
                    except RuntimeError: pass

                #------

                
                shot.unload()
        data.update({f"block {block.id}":block.to_dict()})
    with open(os.path.join(interface.OUTPUT,'data.json'), 'w') as fp:
        json.dump(data, fp)