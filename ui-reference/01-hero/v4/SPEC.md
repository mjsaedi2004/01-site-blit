# Hero · نسخه‌ی ۴ · رسمی و زنده (formal, alive) · handoff spec

> **خلاصه برای خودت:** همون سبک رسمی نسخه‌ی ۴ (چیدمان دعوت‌نامه‌ای، یه دکمه، فهرست اجراهای ویژه)، ولی با جون: عکس رنگی که تا لبه‌ی صفحه می‌ره و تو زمینه حل می‌شه، رنگ مخصوص هر اجرا، خط نستعلیق، نور رنگی که روی عکس جابه‌جا می‌شه، نورافکنی که دنبال موس می‌آد، و نوری که با ضرب موزیک نفس می‌کشه. `index.html` همین پوشه مرجع زنده‌ست.

**Status:** v4, second pass. The owner found the first pass formal but lifeless («بی‌روح»), so this pass keeps the structure and adds warmth, colour, light and livelier motion. Versions 1–3 sit beside it in `../` for comparison.
**Stack:** HTML + CSS + vanilla JS + GSAP 3.13 + Web Audio. No WebGL; no blur or blend modes on anything that moves.

---

## 1. The idea

An evening at the theatre, set like an invitation.
- **Right:** the event number and category, a large Naskh title, a **handwritten Nastaliq line in the show's colour**, the performer, a ruled list of date/time/venue, one button and a small countdown, and at the foot the typographic index of the featured events.
- **Left:** a **colour photograph that runs to the page edge and melts into the paper**. A slow glow in the show's colour drifts over it and a soft spotlight follows the cursor.
- **Colour:** every show brings its own accent.
- **Changing events:** a band of that colour sweeps across the photo and the next one opens behind it. Title words turn up like cards, and the Nastaliq line writes itself in.

---

## 2. Layout

| Part | Value |
|---|---|
| Side margin `--m` | `clamp(20px, 3vw, 60px)` (`max()` with the safe-area insets) |
| Hero | `height: 100svh; min-height: 640px; max-height: 1200px`; rows `auto minmax(0,1fr)` |
| Nav | grid `1fr auto 1fr`: wordmark, five links, music + search + login; a 1px rule under it |
| Spread | grid `minmax(0,1.05fr) minmax(0,1fr)` (text right, photo left), gap `clamp(32px, 4vw, 88px)`, padding-block `--pt / --pb` = `clamp(26px, 4.6svh, 56px)` / `clamp(24px, 4.6svh, 56px)` |
| Photo column | negative margins so it touches the nav rule, the bottom of the hero and the page's left edge (`margin-inline-end: -max(var(--m), safe-area)`) |
| Text column | rows: eyebrow, title, tagline, performer, facts, CTA, `1fr` spacer, index |

**The photo melts into the page:** an overlay (`.edge`) on top of the photo.
```css
linear-gradient(to left, var(--paper) 0%, paper 94% 6%, paper 78% 14%, paper 52% 25%, paper 24% 36%, transparent 48%),  /* inner (right) edge */
linear-gradient(to top, var(--paper) 0%, transparent 22%),                                                        /* bottom */
linear-gradient(to bottom, paper 55% 0%, transparent 16%)                                                         /* top */
```
("paper 78%" means `color-mix(in srgb, var(--paper) 78%, transparent)`; the many stops avoid a visible step.)

Measured: no overflow or overlap and no horizontal scroll at 1920×1080, 1366×768 and 1280×720. Phone (≤ 900px): the photo first (5:6, max 70svh, full width, fading out at the bottom), the text pulled 40px up into the fade, the index as a sideways scroll.

---

## 3. Tokens

**Night** (default): `--paper #0f0d0b`, `--paper-2 #1a1714`, `--ink #f1ebe0`, `--ink-2` 74 %, `--ink-3` 50 %, `--rule` ink at 14 %, `--veil rgba(0,0,0,.5)`, `--on-accent #0f0d0b`.
**Day** (review panel): `--paper #f3eee5`, `--paper-2 #e9e2d6`, `--ink #16130f`, `--ink-2` 72 %, `--ink-3` 48 %, `--rule` 16 %, `--veil rgba(20,16,12,.38)`, `--on-accent #f6f1e8`.

**The show's colour:** each event has a night accent (light) and a day accent (deep); `--accent` picks one per look. It's set once per change, at the moment the new words appear, never animated as a variable.

| Event | night | day |
|---|---|---|
| فرکانس | `#7fa6ff` | `#2f5fd0` |
| طیف | `#e98ae0` | `#a8329e` |
| چهارمضراب | `#dcb874` | `#8a6a3c` |
| سایه‌ها | `#ee9466` | `#a9482a` |
| بی‌تعارف | `#f2c14e` | `#9a6c12` |
| پرواز | `#6ad6c6` | `#1d8a7c` |

The accent appears in:
- the wordmark's ticket and the active link underline;
- the eyebrow number and line;
- the Nastaliq tagline;
- the active index item's number and time line;
- the button's hover fill;
- the music equaliser and its pulse ring;
- the glow and the light band over the photo.

**Type:**
| Role | Font | Size |
|---|---|---|
| Title | **Markazi Text** 600 (option: Vazirmatn 200, `--title-k: .86`) | `clamp(76px, 8.2vw, 168px)`; longer than 7 characters `clamp(62px, 6.4vw, 128px)`; line-height 1.1 |
| Tagline | **Noto Nastaliq Urdu** 600, subset to the taglines | `clamp(26px, 2.25vw, 44px)`, line-height 2 |
| Everything else | **Vazirmatn** 300–500 | — |

Easing: `--ease: cubic-bezier(.16,1,.3,1)`; `--ease-io: cubic-bezier(.77,0,.175,1)`. Slot: `--dur: 7s`.

