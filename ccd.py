from numpy import *
from utils.term import *

#    _____ _____ _____  
#   / ____/ ____|  __ \ 
#  | |   | |    | |  | |
#  | |   | |    | |  | |
#  | |___| |____| |__| |
#   \_____\_____|_____/ 
                   
class CCD():
    __slots__ = ('__dict__','uid','id','data','shot','triplet','block','dataPath',
                'sky_background','background_average','background_median','background_std','background_proportion',
                'fwhm',
                'apcor_inner_radius', 'apcor_outer_radius', 'apcor_factorn', 'apcor_uncertainty',
                'zeropoint',
                'trans_mat')

    all = {}
    lastID = 0

    def __init__(self, id = None, data = None, shot = None, triplet = None, block = None, dataPath = None):
        self.uid                   = f"{shot.id}p{id}"
        self.id                    = id
        self.data                  = data
        self.shot                  = shot
        self.triplet               = triplet
        self.block                 = block
        self.dataPath              = dataPath
        self.sky_background        = None
        self.background_median     = None
        self.background_average    = None
        self.background_std        = None
        self.background_proportion = None
        self.fwhm                  = None
        self.apcor_inner_radius    = None
        self.apcor_outer_radius    = None
        self.apcor_factor          = None
        self.apcor_uncertainty     = None
        self.zeropoint             = None
        self.trans_mat             = None
        CCD.all.update({self.uid:self})

    def compute_sky_background(self, verbose = False, prefix = ""):
        """This function compute the sky background"""
        img = self.data
        
        if img is None:
            print(f"/!\ CCD{self.id} contain no data (shot n°{self.shot.id}, triplet {self.triplet.id})\n   -> {self.shot.dataPath}")
            return

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
 
    def mp_compute_sky_background(ccd, totalCCD=-1, verbose=False, prefix=""):
        """Allow to parrallelize the call of sky_backgroud()"""
        if verbose == 2: print(f"{prefix}Computing sky background of CCD {int(ccd.id)}...")
        if verbose == True: progressbar(int(ccd.id) / (totalCCD-1), prefix=prefix)
        ccd.compute_sky_background()
        if verbose == 2: print(f"{prefix}Sky background of CCD {int(ccd.id)} computed.")

    def computeFWHM(self):
        pass # TODO

    def computeAPCOR(self):
        pass # TODO

    def unload(self,all=False):
        self.data           = None
        self.sky_background = None
        if all:
            self.background_median     = None
            self.background_average    = None
            self.background_std        = None
            self.background_proportion = None

    def to_dict(self):
        dict = {'id':self.id,
                'background_average'   :self.background_average,
                'background_median'    :self.background_median,
                'background_std'       :self.background_std,
                'background_proportion':self.background_proportion,
                'fwhm'                 :self.fwhm,
                'apcor_inner_radius'   :self.apcor_inner_radius,
                'apcor_outer_radius'   :self.apcor_outer_radius,
                'apcor_factor'         :self.apcor_factor,
                'apcor_uncertainty'    :self.apcor_uncertainty,
                'zeropoint'            :self.zeropoint,
                'trans_a'              :self.trans_mat[0] if self.trans_mat is not None else None,
                'trans_b'              :self.trans_mat[1] if self.trans_mat is not None else None,
                'trans_c'              :self.trans_mat[2] if self.trans_mat is not None else None,
                'trans_d'              :self.trans_mat[3] if self.trans_mat is not None else None,
                'trans_e'              :self.trans_mat[4] if self.trans_mat is not None else None,
                'trans_f'              :self.trans_mat[5] if self.trans_mat is not None else None
            }
        # if self.trans_mat is not None: print(dict)
        return dict