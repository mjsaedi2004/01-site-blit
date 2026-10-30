# Hero · نسخه‌ی ۵ · صحنه و هاله (stage and halo) · handoff spec

> **خلاصه برای خودت:** این نسخه مستقیم از روی دو نمونه‌ای که صاحب پروژه فرستاد ساخته شده. وسط صحنه یه اجراکننده‌ی دوربری‌شده هست که به رنگ همون اجرا تک‌رنگ شده و جلوی یه دایره‌ی خط‌خطی نور ایستاده (نمونه‌ی ب). سمت راست تیتر خیلی بزرگ و فشرده‌ی دوخطی هست، با یه جمله‌ی نستعلیق که روش افتاده (نمونه‌ی الف). سمت چپ کارت آدم‌ها و کارت بلیت قرار داره، و پایین صفحه کارت‌های جایگاه ویژه، شمارنده و پخش‌کننده. هر اجرا رنگ خودش رو داره و کل صحنه با همون رنگ روشن می‌شه. موقع پخش آهنگ، بالای خط‌های هاله مثل اکولایزر با موزیک می‌زنه. `index.html` همین پوشه مرجع زنده‌ست.

**Status:** v5, new. After four rounds the owner still hadn't found a version they liked («نه جالب نیستن… یه طرح متفاوت بساز»), so this one follows their two references closely:
- **A**, a festival hero: cut-out singer, «FEEL THE SOUND» with a script line, social-proof card, ticket card, player, countdown, lineup.
- **B**, a conference hero: cut-out figure in front of a striped circle, «FUTURE / VISION» in two colours, an arrow circle, speaker cards, yellow ticket buttons.

Versions 1–4 sit beside it in `../` for comparison.

**Stack:** HTML + CSS + vanilla JS + GSAP 3.13 + Web Audio + one 2D canvas (the halo). No WebGL; no blur, backdrop-filter or blend modes.

---

## 1. The idea

A dark stage card, inset from the window edges, holds everything:
- **Centre:** the performer, cut out of their photo and tinted in the show's colour, stands in front of a circle made of vertical stripes of light. Two soft stage beams fall from the top. Two small chips float beside them.
- **Right:** a chip with the performer, then the title in two lines: the kind of show in white and its name in the show's colour, with an arrow circle beside the name. A handwritten Nastaliq line crosses the title's foot. Below come two lines of description, the buy button and «listen to the teaser».
- **Left:** a card with faces and «۱۲۰ هزار+», then a ticket card with a paper ticket that turns over for each show.
- **Bottom:** the featured shows as small picture cards, a countdown, and the music player.

Every show brings a colour set, and the whole stage is lit in it. On a change:
1. The halo's stripes fall from right to left.
2. The performer steps down and the next one rises.
3. The words turn over and the ticket turns.
4. The halo rises again in the new colour.

---

## 2. Layout

All sizes follow one unit:
```css
--u: clamp(11px, min(1vw, 1.7778svh), 26px);   /* 19.2px at 1920×1080 */
```
On a 16:9 screen `--u` is 1% of the width. On a wider or shorter window the height limits it, so the composition keeps its proportions and never overflows. Text never goes below 11–13px (`max(13px, …)`).

| Part | Value |
|---|---|
| Hero | `height: 100svh; min-height: 560px`; padding `--m = .75u` |
| Stage | radius `1.6u`, background `#0b0915`, 1px `rgba(255,255,255,.08)` inner border, `overflow: hidden` |
| Stage grid | columns `minmax(0,1fr) minmax(0,1fr) max(230px, 18.5u)` (RTL: copy, scene, aside); rows `auto minmax(0,1fr) auto` (nav, main, bottom); column gap `2u`, row gap `1.1u`; padding `1.2u 2.1u 1.3u` |
| Nav | `2.5u` high: logo (five bars + «بلیت»), five links, search, «ورود», «خرید بلیت» pill with a yellow ticket circle |
| Copy | bottom-aligned in the main row, so a smaller title never moves the buttons |
| Scene | spans the main and bottom rows of the middle column, with negative margins into the gaps so it reaches the stage's bottom edge; `container-type: size`, so the performer and the halo are sized in `cqh` / `cqw` |
| Aside | bottom-aligned column: social card (auto height), ticket card (`flex: 0 1 23u`, min `16u`) |
| Bottom row | `max(150px, 10.2u)` high; columns `1fr  max(300px, 21u)  max(330px, 23u)` (featured shows, countdown, player) |

