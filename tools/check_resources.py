#!/usr/bin/env python3
"""Check repository links, configuration syntax and public resource hygiene."""
from __future__ import annotations

import argparse
import json
import re
import sys
import tomllib
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
IGNORED = {".git", "__pycache__", ".venv", "node_modules"}
LINK = re.compile(r"!?\[[^\]\n]*\]\((<[^>\n]+>|[^)\n]+)\)")
FENCE = re.compile(r"^\s*([`~])\1{2,}")
PRIVATE_PATH = re.compile(r"(?i)\b[A-Z]:[\\/](?:Users|Dev|brenn)[\\/]")
SECRET = re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{30,}|sk-[A-Za-z0-9]{30,})\b")


class AssetLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.targets = []

    def handle_starttag(self, tag, attrs):
        if tag not in {"img", "source"}:
            return
        for key, value in attrs:
            if key == "src" and value:
                self.targets.append(value)
            elif key == "srcset" and value:
                self.targets.extend(part.strip().split()[0] for part in value.split(",") if part.strip())


def prose(text: str) -> str:
    """Skip fenced blocks; links in inline prose remain available."""
    result = []
    marker = None
    for line in text.splitlines():
        fence = FENCE.match(line)
        if fence:
            if marker is None:
                marker = fence.group(1)
            elif fence.group(1) == marker:
                marker = None
            result.append("")
        elif marker is None:
            result.append(line)
        else:
            result.append("")
    return "\n".join(result)


def anchors(text: str) -> set[str]:
    found = set()
    counts: dict[str, int] = {}
    for line in prose(text).splitlines():
        heading = re.match(r"^#{1,6}\s+(.+?)\s*#*\s*$", line)
        if heading:
            title = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", heading.group(1))
            slug = re.sub(r"[^\w\s-]", "", title.lower()).replace(" ", "-")
            count = counts.get(slug, 0)
            counts[slug] = count + 1
            found.add(f"{slug}-{count}" if count else slug)
    found.update(re.findall(r'<(?:a|h[1-6])\s+[^>]*id=["\']([^"\']+)', text))
    return found


def check(root: Path) -> dict:
    root = root.resolve()
    errors = []
    counts = {"markdown": 0, "links": 0, "json": 0, "toml": 0, "roles": 0}
    files = sorted(
        path for path in root.rglob("*")
        if path.is_file() and not any(p in IGNORED for p in path.relative_to(root).parts)
    )
    for path in files:
        rel = path.relative_to(root).as_posix()
        if path.suffix not in {".md", ".json", ".toml"}:
            continue
        if path.is_symlink() or not path.resolve().is_relative_to(root):
            errors.append(f"{rel}: resource leaves repository")
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            errors.append(f"{rel}: unreadable ({type(exc).__name__})")
            continue
        if PRIVATE_PATH.search(text) or SECRET.search(text):
            errors.append(f"{rel}: private local path or credential-shaped text")
        try:
            if path.suffix == ".json":
                counts["json"] += 1
                json.loads(text)
            elif path.suffix == ".toml":
                counts["toml"] += 1
                config = tomllib.loads(text)
                if "setup/codex/" in rel and not path.name.endswith(".config.toml"):
                    for field in ("name", "description", "developer_instructions"):
                        if not isinstance(config.get(field), str) or not config[field].strip():
                            errors.append(f"{rel}: missing agent field {field}")
                    counts["roles"] += 1
        except (json.JSONDecodeError, tomllib.TOMLDecodeError) as exc:
            errors.append(f"{rel}: invalid syntax ({type(exc).__name__})")
        if path.suffix != ".md":
            continue
        counts["markdown"] += 1
        if rel.startswith(("setup/claude-code/agents/", "setup/cursor/")):
            if path.suffix == ".md":
                if not text.startswith("---\n") or "\n---\n" not in text[4:]:
                    errors.append(f"{rel}: missing role frontmatter")
                else:
                    header = text.split("---", 2)[1]
                    for field in ("name", "description", "model"):
                        if not re.search(rf"^{field}:\s*\S", header, re.M):
                            errors.append(f"{rel}: missing role field {field}")
                    counts["roles"] += 1
        visible = prose(text)
        html = AssetLinks()
        html.feed(visible)
        targets = [match.group(1) for match in LINK.finditer(visible)] + html.targets
        for target in targets:
            target = target.strip()
            if target.startswith("<"):
                target = target[1:-1]
            else:
                target = re.split(r'\s+["\']', target, maxsplit=1)[0]
            url = urlsplit(target)
            if url.scheme in {"https", "http", "mailto"}:
                continue
            if url.scheme or url.netloc or url.path.startswith(("/", "\\")):
                errors.append(f"{rel}: unsupported local target {target}")
                continue
            counts["links"] += 1
            dest = (path.parent / unquote(url.path)).resolve() if url.path else path
            if not dest.is_relative_to(root):
                errors.append(f"{rel}: link leaves repository: {target}")
            elif not dest.exists():
                errors.append(f"{rel}: missing target: {target}")
            elif url.fragment and dest.suffix == ".md":
                if unquote(url.fragment) not in anchors(dest.read_text(encoding="utf-8")):
                    errors.append(f"{rel}: missing heading: {target}")
    return {"passed": not errors, "checked": counts, "errors": errors}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    if not args.root.is_dir():
        parser.error("root must be an existing directory")
    result = check(args.root)
    print(json.dumps(result, indent=2))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
