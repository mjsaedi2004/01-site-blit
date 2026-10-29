# Hero · «صحنه» (The Stage) · v3 · handoff spec

> **خلاصه برای خودت:** این فایل برای Claude دسکتاپه تا هیروی سایت اصلی رو دقیقاً مثل `index.html` همین پوشه بسازه. چیدمان، اندازه‌ها، رنگ‌ها، زمان‌بندی‌ها، جابه‌جایی پوسترها، سیستم تشخیص ریتم و فیلدهای پنل مدیریت اینجاست. `index.html` مرجع زنده‌ست؛ اگه جایی این متن با کد فرق داشت، کد درسته.

**Status:** v3, the third round. The owner's feedback on v2: too busy, the layout isn't interesting, the music reactions are bad, and the images should be graphic posters (like brochures), not concert photos. v3 is a calmer redesign around the event poster.
**Stack of the prototype:** HTML + CSS + vanilla JS + GSAP 3.13 (+ ScrollTrigger) + Web Audio. No WebGL.
**Source of truth:** `ui-reference/01-hero/v3/index.html`. The sample posters are built in `posters/source.html`.

---

## 0. Viewing the prototype

```bash
cd ui-reference/01-hero && npx http-server -p 8000
# open http://localhost:8000
```

- Use a server with HTTP range support (`http-server` has it), or the player can't seek. The songs aren't in git; see `assets/music/README.md`.
- The small round button at the left edge opens a review panel: poster swap style, music reaction, title font. **It's not part of the site.** Don't port it.
- `?debug` exposes `window.__hero` for tests. Don't port it.

---

## 1. Behaviour in one paragraph

The hero is one rounded **stage** that fits a desktop screen (1920×1080 down to 1280×720) with nothing overflowing, and it holds only a few things. The **featured event's poster** sits in the middle on a soft **halo of its own colours**, like the subject and circle of reference B. The event's name is on the right; the **date card** with the countdown and the **only buy button** is on the left. Along the bottom, the featured events («جایگاه ویژه», paid placements set in the admin panel) sit as **small posters**. A highlight **frame fades off one and onto the next** every 8 s, and a thin bar under it shows the time left. At each change the next poster **flies up out of the row** into the middle, and the previous one shrinks back into its slot. The halo and the background glow cross-fade to the new poster's colours. The week's playlist lives in a small **music pill**. While music plays, the halo breathes gently on each detected beat; nothing else moves with the music unless the review panel says so.

---

## 2. Layout

### 2.1 Frame
| Property | Value |
|---|---|
| Page | `background: #09080d`; `.app` padding `16px` top, `56px` bottom, sides `max(16px, env(safe-area-inset-*))` |
| Stage | `height: calc(100svh - 32px); min-height: 620px; max-height: 1200px; border-radius: 30px; overflow: hidden; background: #100f16` |
| Layers, bottom → top | `.amb` (two colour-blob sets + grain) → `.stage-grid` (the poster stage at z 1, everything else at z 2, so the halo stays behind the text) |

Ambient: each set holds two blurred discs (`78vmax`, radial gradient to transparent). The first is top-right in the poster's first glow colour at 0.26 opacity; the second is bottom-left in the second colour at 0.2. Grain: an SVG `feTurbulence` tile (220px, white noise at 9 % alpha), drawn once.

