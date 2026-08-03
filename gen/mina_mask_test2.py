import numpy as np
from PIL import Image
from scipy import ndimage

ASSETS = r"C:\Users\Jays\AppData\Local\Temp\claude\C--Users-Jays-Documents-Second-Brain-zkjays\9916058f-aa43-41f2-a91d-295529fd98a2\scratchpad\pathode\assets"

mina = Image.open(f"{ASSETS}\\logo-mina.png").convert("RGB")
arr = np.array(mina).astype(float)
lum = 0.299*arr[...,0] + 0.587*arr[...,1] + 0.114*arr[...,2]

thr = 205
mask = lum > thr
# close small gaps then keep largest component
mask_c = ndimage.binary_closing(mask, structure=np.ones((3,3)), iterations=2)
lbl, n = ndimage.label(mask_c)
sizes = ndimage.sum(mask_c, lbl, range(1, n+1))
sizes_sorted = sorted(sizes, reverse=True)
print("thr", thr, "n comp", n, "top sizes", sizes_sorted[:6])
biggest = np.argmax(sizes) + 1
clean = lbl == biggest
print("clean size", clean.sum())
Image.fromarray((clean*255).astype(np.uint8)).save(f"{ASSETS}\\logo-mina-mask.png")
