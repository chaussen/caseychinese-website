# caseychinese.org — Casey Chinese School

Static website for Casey Chinese School (Casey 中文学校), a Saturday community
language school in Narre Warren, Victoria.

## Hosting

Served by **GitHub Pages** from the `main` branch, on the custom domain
`caseychinese.org` (configured via the `CNAME` file). There is no build step —
pushing to `main` deploys the site as-is within a few minutes.

Because GitHub Pages cannot send custom HTTP headers, the Content-Security-Policy
is delivered through a `<meta http-equiv="Content-Security-Policy">` tag in the
`<head>` of each page. If you add a new third-party script or resource, add its
origin to that tag on every page that uses it.

## Pages

| File | What it is |
|---|---|
| `index.html` | The whole main site: about, programs, textbooks, fees, enrolment, FAQ, 2026 schedule, events, gallery, contact. All CSS/JS is inline. |
| `characters.html` | "Learn a Character · 识字小馆" — interactive stroke-order explorer for twelve foundational characters. |
| `404.html` | Custom not-found page; also catches URLs from the retired old site. |
| `learn/char-data.js` | Character content (pinyin, meaning, origin story, example sentence, stroke paths). |
| `learn/explorer.js` | The explorer engine: stroke animation, options, keyboard navigation. |

## Common updates

- **Photos** — see `images/README.md`. Gallery photos are `images/gallery-N.jpg`;
  add the next number and a matching tile in `#galleryGrid` in `index.html`.
  Keep files under ~500 KB.
- **Term dates / fees / events** — edit the matching section in `index.html`
  (search for `id="schedule"`, `id="fees"`, `id="events"`).
- **Enrolment form** — replace `enrolment-form-2026.pdf` and update the link
  text in the `#enrolment` section for the new year.
- **Characters** — add an entry to `learn/char-data.js` (stroke paths and
  medians come from [makemeahanzi](https://github.com/skishore/makemeahanzi),
  1024-unit Y-up space). The wall, counter, and navigation pick it up
  automatically; update the "All twelve" heading if the count changes.
- **New pages** — add the page, link it from the nav, and add it to
  `sitemap.xml`.

## Conventions

- English first, Chinese alongside; Chinese text gets `lang="zh-Hans"`.
- Stroke animations respect `prefers-reduced-motion`: nothing plays
  automatically for those users, but explicit Replay/tap actions still animate
  (the strokes are the lesson content).
- Images use `loading="lazy"` except the hero, which uses
  `fetchpriority="high"`.
