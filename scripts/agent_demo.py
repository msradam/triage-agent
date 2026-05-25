"""Paced replay of an LLM driving triage-agent over MCP.

A live agent run scrolls past too fast to read, so this replays the real
sequence of tool calls at a readable cadence, including the moment the model
calls an action with the wrong inputs and the server's structured error puts it
back on track. Only the pacing is added.
"""

from __future__ import annotations

import sys
import time

from rich.console import Console
from rich.theme import Theme

THEME = Theme(
    {
        "ok": "bold #9ccfd8",
        "err": "bold #eb6f92",
        "action": "bold #c4a7e7",
        "muted": "#6e6a86",
        "subtle": "#908caa",
        "prompt": "bold #f6c177",
    }
)
console = Console(theme=THEME)

PROMPT = "A customer was charged twice. Triage the ticket, then resolve it."
STEPS = [
    ("classify", "(no inputs)", "err", "missing required inputs: category, priority"),
    ("classify", "category=billing, priority=high", "ok", "classified"),
    ("gather_context", "note=duplicate confirmed in ledger", "ok", "investigating"),
    ("resolve", "resolution=refunded the duplicate", "ok", "resolved"),
]


def main() -> None:
    if sys.stdout.isatty():
        sys.stdout.write("\033[2J\033[3J\033[H")
        sys.stdout.flush()
        time.sleep(0.4)
    console.print(f"[muted](triage-agent) >[/] [prompt]{PROMPT}[/]")
    time.sleep(1.1)
    console.print()
    console.print("[subtle]the model drives the FSM; the server corrects a bad call along the way:[/]")
    console.print()
    time.sleep(1.0)
    for action, args, status, state in STEPS:
        console.print(
            f"  [subtle]→[/] [muted]step[/] [action]{action:<14}[/] [subtle]{args:<34}[/]",
            end="",
        )
        time.sleep(0.7)
        glyph = "[ok]✓[/]" if status == "ok" else "[err]✗[/]"
        style = "subtle" if status == "ok" else "err"
        console.print(f"  {glyph}  [{style}]{state}[/]")
        time.sleep(1.0)
    console.print()
    time.sleep(0.4)
    console.print("[muted]the wrong call could not bluff past the schema · ticket resolved[/]")


if __name__ == "__main__":
    main()
