# Tasks for Codex

Keep the implementation simple. Use plain HTML, CSS, JavaScript, and a Python build script only.

## Task 1: Create the static site shell ✅ Completed
Build the base site structure with:
- homepage
- top bar
- left sidebar
- main content area
- breadcrumbs
- clean, readable styling

Keep the layout docs-like and simple.

---

## Task 2: Implement the Python build pipeline ✅ Completed
Create `build.py` to:
- read content from `content/`
- convert Markdown note pages into static HTML pages
- read artifact metadata from artifact folders
- generate pages into `docs/`
- build a unified navigation tree
- generate breadcrumbs
- copy shared assets

Assume GitHub Pages will publish from `main` → `/docs`.


---

## Task 3: Add simple search and sample content ✅ Completed
Add a simple client-side search using generated static data.

Search should cover:
- Page titles
- Markdown note content

---
