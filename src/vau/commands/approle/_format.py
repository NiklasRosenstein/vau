from __future__ import annotations

import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from io import StringIO
from typing import Any

from rich.console import Console
from rich.table import Table


def _fmt_value(value: Any) -> str:
    if isinstance(value, bool):
        return str(value).lower()
    if value is None:
        return "null"
    return repr(value)


###
# ApproleFormatter


class ApproleFormatter(ABC):
    """
    Abstract base class for formatting approles.
    """

    @abstractmethod
    def format_approle(self, approle: dict[str, Any]) -> str:
        ...


@dataclass
class ApproleJsonFormatter(ApproleFormatter):
    indent: int = 2
    sort_keys: bool = True

    def format_approle(self, approle: dict[str, Any]) -> str:
        return json.dumps(approle, indent=self.indent, sort_keys=self.sort_keys)


class ApproleFormat(str, Enum):
    json = "json"

    @property
    def formatter(self) -> ApproleFormatter:
        if self == ApproleFormat.json:
            return ApproleJsonFormatter()
        else:
            raise ValueError(f"Unknown formatter: {self}")


###
# ApproleListFormatter


class ApproleListFormatter(ABC):
    @abstractmethod
    def format_approles(self, approles: list[dict[str, Any]]) -> str:
        ...


@dataclass
class ApproleListJsonFormatter(ApproleListFormatter):
    indent: int = 2
    sort_keys: bool = True

    def format_approles(self, approles: list[dict[str, Any]]) -> str:
        return json.dumps(approles, indent=self.indent, sort_keys=self.sort_keys)


class ApproleListTableFormatter(ApproleListFormatter):
    def format_approles(self, approles: list[dict[str, Any]]) -> str:
        table = Table()
        table.add_column("Role Name")
        table.add_column("Role ID")
        table.add_column("Token Policies")
        table.add_column("Token TTL")
        table.add_column("Token Type")

        for approle in approles:
            table.add_row(
                approle["role_name"],
                approle["role_id"],
                _fmt_value(approle["token_policies"]),
                _fmt_value(approle["token_ttl"]),
                approle["token_type"],
            )

        buffer = StringIO()
        Console(file=buffer).print(table)
        return buffer.getvalue().rstrip()


class ApproleListFormat(str, Enum):
    table = "table"
    json = "json"

    @property
    def formatter(self) -> ApproleListFormatter:
        if self == ApproleListFormat.table:
            return ApproleListTableFormatter()
        elif self == ApproleListFormat.json:
            return ApproleListJsonFormatter()
        else:
            raise ValueError(f"Unknown formatter: {self}")


###
# SecretIdFormatter


class SecretIdFormatter(ABC):
    @abstractmethod
    def format_secretid(self, secretid: dict[str, Any]) -> str:
        ...


class SecretIdJsonFormatter(SecretIdFormatter):
    indent: int = 2
    sort_keys: bool = True

    def format_secretid(self, secretid: dict[str, Any]) -> str:
        return json.dumps(secretid, indent=self.indent, sort_keys=self.sort_keys)


class SecretIdFormat(str, Enum):
    json = "json"

    @property
    def formatter(self) -> SecretIdFormatter:
        if self == SecretIdFormat.json:
            return SecretIdJsonFormatter()
        else:
            raise ValueError(f"Unknown formatter: {self}")


###
# SecretIdAccessorListFormatter


class SecretIdAccessorListFormatter(ABC):
    @abstractmethod
    def format_secretidaccessors(self, secretidaccessors: list[dict[str, Any]]) -> str:
        ...


@dataclass
class SecretIdAccessorListJsonFormatter(SecretIdAccessorListFormatter):
    indent: int = 2
    sort_keys: bool = True

    def format_secretidaccessors(self, secretidaccessors: list[dict[str, Any]]) -> str:
        return json.dumps(secretidaccessors, indent=self.indent, sort_keys=self.sort_keys)


class SecretIdAccessorListTableFormatter(SecretIdAccessorListFormatter):
    def format_secretidaccessors(self, secretidaccessors: list[dict[str, Any]]) -> str:
        table = Table()
        table.add_column("Secret Accessor ID")
        table.add_column("Creation Time")
        table.add_column("Expiration Time")
        table.add_column("Metadata")

        for secretidaccessor in secretidaccessors:
            table.add_row(
                secretidaccessor["accessor_id"],
                secretidaccessor["creation_time"],
                secretidaccessor["expiration_time"],
                json.dumps(secretidaccessor["metadata"]),
            )

        buffer = StringIO()
        Console(file=buffer).print(table)
        return buffer.getvalue().rstrip()


class SecretIdAccessorListFormat(str, Enum):
    table = "table"
    json = "json"

    @property
    def formatter(self) -> SecretIdAccessorListFormatter:
        if self == SecretIdAccessorListFormat.table:
            return SecretIdAccessorListTableFormatter()
        elif self == SecretIdAccessorListFormat.json:
            return SecretIdAccessorListJsonFormatter()
        else:
            raise ValueError(f"Unknown formatter: {self}")
