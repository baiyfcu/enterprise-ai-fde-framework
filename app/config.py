from __future__ import annotations

import os


def get_default_role() -> str:
    return os.getenv("DEFAULT_ROLE", "fde_admin")
