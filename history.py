"""
history.py — Mood history, charts, and stats (Tab 2).

Features:
  • Mood timeline (last 7 / 14 / 30 entries)
  • ASCII sparkline mood graph
  • Mood distribution table
  • Top emotions breakdown
  • All-time stats dashboard
"""

from datetime import datetime
from rich.console import Console
from rich.table   import Table
from rich.panel   import Panel
from rich.text    import Text
from rich.columns import Columns
from rich         import box

import data
import utils

console = Console()


# ── ASCII Sparkline chart ──────────────────────────────────────────────────────

SPARK_CHARS = " ▁▂▃▄▅▆▇█"


def _sparkline(scores: list[float], width: int = 40) -> str:
    """Convert a list of 1-10 scores into a unicode sparkline string."""
    if not scores:
        return "[dim]No data[/dim]"
    mn, mx = 1.0, 10.0
    chars  = []
    for s in scores[-width:]:
        idx = round((s - mn) / (mx - mn) * (len(SPARK_CHARS) - 1))
        idx = max(0, min(len(SPARK_CHARS) - 1, idx))
        chars.append(SPARK_CHARS[idx])
    return "".join(chars)


def _bar_chart(scores: list[float], dates: list[str]) -> Text:
    """Vertical ASCII bar chart — each column is one day."""
    if not scores:
        return Text("No data", style="dim")

    HEIGHT = 8
    t = Text()

    # Y-axis labels + bars
    for row in range(HEIGHT, 0, -1):
        threshold = row * (10 / HEIGHT)
        t.append(f"  {threshold:4.0f} │", style="dim")
        for score in scores:
            filled = score >= threshold
            color  = data.score_to_color(score)
            t.append("    " if filled else "     ", style=color if filled else "")
        t.append("\n")

    # X-axis
    t.append("       └" + "─────" * len(scores) + "\n", style="dim")
    t.append("        ", style="dim")
    for d in dates:
        day = datetime.strptime(d, "%Y-%m-%d").strftime("%d")
        t.append(f"  {day}   ", style="dim")

    return t


# ── Views ──────────────────────────────────────────────────────────────────────

def view_timeline(n: int = 7):
    utils.header("  Mood Timeline", f"Last {n} entries", "blue")
    recent = data.get_recent_entries(n)

    if not recent:
        utils.info("No journal entries yet. Write your first entry!")
        utils.pause()
        return

    # Timeline table
    table = Table(box=box.ROUNDED, border_style="blue", expand=True)
    table.add_column("Date",     style="white",   width=20)
    table.add_column("Mood",     style="bold",     width=16)
    table.add_column("Score",    style="white",    width=26)
    table.add_column("Emotions", style="dim",      min_width=28)
    table.add_column("Summary",  style="dim",      min_width=30)

    for date_str, entry in recent:
        color    = entry.get("color", "white")
        mood     = entry.get("mood", "—")
        score    = entry.get("score", 0.0)
        emotions = ", ".join(entry.get("emotions", []))
        summary  = entry.get("summary", "")[:55] + ("…" if len(entry.get("summary","")) > 55 else "")
        emoji    = data.MOOD_EMOJI.get(mood, )
        friendly = datetime.strptime(date_str, "%Y-%m-%d").strftime("%a, %d %b")

        table.add_row(
            friendly,
            f"[bold {color}]{emoji} {mood}[/]",
            utils.score_bar(score, width=12),
            f"[{color}]{emotions}[/]",
            summary,
        )

    console.print(table)

    # Sparkline
    scores = [e.get("score", 5.0) for _, e in reversed(recent)]
    spark  = _sparkline(scores)
    console.print(f"\n  [dim]Mood trend →[/]  {spark}")
    console.print(f"  [dim]{'Low':>4}{'':>30}High[/]\n")


def view_chart(n: int = 7):
    utils.header("  Mood Bar Chart", f"Last {n} entries", "magenta")
    recent = list(reversed(data.get_recent_entries(n)))

    if not recent:
        utils.info("No entries yet.")
        utils.pause()
        return

    dates  = [d for d, _ in recent]
    scores = [e.get("score", 5.0) for _, e in recent]

    chart = _bar_chart(scores, dates)
    console.print(Panel(chart, title="[bold magenta]Mood Score Chart (1–10)[/]",
                        border_style="magenta", expand=False))

    avg = sum(scores) / len(scores)
    console.print(f"\n  [dim]Average score:[/] {utils.score_bar(avg, width=14)}")


