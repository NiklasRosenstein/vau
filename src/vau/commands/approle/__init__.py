from hvac import Client  # type: ignore[import]
from hvac.api.auth_methods.approle import AppRole  # type: ignore[import]
from hvac.constants.approle import DEFAULT_MOUNT_POINT  # type: ignore[import]
from typer import Option
from typer_builder import Dependencies

from vau.reflection import Reflection


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

    dependencies.set(AppRole, refl.into(AppRole))
