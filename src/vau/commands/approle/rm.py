"""
Remove an AppRole from vault.
"""

from hvac.api.auth_methods.approle import AppRole  # type: ignore[import]
from rich import print
from typer import Option


def main(
    client: AppRole,
    role_name: str = Option(..., help="The name of the approle", metavar="ROLE_NAME"),
) -> None:
    """
    Remove a vault AppRole.

    Note that removing an AppRole that does not exist will not result in an error.
    """

    client.delete_role(role_name)
    print(f"Removed AppRole [bold]{role_name}[/bold].")
