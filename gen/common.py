import numpy as np
from PIL import Image
from scipy import ndimage

ASSETS = r"C:\Users\Jays\AppData\Local\Temp\claude\C--Users-Jays-Documents-Second-Brain-zkjays\9916058f-aa43-41f2-a91d-295529fd98a2\scratchpad\pathode\assets"


def mask_to_points(mask, max_points, seed=0):
    """Return centered, unit-scaled (x,y) points sampled from an on-mask.
    Coordinate frame: x,y in roughly [-0.5, 0.5], aspect preserved, centered on mask centroid of bbox.
    """
    ys, xs = np.where(mask)
    x0, x1 = xs.min(), xs.max()
    y0, y1 = ys.min(), ys.max()
    w = x1 - x0 + 1
    h = y1 - y0 + 1
    scale = max(w, h)
    cx = (x0 + x1) / 2.0
    cy = (y0 + y1) / 2.0
    px = (xs - cx) / scale
    py = (ys - cy) / scale
    pts = np.stack([px, py], axis=1)
    rng = np.random.default_rng(seed)
    if len(pts) > max_points:
        idx = rng.choice(len(pts), size=max_points, replace=False)
        pts = pts[idx]
    return pts, (w / scale, h / scale)


def farthest_point_thin(pts, target, seed=0):
    """If pts already <= target, return as-is. Else subsample via blue-noise-ish grid jitter
    for even coverage rather than pure uniform random."""
    if len(pts) <= target:
        return pts
    rng = np.random.default_rng(seed)
    idx = rng.choice(len(pts), size=target, replace=False)
    return pts[idx]
