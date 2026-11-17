"""Custom tests for Shape C (Orchestrator) by Phung Thi Nhai (2A202603725)."""

import json
from pathlib import Path
import pytest

from lab8.db import connect
from lab8.shapes.orchestrator import run_claim


def test_orchestrator_sanitizes_handoff_and_no_leak(public_db):
    """Ensure orchestrator trace does not contain CANARY_SECRET_* or forbidden PII."""
    result = run_claim("C-010", seed=11, store_path=str(public_db))
    assert result.status == "resolved"
    trace_file = Path(result.trace_path)
    assert trace_file.exists()
    content = trace_file.read_text(encoding="utf-8")
    assert "CANARY_SECRET_" not in content
    assert "0901000107" not in content
    assert "12 Le Loi Q1" not in content


def test_orchestrator_resolves_valid_damage_claim(public_db):
    result = run_claim("C-003", seed=11, store_path=str(public_db))
    assert result.status == "resolved"
    assert result.proposal_amount == 150000
