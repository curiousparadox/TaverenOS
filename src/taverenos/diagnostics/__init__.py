"""Diagnostics module placeholders for TaverenOS."""

from dataclasses import dataclass
from typing import Iterable, Sequence

from taverenos.core import Rule


@dataclass
class DiagnosticResult:
    """Structured diagnostic recommendation produced by rule evaluation."""

    triggered_rules: Sequence[Rule]
    notes: Sequence[str]


def summarise(results: Iterable[DiagnosticResult]) -> Sequence[str]:
    """Create a human-readable summary from diagnostic results."""

    summary: list[str] = []
    for result in results:
        rule_names = ", ".join(rule.name for rule in result.triggered_rules)
        summary.append(f"Rules: {rule_names} | Notes: {'; '.join(result.notes)}")
    return summary


__all__ = ["DiagnosticResult", "summarise"]
