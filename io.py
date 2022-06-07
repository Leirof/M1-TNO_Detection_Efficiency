import yaml
import json
from classes.block   import Block
from classes.triplet import Triplet
from classes.shot    import Shot
from classes.ccd     import CCD
from classes.rate    import Rate
from numpy           import *
import os
import interface

def loadRawData(verbose=True):
    interface.connectData(verbose=verbose)

def loadSerialized(file):

    if file.endswith('.yaml') or file.endswith('.yml'):
        with open(file,'r') as f:
            data = yaml.safe_load(f)

    if file.endswith('.json'):
        with open(file,'r') as f:
            data = json.load(f)

    for block_key, block_value in data.items():
        block = Block(id=block_value["id"])

        for rate_key, rate_value in block_value["rates"].items():

            if "square" in rate_value: func = "square"
            if "tan" in rate_value:    func = "tan"

            block.rates.append(Rate(
                block   = block,
                func    = func,
                min_vel = rate_value["min"],
                max_vel = rate_value["max"],
                a       = rate_value[func]["a"],
                b       = rate_value[func]["b"],
                c       = rate_value[func]["c"],
                d       = rate_value[func]["d"]
            ))

        block_data = []
        triplet_count = 0
        for triplet_key, triplet_value in block_value["tripletList"].items():
            triplet = Triplet(id=triplet_value["id"], block=block)

            triplet_data = []
            for shot_key, shot_value in triplet_value["shotList"].items():
                shot = Shot(id=shot_value["id"], triplet=triplet, block=block)

                shot_data = []

                for ccd_key,        ccd_value       in shot_value["ccdList"].items():
                    ccd = CCD(id=ccd_value["id"], shot=shot, triplet=triplet, block=block)

                    ccd.background_median     = ccd_value["background_median"]
                    ccd.background_average    = ccd_value["background_average"]
                    ccd.background_std        = ccd_value["background_std"]
                    ccd.background_proportion = ccd_value["background_proportion"]
                    ccd.fwhm                  = ccd_value["fwhm"]
                    ccd.apcor_inner_radius    = ccd_value["apcor_inner_radius"]
                    ccd.apcor_outer_radius    = ccd_value["apcor_outer_radius"]
                    ccd.apcor_factor          = ccd_value["apcor_factor"]
                    ccd.apcor_uncertainty     = ccd_value["apcor_uncertainty"]
                    ccd.zeropoint             = ccd_value["zeropoint"]
                    ccd.trans_mat             = array([ ccd_value["trans_a"],
                                                        ccd_value["trans_b"],
                                                        ccd_value["trans_c"],
                                                        ccd_value["trans_d"],
                                                        ccd_value["trans_e"],
                                                        ccd_value["trans_f"],
                                                    ])

def import_all(path = "./data"):
    for folder in os.listdir(path):
        if os.path.isdir(f"./data/{folder}"):
            for file in os.listdir(f"./data/{folder}"):
                print(f"Loading {file}")
                if file.endswith(".yaml") or file.endswith(".yml") or file.endswith(".json"):
                    loadSerialized(f"./data/{folder}/{file}")

def get_ai_ready(func = "tan", vel = 4.5, maxTriplet = 8, maxCCD = 36, randomTriplet = True, randomCCD = True, subsets_per_block=1):
    data = []
    for _, block in Block.all.items():
        i = 0
        while i<subsets_per_block:
            block_data = block.to_ai_ready(func, vel, maxTriplet, maxCCD, randomTriplet, randomCCD)
            if block_data is None:
                break
            # if block_data in data:
            #     continue
            data.append(block_data)
            i+=1
    return array(data)

def save(file, bock = None):
    pass
    
import_all()
print(get_ai_ready())