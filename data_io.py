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
                parent   = block,
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

            for rate_key, rate_value in triplet_value["rates"].items():

                if "square" in rate_value: func = "square"
                if "tan" in rate_value:    func = "tan"

                triplet.rates.append(Rate(
                    parent  =  triplet,
                    func    = func,
                    min_vel = rate_value["min"],
                    max_vel = rate_value["max"],
                    a       = rate_value[func]["a"],
                    b       = rate_value[func]["b"],
                    c       = rate_value[func]["c"],
                    d       = rate_value[func]["d"]
                ))

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

def loadAll(path = "./data"):
    for file in os.listdir(path):
        if file.endswith(".yaml") or file.endswith(".yml") or file.endswith(".json"):
            if file.split('.')[0] in Block.all: print(f"Block {file.split('.')[0]} is already loaded.")
            else:
                print(f"Loading {file}")
                loadSerialized(f"{path}/{file}")

def saveAll(folder = "./data", indent = None):
    for _, block in Block.all.items():
        block.save(folder, indent = indent)

def get_ai_ready(items = Block.all, useExisting = True, func = "tan", vel = 4.5, maxTriplet = 8, maxCCD = 36, randomTriplet = True, randomCCD = True, subsets_per_block=1):
    # if useExisting:
    #     try:    return load("data/ai_ready.npz")["data"]
    #     except: print("No data already available")
    data = []

    itemList = []

    if type(items) == dict:
        for _, value in items.items():
            itemList.append(value)

    for item in itemList:
        i = 0
        while i<subsets_per_block:
            item_data, outputs = item.to_ai_ready(func = func, vel = vel, maxTriplet = maxTriplet, maxCCD = maxCCD, randomTriplet = randomTriplet, randomCCD = randomCCD)
            if item_data is None:
                break
            # if block_data in data:
            #     continue
            data.append(item_data)
            i+=1
    
    data = array(data)
    # savez_compressed("data/ai_ready", data = data)
    return data, outputs


def yaml_to_json():
    for path, dirs, files in os.walk("./data"):
        for file in files:
            if file.endswith(".yaml") or file.endswith(".yml"):
                with open(f"{path}/{file}", 'r') as f:
                    data = yaml.safe_load(f)
                with open(f"{path}/{file.split('.')[0]}.json", 'w') as f:
                    json.dump(data, f)
                os.remove(f"{path}/{file}")

def json_to_yaml():
    for path, dirs, files in os.walk("./data"):
        for file in files:
            if file.endswith(".json"):
                with open(f"{path}/{file}", 'r') as f:
                    data = json.load(f)
                with open(f"{path}/{file.split('.')[0]}.yaml", 'w') as f:
                    yaml.dump(data, f)
                os.remove(f"{path}/{file}")
