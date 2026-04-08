---
name: patent-copilot
description: Local-first utility-model patent workflow for turning sample patent PDFs and research summaries into one AI-selected patent direction plus a reviewed patent package. Use when Codex needs to read local patent corpora, extract writing patterns, choose an innovative but corpus-consistent utility-model direction on its own, draft a disclosure with figure prompts, optionally generate an unfamiliar-domain accelerator page, and complete bundled consistency review. Prefer user-downloaded CNIPA files or browser-assisted import over unattended scraping.
---

# Patent Copilot

Use this skill to turn local patent-related materials into a reusable patent working package. Keep the workflow local-first, use sample PDFs plus optional research summaries as the default input, let AI choose one direction before drafting, and treat drafting plus review as one completion step.

## Workflow

1. Initialize a workspace with `scripts/bootstrap_workspace.py` if `<workspace>/intake/` is missing.
2. Build or refresh the inventory with `scripts/build_manifest.py`.
3. Extract local sample PDF text with `scripts/extract_pdf_text.py` before asking for corpus analysis.
4. Read `references/data-source-policy.md` before planning any network-based import or CNIPA interaction.
5. Read `references/workflow.md` for the full sequence, directory layout, and output expectations.
6. Read `references/prompt-patterns.md` when you need reusable prompt structures for research, AI direction selection, patent package generation, or domain accelerator tasks.
7. Read `references/review-checklist.md` before finalizing the reviewed patent package.

## Default Output Order

1. Writing guide
2. Selected-direction note
3. Patent package
4. Domain accelerator page when useful

Treat the patent package as incomplete unless it includes:

1. Disclosure draft
2. Figure prompts
3. Review report
4. Revised disclosure after the review pass

## Working Rules

1. Prefer local files over web sources.
2. Use `intake/research-notes/` for manually collected online findings, comparison notes, or downloaded reference summaries.
3. Prefer browser-assisted or manual CNIPA downloads over unattended scraping.
4. Use `intake/samples/` as the required input and `intake/research-notes/` as the optional constraint input. Do not depend on recovered chats or hidden historical materials.
5. Choose one direction yourself after research and continue directly to drafting.
6. Treat the user's research notes as direction constraints, not necessarily as the final title.
7. Treat drafting and review as one bundled deliverable.
8. Generate a domain accelerator page whenever the domain is unfamiliar or the user needs non-specialist review support.
9. Mark final legal or technical judgments as requiring human confirmation.
10. Reuse templates from `assets/` instead of inventing new structures each time.

## Bundled Resources

- `scripts/bootstrap_workspace.py`: Create a standard local workspace for a new patent task.
- `scripts/build_manifest.py`: Inventory and classify local materials into a manifest.
- `scripts/extract_pdf_text.py`: Extract plain text from local PDF files into page-marked text files.
- `references/workflow.md`: Core operating sequence and output expectations.
- `references/data-source-policy.md`: Data-source boundaries and CNIPA handling rules.
- `references/prompt-patterns.md`: Reusable prompt patterns for research, AI direction selection, patent package generation, and domain acceleration.
- `references/review-checklist.md`: Review checklist for topic scope, disclosure completeness, and figure consistency.
- `assets/*.md`: Output templates for intake, direction decision, disclosure, review, and domain accelerator materials.
