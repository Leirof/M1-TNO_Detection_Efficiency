import matplotlib.pyplot as plt
from numpy import *
import os

CPUcount = os.cpu_count()
term_size = os.get_terminal_size().columns

def save_ccd_as_png(data,name):
    x = arange(len(data))
    y = arange(len(data[0]))
    plt.clf()
    plt.pcolor(x,y,data.transpose(), shading='auto', cmap="gray")
    plt.colorbar(label='Luminosity')
    plt.xlabel("")
    plt.ylabel("")
    plt.title("Sky view")
    plt.savefig(name)

stop = False
def mp_sky_backgroud(numCCD, img, totalCCD=1, verbose=False, prefix=""):
    """Call sky_background() function by fixing the bug of multiprocess Keyboard Interruption not sent to all processes"""
    global stop
    if stop: return
    try:
        progress = int(min(floor(numCCD/totalCCD*(term_size-10)),term_size-10))
        print(f"   [{'='*progress}{' '*((term_size-10)-progress)}] {int(numCCD/totalCCD*100)}%",end="\r")
        if verbose: print(f"{prefix}Computing sky background of CCD {numCCD}...")
        img = sky_background(img)
        if verbose: print(f"{prefix}Sky background of CCD {numCCD} computed.")
        return (numCCD, img)
    except KeyboardInterrupt: stop = True


def sky_background(img, verbose=False, prefix=""):
    """This function compute the sky background"""
    
    for i in range(3):
        a = mean(img[img!=0]); s = std(img[img!=0])
        if verbose: print(f"{prefix}Loop {i}: Median={round(median(img),2)}, Average={round(a,2)}, Standrad deviation={round(s,2)}")
        img = img * (img < a+3*s) * (img > a-3*s)

    if verbose: print(f"{prefix}Loop {i}: Median={round(median(img),2)}, Average={round(mean(img[img!=0]),2)}, Standrad deviation={round(std(img[img!=0]),2)}")
    return img

def mp_save_ccd(path,i, ccd,ccd_background,totalCCD=1):
    """Call save_ccd() function by fixing the bug of multiprocess Keyboard Interruption not sent to all processes"""
    global stop
    if stop: return
    try:
        progress = int(min(floor(i/totalCCD*(term_size-10)),term_size-10))
        print(f"   [{'='*progress}{' '*((term_size-10)-progress)}] {int(i/totalCCD*100)}%",end="\r")
        save_ccd(path,i, ccd,ccd_background)
    except KeyboardInterrupt: stop = True

def save_ccd(path,i, ccd,ccd_background):
    if not os.path.isdir(f"{path}/ccd{i}"): os.makedirs(f"{path}/ccd{i}")
    savetxt(f"{path}/ccd{i}/ccd{i}.npy",ccd,fmt="%i")
    savetxt(f"{path}/ccd{i}/ccd{i}_background.npy",ccd_background,fmt="%i")