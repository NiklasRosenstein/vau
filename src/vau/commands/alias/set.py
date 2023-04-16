from __future__ import annotations

from typer import Argument, Option

from vau.config import Config, VaultAlias


def main(
    alias: str = Argument(..., help="The alias to create or update"),
    vault_addr: str = Option(..., help="The address of the vault server"),
    token: str | None = Option(None, help="The vault token"),
    namespace: str | None = Option(None, help="The vault namespace"),
    use: bool = Option(False, help="Use the alias after creating it"),
    *,
    config: Config,
) -> None:
    """Create or update a locally configured Vault alias."""

    config.aliases[alias] = VaultAlias(addr=vault_addr, token=token, namespace=namespace)
    if use:
        config.default_alias = alias
    config.to_file()
