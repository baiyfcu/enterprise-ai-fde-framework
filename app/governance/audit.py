from __future__ import annotations

from typing import Literal

from app.models import AuditEvent


def build_audit_event(
    actor: str,
    action: str,
    resource: str,
    outcome: Literal["success", "failure"],
    **details: object,
) -> AuditEvent:
    return AuditEvent(
        actor=actor,
        action=action,
        resource=resource,
        outcome=outcome,
        details={key: value for key, value in details.items() if value is not None},
    )
