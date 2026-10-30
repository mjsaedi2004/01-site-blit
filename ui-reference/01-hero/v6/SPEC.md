# Hero · نسخه‌ی ۶ · هر فایلی که مدیریت داره · handoff spec

> **خلاصه برای خودت:** صحنه همون نسخه‌ی ۵ـه؛ وسط صحنه با هر فایلی که مدیریت داره پر می‌شه:
> - **پوستر یا بنر برگزارکننده:** دست‌نخورده می‌شه طرح یه «بلیت بزرگ» افقی، با ته‌بلیت قیمت و بارکد.
> - **عکس هنرمند، یا پوستری که آدم داره:** سرور آدم رو جدا می‌کنه و به رنگ اجرا درمیاره.
> - **هیچ عکس خوبی نیست:** یکی از آبجکت‌های آماده (نورافکن، بادکنک، میکروفون، توپ دیسکو، دف) به رنگ اجرا.
>
> رنگ هر اجرا از یه پالت ثابت ۸ تایی میاد و خودکار از روی خود تصویر پیشنهاد می‌شه. `index.html` همین پوشه مرجع زنده‌ست، با یه پنل مدیریت نمونه برای امتحان.

**Status:** v6, new. It is built on v5, which the owner liked («خیلی بهتره»). The owner pointed out two things:
- Admins can't hand-make tinted cut-outs for every show. What they actually get from organisers is a poster or a banner.
- A plain tall poster in the middle of the stage "doesn't look good".

The owner also asked for a fixed palette and no video. Everything not described here is unchanged from `../v5/SPEC.md`: layout and the `--u` unit, the halo, copy, cards, countdown, player, music and motion rules.

---

## 1. The idea

The middle of the stage shows one of three things. Everything else on the stage stays the same, and the change from one show to the next works between any two of them.

| Visual | When | What the visitor sees |
|---|---|---|
| **ticket** | the organiser sent a poster or a banner (any ratio) | the poster, untouched, as the art of a big landscape ticket: a stub with brand, seat type, price, barcode and serial; notches on the perforation; a coloured ghost ticket behind; slightly turned (−4°) in front of the halo |
| **cutout** | there is a photo of the artist, or a poster with the artist on it | the person without a background, tinted in the show's colour, standing in front of the halo (as in v5) |
| **emblem** | no usable picture | a ready-made 3D object, tinted in the show's colour, floating in the halo |

**Why a ticket and not a framed poster:** a ticket is wider than tall even for a 9:16 story, because the stub adds width. So the stage never shows a lone tall rectangle. It is also on brand (the site is «بلیت»), and the poster stays exactly as the organiser made it, which organisers of big concerts usually insist on.

---

## 2. What the admin does

The panel in `index.html` («پنل مدیریت · نمونه», the tab on the left edge) runs all of this in the browser. The production version should look the same.

1. **File:** drop or pick a poster, banner, or photo.
   - The panel shows what it found: «پوستر عمودی ۴:۵ · ۱۰۸۰×۱۳۵۰», «بنر عریض ۱۶:۹», «پست مربع ۱:۱», «استوری ۹:۱۶», or «عکسِ بدون پس‌زمینه».
   - The demo also has six sample files.
2. **Display**, suggested automatically:
   - *ticket* is offered for any picture.
   - *cutout* is suggested when the file has no background or the server found a person in it. It is disabled, with a note explaining why, when there is no person to cut out.
   - *emblem* opens a picker of the ready-made objects, already tinted in the current colour.
3. **Colour:** eight swatches. The one suggested from the picture is marked «پیشنهاد». The admin can pick another.
4. **Text:** the type (title line 1), the name (line 2), the venue and the price. The other fields are the same as in v5.
5. Every change is shown on the real stage at once. The show joins the featured row and becomes active, and auto-advance pauses while the panel is open.

---

## 3. What the server does on upload

