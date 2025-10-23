"""Utilities for loading symbolic rule definitions."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Sequence


@dataclass(frozen=True)
class Rule:
    """Represents a single symbolic rule definition.

    Attributes:
        name: Unique identifier for the rule.
        description: Human-readable summary of the rule purpose.
        conditions: Sequence of condition expressions.
        actions: Sequence of actions triggered when conditions are met.
    """

    name: str
    description: str
    conditions: Sequence[str]
    actions: Sequence[str]


class RuleValidationError(ValueError):
    """Raised when a rule definition is invalid."""


def _normalise_rule(raw_rule: Dict[str, Any]) -> Rule:
    try:
        name = raw_rule["name"]
        description = raw_rule.get("description", "")
        raw_conditions = raw_rule.get("conditions", ())
        raw_actions = raw_rule.get("actions", ())
    except KeyError as exc:  # pragma: no cover - defensive branch
        raise RuleValidationError(f"Missing required key: {exc.args[0]}") from exc

    if not isinstance(name, str) or not name:
        raise RuleValidationError("Rule name must be a non-empty string")

    for field_name, value in ("conditions", raw_conditions), ("actions", raw_actions):
        if isinstance(value, str):
            raise RuleValidationError(f"{field_name} must be a sequence of strings")
        if not isinstance(value, Sequence):
            raise RuleValidationError(f"{field_name} must be a sequence of strings")
        if not all(isinstance(item, str) for item in value):
            raise RuleValidationError(f"{field_name} must contain only strings")

    conditions = tuple(raw_conditions)
    actions = tuple(raw_actions)

    return Rule(name=name, description=str(description), conditions=conditions, actions=actions)


def load_rules(source: Path | str) -> List[Rule]:
    """Load rules from a JSON file on disk.

    The loader performs lightweight validation to ensure each rule contains the
    fields required by the core reasoning loop.
    """

    path = Path(source)
    if not path.exists():
        raise FileNotFoundError(f"Rule file not found: {path}")

    data = json.loads(path.read_text())
    if not isinstance(data, (list, tuple)):
        raise RuleValidationError("Rule file must contain a list of rules")

    rules: List[Rule] = []
    for index, raw_rule in enumerate(data):
        if not isinstance(raw_rule, Dict):
            raise RuleValidationError(f"Rule at index {index} is not an object")
        rules.append(_normalise_rule(raw_rule))

    return rules


__all__ = ["Rule", "RuleValidationError", "load_rules"]
