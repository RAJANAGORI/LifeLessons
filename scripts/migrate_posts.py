#!/usr/bin/env python3
"""Move root-level Markdown essays into content/posts/ with Hugo front matter."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POSTS_DIR = ROOT / "content" / "posts"
DRAFT_NAMES = {"Test.md"}
SKIP_NAMES = {"README.md"}
SKIP_DIRS = {"content", "themes", "scripts", "public", "resources", "static", ".git"}


def title_from_body(lines: list[str]) -> str | None:
    for line in lines:
        m = re.match(r"^#\s+(.+?)\s*$", line.strip())
        if m:
            return m.group(1).strip()
    return None


def strip_leading_h1(lines: list[str]) -> list[str]:
    out: list[str] = []
    removed = False
    for line in lines:
        if not removed and re.match(r"^#\s+.+$", line.strip()):
            removed = True
            continue
        out.append(line)
    return out


def normalize_body(text: str) -> str:
    # Notion export: trailing double spaces = hard breaks; keep as-is for poetry.
    lines = text.splitlines()
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    return "\n".join(lines) + "\n"


def migrate_file(path: Path) -> None:
    raw = path.read_text(encoding="utf-8")
    lines = raw.splitlines(keepends=True)
    title = title_from_body([l.rstrip("\n") for l in lines]) or path.stem
    body_lines = strip_leading_h1([l.rstrip("\n") for l in lines])
    body = normalize_body("\n".join(body_lines))

    mtime = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
    date_str = mtime.strftime("%Y-%m-%dT%H:%M:%S+00:00")
    draft = "true" if path.name in DRAFT_NAMES else "false"

    # Web-friendly attachment paths (served from static/)
    body = body.replace("Attachments/", "/Attachments/")

    front = (
        "---\n"
        f"title: {json.dumps(title, ensure_ascii=False)}\n"
        f"date: {date_str}\n"
        f"draft: {draft}\n"
        "---\n\n"
    )

    dest = POSTS_DIR / path.name
    dest.write_text(front + body, encoding="utf-8")
    path.unlink()
    print(f"  migrated: {path.name} -> content/posts/{path.name}")


def main() -> None:
    POSTS_DIR.mkdir(parents=True, exist_ok=True)
    md_files = sorted(p for p in ROOT.glob("*.md") if p.name not in SKIP_NAMES)
    if not md_files:
        print("No root-level .md files to migrate.")
        return
    print(f"Migrating {len(md_files)} posts...")
    for md in md_files:
        migrate_file(md)
    print("Done.")


if __name__ == "__main__":
    main()
