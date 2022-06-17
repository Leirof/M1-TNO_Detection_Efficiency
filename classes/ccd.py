from numpy           import *
from utils.term      import *
from classes.shot    import Shot
from classes.triplet import Triplet
from classes.block   import Block

class CCD():
    __slots__ = ('__dict__','uid','id','data','shot','triplet','block','dataPath',
                'sky_background','background_average','background_median','background_std','background_proportion',
                'fwhm',
                'apcor_inner_radius', 'apcor_outer_radius', 'apcor_factorn', 'apcor_uncertainty',
                'zeropoint',
                'trans_mat')

    all = {}
    lastID = 0

    """
      ___       _ _   
     |_ _|_ __ (_) |_ 
      | || '_ \| | __|
      | || | | | | |_ 
     |___|_| |_|_|\__|
                  
    """

    def __init__(self, id = None, data:ndarray = None, shot:Shot = None, triplet:Triplet = None, block:Block = None, dataPath:str = None):
        self.uid                   :str     = f"{shot.id}p{id}"
        self.id                    :int     = id
        self.data                  :ndarray = data
        self.shot                  :Shot    = shot
        self.triplet               :Triplet = triplet
        self.block                 :Block   = block
        self.dataPath              :str     = dataPath
        self.sky_background        :ndarray = None
        self.background_median     :float   = None
        self.background_average    :float   = None
        self.background_std        :float   = None
        self.background_proportion :float   = None
        self.fwhm                  :float   = None
        self.apcor_inner_radius    :float   = None
        self.apcor_outer_radius    :float   = None
        self.apcor_factor          :float   = None
        self.apcor_uncertainty     :float   = None
        self.zeropoint             :float   = None
        self.trans_mat             :ndarray = None

        if self not in shot.ccdList:
            shot.ccdList.append(self)

        if self.uid in CCD.all:
            raise ValueError("A CCD with this UID already exist")
        else:
            CCD.all.update({self.uid:self})

    """
       ____                            _        _   _                 
      / ___|___  _ __ ___  _ __  _   _| |_ __ _| |_(_) ___  _ __  ___ 
     | |   / _ \| '_ ` _ \| '_ \| | | | __/ _` | __| |/ _ \| '_ \/ __|
     | |__| (_) | | | | | | |_) | |_| | || (_| | |_| | (_) | | | \__ \
      \____\___/|_| |_| |_| .__/ \__,_|\__\__,_|\__|_|\___/|_| |_|___/
                          |_|                                         
    """

    def compute_sky_background(self, verbose = False, prefix = ""):
        """This function compute the sky background"""
        img = self.data
        
        if img is None:
            print(f"/!\ CCD{self.id} contain no data (shot n°{self.shot.id}, triplet {self.triplet.id})\n   -> {self.shot.dataPath}")
            return

        for i in range(3):
            a   = mean(img[img!=0]); s = std(img[img!=0])
            if verbose: print(f"{prefix}Loop {i}: Median={round(median(img),2)}, Average={round(a,2)}, Standrad deviation={round(s,2)}")
            img = img * (img < a+3*s) * (img > a-3*s)

        m = median(img); a = mean(img[img!=0]); s = std(img[img!=0])
        if verbose: print(f"{prefix}Loop {i}: Median={round(m,2)}, Average={round(a,2)}, Standrad deviation={round(s,2)}")

        sizeX, sizeY = img.shape

        self.sky_background        = img
        self.background_median     = m
        self.background_average    = a
        self.background_std        = s
        self.background_proportion = sum(img!=0) / (sizeX*sizeY)
 
    def mp_compute_sky_background(ccd, totalCCD=-1, verbose=False, prefix=""):
        """Allow to parrallelize the call of sky_backgroud()"""

        if verbose == 2:    print(f"{prefix}Computing sky background of CCD {int(ccd.id)}...")
        if verbose == True: progressbar(int(ccd.id) / (totalCCD-1), prefix=prefix)

        ccd.compute_sky_background()

        if verbose == 2:    print(f"{prefix}Sky background of CCD {int(ccd.id)} computed.")

    def computeFWHM(self):
        pass # TODO

    def computeAPCOR(self):
        pass # TODO

    """
      _   _ _   _ _     
     | | | | |_(_) |___ 
     | | | | __| | / __|
     | |_| | |_| | \__ \
      \___/ \__|_|_|___/
                    
    """

    # As the CCD can contain a lot of data, this function allow to free the memory by unloading unused CCDs
    def unload(self,all=False):
        self.data           = None
        self.sky_background = None
        if all:
            self.background_median     = None
            self.background_average    = None
            self.background_std        = None
            self.background_proportion = None

    # Export in a dictionnary to be stored in a human-readable format
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
        return dict

    # Export in numpy array that can be used to train an ai (need to be normalized before)
    def to_ai_ready(self, **kwargs):
        return array(   [   self.background_median,
                            self.background_average,
                            self.background_std,
                            self.background_proportion,
                            self.fwhm,
                            self.apcor_inner_radius,
                            self.apcor_outer_radius,
                            self.apcor_factor,
                            self.apcor_uncertainty,
                            self.zeropoint
                    ] + list(self.trans_mat))