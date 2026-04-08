#!/usr/bin/env sh
set -eu

usage() {
  cat <<'EOF'
Usage:
  sh ./scripts/prepare_patent_workspace.sh

Optional:
  sh ./scripts/prepare_patent_workspace.sh --workspace workspaces/my-task

Options:
  --workspace <path>   Optional workspace path. Default: workspaces/default
  --force              Overwrite starter files when bootstrapping workspace
  -h, --help           Show this help

Workflow:
  1. Put patent PDFs into <workspace>/intake/samples/
  2. Optionally put research notes into <workspace>/intake/research-notes/
  3. Run this script
  4. Paste <workspace>/prompt-for-model.txt to the model

Notes:
  1. Run this script in Git Bash / WSL / any POSIX shell.
  2. The script uses the current `python` command, so it installs dependencies into the current Python environment.
EOF
}

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
PROJECT_ROOT=$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)
SKILL_DIR="$PROJECT_ROOT/skills/patent-copilot"
PYTHON_BIN="${PYTHON_BIN:-python}"

WORKSPACE="workspaces/default"
FORCE=0

while [ "$#" -gt 0 ]; do
  case "$1" in
    --workspace)
      WORKSPACE="${2:-}"
      shift 2
      ;;
    --force)
      FORCE=1
      shift 1
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

cd "$PROJECT_ROOT"

echo "[1/5] Ensure python dependencies in current environment..."
"$PYTHON_BIN" -m ensurepip --upgrade >/dev/null 2>&1 || true
"$PYTHON_BIN" -m pip install --disable-pip-version-check -r "$SKILL_DIR/requirements.txt"

echo "[2/5] Ensure workspace exists..."
if [ "$FORCE" -eq 1 ]; then
  "$PYTHON_BIN" "$SKILL_DIR/scripts/bootstrap_workspace.py" --root "$WORKSPACE" --name "$(basename "$WORKSPACE")" --force
else
  "$PYTHON_BIN" "$SKILL_DIR/scripts/bootstrap_workspace.py" --root "$WORKSPACE" --name "$(basename "$WORKSPACE")"
fi

echo "[3/5] Validate required input files..."
"$PYTHON_BIN" - "$WORKSPACE" <<'PY'
from pathlib import Path
import sys

EMPTY_TEMPLATE_LINES = {
    "-",
    "- Search Themes:",
    "- Confirmed Directions:",
    "- Links or Summaries:",
    "- Questions For AI To Judge:",
}


def has_user_content(path: Path) -> bool:
    text = path.read_text(encoding="utf-8", errors="ignore")
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped in EMPTY_TEMPLATE_LINES:
            continue
        if stripped.startswith("- "):
            value = stripped[2:].strip()
            if not value or value.endswith(":") or value.endswith("："):
                continue
        return True
    return False


workspace = Path(sys.argv[1]).resolve()
samples_dir = workspace / "intake" / "samples"
research_dir = workspace / "intake" / "research-notes"

pdfs = sorted(p for p in samples_dir.glob("*.pdf") if p.is_file())
notes = sorted(p for p in research_dir.iterdir() if p.is_file()) if research_dir.exists() else []
usable_notes = [p for p in notes if has_user_content(p)]

if not pdfs:
    raise SystemExit(
        f"No PDF files found.\nPut patent PDFs into: {samples_dir}"
    )

print(f"Found {len(pdfs)} PDF(s) and {len(usable_notes)} usable research file(s).")
PY

echo "[4/5] Build manifest and extract PDF text..."
"$PYTHON_BIN" "$SKILL_DIR/scripts/build_manifest.py" --source "$WORKSPACE"
"$PYTHON_BIN" "$SKILL_DIR/scripts/extract_pdf_text.py" \
  --input-dir "$WORKSPACE/intake/samples" \
  --output-dir "$WORKSPACE/temp/extracted-text" \
  --force

echo "[5/5] Refresh manifest and write final model prompt..."
"$PYTHON_BIN" "$SKILL_DIR/scripts/build_manifest.py" --source "$WORKSPACE"

PROMPT_FILE=$("$PYTHON_BIN" - "$WORKSPACE" "$SKILL_DIR" <<'PY'
from pathlib import Path
import sys

EMPTY_TEMPLATE_LINES = {
    "-",
    "- Search Themes:",
    "- Confirmed Directions:",
    "- Links or Summaries:",
    "- Questions For AI To Judge:",
}


def has_user_content(path: Path) -> bool:
    text = path.read_text(encoding="utf-8", errors="ignore")
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped in EMPTY_TEMPLATE_LINES:
            continue
        if stripped.startswith("- "):
            value = stripped[2:].strip()
            if not value or value.endswith(":") or value.endswith("："):
                continue
        return True
    return False


workspace = Path(sys.argv[1]).resolve()
skill_dir = Path(sys.argv[2]).resolve()
research_dir = workspace / "intake" / "research-notes"
usable_notes = []
if research_dir.exists():
    usable_notes = [p for p in sorted(research_dir.iterdir()) if p.is_file() and has_user_content(p)]

if usable_notes:
    prompt = (
        f"Use $patent-copilot at {skill_dir} to analyze the local workspace at {workspace}, "
        "read the PDFs in intake/samples, use the notes in intake/research-notes as additional constraints, "
        "choose one innovative utility-model direction by yourself, then produce the full patent package. "
        "Generate a domain accelerator page only if it helps non-specialist review."
    )
else:
    prompt = (
        f"Use $patent-copilot at {skill_dir} to analyze the local workspace at {workspace}, "
        "read the PDFs in intake/samples, "
        "choose one innovative utility-model direction by yourself, then produce the full patent package. "
        "Generate a domain accelerator page only if it helps non-specialist review."
    )

prompt_file = workspace / "prompt-for-model.txt"
prompt_file.write_text(prompt + "\n", encoding="utf-8")
print(prompt_file)
PY
)

echo
echo "Ready."
echo "Input PDFs dir: $(cd "$WORKSPACE/intake/samples" && pwd)"
echo "Input research dir: $(cd "$WORKSPACE/intake/research-notes" && pwd)"
echo "Prompt file: $PROMPT_FILE"
echo "Paste the content of prompt-for-model.txt to the model."
