from hvac.api.auth_methods.approle import AppRole  # type: ignore[import]
from rich import print
from typer import Context, Option


def main(
    client: AppRole,
    ctx: Context,
    role_id: str = Option(..., help="The new role ID for the role", metavar="ROLE_ID"),
) -> None:
    """Update the role ID of an approle."""

    role_name = ctx.ensure_object(str)
    client.update_role_id(role_name, role_id)
    print(f"Updated role ID for role [bold blue]{role_name}[/bold blue] to '{role_id}'.")
