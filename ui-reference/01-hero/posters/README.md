# پوسترهای نمونه · Sample posters

شش پوستر گرافیکی که جای پوستر واقعی هر اجرا نشستن. تو سایت اصلی پوستری که برگزارکننده آپلود می‌کنه جاشون رو می‌گیره.

Six graphic posters standing in for each event's real poster. On the live site they are replaced by the poster the organiser uploads.

- `source.html`: all six designs as 600×900 HTML/SVG compositions, with a shared system: a top line with the category and date, one motif, a large Persian title, a bottom line with the venue and time, and grain.
- `render.js`: renders each `.poster` at 2× to `../assets/posters/<id>.webp` (1200×1800) and `<id>-thumb.webp` (400×600). It needs Playwright and Python Pillow.

```bash
cd ui-reference/01-hero && npx http-server -p 8765 &
node posters/render.js http://127.0.0.1:8765/posters/source.html
```
