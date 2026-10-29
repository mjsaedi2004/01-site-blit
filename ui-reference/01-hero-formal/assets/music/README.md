# موزیک‌ها · Music

فایل‌های صوتی تو گیت نیستن، چون آهنگ‌ها مال صاحبانشون هستن و این مخزن عمومیه. نسخه‌ی خصوصی پیش‌نمایش خودش آهنگ‌ها رو داره.

The audio files are **not committed** (the songs belong to their rights holders and this repository is public). The private hosted preview carries its own copies.

To run locally, put the same three files as hero v2 here (copies or symlinks to `../../../01-hero/assets/music/`):
- `dayan-ta-abad-to.mp3`
- `majid-razavi-manam.mp3`
- `aron-afshar-sanie-var.mp3`

Use a server with HTTP range support (`npx http-server`) so the player can seek. Their rhythm analysis is already embedded in `index.html`. Any other song is analysed in the browser; to try one, use «آهنگ خودت رو امتحان کن» in the playlist.
