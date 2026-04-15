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

## Task 2: Implement the Python build pipeline
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

## Task 3: Support both page types
Implement support for:
- **note pages** from Markdown
- **artifact pages** from artifact folders

Requirements:
- note pages render in the normal site layout
- artifact pages render in the normal site layout with the artifact shown in a sandboxed iframe
- support optional `description.md` above the artifact

---

## Task 4: Add simple search and sample content
Add a simple client-side search using generated static data.

Search should cover:
- page titles
- Markdown note content
- artifact titles
- artifact descriptions

Also add a small sample content set for:
- Spanish
- ROS2
- C++

---

## Task 5: Final cleanup
Finish by:
- keeping the code structure clean
- making local build/run steps obvious
- confirming the site works as a static GitHub Pages site
- updating the README if needed
