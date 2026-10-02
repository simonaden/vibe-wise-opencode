# VibeWise for OpenCode

VibeWise supports learning-first development: you shape the design, OpenCode explains tradeoffs and implements the steps you approve.

This is an OpenCode adaptation of [VibeWise](https://github.com/nykooi1/vibe-wise), originally created by Noah Kim. It keeps learner notes in each project and does not send them to a VibeWise service.

## Install globally

Requirements: OpenCode and Python 3.

1. Clone this repository.
2. From its directory, run:

   ```sh
   python3 install.py
   ```

The installer copies the plugin, skills, and commands into `~/.config/opencode/`. It honors `XDG_CONFIG_HOME` and accepts `--target` for a different OpenCode config directory. Restart OpenCode after installation.

If an existing VibeWise file differs, the installer stops without changing anything. Review the conflict; pass `--force` only if you intend to replace those regular files. Symlink targets are always refused. Rerun the installer to update.

## Use

- `/vibe-wise-learn` starts or resumes learning mode.
- `/vibe-wise-reset` previews a reset and requires explicit confirmation before backing up and restarting onboarding.

When active notes are found, the plugin restores learning context at chat start and before compaction. Project notes live under `.vibe-wise/`; the reset command keeps timestamped backups there. The repository ignores `.vibe-wise/` so personal learning notes are not published with the plugin.

## License and attribution

MIT. This adaptation retains the original VibeWise copyright and license notice; see [LICENSE](LICENSE).
