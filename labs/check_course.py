"""Check local Markdown links and toy data without installing ML packages."""
import re
from pathlib import Path

from audit_and_baseline import audit, read_rows

ROOT = Path(__file__).parent.parent
SKIP = {".venv", "venv", "env", "runs", "__pycache__", ".git", "node_modules"}


def main():
    missing = []
    for page in ROOT.rglob("*.md"):
        if any(part in SKIP for part in page.relative_to(ROOT).parts):
            continue  # a learner's virtualenv contains thousands of package READMEs
        for link in re.findall(r"\[[^\]]+\]\(([^)]+)\)", page.read_text(encoding="utf-8")):
            target = link.split("#", 1)[0]
            if not target or "://" in target or target.startswith("mailto:"):
                continue
            if not (page.parent / target).exists():
                missing.append(f"{page.relative_to(ROOT)} -> {target}")
    if missing:
        raise SystemExit("Missing local links:\n" + "\n".join(missing))
    counts = audit(read_rows())
    print(f"Checked local links and {sum(counts.values())} toy tickets")


if __name__ == "__main__":
    main()
