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
   - May include relative image links such as `![Alt text](images/example.png)`
   - May embed a Claude artifact with:
     - `{{ artifact "artifact-folder/artifact-file.html" }}`

2. **Artifact page**
   - A self-contained HTML file stored in a folder next to the note that references it
   - Used for Claude-generated interactive content
   - Embedded inside note pages as a sandboxed iframe

## Authoring workflow
Content is created manually in VS Code.

- Create/edit Markdown files for notes
- Add images in a folder next to the note, then reference them with a relative Markdown image path
- Add Claude artifacts in a folder next to the note, keeping the downloaded `.html` file intact
- Embed an artifact in a note with:
  - `{{ artifact "artifact-folder/artifact-file.html" }}`
- Run the Python build script locally
- Push the generated site to GitHub

There is no in-browser editor.

### Example content layout
```text
content/
  computer-networking/
    udp/
      udp-broadcast.md
      images/
        udp-header.png
      udp-broadcast-artifact/
        udp_broadcast_subnet_explainer.html
```

### Example note content
```md
# UDP Broadcast

![UDP header](images/udp-header.png)

Here is the interactive artifact:

{{ artifact "udp-broadcast-artifact/udp_broadcast_subnet_explainer.html" }}
```

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
- copy note-adjacent images and artifact files
- generate simple search data

## Rendering rules
- Note pages render as normal site pages
- Artifact embeds render inside a sandboxed iframe
- Artifacts stay isolated from the main site layout

## Goal
Keep the project simple, static, and easy to maintain.
