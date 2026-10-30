# Hero · نسخه‌ی ۷ · عکس تمام‌صفحه و کادرهای کنار صفحه · handoff spec

> **خلاصه برای خودت:** عکس اجرا کل صفحه رو می‌گیره و چند کادر کوچیک کنار صفحه اجراهای دیگه رو نگه می‌دارن. خط پایین کادرِ فعال زمان‌سنجه. وقتی پر شد، عکس اجرای بعدی از دل کادرش باز می‌شه تا کل صفحه رو بگیره، و متن‌های همون اجرا سر جاشون میان. `index.html` همین پوشه مرجع زنده‌ست. دکمه‌ی گوشه‌ی پایین چپ حالت‌های دیگه رو نشون می‌ده.

**Status:** v7, new.

The owner asked for the first screen of leemeenal.app. In their words: a few small boxes at the side of the page; after a few seconds on each, the background becomes that box's picture and the related text takes its proper place. "Simple but attractive."

The site could not be opened from the build environment: every request to leemeenal.app was cut off. So v7 is built from that description alone. The parts that are guesses have options in the prototype panel:
- where the boxes sit
- how the picture changes
- how the title arrives
- how long each show stays

Shared with earlier versions and unchanged:
- **Sizing unit:** `--u`, 1% of the width on a 16:9 screen, smaller on wider ones (`../v5/SPEC.md`).
- **Music:** playlist, stored rhythm analysis, `audioSys` and `analyseTrack()` (`../v2/SPEC.md` §7).
- **Colours:** the fixed palette (`../v6/SPEC.md` §4).
- **Rules:** Persian/RTL (`../v2/SPEC.md` §11) and performance (`../v2/SPEC.md` §10).

---

## 1. Layout

```
┌──────────────────────────────────────────────────────────────────────┐
│ [buy] [login] (search) [♪ music]      categories           bars بلیت │  nav
│                                                                      │
│ ┌──────┐                               ۱ ─── کنسرت پاپ  (پرفروش)     │
│ │ box1 │◀ active                                                     │
│ └──────┘                                           فرکانس            │  huge title
│ ┌─────┐                                    گروه نیمه‌شب · تور ۱۴۰۵    │
│ │box2 │      (the show's photo fills       description, two lines    │
│ └─────┘       the whole screen)            date · time · venue       │
│   …                                        (details)  [buy | price →]│
│ ┌─────┐                                                              │
│ │box6 │                                                              │
│ └─────┘                                                              │
│ (→)(❚❚)(←)                                               ── ۶ / ۱    │  foot
└──────────────────────────────────────────────────────────────────────┘
```

- **Grid:** the hero is `100svh` tall (at least 600px) with three rows: `nav` / `copy boxes` / `foot`.
  - In RTL the words take the right column (`1fr`) and the boxes the left one (`auto`).
  - Padding is `1.5u` at the top and bottom and `3.2u` at the sides; the column gap is `4u`.
- **Words:** up to `46u` wide, vertically centred.
- **Boxes:** a column `12.5u` wide, vertically centred.
- **Background:** the picture sits behind everything (`z-index 0`), then the shade gradients, the beat light and the grain (`1`). The words and the boxes are above them.

The **row** option («ردیف پایین صفحه») moves the boxes into a row at the bottom left. The grid areas become `nav` / `copy copy` / `foot boxes`, and each box is `9.4u × 5.5u`.

---

## 2. The boxes

One box per featured show. The sample has six; the column fits up to seven on a 16:9 screen. Each box is a `role="tab"` button in a `role="tablist"`.

- **Size:** `12.5u × 6.1u`, radius `0.8u`, gap `0.7u`.
- **Picture:** the box holds the whole screen's picture, scaled down. It is the same DOM as the background layer, at the hero's width and height, with `transform: translate(-50%, -50%) scale(--bs)`, where `--bs = max(boxW / heroW, boxH / heroH)`. So a box shows exactly what it will open into, and the opening (§3) is one continuous movement.
- **Over the picture:** a dark gradient at the bottom, then two lines:
  - «۳ · ارکستر», the number and the type, at `0.58u` (at least 10px)
  - the name, bold, at `0.92u` (at least 12px)
