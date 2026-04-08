from __future__ import annotations

import argparse
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


EMPTY_TEMPLATE_LINES = {
    '-',
    '- Search Themes:',
    '- Confirmed Directions:',
    '- Links or Summaries:',
    '- Questions For AI To Judge:',
}


def has_user_content(path: Path) -> bool:
    if not path.is_file():
        return False
    text = path.read_text(encoding='utf-8', errors='ignore')
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith('#'):
            continue
        if stripped in EMPTY_TEMPLATE_LINES:
            continue
        if stripped == '-':
            continue
        if stripped.startswith('- '):
            value = stripped[2:].strip()
            if value.endswith(':') or value.endswith('：'):
                continue
        return True
    return False


def classify(path: Path) -> str:
    suffix = path.suffix.lower()
    lower = path.as_posix().lower()
    name = path.name.lower()

    if "/temp/extracted-text/" in lower and suffix in {".txt", ".md"}:
        return "extracted_text"
    if "/intake/research-notes/" in lower:
        return "research_notes" if has_user_content(path) else "other"
    if "/output/10-guides/" in lower:
        return "writing_guides"
    if "/output/15-selected-direction/" in lower or "selected-direction" in name:
        return "selected_direction" if has_user_content(path) else "other"
    if "/output/30-patent-package/" in lower:
        return "patent_package"
    if "/output/40-domain-accelerator/" in lower or (suffix == ".html" and ("explainer" in name or "accelerator" in name)):
        return "domain_accelerators"
    if suffix == ".pdf":
        return "sample_pdfs"
    if suffix in {".png", ".jpg", ".jpeg", ".svg"}:
        return "figures"
    return "other"


def next_steps(groups: dict[str, list[str]]) -> list[str]:
    steps: list[str] = []
    if not groups.get("sample_pdfs"):
        steps.append("Add local sample patent PDFs to intake/samples.")
    if not groups.get("research_notes"):
        steps.append("Optionally add online research notes or downloaded comparison materials to intake/research-notes.")
    if groups.get("sample_pdfs") and not groups.get("extracted_text"):
        steps.append("Run extract_pdf_text.py on the sample PDFs.")
    if (groups.get("sample_pdfs") or groups.get("extracted_text") or groups.get("research_notes")) and not groups.get("writing_guides"):
        steps.append("Run Research mode to derive a writing guide from PDFs and research notes.")
    if (groups.get("writing_guides") or groups.get("sample_pdfs") or groups.get("research_notes")) and not groups.get("selected_direction"):
        steps.append("Run AI Direction Decision mode to choose one utility-model direction and write selected-direction.md.")
    if groups.get("selected_direction") and not groups.get("patent_package"):
        steps.append("Run Patent Package mode to draft the disclosure, generate figure prompts, complete bundled review, and produce a reviewed draft.")
    if groups.get("selected_direction") and not groups.get("domain_accelerators"):
        steps.append("Optionally generate a domain accelerator page for non-specialist review.")
    if not steps:
        steps.append("Refresh the reviewed draft after human feedback and rebuild the manifest when new files are added.")
    return steps


def main() -> None:
    parser = argparse.ArgumentParser(description="Scan a local patent workspace and write a manifest.")
    parser.add_argument("--source", required=True, help="Workspace root or source folder")
    parser.add_argument("--output", help="Manifest output path. Defaults to <source>/manifest.json")
    args = parser.parse_args()

    source = Path(args.source).resolve()
    output = Path(args.output).resolve() if args.output else source / "manifest.json"

    groups: dict[str, list[str]] = defaultdict(list)
    for path in sorted(p for p in source.rglob("*") if p.is_file()):
        rel = path.relative_to(source).as_posix()
        groups[classify(path)].append(rel)

    output.parent.mkdir(parents=True, exist_ok=True)
    manifest = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": str(source),
        "counts": {key: len(value) for key, value in sorted(groups.items())},
        "files": {key: value for key, value in sorted(groups.items())},
        "recommended_next_steps": next_steps(groups),
    }
    output.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"manifest written: {output}")


if __name__ == "__main__":
    main()
