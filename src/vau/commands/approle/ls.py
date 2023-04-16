from __future__ import annotations

from hvac.api.auth_methods.approle import AppRole  # type: ignore[import]
from typer import Option

from . import list_roles
from ._format import ApproleListFormat


def main(
    client: AppRole,
    format: ApproleListFormat = Option(ApproleListFormat.table, "-o", "--format", help="Output format"),
) -> None:
    """List vault app roles."""

    roles = list_roles(client)
    print(format.formatter.format_approles(roles))