- **Inactive:** opacity `.6`, `scale(.93)` toward the screen edge, and a 1px inner ring. On hover, opacity `.92`.
- **Active:** opacity 1, scale 1, and a 2px white inner ring. A 3px **timer line** runs along the bottom edge in the show's accent and fills from right to left.
  - The timer is a CSS animation (`fill`, `var(--dur)` long, `linear`). Its `animationend` moves on to the next show.
  - It pauses through `animation-play-state: var(--play)` when:
    - the pointer is over the boxes, or focus is inside them
    - the pause button is pressed
    - the hero is scrolled away, or the tab is hidden
    - the visitor prefers reduced motion (auto-advance starts off)
- **Duration:** 7 s by default. The panel offers 5 and 10 s.
- **Click:** opens that show. Clicking the active box moves focus to its buy button.
- **Keys:**
  - ArrowDown or ArrowLeft: next show.
  - ArrowUp or ArrowRight: previous show.
  - Home and End: first and last show.
  - Focus follows the active box (roving `tabindex`).

---

## 3. The change

| t (s) | What happens |
|---|---|
| 0 | The box becomes active, the counter's number rolls, and the old words leave upward. Each line sits in a mask and moves `yPercent: −110` over 0.34 s (`power3.in`), staggered by 0.016 s. The badge fades out. |
| 0 → 1.3 | The new picture **opens out of its box** (below). |
| 0.5 | The show's colours are written once. The new words rise into place: `yPercent 110 → 0`, 1.05 s, `expo.out`, staggered by 0.05 s, in the order number, category, title, performer, description, date, time, venue, price. The badge pops back with `back.out(2)`. |
| 1.3 | The layers underneath are let go. |

**The opening.** The background is a stack of layers (`.lay > .mv > .comp > img`). A change works like this:
1. It takes a free layer and draws the show's picture into it.
2. It waits for `img.decode()`.
3. It puts the layer on top and runs one progress value `p` from 0 to 1 over 1.3 s with `power3.inOut`.

```
box rectangle relative to the hero: bx, by, bw, bh        hero: W × H
s = max(bw / W, bh / H)        q = 1 − p
layer clip-path:  inset(by·q  (W − bx − bw)·q  (H − by − bh)·q  bx·q  round radius·q)
picture (.mv):    translate((bx + bw/2 − W/2)·q, (by + bh/2 − H/2)·q)  scale(s + (1 − s)·p)
layers underneath: .mv scale(1 + 0.06·p), a dark veil at opacity 0.55·p
```

- At `p = 0` the picture inside the clip is exactly the box's picture.
- The clip always lies inside the picture, because both move linearly and the clip starts and ends inside it. So no edge ever shows.
- The new layer sits under the boxes, so the picture seems to grow out from behind its box.
- **Several quick changes:** each opens on top of the last. A layer is let go once a layer above it has fully opened. At most three layers stay in the DOM. Layers that are still opening keep going underneath; only settled ones step back.

**Options in the panel:**
- **«محو و زوم»**, the fade. The new layer fades in over the first 70 % of 1.5 s while its picture settles from `scale(1.08)` to 1 (cubic out). The layers underneath step back a little (`1 + .03p`, veil `.4p`). This is also what happens when the box isn't on screen, as on a phone with the row scrolled away.
- **«پرواز از کادر»**, the flying title. The title leaves the box and grows into its place:
  1. A copy of the title is put exactly where the title will stand, already fitted.
  2. It is moved and shrunk onto the box's name: its right ends meet the name's and the middles of the lines meet. The transform origin is the title's right middle, and the scale is the name's font size divided by the title's.
  3. It is sent back over 1.2 s with `power3.inOut`. Its opacity rises in the first 0.3 s.
  4. When it lands, the real title takes over.
  5. When the new words arrive at 0.5 s and the block has moved, the copy is re-aimed at the title's new place.
