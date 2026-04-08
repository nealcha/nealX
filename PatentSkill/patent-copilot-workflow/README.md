# Patent Copilot Workflow

`Patent Copilot Workflow` is a local-first `skill + workflow` package for utility-model patent drafting.

It is designed for one simple operating mode:

1. Put reference patent PDFs into `workspaces/default/intake/samples/`.
2. Optionally put research summaries into `workspaces/default/intake/research-notes/`.
3. Run `sh ./scripts/prepare_patent_workspace.sh`.
4. Paste the generated prompt file into the model.
5. Let the model choose one direction by itself and complete the reviewed patent package.

## What This Project Contains

- `skills/patent-copilot/`: the reusable Codex skill.
- `scripts/prepare_patent_workspace.sh`: one-command preflight script.
- `workspaces/default/`: the starter local workspace.

## Core Workflow

1. Intake local materials.
2. Extract writing patterns from the PDF corpus.
3. Let AI choose one feasible utility-model direction.
4. Draft the patent package.
5. Review and revise the draft.
6. Optionally generate a domain accelerator page for non-specialist review.

## Default Outputs

- `output/10-guides/writing-guide.md`
- `output/15-selected-direction/selected-direction.md`
- `output/30-patent-package/disclosure-draft.md`
- `output/30-patent-package/figure-prompts.md`
- `output/30-patent-package/review-report.md`
- `output/30-patent-package/disclosure-reviewed.md`
- `output/40-domain-accelerator/` when needed

## Boundaries

- Prefer user-provided local PDFs over live web scraping.
- Treat `research-notes/` as optional constraints, not as a hard dependency.
- Do not rely on recovered chats or hidden historical materials.
- Treat drafting plus review as one bundled completion standard.
- Treat final filing, novelty, legal risk, and figure sufficiency as items that still require human confirmation.

See [USAGE.md](USAGE.md) for the simplest operating steps.
