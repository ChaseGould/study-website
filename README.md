# Study Site

A simple personal study website for storing thoughtfully written study material and interactive Claude-generated artifacts.

## Goal

Build a lightweight documentation-style site with:

- a homepage
- top-level categories:
  - Spanish
  - ROS2
  - C++
- up to 3 levels of content depth
- sidebar navigation
- breadcrumbs
- search
- Markdown-first content
- support for Claude-generated HTML/CSS/JS artifacts

This site is intended for personal use and does **not** need a full in-browser editor or CMS. Content will be added manually in the backend by creating files in the repository.

---

## Key decisions

### 1. Keep the content hierarchy simple
We are capping the practical page depth at **3 levels**.

Example:

- ROS2
  - QoS
    - Reliable vs Best Effort

This keeps navigation clean and avoids burying notes too deeply.

---

### 2. Use a docs-style layout
Recommended layout:

- **Top bar**
  - site title
  - search
  - breadcrumbs
- **Left sidebar**
  - expandable navigation tree
- **Main content area**
  - rendered study page or artifact page

This structure fits hierarchical study material well and scales nicely as more pages are added.

---

### 3. Use Markdown for normal study pages
Normal study content should be written in Markdown.

Examples:

- concept explanations
- study notes
- cheat sheets
- summaries

Markdown keeps the project easy to maintain and version control.

---

### 4. Support Claude artifacts as a separate page type
Claude-generated interactive content should be supported, but **not** forced into Markdown.

We will support two page types:

- `note` → Markdown page
- `artifact` → HTML/CSS/JS artifact page

Artifacts should live in their own folders and render separately from normal note pages.

---

### 5. Store content as files in the repo
This project will use a simple file-based content model instead of a database or CMS.

That means content is added manually in the backend by creating files and folders.

This is a good fit because:

- the site is for personal use
- content will be added thoughtfully, not rapidly
- version control is useful
- implementation stays simple

---

### 6. Use separate files for artifacts
Artifact pages should be stored as folders containing metadata plus the artifact files.

Recommended structure:

```text
content/
  ros2/
    qos/
      reliable-vs-best-effort.md
      qos-compatibility-demo/
        meta.json
        description.md
        index.html
        style.css
        script.js
```

This is preferred because Claude artifacts often naturally come as HTML, CSS, and JS.

---

### 7. Render artifacts in a sandboxed iframe
Artifacts should be rendered inside an **iframe** rather than injected directly into the main app.

Why:

- prevents CSS leakage into the site
- prevents JS from breaking the main site UI
- makes artifact integration safer and cleaner
- allows Claude outputs to remain mostly unchanged

---

## Proposed content model

### Note page
Markdown file with frontmatter:

```md
---
title: Reliable vs Best Effort
slug: reliable-vs-best-effort
parent: qos
order: 1
type: note
---

# Reliable vs Best Effort

Page content here.
```

### Artifact page
Folder with `meta.json` and artifact files:

```json
{
  "title": "QoS Compatibility Demo",
  "slug": "qos-compatibility-demo",
  "parent": "qos",
  "order": 2,
  "type": "artifact"
}
```

Optional `description.md` can be included to provide context before the artifact preview.

---

## Recommended folder structure

```text
content/
  spanish/
    grammar/
      ser-vs-estar.md
  ros2/
    qos/
      reliable-vs-best-effort.md
      qos-compatibility-demo/
        meta.json
        description.md
        index.html
        style.css
        script.js
  cpp/
    memory/
      smart-pointers.md
```

---

## Routing and navigation expectations

The site should support:

- a homepage
- category pages
- subpages
- sub-subpages
- breadcrumbs
- active page highlighting in the sidebar
- collapsed/expandable tree navigation
- search across note content and metadata

The navigation should treat both note pages and artifact pages as normal pages in the same hierarchy.

---

## Search expectations

Search should index at least:

- page titles
- Markdown note content
- tags if added later
- artifact titles
- artifact descriptions

Search does **not** need to deeply index artifact JS or CSS.

---

## Suggested implementation priorities

### v1 priorities
- file-based content loading
- sidebar navigation
- breadcrumbs
- Markdown rendering
- artifact rendering in iframe
- basic search

### Not needed for v1
- database
- CMS/admin panel
- live in-browser editing
- auth
- complex tagging systems
- unlimited nesting

---

## Suggested tech direction

This project should stay simple.

A lightweight frontend approach is preferred. Good options include:

- React-based app
- or simple static-site-style rendering with a lightweight framework

The exact stack can be chosen during implementation, but the architecture should remain:

- file-based
- Markdown-first
- artifact-friendly
- simple to maintain

---

## Summary

This project is a small personal study site with a docs-style layout and a simple file-based content model.

Core principles:

- keep hierarchy shallow
- use Markdown for notes
- support artifacts as a separate page type
- store everything as files in the repo
- isolate artifacts in sandboxed iframes
- keep implementation simple
