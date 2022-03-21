from numpy import *

class CCD():

    all = []
    count = 0
    lastUsedID = 0

    def __init__(self, num = None, data = None):
        self.id = CCD.lastUsedID
        CCD.lastUsedID += 1
        self.num = num
        self.data = data
        CCD.all.append(self)

    def compute_sky_background(self, verbose = False, prefix = ""):
        """This function compute the sky background"""
        img = self.data

        for i in range(3):
            a = mean(img[img!=0]); s = std(img[img!=0])
            if verbose: print(f"{prefix}Loop {i}: Median={round(median(img),2)}, Average={round(a,2)}, Standrad deviation={round(s,2)}")
            img = img * (img < a+3*s) * (img > a-3*s)

        m = median(img); a = mean(img[img!=0]); s = std(img[img!=0])
        if verbose: print(f"{prefix}Loop {i}: Median={round(m,2)}, Average={round(a,2)}, Standrad deviation={round(s,2)}")

        sizeX, sizeY = img.shape

        self.sky_background = img
        self.background_median = m
        self.background_average = a
        self.background_std = s
        self.background_proportion = sum(img!=0) / (sizeX*sizeY)

    def computeFWHM(self):
        self.FWHM = 3
    
    def addCount(self):
        CCD.count += 1