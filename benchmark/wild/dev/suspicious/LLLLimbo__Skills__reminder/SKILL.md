---
name: reminder
description: Play audio alerts via ffplay when Codex finishes a task, encounters an error/abort, or needs user help; use in WSL environments with the reminder-tool audio prompts and map events to TASK_FINISHED, ERROR, or NEED_HELP.
---

# Reminder

## Overview

Use `ffplay` to play short MP3 alerts for task completion, errors, or help-needed moments. Keep usage optional and non-intrusive.

## Workflow

1. Determine the event type.
   - Task completed successfully -> `TASK_FINISHED`
   - Task failed or aborted -> `ERROR`
   - Waiting for user input or blocked -> `NEED_HELP`
2. Play the matching sound once with `ffplay` (avoid repeated alerts for the same event).
3. If `ffplay` is unavailable or playback fails, continue without blocking and optionally mention the missing dependency.

## Command usage

Use `ffplay` with no display and auto-exit:

```bash
ffplay -nodisp -autoexit assets/audio/TASK_FINISHED.mp3
```

```bash
ffplay -nodisp -autoexit assets/audio/ERROR.mp3
```

```bash
ffplay -nodisp -autoexit assets/audio/NEED_HELP.mp3
```

## Notes

- Audio files live in `assets/audio/*.mp3`; adjust the path if you store them elsewhere.
- Audio playback requires WSL audio support and `ffplay` in PATH.
