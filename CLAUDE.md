# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A Jekyll site hosted on GitHub Pages at https://jonbrauer2.github.io/ezra-blog/. Content is written under the persona of "Ezra," an AI assistant producing Seventh-day Adventist devotional, Sabbath School, and health content. There is no application code — everything is Markdown content, Liquid templates, and Jekyll config. The `baseurl` is `/ezra-blog`, so all internal links must be prefixed (`/ezra-blog/...`) or use the `relative_url` filter.

## Build / preview

GitHub Pages builds the site automatically on push to `main`. No build step is required when editing content. To preview locally:

```
bundle install        # one-time; requires Ruby + bundler
bundle exec jekyll serve --baseurl ""   # omit baseurl for localhost
```

`Gemfile` pins to the `github-pages` gem, so the local stack matches what Pages will build with.

A `.github/workflows/daily-rebuild.yml` cron pushes an empty commit at 05:00 UTC daily so that the site re-renders and time-dependent Liquid logic (see below) advances even without new content.

## Content model — collections, not posts

The site uses Jekyll **collections**, not the standard `_posts` directory. (`daily-devotional/_posts/` exists but is not the active source; live devotionals live in `_devotionals/`.) Three collections are configured in `_config.yml`:

| Collection      | Source dir         | Permalink pattern                                    | Landing page              |
|-----------------|--------------------|------------------------------------------------------|---------------------------|
| `devotionals`   | `_devotionals/`    | `/daily-devotional/:year/:month/:day/:title/`        | `daily-devotional/index.md` |
| `sabbathschool` | `_sabbathschool/`  | `/sabbathschool/:path/`                              | `sabbathschool/index.md`  |
| `healthtips`    | `_healthtips/`     | `/healthtips/:year/:month/:day/:title/`              | `healthtips/index.md`     |

`future: true` is set, so posts dated in the future build and are served — but the landing pages filter them out at render time using `site.time` comparisons. Adding a future-dated devotional will not appear on the index until its date arrives, even though the file is built.

`health-papers/` is **not** a collection — it holds standalone HTML files linked from `health-papers/index.md`.

## Front matter conventions (must match for index pages to work)

The landing pages (`daily-devotional/index.md`, `sabbathschool/index.md`) do non-trivial Liquid grouping that depends on specific front-matter keys. When adding new content, mirror the existing files in that collection.

**Devotionals** (`_devotionals/YYYY-MM-DD-slug.md`):
- `layout: post`, `title`, `date` (with time + offset, e.g. `2026-05-21 05:30:00 -0500`)
- `image`, `excerpt`, `scripture`
- `week_start` (YYYY-MM-DD of the week's Sunday) and `week_dates` (human label) — the index groups devotionals into weekly sections by `week_start`. Files without `week_start` fall into an "Earlier devotionals" bucket.

**Sabbath School lessons** (`_sabbathschool/<quarter>/lesson-NN-slug.md`):
- `layout: post`, `title`, `date`, `image`, `excerpt`
- `quarter` (e.g. `"Q4 2026"`), `series`, `lesson_dates`
- `category: lesson-guide` — the index splits on this; non-lesson-guide entries are rendered under "Reference & Background."

**Health tips** (`_healthtips/YYYY-MM-DD-slug.md`): `layout: post`, `title`, `date`, `image`.

## "Current" item selection logic

Both `daily-devotional/index.md` and `sabbathschool/index.md` find the most-recent item whose `date` is `<= site.time` and render it as a highlighted card; older items collapse into `<details>` accordions. Two consequences:

- Local `bundle exec jekyll serve` will show whichever content is "current" relative to the system clock; production picks up the new day via the cron rebuild.
- The "current week" / "current quarter" sections are styled differently from past ones — don't try to remove the duplication by rendering both branches the same way without testing.

## Image and asset paths

Images live under `assets/images/{devotionals,healthtips,sabbathschool}/...` and are referenced with absolute `/ezra-blog/...` paths in front matter and body markdown. Keep that prefix — relative paths break on the GitHub Pages baseurl.

## Theming

`remote_theme: jekyll/minima` — no theme files are vendored. Custom styling is inline in landing-page Liquid (style attributes), not in a stylesheet. If you need site-wide style changes, that means either overriding minima via `assets/css/style.scss` or editing the inline styles in each index page.

## Things to be careful about

- **Don't move files between collections** without updating `_config.yml` permalinks and any internal links — permalink patterns differ.
- **Don't commit `Gemfile.lock`** (it's gitignored; GitHub Pages resolves its own versions).
- **Daily rebuild commits** (`chore: daily rebuild ...`) are expected noise in `git log`; ignore them when looking for content changes.
