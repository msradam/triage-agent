# Demo: an LLM (via fast-agent) driving triage-agent over MCP, Rose Pine.
# Record with: GOOGLE_API_KEY=... vhs demos/triage-agent-agent.tape

Output demos/triage-agent-agent.gif

Set Shell "bash"
Set Theme "rose-pine"
Set FontSize 14
Set Width 1240
Set Height 760
Set Padding 20
Set TypingSpeed 24ms

Hide
Type "export VIRTUAL_ENV_DISABLE_PROMPT=1"
Enter
Type "source .venv/bin/activate >/dev/null 2>&1 || true"
Enter
Type `export PS1="(triage-agent) > "`
Enter
Type "clear"
Enter
Show

Type `uvx fast-agent-mcp go --servers triage-agent --model generic.meta-llama/Llama-3.3-70B-Instruct-Turbo -m "A customer says they were charged twice. Triage the ticket: classify it, record your findings, then resolve it."`
Sleep 600ms
Enter
Sleep 48s
Screenshot demos/triage-agent-agent.png
