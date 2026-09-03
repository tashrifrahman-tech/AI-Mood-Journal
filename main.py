"""
main.py — AI Mood Journal entry point.

Tabs:
  1 →   Journal   (write entry, read past entries, delete)
  2 →   History   (timeline, charts, stats)
"""

from datetime import date
from rich.console import Console
from rich.panel   import Panel
from rich.text    import Text
from rich.columns import Columns
from rich         import box

import data
import utils
import ai
import journal
import history

console = Console()


# ── Dashboard ──────────────────────────────────────────────────────────────────

def _dashboard():
    today  = utils.today_str()
    streak = data.get_streak()
    stats  = data.get_stats()
    entry  = data.get_entry(today)
    recent = data.get_recent_entries(5)

    # ── Today panel ──
    t = Text()
    t.append(f"\n    {utils.friendly_date(today)}\n\n", style="bold white")

    if entry:
        color = entry.get("color", "cyan")
        mood  = entry.get("mood", "—")
        score = entry.get("score", 5.0)
        emoji = data.MOOD_EMOJI.get(mood,)
        t.append("  Today's mood    ", style="dim")
        t.append(f"{emoji} {mood.upper()}\n", style=f"bold {color}")
        t.append("  Score           ", style="dim")
        t.append(utils.score_bar(score, width=12) + "\n")
        t.append("\n  Tip: ", style="dim")
        t.append(entry.get("suggestion", ""), style="italic cyan")
        t.append("\n")
    else:
        t.append("  [dim]No entry yet today.[/dim]\n")
        t.append("  [bold cyan]→ Press 1 to write today's entry[/bold cyan]\n")

    t.append(f"\n   Streak      ", style="dim")
    t.append(f"{streak.get('current', 0)} day(s)", style="bold yellow")
    t.append(f"    Best: {streak.get('longest', 0)} day(s)\n", style="dim")

    today_panel = Panel(t, title="[bold cyan]Today[/]", border_style="cyan", expand=True)

    # ── Recent moods panel ──
    t2 = Text()
    t2.append("\n")
    if recent:
        for d, e in recent:
            color = e.get("color", "white")
            mood  = e.get("mood", "—")
            score = e.get("score", 5.0)
            emoji = data.MOOD_EMOJI.get(mood, "💭")
            day   = date.fromisoformat(d).strftime("%a %d")
            t2.append(f"  {day:<10}", style="dim")
            t2.append(f"{emoji} {mood:<14}", style=f"bold {color}")
            t2.append(f"{score:.1f}\n", style="dim")

        scores = [e.get("score", 5.0) for _, e in reversed(recent)]
        spark  = "".join(" ▁▂▃▄▅▆▇█"[max(0, min(8, round((s-1)/9*8)))] for s in scores)
        t2.append(f"\n  Trend:  {spark}\n", style="cyan")

        if stats:
            t2.append(f"\n  All-time avg  ", style="dim")
            t2.append(f"{stats.get('avg_score', 0):.1f} / 10\n", style="bold white")
            t2.append(f"  Total entries  ", style="dim")
            t2.append(f"{stats.get('total', 0)}\n", style="bold white")
    else:
        t2.append("  [dim]No entries yet.\n  Start journaling to see your history![/dim]\n")

    recent_panel = Panel(t2, title="[bold blue]Recent Moods[/]", border_style="blue", expand=True)

    console.print(Columns([today_panel, recent_panel], equal=True, expand=True))

    # ── AI mode banner ──
    if ai.is_demo_mode():
        console.print(
            Panel(
                "[yellow]⚠  Running in DEMO MODE — AI analysis is simulated.\n"
                "   Add your free Gemini API key to [bold].env[/bold] for real AI mood analysis.\n"
                "   See README.md → 'Getting Your Free API Key' for instructions.[/yellow]",
                border_style="yellow",
                expand=True,
            )
        )


# ── Main Menu ──────────────────────────────────────────────────────────────────

def main():
    while True:
        utils.clear()
        console.print(Panel(
            Text("  AI  MOOD  JOURNAL", justify="center", style="bold cyan"),
            subtitle="[dim]Powered by Google Gemini · Your private, AI-guided journal[/dim]",
            border_style="cyan",
            expand=True,
        ))

        _dashboard()

        console.print()
        console.print(
            "   [bold cyan][ 1 ]     Journal[/]"
            "        "
            "[bold blue][ 2 ]    History & Charts[/]"
        )
        console.print("   [dim]0.  Exit[/]")

        choice = utils.prompt("Select Tab")

        if   choice == "1": journal.menu()
        elif choice == "2": history.menu()
        elif choice == "0":
            utils.clear()
            console.print("\n  [bold cyan]Take care of yourself. See you tomorrow. [/]\n")
            break
        else:
            utils.error("Enter 1, 2, or 0.")


if __name__ == "__main__":
    main()
