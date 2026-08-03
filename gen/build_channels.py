import numpy as np
from scipy.optimize import linear_sum_assignment
import sys

sys.path.insert(0, r"C:\Users\Jays\AppData\Local\Temp\claude\C--Users-Jays-Documents-Second-Brain-zkjays\9916058f-aa43-41f2-a91d-295529fd98a2\scratchpad\pathode\gen")
from common import mask_to_points

ASSETS = r"C:\Users\Jays\AppData\Local\Temp\claude\C--Users-Jays-Documents-Second-Brain-zkjays\9916058f-aa43-41f2-a91d-295529fd98a2\scratchpad\pathode\assets"

N_TRAVELER = 550
N_DENSE = 999999  # effectively no subsampling; keep full dithered point cloud for detail

portrait_mask = np.load(f"{ASSETS}\\portrait-mask.npy")
mina_mask = np.load(f"{ASSETS}\\logo-mina-mask.npy")
darkroom_mask = np.load(f"{ASSETS}\\logo-darkroom-mask.npy")
x_mask = np.load(f"{ASSETS}\\logo-x-mask.npy")

dense_pts, dense_aspect = mask_to_points(portrait_mask, N_DENSE, seed=1)
portrait_pts, p_aspect = mask_to_points(portrait_mask, N_TRAVELER, seed=2)
mina_pts, mina_aspect = mask_to_points(mina_mask, N_TRAVELER, seed=3)
darkroom_pts, dr_aspect = mask_to_points(darkroom_mask, N_TRAVELER, seed=4)
x_pts, x_aspect = mask_to_points(x_mask, N_TRAVELER, seed=5)

print("dense", len(dense_pts), "portrait", len(portrait_pts), "mina", len(mina_pts),
      "darkroom", len(darkroom_pts), "x", len(x_pts))


def pad_to(pts, n, seed):
    """Pad point set to exactly n points by duplicating random existing points with tiny jitter."""
    if len(pts) == n:
        return pts
    rng = np.random.default_rng(seed)
    if len(pts) > n:
        idx = rng.choice(len(pts), size=n, replace=False)
        return pts[idx]
    extra = n - len(pts)
    idx = rng.choice(len(pts), size=extra, replace=True)
    jitter = rng.normal(0, 0.002, size=(extra, 2))
    return np.concatenate([pts, pts[idx] + jitter], axis=0)


portrait_pts = pad_to(portrait_pts, N_TRAVELER, 12)
mina_pts = pad_to(mina_pts, N_TRAVELER, 13)
darkroom_pts = pad_to(darkroom_pts, N_TRAVELER, 14)
x_pts = pad_to(x_pts, N_TRAVELER, 15)


def match(src, dst):
    """Return dst reordered so that dst[i] is the optimal partner for src[i] (Hungarian)."""
    cost = ((src[:, None, :] - dst[None, :, :]) ** 2).sum(axis=2)
    row_ind, col_ind = linear_sum_assignment(cost)
    order = np.empty(len(src), dtype=int)
    order[row_ind] = col_ind
    return dst[order]


# Sequence: portrait -> mina -> darkroom -> x -> (loop back to) portrait
channel_portrait = portrait_pts
channel_mina = match(channel_portrait, mina_pts)
channel_darkroom = match(channel_mina, darkroom_pts)
channel_x = match(channel_darkroom, x_pts)
# loop closes back to channel_portrait (fixed identity, no reassignment - must return exactly to start)

total_cost = (
    np.sum((channel_portrait - channel_mina) ** 2) +
    np.sum((channel_mina - channel_darkroom) ** 2) +
    np.sum((channel_darkroom - channel_x) ** 2) +
    np.sum((channel_x - channel_portrait) ** 2)
)
print("total sq movement cost", total_cost)

np.save(f"{ASSETS}\\channel_portrait.npy", channel_portrait)
np.save(f"{ASSETS}\\channel_mina.npy", channel_mina)
np.save(f"{ASSETS}\\channel_darkroom.npy", channel_darkroom)
np.save(f"{ASSETS}\\channel_x.npy", channel_x)
np.save(f"{ASSETS}\\dense_pts.npy", dense_pts)

print("aspects: portrait", p_aspect, "mina", mina_aspect, "darkroom", dr_aspect, "x", x_aspect, "dense", dense_aspect)
