from __future__ import annotations

from hvac.api.auth_methods.approle import AppRole  # type: ignore[import]
from rich import print
from typer import Option

from ._format import Format


def main(
    client: AppRole,
    format: Format = Option(Format.default, "-o", "--format", help="Output format"),
) -> None:
    """List vault app roles."""

    role_names: list[str] = client.list_roles()["data"]["keys"]
    roles = {role_name: client.read_role(role_name)["data"] for role_name in role_names}
    print(format.formatter.format_approles(roles))