| Step | Detail |
|---|---|
| Read the file | Accept JPEG/PNG/WebP, at least 1000px on the short side for posters; warn below that. Note the ratio and whether there is transparency (more than 5 % of pixels below alpha 245). |
| Suggest the colour | See §4. |
| Find a person | Run background removal: we used `rembg` with `isnet-general-use`; a human-segmentation model such as `u2net_human_seg` or BiRefNet also works. It runs on the site's own server, so there is no paid foreign API. It takes about 2–20 s on CPU. Then clean up as in the next row. If the remaining shape is too small (under ~8 % of the image), don't offer *cutout*. |
| Clean up the cut-out | Keep only the largest connected shape: this drops poster type and logos. Dilate it 8px. Apply the confidence curve `a' = clamp((a − .1) / .42)`, because hands against busy backgrounds come out half-transparent. Pull the background's colour out of half-transparent edge pixels, crop to the subject, and fade the bottom 22 %. Store it as a neutral WebP with alpha, at most 1500×1700. |
| Tint | Tritone with the palette entry's `tri` colours, keeping 20 % of the original: `out = tritone(lum') * .8 + rgb * .2`, where `lum' = ((lum − .02)/.9)^.92`. Bake the tinted version for the chosen colour. The admin preview tints live in the browser with the same recipe (`tinted()` in `index.html`). |
| Ticket art | Keep the original. Make a 520px thumbnail for the featured card. Wide banners are cropped at 26 % from the left on the card, because in RTL banners the picture usually sits on the left. Store an optional focal point if the admin sets one. |
| Placement | For cut-outs: `fig { h, x, b, flip }` (v5 §4.1). Defaults: busts `h: 80`; full-body PNGs (ratio < .7) `h: 96`. The admin can nudge it on the preview. |

`tools/extract_person.py` does all of this, and `tools/tint.py` bakes the tint. **Example:** «استندآپ بی‌تعارف» in the sample data was made this way, by taking the comedian out of `assets/posters/standup-4x5.webp`, a poster with a red curtain and a yellow type band. It took 17 s on the container's CPU. Automatic extraction isn't perfect against busy backgrounds: one fingertip comes out a little pale. So the admin always sees the preview, and can choose *ticket* instead if the cut-out isn't clean.

---

## 4. The fixed palette

Eight sets. Every colour on the stage comes from the show's set. The set is written once per change, never animated as a variable.

| Key | Name | accent | light | deep | pop | text on accent | tri: shadow · mid · highlight |
|---|---|---|---|---|---|---|---|
| violet | بنفش | `#8b5cf6` | `#c4b5fd` | `#2e1065` | `#facc15` | white | `#0d0620` · `#7c3aed` · `#f0e6ff` |
| blue | آبی | `#3b82f6` | `#93c5fd` | `#0c2a6b` | `#facc15` | white | `#050a20` · `#2563eb` · `#e2ecff` |
| teal | فیروزه‌ای | `#14b8a6` | `#5eead4` | `#053d37` | `#facc15` | `#03201c` | `#021412` · `#0d9488` · `#dcfff9` |
| green | سبز | `#22c55e` | `#86efac` | `#05391b` | `#facc15` | `#03200f` | `#03140a` · `#16a34a` · `#dcfce7` |
| gold | طلایی | `#d9a441` | `#f5d48b` | `#4a300a` | `#a78bfa` | `#1a1206` | `#140b03` · `#b7791f` · `#fff1d6` |
| orange | نارنجی | `#f97316` | `#fdba74` | `#5a2205` | `#a78bfa` | `#1b0d03` | `#170a02` · `#ea580c` · `#ffe9d6` |
| crimson | سرخ | `#e11d48` | `#fda4af` | `#4c0519` | `#facc15` | white | `#170309` · `#be123c` · `#ffe1e8` |
| pink | صورتی | `#ec4899` | `#f9a8d4` | `#500724` | `#facc15` | white | `#1a0410` · `#db2777` · `#ffe4f1` |

**Suggestion** (`suggestPalette()`):
1. Shrink the picture to 64px wide.
2. Skip transparent, grey (saturation < .28) and dark (value < .2) pixels.
3. Build a 36-bin hue histogram weighted by `s²·v`, and smooth it by its neighbours.
4. Take the peak hue and snap it to the palette entry with the nearest accent hue.
5. If the vivid weight per pixel is under 0.003 (a black-and-white picture), suggest violet, the brand colour.

Results on the samples:

| Sample | Suggested |
|---|---|
| neon festival banner | violet |
| black-and-white orchestra poster with gold type | gold |
| circus post | teal |
| theatre story | crimson |
| comedian cut-out | orange |

---

## 5. The big ticket

**Geometry** is computed in JS from the scene's size and the image's ratio `r` (`tix.size`):
```
ah = min(0.5 × sceneHeight, 0.9 × sceneWidth / (r + 0.42))   // art height (phones: 0.56 and 0.94)
aw = ah × r                                                  // art width, the image's own proportions
sw = max(0.42 × ah, 92px)                                    // stub width
```
- The ticket is centred at (50 %, 41 cqh), with explicit `left`/`top` offsets. Don't use the CSS `translate` property: GSAP bakes a percentage translate into pixels, so a later ticket of another size lands off-centre.
- The art sits on the right and the stub on the left, which is the ticket's end in RTL.
- The perforation is a 2px dashed line, with notches cut by a radial-gradient mask at `x = sw` (radius `.05 × ah`).

