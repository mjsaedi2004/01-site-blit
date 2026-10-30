# Hero · نسخه‌ی ۷ · خلوت: عکس تمام‌صفحه و چهار کادر کنار صفحه · handoff spec

> **خلاصه برای خودت:** یه عکس کل صفحه رو می‌گیره و تا وقتش تموم بشه آروم زوم می‌شه. چهار کادر کوچیک کنار صفحه اجراها رو نگه می‌دارن و خط باریک پایین کادر فعال زمان رو نشون می‌ده. وقتی وقت تموم شد، پوستر بعدی خیلی نرم از وسط صفحه باز می‌شه و پوستر قبلی همون موقع جلوتر میاد و کمی تاریک می‌شه. متن فقط چهار تیکه‌ست، پایین گوشه‌ی راست. `index.html` همین پوشه مرجع زنده‌ست. دکمه‌ی گوشه‌ی پایین چپ حالت‌های دیگه رو نشون می‌ده.

**Status:** v7, second round.

The owner asked for the first screen of leemeenal.app: a few small boxes at the side of the page; after a few seconds on each, the background becomes that box's picture and the related text takes its place; "simple but attractive".

The first round was "much too busy". The owner asked for:
- **Sparse, like the reference:** at most four posters.
- **Zoom:** each poster zooms in a little while its seconds pass.
- **The change:** after that, the next poster comes in very softly from the middle of the screen, exactly as in the reference.

The site still can't be opened from the build environment: every request to leemeenal.app is cut off. So the opening is a reading of that description. The prototype panel offers alternatives for it:
- a hard-edged frame from the middle
- a fade
- three zoom amounts
- three durations

Shared with earlier versions and unchanged:
- **Sizing unit:** `--u`, 1% of the width on a 16:9 screen, smaller on wider ones (`../v5/SPEC.md`).
- **Music:** playlist, stored rhythm analysis, `audioSys` and `analyseTrack()` (`../v2/SPEC.md` §7).
- **Colours:** the fixed palette (`../v6/SPEC.md` §4).
- **Rules:** Persian/RTL (`../v2/SPEC.md` §11) and performance (`../v2/SPEC.md` §10).

---

## 1. Layout

```
┌──────────────────────────────────────────────────────────────────────┐
│ ورود  ♪ تا ابد تو ▮▮▮▮      کنسرت تئاتر استندآپ خانوادگی   bars بلیت  │  nav
│                                                                      │
│ ┌─────┐                                                              │
│ │ box │◀ active                                                      │
│ └─────┘          (the show's photo fills the screen                  │
│ ┌────┐            and slowly zooms in)                               │
│ │box │                                                               │
│ └────┘                                                               │
│ ┌────┐                                            کنسرت پاپ · ۲۴ آذر  │
│ │box │                                                  فرکانس       │  title
│ └────┘                               گروه نیمه‌شب · مجموعه ورزشی آزادی │
│ ┌────┐                                  (←) از ۱٫۸ میلیون  خرید بلیت  │
│ │box │                                                               │
│ └────┘ (❚❚)                                                          │
└──────────────────────────────────────────────────────────────────────┘
```

- **Grid:** the hero is `100svh` tall (at least 600px) with two rows: `nav` / `copy side`.
  - In RTL the words take the right column (`1fr`) and sit at its bottom.
  - The side column (`auto`, on the left) holds the boxes and the pause button, vertically centred.
  - Padding is `1.5u` at the top, `3u` at the bottom and `3.2u` at the sides.
- **Nothing else:**
  - the menu has the logo, four categories, the music button and «ورود»
  - the words are four lines
  - there is no counter, badge, description or icon row

---

## 2. The boxes

At most four shows; each box is a `role="tab"` button in a `role="tablist"`.

- **Size:** `10.5u × 6u`, radius `0.7u`, gap `0.65u`.
- **Picture:** the box holds the whole screen's picture, scaled down. It is the same DOM as the background layer, at the hero's size, with `transform: translate(-50%, -50%) scale(--bs)`, where `--bs = max(boxW / heroW, boxH / heroH)`. So the box shows exactly what will open.
- **Name:** the show's name at the bottom, `0.78u`, over a dark gradient.
- **Inactive:** opacity `.55` and `scale(.94)` toward the screen edge. On hover, opacity `.9`.
- **Active:** opacity 1, scale 1, and a 1.5px white inner ring. A 2px line along the bottom edge fills from right to left in the show's accent. That line is the show's time (§3).
- **Click:** opens that show. Clicking the active box moves focus to the buy button.
- **Keys:**
  - ArrowDown or ArrowLeft: next show.
  - ArrowUp or ArrowRight: previous show.
  - Home and End: first and last show.
  - Focus follows the active box.
- **Pause button:** a small round button under the boxes (`aria-pressed`).

