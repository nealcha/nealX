# Data Source Policy

## Default Stance

Use a local-first workflow.

Prefer:

1. User-downloaded patent PDFs
2. Local Markdown or Word-export text
3. Local research notes, saved comparisons, or exported search snippets
4. Local figures or screenshots explicitly provided by the user

## CNIPA and Similar Sources

Do not assume the patent search system can be accessed or automated reliably.

Treat CNIPA full-text acquisition as one of these modes:

1. Manual download by the user
2. Browser-assisted import after the user logs in
3. Direct local handoff of already downloaded files

Avoid making unattended scraping a default dependency for the skill.

If online research is needed, prefer saving the resulting notes, summaries, and downloaded files into `intake/research-notes/` before the downstream patent workflow continues.

## Product Design Implication

1. Never block the workflow on automated CNIPA scraping.
2. Base direction generation on local sample PDFs plus optional local research notes.
3. Design import steps around local directories and manifests.
4. If online research is necessary, isolate it as a fallback path and convert it into local notes first.
5. Keep the downstream workflow identical whether files came from local download or manual upload.
