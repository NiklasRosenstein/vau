"""
Remove an AppRole from vault.
"""

from hvac.api.auth_methods.approle import AppRole  # type: ignore[import]
from rich import print


def main(client: AppRole, role_name: str) -> None:
    """Remove a vault approle."""

    client.delete_role(role_name)
    print(f"Removed approle {role_name}")
