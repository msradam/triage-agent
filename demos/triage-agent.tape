# Demo: triage-agent render + sessions show, Rose Pine.
# Record with: vhs demos/triage-agent.tape

Output demos/triage-agent.gif

Set Shell "bash"
Set Theme "rose-pine"
Set FontSize 16
Set Width 1200
Set Height 540
Set Padding 20
Set TypingSpeed 28ms

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

# The graph: no edge from classify straight to resolve. The gate is the shape.
Type "triage-agent render"
Sleep 600ms
Enter
Sleep 3s

Hide
Type "python scripts/seed.py >/dev/null 2>&1"
Enter
Sleep 4s
Type "clear"
Enter
Show

# The recorded walk: classify, gather context, resolve.
Type "triage-agent sessions show --project triage-agent"
Sleep 600ms
Enter
Sleep 2s
Screenshot demos/triage-agent.png
Sleep 2s
