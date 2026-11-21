#!/usr/bin/env python3
"""
Tworzy czysty, gotowy do wypakowania ZIP z tłumaczeniem.

Skrypt należy umieścić w:
        /Notes/scripts/build_github_release.py

Wykrywa root repozytorium automatycznie (dwa poziomy wyżej).
Pakuje tylko Core + DLC; Notes, README files, .git, i inny housekeeping jest pomijany.
"""

from __future__ import annotations

import argparse
import sys
import zipfile
from pathlib import Path, PurePosixPath

MODULES = (
    "Core",
    "Royalty",
    "Ideology",
    "Biotech",
    "Anomaly",
    "Odyssey",
)

EXCLUDED_DIRS = {".git", ".github", "__pycache__"}
EXCLUDED_FILES = {".DS_Store", "Thumbs.db"}


def default_repository_root() -> Path:
    """Zwróc root dla Notes/scripts/<ten skrypciok>."""
    return Path(__file__).resolve().parents[2]


def translation_source(module_dir: Path, language_folder: str) -> Path:
    """Resolve zależnie od tego czy folder jest według struktury tłumaczenia czy gry."""
    languages_dir = module_dir / "Languages"
    if not languages_dir.is_dir():
        return module_dir

    requested = languages_dir / language_folder
    if requested.is_dir():
        return requested

    candidates = sorted(p for p in languages_dir.iterdir() if p.is_dir())
    if len(candidates) == 1:
        return candidates[0]

    raise RuntimeError(
        f"Nie znaleziono folderu tłumaczenia w '{languages_dir}'. "
        f"Wpisz jego nazwę po --language-folder."
    )


def iter_files(root: Path):
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(root)
        if any(part in EXCLUDED_DIRS for part in relative.parts):
            continue
        if path.name in EXCLUDED_FILES:
            continue
        yield path, relative


def build_zip(source: Path, output: Path, language_folder: str) -> tuple[int, list[str]]:
    if not source.is_dir():
        raise FileNotFoundError(f"Folder źródłowy nie istnieje: {source}")

    output = output.resolve()
    packaged_modules: list[str] = []
    file_count = 0

    # Stwórz nowe archiwum; modułowa budowa
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for module in MODULES:
            module_dir = source / module
            if not module_dir.is_dir():
                continue

            content_root = translation_source(module_dir, language_folder)
            files = list(iter_files(content_root))
            if not files:
                continue

            packaged_modules.append(module)
            for file_path, relative in files:
                archive_path = PurePosixPath(
                    "Data", module, "Languages", language_folder, *relative.parts
                ).as_posix()
                archive.write(file_path, archive_path)
                file_count += 1

    if not packaged_modules:
        output.unlink(missing_ok=True)
        raise RuntimeError(
            "Nie znaleziono plików tłumaczenia. Wybrany folder musi zawierać "
            "co najmniej: " + ", ".join(MODULES)
        )

    return file_count, packaged_modules


def main() -> int:
    repository_root = default_repository_root()

    parser = argparse.ArgumentParser(
        description="Spakuj tłumaczenie RimWorld w ZIP szybkiej instalacji"
    )
    parser.add_argument(
        "source",
        nargs="?",
        type=Path,
        default=repository_root,
        help="folder repozytorium (domyślnie root)",
    )
    parser.add_argument(
        "-o", "--output",
        type=Path,
        default=None,
        help="ścieżka gdzie wypluje Ci ZIPa (domyślnie RimWorld-Polish-Quick-Install.zip w folderze źródłowym)",
    )
    parser.add_argument(
        "--language-folder",
        default="Polski (Github)",
        help="nazwa folderu dla instalacji (domyślnie: Polski (Github))",
    )
    args = parser.parse_args()

    source = args.source.expanduser().resolve()
    output = args.output.expanduser().resolve() if args.output else (
        source / "RimWorld-Polish-Quick-Install.zip"
    )

    try:
        count, modules = build_zip(source, output, args.language_folder)
    except (OSError, RuntimeError, zipfile.BadZipFile) as exc:
        print(f"\nERROR: {exc}", file=sys.stderr)
        return 1

    print("\nStworzono ZIP szybkiej instalacji:")
    print(f"  {output}")
    print(f"\nModuły: {', '.join(modules)}")
    print(f"Pliki tłumaczenia: {count}")
    print(f"Folder języka: {args.language_folder}")
    print("\nWypakuj ZIPa do folderu z grą by mieć najnowszą wersję tłumaczenia.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
