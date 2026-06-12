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
| `characters.html` | "Learn a Character · 识字小馆" — interactive stroke-order explorer for 300 common characters in themed groups. |
| `404.html` | Custom not-found page; also catches URLs from the retired old site. |
| `learn/char-data.js` | **Generated** character content (pinyin, meaning, origin story, a common word **and** an example sentence each, stroke paths) — built by `scripts/build-char-data.py`. |
| `learn/explorer.js` | The explorer engine: stroke animation, options, keyboard navigation. |
| `learn/radical-data.js` | Hand-curated info for the 24 most useful radicals (nickname, meaning, story, position, extra examples). |
| `learn/radicals.js` | Renders the "Radical corner" section; example characters are matched live from `char-data.js` by radical, and clicking one opens it in the explorer. |

## Common updates

- **Photos** — see `images/README.md`. Gallery photos are `images/gallery-N.jpg`;
  add the next number and a matching tile in `#galleryGrid` in `index.html`.
  Keep files under ~500 KB.
- **Term dates / fees** — edit the matching section in `index.html`
  (search for `id="schedule"`, `id="fees"`).
- **Events** — add an `<article class="event" data-date="YYYY-MM-DD">` block in
  the `#events` section. Past events hide themselves automatically, and a
  "check back soon" note appears when none are upcoming — so old entries never
  need deleting, just add new ones.
- **Enrolment form** — replace `enrolment-form-2026.pdf` and update the link
  text in the `#enrolment` section for the new year.
- **Characters** — don't edit `learn/char-data.js` by hand. Add or change an
  entry in the curated table at the top of `scripts/build-char-data.py`
  (character, pinyin, gloss, theme group, example word) and run
  `python3 scripts/build-char-data.py`. The script fetches stroke paths and
  medians from [makemeahanzi](https://github.com/skishore/makemeahanzi)
  (cached in `.cache/`), sanity-checks pinyin against its dictionary, and
  regenerates the file. The wall, counter, theme filter, and navigation pick
  up changes automatically. Hand-written origin stories and example sentences
  live in the `OVERRIDES`/`ORIGIN_FIX` tables in the same script.
- **New pages** — add the page, link it from the nav, and add it to
  `sitemap.xml`.

## Checks

Every push and pull request runs `.github/workflows/checks.yml`:
`scripts/check-links.py` verifies that every local `src`/`href` resolves to a
real file, and `html-validate` (configured in `.htmlvalidate.json`) lints the
HTML. Run both locally the same way before pushing if you want a head start.

## Conventions

- English first, Chinese alongside; Chinese text gets `lang="zh-Hans"`.
- Stroke animations respect `prefers-reduced-motion`: nothing plays
  automatically for those users, but explicit Replay/tap actions still animate
  (the strokes are the lesson content).
- Images use `loading="lazy"` except the hero, which uses
  `fetchpriority="high"`.
- The explorer's read-aloud buttons use the browser's built-in Web Speech API
  (no external service); they stay hidden on browsers without a speech engine.
- Old URLs from the retired site (`about/classes/contact/enrolment.html`) are
  kept as tiny redirect stubs pointing at the matching `index.html` section.
