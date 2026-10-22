#!/usr/bin/env python3
"""CLI helper for adding, listing, and validating curated resources."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

from build import DATA_PATH, build, validate_payload


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "resource"


def cmd_add(args: argparse.Namespace) -> int:
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    url = args.url.strip()
    title = args.title.strip() if args.title else urlparse(url).netloc.replace("www.", "")
    rid = args.id.strip() if args.id else slugify(title)

    tags = [slugify(t) for t in args.tags.split(",") if t.strip()]
    scopes = [s.strip().lower() for s in args.scopes.split(",") if s.strip()]
    added = args.added or datetime.now(timezone.utc).strftime("%Y-%m-%d")

    entry = {
        "id": rid,
        "title": title,
        "url": url,
        "description": args.description.strip(),
        "category": args.category.strip(),
        "scopes": scopes,
        "tags": tags,
        "format": args.format,
        "access": args.access,
        "added": added,
        "featured": bool(args.featured),
    }
    if args.notes:
        entry["notes"] = args.notes.strip()

    data["resources"].append(entry)
    errors = validate_payload(data)
    if errors:
        for err in errors:
            print(f"ERROR: {err}", file=sys.stderr)
        return 1

    DATA_PATH.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Added '{title}' ({url}) as '{rid}'.")
    return build()


def cmd_list(_args: argparse.Namespace) -> int:
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    for r in data["resources"]:
        tags = ", ".join(f"#{t}" for t in r.get("tags", []))
        scopes = ", ".join(r.get("scopes", []))
        print(f"- {r['title']} ({r['url']}) [{r['category']} | {scopes}] {tags}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Manage curated internet resources.")
    sub = parser.add_subparsers(dest="command", required=True)

    add_p = sub.add_parser("add", help="Add a resource and rebuild site + README")
    add_p.add_argument("--url", required=True, help="Resource URL")
    add_p.add_argument("--title", required=True, help="Resource title")
    add_p.add_argument("--tags", required=True, help="Comma-separated tags (e.g. art,museum,free)")
    add_p.add_argument("--category", default="arts-culture", help="Category ID")
    add_p.add_argument("--scopes", default="family,personal", help="Comma-separated scopes")
    add_p.add_argument("--description", default="", help="Concise description")
    add_p.add_argument("--notes", default="", help="Optional family/personal note")
    add_p.add_argument("--format", default="archive", help="Resource format")
    add_p.add_argument("--access", default="free", help="Access model (free, freemium, paid, open-source, library)")
    add_p.add_argument("--id", default="", help="Optional custom slug ID")
    add_p.add_argument("--added", default="", help="Added date (YYYY-MM-DD)")
    add_p.add_argument("--featured", action="store_true", help="Mark as featured")
    add_p.set_defaults(func=cmd_add)

    list_p = sub.add_parser("list", help="List all curated resources")
    list_p.set_defaults(func=cmd_list)

    build_p = sub.add_parser("build", help="Validate and rebuild site + README")
    build_p.set_defaults(func=lambda _a: build())

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
