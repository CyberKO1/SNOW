# SNOW

Helps write ServiceNow RFC/PIR content with Codex skills.

## Included skill

- `rfc-writer`: Generates Costa ServiceNow RFC/Change requests in strict template format with a continuous step timeline.

## Use on another computer

### Option 1: Use from this repository

1. Clone the repository:
   - `git clone https://github.com/CyberKO1/SNOW.git`
2. Open the cloned folder in Codex.
3. Confirm the repository includes [AGENTS.md](AGENTS.md). This advertises `rfc-writer` to Codex.
4. Start a prompt with `$rfc-writer` and describe the change details in English.

Example:

```text
$rfc-writer
Generate a Costa ServiceNow RFC in English only.
Scheduled start: 01/04/2026 15:00:00
Scheduled end: 01/04/2026 19:00:00
Business justification: ...
Implementation steps: ...
Regression steps: ...
```

### Option 2: Install as a personal Codex skill

1. Copy `skills/rfc-writer` into your Codex skills directory:
   - Windows: `%USERPROFILE%\\.codex\\skills\\rfc-writer`
2. In the repository or workspace where you want to use it, add an `AGENTS.md` entry pointing to that skill folder.
3. Open that workspace in Codex and invoke `$rfc-writer`.

## Requirements

- `python` available in `PATH`
- Codex running in the repository or workspace that exposes the skill through `AGENTS.md`

The timeline engine used by the skill is [timeline_planner.py](skills/rfc-writer/scripts/timeline_planner.py).
