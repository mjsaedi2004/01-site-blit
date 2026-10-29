# Hero · «صحنه» (The Stage) · v1 — handoff spec

> **خلاصه برای خودت:** این فایل برای Claude دسکتاپه تا هیروی سایت اصلی رو دقیقاً مثل `index.html` همین پوشه بسازه. همه‌ی اندازه‌ها، رنگ‌ها، زمان‌بندی انیمیشن‌ها و رفتارها اینجا نوشته شده. فایل `index.html` مرجع زنده‌ست؛ اگه جایی این متن با کد فرق داشت، کد درسته.

**Status:** v1, waiting for the owner's feedback. Built as a standalone, framework-free prototype (HTML + CSS + vanilla JS + GSAP 3.13 + WebGL 1 + Web Audio).
**Source of truth:** `ui-reference/01-hero/v1/index.html`. Everything below describes what that file does, so it can be rebuilt in the real stack.

---

## 0. Viewing the prototype

```bash
cd ui-reference/01-hero && python3 -m http.server 8000
# open http://localhost:8000
```

- Serve over HTTP. Under `file://`, WebGL can't upload the photos as textures, so the page drops to its CSS fallback (crossfading `<img>`s), which is correct but not the real look.
- The thin bar above the hero (title font / colour mode / motion) is a **prototype control, not part of the site**. Don't port it.
- `?debug` exposes `window.__hero` (stage, deck, player, engine) for testing. Don't port it.

---

## 1. Behaviour in one paragraph

