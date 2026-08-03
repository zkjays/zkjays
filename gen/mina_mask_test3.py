import numpy as np
from PIL import Image
from scipy import ndimage

ASSETS = r"C:\Users\Jays\AppData\Local\Temp\claude\C--Users-Jays-Documents-Second-Brain-zkjays\9916058f-aa43-41f2-a91d-295529fd98a2\scratchpad\pathode\assets"

mina = Image.open(f"{ASSETS}\\logo-mina.png").convert("RGB")
arr = np.array(mina).astype(float)
lum = 0.299*arr[...,0] + 0.587*arr[...,1] + 0.114*arr[...,2]

thr = 205
mask = lum > thr

def disk(r):
    y, x = np.ogrid[-r:r+1, -r:r+1]
    return (x*x + y*y) <= r*r

opened = ndimage.binary_opening(mask, structure=disk(4))
lbl, n = ndimage.label(opened)
sizes = ndimage.sum(opened, lbl, range(1, n+1))
sizes_sorted = sorted(sizes, reverse=True)
print("after opening n comp", n, "top sizes", sizes_sorted[:6])
biggest = np.argmax(sizes) + 1
clean = lbl == biggest
# dilate back a touch to restore stroke width lost by opening
clean = ndimage.binary_dilation(clean, structure=disk(2))
print("clean size", clean.sum())
Image.fromarray((clean*255).astype(np.uint8)).save(f"{ASSETS}\\logo-mina-mask.png")
