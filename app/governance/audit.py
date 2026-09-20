from __future__ import annotations

from app.models import AuditEvent


def build_audit_event(actor: str, action: str, resource: str, outcome: str, **details: object) -> AuditEvent:
    return AuditEvent(
        actor=actor,
        action=action,
        resource=resource,
        outcome=outcome,
        details={key: value for key, value in details.items() if value is not None},
    )
