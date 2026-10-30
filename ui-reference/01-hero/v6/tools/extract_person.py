"""Take the person out of a photo or a poster, the way the server does on upload (SPEC §3).

    python3 extract_person.py in.jpg out.webp [--fade 0.22]

Needs: rembg (with the isnet-general-use model), numpy, scipy, Pillow.
Steps: background removal -> keep the largest connected shape (drops poster type and logos) ->
confidence curve (hands against busy backgrounds come out half transparent) -> pull the background's
colour out of the half-transparent edge -> crop to the subject -> fade the bottom -> neutral WebP with alpha.
The page (or the server) tints the result in the show's colour; see tint.py.
"""
import sys
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage
from rembg import new_session, remove


def extract(src, fade=0.22, min_share=0.08):
    rgb_im = Image.open(src).convert('RGB')
    cut = remove(rgb_im, session=new_session('isnet-general-use'))
    a = np.asarray(cut.getchannel('A'), float) / 255
    lab, n = ndimage.label(a > 0.25)
    if not n:
        return None
    sizes = ndimage.sum(a > 0.25, lab, range(1, n + 1))
    if sizes.max() < min_share * a.size:
        return None  # nothing person-sized: don't offer the cut-out
    keep = ndimage.binary_dilation(lab == 1 + int(np.argmax(sizes)), iterations=8)
    a = np.clip((a * keep - 0.1) / 0.42, 0, 1)
    a = ndimage.gaussian_filter(a, 0.6)
    rgb = np.asarray(rgb_im, float)
    # background colour behind each edge pixel: the removed area, spread inwards by a wide blur
    bgw = (a < 0.02).astype(float)
    blur = lambda x: np.asarray(Image.fromarray(np.clip(x, 0, 255).astype('uint8')).filter(ImageFilter.GaussianBlur(12)), float)
    wsum = blur(bgw * 255) / 255
    bg = np.dstack([blur(rgb[..., c] * bgw) for c in range(3)]) / np.maximum(wsum, 1e-3)[..., None]
    edge = (a > 0.02) & (a < 0.9) & (wsum > 0.05)
    al = np.maximum(a, 0.35)[..., None]  # a gentle un-mix: a strong one overshoots into the opposite colour
    fg = np.clip((rgb - (1 - al) * bg) / al, 0, 255)
    mix = rgb * 0.4 + fg * 0.6
    grey = (0.2126 * mix[..., 0] + 0.7152 * mix[..., 1] + 0.0722 * mix[..., 2])[..., None]
    rgb[edge] = (mix * 0.5 + grey * 0.5)[edge]  # and half the colour off the edge, which the tint replaces anyway
    ys, xs = np.where(a > 0.08)
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    pad = int(0.03 * (y1 - y0))
    x0, y0 = max(0, x0 - pad), max(0, y0 - pad)
    x1, y1 = min(a.shape[1] - 1, x1 + pad), min(a.shape[0] - 1, y1 + pad)
    rgb, a = rgb[y0:y1 + 1, x0:x1 + 1], a[y0:y1 + 1, x0:x1 + 1]
    if fade:
        h = a.shape[0]
        a = a * (np.clip(np.arange(h)[::-1] / (h * fade), 0, 1) ** 1.4)[:, None]
    out = Image.fromarray(np.dstack([rgb, a * 255]).astype('uint8'), 'RGBA')
    out.thumbnail((1500, 1700), Image.LANCZOS)
    return out


if __name__ == '__main__':
    args = sys.argv[1:]
    fade = float(args[args.index('--fade') + 1]) if '--fade' in args else 0.22
    res = extract(args[0], fade)
    if res is None:
        sys.exit('no person found')
    res.save(args[1], 'WEBP', quality=88, method=6)
    print(args[1], res.size)
