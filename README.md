# Kryon Showcase

This repository is the public submission index for apps built with Kryon.
Projects listed here can appear on kryonlabs.com and in other Kryon showcase
surfaces.

## Submit A Project

1. Add a JSON file under `projects/<slug>.json`.
2. Use a stable, lowercase slug with hyphens.
3. Point `repository.url` at a public source repository.
4. Point `banner.url` at a public 16:9 PNG, JPG, or WebP image.
5. Open a pull request.

Ranked projects are sorted by stars from trusted platforms. GitHub is supported
for ranked entries in v1. Other public Git platforms may be listed by setting
`unranked` to `true` until a trusted star counter is added.

## Metadata

Each project file follows `schema/project.schema.json`.

Required fields:

- `schemaVersion`: currently `1`
- `slug`: unique project slug
- `name`: user-facing app name
- `summary`: one-sentence user-facing summary
- `repository`: public source repository
- `banner`: public 16:9 showcase image
- `tags`: short lowercase tags

Optional fields:

- `homepage`: app or docs website
- `featured`: first-party or curated feature candidate
- `unranked`: exclude from star ranking

## Trusted Ranking

The website consumes this repository as metadata, then resolves star counts from
trusted public APIs. If a host cannot be counted reliably, the project remains
visible but is not eligible for the top-10 ranked block.
