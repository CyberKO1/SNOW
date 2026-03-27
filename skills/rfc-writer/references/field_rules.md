# RFC Writer Field Rules

## Required Fields

- `scheduled_start`: RFC start time in `dd/MM/yyyy HH:mm:ss`.
- `scheduled_end`: RFC end time in `dd/MM/yyyy HH:mm:ss`.
- `short_description`: include change type keyword; include `[COSTA CHINA]` for China changes.
- `business_justification`: business need and expected value.
- `affected_services`: impacted services/components or explicit no-impact note.
- `implementation_steps`: executable tasks for pre-implementation and implementation.
- `test_steps`: executable tasks for post-implementation tests, UAT, and monitoring.
- `regression_steps`: rollback and post-regression validation tasks.
- `owner_contacts`: notification contacts and communication owner.

## Optional Fields

- `change_type`
- `actual_start`
- `actual_end`
- `risk_review`
- `communication_plan`
- `end_user_experience`

## Fixed Section Order

1. Change Type
2. Scheduled Start(date & time)
3. Scheduled End(date & time)
4. Short description
5. Change Summary & Business Justification
6. Affected Services/ Systems / Components/ Applications Impacted
7. Implementation plan
8. Test plan
9. Regression Plan
10. End User Experience
11. Risk Review
12. Communication Plan

## Step Format and Constraints

- Line format:
  - `Step N - Start Date and Time - Duration - Description - Owner Name/Team - Service Impact`
- Allowed `Service Impact` values only:
  - `No Outage`
  - `Service Outage`
  - `Service Degradation`
- Duration format:
  - `HH:MM`

## Timeline Constraints

1. First step starts at `scheduled_start`.
2. Every step starts at previous step end.
3. Final step end must equal `scheduled_end`.
4. Use 5-minute granularity for generated durations.
5. If user durations exist, keep them unless continuity repair is needed.
6. If some durations are missing, estimate by complexity weighting.
7. If complexity is unclear, split remaining duration evenly.
8. If window is too short, stop and ask user to expand window or reduce steps.

## Language and Output Policy

1. Final RFC output must be English-only.
2. Keep all template labels and section structure unchanged.
3. Use `NA` only for non-applicable values, not as a placeholder for missing required inputs.

## Default Communication Contacts Template

Use these lines as default communication recipients unless the user provides a different list:

- `3rd Party - Cloud-Costa-GDC - cloudcostagdc@coca-cola.com`
- `Costa - Costa China IT - china.it@costacoffee.com`
