import numpy as np
from PIL import Image
from scipy import ndimage

ASSETS = r"C:\Users\Jays\AppData\Local\Temp\claude\C--Users-Jays-Documents-Second-Brain-zkjays\9916058f-aa43-41f2-a91d-295529fd98a2\scratchpad\pathode\assets"

mina = Image.open(f"{ASSETS}\\logo-mina.png").convert("RGB")
arr = np.array(mina).astype(float)
lum = 0.299*arr[...,0] + 0.587*arr[...,1] + 0.114*arr[...,2]

for thr in (200, 215, 230, 240):
    mask = lum > thr
    lbl, n = ndimage.label(mask)
    sizes = ndimage.sum(mask, lbl, range(1, n+1))
    sizes = sorted(sizes, reverse=True)
    print(thr, "components", n, "top10 sizes", sizes[:10], "total on", mask.sum())

thr = 225
mask = lum > thr
lbl, n = ndimage.label(mask)
sizes = ndimage.sum(mask, lbl, range(1, n+1))
# keep components with size >= 40 (drop tiny watermark glyph fragments)
keep_ids = [i+1 for i, s in enumerate(sizes) if s >= 40]
clean = np.isin(lbl, keep_ids)
print("clean on px", clean.sum(), "kept components", len(keep_ids))
Image.fromarray((clean*255).astype(np.uint8)).save(f"{ASSETS}\\logo-mina-mask.png")
