from pathlib import Path

import pytest

from taverenos.core import Rule, load_rules
from taverenos.core.knowledge_base import RuleValidationError


def test_load_rules_from_json(tmp_path: Path) -> None:
    rules_file = tmp_path / "rules.json"
    rules_file.write_text(
        """
        [
            {
                \"name\": \"diagnostic_rule\",
                \"description\": \"Detects anomalies\",
                \"conditions\": [\"signal > threshold\"],
                \"actions\": [\"raise_alert\"]
            }
        ]
        """
    )

    rules = load_rules(rules_file)

    assert len(rules) == 1
    assert isinstance(rules[0], Rule)
    assert rules[0].name == "diagnostic_rule"
    assert rules[0].conditions == ("signal > threshold",)
    assert rules[0].actions == ("raise_alert",)


def test_load_rules_requires_sequence(tmp_path: Path) -> None:
    rules_file = tmp_path / "invalid_rules.json"
    rules_file.write_text("{}")

    with pytest.raises(RuleValidationError):
        load_rules(rules_file)


def test_missing_file_raises(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        load_rules(tmp_path / "missing.json")
