from __future__ import annotations

from enum import Enum
from typing import Optional

from hvac.api.auth_methods.approle import AppRole  # type: ignore[import]
from rich import print
from typer import Option

from ._format import ApproleFormat
from ._utils import comma_flat_split


class TokenType(str, Enum):
    """The type of token."""

    service = "service"
    batch = "batch"
    default = "default"
    default_service = "default-service"
    default_batch = "default-batch"


def main(
    client: AppRole,
    role_name: str = Option(..., help="The name of the role to create", metavar="ROLE_NAME"),
    role_id: Optional[str] = Option(
        None, help="A custom role ID to use. If not specified, one will be generated.", metavar="ROLE_ID"
    ),
    token_ttl: str = Option("1h", help="The TTL for the token", metavar="DURATION"),
    token_max_ttl: str = Option("24h", help="The max TTL for the token", metavar="DURATION"),
    policies: list[str] | None = Option(None, help="The policies for the token"),
    bind_secret_id: bool = Option(True, help="Whether to bind the secret ID"),
    secret_id_bound_cidrs: list[str] | None = Option(None, help="The CIDRs to bind the secret ID to", metavar="CIDR"),
    secret_id_num_uses: int = Option(0, help="The number of uses for the secret ID"),
    secret_id_ttl: str = Option("1h", help="The TTL for the secret ID", metavar="DURATION"),
    local_secret_ids: bool = Option(False, help="Whether to generate local secret IDs"),
    token_bound_cidrs: list[str] | None = Option(None, help="The CIDRs to bind the token to", metavar="CIDR"),
    token_explicit_max_ttl: str = Option("24h", help="The explicit max TTL for the token", metavar="DURATION"),
    token_no_default_policy: bool = Option(False, help='Whether the "default" policy will be added to the token'),
    token_num_uses: int = Option(0, help="The maximum number of times a token can be used"),
    token_period: str = Option(
        "24h", help="The maximum allowed period value when a periodic token is requested", metavar="DURATION"
    ),
    token_type: TokenType = Option(TokenType.default, help="The type of token"),
    format: ApproleFormat = Option(ApproleFormat.json, "-o", "--format", help="Output format"),
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
    )

    if role_id is not None:
        client.update_role_id(role_name, role_id)

    approle = client.read_role(role_name)["data"]
    print(format.formatter.format_approle(approle))
