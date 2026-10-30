# Hero · نسخه‌ی ۷ · زوم‌اوت و محو، کارت‌ها سمت راست · handoff spec

> **خلاصه برای خودت:** عکس اجرای فعال کل صفحه رو می‌گیره. اول کمی زوم‌شده‌ست و با گذشت ثانیه‌ها آروم زوم‌اوت می‌شه، بعد اجرای بعدی روش محو می‌شه.
> - **متن:** سمت چپ صفحه و راست‌چین، روی یه سایه‌ی تیره. تیتر، مکان و تاریخ، دو خط توضیح و دکمه‌ی خرید به رنگ اجرا.
> - **کارت‌ها:** سمت راست، کارت‌های ۱۶:۹ با دکمه‌ی بالا و پایین.
> - **هدر:** یه کپسول شناور با گوشه‌های کمی گرد.
>
> `index.html` همین پوشه مرجع زنده‌ست.

**Status:** v7, third round, rebuilt from scratch.

The first two rounds were built from a description of leemeenal.app, which can't be opened from the build environment, and both missed. This time the owner sent a screenshot of the reference and described the motion:
- **The zoom:** «عکس‌ها مقداری زوم شده، و ثانیه که می‌گذره زوم‌اوت می‌شه». The pictures start a little zoomed in and zoom out as the seconds pass.
- **The change:** «فید می‌شه و می‌ره رو بعدی… همین‌قدر ساده و جذاب». It fades into the next one; that simple.
- **The header:** «کپسولی… زاویه‌های مربعی، ولی کناره‌هاش مقداری نرم و گرد… نمی‌خوام خیلی گرد بشه». A capsule, squarish, with corners softened a little but not very round.

This version follows the screenshot's layout.

Shared with earlier versions and unchanged:
- **Sizing unit:** `--u`, 1% of the width on a 16:9 screen, smaller on wider ones (`../v5/SPEC.md`).
- **Music:** playlist, stored rhythm analysis, `audioSys` and `analyseTrack()` (`../v2/SPEC.md` §7).
- **Colours:** the fixed palette (`../v6/SPEC.md` §4).
- **Rules:** Persian/RTL (`../v2/SPEC.md` §11) and performance (`../v2/SPEC.md` §10).

---

## 1. Layout

```
┌──────────────────────────────────────────────────────────────────────┐
│ ╭────────────────────────────────────────────────────────────────╮   │
│ │ [ورود | ثبت‌نام]  ♪ تا ابد تو ▮▮   خانوادگی … تئاتر کنسرت  ▮▮▮ بلیت │   │  header capsule
│ ╰────────────────────────────────────────────────────────────────╯   │
│                                                      ( ˄ )           │
│      کنسرت پاپ : تور ۱۴۰۵ گروه نیمه‌شب | فرکانس       ┌────────┐      │
│               مجموعه ورزشی آزادی · سه‌شنبه ۲۴ آذر     │ card 1 │◀ active
│   تور تازه‌ی گروه نیمه‌شب، این بار در سالن ۱۲ هزار…    └────────┘      │
│                         …با هزاران نفری که با هم می‌خوانند. ┌────────┐ │
│                                    [ خرید بلیت ]     │ card 2 │      │
│      (the photo fills the screen, zooming out)        └────────┘      │
│                                                       … card 3, 4    │
│                                                      (❚❚)( ˅ )       │
└──────────────────────────────────────────────────────────────────────┘
```

- **Grid:** the hero is `100svh` tall (at least 600px) with two rows: `nav` / `cards . copy`.
  - In RTL the first column is on the right: the cards (`auto`), then an empty `1fr`, then the words (`minmax(0, 36u)`) on the left.
  - Padding is `1.2u` at the top, `2.6u` on the cards' side, `4.2u` on the words' side and `2.4u` at the bottom.
- **Shade:** a dark gradient from the left edge under the words: 0.8 at the edge, 0.62 at 26 %, 0.22 at 50 %, clear by 64 %. A light one goes at the top and at the bottom.

---

## 2. The header capsule

- **Shape:** a floating bar, `3.3u` tall (at least 54px), inside the page padding.
  - Its radius is `0.75u` (at least 12px): squarish, with the corners softened, not a pill.
  - Background `rgba(16, 14, 26, .64)`, a 1px border at 12 % white and a soft shadow underneath. No backdrop blur.
- **Contents, right to left:**
  - the logo with its five bars (an equaliser while music plays)
  - five categories (the current one bold and white)
  - pushed to the far end, the music control and «ورود | ثبت‌نام»
- **«ورود | ثبت‌نام»:** a white button with the same softened corners (`0.5u`, at least 9px).
- **Music control:** a round play button, the song's name (it opens the playlist panel) and four small bars.
- **Below 1100px wide:** the categories are hidden.
- **On phones:** the logo, the play button and a menu button.

---

## 3. The words

Right-aligned, in the left column, vertically centred:
1. **Title:** Vazirmatn 800, `1.85u` (at least 22px), line-height 1.6, `text-wrap: balance`, one or two lines.
   - It is written like the reference's: «دسته : عنوان | اسم», for example «کنسرت پاپ : تور ۱۴۰۵ گروه نیمه‌شب | فرکانس».
2. **Venue and date:** Vazirmatn 700, `0.95u`. The date uses the Persian calendar (`Intl.DateTimeFormat('fa-IR-u-ca-persian', { timeZone: 'Asia/Tehran' })`).
3. **Description:** `0.95u`, line-height 2. It always takes two lines and is clamped to them, so the block has one height.
4. **«خرید بلیت»:**
   - a pill (`3.1u` tall, at least `9.5u` wide) in the show's accent from the fixed palette, with text in its `onAccent` colour
   - a soft glow of the same colour under it
   - the colour changes with a 0.8 s transition

