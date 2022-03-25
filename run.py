import input_interface
import output_interface
from block import Block
from triplet import Triplet
from shot import Shot
from ccd import CCD
import os
from astropy.io import fits
from numpy import *
from utils.term import *


input_interface.connectData(verbose=True)

for i,shot in enumerate(Triplet.all["E+0+1"].shotList):
    progressbar(i/(len(Triplet.all["E+0+1"].shotList)-1))
    input_interface.getShot(shot)