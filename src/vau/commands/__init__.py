from __future__ import annotations

from pathlib import Path
from sys import stderr

from hvac import Client  # type: ignore[import]
from rich import print
from typer import Option
from typer_builder import Dependencies

from vau.config import Config, VaultAlias

DEFAULT_CONFIG_FILE = Path.home() / ".config" / "vau" / "config.json"


def callback(
    use: str | None = Option(None, help="The vault alias to use", metavar="ALIAS"),
    vault_addr: str | None = Option(None, help="The address of the vault server", envvar="VAULT_ADDR", metavar="URL"),
    token: str | None = Option(None, help="The vault token", envvar="VAULT_TOKEN", metavar="TOKEN"),
    namespace: str
    | None = Option(
        None,
        help="The vault namespace",
        envvar="VAULT_NAMESPACE",
    ),
    config_file: Path = Option(DEFAULT_CONFIG_FILE, help="The config file", envvar="VAU_CONFIG_FILE"),
    dependencies: Dependencies = Dependencies.Provides(Client, Config, VaultAlias),
) -> None:
    if (use is not None) and (vault_addr is not None):
        print("[red]Cannot specify both --use and --vault-addr[/red]", file=stderr)
        exit(1)

    def get_config() -> Config:
        return Config.from_file(config_file)

    def get_vault_alias() -> VaultAlias:
        nonlocal use
        if use is not None or vault_addr is None:
            config = get_config()
            use = use or config.default_alias
            if not use:
                print("[red]No default vault alias specified[/red]", file=stderr)
                exit(1)
            if use not in config.aliases:
                print(f"[red]Unknown vault alias '{use}'[/red]", file=stderr)
                exit(1)
            return config.aliases[use]
        else:
            return VaultAlias(addr=vault_addr, token=token, namespace=namespace)

    def get_client() -> Client:
        alias = get_vault_alias()
        client = Client(url=alias.addr, token=token or alias.token, namespace=namespace or alias.namespace)
        if not client.is_authenticated():
            print("[red]Failed to authenticate with vault[/red]", file=stderr)
            exit(1)
        return client

    dependencies.set_supplier(Config, get_config)
    dependencies.set_supplier(VaultAlias, get_vault_alias)
    dependencies.set_supplier(Client, get_client)