**Layers**, bottom to top:
- **Ghost ticket:** accent→deep gradient, `rotate(7°)`, shifted 5 %.
- **Tilt group:** the cursor tilts it up to 9° × 12° around a base `rotate(−4°)`.
  - **Soft shadow:** a separate element, because a masked element can't cast its own shadow.
  - **Card:** art and stub.
  - **Gloss band:** sweeps across once per change.

**Stub:**
- **Background:** the deep colour, with a soft accent bloom at the top and a slight darkening, so white text stays readable on every palette.
- **Content**, top to bottom: «● بلیت»; then the seat type and «از ۱٫۲ میلیون» in the condensed title font; then a CSS barcode and «№ 0342».
- **Sizing:** the stub is a size container, so its type is set in `cqh`/`cqw` and always fits.

**Motion:**
- **In:** `yPercent 16 → 0`, `rotation −12° → 0`, `rotationY 55° → 0`, `scale .9 → 1`, opacity (1.45 s `expo.out`, perspective 1400). The ghost follows 0.15 s later. The gloss sweeps at 0.45 s.
- **Out:** `rotationY −70°`, `rotation 6°`, `yPercent 8`, fade (0.5 s `power2.in`).
- **Music:** the ticket swells `scale(1 + kick·.006)`; the halo behind it reacts as in v5.

Never tint, crop or redraw the organiser's poster on the stage. Only the featured card uses a cropped thumbnail.

---

## 6. The left card for a show with a ticket

When the show is on the stage as a big ticket, the small paper ticket in the left card would repeat it. Instead the card turns over (the same flip as v5) to a **calendar page**, like reference B's date card:
- the day, large;
- month and year in the light colour;
- weekday and time;
- the venue with a pin.

The kind, seat and price lines below stay.

---

## 7. Featured cards

Each card shows what its show stands on the stage with:
- **Cut-outs:** the tinted cut-out, anchored at the bottom (mirrored when the show's cut-out is).
- **Objects:** the tinted object, centred.
- **Posters:** the thumbnail, cover-cropped (portrait at 22 % from the top, wide banners at 26 % from the left).

The card's frame, timer and arrow use the show's palette, as in v5.

---

## 8. Ready-made objects

| Key | Object | Use for | Placement `fig` |
|---|---|---|---|
| spotlight | نورافکن (stage fresnel with barn doors) | theatre, concerts | `h 50, b 30` |
| balloons | بادکنک | family, kids, circus | `h 64, b 22` |
| microphone | میکروفون | stand-up, concerts | `h 58, b 26` |
| discoball | توپ دیسکو | festivals, parties | `h 60, b 26` |
| daf | دف | Iranian music | `h 50, b 30` |

- **Placement:** objects float in the middle of the halo, not anchored to the bottom, and sway ±3° over 7 s.
- **Making them:** they are studio renders made with three.js. The scenes are in `tools/emblems.html` and `tools/render-emblems.js` renders them. They use neutral grey materials with plenty of mid-tones, because the tint maps brightness onto the palette.
- **Format:** transparent WebP, at most 1100px.
- **Adding more:** a designer can replace them with higher-end renders, or add objects such as tar, kamancheh, piano, theatre masks or a film reel, as long as they are neutral grey with transparency.

---

## 9. Data model

```
{ id, palette: 'violet' | … | 'auto', type, cat, lines[2], name, chip, tagline, description, badge, mood,
  venue, startsAt, ticket { kind, seat, priceFrom, serial }, track,
  visual:
    { type: 'ticket', src, thumb, from: 'poster' | 'banner', focal? }
  | { type: 'cutout', src (neutral cut-out), from: 'photo' | 'poster', poster?, fig { h, x, b, flip } }
  | { type: 'emblem', emblem: 'spotlight' | 'balloons' | 'microphone' | 'discoball' | 'daf' } }
```
When `palette` is `'auto'`, the suggested key is stored at upload, so the visitor's browser never has to compute it.

---

## 10. Measured

- **Fit:** with a ticket on stage, there is no horizontal scroll, nothing outside the stage, no overlap and no clipped text at:
  - 1920×1080 and 1920×1028 (inside the comparison page)
  - 1920×940, 2560×1300, 1536×730, 1440×900
  - 1366×768, 1366×650, 1280×720, 1280×600, 1024×768
  - 390×844
- **Motion:** the change works between every pair of types: photo → banner ticket, poster ticket → object, object → cut-out. After fast clicking (four changes 120 ms apart), the stage ends with exactly one visual showing.
- **Playing music:** about 13 ms of script and 22 ms of style work per second, with no per-frame layout. That is the same as v5.
- **Live tinting:** about 50 ms for a 1500×1700 cut-out, cached per picture and colour.
- **Admin demo:** tested with all six samples and with a real file upload.
