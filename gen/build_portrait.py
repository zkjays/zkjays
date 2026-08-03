import sys
import numpy as np
from PIL import Image, ImageOps, ImageEnhance, ImageFilter

sys.path.insert(0, r"C:\Users\Jays\AppData\Local\Temp\claude\C--Users-Jays-Documents-Second-Brain-zkjays\9916058f-aa43-41f2-a91d-295529fd98a2\scratchpad\pathode\gen")
from dither import floyd_steinberg_serpentine

ASSETS = r"C:\Users\Jays\AppData\Local\Temp\claude\C--Users-Jays-Documents-Second-Brain-zkjays\9916058f-aa43-41f2-a91d-295529fd98a2\scratchpad\pathode\assets"

im = Image.open(f"{ASSETS}\\portrait.png").convert("L")
im = im.resize((300, 300), Image.LANCZOS)
im = ImageOps.autocontrast(im, cutoff=2)
im = ImageEnhance.Contrast(im).enhance(1.3)
im = im.filter(ImageFilter.UnsharpMask(radius=3, percent=140, threshold=2))

arr = np.array(im).astype(np.float64)
mask = floyd_steinberg_serpentine(arr)
print("on px", mask.sum(), "of", mask.size)

Image.fromarray((mask * 255).astype(np.uint8)).save(f"{ASSETS}\\portrait-dither.png")
np.save(f"{ASSETS}\\portrait-mask.npy", mask)
