from __future__ import annotations

import json
import posixpath
import re
import shutil
from dataclasses import dataclass
from html import escape
from pathlib import Path
from typing import Dict, List, Optional, Tuple

ROOT = Path(__file__).parent
CONTENT_DIR = ROOT / "content"
ASSETS_DIR = ROOT / "assets"
DOCS_DIR = ROOT / "docs"


@dataclass
class Page:
    title: str
    url: str
    output_path: Path
    breadcrumbs: List[Tuple[str, Optional[str]]]
    body_html: str
    kind: str


def slug_to_title(value: str) -> str:
    return value.replace("-", " ").replace("_", " ").strip().title()


def parse_frontmatter(text: str) -> Tuple[Dict[str, str], str]:
    lines = text.splitlines()
    if len(lines) < 3 or lines[0].strip() != "---":
        return {}, text

    metadata: Dict[str, str] = {}
    end_index = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end_index = i
            break
        if ":" in lines[i]:
            key, value = lines[i].split(":", 1)
            metadata[key.strip()] = value.strip()

    if end_index is None:
        return {}, text

    content = "\n".join(lines[end_index + 1 :]).lstrip("\n")
    return metadata, content


def markdown_to_html(markdown: str) -> str:
    html_parts: List[str] = []
    lines = markdown.splitlines()
    in_list = False
    in_code = False
    code_lines: List[str] = []

    def close_list() -> None:
        nonlocal in_list
        if in_list:
            html_parts.append("</ul>")
            in_list = False

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("```"):
            close_list()
            if in_code:
                html_parts.append(f"<pre><code>{escape(chr(10).join(code_lines))}</code></pre>")
                code_lines = []
                in_code = False
            else:
                in_code = True
            continue

        if in_code:
            code_lines.append(line)
            continue

        if not stripped:
            close_list()
            continue

        heading_match = re.match(r"^(#{1,6})\s+(.+)$", stripped)
        if heading_match:
            close_list()
            level = len(heading_match.group(1))
            content = escape(heading_match.group(2))
            html_parts.append(f"<h{level}>{content}</h{level}>")
            continue

        list_match = re.match(r"^[-*]\s+(.+)$", stripped)
        if list_match:
            if not in_list:
                html_parts.append("<ul>")
                in_list = True
            html_parts.append(f"<li>{escape(list_match.group(1))}</li>")
            continue

        close_list()
        html_parts.append(f"<p>{escape(stripped)}</p>")

    close_list()
    if in_code:
        html_parts.append(f"<pre><code>{escape(chr(10).join(code_lines))}</code></pre>")

    return "\n".join(html_parts)


def build_breadcrumbs(parts: List[str], url: str, title: str) -> List[Tuple[str, Optional[str]]]:
    crumbs: List[Tuple[str, Optional[str]]] = [("Home", "index.html")]
    if not parts:
        crumbs.append((title, url))
        return crumbs

    for part in parts:
        crumbs.append((slug_to_title(part), None))

    crumbs.append((title, url))
    return crumbs


def collect_pages() -> List[Page]:
    pages: List[Page] = []
    artifact_dirs = {path.parent for path in CONTENT_DIR.rglob("meta.json")}

    for md_path in CONTENT_DIR.rglob("*.md"):
        if any(parent in artifact_dirs for parent in md_path.parents):
            if md_path.name == "description.md":
                continue
            continue

        relative = md_path.relative_to(CONTENT_DIR)
        output_relative = relative.with_suffix(".html")
        url = output_relative.as_posix()

        raw = md_path.read_text(encoding="utf-8")
        frontmatter, markdown_body = parse_frontmatter(raw)
        title = frontmatter.get("title") or slug_to_title(md_path.stem)
        first_heading = re.search(r"^#\s+(.+)$", markdown_body, re.MULTILINE)
        if first_heading:
            title = first_heading.group(1).strip()

        parts = list(relative.parent.parts)
        breadcrumbs = build_breadcrumbs(parts, url, title)
        body_html = markdown_to_html(markdown_body)
        pages.append(
            Page(
                title=title,
                url=url,
                output_path=DOCS_DIR / output_relative,
                breadcrumbs=breadcrumbs,
                body_html=body_html,
                kind="note",
            )
        )

    for artifact_dir in sorted(artifact_dirs):
        relative = artifact_dir.relative_to(CONTENT_DIR)
        meta_path = artifact_dir / "meta.json"
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        title = meta.get("title") or slug_to_title(artifact_dir.name)

        output_relative = relative / "index.html"
        url = output_relative.as_posix()
        parts = list(relative.parts[:-1])
        breadcrumbs = build_breadcrumbs(parts, url, title)

        meta_html = escape(json.dumps(meta, indent=2))
        body_html = "\n".join(
            [
                "<h1>Artifact</h1>",
                f"<h2>{escape(title)}</h2>",
                "<p>Artifact metadata was discovered by the build pipeline.</p>",
                f"<pre><code>{meta_html}</code></pre>",
            ]
        )

        pages.append(
            Page(
                title=title,
                url=url,
                output_path=DOCS_DIR / output_relative,
                breadcrumbs=breadcrumbs,
                body_html=body_html,
                kind="artifact",
            )
        )

    return sorted(pages, key=lambda page: page.url)



