#!/usr/bin/env python3
"""Validate data/resources.json and build static GitHub Pages site + README.md."""

from __future__ import annotations

import html
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "data" / "resources.json"
TEMPLATE_PATH = ROOT / "src" / "template.html"
SITE_DIR = ROOT / "site"
README_PATH = ROOT / "README.md"

SLUG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
CONTROL_CHAR_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
VALID_FORMATS = {
    "interactive",
    "archive",
    "reference",
    "tool",
    "reading",
    "video",
    "course",
    "game",
    "community",
}
VALID_ACCESS = {"free", "freemium", "paid", "open-source", "library"}


def get_domain(url: str) -> str:
    parsed = urlparse(url)
    host = parsed.netloc or url
    return re.sub(r"^www\.", "", host)


def validate_payload(data: dict) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["Root payload must be a JSON object."]

    for key in ("meta", "scopes", "categories", "resources"):
        if key not in data:
            errors.append(f"Missing top-level key: {key}")
    if errors:
        return errors

    scope_ids = {s.get("id") for s in data["scopes"] if isinstance(s, dict)}
    category_ids = {c.get("id") for c in data["categories"] if isinstance(c, dict)}

    seen_ids: set[str] = set()
    seen_urls: set[str] = set()

    for idx, res in enumerate(data["resources"]):
        prefix = f"resources[{idx}]"
        if not isinstance(res, dict):
            errors.append(f"{prefix}: must be an object")
            continue

        for req in ("id", "title", "url", "tags", "category", "scopes", "added"):
            if req not in res:
                errors.append(f"{prefix}: missing required field '{req}'")

        rid = res.get("id", "")
        if rid:
            if not SLUG_RE.match(rid):
                errors.append(f"{prefix}: invalid id slug '{rid}'")
            if rid in seen_ids:
                errors.append(f"{prefix}: duplicate id '{rid}'")
            seen_ids.add(rid)

        url = res.get("url", "")
        if url:
            parsed = urlparse(url)
            if parsed.scheme not in ("http", "https") or not parsed.netloc:
                errors.append(f"{prefix}: invalid http(s) url '{url}'")
            if url in seen_urls:
                errors.append(f"{prefix}: duplicate url '{url}'")
            seen_urls.add(url)

        cat = res.get("category", "")
        if cat and cat not in category_ids:
            errors.append(f"{prefix}: unknown category '{cat}'")

        scopes = res.get("scopes", [])
        if not isinstance(scopes, list) or not scopes:
            errors.append(f"{prefix}: 'scopes' must be a non-empty list")
        else:
            for sc in scopes:
                if sc not in scope_ids:
                    errors.append(f"{prefix}: unknown scope '{sc}'")

        tags = res.get("tags", [])
        if not isinstance(tags, list) or not tags:
            errors.append(f"{prefix}: 'tags' must be a non-empty list")
        else:
            for tag in tags:
                if not isinstance(tag, str) or not SLUG_RE.match(tag):
                    errors.append(f"{prefix}: invalid tag '{tag}' (use lowercase kebab-case)")

        fmt = res.get("format")
        if fmt is not None and fmt not in VALID_FORMATS:
            errors.append(f"{prefix}: invalid format '{fmt}'")

        acc = res.get("access")
        if acc is not None and acc not in VALID_ACCESS:
            errors.append(f"{prefix}: invalid access '{acc}'")

        added = res.get("added", "")
        if added and not DATE_RE.match(added):
            errors.append(f"{prefix}: invalid date '{added}' (expected YYYY-MM-DD)")

        for field_name, val in res.items():
            if isinstance(val, str) and CONTROL_CHAR_RE.search(val):
                errors.append(f"{prefix}: field '{field_name}' contains disallowed control characters")

    return errors


