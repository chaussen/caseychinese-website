# Images

Drop photos into this folder using the filenames below.
GitHub Pages serves them automatically from your custom domain.

## In use

| Filename | Where |
|---|---|
| hero.jpg | Homepage hero, right side |
| gallery-1.jpg … gallery-20.jpg | Homepage gallery (gallery-15 is .webp) |
| logo.png | Nav logo on every page |
| zhongwen-series.jpg | Textbooks section photo |
| wechat-qr.png | Contact section — WeChat QR |
| whatsapp.png | Contact section — WhatsApp QR |

## Adding gallery photos

Add the next number in the sequence (`gallery-21.jpg`, …) and add a matching
`<div class="photo">…</div>` tile inside `#galleryGrid` in `index.html`.
The grid lays photos out automatically — no per-photo sizing needed — and the
"Show all" expander picks up the new count on its own.

JPG, PNG, and WebP all work. Keep files under ~500 KB for fast page loads
(photos are lazy-loaded, but smaller is still better).
