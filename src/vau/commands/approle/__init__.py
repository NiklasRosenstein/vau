from hvac import Client  # type: ignore[import]
from hvac.api.auth_methods.approle import AppRole  # type: ignore[import]
from typer_builder import Dependencies


def callback(client: Client, dependencies: Dependencies = Dependencies.Provides(AppRole)) -> None:
    approle: AppRole = client.auth.approle
    dependencies.set(AppRole, approle)