**On a change:**
- The four parts fade out (0.35 s, `power2.in`, moving up 8px, staggered by 0.03 s).
- At 0.4 s the new show's words and colour are written, and the parts fade in from 14px below (0.85 s, `power3.out`, staggered by 0.07 s).

---

## 4. The picture: zoomed in, zooming out, fading into the next

Each layer is `.lay > img`. The image uses `object-fit: cover`, with `object-position` from the show's `op` (`mop` on phones) and its zoom origin at `o`.

| t (s) | What happens |
|---|---|
| 0 | The new layer goes on top at `opacity 0`, its picture at `scale(1.15)`. |
| 0 → 1.2 | It fades in: opacity 0 → 1, `sine.inOut`. |
| 0 → 8.2 | Its picture zooms out linearly from 1.15 to 1, over the show's 7 s plus the next fade's 1.2 s. So it is still moving while the next one fades in over it. |
| 1.2 | The layers underneath are let go. |
| 7 | The next show starts. |

- **The panel's options:**
  - zoom 1.08 / 1.15 / 1.24
  - 5 / 7 / 10 s per show
  - a fade of 0.8 / 1.2 / 1.8 s
- **Before a fade:** the picture is decoded (`img.decode()`). After the intro, every show's full picture is preloaded one at a time.
- **Pausing:** the timer (`gsap.delayedCall`) and the top picture's zoom pause together when:
  - the pointer is over the cards, or focus is inside them
  - the pause button is pressed
  - the hero is scrolled away, or the tab is hidden
- **Reduced motion:** no zoom, a 0.4 s fade, and auto-advance starts paused.
- **Quick clicking:** each change fades in on top of the last, and a layer is let go once a layer above it has fully faded in. At most three layers stay in the DOM.
- **Intro:** the first picture fades in from the dark page, already zooming out. The header drops in, the cards slide in from the right, and the words fade up.

---

## 5. The cards

A column on the right, `15.5u` wide:
1. **Up bar:** a full-width pill (`1.85u` tall, 9 % white) with a chevron. It goes to the previous show.
2. **List:** one card per show, 16:9, radius `0.6u` (at least 10px), gap `0.75u`.
   - Each card shows the show's photo (`photos/name-640.webp`) and «کنسرت فرکانس» at the bottom, over a dark gradient.
   - The cards are `role="tab"` buttons in a `role="tablist"`.
   - Inactive cards have a 1px ring at 16 % white, and their picture grows 5 % on hover.
   - The active card has a 2px ring in the show's accent and a soft glow.
   - When the column is shorter than the list, the list scrolls so the active card stays in view; the page itself never moves.
3. **Bottom row:** the down bar (next show) and a small round pause button (`aria-pressed`).

**Keys:**
- ArrowDown or ArrowLeft: next show.
- ArrowUp or ArrowRight: previous show.
- Home and End: first and last show.
- Focus follows the active card.

**Clicking the active card** moves focus to the buy button.

**On phones:**
- The four cards are a row under the words, without names.
- The pause button sits at the row's end.
- The up and down bars are hidden.

---

## 6. Music

- **Playlist panel:**
  - the cover
  - a waveform you can scrub
  - previous and next
  - the list, with each song's tempo
  - «آهنگ خودت رو امتحان کن»
- **Songs:** the same tracks and stored analysis as v2–v6.
- **«تپش آروم تصویر»** (default):
  - the whole picture swells very slightly on each beat, `scale(1 + (kick·0.01 + downbeat·0.005)·level)` on the background
  - the logo's bars and the four small bars follow the song
  - the play button's ring pulses
- **«فقط میله‌ها»:** only the bars move.

---

## 7. Data model

```
{ id, pal: 'violet' | 'blue' | 'teal' | 'green' | 'gold' | 'orange' | 'crimson' | 'pink',
  type, name, title, desc, venue, startsAt, price, track,
  photo: { name, o, op, mop } }        // files: photos/name-{640,1920,2560}.webp
```
`title` is the full line on the hero («کنسرت پاپ : تور ۱۴۰۵ گروه نیمه‌شب | فرکانس»). `type` and `name` label the card.

The sample has four shows; the column fits four on every desktop screen tested, and more scroll.

**What makes a good photo:** landscape, at least 1920px wide, with the subject in the middle or on the right. The left half sits under the words.

---

## 8. Measured

- **Fit:** there is no horizontal scroll, nothing outside the hero, no overlap and no clipped text at:
  - 1920×1080, 1920×1028 (inside the comparison page) and 1920×940
  - 2560×1300, 1536×730 and 1440×900
  - 1366×768, 1366×650, 1280×720, 1280×600 and 1024×768
  - 390×844 and 360×700
- **Cards and words:**
  - All four cards are visible at every desktop size tested.
  - Every description fits its two lines.
  - Titles take one line, and two on the shortest screens.
- **Motion:**
  - The fade and the zoom were checked frame by frame on GSAP's own clock.
  - The timer and the zoom stop together with the pointer over the cards and with the pause button.
  - After five quick clicks 120 ms apart, and after fourteen changes in a row, one layer is showing, with the right words and the right active card.
- **Cost:**
  - **Idle:** about 3 ms of script per second.
  - **During a change:** 6 ms of script and 14 ms of style per second.
  - **With music playing:** 14 ms of script and 34 ms of style per second.
  - There is no layout per frame.
