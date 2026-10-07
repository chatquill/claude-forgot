import json, os, re, subprocess, sys, concurrent.futures as cf
sys.path.insert(0, os.path.dirname(__file__))
from tests import TESTS

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = sys.argv[1]
OUT = sys.argv[2]
ONLY = sys.argv[3].split(",") if len(sys.argv) > 3 and sys.argv[3] else None
SUBJECT = os.environ.get("SUBJECT", "claude-sonnet-5-5")
JUDGE = os.environ.get("JUDGE", "claude-opus-5-5")
os.makedirs(OUT, exist_ok=True)

body = open(SKILL).read().split("---", 2)[2].strip()

def inject(text, args=""):
    return (f"<command-message>forgot is running…</command-message>\n<command-name>/forgot</command-name>\n"
            f"<command-args>{args}</command-args>\n\nBase directory for this skill: ~/.claude/skills/forgot\n\n{body}"
            + (f"\n\nARGUMENTS: {args}" if args else ""))

def user_text(text, skill):
    t = text.replace("\n\n[skill loaded]", "")
    if t.startswith("/forgot"):
        return inject(t, t[len("/forgot"):].strip())
    if skill:
        return t + "\n\n<system-reminder>The user's message matches the forgot skill. Skill loaded:</system-reminder>\n\n" + body
    return t

def render(test):
    parts = []
    for role, text in test["turns"]:
        if role == "user":
            text = user_text(text, False)
        parts.append(f'<turn role="{role}">\n{text}\n</turn>')
    final = user_text(test["final"], test.get("skill", True))
    return ("Here is our conversation so far. You are the assistant. Write your next reply to the final user turn, "
            "exactly as you would send it to the user. Output only that reply.\n\n<conversation>\n"
            + "\n".join(parts) + f'\n<turn role="user">\n{final}\n</turn>\n</conversation>')

def claude(prompt, model, system, effort):
    env = {k: v for k, v in os.environ.items() if k != "CLAUDE_CODE_SESSION_ID"}
    r = subprocess.run(["claude", "-p", "--model", model, "--effort", effort, "--tools", "",
                        "--no-session-persistence", "--system-prompt", system, "--strict-mcp-config"],
                       input=prompt, capture_output=True, text=True, timeout=600, env=env, cwd=HERE)
    return r.stdout.strip()

APOLOGY = re.compile(r"^\W*(sorry|apolog|you'?re right|you are right|my bad|good catch|corrected answer|here'?s the corrected|you'?re absolutely)", re.I)

def structural(test, reply):
    errs = []
    has = "Rules for this chat" in reply
    if not test["block"]:
        if has: errs.append("block present but not expected")
    else:
        if reply.count("Rules for this chat") != 1:
            errs.append(f"'Rules for this chat' appears {reply.count('Rules for this chat')} times")
        m = re.search(r"\n---\s*\n+```text\n(Rules for this chat\n.*?)\n```", reply, re.S)
        if not m:
            errs.append("no '---' divider followed by ```text block starting 'Rules for this chat'")
        else:
            lines = m.group(1).split("\n")[1:]
            nums = [l for l in lines if l.strip()]
            if not 1 <= len(nums) <= 10: errs.append(f"{len(nums)} rule lines")
            bad = [l for l in nums if not re.match(r"^\d+\. \S", l)]
            if bad: errs.append(f"non-numbered lines in block: {bad}")
            after = [l for l in reply[m.end():].split("\n") if l.strip() and l.strip() not in ("</turn>", "</parameter>", "</reply>", "</output>", "</conversation>")]
            extra = [l for l in after if not re.match(r"^(Left out:|Early messages were summari[sz]ed)", l)]
            if extra or len(after) > 2: errs.append(f"unexpected text after block: {after}")
            before = reply[:m.start()].strip()
            if before and APOLOGY.match(before) and test["id"] != "30-risky": errs.append("corrected answer opens with apology/meta")
    for f in test.get("forbid", []):
        if f.lower() in reply.lower(): errs.append(f"forbidden string present: {f}")
    return errs

JUDGE_SYS = "You are a strict, precise test grader. Output only JSON."

def judge(test, reply):
    convo = "\n".join(f"{r.upper()}: {t}" for r, t in test["turns"]) + f"\nUSER (final): {test['final']}"
    crit = "\n".join(f"{i+1}. {c}" for i, c in enumerate(test["criteria"]))
    p = (f"A chat assistant ran the forgot skill. It should redo its last answer to follow the user's earlier rules, "
         f"then show a --- divider and a 'Rules for this chat' block.\n\n<conversation>\n{convo}\n</conversation>\n\n"
         f"<reply>\n{reply}\n</reply>\n\nGrade the reply against each criterion. Be strict but literal; count words and sentences when a limit is involved.\n{crit}\n\n"
         'Output JSON only: {"results": [{"n": 1, "pass": true, "why": "..."}, ...]}')
    raw = claude(p, JUDGE, JUDGE_SYS, "medium")
    m = re.search(r"\{.*\}", raw, re.S)
    try:
        return json.loads(m.group(0))["results"]
    except Exception:
        return [{"n": 0, "pass": False, "why": "judge parse error: " + raw[:200]}]

SUBJECT_SYS = "You are Claude, a helpful AI assistant made by Anthropic, chatting with a user."

def one(test):
    sysp = SUBJECT_SYS + ("\n\n" + test["system_extra"] if test.get("system_extra") else "")
    reply = claude(render(test), SUBJECT, sysp, "medium")
    s = structural(test, reply)
    j = judge(test, reply)
    fails = s + [f"criterion {r['n']}: {r['why']}" for r in j if not r.get("pass")]
    res = {"id": test["id"], "pass": not fails, "fails": fails, "reply": reply}
    json.dump(res, open(f"{OUT}/{test['id']}.json", "w"), indent=1, ensure_ascii=False)
    return res

tests = [t for t in TESTS if not ONLY or t["id"] in ONLY]
with cf.ThreadPoolExecutor(int(os.environ.get("PAR", "8"))) as ex:
    results = list(ex.map(one, tests))
bad = [r for r in results if not r["pass"]]
print(f"{len(results)-len(bad)}/{len(results)} passed")
for r in bad:
    print(f"\n### {r['id']}")
    for f in r["fails"]: print("  -", f)