### 2.2 Grid (desktop, `dir="rtl"`)
```css
--ph: clamp(340px, calc(100svh - 360px), 720px);   /* poster height */
--pw: calc(var(--ph) * 2 / 3);                     /* posters are 2:3 */
--th: clamp(84px, 10.5svh, 116px);  --tw: calc(var(--th) * 2 / 3);   /* rail thumbnails */
--pad-x: clamp(20px, 2.2vw, 44px);
grid-template-columns: minmax(0, 1fr) var(--pw) minmax(0, 1fr);   /* column 1 is on the RIGHT in RTL */
grid-template-rows: auto minmax(0, 1fr) auto;
grid-template-areas: "nav nav nav" "info poster date" "ctrl rail player";
column-gap: clamp(36px, 5vw, 104px); row-gap: 18px; padding: 18px var(--pad-x) 26px;
```
- **info** (right, `justify-self: start`): category line → title → Nastaliq tagline → performer. Nothing else.
- **poster** (centre): halo, floor shadow, the poster.
- **date** (left, `justify-self: end`, 310px wide): the date card.
- **ctrl** (bottom right): «جایگاه ویژه» + «۰۱ از ۰۶» + previous / pause / next.
- **rail** (bottom centre): the small posters. It may be wider than the poster column and spill into the side tracks; those cells only hold the small ctrl and player blocks at the far edges.
- **player** (bottom left): the music pill, 310px.

### 2.3 Fit and breakpoints
Measured in the prototype: no block leaves the stage, no two blocks overlap and there's no horizontal scroll at 1920×1080, 1920×940, 1536×730, 1366×768 and 1280×720.

| Condition | Changes |
|---|---|
| `max-height: 820px` and `min-width: 901px` | row gap 12, padding-block `14px 20px`; date card tighter (day 60, month 26, button 52px); title `clamp(56px, 6.4vw, 120px)`, long `clamp(46px, 4.8vw, 92px)` |
| `901–1180px` wide | nav links tighter, rail counter hidden, date card 280px |
| `≤ 900px` (tablet, phone) | one column: nav → poster (`--pw: min(66vw, 330px)`, `--ph = 1.5 × --pw`) → info (centred) → date card (full width) → rail (horizontal scroll with snap, thumbnails 108px tall) → player (full width); rail controls hidden (auto-advance still runs) |

---

## 3. Tokens

### 3.1 Neutrals
| Token | Value | Use |
|---|---|---|
| `--ink-0` | `#09080d` | page |
| `--ink-1` | `#100f16` | stage base |
| `--card` | `rgba(255,255,255,.035)` | date card, pill (**no backdrop-filter**) |
| `--line` / `--line-2` | `rgba(255,255,255,.1)` / `.18` | borders |
| `--fg` / `--fg-2` / `--fg-3` | `#f5f2fa` / 72 % / 50 % | text |
| `--on-accent` | `#120d1c` | text and icons on the accent |

### 3.2 Colour comes from the poster
Each event stores an **accent** (buy button, frame, dots, tagline, waveform) and **two glow colours** (halo and ambient), all picked from its poster. `--accent` is set on `:root` **once**, 300 ms into a change, while the old text is fading out. **Don't put a transition on it**: an inherited variable that animates restyles the whole page every frame. The large accent surfaces fade by themselves (`transition: background-color .6s`). The halo and ambient colours are set on their own layers, and the two layers cross-fade (`opacity`, 1.1–1.3 s).

| Event (sample) | Category | accent | glow 1 | glow 2 |
|---|---|---|---|---|
| فرکانس | کنسرت پاپ | `#ff5c9f` | `#3552ff` | `#ff4f9a` |
| طیف | فستیوال الکترونیک | `#b396ff` | `#6d35ff` | `#19c8ff` |
| چهارمضراب | ارکستر | `#e8bc62` | `#1f9e94` | `#2b37a6` |
| سایه‌ها | تئاتر فیزیکال | `#ff6a52` | `#e0392b` | `#c9a77c` |
| بی‌تعارف | استندآپ کمدی | `#ffc83a` | `#ffb21f` | `#ff5fa2` |
| پرواز | سیرک خانوادگی | `#3fd6c8` | `#0f9e98` | `#e8473a` |

Rule for the accent: a light, saturated colour from the poster with at least 4.5:1 contrast against `#120d1c`.

### 3.3 Type
| Role | Font | Notes |
|---|---|---|
| Display (title, day number, brand) | **Lalezar** 400 | alternatives in the review panel: Noto Kufi Arabic 900 (`--title-k: .74`), Vazirmatn 900 (`.84`) |
| UI / body | **Vazirmatn** 300–900 | |
| Tagline only | **Noto Nastaliq Urdu** 600 | `line-height: 2`; loaded with `&text=` subsetting |