def view_stats():
    utils.header("  All-Time Statistics", "", "green")
    stats  = data.get_stats()
    streak = data.get_streak()

    if not stats:
        utils.info("No entries yet. Start writing to see your stats!")
        utils.pause()
        return

    # ── Stats panels ──
    t1 = Text()
    t1.append(f"\n  Total Entries    ", style="dim")
    t1.append(f"{stats['total']}\n", style="bold white")
    t1.append(f"  Average Score    ", style="dim")
    t1.append(utils.score_bar(stats["avg_score"]) + "\n")
    t1.append(f"  Highest Score    ", style="dim")
    t1.append(f"{stats['highest']:.1f} / 10\n", style="bold bright_green")
    t1.append(f"  Lowest Score     ", style="dim")
    t1.append(f"{stats['lowest']:.1f} / 10\n", style="bold red")
    t1.append(f"\n   Current Streak  ", style="dim")
    t1.append(f"{streak['current']} day(s)\n", style="bold yellow")
    t1.append(f"   Longest Streak  ", style="dim")
    t1.append(f"{streak['longest']} day(s)\n", style="bold yellow")

    t2 = Text()
    top_mood    = stats["top_mood"]
    top_emotion = stats["top_emotion"]
    color       = "cyan"
    t2.append(f"\n  Most Common Mood\n", style="dim")
    t2.append(f"  {data.MOOD_EMOJI.get(top_mood[0], )} {top_mood[0].upper()}  ", style=f"bold {color}")
    t2.append(f"({top_mood[1]}x)\n\n", style="dim")
    t2.append(f"  Top Emotions\n", style="dim")
    for emo, count in stats["all_emotions"]:
        t2.append(f"  #{emo:<16}", style=f"bold {color}")
        t2.append(f"  {count}x\n", style="dim")

    console.print(Columns([
        Panel(t1, title="[bold green] Numbers[/]",  border_style="green",  expand=True),
        Panel(t2, title="[bold cyan] Moods[/]",     border_style="cyan",   expand=True),
    ]))

    utils.pause()


def view_all_entries():
    utils.header("  All Journal Entries", "", "cyan")
    entries = data.get_all_entries()

    if not entries:
        utils.info("No entries yet.")
        utils.pause()
        return

    table = Table(box=box.SIMPLE_HEAVY, border_style="cyan", expand=True)
    table.add_column("Date",  style="white", width=22)
    table.add_column("Mood",  style="bold",  width=18)
    table.add_column("Score", style="white", width=26)
    table.add_column("Emotions", style="dim", min_width=20)

    for date_str in sorted(entries.keys(), reverse=True):
        e      = entries[date_str]
        color  = e.get("color", "white")
        mood   = e.get("mood", "—")
        score  = e.get("score", 5.0)
        emot   = ", ".join(e.get("emotions", []))
        emoji  = data.MOOD_EMOJI.get(mood, )
        dstr   = datetime.strptime(date_str, "%Y-%m-%d").strftime("%a, %d %b %Y")

        table.add_row(
            dstr,
            f"[bold {color}]{emoji} {mood}[/]",
            utils.score_bar(score, width=12),
            f"[{color}]{emot}[/]",
        )

    console.print(table)
    console.print(f"\n  [dim]Total: {len(entries)} entries[/]")
    utils.pause()


# ── Menu ───────────────────────────────────────────────────────────────────────

def menu():
    while True:
        utils.header("  Mood History", "Charts, stats and trends", "blue")
        console.print()
        console.print("  [bold cyan]1.[/]   Timeline  — Last 7 entries")
        console.print("  [bold cyan]2.[/]   Timeline  — Last 14 entries")
        console.print("  [bold cyan]3.[/]   Bar Chart — Last 7 entries")
        console.print("  [bold cyan]4.[/]   Bar Chart — Last 14 entries")
        console.print("  [bold cyan]5.[/]   All Entries")
        console.print("  [bold cyan]6.[/]   All-Time Stats")
        console.print("  [bold cyan]0.[/]   Back")

        choice = utils.prompt("Choice")
        if   choice == "1": view_timeline(7);  utils.pause()
        elif choice == "2": view_timeline(14); utils.pause()
        elif choice == "3": view_chart(7);     utils.pause()
        elif choice == "4": view_chart(14);    utils.pause()
        elif choice == "5": view_all_entries()
        elif choice == "6": view_stats()
        elif choice == "0": break
        else: utils.error("Invalid choice.")
