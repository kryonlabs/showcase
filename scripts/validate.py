#!/usr/bin/env python3
import json
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECTS = ROOT / "projects"
HTTPS_RE = re.compile(r"^https://")
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
BANNER_RE = re.compile(r"^https://.*\.(png|jpg|jpeg|webp)$", re.I)
TRUSTED_HOSTS = {
    "github": "github.com",
    "gitlab": "gitlab.com",
    "codeberg": "codeberg.org"
}


def fail(path, message):
    print(f"{path}: {message}", file=sys.stderr)
    return 1


def check_string(path, data, key, min_len=1, max_len=220):
    value = data.get(key)
    if not isinstance(value, str):
        return fail(path, f"{key} must be a string")
    if len(value) < min_len or len(value) > max_len:
        return fail(path, f"{key} length must be {min_len}..{max_len}")
    return 0


def url_exists(url):
    request = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "kryon-showcase-validator"})
    try:
        with urllib.request.urlopen(request, timeout=12) as response:
            return 200 <= response.status < 400
    except Exception:
        request = urllib.request.Request(url, headers={"User-Agent": "kryon-showcase-validator"})
        try:
            with urllib.request.urlopen(request, timeout=12) as response:
                return 200 <= response.status < 400
        except Exception:
            return False


def validate_project(path):
    with path.open("r", encoding="utf-8") as fh:
        data = json.load(fh)

    allowed = {"schemaVersion", "slug", "name", "summary", "author", "repository", "homepage", "banner", "tags", "featured", "unranked"}
    extra = set(data) - allowed
    if extra:
        return fail(path, f"unknown fields: {', '.join(sorted(extra))}")
    if data.get("schemaVersion") != 1:
        return fail(path, "schemaVersion must be 1")
    if check_string(path, data, "slug", 2, 64):
        return 1
    if not SLUG_RE.match(data["slug"]):
        return fail(path, "slug must be lowercase hyphenated ASCII")
    if path.name != f"{data['slug']}.json":
        return fail(path, "filename must match slug")
    if check_string(path, data, "name", 1, 80) or check_string(path, data, "summary", 20, 220):
        return 1

    author = data.get("author")
    if not isinstance(author, dict):
        return fail(path, "author must be an object")
    if not isinstance(author.get("name"), str) or not 1 <= len(author["name"]) <= 80:
        return fail(path, "author.name must be a short string")
    if not isinstance(author.get("url"), str) or not HTTPS_RE.match(author["url"]):
        return fail(path, "author.url must be an HTTPS URL")

    repo = data.get("repository")
    if not isinstance(repo, dict):
        return fail(path, "repository must be an object")
    for key in ("platform", "url", "owner", "name"):
        if not isinstance(repo.get(key), str) or not repo[key]:
            return fail(path, f"repository.{key} must be a non-empty string")
    if repo["platform"] not in TRUSTED_HOSTS:
        return fail(path, "repository.platform must be github, gitlab, or codeberg")
    expected_host = TRUSTED_HOSTS[repo["platform"]]
    if not repo["url"].startswith(f"https://{expected_host}/"):
        return fail(path, f"repository.url must use https://{expected_host}/")

    if "homepage" in data and (not isinstance(data["homepage"], str) or not HTTPS_RE.match(data["homepage"])):
        return fail(path, "homepage must be an HTTPS URL")

    banner = data.get("banner")
    if not isinstance(banner, dict) or not isinstance(banner.get("url"), str):
        return fail(path, "banner.url must be present")
    if not BANNER_RE.match(banner["url"]):
        return fail(path, "banner.url must be an HTTPS image URL")
    if "alt" in banner and (not isinstance(banner["alt"], str) or len(banner["alt"]) > 140):
        return fail(path, "banner.alt must be a short string")

    tags = data.get("tags")
    if not isinstance(tags, list) or not 1 <= len(tags) <= 8:
        return fail(path, "tags must contain 1..8 values")
    if len(tags) != len(set(tags)):
        return fail(path, "tags must be unique")
    for tag in tags:
        if not isinstance(tag, str) or not SLUG_RE.match(tag) or len(tag) > 32:
            return fail(path, "tags must be lowercase hyphenated ASCII")
    for key in ("featured", "unranked"):
        if key in data and not isinstance(data[key], bool):
            return fail(path, f"{key} must be boolean")

    if "--check-urls" in sys.argv and not url_exists(banner["url"]):
        return fail(path, f"banner URL is not reachable: {banner['url']}")

    return 0


def main():
    paths = sorted(PROJECTS.glob("*.json"))
    if not paths:
        return fail(PROJECTS, "no project files found")
    seen = set()
    rc = 0
    for path in paths:
        rc |= validate_project(path)
        slug = path.stem
        if slug in seen:
            rc |= fail(path, "duplicate slug")
        seen.add(slug)
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
