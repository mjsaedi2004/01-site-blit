# Hero · نسخه‌ی رسمی (Formal) · handoff spec

> **خلاصه برای خودت:** این یه سبک جداست، کنار هیروی نسخه‌ی ۲ (پوشه‌ی `01-hero`) که دست‌نخورده نگه داشته شده. ساده و رسمی و شیک، با موشن‌های آروم و دقیق. `index.html` همین پوشه مرجع زنده‌ست؛ اگه جایی این متن با کد فرق داشت، کد درسته.

**Status:** new direction, waiting for the owner's feedback. The owner asked to keep hero v2 as it is and to try a new style of my own: simple, formal and chic, with professional motion.
**Stack of the prototype:** HTML + CSS + vanilla JS + GSAP 3.13 + Web Audio. No WebGL, no blur, no blend modes.
**Source of truth:** `ui-reference/01-hero-formal/index.html`.

---

## 0. Viewing

```bash
cd ui-reference && npx http-server -p 8000
# open http://localhost:8000/01-hero-formal/
```
The songs aren't in git; see `assets/music/README.md`. The round button at the bottom left opens a review panel (look, photo colour, transition, title font, music reaction). **It's not part of the site.**

---

## 1. The idea

An editorial spread, like a concert-hall programme or an invitation card.
- **Right (text):** the event number, its category, a large Naskh title, the performer, and a definition list of date, time and venue ruled off with hairlines. Under that sit one black button and a small countdown. At the foot is a typographic **index of the featured events** («جایگاه ویژه», 01–06). The hairline under the active one is its timer.
- **Left:** one tall framed photograph, in warm black and white.
- **Structure:** no cards, shadows or boxes; spacing and 1px rules do that job. One bronze accent.
- **Motion:** slow and exact. Every 7 s the next photograph opens like a curtain from right to left while the words leave and return through masks.

---

## 2. Layout

| Part | Value |
|---|---|
| Side margin `--m` | `clamp(20px, 3vw, 60px)`, applied as `max(var(--m), env(safe-area-inset-*))` |
| Hero | `height: 100svh; min-height: 640px; max-height: 1200px`; rows `auto minmax(0,1fr)` |
| Nav | grid `1fr auto 1fr`: wordmark (right), five links (centre), music + search + login (left); padding-block `24px 20px`; a 1px rule along the bottom |
| Spread | grid `minmax(0,1.08fr) minmax(0,1fr)` (text right, photograph left), gap `clamp(32px, 4.4vw, 96px)`, padding-block `clamp(26px, 4.6svh, 56px)` |
| Text column | rows: eyebrow, title, performer, facts, CTA, `1fr` spacer, index (pinned to the bottom) |
| Photograph | fills its column's full height; `object-fit: cover` on a 5:6 crop; caption (venue · ۰۱ / ۰۶) inside, bottom, white |

Measured: nothing overflows or overlaps, with no horizontal scroll, at 1920×1080, 1920×940, 1536×730, 1366×768 and 1280×720.

| Condition | Changes |
|---|---|
| `max-height: 800px` and `min-width: 901px` | nav padding `18/16`; title `clamp(60px, 6.6vw, 120px)`, long `clamp(50px, 5.2vw, 96px)`; tighter fact rows; 52px button; index dates hidden |
| `901–1180px` wide | link gap 22, index gap 12 |
| `≤ 900px` | one column: nav (wordmark + player + menu) → photograph (5:6, max 72svh) → text → index as a horizontal scroll with snap |

---

## 3. Tokens

Both looks are first-class: **day** (ivory paper) and **night** (warm black). The page follows the system theme, and the review panel can force either.

| Token | Day | Night | Use |
|---|---|---|---|
| `--paper` | `#f3efe7` | `#11100e` | page |
| `--paper-2` | `#ebe5da` | `#191714` | photo placeholder |
| `--ink` | `#15130f` | `#efe9de` | text, the button |
| `--ink-2` / `--ink-3` | 70 % / 46 % | 72 % / 48 % | secondary text, labels |
| `--rule` | ink at 16 % | ink at 14 % | hairlines |
| `--accent` | `#8a6a3c` bronze | `#c9a66b` champagne | numbers, the eyebrow line, the button hover, focus |
| `--veil` | `rgba(10,9,7,.38)` | `rgba(0,0,0,.45)` | dims the outgoing photograph |

