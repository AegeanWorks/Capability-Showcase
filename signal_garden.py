#!/usr/bin/env python3
"""Turn a plain-text goal into a small, deterministic execution brief."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass


RISK_TERMS = {
    "auth": "Authentication and authorization need explicit boundaries.",
    "payment": "Payment flows require idempotency and auditability.",
    "secret": "Secrets must stay outside source code and logs.",
    "delete": "Destructive operations need confirmation and recovery.",
    "migration": "Schema changes need a rollback strategy.",
}


@dataclass(frozen=True)
class Brief:
    goal: str
    title: str
    summary: str
    milestones: tuple[str, ...]
    risks: tuple[str, ...]
    effort: str

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


def _title(goal: str) -> str:
    words = re.findall(r"[A-Za-z0-9]+", goal)
    if not words:
        return "Untitled execution brief"
    return " ".join(words[:8]).capitalize()


def build_brief(goal: str) -> Brief:
    """Build a bounded brief without network access or hidden state."""
    normalized = " ".join(goal.split())
    if not normalized:
        raise ValueError("goal must contain at least one non-whitespace character")

    lowered = normalized.lower()
    risks = tuple(message for term, message in RISK_TERMS.items() if term in lowered)
    milestones = (
        "Clarify the outcome and define a measurable success check.",
        "Implement the smallest vertical slice with explicit failure handling.",
        "Exercise the happy path and one meaningful edge case.",
        "Document the usage and record the next improvement.",
    )
    effort = "focused" if len(normalized.split()) <= 12 else "expanded"
    return Brief(
        goal=normalized,
        title=_title(normalized),
        summary=f"Deliver a {effort} first slice for: {normalized}",
        milestones=milestones,
        risks=risks or ("No keyword risk detected; review assumptions before implementation.",),
        effort=effort,
    )


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Create a deterministic execution brief from a plain-text goal."
    )
    parser.add_argument("goal", nargs="+", help="the outcome you want to explore")
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        brief = build_brief(" ".join(args.goal))
    except ValueError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(brief.as_dict(), indent=2))
        return 0

    print(f"{brief.title} [{brief.effort}]")
    print(brief.summary)
    print("\nMilestones:")
    for index, milestone in enumerate(brief.milestones, start=1):
        print(f"  {index}. {milestone}")
    print("\nRisks:")
    for risk in brief.risks:
        print(f"  - {risk}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
