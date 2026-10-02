import argparse
import os
from pathlib import Path
import shutil
import sys


ROOT = Path(__file__).resolve().parent
FILES = (
    (
        Path(".opencode/plugins/vibe-wise.ts"),
        Path("plugins/vibe-wise.ts"),
    ),
    (
        Path(".opencode/skills/vibe-wise-learn/SKILL.md"),
        Path("skills/vibe-wise-learn/SKILL.md"),
    ),
    (
        Path(".opencode/skills/vibe-wise-reset/SKILL.md"),
        Path("skills/vibe-wise-reset/SKILL.md"),
    ),
    (
        Path(".opencode/skills/vibe-wise-reset/reset.py"),
        Path("skills/vibe-wise-reset/reset.py"),
    ),
    (
        Path(".opencode/commands/vibe-wise-learn.md"),
        Path("commands/vibe-wise-learn.md"),
    ),
    (
        Path(".opencode/commands/vibe-wise-reset.md"),
        Path("commands/vibe-wise-reset.md"),
    ),
)


def unsafe_target(target, destination):
    if destination.is_symlink() or (destination.exists() and not destination.is_file()):
        return True
    parent = destination.parent
    while parent != target:
        if parent.is_symlink() or (parent.exists() and not parent.is_dir()):
            return True
        parent = parent.parent
    return False


def install(target, force=False):
    entries = []
    conflicts = []
    for source, relative_target in FILES:
        source_path = ROOT / source
        target_path = target / relative_target
        if not source_path.is_file():
            raise FileNotFoundError(f"Package file is missing: {source_path}")
        if unsafe_target(target, target_path):
            conflicts.append(relative_target)
        elif (
            target_path.is_file()
            and target_path.read_bytes() != source_path.read_bytes()
            and not force
        ):
            conflicts.append(relative_target)
        entries.append((source_path, target_path))
    if conflicts:
        paths = "\n".join(f"  {target / path}" for path in conflicts)
        print(
            "Existing or unsafe targets conflict; nothing installed. Review them; "
            "--force only replaces regular files:\n" + paths,
            file=sys.stderr,
        )
        return 1

    for source_path, target_path in entries:
        if target_path.is_file() and target_path.read_bytes() == source_path.read_bytes():
            print(f"Unchanged: {target_path}")
            continue
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_path, target_path)
        print(f"Installed: {target_path}")
    return 0


def main():
    config_home = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
    parser = argparse.ArgumentParser(description="Install VibeWise for OpenCode.")
    parser.add_argument("--target", type=Path, default=config_home / "opencode")
    parser.add_argument("--force", action="store_true", help="Replace differing VibeWise files")
    args = parser.parse_args()
    try:
        return install(args.target.expanduser().resolve(), args.force)
    except OSError as error:
        print(f"Installation failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
