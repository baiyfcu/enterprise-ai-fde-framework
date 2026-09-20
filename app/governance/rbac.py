from __future__ import annotations

from app.models import RoleBinding


ROLE_PERMISSIONS: dict[str, list[str]] = {
    "fde_admin": ["workflow:run", "tool:query", "tool:create", "audit:read"],
    "solution_architect": ["workflow:run", "tool:query", "audit:read"],
    "analyst": ["workflow:run", "tool:query"],
}


def resolve_role_binding(role: str = "fde_admin") -> RoleBinding:
    permissions = ROLE_PERMISSIONS.get(role, ROLE_PERMISSIONS["analyst"])
    return RoleBinding(role=role if role in ROLE_PERMISSIONS else "analyst", permissions=permissions)