The **row** option («ردیف پایین صفحه») puts the boxes in a row at the bottom left, each `9u × 5.3u`.

---

## 3. A show's time: the slow zoom

One GSAP tween per show, 7 s long by default, with linear easing, drives two things together:
- **The line:** the active box's line, `scaleX(p)`.
- **The zoom:** the picture's scale, `scale(z · (1 + 0.12 · p))`.
  - `z` is the photo's framing zoom; the origin is the photo's `o`.
  - 0.12 is the «متوسط» zoom; the panel also offers 0.06 («کم») and 0.20 («زیاد»).

When it ends, the next show opens.

**Pausing.** The tween pauses, so the line and the zoom stop together, when:
- the pointer is over the boxes, or focus is inside them
- the pause button is pressed
- the hero is scrolled away, or the tab is hidden

**Reduced motion:** no zoom, and auto-advance starts paused.

**Duration:** 7 s by default; the panel offers 5 and 10 s. A new duration keeps how far through the show the line is.

---

## 4. The change: soft, from the middle

| t (s) | What happens |
|---|---|
| 0 | The box becomes active and the old words leave upward. Each line is in a mask and moves `yPercent: −110` over 0.5 s (`power3.in`), staggered by 0.04 s. |
| 0 → 2.2 | The next picture opens from the middle of the screen, while the old picture keeps coming towards the viewer (below). |
| 0.85 | The show's colour is written once and the new words rise into place: `yPercent 110 → 0` over 1.3 s (`expo.out`), staggered by 0.08 s. |
| 2.2 | The layers underneath are let go and the new show's time (§3) starts from zoom 0. |

**The opening («باز شدن نرم از وسط», default).** Each layer is `.lay > .iris > .mv > .comp > img`.

The opening runs one progress value `p` from 0 to 1, linearly, over 2.2 s, with `e = easeInOutSine(p)`:

```
.iris   carries a fixed soft ellipse mask: radial-gradient(closest-side, #000 60%, transparent 100%)
        transform: scale(k),  k = max(0.04, 2.4 · e)         (at 2.4 the screen's corners are inside the solid core)
.mv     transform: scale(grow / k),  grow = 0.86 + 0.14 · easeOutCubic(p)
.lay    opacity: smoothstep(0, 0.15, p)                       (the first moment is a fade, not a dot)
```

- Only transforms and opacity change per frame. The mask itself never changes, so it is drawn once and the compositor scales it.
- Changing the mask's gradient per frame was measured: it was about 25 % slower in software rendering.
- The picture inside the ellipse grows from 86 % to full size while it opens. So the whole screen seems to move towards the viewer.

**The old picture keeps moving.** It continues from the speed its slow zoom had, `v0 = zoom / duration` per second (0 if it was paused), and accelerates evenly:
- It adds `push = 0.16` of scale over the 2.2 s: `.mv scale(1 + v0·t + ½·a·t²)` with `a = 2·(push − v0·T) / T²`.
- A dark veil goes over it at `0.3 · e`.

So nothing stops and restarts; it is one continuous movement.

**Other openings in the panel:**
- **«قاب از وسط»** (1.7 s): a rounded rectangle in the screen's proportions grows from the centre with `clip-path: inset(…)`. The radius goes from 26px to 0. The picture grows from 86 % the same way.
- **«محو»** (1.5 s): the new layer fades in over the first 80 % of the time, while its picture settles from 1.05 to 1.

**Intro:** the first picture opens the same way from the middle, out of the dark page.

**Quick clicking:** each change opens on top of the last. A layer is let go once a layer above it has fully opened. At most three layers stay in the DOM.

---

## 5. The picture

Each show has one wide photo. Its framing is data:

| Field | Meaning | Sample (فرکانس) |
|---|---|---|
| `z` | zoom of the picture (1 = cover) | 1.04 |
| `o` | origin of that zoom and of the slow zoom | `50% 40%` |
| `op` | `object-position` on wide screens | `50% 30%` |
| `mop` | `object-position` on phones (portrait crop) | `44% 50%` |

- **Legibility:** kept light, so the photo breathes.
  - A radial darkening in the bottom-right corner under the words (0.8 at the corner, clear by 62 %).
  - A band at the top for the menu, and one on the left for the boxes.
  - The row layout adds one at the bottom.
- **Grain:** static SVG noise at 6 %.
- **Files:**
  - `photos/name-640.webp` for the boxes
  - `photos/name-1920.webp` and `name-2560.webp` for the background (`srcset` with `sizes="100vw"`)
  - After the intro, every show's full picture is preloaded one at a time.

**What makes a good photo:** landscape, at least 1920px wide, with the subject in the middle or on the left. The opening starts in the middle, and the bottom-right corner will sit under the words.

---

## 6. When a show only has a poster

