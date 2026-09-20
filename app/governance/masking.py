from __future__ import annotations

from collections.abc import Mapping
from typing import Any

SENSITIVE_KEYS = {"password", "secret", "token", "api_key", "email", "phone", "customer_id"}


def mask_sensitive_data(payload: Any) -> Any:
    if isinstance(payload, Mapping):
        masked: dict[str, Any] = {}
        for key, value in payload.items():
            if key.lower() in SENSITIVE_KEYS:
                masked[key] = "***REDACTED***"
            else:
                masked[key] = mask_sensitive_data(value)
        return masked
    if isinstance(payload, list):
        return [mask_sensitive_data(item) for item in payload]
    return payload
