# Study Site

A simple personal study website for storing thoughtful study material and Claude-generated artifacts.

## Stack
- Plain **HTML, CSS, and JavaScript**
- **Python** build script
- **GitHub Pages** hosting
- Content authored manually in **VS Code**

## Scope
- Homepage
- Top-level categories:
  - Spanish
  - ROS2
  - C++
- Up to **3 levels** of page depth
- Left sidebar navigation
- Breadcrumbs
- Search
- Markdown note pages
- Claude artifact pages

## Content model
Two page types:

1. **Note page**
   - Markdown file with frontmatter
   - Used for study notes and explanations

2. **Artifact page**
   - Folder containing:
     - `meta.json`
     - optional `description.md`
     - `index.html`
     - `style.css`
     - `script.js`
   - Used for Claude-generated interactive content

## Authoring workflow
Content is created manually in VS Code.

- Create/edit Markdown files for notes
- Add artifact folders manually
- Run the Python build script locally
- Push the generated site to GitHub

There is no in-browser editor.

## GitHub Pages architecture
This site should be built as a **static site**.

- Source content lives in the repo
- `build.py` generates the final site into `docs/`
- GitHub Pages publishes from:
  - branch: `main`
  - folder: `/docs`

## Recommended structure
```text
content/
  spanish/
  ros2/
  cpp/

templates/
assets/
build.py
docs/
```

## Build responsibilities
`build.py` should:
- scan `content/`
- convert Markdown to HTML
- build sidebar and breadcrumbs
- generate static pages
- copy assets
- copy artifact files
- generate simple search data

## Rendering rules
- Note pages render as normal site pages
- Artifact pages render inside a sandboxed iframe
- Artifacts stay isolated from the main site layout

## Goal
Keep the project simple, static, and easy to maintain.
