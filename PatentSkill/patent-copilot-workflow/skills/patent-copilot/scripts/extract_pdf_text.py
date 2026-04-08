from __future__ import annotations

import argparse
from pathlib import Path

try:
    from pypdf import PdfReader
except ModuleNotFoundError as exc:  # pragma: no cover
    raise SystemExit("Missing dependency: pypdf. Install it before running this script.") from exc


def extract_text(pdf_path: Path) -> str:
    reader = PdfReader(str(pdf_path))
    parts: list[str] = []
    for index, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        parts.append(f"\n\n===== PAGE {index} =====\n{text}")
    return "".join(parts)


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract text from local PDF files into page-marked text files.")
    parser.add_argument("--input-dir", required=True, help="Directory containing source PDFs")
    parser.add_argument("--output-dir", required=True, help="Directory for extracted text files")
    parser.add_argument("--pattern", default="*.pdf", help="Glob pattern for source PDFs")
    parser.add_argument("--force", action="store_true", help="Overwrite existing text files")
    args = parser.parse_args()

    input_dir = Path(args.input_dir).resolve()
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    for pdf_path in sorted(input_dir.glob(args.pattern)):
        output_path = output_dir / f"{pdf_path.stem}.txt"
        if output_path.exists() and not args.force:
            print(f"skip: {pdf_path.name}")
            continue
        output_path.write_text(extract_text(pdf_path), encoding="utf-8")
        print(f"extracted: {pdf_path.name} -> {output_path.name}")


if __name__ == "__main__":
    main()
