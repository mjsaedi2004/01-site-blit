# Photo credits

All photos come from [Unsplash](https://unsplash.com) and are used under the [Unsplash License](https://unsplash.com/license) (free for commercial and non-commercial use, no permission needed). They are placeholders: the real site shows each event's own poster or photo.

| Files | Unsplash image | Notes |
|---|---|---|
| `events/pop-frequency-*` | https://images.unsplash.com/photo-1600442715242-3e496a4d7ec8 | flipped horizontally |
| `events/edm-spectrum-*` | https://images.unsplash.com/photo-1599739291127-15c456e459ee | flipped horizontally |
| `events/orchestra-chaharmezrab-*` | https://images.unsplash.com/photo-1759502418465-62fb7c781e73 | |
| `events/theatre-shadows-*` | https://images.unsplash.com/photo-1529229504105-4ea795dcbf59 | |
| `events/standup-bitaarof-*` | https://images.unsplash.com/photo-1728674115193-6febdf9fe365 | |
| `events/circus-parvaz-*` | https://images.unsplash.com/photo-1645287642975-fb04fa89347a | flipped horizontally |
| `avatars/a1.jpg` | https://images.unsplash.com/photo-1494790108377-be9c29b29330 | |
| `avatars/a2.jpg` | https://images.unsplash.com/photo-1506794778202-cad84cf45f1d | |
| `avatars/a3.jpg` | https://images.unsplash.com/photo-1534528741775-53994a69daeb | |

Three photos are flipped so the subject sits on the left, away from the right-aligned Persian text.

Sizes, all WebP from one 3200 px master per event:
- `name-1920.webp`, `name-2560.webp`, `name-3200.webp`: the stage background. The page picks the smallest one that covers the displayed width × device pixel ratio (capped at 2).
- `name-thumb.webp`, 720×360: the featured-rail card. It is cut from the same master around the event's focal point with the `cardCrop()` formula in `index.html`.

Music is not part of this repository; see `music/README.md`.
