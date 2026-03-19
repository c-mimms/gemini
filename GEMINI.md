
## General UI & Layout
- **Defensive CSS:** When designing shared stylesheets for dynamically generated HTML (like markdown-to-HTML tasks), apply max-width and layout constraints defensively on inner elements (e.g. `main` or `.body`). Do not rely solely on the AI remembering to inject a master wrapper `.container`.
- **Responsive Tables:** Always wrap `<table>` elements in a div with `overflow-x: auto; max-width: 100%; -webkit-overflow-scrolling: touch;` to prevent them from causing horizontal overflow on mobile viewports.

## Agent Prompting & Content Generation
- **Separation of Concerns (Content vs Layout):** When prompting an LLM to generate pages for a static site, don't make the LLM responsible for the macro-layout (like centering, `max-width` wrappers, sidebars). Have the LLM focus on generating the semantic content (`<main>`, `<h2>`, `<p>`), and use the build script (e.g. `build_news.py`) to wrap that content in the structural layout containers.
- **Component-Driven Prompts:** Providing a highly prescriptive, line-by-line HTML template in a prompt restricts the LLM's creativity and leads to repetitive outputs. Instead, provide a "Tool Inventory" of available CSS classes (e.g., `.stat-callout`, `.verdict`) and let the agent compose the page naturally based on the story it wants to tell.