def render_ssr_cards(data: dict) -> str:
    scope_map = {s["id"]: s["label"] for s in data["scopes"]}
    cat_map = {c["id"]: c["label"] for c in data["categories"]}
    cards: list[str] = []

    for r in data["resources"]:
        domain = html.escape(get_domain(r["url"]))
        fmt_suffix = f" · {html.escape(r['format'])}" if r.get("format") else ""
        scopes_html = "".join(
            f'<span class="scope-badge" data-scope="{html.escape(sc)}">'
            f"{html.escape(scope_map.get(sc, sc))}</span>"
            for sc in r.get("scopes", [])
        )
        tags_html = "".join(
            f'<button type="button" class="tag-pill" data-card-tag="{html.escape(t)}">'
            f"#{html.escape(t)}</button>"
            for t in r.get("tags", [])
        )
        notes_html = (
            f'<p class="card-notes">{html.escape(r["notes"])}</p>'
            if r.get("notes")
            else ""
        )
        cat_label = html.escape(cat_map.get(r["category"], r["category"]))

        cards.append(
            f'<article class="resource-card" id="res-{html.escape(r["id"])}">'
            f'  <div class="card-top">'
            f'    <div class="card-meta-row">'
            f'      <span class="domain-badge">{domain}{fmt_suffix}</span>'
            f'      <div class="badges-group">{scopes_html}</div>'
            f"    </div>"
            f'    <h2 class="card-title">'
            f'      <a href="{html.escape(r["url"])}" target="_blank" rel="noopener noreferrer">'
            f'        <span>{html.escape(r["title"])}</span>'
            f'        <span class="ext-arrow" aria-hidden="true">↗</span>'
            f"      </a>"
            f"    </h2>"
            f'    <p class="card-desc">{html.escape(r.get("description", ""))}</p>'
            f"    {notes_html}"
            f"  </div>"
            f'  <div class="card-footer">'
            f'    <div class="card-tags">{tags_html}</div>'
            f'    <span class="card-category">{cat_label}</span>'
            f"  </div>"
            f"</article>"
        )

    return f'<div class="cards-grid">{"".join(cards)}</div>'


def render_bookmarks_html(data: dict) -> str:
    cat_map = {c["id"]: c["label"] for c in data["categories"]}
    lines = [
        "<!DOCTYPE NETSCAPE-Bookmark-file-1>",
        '<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">',
        f"<TITLE>{html.escape(data['meta']['title'])}</TITLE>",
        f"<H1>{html.escape(data['meta']['title'])}</H1>",
        "<DL><p>",
    ]
    for cat in data["categories"]:
        entries = [r for r in data["resources"] if r["category"] == cat["id"]]
        if not entries:
            continue
        lines.append(f"  <DT><H3>{html.escape(cat_map[cat['id']])}</H3>")
        lines.append("  <DL><p>")
        for r in entries:
            tags_attr = ",".join(r.get("tags", []))
            lines.append(
                f'    <DT><A HREF="{html.escape(r["url"])}" TAGS="{html.escape(tags_attr)}">'
                f'{html.escape(r["title"])}</A>'
            )
            if r.get("description"):
                lines.append(f'    <DD>{html.escape(r["description"])}')
        lines.append("  </DL><p>")
    lines.append("</DL><p>")
    return "\n".join(lines) + "\n"