Measured: there is no horizontal scroll, nothing leaves the stage and none of the main blocks overlap at these sizes:
- 1920×1080 and 1920×1028 (inside the comparison page)
- 1920×940, 2560×1300, 1536×730, 1440×900
- 1366×768, 1366×650, 1280×720, 1280×600, 1024×768

Smaller screens:
- **1101–1280px wide:** «ورود» is hidden.
- **901–1100px wide:** the links are hidden and the countdown card is dropped; the ticket still shows the date.
- **Phones (≤ 900px):** one column. The scene comes first, `min(118vw, 620px)` high. The copy comes up 110px over its faded bottom, then the cards stack, and the featured row scrolls sideways with snap.

The featured row shows four cards when its inner width is over 760px, three up to that and two below 470px. It uses a container query on `.rail-view`.

---

## 3. Tokens

**Neutrals:**
- page `#06050b`, stage `#0b0915`
- card `rgba(20,17,31,.8)` with a 1px `rgba(255,255,255,.08)` border; radius `1.25u` (the inner cards in the featured row use `.95u`)
- ink `#f7f5fd`, ink-2 70 %, ink-3 46 %

**The show's colour.** Each show has a set. It is written once per change, as CSS variables on the stage, at the moment the new words arrive (`MID = 0.5 s` into the change), and is never animated as a variable.

| Show | accent | light | deep | pop | text on accent |
|---|---|---|---|---|---|
| کنسرت فرکانس | `#8b5cf6` violet | `#c4b5fd` | `#2e1065` | `#facc15` | white |
| فستیوال طیف | `#3b82f6` blue | `#93c5fd` | `#0c2a6b` | `#facc15` | white |
| چهار مضراب | `#d9a441` gold | `#f5d48b` | `#4a300a` | `#a78bfa` | `#1a1206` |
| نمایش سایه‌ها | `#e11d48` crimson | `#fda4af` | `#4c0519` | `#facc15` | white |
| استندآپ بی‌تعارف | `#f97316` orange | `#fdba74` | `#5a2205` | `#a78bfa` | `#1b0d03` |
| سیرک پرواز | `#14b8a6` teal | `#5eead4` | `#053d37` | `#facc15` | `#03201c` |

Where the colours appear:
- **accent:** the second title line, the buy button, the dots, the play button, the waveform's played part, the logo bars, the halo's lower stripes and the glow.
- **light:** the Nastaliq line, the top of the halo stripes and the stage beams.
- **deep:** the ticket card and the floor glow.
- **pop:** the circle on the ticket buttons, yellow as in reference B (violet on the warm shows).

The review panel has «بنفش، مثل نمونه‌ها», which uses the violet set and violet-tinted cut-outs for every show.

**Type:**
| Role | Font | Size |
|---|---|---|
| Title, prices, countdown digits, «۱۲۰ هزار+», card names | **Noto Sans Arabic** 900 at width 62.5 % (a condensed black, like the references' condensed caps); option: Lalezar | title `8.2u` (157px at 1080p), shrunk to fit the column (`--fit`) |
| Handwritten line | **Noto Nastaliq Urdu** 600, subset to the taglines | `2.25u`, line-height 1.95, `rotate(3deg)` so it rises toward its end on the left, pulled up `-1.45u` over the title's foot |
| Everything else | **Vazirmatn** 300–800 | `.64u`–`.96u`, never under 11px |

The title's two lines are `.ln` rows with a space between them, so screen readers read «کنسرت فرکانس». Each word sits in a `.w > .wi` mask (padding `.16em .05em .3em`, so Persian dots and descenders aren't clipped). Easing: `--ease: cubic-bezier(.16,1,.3,1)`; `--ease-io: cubic-bezier(.77,0,.175,1)`.

---

## 4. The scene

