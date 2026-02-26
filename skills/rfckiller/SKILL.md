---
name: openclaw
description: Generate and fill Costa ServiceNow Change Request content from user-provided change details. Use when asked to create, complete, or format Costa change request templates (including COSTA CHINA requests), enforce strict section/line format, ask follow-up questions for missing required fields, and build a continuous end-to-end step timeline from scheduled start to scheduled end.
---

# OpenClaw

Use this skill to produce a fully filled Costa ServiceNow Change Request in the exact template structure.

## Load References

1. Read `references/template.txt` for required output structure and section order.
2. Read `references/example.txt` for line-level formatting style.
3. Read `references/field_rules.md` for validation and defaults.

## Mandatory Workflow

1. Extract provided facts from the user message.
2. Validate required inputs:
   - `scheduled_start`
   - `scheduled_end`
   - `short_description`
   - `business_justification`
   - `affected_services`
   - implementation/test/regression step intent (can be high level)
   - owner contacts
3. If any required field is missing, ask concise follow-up questions first. Do not output a partial final template.
4. Build full step records across these sections in order:
   - Pre- Implementation Plan
   - Implementation Plan
   - Post-implementation Tests
   - User Acceptance Testing
   - Post-implementation monitoring
   - Regression Steps
   - Post Regression Tests
5. Use `scripts/timeline_planner.py` to assign/repair start time and duration for all step rows so that:
   - first step start equals scheduled start
   - each next step starts at previous step end
   - final step end equals scheduled end
6. Output the final request in the same section order and line pattern as `references/template.txt`.

## Formatting Rules

1. Use datetime format `dd/MM/yyyy HH:mm:ss` for all step start timestamps and scheduled start/end fields.
2. Use step row format exactly:
   - `Step N - Start Date and Time - Duration - Description - Owner Name/Team - Service Impact`
3. Allowed `Service Impact` values only:
   - `No Outage`
   - `Service Outage`
   - `Service Degradation`
4. Preserve short-description keyword requirements:
   - Keep change type keyword such as `[Normal]` or `[ACCELERATED]`.
   - For China changes include `[COSTA CHINA]`.
5. Use `NA` for non-applicable fields without changing section structure.

## Duration Policy

1. If user provides step durations, keep them unless continuity fix is required.
2. If durations are missing, estimate by complexity:
   - complex task: higher weight
   - normal task: medium weight
   - trivial verification/notification: lower weight
3. If complexity is unclear, split evenly.
4. Round durations to 5-minute increments while preserving exact scheduled end closure.

## Output Constraint

Return only one complete, submission-ready change request body in template order.
