"""The `triage-agent` command, built on burrmcp's build_cli."""

from __future__ import annotations

from burrmcp.cli import build_cli, run

from triage_agent.app import build_application

cli = build_cli(
    "triage-agent",
    application=build_application,
    help="Support-triage agent: a Burr state machine served over MCP.",
    server_name="triage-agent",
)


def main() -> int:
    return run(cli)
