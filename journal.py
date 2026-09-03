"""
journal.py — Write and view journal entries (Tab 1).

Features:
  • Write today's entry (multi-line input)
  • AI analysis: mood, score, emotions, summary, suggestion
  • View / re-read any past entry
  • Delete an entry
"""

from rich.console import Console
from rich.panel   import Panel
from rich.table   import Table
from rich.text    import Text
from rich.spinner import Spinner
from rich         import box
import time

import data
import utils
import ai

console = Console()


# ── Write entry ────────────────────────────────────────────────────────────────

def write_entry():
    today = utils.today_str()
    utils.header(
        "   Write Today's Journal",
        f"  {utils.friendly_date(today)}",
        "cyan",
    )

    # Warn if entry already exists
    if data.has_entry_today():
        utils.warn("You already have an entry for today. Writing a new one will overwrite it.")
        confirm = utils.prompt("Continue? (y/n)", "n")
        if confirm.lower() != "y":
            return

    # AI mode notice
    if ai.is_demo_mode():
        utils.info("Running in DEMO MODE (no API key). Add GEMINI_API_KEY to .env for full AI analysis.")
    else:
        utils.info("AI analysis powered by Google Gemini ")

    console.print()
    text = utils.multiline_input("How was your day? Write freely — no judgment here.")

    if not text or len(text) < 10:
        utils.error("Entry too short. Write at least a sentence.")
        utils.pause()
        return

    # ── AI Analysis ──
    console.print()
    with console.status("[bold cyan]  Analysing your mood with AI...[/]", spinner="dots"):
        time.sleep(0.5)   # small delay for UX
        result = ai.analyze(text)

    # ── Save ──
    data.save_entry(
        date_str   = today,
        text       = text,
        mood       = result["mood"],
        score      = result["score"],
        emotions   = result["emotions"],
        summary    = result["summary"],
        suggestion = result["suggestion"],
        color      = result["color"],
    )

    # ── Show result ──
    _show_analysis(result, today)
    utils.pause()


def _show_analysis(result: dict, date_str: str):
    """Print a rich panel showing the AI analysis result."""
    color  = result.get("color", "yellow")
    mood   = result.get("mood", "neutral")
    score  = result.get("score", 5.0)
    streak = data.get_streak()

    # ── Mood panel ──
    t = Text()
    t.append("\n  Mood     ", style="dim")
    t.append(utils.mood_badge(mood, color))
    t.append("\n\n  Score    ", style="dim")
    t.append(utils.score_bar(score))

    t.append("\n\n  Emotions ", style="dim")
    for emo in result.get("emotions", []):
        t.append(f"  [{color}]#{emo}[/{color}]")

    t.append(f"\n\n  Summary  ", style="dim")
    t.append(result.get("summary", ""), style="white")

    t.append(f"\n\n   Tip   ", style="dim")
    t.append(result.get("suggestion", ""), style=f"italic {color}")

    t.append(f"\n\n   Streak  ", style="dim")
    t.append(f"{streak['current']} day(s)  ", style="bold yellow")
    t.append(f"  Best: {streak['longest']} day(s)", style="dim")
    t.append("\n")

    if result.get("_demo"):
        t.append("\n  [dim]⚠  Demo mode — add GEMINI_API_KEY to .env for real AI analysis[/dim]")

    console.print(Panel(
        t,
        title=f"[bold {color}]  AI Mood Analysis — {utils.friendly_date(date_str)}[/]",
        border_style=color,
        expand=True,
    ))


# ── View single entry ──────────────────────────────────────────────────────────

def view_entry(date_str: str = None):
    if date_str is None:
        date_str = utils.ask_date("View entry for date (YYYY-MM-DD)")

    entry = data.get_entry(date_str)
    if not entry:
        utils.error(f"No entry found for {date_str}.")
        utils.pause()
        return

    color = entry.get("color", "cyan")
    utils.header(
        f"  Journal Entry",
        utils.friendly_date(date_str),
        color,
    )

    # Original text
    console.print(Panel(
        f"\n{entry['text']}\n",
        title="[dim]Your Words[/dim]",
        border_style="dim",
        expand=True,
    ))

    # AI result
    _show_analysis(entry, date_str)
    utils.pause()


# ── Delete entry ───────────────────────────────────────────────────────────────

def delete_entry():
    utils.header("   Delete Entry", "", "red")
    date_str = utils.ask_date("Delete entry for date (YYYY-MM-DD)")

    entry = data.get_entry(date_str)
    if not entry:
        utils.error(f"No entry found for {date_str}.")
        utils.pause()
        return

    console.print(f"\n  Entry: [bold]{entry.get('mood','?')}[/] mood on [bold]{utils.friendly_date(date_str)}[/]")
    confirm = utils.prompt("Permanently delete this entry? (y/n)", "n")
    if confirm.lower() == "y":
        data.delete_entry(date_str)
        utils.success("Entry deleted.")
    else:
        utils.info("Cancelled.")
    utils.pause()


# ── Menu ───────────────────────────────────────────────────────────────────────

def menu():
    while True:
        utils.header("   Journal", "Write, read, and reflect", "cyan")
        console.print()
        console.print("  [bold cyan]1.[/]    Write Today's Entry")
        console.print("  [bold cyan]2.[/]   Read a Past Entry")
        console.print("  [bold cyan]3.[/]    Delete an Entry")
        console.print("  [bold cyan]0.[/]  Back")

        choice = utils.prompt("Choice")
        if   choice == "1": write_entry()
        elif choice == "2": view_entry()
        elif choice == "3": delete_entry()
        elif choice == "0": break
        else: utils.error("Invalid choice.")
