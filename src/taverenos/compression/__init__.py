"""Compression utilities for energetic emission vectors (EEVs)."""

from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class CompressionArtifact:
    """Represents the output of an EEV compression pipeline."""

    method: str
    checksum: str
    payload: Sequence[float]


__all__ = ["CompressionArtifact"]
