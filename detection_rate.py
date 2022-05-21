"""_summary_
This script is used to get the detection rate model parameters from the experimental detection rate given by the fake objects method.
"""

INPUT = "D:\Lab_Project\Fake_Objects_Data"

import os
from numpy import *
import re
import interface
import matplotlib.pyplot as plt
import scipy.optimize as optimize

from block import Block
from triplet import Triplet
from shot import Shot
from ccd import CCD

def ft(m,a,b,c,d):
    return  1/4 * a * (1-tanh((m-b)/c)) * (1-tanh((m-b)/d))

def fs(m,a,b,c,d):
    return  (a-b*(m-21)**2) / (1+exp((m-c)/d))


data = loadtxt("D:/Lab_Project/Fake_Objects_Data/2013A/Oblock/sL2_fk_O.0.50-7.00-0.2.mag-rate.eff")

mag = data[:,0]
eff = data[:,1]
paramft = [1,21,10,1]
paramfs = [25,0,25,3]

paramft = optimize.curve_fit(ft, mag, eff, paramft)[0]
paramfs = optimize.curve_fit(fs, mag, eff, paramfs, maxfev=100000)[0]

print(paramft)
print(paramfs)

plt.subplot(121)
plt.plot(mag,eff,"x",label="Experimental")
plt.plot(mag,ft(mag,*paramft),label="FT")
plt.legend()
plt.grid()
plt.subplot(122)
plt.plot(mag,eff,"x",label="Experimental")
plt.plot(mag,fs(mag,*paramfs),label="FS")
plt.legend()
plt.grid()
plt.show()


'''
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

if __name__ == "__main__":
    # interface.connectData(verbose=True)
    for root, dir, files in os.walk(INPUT):
        for file in files:
            if  file[-12:] == ".reals.match":
                unpack(os.path.join(root, file))
                #print(data)

'''