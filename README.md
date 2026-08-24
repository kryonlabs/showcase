# Kryon Showcase

This repository is the public submission index for apps built with Kryon.
Projects listed here can appear on kryonlabs.com and in other Kryon showcase
surfaces.

## Submit A Project

Fast path:

```sh
python3 scripts/new_project.py \
  --slug my-kryon-app \
  --name "My Kryon App" \
  --summary "A short user-facing sentence describing what the app does." \
  --author "Example Author" \
  --author-url https://example.com \
  --repo https://github.com/example/my-kryon-app \
  --banner https://raw.githubusercontent.com/example/my-kryon-app/master/showcase/banner.png \
  --homepage https://example.com/my-kryon-app \
  --tags app,kryon,desktop
python3 scripts/validate.py
```

Manual path:

1. Copy `templates/project.json` to `projects/<slug>.json`.
2. Use a stable, lowercase slug with hyphens.
3. Point `repository.url` at a public source repository.
4. Point `banner.url` at a public 16:9 PNG, JPG, or WebP image.
5. Open a pull request.

If you do not want to edit JSON yourself, open a Project submission issue and
maintainers can turn it into a pull request.

Ranked projects are sorted by stars from supported platforms. GitHub is supported
for ranked entries in v1. Other public Git platforms may be listed by setting
`unranked` to `true` until a star counter is added.

## Metadata

Each project file follows `schema/project.schema.json`.

Required fields:

- `schemaVersion`: currently `1`
- `slug`: unique project slug
- `name`: user-facing app name
- `summary`: one-sentence user-facing summary
- `author`: public author name and website
- `repository`: public source repository
- `banner`: public 16:9 showcase image
- `tags`: short lowercase tags

Optional fields:

- `homepage`: app or docs website
- `featured`: first-party or curated feature candidate
- `unranked`: exclude from star ranking

## Stars

The website consumes this repository as metadata, then resolves star counts from
supported public APIs. If a host cannot be counted reliably, the project remains
visible but is not eligible for the top-10 ranked block.
