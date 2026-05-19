# Life Lessons

Personal essays in Hindi and English, published at [lessons.rajanagori.in](https://lessons.rajanagori.in).

Built with [Hugo](https://gohugo.io/) and the [PaperMod](https://github.com/adityatelange/hugo-PaperMod) theme.

## Add a new post

1. Create a file in `content/posts/` with front matter:

```yaml
---
title: "Your title"
date: 2026-05-19T10:00:00+00:00
draft: false
---
```

2. Write the body in Markdown below the front matter.
3. Push to `main` — GitHub Actions builds and deploys the site.

Set `draft: true` to hide a post from the live site.

## Local preview

```bash
git submodule update --init --recursive
hugo server -D
```

Open http://localhost:1313

## Deploy (GitHub Pages)

Pushes to `main` run `.github/workflows/hugo-deploy.yml`.

**One-time setup** in the GitHub repo:

1. **Settings → Pages → Build and deployment** → Source: **GitHub Actions**
2. Keep your DNS pointing `lessons.rajanagori.in` at GitHub Pages (CNAME is in `static/CNAME`)

## Images

Place images in `static/Attachments/` and reference them as `/Attachments/your-image.jpg` in Markdown.
