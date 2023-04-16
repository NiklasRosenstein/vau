from hvac.api.auth_methods.approle import AppRole  # type: ignore[import]
from rich import print
from typer import Option

from ._format import Format


def main(
    client: AppRole,
    role_name: str,
    format: Format = Option(Format.default, "-o", "--format", help="Output format"),
    mount_point: str = Option("approle", help="Approle mount point"),
) -> None:
    """Get a vault approle."""

    approle = client.read_role(role_name, mount_point=mount_point)["data"]
    print(format.formatter.format_approle(role_name, approle))
