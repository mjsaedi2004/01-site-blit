# Hero · «صحنه» (The Stage) · v2 · handoff spec

> **خلاصه برای خودت:** این فایل برای Claude دسکتاپه تا هیروی سایت اصلی رو دقیقاً مثل `index.html` همین پوشه بسازه. اندازه‌ها، رنگ‌ها، زمان‌بندی‌ها، فرمول‌های تعویض پس‌زمینه، الگوریتم تشخیص ریتم و فیلدهای پنل مدیریت همه اینجاست. `index.html` مرجع زنده‌ست؛ اگه جایی این متن با کد فرق داشت، کد درسته.

**Status:** v2, the second round. It answers the owner's feedback on v1: sharper photos, too laggy, dull motion, a countdown that was too big, a featured row like reference B, Iranian songs with rhythm detection, a choice of reaction modes, and a fit in 1920×1080.
**Stack of the prototype:** HTML + CSS + vanilla JS + GSAP 3.13 (+ ScrollTrigger) + Web Audio. No WebGL.
**Source of truth:** `ui-reference/01-hero/index.html`.

---

## 0. Viewing the prototype

```bash
cd ui-reference/01-hero && npx http-server -p 8000
# open http://localhost:8000
```

- Use a server with HTTP range support (`http-server` has it), or the player can't seek. The songs aren't in git; see `assets/music/README.md`.
- The floating **«تنظیمات نمونه»** button opens a review panel: reaction mode, background transition, title font, colour mode, and a song upload. **It's not part of the site.** Don't port it.
- `?debug` exposes `window.__hero` for tests. Don't port it.

---

## 1. Behaviour in one paragraph

The hero is one rounded **stage** that fits a desktop screen (1920×1080 and down to 1280×720) with nothing overflowing. Behind it is a sharp photo of the **featured event**. Along the bottom runs the **featured rail** («جایگاه ویژه», paid placements chosen in the admin panel), a row of image cards like reference B. A highlight **frame fades off one card and onto the next** every 8 s. The active card's photo slowly zooms and a thin bar under it shows the time left. On each change, the new background **grows out of the active card** until it fills the stage. The title words swap, the colour accent follows the event, and the **date card** (left column, reference B's date card) updates its compact countdown. Above the date card sits a **music player** with the week's Iranian playlist. Each song has been **analysed for rhythm** (every beat time, the downbeat, energy), so the stage reacts on the beat in one of four light modes. In **auto** mode the song itself picks the mode.

---

## 2. Layout

### 2.1 Frame
| Property | Value |
|---|---|
| Page | `background: #07060b`; `.app` padding `16px` top, `56px` bottom, sides `max(16px, env(safe-area-inset-*))` |
| Stage | `height: calc(100svh - 32px); min-height: 640px; max-height: 1240px; border-radius: 30px; overflow: hidden` |
| Layers, bottom → top | `#bg` (z0) → `.scrim` (z1) → `#react` music layer (z2) → `.stage-grid` content (z3) |

