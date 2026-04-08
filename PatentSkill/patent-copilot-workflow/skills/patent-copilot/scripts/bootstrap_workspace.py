from __future__ import annotations

import argparse
import json
from pathlib import Path

DIRS = [
    "intake/samples",
    "intake/research-notes",
    "intake/notes",
    "temp/extracted-text",
    "output/10-guides",
    "output/15-selected-direction",
    "output/30-patent-package",
    "output/40-domain-accelerator",
]

INPUT_BRIEF = """# Input Brief

## Current Goal

- 

## Available Materials

- Local sample patent PDFs:
- Online research notes or search summaries:

## Expected Flow

- Read the PDFs and research notes first.
- Choose one innovative but corpus-consistent direction by AI.
- Continue directly to a full patent package.

## Expected Outputs

- Writing guide
- Selected direction
- Patent package (draft + figure prompts + review report + reviewed draft)
- Domain accelerator page if needed

## Notes

- 
"""

RESEARCH_NOTES = """# Research Notes

## Search Themes

- 

## Confirmed Directions

- 

## Links or Summaries

- 

## Questions For AI To Judge

- 
"""

SELECTED_DIRECTION = """# Selected Direction

## Final Title

- 

## Target Problem

- 

## Core Structural Scheme

- 

## Why AI Chose This Direction

- 

## Drafting Assumptions

- 

## Missing Information

- 
"""


def write_text(path: Path, content: str, force: bool) -> None:
    if path.exists() and not force:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a standard local patent workspace.")
    parser.add_argument("--root", required=True, help="Workspace root directory")
    parser.add_argument("--name", default="patent-task", help="Logical task name")
    parser.add_argument("--force", action="store_true", help="Overwrite starter files if they already exist")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    for relative in DIRS:
        (root / relative).mkdir(parents=True, exist_ok=True)

    write_text(root / "intake/notes/input-brief.md", INPUT_BRIEF, args.force)
    write_text(root / "intake/research-notes/online-research.md", RESEARCH_NOTES, args.force)
    write_text(root / "output/15-selected-direction/selected-direction.md", SELECTED_DIRECTION, args.force)

    manifest_path = root / "manifest.json"
    if not manifest_path.exists() or args.force:
        manifest = {
            "task_name": args.name,
            "workspace_root": str(root),
            "expected_outputs": [
                "writing-guide",
                "selected-direction",
                "patent-package",
                "domain-accelerator-optional",
            ],
            "next_steps": [
                "Place sample PDFs in intake/samples.",
                "Place online research notes or downloaded comparison materials in intake/research-notes.",
                "Describe any scope constraint in intake/notes/input-brief.md.",
                "Run build_manifest.py after import.",
            ],
        }
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"workspace ready: {root}")


if __name__ == "__main__":
    main()
