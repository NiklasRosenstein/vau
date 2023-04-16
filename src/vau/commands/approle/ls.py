from __future__ import annotations

from hvac.api.auth_methods.approle import AppRole  # type: ignore[import]
from rich import print
from typer import Option

from ._format import Format


def main(
    approle: AppRole,
    format: Format = Option(Format.default, "-o", "--format", help="Output format"),
    mount_point: str = Option("approle", help="Approle mount point"),
) -> None:
    """List vault app roles."""

    role_names: list[str] = approle.list_roles()["data"]["keys"]
    roles = {role_name: approle.read_role(role_name, mount_point=mount_point)["data"] for role_name in role_names}
    print(format.formatter.format_approles(roles))