Type:
| Role | Font | Size |
|---|---|---|
| Title | **Markazi Text** 600 (option: Vazirmatn 200, `--title-k: .86`) | `clamp(72px, 7.8vw, 160px)`; longer than 7 characters `clamp(60px, 6.2vw, 124px)`; line-height 1.12 |
| Wordmark | Markazi Text 600 | 34 |
| Index titles | title font | `clamp(18px, 1.35vw, 24px)` |
| Everything else | **Vazirmatn** 300–500 | performer `clamp(18px, 1.35vw, 24px)` / 300; facts 15.5; labels 12.5; nav 14.5 |
No letter-spacing on Persian. Digits are Persian; `tabular-nums` where they line up.

Easing: `--ease: cubic-bezier(.16,1,.3,1)` (expo out) for entrances and settling; `--ease-io: cubic-bezier(.77,0,.175,1)` for wipes and lines. Slot length `--dur: 7s`.

---

## 4. Components

- **Eyebrow:** `۰۱` in the accent, a 44px accent line, «کنسرت پاپ · پرفروش».
- **Title:** each word in `.w > .wi` (a mask with room above and below for Persian ascenders and descenders).
- **Facts:** a `dl` with a top rule; each row is `96px label | value`, ruled off, values on one line with an ellipsis.
- **Button:** black, square-cornered, 58px tall: «خرید بلیت» · «از ۱٫۸ میلیون تومان» · arrow. Hover: a bronze fill grows from the right (`scaleX`, 0.6 s `--ease`) and the arrow moves 5px forward (left). It's the only button in the hero.
- **Countdown:** «تا اجرا» over «۴۶ روز ۰۲:۱۴:۰۹». The days are in the title font; the clock is LTR, with each digit an odometer strip (changed digits roll 0.7 s expo out; on change all digits spin a full turn, 1.1 s expo in-out, staggered 0.03 s). Screen readers get one sentence.
- **Index:** six buttons in a `tablist`, each «۰۱ / فرکانس / ۲۴ آذر» over a 1px rule. Inactive titles are in `--ink-3`, the hovered one in `--ink-2`, the active one in `--ink`, with its number in the accent. The active rule fills with ink from the right over `--dur`; its `animationend` advances to the next event. Pause: pointer over the photograph or the index, focus in the index, the pause button, off-screen, hidden tab, reduced motion. Keyboard: ArrowLeft = next, ArrowRight = previous.
- **Photograph:** two layers. The active one drifts `scale 1 → 1.06` over 11 s, linear. On fine pointers the image follows the cursor by up to 7×5 px (lerp `1 − e^(−3·dt)`).
- **Music:** in the header: a round play button (34px, outlined; filled ink while playing), the title and «دایان · ۸۰ ضرب», and three 1.5px bronze equaliser bars. Clicking the title opens a dropdown with the waveform seek bar (ink for played, accent on hover), the time row, previous/next, the playlist with BPM and length, and «آهنگ خودت رو امتحان کن».

---

## 5. Motion

### 5.1 Intro (~1.8 s)
| t (s) | What |
|---|---|
| 0 | the nav rule draws from right to left (`scaleX 0 → 1`, 1.4 s `--ease-io`) |
| 0.15–0.3 | wordmark, links and tools rise out of nothing (`yPercent 60–80`, 1–1.1 s expo out, stagger 0.05) |
| 0 | the photograph opens upward: `clip-path: inset(100% 0 0 0) → inset(0)` (1.5 s `--ease-io`) while the image settles from `scale 1.22` (2.2 s `--ease`) |
| 0.45 | the eyebrow line draws |
| 0.55 | title words rise through their masks (`yPercent 115 → 0`, 1.15 s expo out, stagger 0.08); the other lines follow (1 s, stagger 0.05) |
| 0.7 | fact rows fade in (stagger 0.07) |
| 0.95 | button and countdown rise 18px |
| 1.05–1.1 | index head, then the six items (stagger 0.06) |
| 1.15 | countdown digits spin |
The entrance tweens are created with their delays at once (`fromTo`), so their start state applies immediately and nothing flashes.