def render_readme(data: dict) -> str:
    meta = data["meta"]
    owner = meta["owner"]
    resources = data["resources"]
    scope_map = {s["id"]: s["label"] for s in data["scopes"]}
    cat_map = {c["id"]: c["label"] for c in data["categories"]}

    lines = [
        f"# {meta['title']}",
        "",
        f"> {meta['subtitle']}",
        "",
        f"**Live Site:** [https://{owner}.github.io/curated/](https://{owner}.github.io/curated/)",
        "",
        "A curated directory of enduring internet resources for personal and family use, organized across multiple views and scopes:",
        "",
        f"- **Cards View:** [`#view=cards`](https://{owner}.github.io/curated/#view=cards) — Editorial cards with descriptions, notes, scopes, and tags",
        f"- **Compact Index:** [`#view=index`](https://{owner}.github.io/curated/#view=index) — Dense table view for rapid scanning",
        f"- **Category Directory:** [`#view=directory`](https://{owner}.github.io/curated/#view=directory) — Grouped by subject area",
        f"- **Tag Atlas:** [`#view=tags`](https://{owner}.github.io/curated/#view=tags) — Cross-referenced tag matrix",
        "",
        "---",
        "",
        "## Browse by Scope",
        "",
        "| Scope | Description | Entries | Direct View |",
        "| :--- | :--- | :---: | :--- |",
    ]

    for sc in data["scopes"]:
        count = sum(1 for r in resources if sc["id"] in r.get("scopes", []))
        lines.append(
            f"| **{sc['label']}** | {sc['description']} | {count} | "
            f"[Open {sc['label']} View](https://{owner}.github.io/curated/#scope={sc['id']}) |"
        )

    lines.extend(["", "## Resources by Category", ""])

    for cat in data["categories"]:
        entries = [r for r in resources if r["category"] == cat["id"]]
        if not entries:
            continue
        lines.append(f"### {cat['label']}")
        lines.append("")
        lines.append(f"*{cat['description']}*")
        lines.append("")
        for r in entries:
            tags_str = " ".join(f"`#{t}`" for t in r.get("tags", []))
            scopes_str = ", ".join(scope_map.get(s, s) for s in r.get("scopes", []))
            lines.append(f"- **[{r['title']}]({r['url']})** ({get_domain(r['url'])}) — {r.get('description', '')}")
            lines.append(f"  - *Scopes:* {scopes_str} · *Tags:* {tags_str}")
            if r.get("notes"):
                lines.append(f"  - *Note:* {r['notes']}")
        lines.append("")

    # Tag index
    tag_map: dict[str, list[dict]] = {}
    for r in resources:
        for t in r.get("tags", []):
            tag_map.setdefault(t, []).append(r)

    lines.extend(["## Tag Index", ""])
    for tag in sorted(tag_map.keys()):
        linked = ", ".join(f"[{r['title']}]({r['url']})" for r in tag_map[tag])
        lines.append(
            f"- [`#{tag}`](https://{owner}.github.io/curated/#tags={tag}) ({len(tag_map[tag])}): {linked}"
        )

    lines.extend(
        [
            "",
            "---",
            "",
            "## Adding or Updating Resources",
            "",
            "Resources live in [`data/resources.json`](data/resources.json) and follow [`schema/resources.schema.json`](schema/resources.schema.json).",
            "",
            "### Quick CLI (`scripts/curate.py`)",
            "",
            "```bash",
            "# Add a resource and rebuild the site + README",
            "python3 scripts/curate.py add \\",
            '  --url "https://lastmuseum.com/" \\',
            '  --title "The Last Museum" \\',
            '  --tags "art,museum,free" \\',
            '  --category "arts-culture" \\',
            '  --scopes "family,kids,personal" \\',
            '  --description "Search and browse over 6.3 million artworks across human history."',
            "",
            "# Validate data and regenerate site/ + README.md",
            "python3 scripts/build.py",
            "```",
            "",
        ]
    )

    return "\n".join(lines)


def build() -> int:
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    errors = validate_payload(data)
    if errors:
        for err in errors:
            print(f"ERROR: {err}", file=sys.stderr)
        return 1

    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    SITE_DIR.mkdir(parents=True, exist_ok=True)

    total = len(data["resources"])
    summary = f"Showing all {total} curated {'resource' if total == 1 else 'resources'}"
    updated_date = max(
        (r.get("added", "") for r in data["resources"]),
        default=datetime.now(timezone.utc).strftime("%Y-%m-%d"),
    )

    safe_json = (
        json.dumps(data, ensure_ascii=False, indent=2)
        .replace("&", "\\u0026")
        .replace("<", "\\u003c")
        .replace(">", "\\u003e")
    )

    rendered_html = (
        template.replace("{{TITLE}}", html.escape(data["meta"]["title"]))
        .replace("{{SUBTITLE}}", html.escape(data["meta"]["subtitle"]))
        .replace("{{OWNER}}", html.escape(data["meta"]["owner"]))
        .replace("{{INITIAL_SUMMARY}}", html.escape(summary))
        .replace("{{UPDATED_DATE}}", html.escape(updated_date))
        .replace("{{SSR_CONTENT}}", render_ssr_cards(data))
        .replace("{{DATA_JSON}}", safe_json)
    )

    (SITE_DIR / "index.html").write_text(rendered_html, encoding="utf-8")
    (SITE_DIR / "resources.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (SITE_DIR / "bookmarks.html").write_text(render_bookmarks_html(data), encoding="utf-8")
    (SITE_DIR / ".nojekyll").write_text("", encoding="utf-8")

    README_PATH.write_text(render_readme(data), encoding="utf-8")
    print(f"Built site/ and README.md ({total} resource(s)).")
    return 0


if __name__ == "__main__":
    raise SystemExit(build())
