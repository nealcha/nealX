# Workflow

## Core Rule

Run the workflow in this order unless the user explicitly narrows the task:

1. Intake
2. Research
3. AI Direction Decision
4. Patent Package
5. Domain Accelerator

## 1. Intake

`intake/` always lives directly under the current workspace root. If the workspace is `workspaces/demo`, the intake folder is `workspaces/demo/intake/`.

Use this layout:

```text
<workspace>/
  intake/
    samples/
    research-notes/
    notes/
  temp/
    extracted-text/
  output/
    10-guides/
    15-selected-direction/
    30-patent-package/
    40-domain-accelerator/
```

Check whether the workspace contains:

1. Sample patent PDFs
2. Saved online research notes or manually downloaded comparison materials
3. A brief from the user

If the workspace is not structured yet, run `scripts/bootstrap_workspace.py`.

If a manifest is missing or stale, run `scripts/build_manifest.py`.

Use the intake folders like this:

1. `intake/samples/`: Local sample patents, including user-downloaded CNIPA full-text PDFs.
2. `intake/research-notes/`: Search summaries, copied links, manual comparison notes, or exported research snippets.
3. `intake/notes/`: Input brief and other task-specific notes.

## 2. Research

Goal:

1. Extract patterns from local sample patents and research notes.
2. Identify section order, wording style, numbering habits, structural scope, and recurring risk points.
3. Produce a reusable writing guide for the current domain.

Write the main guide to `output/10-guides/writing-guide.md`.

## 3. AI Direction Decision

Goal:

1. Combine the PDF corpus direction with the user's online-research notes.
2. Choose one feasible utility-model topic that is both innovative and still supported by the corpus.
3. Record why that direction was chosen and what assumptions will drive drafting.

The selected-direction note should include:

1. Final title
2. Intended problem
3. Core structural scheme
4. Why it fits the sample PDFs and research findings
5. Likely figure set or key numbered components
6. Drafting assumptions
7. Missing information and risk points

Write the result to `output/15-selected-direction/selected-direction.md`.

## 4. Patent Package

Goal:

1. Draft the disclosure from the AI-selected direction.
2. Generate figure prompts for the required drawings.
3. Run a bundled review on completeness, figure-text consistency, numbering stability, and open questions.
4. Revise the draft once based on the review pass before finalizing.

Use `output/30-patent-package/` for the main package. Default files:

1. `disclosure-draft.md`
2. `figure-prompts.md`
3. `review-report.md`
4. `disclosure-reviewed.md`

Treat the patent package as the natural completion standard for one patent task. A draft without review is not complete.

## 5. Domain Accelerator

Treat this as optional by default. Generate it when the domain is unfamiliar to the likely reader or the user explicitly wants a non-specialist explanation page.

Goal:

1. Explain the structure in plain language.
2. Build a visual or narrative bridge between raw patent text and human understanding.
3. Support later manual review.

Write the main result to `output/40-domain-accelerator/`.