### 5.2 Changing events («پرده», the default)
| t (ms) | What |
|---|---|
| 0 | title words leave upward through their masks (`yPercent -112`, 0.5 s `power3.in`, stagger 0.04); the other lines do the same (0.45 s, stagger 0.025) |
| 0 | the new photograph is uncovered from the right edge: `clip-path: inset(0 0 0 100%) → inset(0 0 0 0)` (1250 ms `--ease-io`); inside, the image goes `scale(1.16) translateX(4%) → none` (1700 ms `--ease`) |
| 0 | the old photograph moves `translateX(-7%)` and its veil fades in (1250 ms `--ease-io`), so the two read as layers |
| ~560 | the new words rise (as in the intro, 0.05 s later) |
| 0 | the countdown spins to the new date |
«محو» (fade): opacity 0 → 1 (1.1 s) with `scale 1.06 → 1` (1.8 s). Reduced motion: a 0.4 s fade, no auto-advance. Rapid input is safe: a running change is finished first.

---

## 6. Photographs

5:6 crops around each event's focal point, from 3200 px masters, at `1200` and `2000` px wide. The page picks by frame width × DPR (> 1100 → 2000). Black and white is made offline, not with CSS filters:
```python
g = ImageOps.autocontrast(ImageOps.grayscale(crop), cutoff=(0.4, 0.2))
g = ImageEnhance.Contrast(g).enhance(1.08)
bw = ImageOps.colorize(g, black=(18, 15, 12), white=(246, 240, 228), mid=(128, 120, 110))   # warm, like a gallery print
```
In production the admin uploads the photo and marks its focal point. The server makes the crops, plus the black-and-white version if the site keeps that look.

---

## 7. Music and rhythm

The same rhythm analysis as hero v2 (`01-hero/SPEC.md` §7, `analyseTrack()` in the page): beat times, downbeat, energy, waveform peaks. It's computed on upload and stored with the track; the three sample songs have it embedded. Seeking falls back to playing from memory when the server can't serve byte ranges.

The reaction is deliberately quiet:
- **فقط نشانگر** (default): the three equaliser bars in the header follow three bands, and the first one also takes the beat.
- **تنفس عکس**: in addition, the photograph swells `1 + kick × 0.008` on each beat. `transform` only.
Measured while playing: no layout per frame, about 4 ms of style work per second.

---

## 8. Admin fields

Event: `{ category, badge, performer, title, venue, place (short), startsAt (ISO with +03:30), priceFrom, photo { master, focus: [x, y] }, featured { from, to, order } }`. Track: `{ title, artist, url, analysis }`. Dates are formatted with `Intl.DateTimeFormat('fa-IR-u-ca-persian', { timeZone: 'Asia/Tehran' })`.

---

## 9. Rules

1. Continuous motion only on `transform` and `opacity`, plus one-off `clip-path` wipes. No backdrop-filter, filters, blend modes or WebGL; black and white is baked into the files.
2. No transitions on inherited custom properties (the theme switch is a one-off 0.6 s `background-color`/`color` transition on `.app`).
3. Persian:
   - Never split words into letters.
   - Clocks and media rows are LTR.
   - Arrows are mirrored (next = ←).
   - Persian digits and the Persian calendar.
4. Accessibility:
   - The hero is `aria-roledescription="carousel"`.
   - The text block is `aria-live="off"` during auto-advance and `polite` after user navigation.
   - The index is a tablist with a pause control.
   - Focus is shown as a 1px accent outline 4px out.
   - Reduced motion is respected throughout.

---

## 10. Porting notes

Components: `<HeroNav>` (with `<MusicPlayer>`) · `<EventCopy>` · `<Countdown>` · `<FeaturedIndex>` · `<HeroPhoto>`. Drive auto-advance from the index rule's `animationend`, keep audio values out of React state, and run the photo wipe with WAAPI keyed by the event index. Server-render the first event.
