from __future__ import annotations

from itertools import chain
from typing import Iterable


def comma_flat_split(values: Iterable[str]) -> list[str]:
    """Split a comma-separated list of values into a flat list of values."""
    return list(chain.from_iterable(value.split(",") for value in values))
