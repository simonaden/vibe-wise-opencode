from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / "install.py"


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.target = Path(self.temp.name) / "opencode"

    def run_installer(self, *arguments):
        return subprocess.run(
            [
                sys.executable,
                "-B",
                str(INSTALLER),
                "--target",
                str(self.target),
                *arguments,
            ],
            capture_output=True,
            text=True,
            check=False,
        )

    def test_installs_all_files_and_is_idempotent(self):
        first = self.run_installer()
        self.assertEqual(first.returncode, 0, first.stderr)
        for source, destination in (
            (
                ROOT / ".opencode/plugins/vibe-wise.ts",
                self.target / "plugins/vibe-wise.ts",
            ),
            (
                ROOT / ".opencode/skills/vibe-wise-learn/SKILL.md",
                self.target / "skills/vibe-wise-learn/SKILL.md",
            ),
            (
                ROOT / ".opencode/skills/vibe-wise-reset/SKILL.md",
                self.target / "skills/vibe-wise-reset/SKILL.md",
            ),
            (
                ROOT / ".opencode/skills/vibe-wise-reset/reset.py",
                self.target / "skills/vibe-wise-reset/reset.py",
            ),
            (
                ROOT / ".opencode/commands/vibe-wise-learn.md",
                self.target / "commands/vibe-wise-learn.md",
            ),
            (
                ROOT / ".opencode/commands/vibe-wise-reset.md",
                self.target / "commands/vibe-wise-reset.md",
            ),
        ):
            self.assertEqual(destination.read_bytes(), source.read_bytes())
        second = self.run_installer()
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertIn("Unchanged:", second.stdout)

    def test_conflict_aborts_without_overwriting_or_partial_install(self):
        skill = self.target / "skills/vibe-wise-learn/SKILL.md"
        skill.parent.mkdir(parents=True)
        skill.write_text("local edit\n", encoding="utf-8")
        result = self.run_installer()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(skill.read_text(encoding="utf-8"), "local edit\n")
        self.assertFalse((self.target / "plugins/vibe-wise.ts").exists())

    def test_force_replaces_only_after_explicit_request(self):
        self.assertEqual(self.run_installer().returncode, 0)
        plugin = self.target / "plugins/vibe-wise.ts"
        plugin.write_text("local edit\n", encoding="utf-8")
        self.assertNotEqual(self.run_installer().returncode, 0)
        result = self.run_installer("--force")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(plugin.read_bytes(), (ROOT / ".opencode/plugins/vibe-wise.ts").read_bytes())

    def test_refuses_symlink_target_even_with_force(self):
        outside = Path(self.temp.name) / "outside.ts"
        outside.write_text("keep this file\n", encoding="utf-8")
        plugin = self.target / "plugins/vibe-wise.ts"
        plugin.parent.mkdir(parents=True)
        try:
            plugin.symlink_to(outside)
        except (NotImplementedError, OSError) as error:
            self.skipTest(f"Symlinks are unavailable: {error}")
        result = self.run_installer("--force")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(outside.read_text(encoding="utf-8"), "keep this file\n")


if __name__ == "__main__":
    unittest.main()
