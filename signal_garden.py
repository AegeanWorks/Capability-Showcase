#!/usr/bin/env python3
"""Turn a plain-text goal into a small, deterministic execution brief."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass

MAX_GOAL_CHARS = 10_000

RISK_TERMS = {
    "auth": "Authentication and authorization need explicit boundaries.",
    "payment": "Payment flows require idempotency and auditability.",
    "secret": "Secrets must stay outside source code and logs.",
    "delete": "Destructive operations need confirmation and recovery.",
    "migration": "Schema changes need a rollback strategy.",
    "network": "Network boundaries require timeouts, retries, and failure containment.",
    "concurrency": "Concurrent execution requires explicit synchronization and race avoidance.",
    "database": "State persistence requires data integrity, rollback safety, and atomicity.",
    "perf": "Performance paths require resource bounds and benchmark verification.",
    "privacy": "Personal or sensitive data handling requires redaction and retention boundaries.",
}

RISK_ALIASES = {
    "login": "auth",
    "token": "auth",
    "permission": "auth",
    "billing": "payment",
    "transaction": "payment",
    "password": "secret",
    "credential": "secret",
    "purge": "delete",
    "destroy": "delete",
    "schema": "migration",
    "http": "network",
    "api": "network",
    "remote": "network",
    "thread": "concurrency",
    "parallel": "concurrency",
    "async": "concurrency",
    "db": "database",
    "persist": "database",
    "sql": "database",
    "cache": "database",
    "scale": "perf",
    "speed": "perf",
    "latency": "perf",
    "pii": "privacy",
    "gdpr": "privacy",
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

    def to_markdown(self) -> str:
        lines = [
            f"# {self.title}",
            "",
            f"> **Effort**: `{self.effort}` | **Goal**: {self.goal}",
            "",
            self.summary,
            "",
            "### 🎯 Milestones",
        ]
        for index, milestone in enumerate(self.milestones, start=1):
            lines.append(f"- [ ] {index}. {milestone}")
        lines.append("")
        lines.append("### ⚠️ Identified Risks")
        for risk in self.risks:
            lines.append(f"- {risk}")
        return "\n".join(lines)

    def to_aikit_checkpoint(self, task_id: str = "showcase-task") -> str:
        risks_str = "; ".join(self.risks).replace('"', '\\"')
        return (
            f"python aikit.py checkpoint capability-showcase --task {task_id} "
            f'--phase-num 2 --desc "[1/4] {self.title}" '
            f'--why "{self.goal}" --benefits "{self.summary}" '
            f'--risks "{risks_str}" '
            '--mitigation "Follow the 4-phase milestone delivery with verified tests."'
        )


def _title(goal: str) -> str:
    words = re.findall(r"[A-Za-z0-9_-]+", goal)
    if not words:
        return "Untitled execution brief"
    selected = words[:8]
    first = selected[0]
    first_cap = first[:1].upper() + first[1:]
    return " ".join([first_cap, *selected[1:]])


def _tailor_milestones(lowered: str) -> tuple[str, ...]:
    has_auth = any(term in lowered for term in ("auth", "login", "permission"))
    has_payment = any(term in lowered for term in ("payment", "billing", "transaction"))
    has_data = any(term in lowered for term in ("data", "db", "database", "migration", "sql"))
    has_network = any(term in lowered for term in ("network", "api", "http", "remote"))
    has_perf = any(term in lowered for term in ("perf", "scale", "latency", "benchmark"))

    if has_auth:
        m1 = "Clarify authentication boundaries, access control, and success criteria."
    elif has_data:
        m1 = "Clarify data schema invariants, migration rollback, and success checks."
    else:
        m1 = "Clarify the outcome and define a measurable success check."

    if has_payment:
        m2 = "Implement the smallest vertical slice with idempotent handlers and failure safety."
    elif has_perf:
        m2 = "Implement the smallest vertical slice with resource-bounded execution."
    elif has_auth:
        m2 = "Implement the smallest vertical slice with explicit authorization gates."
    else:
        m2 = "Implement the smallest vertical slice with explicit failure handling."

    if has_network:
        m3 = "Exercise the happy path, network disconnects, and retry timeouts."
    elif has_auth:
        m3 = "Exercise the happy path, unauthorized requests, and credential boundaries."
    else:
        m3 = "Exercise the happy path and one meaningful edge case."

    m4 = "Document the usage and record the next improvement."
    return (m1, m2, m3, m4)


def build_brief(goal: str) -> Brief:
    """Build a bounded brief without network access or hidden state."""
    if len(goal) > MAX_GOAL_CHARS:
        raise ValueError(f"goal exceeds maximum allowed length of {MAX_GOAL_CHARS} characters")

    normalized = " ".join(goal.split())
    if not normalized:
        raise ValueError("goal must contain at least one non-whitespace character")

    lowered = normalized.lower()
    matched_keys: set[str] = set()
    for term in RISK_TERMS:
        if term in lowered:
            matched_keys.add(term)
    for alias, primary in RISK_ALIASES.items():
        if alias in lowered:
            matched_keys.add(primary)

    risks = tuple(RISK_TERMS[key] for key in sorted(matched_keys))
    milestones = _tailor_milestones(lowered)
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
    parser.add_argument("goal", nargs="*", default=[], help="the outcome you want to explore (or '-' for stdin)")
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    parser.add_argument("-m", "--markdown", action="store_true", help="emit GitHub Flavored Markdown brief")
    parser.add_argument("--aikit", action="store_true", help="emit an AIKit checkpoint plan command")
    parser.add_argument("--task-id", default="showcase-task", help="task identifier for AIKit checkpoint export")
    return parser


def _read_goal(args_goal: list[str]) -> str:
    if not args_goal or args_goal == ["-"]:
        if not sys.stdin.isatty():
            content = sys.stdin.read().strip()
            if content:
                return content
        if args_goal == ["-"]:
            return sys.stdin.read().strip()
    return " ".join(args_goal)


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        goal_text = _read_goal(args.goal)
        brief = build_brief(goal_text)
    except ValueError as error:
        print(
            f"Error: {error}\n"
            "Why: A goal must be a non-empty string under 10,000 characters.\n"
            'Fix: Provide a descriptive outcome, e.g.: python signal_garden.py "ship an auth service"',
            file=sys.stderr,
        )
        return 2

    if args.json:
        print(json.dumps(brief.as_dict(), indent=2))
        return 0

    if args.markdown:
        print(brief.to_markdown())
        return 0

    if args.aikit:
        print(brief.to_aikit_checkpoint(task_id=args.task_id))
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
