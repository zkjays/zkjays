import numpy as np
from PIL import Image
from scipy import ndimage

ASSETS = r"C:\Users\Jays\AppData\Local\Temp\claude\C--Users-Jays-Documents-Second-Brain-zkjays\9916058f-aa43-41f2-a91d-295529fd98a2\scratchpad\pathode\assets"

mina = Image.open(f"{ASSETS}\\logo-mina.png").convert("RGB")
arr = np.array(mina).astype(float)
lum = 0.299*arr[...,0] + 0.587*arr[...,1] + 0.114*arr[...,2]

thr = 240
mask = lum > thr
lbl, n = ndimage.label(mask, structure=np.ones((3,3)))
sizes = ndimage.sum(mask, lbl, range(1, n+1))
biggest = np.argmax(sizes) + 1
clean = lbl == biggest
# small dilation to thicken the thin outline slightly for nicer dot sampling
clean = ndimage.binary_dilation(clean, iterations=1)
print("clean size", clean.sum())
Image.fromarray((clean*255).astype(np.uint8)).save(f"{ASSETS}\\logo-mina-mask.png")