- **Reduced motion:** no slow zoom and no opening. The picture cross-fades in 0.5 s, the words just fade, and auto-advance starts paused.

---

## 4. The picture

Each show has one wide photo. Its framing is data:

| Field | Meaning | Sample (فرکانس) |
|---|---|---|
| `z` | zoom of the picture (1 = cover) | 1.06 |
| `o` | origin of that zoom (and of the slow zoom) | `100% 40%` |
| `op` | `object-position` on wide screens | `50% 30%` |
| `mop` | `object-position` on phones (portrait crop) | `44% 50%` |

- **Slow zoom:** while a show is on, its picture zooms from `z` to `1.1·z`, linearly, over 2.4 × the show's duration (16.8 s by default). It is a CSS animation on `transform`, paused when the hero is off screen.
- **Legibility:** fixed gradients that never change with the show. They are dark on the right for the words (0.86 at the edge, 0.64 at 24 %, 0.2 at 50 %, clear by 64 %), at the top for the menu, at the bottom, and on the left for the boxes. The row layout makes the bottom one deeper.
- **Grain:** static SVG noise at 6 %.
- **Files:**
  - `photos/name-640.webp` for the boxes
  - `photos/name-1920.webp` and `name-2560.webp` for the background (`srcset` with `sizes="100vw"`)
  - After the intro, every show's full picture is preloaded one at a time, so each change opens at once.

**What makes a good photo:** landscape, at least 1920px wide, with the person or the stage on the left or in the middle. The right third will sit under the words.

---

## 5. When a show only has a poster

This is the «اگه فقط پوستر باشه» option; in the sample, «چهارمضراب» and «بی‌تعارف» switch to their posters.

- **Background:** the poster itself, drawn once at 160×90 with `blur(6px) saturate(1.3)` into a data URL, covering the screen. A 30 % dark veil goes over it. A tiny picture blurred once is cheap to show full-screen and cheap to animate; a CSS `filter: blur()` on a full-screen layer is not.
- **The poster:** it stands in a frame between the boxes and the words.
  - Its centre is at `(--pfx, --pfy)`: `(34 %, 51 %)` in the column layout, `(30 %, 43 %)` in the row layout and `(50 %, 30 %)` on phones.
  - Its height is `--pfh` of the hero: 64 %, 56 % and 38 % respectively. Its width follows the poster's ratio.
  - It is rotated −2.5°, with a radius of 1.4 % of the hero height, a deep shadow and a 1px light edge.
- **Boxes:** the box shows the same composition, so the opening works exactly as with a photo.

---

## 6. Words

- **Kicker:** the show's number (in the palette's `light` tone), a `3u` line, the category, and a badge pill tinted with the accent («پرفروش», «آخرین بلیت‌ها» …).
- **Title:** the show's name in Noto Sans Arabic 900 at width 62.5, `9.4u`, line-height 1.12, on one line.
  - It shrinks to fit its column through `--tf`, the column width divided by the name's width.
  - The longest sample name, «چهارمضراب», needs 0.99.
- **Performer:** `1.3u`, weight 300.
- **Description:** `0.9u`, line-height 1.95, up to `34u` wide.
  - It always takes two lines of space (three on phones) and is clamped to them. So the block has one height for every show and nothing jumps when the words change.
  - All sample descriptions fit.
- **Meta row:**
  - the date in the Persian calendar (`Intl.DateTimeFormat('fa-IR-u-ca-persian', { timeZone: 'Asia/Tehran' })`)
  - the time
  - the venue
  - Each has an icon in the `light` tone.
- **Buttons:**
  - **«خرید بلیت»:** a white pill showing «از ۹۵۰ هزار تومان» behind a thin divider, and a round arrow button in the accent. The arrow icon uses the palette's `onAccent` colour.
  - **«جزئیات اجرا»:** an underlined text button.
- **Numbers:** Persian digits without a leading zero. «۰۱» reads badly, because the Persian zero is a small ring.

---

## 7. Bottom row and menu

