# مرجع رابط کاربری سایت بلیت · UI reference

این پوشه مرجع طراحی (UI) سایت بلیت است. صفحه‌ی اصلی رو بخش به بخش اینجا می‌سازیم. هر بخش یه پروتوتایپ زنده‌ی HTML داره، با یه فایل `SPEC.md` که Claude دسکتاپ از روش همون بخش رو تو سایت اصلی پیاده می‌کنه.

This folder is the UI reference for the ticketing site. The home page is designed **one section at a time**. Each section has a live HTML prototype plus a `SPEC.md` handoff that the desktop agent uses to build it in the real codebase. The prototypes are the source of truth for look and motion.

## چطور ببینی · How to view

```bash
cd ui-reference && npx http-server -p 8000
```
Then open http://localhost:8000/01-hero/ to compare the hero versions. Use a local server rather than double-clicking the file. Pick one that supports range requests (`http-server` does), so the music player can seek. The songs aren't in git; see [`01-hero/assets/music/README.md`](01-hero/assets/music/README.md).

Hosted previews (private to the owner; the hero preview includes the songs):
- Moodboard of 16 international ticketing, festival and theatre sites: https://claude.ai/artifact/G67hnwxgRA75NhkLfJZUAP
- Hero, all versions on one page (tabs 1–7): https://claude.ai/artifact/FMdoTVhR22nUCmfX76FvjU

## بخش‌ها · Sections

| # | بخش | Section | Status | Refs |
|---|---|---|---|---|
| 1 | هیرو (صحنه) | Hero: seven versions side by side (v1 WebGL stage, v2 photo + featured rail, v3 posters, v4 formal and alive, v5 cut-out performer and striped halo after references A and B, v6 = v5 working with posters, banners, photos or nothing, plus a demo admin panel, v7 sparse: a full-screen photo that slowly zooms, four small boxes at the side and the next poster opening softly from the middle, after leemeenal.app) | **v7 new, waiting for feedback; v5 liked** → [`01-hero`](01-hero/) | الف، ب، ۱۰، ۱۵، leemeenal.app |
| 2 | جستجو با حال‌وهوا | Mood search ("something funny", "date night", "this weekend") | next | ۳، ۵ |
| 3 | پرفروش‌های هفته | Weekly best sellers with giant numbers | later | ۳ |
| 4 | قفسه‌ی تئاتر | Theatre poster shelf | later | ۵، ۱۴ |
| 5 | تقویم رویدادها | Events calendar (month + selected day) | later | ۱۳، ۹ |
| 6 | هنرمندها | Artists as stories | later | ۷، ۲ |
| 7 | سالن‌ها | Venues | later | ۸، ۱۶ |
| 8 | قسطی، پکیج، اپ، فوتر | Instalments, packages, app, footer | later | ۱۱، ۵ |

Reference numbers point to [`references.md`](references.md).

## قواعد مشترک همه‌ی بخش‌ها · Shared rules

- Dark stage look: neutrals `#07060b / #0e0c15`, solid translucent panels (no backdrop blur), one accent at a time through `--accent` (per event; brand violet `#a78bfa` as the default).
- Type: Lalezar (display), Vazirmatn (UI and body), Noto Nastaliq Urdu (taglines only).
- Motion: GSAP for timelines, WAAPI or CSS for compositor-only effects; `expo.out` for entrances, `power3.in` for exits; always a reduced-motion path.
- Performance: continuous animation only on `transform` and `opacity`; no WebGL, backdrop-filter or blend modes; nothing restyles the whole page per frame. See [`01-hero/v2/SPEC.md` §10](01-hero/v2/SPEC.md#10-performance-rules).
- RTL rules (no per-letter splitting, LTR clocks and media bars, mirrored arrows, unmirrored media icons) are in [`01-hero/v2/SPEC.md` §11](01-hero/v2/SPEC.md#11-persian--rtl-rules).
