# Tests

50 chat scenarios for the `forgot` skill. Each one sets rules early in a chat, has Claude break them, then runs `/forgot`. The runner checks the reply's shape (divider, block, at most 10 rules, no leaked secrets) and asks a second Claude model to grade it against the scenario's criteria.

Needs the `claude` CLI, signed in.

```bash
python3 tests/run.py skills/forgot/SKILL.md /tmp/forgot-out            # all 50, Sonnet
SUBJECT=claude-haiku-4-5-20251001 python3 tests/run.py skills/forgot/SKILL.md /tmp/forgot-out
python3 tests/run.py skills/forgot/SKILL.md /tmp/forgot-out 07-apikey,30-risky   # selected tests
```

`PAR` sets how many run at once (default 8). `JUDGE` sets the grading model.
