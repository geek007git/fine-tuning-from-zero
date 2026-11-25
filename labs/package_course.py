"""Bundle course sources, excluding local run artifacts and Python caches."""
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).parent.parent
DEST = ROOT.parent / "Fine_Tuning_from_Zero_English_Core.zip"
EXCLUDE = {".venv", "__pycache__", "runs", ".git"}


def main():
    with ZipFile(DEST, "w", ZIP_DEFLATED) as archive:
        for source in sorted(ROOT.rglob("*")):
            if source.is_file() and not any(part in EXCLUDE for part in source.relative_to(ROOT).parts):
                archive.write(source, f"{ROOT.name}/{source.relative_to(ROOT).as_posix()}")
    print(f"Bundled course at {DEST}")


if __name__ == "__main__":
    main()
