# Contributing

Kryon Showcase accepts public apps, tools, examples, and games built with
Kryon. Submissions are reviewed through pull requests.

## Quick Submission

Use the helper to create a project file:

```sh
python3 scripts/new_project.py \
  --slug my-kryon-app \
  --name "My Kryon App" \
  --summary "A short user-facing sentence describing what the app does." \
  --repo https://github.com/example/my-kryon-app \
  --homepage https://example.com/my-kryon-app \
  --banner https://raw.githubusercontent.com/example/my-kryon-app/master/showcase/banner.png \
  --tags app,kryon,desktop
```

Then run:

```sh
python3 scripts/validate.py
```

Open a pull request with the generated `projects/<slug>.json` file.

## Manual Submission

Copy `templates/project.json` to `projects/<slug>.json`, replace every example
value, and make sure the filename matches the `slug` field.

## Banner Requirements

- Use HTTPS.
- Use PNG, JPG, JPEG, or WebP.
- Use a 16:9 landscape image when possible.
- Avoid copyrighted screenshots or art you cannot redistribute.
- Prefer a real app screenshot or product banner that clearly represents the
  project.

## Ranking

Ranked entries must use trusted public source platforms. GitHub is supported
for automatic star counts in v1. GitLab and Codeberg entries are accepted but
may be marked `unranked` until their star counters are wired into the website
update script.
