#!/usr/bin/env python3
"""Plan and validate a continuous ServiceNow change timeline."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any

DT_FORMAT = "%d/%m/%Y %H:%M:%S"
ALLOWED_IMPACTS = {"No Outage", "Service Outage", "Service Degradation"}
MIN_STEP_MINUTES = 5


@dataclass
class Step:
    section: str
    description: str
    owner: str
    service_impact: str
    complexity: str = "normal"
    duration_minutes: int | None = None
    start: datetime | None = None
    end: datetime | None = None


def parse_datetime(value: str) -> datetime:
    return datetime.strptime(value, DT_FORMAT)


def fmt_datetime(value: datetime) -> str:
    return value.strftime(DT_FORMAT)


def parse_duration_to_minutes(value: str | None) -> int | None:
    if value is None:
        return None
    text = value.strip()
    if not text:
        return None
    parts = text.split(":")
    if len(parts) != 2:
        raise ValueError(f"Invalid duration '{value}'. Expected HH:MM.")
    hours = int(parts[0])
    minutes = int(parts[1])
    total = (hours * 60) + minutes
    if total <= 0:
        raise ValueError(f"Duration must be positive: '{value}'.")
    return total


def format_duration(minutes: int) -> str:
    hours = minutes // 60
    mins = minutes % 60
    return f"{hours:02d}:{mins:02d}"


def complexity_weight(level: str) -> int:
    text = (level or "").strip().lower()
    if text in {"high", "complex"}:
        return 3
    if text in {"low", "trivial"}:
        return 1
    return 2


def round_down_to_5(minutes: float) -> int:
    return int(minutes // 5) * 5


def allocate_missing_durations(
    steps: list[Step], total_minutes: int, strict_five_minute: bool = True
) -> None:
    known_total = sum(s.duration_minutes or 0 for s in steps)
    missing = [idx for idx, step in enumerate(steps) if step.duration_minutes is None]

    if not missing:
        delta = total_minutes - known_total
        if delta == 0:
            return
        if steps[-1].duration_minutes is None:
            steps[-1].duration_minutes = MIN_STEP_MINUTES
        adjusted = (steps[-1].duration_minutes or 0) + delta
        if adjusted < MIN_STEP_MINUTES:
            raise ValueError(
                "Cannot fit scheduled window with provided durations. "
                "Increase window or reduce durations."
            )
        steps[-1].duration_minutes = adjusted
        return

    remaining = total_minutes - known_total
    minimum_needed = MIN_STEP_MINUTES * len(missing)
    if remaining < minimum_needed:
        raise ValueError(
            "Scheduled window too short for step count and minimum duration. "
            "Increase change window or reduce steps."
        )

    weights = [complexity_weight(steps[idx].complexity) for idx in missing]
    weight_sum = sum(weights)

    provisional: list[int] = []
    remainders: list[tuple[float, int]] = []
    base_pool = remaining - minimum_needed

    for local_idx, global_idx in enumerate(missing):
        share = (base_pool * weights[local_idx]) / weight_sum if weight_sum else 0
        rounded = round_down_to_5(share) if strict_five_minute else int(share)
        provisional.append(MIN_STEP_MINUTES + rounded)
        remainders.append((share - rounded, global_idx))

    used = sum(provisional)
    leftover = remaining - used

    remainders.sort(reverse=True)
    pos = 0
    while leftover >= 5 and remainders:
        target_global_idx = remainders[pos % len(remainders)][1]
        target_local_idx = missing.index(target_global_idx)
        provisional[target_local_idx] += 5
        leftover -= 5
        pos += 1

    if leftover > 0:
        provisional[-1] += leftover

    for local_idx, global_idx in enumerate(missing):
        steps[global_idx].duration_minutes = provisional[local_idx]


def build_timeline(payload: dict[str, Any]) -> dict[str, Any]:
    scheduled_start = parse_datetime(payload["scheduled_start"])
    scheduled_end = parse_datetime(payload["scheduled_end"])
    if scheduled_end <= scheduled_start:
        raise ValueError("scheduled_end must be later than scheduled_start.")

    raw_steps = payload.get("steps", [])
    if not raw_steps:
        raise ValueError("At least one step is required.")

    steps: list[Step] = []
    for raw in raw_steps:
        impact = raw.get("service_impact", "No Outage")
        if impact not in ALLOWED_IMPACTS:
            raise ValueError(
                f"Invalid service_impact '{impact}'. Allowed: {sorted(ALLOWED_IMPACTS)}"
            )
        step = Step(
            section=str(raw.get("section", "")).strip(),
            description=str(raw.get("description", "")).strip(),
            owner=str(raw.get("owner", "")).strip(),
            service_impact=impact,
            complexity=str(raw.get("complexity", "normal")).strip() or "normal",
            duration_minutes=parse_duration_to_minutes(raw.get("duration")),
        )
        if not step.description:
            raise ValueError("Each step must include a non-empty description.")
        if not step.owner:
            raise ValueError("Each step must include owner.")
        steps.append(step)

    total_minutes = int((scheduled_end - scheduled_start).total_seconds() // 60)
    allocate_missing_durations(steps, total_minutes, strict_five_minute=True)

    cursor = scheduled_start
    for step in steps:
        duration = step.duration_minutes or MIN_STEP_MINUTES
        step.start = cursor
        step.end = cursor + timedelta(minutes=duration)
        cursor = step.end

    if cursor != scheduled_end:
        delta = int((scheduled_end - cursor).total_seconds() // 60)
        final = steps[-1]
        adjusted = (final.duration_minutes or MIN_STEP_MINUTES) + delta
        if adjusted < MIN_STEP_MINUTES:
            raise ValueError("Cannot close timeline exactly with current durations.")
        final.duration_minutes = adjusted
        final.end = final.start + timedelta(minutes=adjusted)
        cursor = final.end

    if cursor != scheduled_end:
        raise ValueError(
            "Timeline end does not match scheduled_end after reconciliation."
        )

    by_section: dict[str, int] = {}
    output_steps = []
    for step in steps:
        by_section[step.section] = by_section.get(step.section, 0) + 1
        output_steps.append(
            {
                "section": step.section,
                "step_number": by_section[step.section],
                "start": fmt_datetime(step.start),
                "duration": format_duration(step.duration_minutes or MIN_STEP_MINUTES),
                "description": step.description,
                "owner": step.owner,
                "service_impact": step.service_impact,
                "end": fmt_datetime(step.end),
                "line": (
                    f"Step {by_section[step.section]} - {fmt_datetime(step.start)} - "
                    f"{format_duration(step.duration_minutes or MIN_STEP_MINUTES)} - "
                    f"{step.description} - {step.owner} - {step.service_impact}"
                ),
            }
        )

    return {
        "scheduled_start": fmt_datetime(scheduled_start),
        "scheduled_end": fmt_datetime(scheduled_end),
        "total_minutes": total_minutes,
        "steps": output_steps,
        "timeline_ok": True,
    }


def read_payload(path: str | None) -> dict[str, Any]:
    if not path or path == "-":
        return json.load(fp=sys.stdin)
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def write_output(result: dict[str, Any], path: str | None, pretty: bool) -> None:
    content = json.dumps(result, indent=2 if pretty else None, ensure_ascii=False)
    if not path or path == "-":
        print(content)
        return
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(content)
        fh.write("\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build and validate a continuous timeline for Costa CR steps."
    )
    parser.add_argument(
        "--input",
        "-i",
        default="-",
        help="Input JSON file. Use '-' for stdin (default).",
    )
    parser.add_argument(
        "--output",
        "-o",
        default="-",
        help="Output JSON file. Use '-' for stdout (default).",
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty-print JSON output.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        payload = read_payload(args.input)
        result = build_timeline(payload)
        write_output(result, args.output, args.pretty)
    except Exception as exc:  # noqa: BLE001
        err = {"timeline_ok": False, "error": str(exc)}
        write_output(err, args.output, True)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
