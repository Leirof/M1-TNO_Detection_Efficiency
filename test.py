from turtle import back
import matplotlib.pyplot as plt
from numpy import *
from astropy.io import fits
import os

hdul = fits.open('D:/1615904/1615904p.fits.fz')
print(hdul.info())

data = hdul[1].data

sizeX, sizeY = data.shape
x = arange(sizeX)
y = arange(sizeY)

def background(data,verbose=False):
    m = median(data); a = mean(data); s = std(data)
    if verbose: print(f"   Initial: Median={round(m,2)}, Average={round(a,2)}, Standrad deviation={round(s,2)}")

    for i in range(3):
        data = data * (data < a+3*s) * (data > a-3*s)
        m = median(data); a = mean(data, where=data!=0); s = std(data)
        if verbose: print(f"   Loop {i}: Median={round(m,2)}, Average={round(a,2)}, Standrad deviation={round(s,2)}")

    return data

ccd = hdul[1].data
sizeX,sizeY = ccd.shape
ccd = empty([len(hdul)-1,sizeX,sizeY])
ccd_background = empty([len(hdul)-1,sizeX,sizeY])

def save_ccd_as_png(x,y,data,name):
    plt.pcolor(x,y,data.transpose(), shading='auto', cmap="gray")
    plt.colorbar(label='Luminosity')
    plt.xlabel("")
    plt.ylabel("")
    plt.title("Sky view")
    plt.savefig(f'{name}.png')

for i in arange(len(hdul)-1):
    ccd[i] = hdul[i+1].data
    print(f"Treating ccd {i}")
    ccd_background[i] = background(ccd[i])

    if not os.path.isdir(f'results/ccd{i}'):
        os.makedirs(f'results/ccd{i}')
    print(f"   Saving results...")
    savetxt(f"results/ccd{i}/ccd{i}.npy", ccd[i])
    savetxt(f"results/ccd{i}/ccd{i}_background.npy", ccd_background[i])
    print(f"   Generating images...")
    save_ccd_as_png(x,y,ccd[i],f"results/ccd{i}/ccd{i}.png")
    save_ccd_as_png(x,y,ccd_background[i],f"results/ccd{i}/ccd{i}_background.png")

