# Tasks for Codex

Implement the study site in a small number of clear steps. Keep the implementation simple and avoid overengineering.

## Task 1: Scaffold the app shell and layout
Create the initial site structure with:

- top bar
- left sidebar
- main content area
- homepage
- routes/pages for:
  - Spanish
  - ROS2
  - C++

Requirements:

- docs-style layout
- left sidebar should support expandable nested navigation
- breadcrumbs should appear in the top area
- sidebar should highlight the active page
- design should be clean and readable, not flashy

Do not add authentication, CMS features, or database support.

---

## Task 2: Implement file-based content loading
Build a file-based content system that supports two page types:

- `note` → Markdown file with frontmatter
- `artifact` → folder containing `meta.json` and artifact files

Requirements:

- support up to 3 levels of hierarchy
- load content from a `content/` directory
- parse Markdown note metadata
- parse artifact metadata
- build a unified navigation tree from both content types
- provide a clean way to resolve parent/child relationships
- include a small sample content set for Spanish, ROS2, and C++

---

## Task 3: Render note pages and artifact pages
Implement page rendering for both page types.

### Note page requirements
- render Markdown content in the main content area
- show page title and breadcrumbs
- style content for readability

### Artifact page requirements
- render artifact inside a sandboxed iframe
- support artifact folder files such as:
  - `index.html`
  - `style.css`
  - `script.js`
- optionally render `description.md` above the iframe if present
- keep artifact CSS/JS isolated from the main site

---

## Task 4: Add search and polish navigation
Implement simple search across:

- page titles
- Markdown content
- artifact titles
- artifact descriptions

Requirements:

- search input in the top bar
- results should navigate to matching pages
- keep the implementation simple
- preserve sidebar, breadcrumbs, and active-page behavior

Also add small usability improvements:

- responsive sidebar behavior
- clean empty/home states
- previous/next page links if easy to add without much complexity

---

## Task 5: Final cleanup and docs
Before finishing:

- clean up the code structure
- add comments where useful
- make sure sample content demonstrates both notes and artifacts
- ensure the project is easy to run locally

Update the project README if needed with:

- how content is stored
- how to add a Markdown page
- how to add an artifact page
- how to run the site locally