### 4.1 Performer cut-outs
How each image is made, in production on upload:
1. **Remove the background.** We used `rembg` with the `isnet-general-use` model.
2. **Crop** to the subject.
3. **Tint** with a tritone in the show's colours (shadow, mid, highlight), keeping 20 % of the original colour: `out = tritone(lum) * .8 + rgb * .2`. Contrast goes up slightly first.
4. **Fade the bottom 20 %** to transparent so the body melts into the stage. Not for floating subjects like the acrobat.
5. **Export** `name.webp` (max 1500×1700) and `name-card.webp` (max 420×460), plus `-violet` versions for the violet option.

The tritones:

| Show | shadow | mid | highlight |
|---|---|---|---|
| violet | `#0d0620` | `#7c3aed` | `#f0e6ff` |
| blue | `#050a20` | `#2563eb` | `#e2ecff` |
| gold | `#140b03` | `#b7791f` | `#fff1d6` |
| crimson | `#170309` | `#be123c` | `#ffe1e8` |
| orange | `#170a02` | `#ea580c` | `#ffe9d6` |
| teal | `#021412` | `#0d9488` | `#dcfff9` |

**Placement:** each show stores `fig: { h, x, b, flip }`, the height in % of the scene height, the shift in % of its width, the lift from the bottom, and a mirror. The singer is mirrored so she looks up toward the title. The acrobat floats (`b: 16`).

### 4.2 The halo (canvas)
The canvas is a square centred at (50 %, 37 cqh). Its size is `min(80cqw, 60cqh) / .72`, so the visible circle has radius `R = 0.72 × half the canvas`, with room left over for the crown and the rings. DPR is capped at 1.5.

**Stripes:**
- Number of stripes: `n = round(diameter / 14px)`, from 24 to 60.
- Each stripe is a vertical bar on a chord of the circle.
- Width: 38 % of the pitch.
- One vertical gradient serves every stripe: light at the top, accent at the centre, transparent by `c + R`. The circle reads clearly at the top and melts behind the performer's shoulders.
- A radial glow sits behind the stripes: accent, 20 % alpha at about `1.1R`.

**Per stripe `k`:**
- `vis[k]` (0–1) is the visible length, measured up from the stripe's bottom end.
- `ext[k]` (0–1) is the music crown, up to `0.17R` above the circle.

**Waves:**
| Kind | Duration | Order | Ease per stripe |
|---|---|---|---|
| intro | 1.8 s | from the centre out | quart out |
| out (a change) | `MID` = 0.5 s | right to left | cubic in |
| in (a change) | 1.1 s | right to left | quart out |

Each stripe runs `q = clamp(p·(1+S) − order·S, 0, 1)` with `S = 0.9`, so they ripple instead of moving together.

**Redraws:**
- **Idle:** one slow band of light crosses the stripes about every 8 s. It is drawn at about 25 fps and nothing else redraws.
- **Waves and music:** every frame.
- **Hidden hero or tab:** no drawing at all.

### 4.3 Light, chips and depth
**Glow:** two stacked layers, each with four radial gradients:
- the show's accent behind the performer, at the scene's real centre (`--sx`, measured from the grid);
- a light spill at the top;
- a deep floor glow;
- a side wash.

A change sets the colours on the hidden layer and cross-fades the two (1.4 s, `--ease-io`).

**Beams:** two cones of light, built from a `conic-gradient` mask so their edges are soft. Each sways about 9° (11 s and 13 s, `alternate`), with a soft flare where they meet. They dip to 15 % during a change and come back in the new colour.

**Chips:** the show's badge with a star, and a mood word with a bolt («پرفروش · فراموش‌نشدنی», …). They bob ±.35u (5.5 s and 6.5 s). On a change they pop out (`scale .6`, 0.32 s) and back in (`back.out(2.2)`, 0.85 s).

**Depth:** the cursor moves each layer by its own amount (lerp `1 − e^(−2.6·dt)`):
| Layer | Movement |
|---|---|
| halo | 8 × 6 px |
| performer | 18 × 12 px |
| chips | 26–30 × 20–24 px |

The performer also floats `−.7u` over 7 s.

---

## 5. Cards

