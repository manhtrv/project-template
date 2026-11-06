#!/usr/bin/env python3
"""Apply the repository-local OMP template to another project."""

from __future__ import annotations

import argparse
import os
import shutil
import stat
import sys
import tempfile
from pathlib import Path
from typing import Iterable

TEMPLATE_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_PATHS = (Path(".omp"), Path("AGENTS.md"), Path("CONTEXT.md"))


class ApplyError(RuntimeError):
    """A safe, user-actionable template application failure."""


def existing(path: Path) -> bool:
    return path.exists() or path.is_symlink()


def remove_path(path: Path) -> None:
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.is_dir():
        shutil.rmtree(path)


def validate_source() -> None:
    for relative in TEMPLATE_PATHS:
        source = TEMPLATE_ROOT / relative
        try:
            metadata = source.lstat()
        except FileNotFoundError as error:
            raise ApplyError(f"Template source is missing {relative}") from error
        if stat.S_ISLNK(metadata.st_mode):
            raise ApplyError(f"Template source must not be a symlink: {relative}")
        if relative == Path(".omp") and not stat.S_ISDIR(metadata.st_mode):
            raise ApplyError("Template source .omp must be a directory")
        if relative != Path(".omp") and not stat.S_ISREG(metadata.st_mode):
            raise ApplyError(f"Template source must be a regular file: {relative}")

    for directory, directories, files in os.walk(TEMPLATE_ROOT / ".omp", followlinks=False):
        base = Path(directory)
        for name in (*directories, *files):
            path = base / name
            if path.is_symlink():
                raise ApplyError(f"Template source must not contain symlinks: {path.relative_to(TEMPLATE_ROOT)}")


def resolve_target(raw_target: str) -> Path:
    target = Path(raw_target).expanduser()
    try:
        resolved = target.resolve(strict=True)
    except FileNotFoundError as error:
        raise ApplyError(f"Target project does not exist: {target}") from error
    if not resolved.is_dir():
        raise ApplyError(f"Target project is not a directory: {resolved}")
    if resolved == TEMPLATE_ROOT:
        raise ApplyError("Target project must differ from the template repository")
    return resolved


def conflict_paths(target: Path) -> list[Path]:
    return [relative for relative in TEMPLATE_PATHS if existing(target / relative)]


def format_paths(paths: Iterable[Path]) -> str:
    return ", ".join(str(path) for path in paths)


def stage_template(stage: Path) -> None:
    shutil.copytree(TEMPLATE_ROOT / ".omp", stage / ".omp")
    shutil.copy2(TEMPLATE_ROOT / "AGENTS.md", stage / "AGENTS.md")
    shutil.copy2(TEMPLATE_ROOT / "CONTEXT.md", stage / "CONTEXT.md")


def install_staged(stage: Path, target: Path, conflicts: list[Path]) -> None:
    backup = stage.parent / "backup"
    backup.mkdir()
    backed_up: list[Path] = []
    installed: list[Path] = []

    try:
        for relative in conflicts:
            os.replace(target / relative, backup / relative)
            backed_up.append(relative)
        for relative in TEMPLATE_PATHS:
            os.replace(stage / relative, target / relative)
            installed.append(relative)
    except Exception as error:
        rollback_errors: list[str] = []
        for relative in reversed(installed):
            try:
                remove_path(target / relative)
            except Exception as rollback_error:
                rollback_errors.append(f"remove {relative}: {rollback_error}")
        for relative in reversed(backed_up):
            try:
                os.replace(backup / relative, target / relative)
            except Exception as rollback_error:
                rollback_errors.append(f"restore {relative}: {rollback_error}")
        suffix = f" Rollback errors: {'; '.join(rollback_errors)}" if rollback_errors else ""
        raise ApplyError(f"Failed to apply template: {error}.{suffix}") from error


def apply_template(target: Path, *, replace: bool = False, dry_run: bool = False) -> list[Path]:
    validate_source()
    conflicts = conflict_paths(target)
    if conflicts and not replace:
        raise ApplyError(
            f"Refusing to overwrite {format_paths(conflicts)} in {target}. "
            "Re-run with --replace only after reviewing those paths."
        )
    if dry_run:
        return conflicts

    with tempfile.TemporaryDirectory(prefix=".principal-omp-", dir=target.parent) as temporary:
        temporary_root = Path(temporary)
        stage = temporary_root / "new"
        stage.mkdir()
        stage_template(stage)
        install_staged(stage, target, conflicts)
    return conflicts


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Copy only .omp/, AGENTS.md, and CONTEXT.md from this template into another project."
    )
    parser.add_argument("target", help="Existing target project directory")
    parser.add_argument(
        "--replace",
        action="store_true",
        help="Replace existing target .omp/, AGENTS.md, and CONTEXT.md after staging the new copies",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate and report without changing the target; combine with --replace to preview replacement",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        target = resolve_target(args.target)
        conflicts = apply_template(target, replace=args.replace, dry_run=args.dry_run)
    except ApplyError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    action = "Would replace" if args.dry_run and conflicts else "Would copy" if args.dry_run else "Applied"
    print(f"{action} Principal Engineering OMP template in {target}")
    print(f"Paths: {format_paths(TEMPLATE_PATHS)}")
    if conflicts:
        print(f"Existing selected paths: {format_paths(conflicts)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
