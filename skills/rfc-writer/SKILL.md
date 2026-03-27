---
name: rfc-writer
description: Generate Costa ServiceNow RFC/Change requests from user-provided change details. Use when asked to create, fill, or format ServiceNow change request templates, enforce exact template structure and step-line format, ask follow-up questions for missing required fields, and produce a continuous step timeline from scheduled start to scheduled end.
---

# RFC Writer

Use this skill to produce a submission-ready Costa ServiceNow RFC/Change request in strict template order.

## Load References

1. Read `references/template.txt` for required section order and labels.
2. Read `references/example.txt` for expected style and step formatting.
3. Read `references/field_rules.md` for required fields, allowed values, and defaults.

## Required Workflow

1. Extract user-provided facts first.
2. Validate required fields from `references/field_rules.md`.
3. Ask concise follow-up questions for any missing required fields before generating final output.
   - If communication contacts are missing, apply defaults from `references/field_rules.md`.
4. Build full step data across these sections in this order:
   - Pre- Implementation Plan
   - Implementation Plan
   - Post-implementation Tests
   - User Acceptance Testing
   - Post-implementation monitoring
   - Regression Steps
   - Post Regression Tests
5. Run `scripts/timeline_planner.py` to assign/repair step timing.
6. Output one complete RFC body in exact template section order.

## Formatting Rules

1. Output must be English-only. Do not include any Chinese text.
2. Use datetime format `dd/MM/yyyy HH:mm:ss`.
3. Use step row format exactly:
   - `Step N - Start Date and Time - Duration - Description - Owner Name/Team - Service Impact`
4. Preserve short-description keyword conventions:
   - Keep change type marker such as `[Normal]` or `[ACCELERATED]`.
   - Include `[COSTA CHINA]` for China changes.
5. Allowed `Service Impact` values only:
   - `No Outage`
   - `Service Outage`
   - `Service Degradation`
6. Use `NA` only when a field is not applicable, without removing template sections.

## Timeline Rules

1. First step start time must equal `Scheduled Start(date & time)`.
2. Each subsequent step must start exactly when the previous step ends.
3. Last step end time must equal `Scheduled End(date & time)`.
4. If duration is provided by user, keep it unless continuity repair is required.
5. If duration is missing, estimate by complexity.
6. If complexity is unclear, split evenly.
7. Use 5-minute granularity while preserving exact end-time closure.

## Output Constraint

Return only one submission-ready RFC body with no placeholders.
