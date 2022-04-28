"""_summary_
This script is used to get the detection rate model parameters from the experimental detection rate given by the fake objects method.
"""

INPUT = "D:\Lab_Project\Fake_Objects_Data"

import os
import numpy as np
import re
import interface

from block import Block
from triplet import Triplet
from shot import Shot
from ccd import CCD



tmpFile = -1
def unpack(file_name):
    """
    Unpack the data from the file.
    """
    global tmpFile

    if not os.path.isdir("tmp"): os.mkdir("tmp")
    tmp = open("tmp/asupr.txt", "w")

    with open(file_name, 'r') as f:
        for line in f:
            if line.startswith("#fk") or line.startswith("#K EXPNUM"):
                if tmpFile >= 0: tmp.close()
                tmpFile += 1
                tmp = open(f"tmp/{tmpFile}.txt", "a")
            tmp.write(line)
        tmp.close()

"""
    print(file_name)
    regex1 = re.compile('#fk([0-9]*)s([0-9]*).*')
    regex2 = re.compile('#V ([0-9][0-9][0-9][0-9][0-9][0-9][0-9]).*')

    if not os.path.isdir("tmp"): os.mkdir("tmp")

    dict = {}
    data = []
    oldShots = []
    for line in open(file_name):
        if line.startswith("# "): continue

        # Case 1
        if line.startswith("#fk"):
            shot, ccd = regex1.search(line).groups()
            shots = [shot]
            ccd = int(ccd)
            print("Case 1 ----------")
            print(shot, ccd)

        # Case 2
        if line.startswith("#K EXPNUM"):
            shots = []
            ccd = 0
            print("Case 2 ----------")
        if regex2.match(line):
            shots.append(regex2.search(line).groups()[0])
            if len(shots) == 3:
                if shots == oldShots: ccd += 1
                else: ccd = 0
                oldShots = shots
                print(shots,ccd)

        # Values
        if not line.startswith("#"):
            for shot in shots:
                if not os.path.isdir(f"tmp/{shot}"): os.mkdir(f"tmp/{shot}")
                if ccd < 10: sccd = f"0{ccd}"
                else: sccd = str(ccd)
                with open(f"tmp/{shot}/{sccd}.npy","a") as f:
                    f.write(line)
    return data
"""

if __name__ == "__main__":
    # interface.connectData(verbose=True)
    for root, dir, files in os.walk(INPUT):
        for file in files:
            if  file[-12:] == ".reals.match":
                unpack(os.path.join(root, file))
                #print(data)
