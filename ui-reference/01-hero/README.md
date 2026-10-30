# هیرو · نسخه‌ها · Hero versions

همه‌ی نسخه‌های هیرو اینجا کنار هم هستن. `index.html` همین پوشه یه صفحه‌ست با زبانه‌های ۱ تا ۵ که هر نسخه رو زیرش نشون می‌ده، برای مقایسه.

Every hero version, side by side. `index.html` in this folder is the comparison page: tabs 1–5 on top (or keys 1–5, or `#v1` … `#v5` in the URL), and the chosen version underneath.

| Version | Folder | What it is | Status |
|---|---|---|---|
| ۱ | [`v1/`](v1/) | First round: WebGL stage with stage lights reacting to synthesised music, ticket deck, big countdown, bento player | kept for comparison |
| ۲ | [`v2/`](v2/) | Sharp photos, the featured rail like reference B, a date card, the player with rhythm detection, four reaction modes | kept (the owner's preferred base so far) |
| ۳ | [`v3/`](v3/) | Graphic posters (original artwork) in a calm, poster-centred layout | kept for comparison; the owner didn't like it |
| ۴ | [`v4/`](v4/) | Formal editorial spread with more life: colour photo melting into the page, the show's own colour, Nastaliq line, drifting light and a cursor spotlight, light that breathes with the music | kept for comparison; the owner didn't find it interesting |
| ۵ | [`v5/`](v5/) | Built closely on the owner's two references: a cut-out performer tinted in the show's colour in front of a striped circle of light that moves with the music, a huge condensed two-line title with a Nastaliq line, a ticket card, featured cards, countdown and player | new, waiting for feedback |

Each version has its own `SPEC.md` handoff and assets. The songs are shared in `assets/music/` and aren't committed (see the README there).

```bash
cd ui-reference && npx http-server -p 8000
# open http://localhost:8000/01-hero/         (the comparison page)
# or   http://localhost:8000/01-hero/v5/      (one version on its own)
```
Version 1 needs WebGL for its stage; without it, it shows a CSS fallback.
