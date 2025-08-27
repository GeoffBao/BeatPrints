"""Public API for the BeatPrints package.

Avoid importing heavy submodules at import time to improve startup performance.
"""

from importlib import import_module
from typing import Any

__all__ = ["spotify", "lyrics", "poster", "errors"]

_SUBMODULES = set(__all__)


def __getattr__(name: str) -> Any:
    if name in _SUBMODULES:
        return import_module(f".{name}", __name__)
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
