from __future__ import annotations

import json
import re
import shutil
from dataclasses import dataclass
from html import escape
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).parent
CONTENT_DIR = ROOT / "content"
ASSETS_DIR = ROOT / "assets"
DOCS_DIR = ROOT / "docs"


@dataclass
class Page:
    title: str
    url: str
    output_path: Path
    breadcrumbs: List[Tuple[str, str]]
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


def build_breadcrumbs(parts: List[str], url: str, title: str) -> List[Tuple[str, str]]:
    crumbs: List[Tuple[str, str]] = [("Home", "index.html")]
    if not parts:
        crumbs.append((title, url))
        return crumbs

    current_parts: List[str] = []
    for part in parts:
        current_parts.append(part)
        crumbs.append((slug_to_title(part), "/".join(current_parts) + "/index.html"))

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


def render_nav(node: Dict[str, dict], depth: int = 0) -> str:
    items: List[str] = []

    for section, child in sorted(node["_children"].items()):
        label = slug_to_title(section)
        subsection = render_nav(child, depth + 1)
        pages_html = "".join(
            f'<li><a href="{escape(page.url)}">{escape(page.title)}</a></li>' for page in sorted(child["_pages"], key=lambda p: p.title.lower())
        )
        combined = ""
        if pages_html:
            combined += f"<ul>{pages_html}</ul>"
        if subsection:
            combined += subsection
        items.append(f"<li><span>{escape(label)}</span>{combined}</li>")

    root_pages = "".join(
        f'<li><a href="{escape(page.url)}">{escape(page.title)}</a></li>' for page in sorted(node["_pages"], key=lambda p: p.title.lower())
    )

    html = ""
    if root_pages:
        html += f"<ul>{root_pages}</ul>"
    if items:
        html += f"<ul>{''.join(items)}</ul>"
    return html


def render_breadcrumbs(crumbs: List[Tuple[str, str]]) -> str:
    out: List[str] = []
    for i, (label, href) in enumerate(crumbs):
        if i == len(crumbs) - 1:
            out.append(f'<span aria-current="page">{escape(label)}</span>')
        else:
            out.append(f'<a href="/{escape(href)}">{escape(label)}</a><span>/</span>')
    return "".join(out)


def page_shell(title: str, nav_html: str, breadcrumbs_html: str, body_html: str) -> str:
    return f"""<!DOCTYPE html>
<html lang=\"en\">
<head>
  <meta charset=\"UTF-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
  <title>{escape(title)} | Study Site</title>
  <link rel=\"stylesheet\" href=\"/assets/site.css\" />
</head>
<body>
  <header class=\"topbar\">
    <div class=\"brand\"><a href=\"/index.html\">Study Site</a></div>
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
    return page_shell("Home", nav_html, '<span aria-current="page">Home</span>', body)


def copy_assets() -> None:
    if not ASSETS_DIR.exists():
        return
    dest = DOCS_DIR / "assets"
    shutil.copytree(ASSETS_DIR, dest, dirs_exist_ok=True)


def build() -> None:
    pages = collect_pages()
    nav_tree = build_tree(pages)
    nav_html = render_nav(nav_tree)

    if DOCS_DIR.exists():
        shutil.rmtree(DOCS_DIR)
    DOCS_DIR.mkdir(parents=True, exist_ok=True)

    copy_assets()

    (DOCS_DIR / "index.html").write_text(render_home(nav_html), encoding="utf-8")

    for page in pages:
        page.output_path.parent.mkdir(parents=True, exist_ok=True)
        html = page_shell(page.title, nav_html, render_breadcrumbs(page.breadcrumbs), page.body_html)
        page.output_path.write_text(html, encoding="utf-8")

    print(f"Built {len(pages)} content pages into {DOCS_DIR}")


if __name__ == "__main__":
    build()
