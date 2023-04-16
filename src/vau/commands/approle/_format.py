from __future__ import annotations

import builtins
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from functools import partial
from io import StringIO
from typing import Any

from rich.console import Console
from rich.table import Table


class Formatter(ABC):
    """
    Abstract base class for formatting approles.
    """

    @abstractmethod
    def format_approle(self, role_name: str, approle: dict[str, Any]) -> str:
        ...

    def format_approles(self, approles: dict[str, dict[str, Any]]) -> str:
        buffer = StringIO()
        print = partial(builtins.print, file=buffer)
        for role_name, approle in approles.items():
            print(self.format_approle(role_name, approle))
        return buffer.getvalue().rstrip()


@dataclass
class DefaultFormatter(Formatter):
    """
    Default formatter for approles.
    """

    def _fmt_value(self, value: Any) -> str:
        if isinstance(value, list):
            return repr(value)
        elif isinstance(value, bool):
            return str(value).lower()
        elif value is None:
            return "null"
        else:
            return repr(value)

    def _add_approle_to_rich_table(self, table: Table, role_name: str, approle: dict[str, Any]) -> None:
        table.add_row(
            role_name,
            self._fmt_value(approle["token_ttl"]),
            self._fmt_value(approle["token_max_ttl"]),
            self._fmt_value(approle["token_policies"]),
            self._fmt_value(approle["bind_secret_id"]),
            self._fmt_value(approle["secret_id_bound_cidrs"]),
            self._fmt_value(approle["secret_id_num_uses"]),
            self._fmt_value(approle["secret_id_ttl"]),
            self._fmt_value(approle["local_secret_ids"]),
            self._fmt_value(approle["token_bound_cidrs"]),
            self._fmt_value(approle["token_explicit_max_ttl"]),
            self._fmt_value(approle["token_no_default_policy"]),
            self._fmt_value(approle["token_num_uses"]),
            self._fmt_value(approle["token_period"]),
            self._fmt_value(approle["token_type"]),
        )

    def format_approle(self, role_name: str, approle: dict[str, Any]) -> str:
        rows = [("Key", "Value")]
        for key in sorted(approle):
            rows.append((key, self._fmt_value(approle[key])))
        max_width = max(len(key) for key, _ in rows)
        return "\n".join(f"{key:<{max_width}} {value}" for key, value in rows)

    def format_approles(self, approles: dict[str, dict[str, Any]]) -> str:
        table = Table()
        table.add_column("Role Name")
        table.add_column("Token Policies")
        table.add_column("Token TTL")
        table.add_column("Token Type")

        for role_name, approle in approles.items():
            table.add_row(
                role_name,
                self._fmt_value(approle["token_policies"]),
                self._fmt_value(approle["token_ttl"]),
                self._fmt_value(approle["token_type"]),
            )

        buffer = StringIO()
        Console(file=buffer).print(table)
        return buffer.getvalue().rstrip()


class JsonFormatter(Formatter):
    def format_approle(self, role_name: str, approle: dict[str, Any]) -> str:
        return json.dumps(approle, indent=2)

    def format_approles(self, approles: dict[str, dict[str, Any]]) -> str:
        return json.dumps(approles, indent=2)


class Format(str, Enum):
    default = "default"
    full = "full"
    json = "json"

    @property
    def formatter(self) -> Formatter:
        if self == Format.default:
            return DefaultFormatter()
        elif self == Format.json:
            return JsonFormatter()
        else:
            raise ValueError(f"Unknown formatter: {self}")