---

## 4. The photograph's layers (bottom → top, all inside `.frame`, `overflow: hidden`)

1. **Two photo layers.** Each is a `.move` wrapper (cursor parallax, `inset: -18px` so it can move) around an `img` (`object-fit: cover`). The active one drifts `scale 1 → 1.07` over 12 s. Each layer also has a `.veil` that dims it while it leaves.
2. **Glow** (`.leaks`, two layers cross-faded per event): a circle 95 % of the frame wide. Its radial gradient goes from the accent at 62 % to 20 % at 48 % to transparent at 72 %. Each layer runs an endless 19 s `ease-in-out alternate` drift (`translate` and `scale` only; the second is offset by −9 s). The container sits at opacity 0.72, so the music can raise it.
3. **Spotlight** (`.spot`, fine pointers only): a 620px warm radial gradient (`rgba(255,246,228,.2)` → transparent) that follows the cursor (lerp `1 − e^(−7·dt)`) and fades in on hover.
4. **Light band** (`.sweep`, only during a change): 38 % wide, a horizontal gradient of accent 30 % → warm white 50 % → accent 30 %.
5. **Edge fade** (§2), **grain** (an SVG noise tile at 8 % alpha, static), then the caption (venue · ۰۱ / ۰۶) in `--ink-2`, sitting in the faded bottom.

Cursor parallax: the photo moves up to 8×6 px against the cursor and the text block moves a quarter of that the other way, for depth.

---

## 5. Motion

### 5.1 Intro (~2 s)
| t (s) | What |
|---|---|
| 0 | the nav rule draws right → left (1.4 s `--ease-io`) |
| 0 | the photo comes up out of the dark (`opacity 0 → 1`, 1.6 s) while settling from `scale 1.16` (2.6 s `--ease`) |
| 0.3 | the glow blooms (`opacity 0, scale .7` → its rest state, 2.4 s) |
| 0.15–0.3 | wordmark, links, tools rise in |
| 0.5 | the eyebrow line draws |
| 0.6 | title words turn up (`yPercent 75, rotateX −80° → 0`, origin at their baseline, inside a 700px perspective; 1.3 s expo out, stagger 0.09); the other lines rise through masks (stagger 0.05) |
| 0.9 | the Nastaliq line writes itself right → left (mask `--reveal 0% → 115%`, 1.5 s `power2.inOut`) |
| 0.8–1.2 | fact rows, button + countdown, index |
| 1.25 | countdown digits spin |

### 5.2 Changing events («باریکه‌ی نور», the default)
| t (ms) | What |
|---|---|
| 0 | title words turn away (`yPercent −60, rotateX 70°`, fading, 0.55 s `power3.in`, stagger 0.04); the tagline fades; other lines leave upward through masks |
| 0 | curtain: `clip-path: inset(0 0 0 100%) → inset(0)` on the new photo (1300 ms `--ease-io`); inside it `scale(1.14) translateX(4%) → none` (1800 ms `--ease`) |
| 0 | the **light band rides exactly on the curtain's edge**: `translateX(W − bw/2) → translateX(−bw/2)` with the same duration and easing, fading in over the first 12 % and out after 80 % |
| 0 | the old photo slides `translateX(−8%)` under its veil; the glow cross-fades to the new colour (1.4 s) |
| ~600 | the accent switches; the new words turn up, the lines rise, the Nastaliq line writes |
| 0 | countdown spins; the days number slides in |
Other options: «پرده» (the curtain without the band), «محو» (fade 1.1 s + `scale 1.06 → 1`). Reduced motion: a 0.4 s fade, no auto-advance, no endless drift.

### 5.3 Index
The hairline under the active item fills in the show's colour over `--dur`; its `animationend` advances. Items lift 3px on hover. Pause: pointer over the photo or the index, focus in the index, the pause button, off-screen, hidden tab, reduced motion.

---

## 6. Music

Same player and rhythm analysis as before (`../v2/SPEC.md` §7): beat times, downbeat, energy, peaks. The songs are shared in `../assets/music/`.

**«نور با ریتم»** (default) and «فقط نشانگر» (equaliser only):
- glow container `opacity 0.72 + 0.28·g`, `scale(1 + 0.05·g)`, with `g = clamp((kick·0.55 + down·0.4 + energy·0.15)·level, 0, 1)`;
- photo `scale(1 + kick·0.008·level)`;
- the play button's accent ring `scale(1 + kick·0.18·level)`;
- four equaliser bars follow four bands.
Everything is `transform`/`opacity`, written only when the value changes. Measured while playing: no layout per frame.

---

## 7. Photographs and admin fields

5:6 crops around each subject at 1200 and 2000 px, in colour, plus black and white baked offline for the option. In production the admin uploads the photo, marks the focal point, and picks (or accepts suggested) night and day accents with a contrast check. Event fields: `{ category, badge, performer, title, tagline, venue, place, startsAt (ISO, +03:30), priceFrom, photo { master, focus }, accent { night, day }, featured { from, to, order } }`.

---

## 8. Rules

1. Continuous motion only on `transform` and `opacity`; clip-path only for the one-off curtain.
2. Never animate inherited custom properties; set the accent once per change.
3. **Persian:**
   - Don't split words into letters (the word flips are whole words).
   - The Nastaliq line needs `line-height: 2`.
   - Clocks and media rows stay LTR.
   - Mirror the arrows.
4. **Accessibility:**
   - The hero is `aria-roledescription="carousel"`, and the text is `aria-live="off"` during auto-advance.
   - The index is a tablist with a pause control.
   - The countdown is read as one sentence.
   - Focus is shown as a 1px accent outline.
