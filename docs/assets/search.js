const root = document.querySelector("[data-search-root]");
const script = document.currentScript;

if (root && script) {
  const input = root.querySelector("[data-search-input]");
  const results = root.querySelector("[data-search-results]");
  let pages = Array.isArray(window.__SEARCH_INDEX__) ? window.__SEARCH_INDEX__ : [];
  const siteRoot = new URL("../", script.src);

  const escapeHtml = (value) =>
    value
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#39;");

  const getSnippet = (content, query) => {
    if (!content) {
      return "Open this page.";
    }

    const lowerContent = content.toLowerCase();
    const index = lowerContent.indexOf(query);
    const start = index >= 0 ? Math.max(0, index - 55) : 0;
    const end = Math.min(content.length, start + 150);
    const prefix = start > 0 ? "..." : "";
    const suffix = end < content.length ? "..." : "";
    return `${prefix}${content.slice(start, end).trim()}${suffix}`;
  };

  const hideResults = () => {
    results.hidden = true;
    results.innerHTML = "";
  };

  const renderResults = (query) => {
    const trimmed = query.trim().toLowerCase();
    if (!trimmed) {
      hideResults();
      return;
    }

    const matches = pages
      .filter((page) => {
        const haystack = `${page.title} ${page.content}`.toLowerCase();
        return haystack.includes(trimmed);
      })
      .slice(0, 8);

    if (!matches.length) {
      results.innerHTML = '<div class="search-empty">No matching notes found.</div>';
      results.hidden = false;
      return;
    }

    results.innerHTML = matches
      .map((page) => {
        const snippet = getSnippet(page.content, trimmed);
        const href = new URL(page.url, siteRoot).href;
        return `
          <a class="search-result" href="${href}">
            <span class="search-result-title">${escapeHtml(page.title)}</span>
            <span class="search-result-snippet">${escapeHtml(snippet)}</span>
          </a>
        `;
      })
      .join("");
    results.hidden = false;
  };

  input.addEventListener("input", (event) => {
    renderResults(event.target.value);
  });

  input.addEventListener("focus", () => {
    if (input.value.trim()) {
      renderResults(input.value);
    }
  });

  document.addEventListener("click", (event) => {
    if (!root.contains(event.target)) {
      hideResults();
    }
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      hideResults();
      input.blur();
    }
  });
}
