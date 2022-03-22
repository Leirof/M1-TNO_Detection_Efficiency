import os
from block import Block
from triplet import Triplet
from shot import Shot
from ccd import CCD

OUTPUT_ROOT = "./results/"

def block_path(block : Block) -> str:
    return os.join(OUTPUT_ROOT,block.id)

def triplet_path(triplet : Triplet) -> str:
    path = OUTPUT_ROOT
    if triplet.block is not None: path = os.path.join(path, triplet.block.id)
    else:                         path = os.path.join(path, "unknown_block")
    return os.path.join(path,triplet.id)

def shot_path(shot : Shot) -> str:
    path = OUTPUT_ROOT
    if   shot.triplet is not None: path = block_path(shot.triplet)
    elif shot.block   is not None: path = os.path.join(block_path(shot.block),"orphan_shot")
    else:                          path = os.path.join(path, "unknown_block/orphan_shot")
    return os.path.join(path,shot.id)

def CCD_path(ccd : CCD) -> str:
    path = OUTPUT_ROOT
    if   ccd.shot    is not None: path = block_path(ccd.shot)
    if   ccd.triplet is not None: path = block_path(ccd.triplet)
    elif ccd.block   is not None: path = os.path.join(block_path(ccd.block),"orphan_shot")
    else:                         path = os.path.join(path, "unknown_block/orphan_shot")
    return os.path.join(path,ccd.id)