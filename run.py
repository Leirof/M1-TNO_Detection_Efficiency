import interface
from block import Block
from triplet import Triplet
from shot import Shot
from ccd import CCD
import os
from astropy.io import fits
from numpy import *
from utils.multithread import *
from multiprocessing import Pool
from ccd import *
import time
from utils.term import *
import json

if __name__ == "__main__":

    interface.connectData(verbose=True)

    print("Treating Data...")
    i=0
    data = {}
    for block in Block.all.values():
        if i > 0: break
        print(f"Block {block.id}")
        for triplet in block.tripletList:
            if i > 0: break
            print(f"|  Triplet {triplet.id}")
            for shot in triplet.shotList:
                if i > 0: break
                else: i+=1
                print(f"|  |  Shot {shot.id}")

                print("|  |  Loading shot...",end="\r")
                interface.loadShot(shot)

                #------ MonoThread

                for ccd in shot.ccdList:
                    #print(f"|  |  |   CCD {ccd.id}")
                    progressbar(int(ccd.id)/(len(shot.ccdList)-1),prefix="|  |  ")
                    ccd.compute_sky_background()

                #------ Multithread

                # args = []
                # for ccd in shot.ccdList:
                #     args.append((ccd, len(shot.ccdList), 2, "|  |  "))
                    
                # print("|  |  Computing...",end="\r")
                # cores = min(len(shot.ccdList),CPUcount)
                # print(len(args),cores)
                # with Pool(cores) as p: ccds_background = p.starmap(CCD.mp_compute_sky_backgroud,args) # Computing all ccd's sky background and put hem in the good order
                # shot.unload()

                #------

                
                shot.unload()
        data.update({f"block {block.id}":block.to_dict()})
    with open(os.path.join(interface.OUTPUT,'data.json'), 'w') as fp:
        json.dump(data, fp)