This is the «اگه فقط پوستر باشه» option; in the sample, «چهارمضراب» switches to its poster.

- **Background:** the poster itself, drawn once at 160×90 with `blur(6px) saturate(1.3)` into a data URL, covering the screen. A 30 % dark veil goes over it.
- **The poster:** it stands in a frame between the boxes and the words.
  - Its centre is at `(--pfx, --pfy)`: `(40 %, 47 %)` in the column layout, `(34 %, 40 %)` in the row layout and `(50 %, 32 %)` on phones.
  - Its height is `--pfh` of the hero: 60 %, 54 % and 40 % respectively.
  - It is rotated −2.5°, with a radius of 1.4 % of the hero height and a deep shadow.
- **Behaviour:** the poster zooms and opens exactly like a photo.

---

## 7. Words

Four lines in the bottom-right corner, up to `40u` wide:
1. **Kicker:** the category and the date, «کنسرت پاپ · سه‌شنبه ۲۴ آذر». It uses the Persian calendar (`Intl.DateTimeFormat('fa-IR-u-ca-persian', { timeZone: 'Asia/Tehran' })`), `0.82u`.
2. **Title:** the show's name in Noto Sans Arabic 900 at width 62.5, `7.4u`, on one line. It shrinks to fit its column (`--tf`).
3. **Performer and venue:** «گروه نیمه‌شب · مجموعه ورزشی آزادی», `1.02u`, weight 300.
4. **Buy button:** a white pill: «خرید بلیت», then the starting price in grey, then a round arrow in the accent. The arrow icon uses the palette's `onAccent`.

---

## 8. Menu and music

- **Menu:** the logo with its five bars, four categories, the music button and «ورود».
- **Music button:**
  - a round play button
  - the song's name (it opens the playlist)
  - four small bars
- **Playlist panel:**
  - the cover
  - a waveform you can scrub
  - previous and next
  - the list, with each song's tempo
  - «آهنگ خودت رو امتحان کن»
- **Songs:** the same tracks and stored analysis as v2–v6.
- **Reactions:**
  - **«تپش آروم تصویر»** (default): the whole picture swells very slightly on each beat, `scale(1 + (kick·0.01 + downbeat·0.005)·level)`. The logo bars follow frequency bands relative to their own recent average, the button's bars follow the song, and the play button's ring pulses.
  - **«فقط میله‌ها»:** only the bars move.

---

## 9. Smaller screens

- **1100px wide and below:** the categories are hidden.
- **760px wide and below (phones):**
  - The words sit at the bottom.
  - The four boxes are a row under them; each takes a quarter of the row at 16:10, and the pause button sits at the row's end.
  - Under the words the gradient is deeper.
  - The title is `min(15vw, 80px)`.

---

## 10. Data model

```
{ id, pal: 'violet' | 'blue' | 'teal' | 'green' | 'gold' | 'orange' | 'crimson' | 'pink',
  type, cat, name, by, venue, startsAt, price, track,
  photo:   { name, z, o, op, mop },          // files: photos/name-{640,1920,2560}.webp
  poster?: { src, thumb, r } }               // used when there is no photo
```
At most four shows on the hero.

`pal` keys the fixed palette. v7 uses three of each set's colours:
- `accent` for the time line and the arrow button
- `light` for the playlist's tempo
- `onAccent` for the arrow icon

---

## 11. Measured

- **Fit:** in both layouts, there is no horizontal scroll, nothing outside the hero, no overlap and no clipped text at:
  - 1920×1080, 1920×1028 (inside the comparison page) and 1920×940
  - 2560×1300, 1536×730 and 1440×900
  - 1366×768, 1366×650, 1280×720, 1280×600 and 1024×768
  - 390×844 and 360×700
- **Motion:**
  - The openings were checked frame by frame on GSAP's own clock.
  - The time line and the zoom stop and go together with the pointer over the boxes and with the pause button.
  - After five quick clicks 120 ms apart, and after fourteen changes in a row, the screen ends with one layer showing, the right words and active box, and no mask left behind.
  - The layer pool stays at three.
- **Frame rate** (software rendering in the test machine, so far below a real GPU; the comparison is what matters): during a change, about 27 frames/s for the soft opening and 40 for the frame and the fade. The idle screen runs at 60.
- **Cost of music:** about 15 ms of script and 29 ms of style work per second, with no layout per frame.

---

## 12. To confirm with the owner

The real site was never seen, so these are guesses:
- **The opening:** a soft ellipse from the middle (default), or a hard frame from the middle?
- **Zoom:** 12 % per show, linear.
- **The new picture:** it grows from 86 % to full size while it opens.
- **Timing:** 7 s per show and a 2.2 s opening.

A screen recording of leemeenal.app's first screen would settle them. So would allowing the domain in the environment's network settings.