Sizes: title `clamp(64px, 7.2vw, 150px) × --title-k`; titles longer than 7 characters `clamp(52px, 5.4vw, 112px)`; tagline `clamp(22px, 1.9vw, 34px)`; performer 18/600; category line 14/600; date day 76, month 30, year 13; countdown digits 21; pill title 14.5/800.

### 3.4 Shape & motion constants
| | |
|---|---|
| Radii | stage 30, date card 24, poster 6, thumbnails 5 (frame 10), pill 999 |
| `--ease-out` | `cubic-bezier(.16, 1, .3, 1)` (≈ GSAP `expo.out`) |
| fly ease | `cubic-bezier(.7, 0, .2, 1)` |
| `--dur` | `8s`, one featured slot |

---

## 4. Components

### 4.1 Nav
Brand (SVG ticket in the accent with four HTML equaliser bars that move with the music) + «بلیت»; five category links with a sliding hover pill; search that expands to 260px with a self-typing placeholder; login. Mobile: menu button instead of the links.

### 4.2 Info (right)
- Category line: an accent dot, «کنسرت پاپ · پرفروش».
- **Title**: each word in `.w > .wi` (`.w` is `overflow: hidden` with padding and a negative margin so Persian ascenders and descenders aren't clipped).
- **Tagline** in Nastaliq, in the accent, written right → left by a mask (§10.5).
- Performer.

### 4.3 Poster stage (centre)
- **Halo**: a circle `1.34 × --ph` wide behind the poster. Radial gradient: glow 1 at 70 % at the centre, 34 % at 36 %, glow 2 at 20 % at 60 %, transparent at 76 %. Two layers cross-fade on change.
- **Floor shadow**: a blurred dark ellipse under the poster (`radial-gradient`, static).
- **Poster**: the image at `--pw × --ph`, radius 6, a layered shadow (`0 50px 90px -40px rgba(0,0,0,.9), 0 22px 40px -22px rgba(0,0,0,.8)`). There are two poster cards, the current one and the next, so a change never reloads the visible one.
- **Tilt** (fine pointers): the pointer position over the poster (−0.5…0.5) gives `rotateX(−y × 9°) rotateY(x × 12°)`. It's lerped `1 − e^(−6·dt)` in the frame loop on a `perspective: 1400px` stage. A soft light **sheen** (a 60 %-wide white gradient band) slides across with the pointer and fades in while hovering.
- **Click** → poster viewer: a full-screen dark layer with the poster at `min(92svh, 1500px)` tall, which grows out of the stage poster (FLIP, 0.7 s `expo.out`). Click or Esc shrinks it back (0.5 s).

### 4.4 Date card (left), reference B's date card
- «تاریخ اجرا» + reminder bell (toggle; the bell swings; a toast confirms).
- Day (Lalezar 76) + month (Lalezar 30) + year (13, muted).
- Rows: clock «سه‌شنبه، ساعت ۲۰:۳۰», pin + venue.
- **Countdown** box: «۴۶ روز ۰۲:۵۰:۱۳». The clock is LTR; each digit is an odometer strip of 20 cells inside a 1.12em window. Each second, changed digits roll 0.5 s `back.out(1.6)` and always roll the same way. On an event change every digit spins at least a full turn (0.9 s + 0.05 s per digit, `power3.inOut`). After the start time it reads «این اجرا برگزار شد». Screen readers get one sentence instead.
- **Buy button** (the only one): «خرید بلیت» + «از ۱٫۸ میلیون تومان», accent pill 58px tall with a dark circle and a ticket icon (tilts −14° on hover).
Dates are stored as ISO with the Tehran offset (`2026-12-15T20:30:00+03:30`) and formatted with `Intl.DateTimeFormat('fa-IR-u-ca-persian', { timeZone: 'Asia/Tehran' })`.

### 4.5 Featured rail (bottom centre)
- Six small posters, `--tw × --th`, 14px gaps, `role="tablist"`, each a `button role="tab"` with a label «فرکانس، کنسرت پاپ، ۲۴ آذر».
- Inactive: opacity 0.5. Hover: 0.9 and lift 4px. Active: opacity 1 and lift 10px.
- **Frame**: `inset: -6px`, radius 10, `1.5px` border in the event's accent, a 4px ring at 16 %, a coloured glow. Inactive `opacity 0; scale .9`; active `opacity 1` (0.55 s) and `scale 1` (0.7 s), `--ease-out`.
- **Time bar**: 2px under the active poster, filling from the right over `--dur`.
- **Auto-advance is driven by CSS**: the bar's `animationend` (`fillbar`) moves to the next event. Pausing sets `--play: paused` (read by `animation-play-state`). It pauses while the pointer is on the rail or the poster, while focus is in the rail, when the user presses pause, when the stage is off-screen, when the tab is hidden, while the poster viewer is open, and always under reduced motion (WCAG 2.2.2).
- Click a poster to feature it; click the active one to jump to the buy button. ArrowLeft = next, ArrowRight = previous (RTL), roving `tabindex`.

### 4.6 Music pill (bottom left)
- Round cover 44px (spins slowly while playing, like a record) · title + «دایان · ۸۰ ضرب در دقیقه» · four equaliser bars in the accent · a light play button (44px; a spinner while buffering).
- Clicking the title opens a **popover** above the pill. It holds the waveform seek bar (from the stored peaks, played part in the accent, hover preview, `role="slider"`, ArrowLeft/ArrowRight ±5 s), the LTR time row with previous/next, the playlist (cover, title, artist, BPM, duration), and «آهنگ خودت رو امتحان کن» (a local file, analysed on the spot). Esc or an outside click closes it.
- Audio loads only when the user presses play (`preload="none"`); the duration shown before that comes from the stored analysis.

### 4.7 Toast
Bottom centre, `role="status"`, slides up 0.5 s, leaves after 3.8 s.

---

## 5. Motion

### 5.1 Intro (first load, ~1.6 s)
| t (s) | What |
|---|---|
| 0 | ambient glow fades in (1.4 s) |
| 0.1 | halo grows from `scale .6` (1.8 s `expo.out`) |
| 0.15–0.3 | brand, links, tools drop in |
| 0.2 | the poster rises: `y 90 → 0`, `rotate -4° → 0`, fading in (1.3 s `expo.out`) |
| 0.5 | title words rise, the tagline is written |
| 0.55 | date card slides in from the left (30px) |
| 0.7 | rail posters rise in turn (`y 40`, stagger 0.06) |
| 0.85 | rail controls and the music pill |
| 1.0 | countdown spins |
Content is hidden only while JS runs (`.is-intro`, removed after 4 s as a failsafe).

### 5.2 Event change
1. Rail: the frame and the lift move to the new poster, and its time bar starts.
2. **Poster swap**, «پرواز از ردیف» (fly, default): FLIP between the rail and the stage, both 0.9–0.95 s on `cubic-bezier(.7,0,.2,1)`.
   ```js
   // r = stage poster box, t = a thumbnail's rect at rest (minus its lift), sc = the stage's current scale
   rel(t) = { x: (t.cx - r.cx) / sc, y: (t.cy - r.cy) / sc, s: t.width / r.width }
   incoming:  translate(rel(next).x, rel(next).y) scale(rel(next).s) rotate(-5deg)  →  none          (950 ms)
   outgoing:  none  →  translate(rel(prev).x, rel(prev).y) scale(rel(prev).s) rotate(4deg), fading out over the last 8 %   (900 ms)
   ```
   The incoming poster starts exactly on top of its thumbnail and the outgoing one lands exactly on its own thumbnail, so the two posters trade places. «ورق» (flip): the old poster turns `rotateY 0 → -90°` (360 ms, ease-in), then the new one turns `90° → 0` (620 ms, `--ease-out`). Reduced motion: a 0.5 s fade. Rapid input is safe; the running swap is finished first.
3. Halo and ambient cross-fade to the new glow colours.
4. Info: old words exit (`yPercent -110`, 0.32 s `power3.in`, stagger 0.035) and the rest fades (0.25 s). Then the new text renders: words `yPercent 118 → 0` (0.95 s `expo.out`, stagger 0.07), tagline written in 1.15 s.
5. Accent switches at 300 ms.
6. Date card: parts exit up (0.25 s) and enter from below (0.6 s `expo.out`); the countdown spins.

### 5.3 Reduced motion
No auto-advance; swaps are fades; digits jump; no tilt or sheen; the intro is a 0.5 s fade; the viewer opens without the zoom.

---

## 6. Posters

In production the poster is the image the organiser uploads: **2:3, at least 1200×1800**, WebP or JPG. The site needs two sizes, the full one for the stage and the viewer and a 400×600 thumbnail for the rail.

The six sample posters are original compositions made for this prototype in `posters/source.html`. `posters/render.js` renders them at 2× into `assets/posters/<id>.webp` and `<id>-thumb.webp`. They share one brochure-like system:
- a top line with the category and the full date, and a bottom line with the venue, time and «بلیت», each ruled off with a 1.5px line;
- one strong graphic motif per show;
- a large Persian title;
- print grain.

| Poster | Motif |
|---|---|
| فرکانس | two offset ring fields making a moiré disc (two voices, one frequency) |
| طیف | a fan of spectrum laser rays from one light source |
| چهارمضراب | a ten-fold girih rosette in gold over turquoise, Nastaliq title |
| سایه‌ها | a figure reaching for a red sun, its long shadow across the floor |
| بی‌تعارف | a black speech bubble on yellow, with halftone dots, a squiggle and sparkles |
| پرواز | a striped circus tent, a trapeze and an acrobat in mid-air |

---

## 7. Rhythm detection

Runs **once per track**. In production: when the admin uploads a song, run `analyseTrack(file)` (copy it from `index.html`) in the admin's browser or in a headless browser worker, and save the JSON next to the track. The public site only reads that JSON. Tracks without it fall back to live onset detection.

### 7.1 Algorithm (`analyseTrack`)
1. **Decode** at 22.05 kHz. Render offline at 16 kHz in **30 s chunks** (0.5 s pre-roll) through **10 band-pass filters** (`60 × 2^(0.75k)` Hz, k = 0…9, Q 1.9) plus the full signal. Chunking keeps memory at about 20 MB.
2. Frames of 10 ms (hop 160). Per band: energy in dB with an 80 dB floor below that band's maximum.
3. **Onset strength** = mean over bands of the positive dB rise frame to frame. Subtract a 0.4 s running mean, clip at 0, and divide by the RMS.
4. **Tempo**: autocorrelation of the onset curve over the whole track. Each lag L scores `(ac(L) + 0.5·ac(2L) + 0.25·ac(4L)) × prior`, with a log-normal prior at **100 BPM** and σ 0.75 octaves. The multiples favour the real beat over figures such as 3-3-2. The prior keeps the visual pulse in a comfortable 70–140 range. The best lag is refined with a parabolic fit.
5. **Beats** (dynamic programming, Ellis 2007): smooth the onset curve with a Gaussian (σ = period / 32). Each frame scores its onset plus the best previous beat 0.5–2 periods back, minus `100 × ln(gap / period)²`. Backtrack from the last strong peak, then trim weak beats at both ends. This gives **real beat times** that follow small tempo changes; a fixed grid drifts by about a second over a song.
6. **Downbeat**: the beat class (mod 4) with the strongest low-band onsets.
7. **Energy**: full-band RMS at 4 Hz, smoothed, normalised to the track's own 5th–95th percentile.
8. **Peaks**: 200 waveform maxima for the seek bar.
9. **Hook** (loudest 12 s) and **style** are also stored, for later sections such as a teaser. The v3 hero doesn't use them.

About 2–3 s for a 3-minute song on a laptop. Checked against librosa on the three sample songs: the beats match librosa's (at half its tempo) with an F-measure of 0.94 and 0.82 on two of them. On all three, the detected beats land on stronger onsets than librosa's own beats. «منم» is in a compound meter; librosa picks 99 BPM there, which doesn't fit its bar.

| Track | BPM |
|---|---|
| دایان · تا ابد تو | 80 |
| مجید رضوی · منم | 74 |
| آرون افشار · ثانیه وار | 76 |

### 7.2 Stored format
```jsonc
{
  "bpm": 80,                       // median beat interval → BPM
  "beats": [0.36, 1.14, 1.77, …],  // seconds, 3 decimals; ~2 KB for a 3-minute song
  "down": 0,                       // beat index mod 4 that starts a bar
  "energy": [0, 0.01, …],          // 4 Hz, 0–1 relative to the track
  "peaks": [0.84, 0.96, …],        // 200 values, 0–1, for the seek bar
  "hook": 167.8, "duration": 205.91, "drive": 0.7, "style": "pulse"
}
```

### 7.3 Live signals (every frame)
`<audio>` → `MediaElementSource` → `AnalyserNode` (fftSize 2048, smoothing 0.55, dB range −92…−16) → speakers. Shared object `A`:

| Signal | How |
|---|---|
| `level` | 0 → 1 when playing (rate 3/s), back to 0 at 2/s; everything is multiplied by it |
| `bands[48]` | log-spaced 40 Hz–12 kHz, attack 0.55, release 0.16 |
| `t` | `currentTime`, interpolated between media clock updates, minus `outputLatency` |
| beat | pointer into `beats` (binary search after a seek); each new beat sets `kick = max(kick, amp)` |
| `amp` | `(0.5 + 0.5 × energy) × gate`, with `gate = smoothstep(0.012, 0.07, live RMS)` so quiet passages stay calm |
| `kick` | decays `e^(−7.5t)` (≈ 0.15 s) |
| `energy` | from the stored curve, smoothed `e^(−2t)` |

If the server can't serve byte ranges, seeking falls back to fetching the file once and playing it from memory.

---

## 8. Music reactions (quiet on purpose)

| Mode | Look | Formula |
|---|---|---|
| **نفس هاله** (default) | the halo behind the poster breathes on every beat; the poster swells a hair | halo `scale(1 + (kick·0.045 + energy·0.02)·level)`; poster `scale(1 + kick·0.006·level)` |
| **رقص پوسترها** | the small posters in the rail bob with the music, alternating on the beat | each thumbnail `translate: 0 -(band·9 + kick·7 on alternate beats)·level px` (the `translate` property, so it doesn't fight the hover and active lift in `transform`) |
| خاموش | nothing moves with the music | — |

The pill's equaliser bars and the logo's bars follow four bands in every mode. All of it is `transform` only and stops once the music has faded out.

---

## 9. Admin panel fields

**Featured event** (the rail is the paid «جایگاه ویژه»; order and dates are set by the admin):
```jsonc
{
  "id": "frequency",
  "category": "کنسرت پاپ", "badge": "پرفروش",
  "performer": "گروه نیمه‌شب",
  "title": "فرکانس",
  "tagline": "لحظه را زندگی کن",           // short, set in Nastaliq
  "venue": "مجموعه ورزشی آزادی",
  "startsAt": "2026-12-15T20:30:00+03:30",
  "priceFrom": 1800000, "currency": "IRT",  // shown as «از ۱٫۸ میلیون تومان»
  "poster": { "src": "…", "thumb": "…", "w": 1200, "h": 1800 },
  "accent": "#ff5c9f", "glow": ["#3552ff", "#ff4f9a"],
  "featured": { "from": "…", "to": "…", "order": 1 }
}
```
On upload the server makes the 400×600 thumbnail and **suggests** the accent and the two glow colours from the poster, for example k-means on a 64×96 copy: the two largest saturated clusters for the glow, and the lightest saturated colour that passes 4.5:1 against `#120d1c` for the accent. The editor can change them and should see a live preview of the stage.

**Track**: `{ id, title, artist, url, cover?, analysis }`. On upload, run the analysis and store `analysis` (§7.2); show the BPM in the panel. Audio files need **CORS headers** if they're served from another host (the analyser reads them), and **range requests** for seeking.

---

## 10. Performance, RTL and accessibility rules

1. Continuous animations touch only `transform` and `opacity`. No `backdrop-filter`, no WebGL, no `mix-blend-mode` on moving layers, no animated masks.
2. Don't animate inherited custom properties on `:root` (§3.2).
3. No per-frame DOM writes that cause layout. Measured while music plays: 0 layouts per second, about 10–18 ms of style work per second.
4. One `requestAnimationFrame` loop, idle when the stage is off-screen, the tab is hidden or nothing plays.
5. **Persian:** never split text into characters for animation (it breaks the joins). Use Persian digits, Persian-calendar dates, and LTR clocks and media rows. Mirror arrows but not media icons. Nastaliq needs `line-height ≥ 2`. The tagline reveal uses `mask-image: linear-gradient(to left, #000 calc(var(--reveal) - 15%), transparent var(--reveal))` with `--reveal` registered as `<percentage>` and animated 0% → 115%.
6. **Accessibility:**
   - The stage is `aria-roledescription="carousel"`. The info region is `aria-live="off"` during auto-advance and `polite` after user navigation.
   - The rail is a tablist with a pause control.
   - Posters have `alt="پوستر …"`.
   - The player buttons are labelled, the waveform is a slider, and the countdown is read as one sentence.
   - Focus rings use the accent.

---

## 11. Porting notes (React / Next.js or similar)

Components: `<HeroStage>` (ambient + halo + two poster cards + tilt; receives `index` and the thumbnail rects) · `<EventInfo>` · `<DateCard>` · `<FeaturedRail events index onSelect>` · `<MusicPill tracks>` · `<PosterViewer>`.
- One store for `featuredIndex`, `paused`, `hover`, `reactMode`, `swapStyle`. Keep per-frame audio values (`A`) in a plain mutable object read by the rAF loop, **not** in React state.
- Drive auto-advance from the rail's CSS `animationend`, as the prototype does, so the timer and the bar can't drift apart.
- Run the poster swap with WAAPI from an effect keyed by `featuredIndex`; read the two thumbnail rects at click time (minus the lift).
- Server-render the first event so the hero reads before JS; hide only behind `.is-intro`.

---

## 12. Implementation checklist

- [ ] Tokens, fonts, `--accent` set once per change
- [ ] Stage grid that fits 1920×1080 → 1280×720; phone stack
- [ ] Ambient glow + halo cross-fades from the poster's colours
- [ ] Poster stage: two cards, fly and flip swaps, tilt + sheen, viewer
- [ ] Date card with the compact odometer countdown, reminder, the only buy button
- [ ] Featured rail: small posters, frame, time bar, CSS-driven auto-advance, pause rules, keyboard
- [ ] Info swap with word masks and the Nastaliq reveal
- [ ] Music pill + popover: real audio → analyser, stored analysis → beat clock, waveform seek, playlist with BPM, upload
- [ ] Music reaction modes (halo breathing default)
- [ ] Admin: poster upload with colour suggestions and preview; track upload with analysis
- [ ] Reduced-motion paths, a11y attributes

---

## 13. Credits

Posters: original sample artwork for this prototype (`posters/source.html`), using Lalezar, Vazirmatn, Noto Kufi Arabic and Noto Nastaliq Urdu (all SIL Open Font License). Songs: the owner's sample playlist, which is not in the repository (see `assets/music/README.md`). Event names, performers, prices and dates are sample content; the venues are real Tehran halls, used as realistic placeholders.
