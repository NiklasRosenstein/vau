"""
Remove an AppRole from vault.
"""

from hvac.api.auth_methods.approle import AppRole  # type: ignore[import]
from rich import print
from typer import Option


def main(client: AppRole, role_name: str, mount_point: str = Option("approle", help="Approle mount point")) -> None:
    """Remove a vault approle."""

    client.delete_role(role_name, mount_point=mount_point)
    print(f"Removed approle {role_name}")
