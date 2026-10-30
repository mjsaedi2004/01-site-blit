# موزیک‌ها · Music

فایل‌های صوتی این پوشه تو گیت نیستن. آهنگ‌ها مال صاحبانشون هستن و این مخزن عمومیه. نسخه‌ی خصوصی پیش‌نمایش خودش آهنگ‌ها رو داره.

The audio files are **not committed** (the songs belong to their rights holders and this repository is public). The private hosted preview carries its own copies. Versions 2–7 all read the songs from here (`../assets/music/` from their folders); version 1 synthesises its own music.

## اجرا روی سیستم خودت · Running locally

Put the files here with exactly these names:

| File | Track |
|---|---|
| `dayan-ta-abad-to.mp3` | دایان · تا ابد تو |
| `majid-razavi-manam.mp3` | مجید رضوی · منم |
| `aron-afshar-sanie-var.mp3` | آرون افشار · ثانیه وار |
| `majid-razavi-manam.webp`, `aron-afshar-sanie-var.webp` | optional square covers (versions 2, 3, 5, 6 and 7); without them the player draws a cover from the title |

Serve `ui-reference/` with a server that supports HTTP range requests (`npx http-server`), so the players can seek. Python's `http.server` plays the songs but can't seek.

## ریتم · Rhythm data

The rhythm analysis for these three songs is embedded in each version's `index.html`, between `/* ANALYSIS:start */` and `/* ANALYSIS:end */`. It holds the tempo, every beat time, the downbeat, a 4 Hz energy curve, the waveform peaks and the loudest 12 s. Any other song is analysed in the browser by `analyseTrack()`; to try one, use «آهنگ خودت رو امتحان کن» in a player's playlist. In production, run it once when the admin uploads a track and store its JSON next to the track (`v2/SPEC.md` §7).
