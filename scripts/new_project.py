#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
PROJECTS = ROOT / "projects"
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
HOST_PLATFORMS = {
    "github.com": "github",
    "gitlab.com": "gitlab",
    "codeberg.org": "codeberg"
}


def parse_repo(url):
    parsed = urlparse(url)
    if parsed.scheme != "https":
        raise SystemExit("repository URL must use https")
    platform = HOST_PLATFORMS.get(parsed.netloc.lower())
    if not platform:
        raise SystemExit("repository host must be github.com, gitlab.com, or codeberg.org")

    parts = [part for part in parsed.path.split("/") if part]
    if len(parts) < 2:
        raise SystemExit("repository URL must include owner and repo name")
    owner = parts[0]
    name = parts[1]
    if name.endswith(".git"):
        name = name[:-4]
    return platform, owner, name


def parse_tags(raw):
    tags = [tag.strip() for tag in raw.split(",") if tag.strip()]
    if not tags:
        raise SystemExit("at least one tag is required")
    for tag in tags:
        if not SLUG_RE.match(tag):
            raise SystemExit(f"invalid tag: {tag}")
    return tags


def main():
    parser = argparse.ArgumentParser(description="Create a Kryon showcase project JSON file.")
    parser.add_argument("--slug", required=True, help="Lowercase project slug, e.g. my-kryon-app.")
    parser.add_argument("--name", required=True, help="Public project name.")
    parser.add_argument("--summary", required=True, help="One user-facing sentence.")
    parser.add_argument("--author", required=True, help="Public author name.")
    parser.add_argument("--author-url", required=True, help="Public HTTPS author website.")
    parser.add_argument("--repo", required=True, help="Public HTTPS repository URL.")
    parser.add_argument("--banner", required=True, help="Public HTTPS banner image URL.")
    parser.add_argument("--homepage", help="Optional HTTPS homepage URL.")
    parser.add_argument("--tags", required=True, help="Comma-separated tags, e.g. app,desktop,tool.")
    parser.add_argument("--featured", action="store_true", help="Mark as featured. Maintainers may change this.")
    parser.add_argument("--unranked", action="store_true", help="Exclude from star ranking.")
    args = parser.parse_args()

    if not SLUG_RE.match(args.slug):
        raise SystemExit("slug must be lowercase letters, numbers, and hyphens")
    platform, owner, repo_name = parse_repo(args.repo)
    if args.homepage and not args.homepage.startswith("https://"):
        raise SystemExit("homepage must use https")
    if not args.author_url.startswith("https://"):
        raise SystemExit("author URL must use https")
    if not args.banner.startswith("https://"):
        raise SystemExit("banner must use https")

    data = {
        "schemaVersion": 1,
        "slug": args.slug,
        "name": args.name,
        "summary": args.summary,
        "author": {
            "name": args.author,
            "url": args.author_url
        },
        "repository": {
            "platform": platform,
            "url": args.repo,
            "owner": owner,
            "name": repo_name
        },
        "banner": {
            "url": args.banner,
            "alt": f"{args.name} showcase banner"
        },
        "tags": parse_tags(args.tags),
        "featured": bool(args.featured)
    }
    if args.homepage:
        data["homepage"] = args.homepage
    if args.unranked:
        data["unranked"] = True

    path = PROJECTS / args.slug / "project.json"
    if path.exists():
        raise SystemExit(f"{path} already exists")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2)
        fh.write("\n")
    print(path.relative_to(ROOT))


if __name__ == "__main__":
    main()
