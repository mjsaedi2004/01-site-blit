# موزیک‌ها · Music

فایل‌های صوتی این پوشه تو گیت نیستن. آهنگ‌ها مال صاحبانشون هستن و این مخزن عمومیه. نسخه‌ی خصوصی پیش‌نمایش (artifact) خودش آهنگ‌ها رو داره.

The audio files are **not committed**: the songs belong to their rights holders and this repository is public. The private hosted preview carries its own copies.

## اجرا روی سیستم خودت · Running locally

Put the files here with exactly these names:

| File | Track |
|---|---|
| `dayan-ta-abad-to.mp3` | دایان · تا ابد تو |
| `majid-razavi-manam.mp3` | مجید رضوی · منم |
| `aron-afshar-sanie-var.mp3` | آرون افشار · ثانیه وار |
| `majid-razavi-manam.webp`, `aron-afshar-sanie-var.webp` | optional square covers; without them the player draws a cover from the title |

Serve the folder with a server that supports HTTP range requests, so the player can seek and the teaser can jump to the chorus. `npx http-server ui-reference/01-hero` works. Python's `http.server` plays the songs but can't seek.

## ریتم · Rhythm data

The rhythm analysis for these three songs is already embedded in `index.html`, between `/* ANALYSIS:start */` and `/* ANALYSIS:end */`. It holds the tempo, every beat time, the downbeat, a 4 Hz energy curve, the waveform peaks, the loudest 12 s and the reaction style.

Any other song is analysed in the browser by `analyseTrack()`, which takes about 2–3 s for a 3-minute song. You can try this with «آهنگ خودت» in the prototype panel or the playlist. In production, run the same function once when the admin uploads a track and store its JSON next to the track; see `../../SPEC.md` §7.
