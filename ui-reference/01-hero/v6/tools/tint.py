"""Tint a neutral cut-out or ready-made object in a palette colour (SPEC §3, §4).

    python3 tint.py in.webp out.webp violet

The same recipe as tinted() in index.html: a tritone of the brightness, keeping 20 % of the original.
"""
import sys
import numpy as np
from PIL import Image

TRI = {  # shadow, mid, highlight
    'violet': ('#0d0620', '#7c3aed', '#f0e6ff'), 'blue': ('#050a20', '#2563eb', '#e2ecff'),
    'teal': ('#021412', '#0d9488', '#dcfff9'), 'green': ('#03140a', '#16a34a', '#dcfce7'),
    'gold': ('#140b03', '#b7791f', '#fff1d6'), 'orange': ('#170a02', '#ea580c', '#ffe9d6'),
    'crimson': ('#170309', '#be123c', '#ffe1e8'), 'pink': ('#1a0410', '#db2777', '#ffe4f1'),
}


def hex_rgb(h):
    return np.array([int(h[i:i + 2], 16) for i in (1, 3, 5)], float)


def tint(im, key):
    arr = np.asarray(im.convert('RGBA'), float)
    rgb, a = arr[..., :3], arr[..., 3:]
    s, m, h = (hex_rgb(c) for c in TRI[key])
    lum = (0.2126 * rgb[..., 0] + 0.7152 * rgb[..., 1] + 0.0722 * rgb[..., 2]) / 255
    lum = (np.clip((lum - 0.02) / 0.9, 0, 1) ** 0.92)[..., None]
    lo = s + (m - s) * np.clip(lum / 0.5, 0, 1)
    hi = m + (h - m) * np.clip((lum - 0.5) / 0.5, 0, 1)
    col = np.where(lum < 0.5, lo, hi) * 0.8 + rgb * 0.2
    return Image.fromarray(np.dstack([np.clip(col, 0, 255), a]).astype('uint8'), 'RGBA')


if __name__ == '__main__':
    src, dst, key = sys.argv[1:4]
    tint(Image.open(src), key).save(dst, 'WEBP', quality=88, method=6)
    print(dst)
