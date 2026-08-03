import numpy as np


def floyd_steinberg_serpentine(gray):
    """gray: float32 array in [0,255]. Returns boolean array, True = ink (dark->on for our convention
    we treat 'on' as the pixel that should be LIT, i.e. high input value after processing means foreground).
    Here we dither treating higher value = more likely ON (white=on)."""
    img = gray.astype(np.float64).copy()
    h, w = img.shape
    out = np.zeros((h, w), dtype=bool)
    for y in range(h):
        serpentine = (y % 2 == 1)
        xs = range(w - 1, -1, -1) if serpentine else range(w)
        for x in xs:
            old = img[y, x]
            new = 255.0 if old >= 128 else 0.0
            out[y, x] = new == 255.0
            err = old - new
            if serpentine:
                if x - 1 >= 0:
                    img[y, x - 1] += err * 7 / 16
                if y + 1 < h:
                    if x + 1 < w:
                        img[y + 1, x + 1] += err * 3 / 16
                    img[y + 1, x] += err * 5 / 16
                    if x - 1 >= 0:
                        img[y + 1, x - 1] += err * 1 / 16
            else:
                if x + 1 < w:
                    img[y, x + 1] += err * 7 / 16
                if y + 1 < h:
                    if x - 1 >= 0:
                        img[y + 1, x - 1] += err * 3 / 16
                    img[y + 1, x] += err * 5 / 16
                    if x + 1 < w:
                        img[y + 1, x + 1] += err * 1 / 16
    return out
