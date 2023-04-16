from hvac.api.auth_methods.approle import AppRole  # type: ignore[import]
from rich import print
from typer import Option

from ._format import ApproleFormat


def main(
    client: AppRole,
    role_name: str = Option(..., help="The name of the approle", metavar="ROLE_NAME"),
    format: ApproleFormat = Option(ApproleFormat.json, "-o", "--format", help="Output format"),
) -> None:
    """Get a vault approle."""

    approle = client.read_role(role_name)["data"]
    print(format.formatter.format_approle(approle))
