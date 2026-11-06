from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.apply_template import ApplyError, TEMPLATE_ROOT, TEMPLATE_PATHS, apply_template


def relative_files(root: Path) -> set[Path]:
    return {path.relative_to(root) for path in root.rglob("*") if path.is_file()}


class ApplyTemplateTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.target = Path(self.temporary.name) / "project"
        self.target.mkdir()

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def test_copies_exact_runtime_footprint_and_preserves_unrelated_files(self) -> None:
        unrelated = self.target / "keep.txt"
        unrelated.write_text("keep", encoding="utf-8")

        conflicts = apply_template(self.target)

        self.assertEqual([], conflicts)
        self.assertEqual(
            {".omp", "AGENTS.md", "CONTEXT.md", "keep.txt"},
            {path.name for path in self.target.iterdir()},
        )
        self.assertEqual(
            relative_files(TEMPLATE_ROOT / ".omp"),
            relative_files(self.target / ".omp"),
        )
        for relative in (Path("AGENTS.md"), Path("CONTEXT.md")):
            self.assertEqual(
                (TEMPLATE_ROOT / relative).read_bytes(),
                (self.target / relative).read_bytes(),
            )
        self.assertEqual("keep", unrelated.read_text(encoding="utf-8"))

    def test_refuses_conflict_before_copying_any_path(self) -> None:
        existing_agents = self.target / "AGENTS.md"
        existing_agents.write_text("project policy", encoding="utf-8")

        with self.assertRaisesRegex(ApplyError, "Refusing to overwrite AGENTS.md"):
            apply_template(self.target)

        self.assertEqual("project policy", existing_agents.read_text(encoding="utf-8"))
        self.assertFalse((self.target / ".omp").exists())
        self.assertFalse((self.target / "CONTEXT.md").exists())

    def test_replace_removes_stale_selected_content_only(self) -> None:
        (self.target / ".omp").mkdir()
        (self.target / ".omp" / "stale.md").write_text("stale", encoding="utf-8")
        (self.target / "AGENTS.md").write_text("old agents", encoding="utf-8")
        (self.target / "CONTEXT.md").write_text("old context", encoding="utf-8")
        unrelated = self.target / "src.txt"
        unrelated.write_text("source", encoding="utf-8")

        conflicts = apply_template(self.target, replace=True)

        self.assertEqual(list(TEMPLATE_PATHS), conflicts)
        self.assertFalse((self.target / ".omp" / "stale.md").exists())
        self.assertEqual(relative_files(TEMPLATE_ROOT / ".omp"), relative_files(self.target / ".omp"))
        self.assertEqual("source", unrelated.read_text(encoding="utf-8"))

    def test_dry_run_reports_replacement_without_changes(self) -> None:
        existing_agents = self.target / "AGENTS.md"
        existing_agents.write_text("project policy", encoding="utf-8")

        conflicts = apply_template(self.target, replace=True, dry_run=True)

        self.assertEqual([Path("AGENTS.md")], conflicts)
        self.assertEqual("project policy", existing_agents.read_text(encoding="utf-8"))
        self.assertEqual(["AGENTS.md"], [path.name for path in self.target.iterdir()])


if __name__ == "__main__":
    unittest.main()
