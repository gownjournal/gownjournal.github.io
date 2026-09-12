# The Gown Journal

Source for [gownjournal.github.io](https://gownjournal.github.io), an editorial guide to wedding dresses published by the team behind Lace & Love.

Built with [Eleventy](https://www.11ty.dev/). Deployed to GitHub Pages by the workflow in `.github/workflows/deploy.yml` on every push to `main`.

## Local development

```bash
npm install
npm run serve
```

## Adding a guide

Create `src/posts/<slug>.md` with front matter (`title`, `description`, `date`, `category`, optional `faq`) and Markdown body. `category` must be one of the slugs in `src/_data/categories.json`. Site settings live in `src/_data/site.json`.