**Social:**
- three avatars overlapping by `.55u`, then a «+» in the accent that turns 90° on hover;
- «۱۲۰ هزار+» counts up on load (2.2 s, `expo.out`);
- «نفر امسال با بلیت به تماشا رفتند» and «از فروردین ۱۴۰۵».

**Ticket:**
- **Card:** the deep colour, with a top-left accent bloom and a white sheen.
- **Paper ticket:** `#f6f3fb`, aspect 1.62, `rotate(-8deg)`. The stub (27 %) holds a CSS barcode and «№ 0128». The perforation is a dashed line with two notches cut by a radial-gradient mask.
- **Main part:** «بلیت» with the accent dot, «۱۴۰۵», the show's type, its name (fitted, never cut), weekday, date, time and venue.
- **Under the ticket:** the kind («پیش‌فروش ویژه»), seat and date, the price («از ۱٫۸ میلیون»), and a white arrow button.
- **Hover:** the ticket tilts toward the cursor (up to 14° × 18°) with a moving glare.
- **Change:** it turns away (`rotationY −90°`, 0.45 s) and back (`90° → 0`, 1.1 s `expo.out`), and the three lines below rise through masks.

**Featured shows** («جایگاه ویژه», like B's speaker cards):
- **Header:** title, «۰۱ / ۰۶», previous / pause / next, «همه‌ی اجراها».
- **Each card:** the cut-out on a radial gradient of its own colours, then the type, the name (fitted), the date, a 2px timer line and a ↖ arrow circle.
- **Active card:** framed in its colour, with a soft halo of the same colour. With «محو», the default the owner asked for, the frame fades onto the next card: opacity `0 → 1`, `scale 1.06 → 1` over 0.75–1 s. With «لغزان», one frame glides from card to card (0.85 s `expo.inOut`).
- **Timer:** the line fills over `--dur` = 7 s, and its `animationend` moves to the next show.
- **Hidden cards** wait on the left; the row slides by one card (0.9 s `--ease-io`) when the next one is out of view.
- **Hover:** a card lifts 3px, its picture zooms to 1.07 and its arrow fills.

**Countdown** (like A): «تا شروع اجرا» and the show's name, then روز, ساعت, دقیقه and ثانیه, right to left, with thin dividers. Each digit is an odometer strip of 20 digits:
- each second rolls up (0.7 s `expo.out`);
- a change spins every digit (1.1 s + 0.05 s per digit, `expo.inOut`).

**Player** (like A):
- the cover (the stored square, or one drawn from the title), the song, «artist · ۸۰ ضرب», and a playlist button;
- a waveform drawn from the stored peaks: played part in the accent, hover preview, click or drag to seek, arrow keys ±5 s;
- times and controls stay LTR (media convention);
- the playlist opens upward, with covers, beats per minute, durations and «آهنگ خودت رو امتحان کن».

---

## 6. Motion

### 6.1 Intro (~2 s)
Everything starts hidden from the first frame, so nothing flashes.

| t (s) | What |
|---|---|
| 0 | the stage card fades in from `scale .985` (1.2 s) |
| 0.1 | the glow blooms (2.2 s) |
| 0.3 | the beams come down (2.2 s); the halo's stripes grow from the centre outward (1.8 s) |
| 0.2–0.34 | logo, links and buttons drop in (stagger .05) |
| 0.45 | the performer rises: `yPercent 9 → 0`, `scale 1.04 → 1`, fade (1.7 s `expo.out`) |
| 0.55–0.6 | the chip rises; the title words rise through their masks (1.15 s, stagger .09) |
| 0.92 | the arrow circle spins in (`back.out`); the Nastaliq line writes from right to left (mask `--reveal 0 → 115 %`, 1.4 s `power2.inOut`) |
| 0.8–1.2 | the aside cards, the ticket (from `rotationY 75°`), the bottom cards and the featured cards rise (stagger) |
| 0.9 / 1.2 | the count-up; the countdown spins |
| 1.4 | the chips pop in |

### 6.2 A change
| t (ms) | What |
|---|---|
| 0 | the halo's stripes fall, right to left (500 ms); the old performer steps down `yPercent 4, scale .97` and fades (520 ms `power2.in`) |
| 0 | the title words rise out (`yPercent −108`, 480 ms `power3.in`, stagger 50); the Nastaliq line fades; chip text and description leave upward |
| 0 | chips pop out; the ticket turns away; the beams dip; the countdown spins; the glow starts its 1.4 s cross-fade |
| 380 | the new performer rises: `yPercent 8 → 0`, `scale 1.05 → 1`, fade (1.3 s `expo.out`) |
| 500 | **the colour set changes**; new words rise in; the Nastaliq line writes (from 850 ms); the halo rises again, right to left, in the new colour (1.1 s); the ticket turns back; the chips pop in; the beams return |

If the user clicks again mid-change, the pending half is cancelled and the new change starts from whatever is on screen. Tested with four clicks 120 ms apart.

**Reduced motion:**
- a 0.2–0.4 s fade instead of all of the above;
- no auto-advance, no idle bob, float or sway;
- the halo is drawn once.

---

## 7. Music

The player and the rhythm analysis are the same as before (`../v2/SPEC.md` §7): the beat times, downbeat, a 4 Hz energy curve, waveform peaks and the loudest 12 s of each song are stored with the track. The songs are shared in `../assets/music/`.

### «هاله و نور» (default)
**Crown:** the top of each stripe follows a frequency band, with bass in the middle and highs at the edges, mirrored. Each band is measured against its own level over the last second: `lift = clamp(.2 + (band − avg) / .14, 0, 1)`. So the crown moves with the music instead of sitting at full height on a loud song. It rises fast (×0.5 per frame) and falls slowly (×0.12).

**Beat and bar:**
- every beat swells the halo `scale(1 + kick·.028)` and brightens the stripes;
- every bar sends a thin ring out from the circle, fading over about a second;
- the performer breathes `scale(1 + kick·.008)`;
- the beams' opacity goes `.6 + .4·(kick·.7 + energy·.35)`.

**Meters:** the logo's five bars become a small meter using the same relative measure. The play and teaser buttons get a pulse ring.

### «فقط نشانگرها»
Only the meters and the pulse rings react.

### Teaser
«شنیدن تیزر» plays the show's song from its loudest 12 s:
- a 0.8 s fade in, then after 12 s a 0.9 s fade out, and the player pauses;
- pressing it again stops it the same way;
- touching the player cancels the teaser and keeps playing.

Measured on desktop Chrome at 1920×1080 while playing: about 12 ms of script and 21 ms of style work per second. The only layouts are about four a second, from the time label.

---

## 8. Admin fields

**Show:**
```
{ type, category, titleLines[2], name, performerChip, tagline, description,
  badge, mood, venue, startsAt (ISO, +03:30), ticket { kind, seat, priceFrom, serial },
  colours { accent, light, deep, pop, onAccent },
  cutout { master, card, violet?, placement { h, x, b, flip } }, track,
  featured { from, to, order } }
```

On upload:
1. The admin uploads a photo and the server cuts it out.
2. The admin picks a colour set, or accepts one suggested from the photo, with a contrast check for the button text.
3. The server bakes the tinted cut-outs.
4. The admin nudges the placement on a preview of this scene.

**Track:** `{ title, artist, file, cover?, analysis }`. The analysis runs once on upload (`analyseTrack()`).

---

## 9. Rules

1. **Motion:**
   - Continuous motion only on `transform` and `opacity`, plus the halo canvas, which redraws only while a wave or a song is running, or at about 25 fps for the idle light.
   - Per-frame writes only when a value changes.
   - Never animate inherited custom properties.
2. **Persian:**
   - Don't split words into letters.
   - Masks keep room for dots and descenders.
   - The Nastaliq line needs its tall line-height.
   - Clocks, digits and media rows stay LTR; the countdown units run right to left.
   - Arrows are mirrored; media icons aren't.
3. **Accessibility:**
   - The hero is `aria-roledescription="carousel"`, and the copy is `aria-live="off"` during auto-advance.
   - The featured row is a tablist: arrow keys follow RTL, and focus or hover pauses it.
   - The countdown is read as one sentence.
   - The halo, beams, chips and performer are decorative (`aria-hidden`).
4. **Content:** the cut-outs are placeholders from Unsplash (see `assets/CREDITS.md`). A band logo on one shirt was painted out.
