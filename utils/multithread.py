import os
import threading
from utils.term import *

CPUcount = os.cpu_count()

class mp(threading.Thread):
    def run_compute_sky_backgroud(self, ccd, totalCCD=-1, verbose=False, prefix=""):
            """Allow to parrallelize the call of sky_backgroud()"""

            if verbose == 2: print(f"{prefix}Computing sky background of CCD {int(ccd.id)}...")
            if verbose == True: progressbar(int(ccd.id) / (totalCCD-1), prefix=prefix)

            ccd.compute_sky_background()

            if verbose == 2: print(f"{prefix}Sky background of CCD {int(ccd.id)} computed.")