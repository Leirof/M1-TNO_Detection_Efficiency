import yaml
import json
from block import Block
from triplet import Triplet
from shot import Shot
from ccd import CCD
from numpy import *

def load(file):
    if file.endwith('.yaml') or file.endwith('.yml'):
        with open(file,'r') as f:
            data = yaml.safe_load(f)
    if file.endwith('.json'):
        with open(file,'r') as f:
            data = json.load(f)

    for block_key, block_value in data.items():
        block = Block(id=block_value["id"])

        for triplet_key, triplet_value in block_value["tripletList"].items():
            triplet = Triplet(id=triplet_value["id"], block=block)

            for shot_key, shot_value in triplet_value["shotList"].items():
                shot = Shot(id=shot_value["id"], triplet=triplet, block=block)

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

def save(file, bock = None):
    pass
    