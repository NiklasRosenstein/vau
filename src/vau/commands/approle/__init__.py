"""
Manage AppRoles.

AppRoles are a way to authenticate against Vault. They are similar to AWS IAM roles.
"""

from __future__ import annotations

from typing import Any

from hvac import Client  # type: ignore[import]
from hvac.api.auth_methods.approle import AppRole  # type: ignore[import]
from hvac.constants.approle import DEFAULT_MOUNT_POINT  # type: ignore[import]
from typer import Option
from typer_builder import Dependencies

from vau.reflection import Reflection

# NOTE(@NiklasRosenstein): Details on the AppRole API can be found here:
#       https://developer.hashicorp.com/vault/api-docs/auth/approle


def callback(
    client: Client,
    dependencies: Dependencies = Dependencies.Provides(AppRole),
    mount_point: str = Option(DEFAULT_MOUNT_POINT, help="Approle mount point", metavar="MOUNT_POINT"),
) -> None:
    # Inject the mount_point option as default value into all methods of the approle object that accept it.
    refl = Reflection(client.auth.approle)
    for method in refl.methods():
        if "mount_point" in method.signature.parameters:
            method.kwargs["mount_point"] = mount_point

    # Ensure that read_role() returns the role id as well.
    method = refl.method("read_role")

    @method.wrapper
    def _read_role(role_name: str, **kwargs: Any) -> dict[str, str]:
        role = method.original(role_name, **kwargs)
        role_id = client.auth.approle.read_role_id(role_name, **kwargs)["data"]["role_id"]
        role["data"]["role_name"] = role_name
        role["data"]["role_id"] = role_id
        return role  # type: ignore[no-any-return]

    dependencies.set(AppRole, refl.into(AppRole))


def list_roles(client: AppRole) -> list[dict[str, Any]]:
    """
    List all vault app roles and their role ids.
    """

    role_names: list[str] = client.list_roles()["data"]["keys"]
    return [
        {
            **client.read_role(role_name)["data"],
            "role_name": role_name,
            "role_id": client.read_role_id(role_name)["data"]["role_id"],
        }
        for role_name in role_names
    ]
