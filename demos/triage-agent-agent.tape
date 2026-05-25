# Demo: an LLM driving triage-agent over MCP, replayed at a readable pace.
# Record with: vhs demos/triage-agent-agent.tape

Output demos/triage-agent-agent.gif

Set Shell "bash"
Set Theme "rose-pine"
Set FontSize 18
Set Width 1180
Set Height 480
Set Padding 24
Set TypingSpeed 24ms

Hide
Type "source .venv/bin/activate >/dev/null 2>&1 || true"
Enter
Type "python scripts/agent_demo.py"
Enter
Sleep 500ms
Show
Sleep 11s
Screenshot demos/triage-agent-agent.png
