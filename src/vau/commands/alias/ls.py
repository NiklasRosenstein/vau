from __future__ import annotations

from rich.console import Console
from rich.table import Table
from typer import Option

from vau.config import Config


def main(
    show_tokens: bool = Option(False, help="Show tokens in the table"),
    *,
    config: Config,
) -> None:
    """
    List all aliases in a rich table.
    """

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Alias", style="dim", width=12)
    table.add_column("Vault Address", style="dim")
    table.add_column("Token", style="dim")
    table.add_column("Namespace", style="dim")

    for alias, details in config.aliases.items():
        table.add_row(
            f"[bold green]{alias}[/bold green]" if alias == config.default_alias else alias,
            details.addr,
            details.token if show_tokens else "********" if details.token else "",
            details.namespace or "-",
        )

    console = Console()
    console.print(table)
