"""Automation hooks for ritual orchestration."""

from dataclasses import dataclass
from datetime import datetime
from typing import Mapping, Sequence


@dataclass
class RitualInstruction:
    """Instruction payload to be sent to a ritual automation interface."""

    ritual_id: str
    parameters: Mapping[str, float]
    scheduled_for: datetime
    safety_checks: Sequence[str]


__all__ = ["RitualInstruction"]
