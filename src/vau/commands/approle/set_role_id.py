from hvac.api.auth_methods.approle import AppRole  # type: ignore[import]
from rich import print
from typer import Argument, Option

from ._format import Format


def main(
    role_name: str = Argument(..., help="The name of the role to update the role ID of", metavar="ROLE_NAME"),
    role_id: str = Argument(..., help="The new role ID for the role", metavar="ROLE_ID"),
    format: Format = Option(Format.default, "-o", "--format", help="Output format"),
    *,
    client: AppRole,
) -> None:
    """Update the role ID of an approle."""

    client.update_role_id(role_name, role_id)
    role = client.read_role(role_name)["data"]
    print(format.formatter.format_approle(role_name, role))