def build_tree(pages: List[Page]) -> Dict[str, dict]:
    root = {"_pages": [], "_children": {}}
    for page in pages:
        parts = Path(page.url).parts[:-1]
        node = root
        for part in parts:
            node = node["_children"].setdefault(part, {"_pages": [], "_children": {}})
        node["_pages"].append(page)
    return root


def relative_href(from_url: str, to_url: str) -> str:
    base_dir = posixpath.dirname(from_url) or "."
    return posixpath.relpath(to_url, base_dir)


def render_nav(node: Dict[str, dict], current_url: str, current_path: str = "") -> str:
    items: List[str] = []

    for page in sorted(node["_pages"], key=lambda p: p.title.lower()):
        href = relative_href(current_url, page.url)
        items.append(f'<li><a href="{escape(href)}">{escape(page.title)}</a></li>')

    for section, child in sorted(node["_children"].items()):
        label = slug_to_title(section)
        section_path = f"{current_path}/{section}" if current_path else section
        subsection = render_nav(child, current_url, section_path)
        is_open = current_url.startswith(f"{section_path}/") or current_url == "index.html"
        open_attr = " open" if is_open else ""
        items.append(
            f'<li><details class="nav-section"{open_attr}>'
            f"<summary>{escape(label)}</summary>"
            f"{subsection}</details></li>"
        )

    if not items:
        return ""
    return f"<ul>{''.join(items)}</ul>"


def render_breadcrumbs(crumbs: List[Tuple[str, Optional[str]]], current_url: str) -> str:
    out: List[str] = []
    for i, (label, href) in enumerate(crumbs):
        if i == len(crumbs) - 1:
            out.append(f'<span aria-current="page">{escape(label)}</span>')
        elif href:
            relative = relative_href(current_url, href)
            out.append(f'<a href="{escape(relative)}">{escape(label)}</a><span>/</span>')
        else:
            out.append(f"<span>{escape(label)}</span><span>/</span>")
    return "".join(out)


def page_shell(title: str, current_url: str, nav_html: str, breadcrumbs_html: str, body_html: str) -> str:
    stylesheet_href = relative_href(current_url, "assets/site.css")
    home_href = relative_href(current_url, "index.html")
    return f"""<!DOCTYPE html>
<html lang=\"en\">
<head>
  <meta charset=\"UTF-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
  <title>{escape(title)} | Study Site</title>
  <link rel=\"stylesheet\" href=\"{escape(stylesheet_href)}\" />
</head>
<body>
  <header class=\"topbar\">
    <div class=\"brand\"><a href=\"{escape(home_href)}\">Study Site</a></div>
  </header>
  <div class=\"layout\">
    <aside class=\"sidebar\" aria-label=\"Sidebar\">
      <h2>Sections</h2>
      {nav_html}
    </aside>
    <main class=\"content\" id=\"main-content\">
      <nav class=\"breadcrumbs\" aria-label=\"Breadcrumbs\">{breadcrumbs_html}</nav>
      {body_html}
    </main>
  </div>
</body>
</html>
"""


def render_home(nav_html: str) -> str:
    body = """
      <h1>Welcome to your study site</h1>
      <p>Build complete. Add note pages and artifact folders inside <code>content/</code>.</p>
    """
    return page_shell("Home", "index.html", nav_html, '<span aria-current="page">Home</span>', body)


def copy_assets() -> None:
    if not ASSETS_DIR.exists():
        return
    dest = DOCS_DIR / "assets"
    shutil.copytree(ASSETS_DIR, dest, dirs_exist_ok=True)


def build() -> None:
    pages = collect_pages()
    nav_tree = build_tree(pages)

    if DOCS_DIR.exists():
        shutil.rmtree(DOCS_DIR)
    DOCS_DIR.mkdir(parents=True, exist_ok=True)

    copy_assets()

    home_nav_html = render_nav(nav_tree, "index.html")
    (DOCS_DIR / "index.html").write_text(render_home(home_nav_html), encoding="utf-8")

    for page in pages:
        page.output_path.parent.mkdir(parents=True, exist_ok=True)
        nav_html = render_nav(nav_tree, page.url)
        breadcrumbs_html = render_breadcrumbs(page.breadcrumbs, page.url)
        html = page_shell(page.title, page.url, nav_html, breadcrumbs_html, page.body_html)
        page.output_path.write_text(html, encoding="utf-8")

    print(f"Built {len(pages)} content pages into {DOCS_DIR}")


if __name__ == "__main__":
    build()