- **Counter:** the current number rolls (out up, in from below). A thin line shows the position among the shows and fills from the right.
- **Controls:** previous, pause/resume auto-advance (`aria-pressed`) and next.
- **Menu:** the logo bars (an equaliser while music plays), the categories, the music pill, search, «ورود» and a white «خرید بلیت» pill.

---

## 8. Music

- **Player:** a pill in the menu: play/pause, the title and artist, and four equaliser bars. The title opens a panel with:
  - the cover
  - a waveform you can scrub (LTR)
  - previous and next
  - the playlist, with each song's tempo and length
  - «آهنگ خودت رو امتحان کن»
- **Songs:** the same tracks and stored analysis as v2–v6.
- **Reactions, «تپش پس‌زمینه و نور» (default):**
  - **Background:** it swells on each beat: `.bg { transform: scale(1 + (kick · 0.012 + downbeat · 0.006) · level) }`.
  - **Light from below:** in the show's accent, at opacity `(kick · 0.55 + energy · 0.22) · level`, capped at 0.85.
  - **Logo bars:** each follows one frequency band, relative to that band's own recent average, so quiet and loud songs both move.
  - **Play button:** its ring pulses on the beat.
- **Reactions, «فقط نشانگرها»:** only the bars move.
- **Writes:** every per-frame write is a `transform` or an `opacity`, written only when the value changes.

---

## 9. Smaller screens

- **1100px wide and below:** the categories and «ورود» are hidden, and a menu button appears.
- **760px wide and below (phones):**
  - The words sit at the bottom, and the boxes are a swipeable row under them (`31vw × 19vw`). The active box is scrolled into view without moving the page.
  - Under the words the gradient is deeper.
  - The title is `min(16vw, 84px)`.
  - The description gets three lines; it is hidden when the phone is shorter than 700px.
  - «جزئیات اجرا» is hidden.
  - The opening starts from the box when it is on screen and falls back to the fade when it isn't.

---

## 10. Data model

```
{ id, pal: 'violet' | 'blue' | 'teal' | 'green' | 'gold' | 'orange' | 'crimson' | 'pink',
  type, cat, name, by, badge, desc, venue, startsAt, price, track,
  photo:   { name, z, o, op, mop },          // files: photos/name-{640,1920,2560}.webp
  poster?: { src, thumb, r } }               // used when there is no photo
```
`pal` keys the fixed palette. v7 uses three of each set's colours:
- `accent` for the lines, the light and the arrow button
- `light` for small coloured text on the photo
- `onAccent` for the arrow icon

---

## 11. Measured

- **Fit:** in both layouts, there is no horizontal scroll, nothing outside the hero, no overlap and no clipped or cut description at:
  - 1920×1080, 1920×1028 (inside the comparison page) and 1920×940
  - 2560×1300, 1536×730 and 1440×900
  - 1366×768, 1366×650, 1280×720, 1280×600 and 1024×768
  - 390×844 and 360×700
- **Motion:**
  - The opening and the flying title were checked frame by frame on GSAP's own clock.
  - After five quick clicks 120 ms apart, and after fourteen changes in a row, the screen ends with one layer showing, the right title, number and active box, and no flying copy left behind.
  - The layer pool stays at three.
- **Cost** (main thread, software rendering, 1920×1080):

  | State | Script | Style |
  |---|---|---|
  | Idle | about 3 ms/s | 6 ms/s |
  | During a change | 8 ms/s | 18 ms/s |
  | With music playing | 11 ms/s | 33 ms/s |

  There is no layout per frame.

---

## 12. To confirm with the owner

The real site was never seen, so these are guesses:
- **Boxes:** a column at the side (default) or a row at the bottom?
- **Box content:** the picture with the name, or something else?
- **The change:** opening out of the box (default) or a fade?
- **The title:** rising into place (default) or flying out of the box?
- **Timing:** 7 s per show.

A screen recording or a few screenshots of leemeenal.app would settle all of them. So would allowing the domain in the environment's network settings.
