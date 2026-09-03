"""
utils.py — Shared display helpers and input utilities using Rich.
"""

from datetime import datetime, date
from rich.console import Console
from rich.panel   import Panel
from rich.text    import Text
from rich         import box

console = Console()

APP_TITLE = "  A I   M O O D   J O U R N A L"


# ── Generic UI helpers ─────────────────────────────────────────────────────────

def clear():
    console.clear()


def header(title: str, subtitle: str = "", color: str = "cyan"):
    clear()
    t = Text(justify="center")
    t.append(f"\n{APP_TITLE}\n", style="bold cyan")
    t.append(f"{title}\n", style=f"bold {color}")
    if subtitle:
        t.append(subtitle, style="dim")
    console.print(Panel(t, border_style=color, expand=True))


def success(msg: str):
    console.print(f"\n  [bold green]✓[/] {msg}")


def error(msg: str):
    console.print(f"\n  [bold red]✗[/] {msg}")


def info(msg: str):
    console.print(f"\n  [dim cyan]ℹ[/] {msg}")


def warn(msg: str):
    console.print(f"\n  [bold yellow]⚠[/] {msg}")


def prompt(msg: str, default: str = "") -> str:
    try:
        val = console.input(f"\n  [bold cyan]>[/] {msg}: ").strip()
        return val if val else default
    except (EOFError, KeyboardInterrupt):
        return default


def pause():
    try:
        console.input("\n  [dim]Press Enter to continue...[/]")
    except (EOFError, KeyboardInterrupt):
        pass


def ask_date(label: str = "Date (YYYY-MM-DD)") -> str:
    default = date.today().isoformat()
    while True:
        val = prompt(label, default)
        try:
            datetime.strptime(val, "%Y-%m-%d")
            return val
        except ValueError:
            error("Use YYYY-MM-DD format (e.g. 2025-04-14)")


def pick_from(options: list, label: str = "Choose") -> int | None:
    console.print()
    for i, opt in enumerate(options, 1):
        console.print(f"  [bold cyan]{i}.[/] {opt}")
    console.print("  [dim]0. Cancel[/]")
    raw = prompt(label)
    try:
        n = int(raw)
        if n == 0:
            return None
        if 1 <= n <= len(options):
            return n - 1
    except ValueError:
        pass
    error("Invalid choice.")
    return None


# ── Date helpers ───────────────────────────────────────────────────────────────

def today_str() -> str:
    return date.today().isoformat()


def friendly_date(date_str: str) -> str:
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").strftime("%A, %d %B %Y")
    except ValueError:
        return date_str


# ── Mood-specific display ──────────────────────────────────────────────────────

def score_bar(score: float, width: int = 20) -> str:
    """Return a colored ASCII progress bar for a mood score (1-10)."""
    filled = round((score / 10) * width)
    bar    =  * filled +  * (width - filled)
    if score >= 8:
        color = "bright_green"
    elif score >= 6:
        color = "green"
    elif score >= 4:
        color = "yellow"
    elif score >= 2:
        color = "red"
    else:
        color = "bright_red"
    return f"[{color}]{bar}[/{color}]  [{color}]{score:.1f}/10[/{color}]"


def mood_badge(mood: str, color: str) -> str:
    from data import MOOD_EMOJI
    emoji = MOOD_EMOJI.get(mood, )
    return f"[bold {color}]{emoji}  {mood.upper()}[/bold {color}]"


def multiline_input(prompt_text: str) -> str:
    """
    Accept multi-line journal input.
    User types their entry and ends with a blank line or 'END'.
    """
    console.print(f"\n  [bold cyan]>[/] {prompt_text}")
    console.print("  [dim](Type your entry below. Press Enter twice or type END on a new line to finish.)[/]")
    console.print()

    lines = []
    blank_count = 0
    try:
        while True:
            line = input("  ")
            if line.strip().upper() == "END":
                break
            if line.strip() == "":
                blank_count += 1
                if blank_count >= 2:
                    break
                lines.append("")
            else:
                blank_count = 0
                lines.append(line)
    except (EOFError, KeyboardInterrupt):
        pass

    return "\n".join(lines).strip()
