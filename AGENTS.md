# AGENTS.md

## Skills
A skill is a set of local instructions stored in a `SKILL.md` file. Use the skills below when the user names the skill directly or when the request clearly matches the skill description.

### Available skills
- `rfc-writer`: Generate Costa ServiceNow RFC/Change requests from user-provided change details. Use when asked to create, fill, or format ServiceNow change request templates, enforce exact template structure and step-line format, ask follow-up questions for missing required fields, and produce a continuous step timeline from scheduled start to scheduled end. (file: `skills/rfc-writer/SKILL.md`)

## How to use skills
- Open the referenced `SKILL.md` and read only what is needed for the current task.
- Load files from `references/` only when needed.
- Use files in `scripts/` for deterministic work such as timeline generation or validation.
- Do not carry a skill across turns unless the user names it again or the new task clearly matches it.
