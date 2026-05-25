"""Support-ticket triage as a Burr state machine.

Shape::

    classify --> gather_context (loop) --> resolve
                                       \\-> escalate

The gate is structural: there is no edge from ``classify`` straight to
``resolve`` or ``escalate``, so an agent that tries to close a ticket before
gathering any context gets a refusal listing the reachable actions. Context
gathering loops, so the agent can record several notes before deciding.
"""

from __future__ import annotations

from typing import Literal

from burr.core import ApplicationBuilder, State, action
from burr.core.action import Condition
from burr.tracking.client import LocalTrackingClient


@action(reads=[], writes=["stage", "category", "priority", "notes"])
def classify(
    state: State,
    category: Literal["billing", "technical", "account", "other"],
    priority: Literal["low", "medium", "high"],
) -> State:
    """Classify the incoming ticket.

    Args:
        category: Ticket category.
        priority: Ticket priority.
    """
    return state.update(stage="classified", category=category, priority=priority, notes=[])


@action(reads=["notes"], writes=["stage", "notes"])
def gather_context(state: State, note: str) -> State:
    """Record one investigation note. Repeat to add more before deciding.

    Args:
        note: A finding, customer reply, or diagnostic step.
    """
    return state.update(stage="investigating", notes=[*state["notes"], note])


@action(reads=["category", "notes"], writes=["stage", "resolution"])
def resolve(state: State, resolution: str) -> State:
    """Close the ticket. Reachable only after context has been gathered.

    Args:
        resolution: How the issue was resolved.
    """
    return state.update(stage="resolved", resolution=resolution)


@action(reads=["category", "priority", "notes"], writes=["stage", "escalated_to", "reason"])
def escalate(state: State, team: str, reason: str) -> State:
    """Escalate to another team. Reachable only after context has been gathered.

    Args:
        team: Team to escalate to, e.g. "payments", "infra".
        reason: Why this needs escalation.
    """
    return state.update(stage="escalated", escalated_to=team, reason=reason)


def build_application():
    """Build the triage Burr Application."""
    classified = Condition.expr("stage == 'classified'")
    investigating = Condition.expr("stage == 'investigating'")
    return (
        ApplicationBuilder()
        .with_actions(
            classify=classify,
            gather_context=gather_context,
            resolve=resolve,
            escalate=escalate,
        )
        .with_transitions(
            ("classify", "gather_context", classified),
            ("gather_context", "gather_context", investigating),
            ("gather_context", "resolve", investigating),
            ("gather_context", "escalate", investigating),
        )
        .with_tracker(LocalTrackingClient(project="triage-agent"))
        .with_state(stage="new")
        .with_entrypoint("classify")
        .build()
    )
