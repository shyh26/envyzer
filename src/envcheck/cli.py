from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from .core import compare

cli = typer.Typer()
console = Console()


@cli.command()
def check(
    base: Path = typer.Option(".env.example", help="Reference .env file"),
    files: list[Path] = typer.Argument(..., help=".env files to compare against base"),
) -> None:
    """Compare .env files against a reference."""
    diffs = compare(base, *files)

    if not diffs:
        console.print("[green]All environment variables match![/green]")
        return

    table = Table(title=f"Env Check: {base.name} vs {', '.join(f.name for f in files)}")
    table.add_column("Key", style="cyan")
    table.add_column("Issue", style="yellow")
    table.add_column(base.name)
    for f in files:
        table.add_column(f.name)

    for d in diffs:
        row = [d.key, _label(d.issue)]
        row.append(_val(d.values.get(base.name)))
        for f in files:
            row.append(_val(d.values.get(f.name)))
        table.add_row(*row)

    console.print(table)
    console.print(f"\n[red]{len(diffs)} issues found[/red]")


def _label(issue: str) -> str:
    return {"missing": "[red]MISSING[/red]", "extra": "[yellow]EXTRA[/yellow]",
            "mismatch": "[yellow]MISMATCH[/yellow]"}.get(issue, issue)


def _val(v: str | None) -> str:
    if v is None:
        return "[dim]—[/dim]"
    if len(v) > 40:
        return v[:37] + "..."
    return v


def main() -> None:
    cli()
