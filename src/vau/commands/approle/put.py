from __future__ import annotations

from enum import Enum
from itertools import chain
from typing import Iterable

from hvac.api.auth_methods.approle import AppRole  # type: ignore[import]
from rich import print
from typer import Argument, Option

from ._format import Format


def comma_flat_split(values: Iterable[str]) -> list[str]:
    """Split a comma-separated list of values into a flat list of values."""
    return list(chain.from_iterable(value.split(",") for value in values))


class TokenType(str, Enum):
    """The type of token."""

    SERVICE = "service"
    BATCH = "batch"
    DEFAULT = "default"
    DEFAULT_SERVICE = "default-service"
    DEFAULT_BATCH = "default-batch"


def main(
    role_name: str = Argument(..., help="The name of the role to create"),
    token_ttl: str = Option("1h", help="The TTL for the token"),
    token_max_ttl: str = Option("24h", help="The max TTL for the token"),
    policies: list[str] | None = Option(None, help="The policies for the token"),
    bind_secret_id: bool = Option(True, help="Whether to bind the secret ID"),
    secret_id_bound_cidrs: list[str] | None = Option(None, help="The CIDRs to bind the secret ID to"),
    secret_id_num_uses: int = Option(0, help="The number of uses for the secret ID"),
    secret_id_ttl: str = Option("1h", help="The TTL for the secret ID"),
    local_secret_ids: bool = Option(False, help="Whether to generate local secret IDs"),
    token_bound_cidrs: list[str] | None = Option(None, help="The CIDRs to bind the token to", metavar="CIDR"),
    token_explicit_max_ttl: str = Option("24h", help="The explicit max TTL for the token", metavar="DURATION"),
    token_no_default_policy: bool = Option(False, help='Whether the "default" policy will be added to the token'),
    token_num_uses: int = Option(0, help="The maximum number of times a token can be used"),
    token_period: str = Option(
        "24h", help="The maximum allowed period value when a periodic token is requested", metavar="DURATION"
    ),
    token_type: TokenType = Option(TokenType.DEFAULT, help="The type of token"),
    mount_point: str = Option("approle", help="The mount point for the AppRole auth method", metavar="MOUNT_POINT"),
    format: Format = Option(Format.default, "-o", "--format", help="Output format"),
    *,
    client: AppRole,
) -> None:
    """Create or update a vault approle."""

    client.create_or_update_approle(
        role_name=role_name,
        bind_secret_id=bind_secret_id,
        secret_id_bound_cidrs=comma_flat_split(secret_id_bound_cidrs or []),
        secret_id_num_uses=secret_id_num_uses,
        secret_id_ttl=secret_id_ttl,
        enable_local_secret_ids=local_secret_ids,
        token_ttl=token_ttl,
        token_max_ttl=token_max_ttl,
        token_policies=comma_flat_split(policies or []),
        token_bound_cidrs=comma_flat_split(token_bound_cidrs or []),
        token_explicit_max_ttl=token_explicit_max_ttl,
        token_no_default_policy=token_no_default_policy,
        token_num_uses=token_num_uses,
        token_period=token_period,
        token_type=token_type,
        mount_point=mount_point,
    )

    role = client.read_role(role_name, mount_point=mount_point)["data"]
    print(format.formatter.format_approle(role_name, role))
