# OpenClaw Field Rules

## Required Fields

- `scheduled_start`: change window start in `dd/MM/yyyy HH:mm:ss`.
- `scheduled_end`: change window end in `dd/MM/yyyy HH:mm:ss`.
- `short_description`: must preserve change-type keyword and include `[COSTA CHINA]` for China changes.
- `business_justification`: clear reason and business value.
- `affected_services`: impacted or explicitly no-impact systems.
- `implementation_steps`: executable tasks for pre-implementation + implementation sections.
- `test_steps`: executable tasks for post-implementation tests + UAT + monitoring.
- `regression_steps`: rollback + post-regression validation tasks.
- `owner_contacts`: communication recipients and responsible sender.

## Optional Fields

- `risk_review`
- `communication_plan`
- `end_user_experience`
- `actual_start`
- `actual_end`
- `change_type`

## Section Order (Must Not Change)

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

## Step Row Format

`Step N - Start Date and Time - Duration - Description - Owner Name/Team - Service Impact`

## Service Impact Allowed Values

- `No Outage`
- `Service Outage`
- `Service Degradation`

## Timeline Rules

1. First step start equals `scheduled_start`.
2. Every step starts when previous step ends.
3. Final step end equals `scheduled_end`.
4. Default duration granularity is 5 minutes.
5. Prefer user durations; fill missing durations by complexity-based estimate.
6. If complexity is unclear, split evenly.
7. If total window is too short to assign valid durations, request user to adjust window or reduce steps.

## Missing Information Questions

Ask concise follow-up questions when required fields are missing. Prioritize:

1. change window start/end
2. implementation/test/regression task intents
3. owners and communication contacts
4. risk and user-impact statements
