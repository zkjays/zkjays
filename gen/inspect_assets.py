import numpy as np
from PIL import Image, ImageDraw, ImageFont

ASSETS = r"C:\Users\Jays\AppData\Local\Temp\claude\C--Users-Jays-Documents-Second-Brain-zkjays\9916058f-aa43-41f2-a91d-295529fd98a2\scratchpad\pathode\assets"

mina = Image.open(f"{ASSETS}\\logo-mina.png").convert("RGBA")
arr = np.array(mina)
print("mina shape", arr.shape)
rgb = arr[..., :3].astype(float)
lum = 0.299*rgb[...,0] + 0.587*rgb[...,1] + 0.114*rgb[...,2]
print("lum percentiles", np.percentile(lum, [1,5,25,50,75,90,95,99]))

darkroom = Image.open(f"{ASSETS}\\logo-darkroom.png").convert("RGBA")
darr = np.array(darkroom)
print("darkroom shape", darr.shape, "alpha max", darr[...,3].max(), "alpha>10 count", (darr[...,3]>10).sum())
ys, xs = np.where(darr[...,3] > 10)
if len(xs):
    print("darkroom bbox", xs.min(), xs.max(), ys.min(), ys.max())

# build X glyph
size = 500
img = Image.new("L", (size, size), 255)
d = ImageDraw.Draw(img)
font = ImageFont.truetype(r"C:\Windows\Fonts\ariblk.ttf", int(size*0.95))
bbox = d.textbbox((0,0), "X", font=font)
w = bbox[2]-bbox[0]
h = bbox[3]-bbox[1]
d.text(((size-w)/2 - bbox[0], (size-h)/2 - bbox[1]), "X", font=font, fill=0)
img.save(f"{ASSETS}\\logo-x.png")
xarr = np.array(img)
print("x glyph dark px", (xarr<128).sum())
