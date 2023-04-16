from __future__ import annotations

from hvac.api.auth_methods.approle import AppRole  # type: ignore[import]
from rich import print
from typer import Context, Option


def main(
    client: AppRole,
    ctx: Context,
    secret_id: str | None = Option(None, help="The secret ID to remove", metavar="SECRET_ID"),
    accessor_id: str | None = Option(None, help="The accessor ID of the secret ID to remove", metavar="ACCESSOR_ID"),
) -> None:
    """
    Remove a secret ID from an AppRole by the secret ID or the accessor ID.

    Note that an attempt to remove a secret ID that does not exist will not result in an error.
    """

    role_name = ctx.ensure_object(str)

    if secret_id is not None and accessor_id is not None:
        print("[bold red]Cannot specify both --secret-id and --accessor-id[/bold red]")
        exit(1)

    if secret_id is not None:
        client.destroy_secret_id(role_name, secret_id)
        print(f"Removed secret ID [bold]{secret_id}[/bold] of AppRole [bold]{role_name}[/bold].")
    elif accessor_id is not None:
        client.destroy_secret_id_accessor(role_name, accessor_id)
        print(f"Removed secret ID accessed by [bold]{accessor_id}[/bold] of AppRole [bold]{role_name}[/bold].")
    else:
        print("[bold red]Must specify either --secret-id or --accessor-id[/bold red]")
        exit(1)