`#bg` contains `.bg-pulse` (used by the pulse mode) → two `.bg-layer`s (current and next) → `.bg-in` (the transition's transform) → `.bg-zoom` (Ken Burns) → `img.bg-img` (focal-point placement). Each layer also has a `.bg-dim` overlay.

Scrim (RTL, so the dark side is on the right, under the text):
```css
linear-gradient(to left,   rgba(7,6,11,.9) 0%, rgba(7,6,11,.7) 24%, rgba(7,6,11,.3) 44%, rgba(7,6,11,0) 60%),
linear-gradient(to top,    rgba(7,6,11,.92) 0%, rgba(7,6,11,.55) 18%, rgba(7,6,11,0) 36%),
linear-gradient(to bottom, rgba(7,6,11,.7) 0%, rgba(7,6,11,0) 15%),
linear-gradient(to right,  rgba(7,6,11,.66) 0%, rgba(7,6,11,.2) 20%, rgba(7,6,11,0) 30%);
```

### 2.2 Grid (desktop, `dir="rtl"`)
```css
--side-w: clamp(296px, 19vw, 364px);
--pad-x: clamp(18px, 1.7vw, 34px);
grid-template-columns: minmax(0, 1fr) var(--side-w);   /* column 1 is on the RIGHT in RTL */
grid-template-rows: auto minmax(0, 1fr) auto;
grid-template-areas: "nav nav" "info side" "rail side";
gap: 16px 28px; padding: 18px var(--pad-x) 24px;
```
- **info** (right): chips → performer → title → Nastaliq tagline → description → CTAs → social proof. `max-width: 660px`, vertically centred.
- **side** (left, spans info + rail rows): player at the top, date card at the bottom (`justify-content: space-between`), so the date card's bottom lines up with the rail.
- **rail** (bottom, under info): head (label, counter, ← ⏸ →) and the card row.
- The photo's focal point lands at **(0.36, 0.44)** of the stage on desktop and **(0.5, 0.3)** on mobile. That's between the side column and the text.

### 2.3 Fit and breakpoints
Measured in the prototype: no element leaves the stage and there's no horizontal scroll at 1920×1080, 1920×940 (a 1080p screen minus browser chrome), 1536×730 (1080p at 125 % scaling), 1440×900, 1366×768 and 1280×720.

| Condition | Changes |
|---|---|
| `max-height: 860px` and `min-width: 901px` | gaps `12px 24px`, padding-block `14px 18px`; title `clamp(60px, 6.8vw, 124px)`, long `clamp(52px, 5.4vw, 100px)`; tagline `clamp(22px, 1.9vw, 30px)`; social proof hidden; date day 46 / month 26; tighter cards |
| `max-height: 740px` and `min-width: 901px` | description and the venue row hidden |
| `901–1180px` wide | nav links tighter, city button hidden |
| `≤ 900px` (tablet, phone) | one column: nav → info → rail → side; stage `height: auto`; `#bg`, `#react` and the scrim cover the top `min(90svh, 820px)` and the photo fades out with a mask; info gets `padding-top: clamp(200px, 40svh, 360px)` so it reads like a poster; rail becomes a native horizontal scroll with snap, cards `min(290px, 80%)` × 132px; rail subtitle and counter hidden; the "window" transition falls back to a fade |

---

## 3. Tokens

### 3.1 Neutrals
| Token | Value | Use |
|---|---|---|
| `--ink-0` | `#07060b` | page |
| `--ink-1` | `#0e0c15` | stage base |
| `--panel` | `rgba(14,12,22,.82)` | cards (**no backdrop-filter**) |
| `--panel-hi` | `rgba(24,20,36,.9)` | hover |
| `--line` / `--line-2` | `rgba(255,255,255,.09)` / `.17` | borders |
| `--fg` / `--fg-2` / `--fg-3` | `#f6f3fb` / 76 % / 54 % | text |
| `--on-accent` | `#120d1c` | text and icons on accent fills |
| `--live` | `#ff4d6a` | the pulsing "selling" dot |

### 3.2 Accent (one per event)
```css
@property --accent      { syntax: '<color>'; inherits: true; initial-value: #5aa2ff; }
@property --accent-deep { syntax: '<color>'; inherits: true; initial-value: #1f4fd6; }
```
Set both on `:root` **once**, 300 ms after a change starts, while the old text is fading out. **Don't put a transition on these variables.** An inherited variable that animates makes the browser restyle the whole page every frame. In v1 that was about 100 ms of style work per change; now it's about 18 ms. The large accent surfaces (buy button, seat button, play button, logo) fade on their own with `transition: background-color .6s` / `fill .6s`. The music layer lerps its own copy of the colour in JS (`1 − e^(−3.6·dt)`).

| Event (sample) | Category | `--accent` | `--accent-deep` |
|---|---|---|---|
| فرکانس | کنسرت پاپ | `#5aa2ff` | `#1f4fd6` |
| طیف | فستیوال الکترونیک | `#ff4fd8` | `#a21caf` |
| چهارمضراب | ارکستر | `#a78bfa` | `#6d28d9` |
| سایه‌ها | تئاتر فیزیکال | `#ff6a4d` | `#c2361b` |
| بی‌تعارف | استندآپ کمدی | `#ffb547` | `#c2410c` |
| پرواز | سیرک خانوادگی | `#2ee6c8` | `#0f9e88` |
| brand (colour mode «بنفش ثابت») | — | `#a78bfa` | `#6d28d9` |

### 3.3 Type
| Role | Font | Notes |
|---|---|---|
| Display (titles, digits, brand) | **Lalezar** 400 | Alternatives in the review panel: Noto Kufi Arabic 900 (`--title-k: .74`), Vazirmatn 900 (`.84`) |
| UI / body | **Vazirmatn** 300–900 | |
| Tagline only | **Noto Nastaliq Urdu** 600 | `line-height: 2`; loaded with `&text=` subsetting, so subset to the real taglines or self-host |

Sizes: title `clamp(70px, 8.2vw, 166px) × --title-k`; titles longer than 7 characters `clamp(58px, 6.4vw, 128px)`; tagline `clamp(24px, 2.2vw, 40px)`; performer 18/600; body 15/1.9; chips 13/500; rail card title 22 (Lalezar); date day 56, month 30; countdown digits 24.

### 3.4 Shape & motion constants
| | |
|---|---|
| Radii | stage 30, cards 22, rail cards 18, chips/pills 999 |
| `--ease-out` | `cubic-bezier(.16, 1, .3, 1)` (≈ GSAP `expo.out`) |
| `--ease-io` | `cubic-bezier(.65, 0, .35, 1)` |
| `--dur` | `8s`, one featured slot |
| `--card-h` | `clamp(92px, 10.8svh, 124px)`; 132px on mobile |

---

## 4. Components

### 4.1 Nav
- Brand: an SVG ticket in the accent with 4 equaliser bars on top. The bars are **HTML elements**, because changing an SVG element's transform re-lays-out the SVG every frame. While music plays they scale with 4 frequency bands; at rest they're still.
- Centre pill of category links; a highlight pill slides under the hovered or focused link (`transform` + `width`, 0.5 s).
- Search circle expands to 268px and its placeholder types itself. City «تهران», login. Mobile shows a menu button instead of the links.

### 4.2 Info block
- Chips: category (icon in the accent) and a status badge with a pulsing dot. The pulse is a pseudo-element animating `transform` and `opacity`, not a `box-shadow`.
- Performer → **title** (each word in `.w > .wi`; `.w` is `overflow: hidden` with padding and a negative margin so Persian ascenders and descenders aren't clipped) → **tagline** (Nastaliq, accent, soft glow) → description (46ch) → CTAs → social proof (avatars + «۱۲۰ هزار نفر …», counts up on load).
- Buy button: accent pill «خرید بلیت» + price, dark circle with a ticket icon; a shine sweeps on hover; magnetic on fine pointers (`dx × .18`, `dy × .28`, back with `elastic.out(1, .35)`).
- Teaser button: a 54px circle with an expanding ring, «تماشای تیزر / ۹ ثانیه، با موزیک».

### 4.3 Featured rail («جایگاه ویژه»), reference B
- Head: star + «جایگاه ویژه» + «اجراهای منتخب این هفته» · counter `۰۱ / ۰۶` · previous (→), pause/play, next (←).
- Row layout: as many cards as fit at ≥ 210px wide (6 at 1920, 5 at 1536, 4 at 1280–1440), widened to fill the row, 12px gaps. If the active card is outside the visible window, the track slides (`translate3d`, 0.8 s `--ease-out`).
- **Card anatomy** (a `button`, `role="tab"`):
  - photo `720×360` WebP, `object-fit: cover`, cut from the same master as the background (§6.1);
  - bottom gradient `rgba(7,6,11,.94) → 0` at 76 %;
  - a dim layer (`.5`) that fades out on hover and on the active card (0.6 s);
  - category chip at the top start corner with the event's colour dot;
  - title (Lalezar 22) and «۲۴ آذر · سالن ۱۲ هزار نفری» at the bottom;
  - 3px progress bar on the bottom edge, filling from the right over `--dur`;
  - **highlight frame**: `inset: -4px`, radius 22, `1.5px` border in the card's colour, a 4px ring at 15 %, a coloured glow. Inactive: `opacity 0; scale .94`. Active: `opacity 1` (0.55 s) and `scale 1` (0.7 s), both `--ease-out`. That makes the frame fade off one card and land on the next.
- Active card motion: the photo zooms `transform: scale(1 → 1.14)` linearly over `--dur`. Hover uses the separate `scale` property (`1 → 1.06`, 0.9 s), so hover and the slow zoom never fight, and the card lifts 4px.
- **Auto-advance is driven by CSS**: the progress bar's `animationend` (`fillbar`) moves to the next card. Pausing sets `--play: paused`, which every running animation reads through `animation-play-state`. It pauses while the pointer or focus is on the rail, when the user presses pause, when the stage is off-screen, when the tab is hidden, while the teaser is open, and always under reduced motion (WCAG 2.2.2).
- Click a card to feature it; click the active card to buy. Keyboard: `role="tablist"`, **ArrowLeft = next, ArrowRight = previous** (RTL), roving `tabindex`.

### 4.4 Side column: player
- Head row: «پلی‌لیست هفته · ۸۰ ضرب», a 6px **beat dot** that pulses on every detected beat (it shows the rhythm detection at work), like (heart burst of 9 particles), playlist.
- Cover 54px (track artwork, or a cover drawn on canvas from the title and two colours). When playing, a vinyl slides out from behind the cover (`translate: -24px 0`) and spins (1.8 s per turn), and the cover's end margin grows to 22px so it doesn't touch the title.
- **Waveform = seek bar**: drawn from the stored `peaks` (one bar per ~5px), played part in the accent, hover preview, bars near the playhead jump with the beat. `role="slider"`; ArrowLeft/ArrowRight seek ±5 s.
- Transport row is **LTR** (elapsed, ⏮ ▶ ⏭, duration), following media conventions even in RTL. A spinner shows while buffering.
- Playlist popover: cover, title, artist, **BPM**, duration, an EQ on the current track, and «آهنگ خودت رو امتحان کن» (local file, analysed on the spot).
- Audio loads only when the user presses play (`preload="none"`); the duration shown before that comes from the stored analysis.

### 4.5 Side column: date card (reference B), with the countdown inside it
- «تاریخ اجرا» + reminder bell (toggle; the bell swings; a toast confirms).
- Day (Lalezar 56) + month (Lalezar 30, accent) + weekday pill.
- Rows: clock «ساعت ۲۰:۳۰», pin and venue (ellipsis).
- **Compact countdown** box: «۴۷ روز و ۰۲:۵۰:۱۳ تا اجرا». The clock is LTR; each digit is an odometer strip of 20 cells (`۰–۹ ۰–۹`) inside a 1.12em window. Each second, changed digits roll 0.5 s `back.out(1.6)` and always roll the same way. On an event change, every digit spins at least a full turn (0.9 s + 0.05 s per digit, `power3.inOut`). The days number slides in. Screen readers get one sentence instead («۴۷ روز و ۲ ساعت تا اجرا مانده»).
- Capacity: a 5px bar in the accent gradient (`scaleX` = sold %, 1.1 s `expo.out`) and «۸۲٪ ظرفیت پر شده». The label is rewritten only when the integer changes.
- «رزرو صندلی» button.

### 4.6 Teaser (9 s)
A full-screen `<dialog>` with letterbox bars. It opens as a `clip-path: circle()` from the button (0.9 s `expo.inOut`). The photo zooms from 1.25 to 1.02 over 9 s. «{performer} تقدیم می‌کند» shows from 0.7 to 2.3 s. At 2.8 s the title words rise (1.2 s `expo.out`) while the title scales from 1.3 to 1. An accent light sweeps right → left at 3.0 s. The tagline is written right → left at 4.1 s. The date, buy and replay appear at 6.2 s, and a progress line runs underneath. If no music is playing, the current track starts **from its loudest 12 s** (`analysis.hook`) and stops again when the teaser closes.

### 4.7 Toast
Bottom centre, `role="status"`, slides up 0.5 s, leaves after 3.8 s.

---

## 5. Motion

### 5.1 Intro (first load, ~1.8 s)
| t (s) | What |
|---|---|
| 0 | background fades in (1.4 s) and settles from `scale 1.08` (2.2 s) |
| 0.15–0.3 | brand, nav pill, tools drop in (−22 / −18 / −14 px) |
| 0.45 | title words rise, the tagline is written, chips, performer and description fade up |
| 0.7 | side cards rise (34px, stagger 0.12), rail head |
| 0.75 | rail cards slide in from the start side (`x: 70`, stagger 0.07) |
| 0.85 | CTAs and proof rise |
| 1.0 | countdown spins; «۱۲۰ هزار» counts up |
Content is hidden only while JS runs (`.is-intro`, set by an inline script and removed after 4 s as a failsafe). Use `fromTo` / `from` with `clearProps`.

### 5.2 Event change
1. Rail: frame and dim move to the new card, its slow zoom and progress bar start, and the track slides if needed.
2. Background: the chosen transition (§6.2), about 1.15 s.
3. Info: old title words exit (`yPercent -110`, 0.32 s `power3.in`, stagger 0.035) while the rest fades (0.25 s). Then the new text renders and enters: words `yPercent 118 → 0` (0.95 s `expo.out`, stagger 0.07), tagline written in 1.15 s, other parts `y 12 → 0` (0.7 s).
4. Accent switches at 300 ms (§3.2).
5. Date card: parts exit up and enter from below (0.25 s + 0.6 s `expo.out`), the countdown spins, the capacity bar animates.
6. The music layer re-centres on the new focal point (lerp `1 − e^(−4·dt)`).
Rapid input is safe. A pending background change is finished or cancelled before the next one, through a token plus `settle()`. A running info swap is killed.

### 5.3 Ambient
Background Ken Burns (`scale 1 → 1.05`, 11 s, linear, origin at the focal point), active-card zoom, live dot ping, teaser ring, countdown separators blinking.

### 5.4 Micro-interactions
Magnetic buttons, the nav hover pill, search expand, like burst, bell swing, playlist pop (0.4 s `expo.out`, items stagger 0.04). On scroll the stage scales to 0.95 and its radius grows to 44px (ScrollTrigger scrub).

### 5.5 Reduced motion
No auto-advance (the user moves through the rail). Every background change is a 0.45 s fade. Digits jump instead of rolling. The intro is a 0.5 s fade. No magnetic buttons. The teaser opens without the circle wipe. Music reactions still follow the beat, but nothing loops on its own.

---

## 6. Background

### 6.1 Photos and focal point
Each event stores one master photo (≥ 3200 px wide) and a **focal point** `fit = { x, y, zoom }` (0–1 of the photo) for its subject. For the card it also stores `card` (crop width as a fraction of the photo width, default 0.6) and optionally `cy` (the card crop's own vertical centre).

Placement ("cover" around the focal point):
```js
k  = max(W / imgW, H / imgH) * (mobile ? 1 : fit.zoom)        // fit.zoom ≤ 1.3
dw = imgW * k;  dh = imgH * k
ox = clamp(tx * W - fit.x * dw, W - dw, 0)                     // (tx, ty) = (.36, .44) desktop, (.5, .3) mobile
oy = clamp(ty * H - fit.y * dh, H - dh, 0)
img: width dw, height dh, transform translate3d(ox, oy, 0)
file: smallest of 1920 / 2560 / 3200 with width ≥ dw × min(devicePixelRatio, 2)
```

Card crop (2:1). The generator and the page use the same formula:
```js
w = fit.card || .6;  h = w * imgW / 2 / imgH
x = clamp(fit.x - w / 2, 0, 1 - w);  y = clamp((fit.cy ?? fit.y) - h / 2, 0, 1 - h)
```

### 6.2 Transitions (only `clip-path`, `transform` and `opacity`, all WAAPI)
- **پنجره «window»** (default): a shared-element move. At t = 0 the new background shows **exactly the card's crop at the card's place**: the layer is clipped to the card rect, and `.bg-in` is transformed so the same photo pixels line up. Then the clip and the transform grow together to the full stage. Both run 1.15 s with `cubic-bezier(.7,0,.16,1)`, so the image always covers the clip, and the old layer dims to 0.6.
  ```js
  // card rect (unscaled stage px) {x, y, w, h}, its image zoom z, crop c, bg placement {ox, oy, dw}
  cw = c.w * imgW;  ch = c.h * imgH
  kc = max(w / cw, h / ch) * z                  // card px per photo px (object-fit: cover)
  sx0 = c.x * imgW + (cw - w / kc) / 2;  sy0 = c.y * imgH + (ch - h / kc) / 2
  k = dw / imgW;  s = kc / k
  from: clip-path inset(y, W-x-w, H-y-h, x round 18px);  .bg-in transform: translate(x - s*(ox + sx0*k), y - s*(oy + sy0*k)) scale(s), origin 0 0
  to:   clip-path inset(0 round 0);                     .bg-in transform: none
  ```
  Read the card rect after the rail's slide target is known (add the track's pending offset), divide by the stage's current scale (it shrinks on scroll), and read the card image's current `scale` (hover). If the card isn't inside the background box (mobile), use the fade.
- **محو «fade»**: opacity 0 → 1 (0.9 s, ease-out) and `scale 1.08 → 1` (1.6 s, `--ease-out`).
- **پرده «blinds»**: the new photo is cut into 7 vertical strips (5 on mobile). Each strip slides in from above or below, alternating (`translateY ±102% → 0`, 0.8 s `cubic-bezier(.76,0,.24,1)`), from right to left with a 55 ms stagger. The old layer dims to 0.5.

When a transition ends, the new layer gets `.is-active`, which starts its Ken Burns, and the old layer is hidden.

---

## 7. Rhythm detection

Runs **once per track**. In production: when the admin uploads a song, run `analyseTrack(file)` (copy it from `index.html`) in the admin's browser or in a headless browser worker, and save the JSON next to the track. The public site only reads that JSON. Tracks without it fall back to live onset detection.

### 7.1 Algorithm (`analyseTrack`)
1. **Decode** at 22.05 kHz. Render offline at 16 kHz in **30 s chunks** (0.5 s pre-roll) through **10 band-pass filters** (`60 × 2^(0.75k)` Hz, k = 0…9, Q 1.9) plus the full signal. Chunking keeps memory at about 20 MB.
2. Frames of 10 ms (hop 160). Per band: energy in dB with an 80 dB floor below that band's maximum.
3. **Onset strength** = mean over bands of the positive dB rise frame to frame. Subtract a 0.4 s running mean, clip at 0, and divide by the RMS.
4. **Tempo**: autocorrelation of the onset curve over the whole track. Each lag L scores `(ac(L) + 0.5·ac(2L) + 0.25·ac(4L)) × prior`, where the prior is log-normal at **100 BPM** with σ 0.75 octaves. The multiples favour the real beat over rhythmic figures such as 3-3-2. The prior keeps the visual pulse in a comfortable 70–140 range. The best lag is refined with a parabolic fit.
5. **Beats** (dynamic programming, Ellis 2007): smooth the onset curve with a Gaussian (σ = period / 32). Each frame scores its onset plus the best previous beat 0.5–2 periods back, minus `100 × ln(gap / period)²`. Backtrack from the last strong peak, then trim weak beats at the start and the end. This yields **real beat times** that follow small tempo changes; a fixed grid drifts by about a second over a song.
6. **Downbeat**: the beat class (mod 4) with the strongest low-band onsets.
7. **Energy**: full-band RMS at 4 Hz, smoothed, normalised to that track's own 5th–95th percentile.
8. **Peaks**: 200 waveform maxima for the seek bar.
9. **Hook**: the loudest 12 s, skipping the first and last 15 s, for the teaser.
10. **Style** for auto mode: `drive` = autocorrelation at half a beat ÷ at one beat (how busy the off-beats are). `beams` if drive > 0.75 and mean energy > 0.55; `halo` if BPM < 90 and drive < 0.6; otherwise `pulse`.

About 2–3 s for a 3-minute song on a laptop.

Checked against librosa on the three sample songs: the beats match librosa's (at half its tempo) with an F-measure of 0.94 and 0.82 on two of them. On all three, the detected beats land on stronger onsets than librosa's own beats, measured with librosa's onset curve. «منم» is in a compound meter; librosa picks 99 BPM there, which doesn't fit its bar.

| Track | BPM (visual pulse) | Style |
|---|---|---|
| دایان · تا ابد تو | 80 | pulse |
| مجید رضوی · منم | 74 | halo |
| آرون افشار · ثانیه وار | 76 | beams |

### 7.2 Stored format
```jsonc
{
  "bpm": 80,                       // median beat interval → BPM (the pulse the visuals use)
  "beats": [0.36, 1.14, 1.77, …],  // seconds, 3 decimals; ~2 KB for a 3-minute song
  "down": 0,                       // beat index mod 4 that starts a bar
  "energy": [0, 0.01, …],          // 4 Hz, 0–1 relative to the track
  "peaks": [0.84, 0.96, …],        // 200 values, 0–1
  "hook": 167.8,                   // seconds
  "duration": 205.91,
  "drive": 0.7,
  "style": "pulse"                 // halo | pulse | beams
}
```

### 7.3 Live signals (every frame)
`<audio>` → `MediaElementSource` → `AnalyserNode` (fftSize 2048, smoothing 0.55, **dB range −92…−16**, so loud masters don't pin every band) → speakers. Shared object `A`:

| Signal | How |
|---|---|
| `level` | 0 → 1 when playing (rate 3/s), back to 0 at 2/s; everything is multiplied by it |
| `bands[48]` | log-spaced 40 Hz–12 kHz, attack 0.55, release 0.16 |
| `t` | `currentTime`, interpolated between media clock updates, minus `outputLatency` |
| beat | pointer into `beats` (binary search after a seek); on each new beat `kick = max(kick, amp)` |
| `amp` | `(0.5 + 0.5 × energy) × gate`, with `gate = smoothstep(0.012, 0.07, live RMS)` so quiet passages don't flash |
| `kick` | decays `e^(−7.5t)` (≈ 0.15 s) |
| `down` | on downbeats, decays `e^(−3.2t)`; `bars` counts them |
| `phase` | 0–1 position inside the current beat |
| `energy` | from the stored curve, smoothed `e^(−2t)` |
Without stored analysis: low-band flux above 2.2 × its running mean (min 0.28 s apart) counts as a beat.

---

## 8. Music reactions (`#react`, above the scrim, below the content)

All four modes are light by design. Each frame they change only `transform` or `opacity`, or redraw one small canvas (DPR ≤ 1.5). They use **no blend modes, masks, filters or WebGL**, and they stop drawing once the music has faded out.

| Mode | Look | Formula |
|---|---|---|
| **هاله** halo | Reference B's **striped circle** around the subject: 30 horizontal stripes inside a ring (R0 = 0.19 S, R1 = 0.44 S, S = min(bgH × 0.84, W × 0.48, 900)) centred on the focal point | stripe thickness `(1.1 + v·4.2 + kick·2.2·f²)·dpr`, alpha `0.12 + v·0.5 + boost·0.4` (v = its band: bass at the bottom, treble at the top); a bright band sweeps bottom → top **once per bar**, locked to beat and phase; an outline ring (`0.22 + kick·0.45`); each downbeat sends a ripple (speed 0.12 S/s, decay `e^(−2.4t)`); canvas `scale(1 + kick·0.028)` |
| **نبض** pulse | the photo breathes, a soft light blooms behind the subject, downbeats flash from the top | `.bg-pulse` `scale(1 + kick·0.016)` at the focal point; 900px radial bloom `scale(0.85 + kick·0.22)`, opacity `(0.1 + kick·0.5 + energy·0.15)·level`; top flash opacity `down·0.38` |
| **طیف** spectrum | a mirrored equaliser **standing on the rail**, between the side column and the title | width = that gap minus 24px each side, height `clamp(bgH·0.2, 90, 210)`; bars = clamp(width / 13, 24, 64), bass in the middle, rounded, gradient accent → white; height `v·H·0.9·(0.55 + 0.45·energy)·envelope`; white caps fall at 0.35 H/s |
| **نورافکن** beams | six stage beams from above; odd and even take turns on the beat | each beam is a 34vw × 125% layer showing a **light-cone image drawn once per accent** (canvas → blob URL); `rotate = sin(t·0.45 + i·1.3)·9° + (i − 2.5)·7°·(0.6 + 0.4·energy)`; opacity `((0.05 + kick·0.6·on)(0.55 + 0.45·energy) + down·0.22)·level`, on = 1 or 0.22 |
| **خودکار** auto (default) | uses the track's `style` | switches when the track changes; the panel shows the pick («خودکار · هاله») |
| خاموش off | — | — |

---

## 9. Admin panel fields

**Featured event** (the rail is the paid «جایگاه ویژه»; order and dates set by the admin):
```jsonc
{
  "id": "frequency",
  "category": "کنسرت پاپ", "categoryIcon": "mic",
  "badge": "پرفروش",
  "performer": "گروه نیمه‌شب",
  "title": "فرکانس",
  "tagline": "لحظه را زندگی کن",           // short, set in Nastaliq
  "description": "…",                     // ≤ 2 lines at 46ch
  "venue": "مجموعه ورزشی آزادی، سالن ۱۲ هزار نفری", "venueShort": "سالن ۱۲ هزار نفری",
  "startsAt": "2026-12-14T20:30:00+03:30",
  "priceFrom": 1800000, "currency": "IRT",  // shown as «از ۱٫۸ میلیون تومان»
  "soldPercent": 82,
  "accent": "#5aa2ff", "accentDeep": "#1f4fd6",
  "image": { "master": "…", "w": 3200, "h": 2138, "fit": { "x": 0.57, "y": 0.36, "zoom": 1.24, "card": 0.62 } },
  "featured": { "from": "…", "to": "…", "order": 1 }
}
```
The upload screen should let the editor **click the subject** to set `fit.x/y`, preview the stage and the card crop live, and set `zoom` (≤ 1.3) and `card`. The server cuts `-1920/-2560/-3200.webp` and `-thumb.webp` (720×360) with the formulas in §6.1.

**Track**: `{ id, title, artist, url, cover?, analysis }`. On upload, run the analysis and store `analysis` (§7.2). Show its BPM and style in the panel, so the editor can see what auto mode will do. The audio files need **CORS headers** if they're served from another host (the analyser reads them), and **range requests** for seeking.

---

## 10. Performance rules

1. Continuous animations touch only `transform` and `opacity`. No `backdrop-filter`, no WebGL, no `mix-blend-mode`, no animated masks. v1's lag came mostly from a full-screen shader plus backdrop blur over a moving canvas.
2. Don't animate inherited custom properties on `:root` (§3.2).
3. No per-frame DOM writes that cause layout: no SVG transforms, no `innerHTML` in tweens unless the value changed, and timers only update text when it changes.
4. Per-frame work lives in **one** `requestAnimationFrame` loop, which stops drawing when the stage is off-screen or the tab is hidden. The music layer idles when nothing plays.
5. Big images: decode before the transition (`img.decode()`), preload the others after the first paint, and pick the size by displayed pixels.
6. Measured in the prototype (headless Chromium, per second of wall time, main thread): idle ≈ 7 ms of style work; an event change ≈ 18 ms of style and 5 ms of layout; music playing ≈ 2 ms of layout.

---

## 11. Persian & RTL rules

1. **Never split Persian text into characters** for animation; it breaks the joins. Animate words (`.w > .wi`) or lines.
2. Persian digits everywhere (`fa()` digit map or `toLocaleString('fa-IR')`). Dates use `Intl.DateTimeFormat('fa-IR-u-ca-persian', …)`.
3. Clock-like things stay **LTR**: times, the countdown, the media transport and seek bar.
4. Mirror directional arrows (next = ←, previous = →, progress fills from the right) but **not** media icons.
5. Nastaliq needs `line-height ≥ 2`. Its reveal runs right → left with `mask-image: linear-gradient(to left, #000 calc(var(--reveal) - 15%), transparent var(--reveal))`, where `--reveal` is registered as `<percentage>` and animated 0% → 115%.
6. `font-variant-numeric: tabular-nums` where digits line up.

---

## 12. Accessibility

- Stage: `aria-roledescription="carousel"`. The info region is `aria-live="off"` during auto-advance and `polite` after user navigation.
- Rail: `role="tablist"`, cards are `role="tab"` with `aria-selected` and a label «فرکانس، کنسرت پاپ، ۲۴ آذر»; roving `tabindex`; a pause control with `aria-pressed`.
- Player: labelled buttons, `aria-pressed` on like, `aria-expanded` on the playlist, and the waveform as a `slider` with `aria-valuenow`.
- Countdown digits are hidden from screen readers; a sentence replaces them.
- Decorative layers (`#bg`, `#react`, frames, bars) are `aria-hidden`; images have `alt=""`.
- Focus rings use the accent (`outline: 2px`, offset 3px).

---

## 13. Porting notes (React / Next.js or similar)

Components: `<HeroStage>` (background layers + transitions; receives `index` and the card rect) · `<MusicLayer>` (canvas + beams + bloom; reads the audio store) · `<HeroNav>` · `<EventInfo>` · `<FeaturedRail events index onSelect>` · `<MusicPlayer tracks>` · `<DateCard event>` · `<TeaserDialog>`.

- One store (context or zustand) for `featuredIndex`, `paused`, `hover`, `reactMode`, `transition`. Keep the per-frame audio values (`A`) in a plain mutable object read by the rAF loop, **not** in React state.
- Drive auto-advance from the rail card's CSS `animationend`, as the prototype does. Pausing is then one CSS variable, and the timer, the progress bar and the slow zoom can't drift apart.
- Run the WAAPI transitions from an effect, keyed by `featuredIndex`. Pass the card's rect through a ref read at click time.
- GSAP: register ScrollTrigger once; create tweens inside `gsap.context()` / `useGSAP()` so they clean up.
- Server-render the first event's text and the rail so the hero reads before JS; hide only behind `.is-intro`.

---

## 14. Implementation checklist

- [ ] Tokens, fonts (Lalezar, Vazirmatn, Nastaliq subset), `@property` accent without a root transition
- [ ] Stage grid that fits 1920×1080 → 1280×720 with no overflow; tablet/phone stack
- [ ] Background layers, focal-point placement, responsive image sizes, Ken Burns
- [ ] Transitions: window (FLIP from the card), fade, blinds; race-safe
- [ ] Featured rail: image cards, highlight frame, progress bar, CSS-driven auto-advance, pause rules, keyboard
- [ ] Info swap with word masks and the Nastaliq reveal
- [ ] Date card with the compact odometer countdown, capacity bar, reminder
- [ ] Player: real audio → analyser, stored analysis → beat clock, waveform seek, playlist with BPM, upload
- [ ] Music layer: halo, pulse, spectrum, beams, auto
- [ ] Admin: focal-point picker, card crop preview, track upload with analysis
- [ ] Teaser dialog from the track's hook
- [ ] Intro timeline, scroll recede, toasts, reduced-motion paths, a11y attributes

---

## 15. Credits

Photos: Unsplash (Unsplash License), listed in `assets/CREDITS.md`. Songs: the owner's sample playlist, which is not in the repository (see `assets/music/README.md`). Event names, performers, prices and dates are sample content; the venues are real Tehran halls, used as realistic placeholders.
