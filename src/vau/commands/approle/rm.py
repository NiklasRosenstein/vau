"""
Remove an AppRole from vault.
"""

from hvac.api.auth_methods.approle import AppRole  # type: ignore[import]
from rich import print
from typer import Option


def main(approle: AppRole, role_name: str, mount_point: str = Option("approle", help="Approle mount point")) -> None:
    """Remove a vault approle."""

    approle.delete_role(role_name, mount_point=mount_point)
    print(f"Removed approle {role_name}")
