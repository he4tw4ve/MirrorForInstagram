from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
import re

def clean_text(s):
    if not s:
        return ""
    # remove zero-width and control chars
    return re.sub(r"[\u200B-\u200F\uFEFF\u202A-\u202E]", "", s)

console = Console()


# ==================================
# Print para una lista de usuarios
# ==================================

def print_user_table(users, title=None):
    if not users:
        return

    # You CAN choose a box, but you cannot color it here.
    # Color must be applied using border_style in Table().
    custom_box = box.SQUARE

    table = Table(
        show_header=True,
        header_style="bold magenta",
        show_lines=True,
        box=custom_box,
        expand=True,
        border_style="cyan",  # <-- COLOR OF LINES AND BORDERS
    )

    # Column headers
    table.add_column("Usuario", style="yellow bold", no_wrap=True)
    table.add_column("Nombre", style="white")
    table.add_column("ID", style="white", no_wrap=True)
    table.add_column("Foto", style="cyan bold", justify="right", no_wrap=True)

    # Rows
    for u in users:
        foto = u.get("Foto de perfil", "")
        link = f"[link={foto}]<foto>[/link]" if foto else "-"

        table.add_row(
            u.get("Usuario", ""),
            u.get("Nombre", ""),
            str(u.get("ID", "")),
            link
        )

    # Panel (only outer border gets colored)
    panel = Panel(
        table,
        title=f"[bold magenta]{title}[/bold magenta]" if title else None,
        border_style="blue",
        expand=True
    )

    console.print(panel)


# ==================================
# Print para informacion de usuario
# ==================================

def print_user_info(user):
    if not user:
        console.print("[bold red]No user info available.[/bold red]")
        return

    username = clean_text(str(user.get("Usuario", "")))

    # Create 2-column table
    info_table = Table.grid(padding=(0, 1))
    info_table.add_column(justify="left", style="bold yellow")
    info_table.add_column(style="white")

    for key, value in user.items():
        # make profile picture clickable
        if key == "Foto de perfil" and value:
            value = f"[link={value}]<foto>[/link]"

        info_table.add_row(key, clean_text(str(value)))

    # Wrap table in a nice panel
    panel = Panel(
        info_table,
        title=f"[bold magenta]Información de {username}[/bold magenta]",
        border_style="cyan",
        padding=(2, 2, 2, 2),
        expand=False
    )

    console.print(panel)
