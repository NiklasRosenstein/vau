from sys import stderr

from rich import print
from typer import Argument

from vau.config import Config


def main(
    alias: str = Argument(..., help="The alias to delete"),
    *,
    config: Config,
) -> None:
    """Delete a locally configured Vault alias."""

    if alias not in config.aliases:
        print(f"[red]Unknown alias '{alias}'[/red]", file=stderr)
        exit(1)

    del config.aliases[alias]
    if config.default_alias == alias:
        config.default_alias = None
    config.to_file()
