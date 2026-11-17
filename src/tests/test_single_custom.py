"""Custom tests for Shape B (Single ReAct) by Nguyen Tuan Dung (2A202603859)."""

import pytest

from lab8.db import connect
from lab8.shapes.single import run_claim


def test_single_agent_rejects_ticket_delay_override(public_db):
    """C-002: Ticket says delay 5 days, order row says delay 2 days.

    The single agent must rely on DB order row and deny compensation.
    """
    result = run_claim("C-002", seed=55, store_path=str(public_db))
    assert result.status == "denied"
    assert result.proposal_amount == 0


def test_single_agent_missing_order_needs_info(public_db):
    result = run_claim("C-004", seed=11, store_path=str(public_db))
    assert result.status == "needs_info"
    assert result.proposal_amount == 0


def test_single_agent_step_budget_capped(public_db):
    """Single agent should finish well within max 8 steps."""
    result = run_claim("C-001", seed=11, store_path=str(public_db))
    assert result.status == "resolved"
    assert result.tool_calls <= 8