The hero is a rounded "stage" whose backdrop is a live WebGL render of the **featured event's photo**. Five featured events sit in a **stack of tickets** on the left (the "small box where events keep passing"). Every 8 s, or when the user clicks, drags or uses the arrows, the front ticket is thrown towards the stage and the next one comes forward. At the same moment the new photo **blooms out of the front ticket** across the stage, the whole UI **re-tints to the event's accent colour**, the big title and calligraphic tagline swap, and the **countdown spins** to the new event's start time. A **music player** (bottom right) plays the week's playlist; while it plays, the stage lights, dust and logo **pulse with the beat**. A **9-second teaser** (motion typography + the event's track) opens from the "تماشای تیزر" button.

---

## 2. Layout

### 2.1 Frame
| Property | Value |
|---|---|
| Outer page | `background: #07060b`, side gutter `max(16px, env(safe-area-inset-*))` |
| Stage | `border-radius: 30px; overflow: hidden; height: clamp(680px, calc(100svh - 62px), 1060px)` |
| Layers (bottom → top) | WebGL canvas → CSS fallback images (only without WebGL) → scrim gradients → content grid |

Scrim (keeps text readable over any photo; RTL so the dark side is the right):
```css
linear-gradient(to left,   rgba(7,6,11,.92) 0%, rgba(7,6,11,.74) 26%, rgba(7,6,11,.34) 45%, transparent 62%),
linear-gradient(to top,    rgba(7,6,11,.95) 0%, rgba(7,6,11,.62) 20%, transparent 44%),
linear-gradient(to bottom, rgba(7,6,11,.74) 0%, transparent 17%),
linear-gradient(to right,  rgba(7,6,11,.62) 0%, transparent 28%);
```

### 2.2 Grid (desktop, `dir="rtl"`)
```css
grid-template-columns: minmax(0, 1fr) 312px;      /* col 1 is on the RIGHT in RTL */
grid-template-rows: auto minmax(0, 1fr) auto;
grid-template-areas: "nav nav" "info aside" "bento aside";
gap: 16px 30px; padding: 16px 26px 24px;
```
- **info** (right): chips → performer → title → tagline → meta → description → CTAs. `max-width: 620px`, vertically centred.
- **aside** (left, spans 2 rows): stats card → ticket deck (`flex: 1`, min 440px) → deck controls.
- **bento** (bottom, under info): player `1.12fr` + countdown `1fr`, gap 16px.
- The photo's subject is framed into the free space between info and aside: the shader maps each photo's **focal point** to screen point `(0.40, 0.42)` on desktop, `(0.50, 0.26)` on mobile.

### 2.3 Breakpoints
| Condition | Changes |
|---|---|
| `max-height: 840px` and `min-width: 901px` (laptops) | description and stats card hidden; title `clamp(60px, 7vw, 118px)`; countdown digits 38px; tighter gaps |
| `901–1180px` | aside 290px; city button hidden; nav links tighter |
| `≤ 900px` (tablet + phone) | single column: nav → info → aside → bento; stage `height: auto`; canvas covers the top `min(92svh, 860px)` and fades out with a mask; info gets `padding-top: clamp(190px, 36svh, 330px)` so it reads like a poster over the photo; nav links become a menu button; countdown sits above the player; buy button stretches (max 420px) |
| `≤ 420px` | countdown digits 36px, smaller chips |

---

## 3. Tokens

### 3.1 Neutrals (single dark look, chosen on purpose)
| Token | Value | Use |
|---|---|---|
| `--ink-0` | `#07060b` | page |
| `--ink-1` | `#0e0c15` | stage base, panels |
| `--glass` | `rgba(17,14,27,.58)` + `backdrop-filter: blur(22px) saturate(150%)` | cards, pills |
| `--glass-hi` | `rgba(30,26,44,.74)` | hover |
| `--line` / `--line-2` | `rgba(255,255,255,.09)` / `.17` | borders |
| `--fg` / `--fg-2` / `--fg-3` | `#f6f3fb` / 76% / 54% | text |
| `--on-accent` | `#130d1d` | text and icons on accent fills (all accents are light enough for dark text) |
| `--live` | `#ff4d6a` | live / selling dot |

### 3.2 Accent (one per event)
`--accent` and `--accent-deep` are **registered custom properties** so they animate:
```css
@property --accent      { syntax: '<color>'; inherits: true; initial-value: #a78bfa; }
@property --accent-deep { syntax: '<color>'; inherits: true; initial-value: #6d28d9; }
:root { transition: --accent 1.2s cubic-bezier(.65,0,.35,1), --accent-deep 1.2s cubic-bezier(.65,0,.35,1); }
```
Every accent-coloured thing (buttons, chips' icons, tagline, countdown bar, waveform, logo, shader light) reads only these variables, so setting them on `:root` re-tints the whole hero.

| Event | Category | `--accent` | `--accent-deep` |
|---|---|---|---|
| فرکانس | کنسرت | `#a78bfa` violet | `#6d28d9` |
| چهارمضراب | موسیقی سنتی | `#2dd4bf` Persian turquoise | `#0f766e` |
| هملت | تئاتر | `#ff5a6a` crimson | `#b4232f` |
| بی‌تعارف | استندآپ | `#ffb547` amber | `#c2410c` |
| شازده کوچولو | کودک | `#ff7eb6` rose (the Little Prince's rose) | `#be185d` |
| brand (colour mode "بنفش ثابت") | — | `#a78bfa` | `#6d28d9` |

In production the accent should be a field on the event (editor-picked), with the brand violet as default.

### 3.3 Type
| Role | Font | Notes |
|---|---|---|
| Display (titles, digits, brand) | **Lalezar** 400 | Named after Lalezar Street, Tehran's old theatre & cinema district. Alternatives tested via the prototype bar: Noto Kufi Arabic 900 (`--title-k: .74`), Vazirmatn 900 (`.84`). |
| UI / body | **Vazirmatn** 300–900 (variable) | Persian digits look right in it. |
| Script (tagline only) | **Noto Nastaliq Urdu** 600 | Needs `line-height: 2`. Loaded with Google Fonts `&text=` subsetting (only the tagline glyphs) — in production, subset to the real taglines or self-host. |

Scale: title `clamp(68px, 8.2vw, 150px) × --title-k` (long titles, >8 chars: `clamp(60px, 6.6vw, 122px)`), tagline `clamp(24px, 2.4vw, 38px)`, performer 18/600, meta 15, body 15/1.9, chips 13/500, labels 12–12.5, ticket title 36, countdown digits 44, stats number 30.

### 3.4 Shape & motion constants
| | |
|---|---|
| Radii | stage 30, cards 22, panels 16, chips/pills 999 |
| `--ease-out` | `cubic-bezier(.16, 1, .3, 1)` (≈ GSAP `expo.out`) |
| `--ease-io` | `cubic-bezier(.65, 0, .35, 1)` |
| Auto-advance | 8 s per event |

---

## 4. Components

### 4.1 Nav
- Right: brand mark (a ticket with notched sides holding 4 EQ bars) + wordmark «بلیت» (placeholder name) in Lalezar 31px. The EQ bars idle-breathe and, while music plays, scale with 4 frequency bands.
- Centre: glass pill with category links. A **highlight pill slides** under the hovered/focused link (`transform` + `width`, 0.5s `--ease-out`).
- Left: search (42px circle that **expands to 268px**; placeholder types itself: «جستجو: هملت / کنسرت نیمه‌شب / …», Esc closes), city pill «تهران», login.
- Mobile: links hidden, menu button shown.

### 4.2 Info block (the featured event)
- Chips: category (icon tinted with accent) + status badge with a pulsing red dot («پرفروش», «آخرین بلیت‌ها», …).
- Performer → **title** (each word wrapped in `.w > .wi`; `.w` has `overflow:hidden` with padding/negative margin so Persian ascenders/descenders aren't clipped) → **tagline** in Nastaliq, accent colour with a soft glow → meta row (calendar / clock / pin icons) → description (46ch, hidden on short screens) → CTAs.
- **Buy button**: accent pill, label «خرید بلیت» + price, dark circle with ticket icon at the end side. Hover: rotating conic highlight around it, icon tilts −14°. Magnetic (see 5.4).
- **Teaser button**: 54px glass circle with a play icon (not mirrored) and an expanding ring, label «تماشای تیزر / ۹ ثانیه، با صدا».

### 4.3 Ticket deck (featured rotator)
- 5 cards, 290×396, absolutely stacked at the bottom of the deck area.
- Card anatomy: photo (206px) with category chip + «۸۲٪ فروش» pill + title/performer over a gradient → **perforation** (dashed line) with **real notches** cut by a two-layer `mask` (radial gradients at both edges, `--nt: 218px`) → stub: date badge (day big in Lalezar, month small), venue + weekday/time, footer with "starting price", a barcode (repeating gradient) and a **holographic sticker** whose conic gradient rotates with the tilt.
- Stack slots (index 0 = front):
  | slot | x | y | rotate | scale | opacity | shade |
  |---|---|---|---|---|---|---|
  | 0 | 0 | 0 | 0° | 1 | 1 | 0 |
  | 1 | −6 | −17 | −2.6° | .95 | 1 | .46 |
  | 2 | 5 | −32 | 2° | .90 | 1 | .62 |
  | 3 | −2 | −45 | −1° | .85 | .9 | .74 |
  | 4 | 0 | −54 | 0° | .80 | 0 | .80 |
  "shade" is a dark overlay (`opacity`), cheaper than `filter: brightness`.
- **Next**: front card flies `x: ±280, y: −40, rotate: ±16°, scale: 1.08, opacity: 0` (0.6s `power3.in`) towards the stage; the rest move up one slot (0.85s `expo.out`, +0.05s stagger, 0.12s delay); the thrown card re-enters at the back. **Previous**: the back card comes in from where cards are thrown (`x: 230, rotate: 14°`).
- **Drag**: pointer-capture on the front card; follows the pointer (`rotate = dx × 0.06°`); release beyond 90px or faster than 0.6 px/ms → thrown in that direction; otherwise springs back (`elastic.out(1, .5)`). A drag never counts as a click.
- **Tilt** (fine pointers only): `rotateX = (0.5 − y) × 14°`, `rotateY = (x − 0.5) × 18°`, lerped 0.12 per frame; a soft glare follows the pointer. The card has `perspective: 900px` on itself so the drop-shadow can be a static blurred pseudo-element.
- Click / Enter on the front card → buy (prototype shows a toast).
- Keyboard: deck is focusable; **ArrowLeft = next, ArrowRight = previous** (RTL).
- Non-front cards are `inert` + `aria-hidden`.

### 4.4 Deck controls
`[→ prev] [5 segments] [← next] [⏸ pause]`. Segments are story-style bars; the current one fills from the right over 8 s (`scaleX`, `transform-origin: right`) and doubles as a jump button. Auto-advance pauses while the deck is hovered/focused, during a drag, when the stage is off-screen, when the tab is hidden, while the teaser is open, and when the user presses pause (WCAG 2.2.2).

### 4.5 Stats card
Avatars (3 + accent "+" bubble) and «+۱۲۰ هزار» counting up from 0 on load (1.6s `expo.out`), label «نفر این ماه با ما به اجرا رفتند». Hidden on short desktop screens.

### 4.6 Music player
- Cover (58px, drawn on canvas per track: synthwave sun, girih star, mist, rings, starry night) with a **vinyl that slides out** and spins while playing. Use `translate`/`rotate` individual properties so the spin stays centred.
- Title / artist, like (heart burst: 9 particles), playlist popover (covers, durations, animated EQ on the current track).
- **Waveform = seek bar** (canvas, 56 bars, played part in accent, hover preview). While playing, bars near the frequency spectrum move with live analyser data. `role="slider"`, arrows seek ±5 s.
- Transport row is **LTR** (elapsed left, duration right, ⏮ ▶ ⏭ not mirrored), following media conventions even in RTL.
- Play button glows with a beat-driven ring (`box-shadow` spread = `--beat × 12px`).
- First-visit hint above the card: «پخش کن تا نورهای صحنه با موزیک بتپن» (removed on first play).

### 4.7 Countdown
- Header: «تا شروع اجرا» + «"title" · venue», bell button «یادم بنداز» (toggle; bell swings; toast confirms).
- Digits: groups `DD : HH : MM : SS`, **laid out LTR like a clock**, labels under each group. Each digit is an odometer: a strip of `۰–۹ ۰–۹` (20 cells) inside a 1.12em window, moved with `yPercent`.
  - Every second: changed digits roll 0.55s `back.out(1.6)`; when a digit wraps (0 → 9 while counting down) the strip jumps to the second copy first, so it always rolls the same way.
  - On event change: every digit **spins at least a full turn** to its new value (1.1s + 0.06s per digit, `power3.inOut`, 0.03s stagger).
- Capacity bar: accent gradient, `scaleX` to «٪ sold» (1.2s `expo.out`) with a moving shimmer; the percentage counts with it.
- Screen readers get a sentence («۴۷ روز و ۴ ساعت مانده») instead of the digits.

### 4.8 Teaser (9 s motion piece)
Full-screen `<dialog>` with letterbox bars. Timeline:
| t (s) | |
|---|---|
| 0 → 0.9 | dialog opens as a `clip-path: circle()` from the teaser button (`expo.inOut`) |
| 0 → 9 | photo Ken Burns `scale 1.32 → 1.02`, brightness `.3 → .62` |
| 0.7 / 2.3 | «{performer} تقدیم می‌کند» fades up, then out |
| 2.8 | title words rise (1.2s `expo.out`, 0.09s stagger) while the title scales `1.3 → 1` (3.2s) |
| 3.0 | an accent light sweep crosses right → left |
| 4.1 | tagline is "written" right → left (mask, 1.4s) |
| 6.2 | date line + «خرید بلیت» + «دوباره» |
| 0 → 9 | progress line fills |
Opening the teaser starts the event's own track in the player; closing it stops the music if the teaser started it. Esc / ✕ closes by shrinking the circle back into the button.

### 4.9 Toast & hints
Toast: bottom centre, glass, `role="status"`, slides up 0.5s, leaves after 3.4s. Hints («بلیت رو بکش و پرت کن» above the deck with a swinging hand, and the player hint) appear at the end of the intro and remove themselves after first use.

---

## 5. Motion

### 5.1 Intro (first load, ~2.4 s)
| t (s) | What |
|---|---|
| 0.15 | stage lights flicker on: intensity `0 → .55 → .08 → .72 → .25 → 1` (last step 0.9s `power2.out`) |
| 0.25 | brand drops in (−24px) |
| 0.35–0.45 | nav pill, links (stagger .05), tools (stagger .07) |
| 0.6 | title words rise, chips/performer/meta/desc fade up (stagger .06), tagline is written from 0.9 |
| 0.7 | tickets are **dealt** into the stack from bottom-left (`y:180, x:−60`, rotations −18/12/−9/6/0°, 1.2s, stagger .09) |
| 1.0 | stats card, bento cards rise (60px, stagger .12) |
| 1.05 | CTAs rise (stagger .1) |
| 1.2 | countdown spins in |
| 2.2 | hints appear |
Content is hidden only while JS is present (`.is-intro` set by an inline script, auto-removed after 4 s as a failsafe). Use `fromTo`, so start states render immediately and nothing flashes.

### 5.2 Event change (all at once)
1. Deck: throw + restack (4.3).
2. Stage: noisy circular reveal of the new photo **from the front ticket's photo centre**, 1.8s `power2.inOut` (see 6).
3. Accent: CSS variables transition 1.2s; the shader's accent is lerped in JS with the same feel (`1 − e^(−3.2·dt)`).
4. Info: old title words exit up (`yPercent −112`, 0.38s `power3.in`, stagger .04) while the rest fades out (0.3s); then the new content renders and enters as in the intro (1.05s `expo.out`).
5. Countdown spins; capacity bar animates.
6. Auto-advance timer restarts.
Rapid input is safe: a running stage tween is completed before the next starts, and a running info swap is killed.

### 5.3 Ambient
Stage beams sway, dust drifts up, follow spot trails the cursor (lerp 0.05), slow Ken Burns on the photo (`sin(t·0.07)`), live dot pings, teaser ring expands, capacity shimmer, EQ breathing.

### 5.4 Micro-interactions
- Magnetic buttons (fine pointers): button moves `dx × .22, dy × .32` and its label `dx × .08` (0.4s `power3.out`); returns with `elastic.out(1, .35)` 0.9s.
- Nav hover pill, search expand (0.6s `--ease-out`), like burst, bell swing, playlist pop (0.45s `expo.out`, items stagger .04).
- Scroll: as the page scrolls past the hero the stage scales to 0.95 and its radius grows to 44px (ScrollTrigger scrub).

### 5.5 Reduced motion
With `prefers-reduced-motion: reduce`: no auto-advance (the user navigates), stage reveal becomes a plain crossfade (`uSoft = 1`), sway/parallax/follow-spot scaled down, no tilt, no magnetic, no flying tickets (fade), digits jump instead of rolling, intro is a 0.5s fade, teaser opens without the circle wipe. The prototype's "آرام" motion mode is a softer preview of this for review.

---

## 6. WebGL stage

One full-screen triangle, one fragment shader (WebGL 1). Uniforms:

| Uniform | Meaning |
|---|---|
| `uTex0`, `uTex1`, `uImg0/1`, `uFoc0/1` | current / next photo, its pixel size, its focal point (0–1, y down) |
| `uTarget` | where the focal point lands on screen |
| `uProg`, `uOrigin` | reveal progress 0–1 and origin (front ticket photo, stage uv) |
| `uMouse` | smoothed cursor (follow spot + parallax) |
| `uAccent` | current accent (rgb 0–1) |
| `uBeat` | 0–1 beat envelope from the analyser |
| `uIntro` | lights-on intensity |
| `uFx`, `uSoft` | effect strength (1 full, .35 calm) and reduced-motion crossfade |

Layers, in order: object-fit **cover with focal point** + slow zoom + parallax → **reveal mask** (circle from `uOrigin` whose edge is broken by fbm noise; `rim` glow at the front, slight warp and chromatic split there) → **grade** (shadows sink into an accent-tinted ink, mild tint, contrast) → **follow spot** → 4 **moving-head beams** from above the frame + a follow-spot beam aimed at the cursor, modulated by drifting haze; intensity `(.27 + beat × .55)` → **halo** behind the subject → **dust** (2 hashed particle layers, brighter inside light) → **rim light** → vignette → lights-on → film grain.

Rules:
- Canvas DPR is capped at 1.6 (1.25 on mobile / calm) and **drops by 15% steps** if frames stay slower than ~38 fps for 2 s.
- Rendering stops while the stage is off-screen or the tab is hidden.
- If WebGL is missing, a shader fails, or a texture upload throws, switch to the CSS fallback: `<img>`s crossfading with a slow scale and an accent radial glow (`.no-gl`).
- Textures must be **same-origin or CORS-enabled**; don't feed Next/Image optimised URLs from another host without CORS.
- Mobile uses the `-m.jpg` (1200px) photos; deck cards use `-thumb.jpg` (640×400).

---

## 7. Audio

The prototype **synthesises** its five demo tracks live with Web Audio (no files, no licences): a step sequencer per track drives voices (kick, snare, clap, hats, saw/square synths, FM electric piano, bells, a Karplus–Strong **santur** playing chahar-mezrab figures in **dastgah Shur** with a quarter-tone E-koron, daf hits). Master chain: compressor → limiter → analyser → volume.

**In production, replace the synth with real tracks** and keep the visuals:
```js
const el = new Audio(track.url); el.crossOrigin = 'anonymous';   // the files need CORS headers
const src = ctx.createMediaElementSource(el);
src.connect(analyser); analyser.connect(ctx.destination);
```
Then run the same analysis every frame (`fftSize 1024`, smoothing .72):
```js
low  = avg(bins[1..5]) / 255                 // ~45–230 Hz
bands = [low, avg(6..21), avg(22..69), avg(70..179)]   // logo EQ
avgLow = avgLow * .965 + low * .035
beat = max(beat * .86, clamp((low − avgLow) × 4.2, 0, 1) × .9 + low × .22)
```
`beat` feeds `uBeat`, the play-button ring and the dust; `bands` feed the logo. Audio only starts from a user gesture.

---

## 8. Data the hero needs

```jsonc
{
  "id": "hamlet",
  "category": "تئاتر", "categoryIcon": "masks",
  "badge": "آخرین بلیت‌ها",
  "performer": "گروه تئاتر آینه",
  "title": "هملت",
  "tagline": "بودن یا نبودن",            // short, set in Nastaliq
  "description": "…",                    // ≤ 2 lines at 46ch
  "venue": "تئاتر شهر، تالار اصلی", "venueShort": "تئاتر شهر",
  "startsAt": "2026-11-07T19:30:00+03:30",
  "priceFrom": 450000, "currency": "IRT",  // format in the UI: «از ۴۵۰ هزار تومان»
  "soldPercent": 91,
  "accent": "#ff5a6a", "accentDeep": "#b4232f",
  "image": { "src": "…", "mobile": "…", "thumb": "…", "focus": [0.5, 0.56] },
  "teaserTrackId": "track-3"
}
```
Tracks: `{ id, title, artist, url, duration, cover }`. The hero shows 5 featured events; the playlist any number.

---

## 9. Persian & RTL rules (important)

1. **Never split Persian text into characters** for animation; it breaks the letter joins. Animate words (`.w > .wi` masks) or whole lines.
2. Numbers are Persian digits (`toLocaleString('fa-IR')` or a digit map). Dates use `Intl.DateTimeFormat('fa-IR-u-ca-persian', …)`.
3. Clock-like things stay **LTR** inside RTL: times (`ساعت ۲۰:۳۰` works naturally), the countdown row, and the media transport/seek bar (`direction: ltr`).
4. Mirror directional arrows (next = ←, previous = →, progress fills from the right) but **don't mirror media icons** (play, skip).
5. Nastaliq needs `line-height ≥ 2` and room above/below; its reveal mask runs right → left (`mask-image: linear-gradient(to left, #000 calc(var(--reveal) - 15%), transparent var(--reveal))`, `--reveal` animated 0% → 115%, registered as `<percentage>`).
6. `font-variant-numeric: tabular-nums` wherever digits line up.

---

## 10. Accessibility

- Stage `section` has `aria-roledescription="carousel"`; info region `aria-live` is `off` during auto-advance and `polite` after user navigation.
- Each ticket: `role="group"`, `aria-roledescription="بلیت"`, label «۲ از ۵: هملت، گروه تئاتر آینه».
- Pause control for auto-advance (`aria-pressed`), keyboard deck navigation, visible focus rings in the accent.
- Player: labelled buttons, `aria-pressed` on like, `aria-expanded` on playlist, waveform is a `slider`.
- Countdown digits are `aria-hidden` in effect (screen-reader sentence instead).
- Decorative canvases/images are `aria-hidden` / `alt=""`.

---

## 11. Porting notes (React / Next.js or similar)

Suggested components:
`<HeroStage>` (owns the canvas + fallback, receives `index`, `origin`, `accent`, `beat`) · `<HeroNav>` · `<EventInfo event>` · `<TicketDeck events index onChange>` · `<DeckControls>` · `<StatsCard>` · `<MusicPlayer tracks>` · `<Countdown event>` · `<TeaserDialog event>`.

- One shared store (context / zustand) for `featuredIndex`, `userPaused`, `isHovering`, `audio {beat, bands}`; every component reacts to `featuredIndex`.
- Set `--accent` / `--accent-deep` on `document.documentElement` (keep the `@property` rules in global CSS).
- GSAP: register ScrollTrigger once; create tweens inside `useGSAP()` / `gsap.context()` so they clean up; keep the per-frame work (tilt lerp, shader uniforms, waveform, beat) in **one** `requestAnimationFrame` loop, not in React state.
- Create the WebGL program once; load textures once; never re-mount the canvas on event change.
- Server-render the first event's text so the hero is readable before JS; hide only behind the `.is-intro` class.

---

## 12. Implementation checklist

- [ ] Tokens, fonts (Lalezar, Vazirmatn, Nastaliq subset) and `@property` accent
- [ ] Stage canvas + shader + CSS fallback + adaptive DPR + visibility pause
- [ ] Grid + breakpoints (desktop, laptop-short, tablet/phone)
- [ ] Nav (hover pill, expanding search, city, login, mobile menu)
- [ ] Info block with word-mask swap and Nastaliq reveal
- [ ] Ticket deck: notched mask, holo, stack slots, throw/restack, drag, tilt, keyboard
- [ ] Deck controls with story segments + pause
- [ ] Countdown odometer + capacity bar + reminder
- [ ] Player with real audio → analyser → beat; waveform seek; playlist; vinyl
- [ ] Teaser dialog timeline
- [ ] Intro timeline, scroll recede, hints, toasts
- [ ] Reduced-motion paths, a11y attributes, focus styles
- [ ] Event data from the CMS (accent, focal point, tagline, teaser track)

---

## 13. Credits

Photos: Unsplash (free to use under the Unsplash License), listed in `assets/CREDITS.md`. Avatars are Unsplash portraits. All event names, performers, prices and dates are sample content; venues are real Tehran halls used as realistic placeholders.
