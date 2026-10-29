# مرجع رابط کاربری سایت بلیت · UI reference

این پوشه مرجع طراحی (UI) سایت بلیت است. صفحه‌ی اصلی رو بخش به بخش اینجا می‌سازیم. هر بخش یه پروتوتایپ زنده‌ی HTML داره، با یه فایل `SPEC.md` که Claude دسکتاپ از روش همون بخش رو تو سایت اصلی پیاده می‌کنه.

This folder is the UI reference for the ticketing site. The home page is designed **one section at a time**. Each section has a live HTML prototype plus a `SPEC.md` handoff that the desktop agent uses to build it in the real codebase. The prototypes are the source of truth for look and motion.

## چطور ببینی · How to view

```bash
cd ui-reference/01-hero && npx http-server -p 8000
```
Then open http://localhost:8000. Use a local server rather than double-clicking the file. Pick one that supports range requests (`http-server` does), so the music player can seek. The songs aren't in git; see [`01-hero/assets/music/README.md`](01-hero/assets/music/README.md).

Hosted previews (private to the owner; the hero preview includes the songs):
- Moodboard of 16 international ticketing, festival and theatre sites: https://claude.ai/artifact/G67hnwxgRA75NhkLfJZUAP
- Hero: https://claude.ai/artifact/FMdoTVhR22nUCmfX76FvjU

## بخش‌ها · Sections

| # | بخش | Section | Status | Refs |
|---|---|---|---|---|
| 1 | هیرو (صحنه) | Hero: the featured poster on a colour halo, date card, featured poster rail, music pill with rhythm detection | **v3, waiting for feedback** → [`01-hero`](01-hero/) | الف، ب، ۱۰، ۱۵ |
| 2 | جستجو با حال‌وهوا | Mood search ("something funny", "date night", "this weekend") | next | ۳، ۵ |
| 3 | پرفروش‌های هفته | Weekly best sellers with giant numbers | later | ۳ |
| 4 | قفسه‌ی تئاتر | Theatre poster shelf | later | ۵، ۱۴ |
| 5 | تقویم رویدادها | Events calendar (month + selected day) | later | ۱۳، ۹ |
| 6 | هنرمندها | Artists as stories | later | ۷، ۲ |
| 7 | سالن‌ها | Venues | later | ۸، ۱۶ |
| 8 | قسطی، پکیج، اپ، فوتر | Instalments, packages, app, footer | later | ۱۱، ۵ |

Reference numbers point to [`references.md`](references.md).

## قواعد مشترک همه‌ی بخش‌ها · Shared rules

- Dark stage look: neutrals `#09080d / #100f16`, few elements, no backdrop blur. Events are shown by their **graphic posters** (2:3), never stock photos; each event's accent and glow colours come from its poster.
- Type: Lalezar (display), Vazirmatn (UI and body), Noto Nastaliq Urdu (taglines only).
- Motion: GSAP for timelines, WAAPI or CSS for compositor-only effects; `expo.out` for entrances, `power3.in` for exits; always a reduced-motion path.
- Performance: continuous animation only on `transform` and `opacity`; no WebGL, backdrop-filter or blend modes on moving layers; nothing restyles the whole page per frame. See [`01-hero/SPEC.md` §10](01-hero/SPEC.md#10-performance-rtl-and-accessibility-rules).
- RTL rules (no per-letter splitting, LTR clocks and media bars, mirrored arrows, unmirrored media icons) are in the same section.
