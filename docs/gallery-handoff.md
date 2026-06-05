# Gallery Section — Scalable Redesign (Handoff)

This replaces the old hand-sized bento gallery (`g1`–`g7` classes) with an
**auto-flowing grid** that takes any number of photos with zero per-photo setup,
and **caps its height** behind a "Show all" expander so the section never grows
unbounded down the page.

## What to change

Three edits inside `index.html`, all scoped to the gallery. Nothing else changes.

1. Replace the gallery CSS block.
2. Replace the gallery `@media (max-width: 920px)` rules.
3. Replace the gallery markup (`<div class="gallery">…</div>`).
4. Add the gallery toggle script (inside the existing `<script>` at the end of `<body>`).

> Note: the gallery `<section>` already has `id="gallery"`. The grid `<div>` must
> use a **different** id (`galleryGrid`) — do not reuse `gallery`, or
> `getElementById` will grab the section and the expander will silently break.

---

## 1. CSS — replace the `/* ───── GALLERY ───── */` block

```css
/* ───── GALLERY ───── */
/* Auto-flowing grid: every tile is a plain .photo — drop in as many as you
   like, no per-photo sizing needed. A repeating rhythm gives a few tiles
   extra presence so the wall stays lively as it grows. */
.gallery {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  grid-auto-rows: 150px;
  grid-auto-flow: dense;
  gap: 12px;
}
.gallery .photo {
  border-radius: 4px;
  grid-column: span 1;
  grid-row: span 1;
}
/* repeating accent pattern — auto-applies no matter how many photos exist */
.gallery .photo:nth-child(9n+1) { grid-column: span 2; grid-row: span 2; }
.gallery .photo:nth-child(9n+5) { grid-column: span 2; }
.gallery .photo:nth-child(9n+8) { grid-row: span 2; }

/* collapsed state caps the wall to a tidy preview */
.gallery.is-collapsed .photo:nth-child(n+11) { display: none; }

.gallery-foot {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 18px;
  margin-top: 32px;
}
.gallery-foot::before,
.gallery-foot::after {
  content: '';
  height: 1px;
  flex: 1;
  background: var(--line);
}
.gallery-toggle {
  flex: none;
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 11px 22px;
  border-radius: 999px;
  border: 1.5px solid var(--line);
  background: var(--paper);
  color: var(--ink);
  font-family: var(--sans);
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: border-color .2s ease, color .2s ease, background .2s ease;
}
.gallery-toggle:hover { border-color: var(--red-soft); color: var(--red-deep); }
.gallery-toggle .count {
  color: var(--ink-mute);
  font-weight: 500;
}
.gallery-toggle .chev {
  transition: transform .25s ease;
  font-size: 11px;
}
.gallery-toggle[aria-expanded="true"] .chev { transform: rotate(180deg); }
```

---

## 2. CSS — replace the gallery lines inside `@media (max-width: 920px)`

Old (remove):

```css
.gallery { grid-template-columns: repeat(6, 1fr); grid-auto-rows: 100px; }
.g1 { grid-column: span 6; grid-row: span 2; }
.g2 { grid-column: span 6; grid-row: span 2; }
.g3, .g4, .g5, .g6, .g7 { grid-column: span 3; grid-row: span 1; }
```

New:

```css
.gallery { grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); grid-auto-rows: 110px; }
.gallery .photo:nth-child(9n+1) { grid-column: span 2; grid-row: span 2; }
.gallery .photo:nth-child(9n+5) { grid-column: span 2; grid-row: span 1; }
.gallery .photo:nth-child(9n+8) { grid-column: span 1; grid-row: span 2; }
.gallery.is-collapsed .photo:nth-child(n+9) { display: none; }
```

---

## 3. Markup — replace the `<div class="gallery">…</div>`

Each tile is identical apart from its `data-src`. The existing image-probe
script swaps in the real photo when the file exists, otherwise shows the
striped placeholder — that behavior is unchanged.

```html
<div class="gallery is-collapsed" id="galleryGrid">
  <div class="photo">
    <img alt="" data-src="images/gallery-1.jpg" />
    <div class="ph-fallback">images/gallery-1.jpg<br /><span style="opacity:.7">any size · crops to fit</span></div>
  </div>
  <!-- …repeat one .photo block per image… -->
</div>

<div class="gallery-foot" id="galleryFoot" hidden>
  <button class="gallery-toggle" id="galleryToggle" aria-expanded="false" aria-controls="galleryGrid">
    <span class="label">Show all</span>
    <span class="count"></span>
    <span class="chev">▾</span>
  </button>
</div>
```

### To add a photo
Just paste one more block — no classes, no sizing:

```html
<div class="photo">
  <img alt="" data-src="images/gallery-15.jpg" />
  <div class="ph-fallback">images/gallery-15.jpg<br /><span style="opacity:.7">any size · crops to fit</span></div>
</div>
```

Drop the file into `images/`. The grid reflows automatically and the
"Show all · N photos" count updates itself.

---

## 4. JS — add to the existing `<script>` at the end of `<body>`

```js
// gallery: cap the wall to a tidy preview, expand on demand.
// The cap matches the CSS nth-child rule (>10 on desktop, >8 on small screens).
(function () {
  const gallery = document.getElementById('galleryGrid');
  const foot = document.getElementById('galleryFoot');
  const btn = document.getElementById('galleryToggle');
  if (!gallery || !btn) return;
  const previewCount = () => window.matchMedia('(max-width: 920px)').matches ? 8 : 10;
  const total = gallery.querySelectorAll('.photo').length;

  function sync() {
    const hidden = total - previewCount();
    if (hidden > 0 && gallery.classList.contains('is-collapsed')) {
      foot.hidden = false;
      btn.querySelector('.label').textContent = 'Show all';
      btn.querySelector('.count').textContent = total + ' photos';
    } else if (hidden > 0) {
      foot.hidden = false;
      btn.querySelector('.label').textContent = 'Show less';
      btn.querySelector('.count').textContent = '';
    } else {
      foot.hidden = true;
    }
  }

  btn.addEventListener('click', () => {
    const expanded = gallery.classList.toggle('is-collapsed') === false;
    btn.setAttribute('aria-expanded', String(expanded));
    sync();
  });
  window.addEventListener('resize', sync, { passive: true });
  sync();
})();
```

---

## How it works (rationale)

- **Auto-flow + dense packing** (`grid-auto-flow: dense`) means tiles fill gaps
  left by the larger accent tiles, so the wall stays compact regardless of count.
- **`repeat(auto-fill, minmax(180px, 1fr))`** keeps a consistent tile size and
  adapts column count to the viewport — no fixed 12-column math to maintain.
- **`:nth-child(9n+…)`** applies the "feature / wide / tall" rhythm on a 9-tile
  loop, so visual variety repeats cleanly however many photos you add.
- **`.is-collapsed` + `:nth-child(n+11)`** hide everything past the preview with
  clean tile edges (no half-cropped photo). The JS only toggles that one class
  and keeps the button label/count in sync; the cap number is defined once in CSS.

## Tuning knobs

| Want to… | Change |
|---|---|
| Show more/fewer before "Show all" | `:nth-child(n+11)` in CSS **and** `previewCount()` in JS (keep them equal) |
| Bigger/smaller tiles | `minmax(180px, 1fr)` and `grid-auto-rows: 150px` |
| More/less white space between tiles | `gap: 12px` |
| Change accent-tile frequency | the `9n+…` selectors |
