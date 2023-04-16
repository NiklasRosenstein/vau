"""
Set the default vault alias to use.
"""

from sys import stderr

from rich import print
from typer import Argument

from vau.config import Config


def main(
    alias: str = Argument(..., help="The alias to set as default"),
    *,
    config: Config,
) -> None:
    """Set the default vault alias to use."""

    if alias not in config.aliases:
        print(f"[red]Unknown vault alias '{alias}'[/red]", file=stderr)
        exit(1)
    config.default_alias = alias
    config.to_file()
