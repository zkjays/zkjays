import numpy as np
from PIL import Image
from scipy import ndimage

ASSETS = r"C:\Users\Jays\AppData\Local\Temp\claude\C--Users-Jays-Documents-Second-Brain-zkjays\9916058f-aa43-41f2-a91d-295529fd98a2\scratchpad\pathode\assets"

# --- Darkroom wordmark: use alpha channel ---
dr = Image.open(f"{ASSETS}\\logo-darkroom.png").convert("RGBA")
darr = np.array(dr)
dmask = darr[..., 3] > 100
lbl, n = ndimage.label(dmask, structure=np.ones((3, 3)))
sizes = ndimage.sum(dmask, lbl, range(1, n + 1))
# keep all components with reasonable size (letters are separate components!)
keep_ids = [i + 1 for i, s in enumerate(sizes) if s >= 8]
dmask_clean = np.isin(lbl, keep_ids)
print("darkroom on px", dmask_clean.sum(), "components kept", len(keep_ids), "of", n)
Image.fromarray((dmask_clean * 255).astype(np.uint8)).save(f"{ASSETS}\\logo-darkroom-mask.png")
np.save(f"{ASSETS}\\logo-darkroom-mask.npy", dmask_clean)

# --- Mina: reuse cleaned mask already saved as logo-mina-mask.png ---
mina_mask_img = Image.open(f"{ASSETS}\\logo-mina-mask.png").convert("L")
mina_mask = np.array(mina_mask_img) > 128
np.save(f"{ASSETS}\\logo-mina-mask.npy", mina_mask)
print("mina on px", mina_mask.sum())

# --- X glyph ---
x_img = Image.open(f"{ASSETS}\\logo-x.png").convert("L")
xarr = np.array(x_img)
xmask = xarr < 128
np.save(f"{ASSETS}\\logo-x-mask.npy", xmask)
print("x on px", xmask.sum())
