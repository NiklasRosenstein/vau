from __future__ import annotations

import json
from pathlib import Path
from sys import stderr
from typing import Optional

from hvac.api.auth_methods.approle import AppRole  # type: ignore[import]
from rich import print
from typer import Context, Option

from .._format import SecretIdFormat
from .._utils import comma_flat_split

# NOTE(@NiklasRosenstein): We're using `Optional[str]` instead of `str | None` here because of a Black formatting
#       bug described in https://github.com/psf/black/issues/3649.

# NOTE(@NiklasRosenstein): It appears that `num_uses` and `ttl` is not currently supported by hvac.


def main(
    client: AppRole,
    ctx: Context,
    secret_id: Optional[str] = Option(
        None,
        help="A custom secret ID to use. If not specified, one will be generated.",
        metavar="SECRET_ID",
    ),
    metadata: Optional[str] = Option(
        None, help="JSON-formatted metadata to associate with the secret ID", metavar="JSON"
    ),
    metadata_file: Optional[Path] = Option(
        None,
        help="A file containing JSON-formatted metadata to associate with the secret ID",
    ),
    cidr: list[str] | None = Option(None, help="The CIDRs to bind the secret ID to", metavar="CIDR"),
    token_bound_cidrs: list[str] | None = Option(None, help="The CIDRs to bind the token to", metavar="CIDR"),
    format: SecretIdFormat = Option(SecretIdFormat.json, "-o", "--format", help="Output format"),
) -> None:
    """
    Create a new secret ID for an AppRole.
    """

    role_name = ctx.ensure_object(str)

    if metadata_file is not None:
        if metadata is not None:
            print("Cannot specify both --metadata and --metadata-file", file=stderr)
            exit(1)
        metadata_json = json.loads(metadata_file.read_text())
    else:
        metadata_json = json.loads(metadata or "{}")

    if secret_id is None:
        secretid = client.generate_secret_id(
            role_name,
            metadata=metadata_json,
            cidr_list=comma_flat_split(cidr or []),
            token_bound_cidrs=comma_flat_split(token_bound_cidrs or []),
        )["data"]
    else:
        secretid = client.create_custom_secret_id(
            role_name=role_name,
            secret_id=secret_id,
            metadata=metadata_json,
            cidr_list=comma_flat_split(cidr or []),
            token_bound_cidrs=comma_flat_split(token_bound_cidrs or []),
        )["data"]

    print(format.formatter.format_secretid(secretid))
