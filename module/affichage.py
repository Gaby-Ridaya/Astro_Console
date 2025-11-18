from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

def afficher_ascendant_mc(theme):
    table = Table(title="[bold blue]Ascendant & MC[/bold blue]", title_style="bold blue")
    table.add_column("Type", style="bold yellow")
    table.add_column("Position", style="bold cyan")
    table.add_row("Ascendant", f"[green]{theme['ascendant']}[/green]")
    table.add_row("MC", f"[green]{theme['mc']}[/green]")
    console.print(table)

def afficher_maisons(maisons):
    table = Table(title="[bold magenta]Maisons[/bold magenta]", title_style="bold magenta")
    table.add_column("Maison", style="bold yellow")
    table.add_column("Position", style="bold cyan")
    for nom, position in maisons:
        table.add_row(f"[yellow]{nom}[/yellow]", f"[green]{position}[/green]")
    console.print(table)

def afficher_planetes(planetes):
    table = Table(title="[bold green]Planètes[/bold green]", title_style="bold green")
    table.add_column("Planète", style="bold yellow")
    table.add_column("Position", style="bold cyan")
    for nom, position in planetes:
        table.add_row(f"[yellow]{nom}[/yellow]", f"[cyan]{position}[/cyan]")
    console.print(table)

def afficher_rahu_ketu(noeuds):
    table = Table(title="[bold red]Rahu & Ketu[/bold red]", title_style="bold red")
    table.add_column("Noeud", style="bold yellow")
    table.add_column("Position", style="bold cyan")
    table.add_row("Rahu", f"[magenta]{noeuds['Rahu']}[/magenta]")
    table.add_row("Ketu", f"[magenta]{noeuds['Ketu']}[/magenta]")
    console.print(table)

def afficher_aspects(aspects):
    table = Table(title="[bold cyan]Aspects[/bold cyan]", title_style="bold cyan")
    table.add_column("Planètes", style="bold yellow")
    table.add_column("Aspect", style="bold green")
    table.add_column("Angle", style="bold magenta")
    for aspect in aspects:
        table.add_row(f"[yellow]{aspect['planetes']}[/yellow]", f"[green]{aspect['aspect']}[/green]", f"[magenta]{aspect['angle']}°[/magenta]")
    console.print(table)
