---
name: vibe-wise-reset
description: Safely reset VibeWise learning notes with a preview, explicit confirmation, and backup. Use only when the user explicitly invokes /vibe-wise-reset or requests resetting VibeWise learning notes.
---

# VibeWise Reset

Respond in the learner's language. Reset only this project's learning profile, progress, and project map. Never reset application source, Git history, dependencies, or another project.

1. Determine the current absolute project path. Run the preview:

   ```sh
   python3 "$HOME/.config/opencode/skills/vibe-wise-reset/reset.py" --cwd "<absolute project path>"
   ```

   Replace the placeholder with the actual path and quote it safely. Preview is read-only. If the result is `no_notes`, change nothing and suggest `/vibe-wise-learn`. Stop on errors.

2. Show the project path, notes path, files to reset, and backup location. Ask explicitly whether to reset exactly these notes. Offer Cancel and Reset learning; use OpenCode's question tool if available, otherwise ask in plain text. Wait for a clear answer. Invocation, silence, or ambiguity is not confirmation. Cancel means no changes.

3. Only after explicit confirmation, run the same script with the unchanged project path and exact preview token:

   ```sh
   python3 "$HOME/.config/opencode/skills/vibe-wise-reset/reset.py" --cwd "<absolute project path>" --confirm "<preview token>"
   ```

   If the project or notes changed, preview again and get fresh confirmation. Do not substitute ad hoc deletion commands. If reset fails, do not claim success.

4. On success, report the backup path, discard pre-reset notes/preferences, and restart onboarding with `/vibe-wise-learn`. Backups are history, not active instructions.
