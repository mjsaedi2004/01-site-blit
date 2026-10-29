# مرجع رابط کاربری سایت بلیت · UI reference

این پوشه مرجع طراحی (UI) سایت بلیت است. صفحه‌ی اصلی رو بخش به بخش اینجا می‌سازیم. هر بخش یه پروتوتایپ زنده‌ی HTML داره، با یه فایل `SPEC.md` که Claude دسکتاپ از روش همون بخش رو تو سایت اصلی پیاده می‌کنه.

This folder is the UI reference for the ticketing site. The home page is designed **one section at a time**; each section has a live HTML prototype plus a `SPEC.md` handoff that the desktop agent uses to build it in the real codebase. The prototypes are the source of truth for look and motion.

## چطور ببینی · How to view

```bash
cd ui-reference/01-hero && python3 -m http.server 8000
```
Open http://localhost:8000. Use a local server, not a double-click: WebGL needs the photos served over HTTP.

Hosted previews (private to the owner):
- Moodboard of 16 international ticketing/festival/theatre sites: https://claude.ai/artifact/G67hnwxgRA75NhkLfJZUAP
- Hero v1: https://claude.ai/artifact/FMdoTVhR22nUCmfX76FvjU

## بخش‌ها · Sections

| # | بخش | Section | Status | Refs |
|---|---|---|---|---|
| 1 | هیرو (صحنه) | Hero: live stage + featured ticket deck + player + countdown | **v1, waiting for feedback** → [`01-hero`](01-hero/) | الف، ب، ۱۰، ۱۵ |
| 2 | جستجو با حال‌وهوا | Mood search ("something funny", "date night", "this weekend") | next | ۳، ۵ |
| 3 | پرفروش‌های هفته | Weekly best sellers with giant numbers | later | ۳ |
| 4 | قفسه‌ی تئاتر | Theatre poster shelf | later | ۵، ۱۴ |
| 5 | تقویم رویدادها | Events calendar (month + selected day) | later | ۱۳، ۹ |
| 6 | هنرمندها | Artists as stories | later | ۷، ۲ |
| 7 | سالن‌ها | Venues | later | ۸، ۱۶ |
| 8 | قسطی، پکیج، اپ، فوتر | Instalments, packages, app, footer | later | ۱۱، ۵ |

Reference numbers point to [`references.md`](references.md).

## قواعد مشترک همه‌ی بخش‌ها · Shared rules

- Dark stage look; neutrals `#07060b / #0e0c15`, glass cards, one accent at a time through `--accent` (per event, brand violet `#a78bfa` by default).
- Type: Lalezar (display), Vazirmatn (UI/body), Noto Nastaliq Urdu (taglines only).
- Motion: GSAP; `expo.out` for entrances, `power3.in` for exits, `power2.inOut` for scene changes; always a reduced-motion path.
- RTL rules (no per-letter splitting, LTR clocks and media bars, mirrored arrows, unmirrored media icons) are in [`01-hero/SPEC.md`](01-hero/SPEC.md#9-persian--rtl-rules-important).
