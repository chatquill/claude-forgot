# Forgot

A Claude plugin for long chats where Claude stops following the rules you gave it at the start.

You set rules early on: reply in British English, keep it under 100 words, no bullet points, we're using Postgres. Forty messages later Claude has slipped. Type `/forgot`. Claude re-reads the whole chat, redoes its last answer so it follows every rule, and pins a short list of the chat's rules under it. That list puts the rules back near the end of the chat, where Claude pays most attention. You can also copy it into a new chat.

**Quick install:** inside Claude Code, run `/plugin marketplace add chatquill/claude-forgot`, then `/plugin install forgot@forgot`. Other ways to install are [below](#install).

## What it does

- Reads the whole conversation, not just the recent part, and collects two kinds of rule:
  - **Instructions**: language, spelling, tone, length, format, what to include or leave out.
  - **Decisions** you locked in: the audience, the stack, a name, the option you picked.
- If you changed a rule along the way, it keeps the latest version and marks it, for example `(changed from: bullet points)`. Rules you dropped are left out.
- Redoes the last answer so it follows every rule. The corrected answer comes first, on its own, with no apology or explanation.
- If the last answer already followed the rules, it says so in one line instead of rewriting it.
- Below a `---` divider, it shows one block titled **Rules for this chat**. The block has at most 10 short lines, so it's cheap to re-read in a long chat.
- Leaves out passwords, API keys, card numbers and private details, and tells you in one line when it did.
- Shows the block only when you run `/forgot`. Later replies follow the rules without repeating the block.

### Example

Early in the chat you wrote:

```text
Explain things for a complete beginner. Keep every answer under 100 words. Use British spelling.
```

Later you added "skip the bullet points, I prefer short paragraphs". Forty messages on, Claude answers in 250 words of jargon, with bullet points and American spelling. You type:

```text
/forgot
```

Claude replies with the corrected answer: under 100 words, plain language, British spelling, short paragraphs. Under it:

````text
---

```text
Rules for this chat
1. Keep every answer under 100 words.
2. Use British spelling.
3. Write for a complete beginner; explain any jargon.
4. Use short paragraphs, not bullet points (changed from: bullet points).
```
````

### Pointing at the rule it broke

You can say which rule was broken. Claude checks that one first, then still goes through the whole chat:

```text
/forgot you used feet again
```

If you name a rule you never actually gave, Claude treats it as a new rule and adds it to the block.

You don't have to use the command. Claude also picks up the skill when you say things like "you forgot I asked for British spelling" or "you're ignoring what I said at the start".

## Install

### Option 1: Claude Code plugin from GitHub

Run these two commands inside Claude Code:

```text
/plugin marketplace add chatquill/claude-forgot
/plugin install forgot@forgot
```

Then run `/reload-plugins` or start a new session. The command is `/forgot:forgot`, or type `/forgot` and pick it from the list.

### Option 2: Copy the skill folder into Claude Code

1. Clone this repository:

   ```bash
   git clone https://github.com/chatquill/claude-forgot.git
   ```

2. Copy the skill folder into your personal skills folder:

   ```bash
   mkdir -p ~/.claude/skills
   cp -r claude-forgot/skills/forgot ~/.claude/skills/
   ```

   On Windows (PowerShell):

   ```powershell
   New-Item -ItemType Directory -Force "$HOME\.claude\skills"
   Copy-Item -Recurse claude-forgot\skills\forgot "$HOME\.claude\skills\"
   ```

3. Check that `SKILL.md` is at `~/.claude/skills/forgot/SKILL.md`.

4. Start a new Claude Code session. A session that was already open won't see the new skill. The command is `/forgot`.

### Option 3: Upload the skill file to Claude.ai

1. Download [`forgot.skill`](https://github.com/chatquill/claude-forgot/releases/latest/download/forgot.skill) from the latest release. It's a zip file that contains the skill folder.
2. In Claude, open **Settings** and find the **Skills** section (under **Capabilities** on most accounts).
3. Choose **Upload skill** and select `forgot.skill`.
4. Make sure the skill is switched on.

Skills need code execution to be turned on in your settings. On Team and Enterprise plans, an admin may have to allow skills first.

In Claude chat or Cowork, type `/` in the message box and pick Forgot, or just tell Claude it forgot a rule.

## Updating

- **GitHub plugin (Option 1):** run `/plugin marketplace update forgot` in Claude Code.
- **Copied folder (Option 2):** pull the latest version and copy it again:

  ```bash
  cd claude-forgot
  git pull
  cp -r skills/forgot ~/.claude/skills/
  ```

- **Uploaded skill (Option 3):** delete the old skill in Settings and upload `forgot.skill` from the latest release.

## Limits

- If the start of the chat was summarized to save space (Claude Code does this in very long sessions), some rules may be lost. Claude says so under the block. Paste the missing rule in.
- It won't redo anything that can't be undone, such as sending an email or deploying. It shows what it would change and asks first.
- Rules from your system prompt, project instructions or `CLAUDE.md` aren't listed. Claude re-reads those every turn, so they don't fade.

## Files

```text
.claude-plugin/
├── plugin.json              Plugin manifest
└── marketplace.json         Lets this repo work as its own marketplace
skills/forgot/
└── SKILL.md                 The instructions Claude follows
tests/                       50 chat scenarios and a runner (not part of the plugin)
```

To build the `.skill` file yourself:

```bash
cd skills
zip -r ../forgot.skill forgot
```

## Feedback

Found a chat it handles badly? [Open an issue](https://github.com/chatquill/claude-forgot/issues). Include the rules you set and what Claude returned.

## Privacy

The plugin has no code and sends no data anywhere. It only reads the conversation in your own Claude session. See [PRIVACY.md](PRIVACY.md).

## License

[MIT](LICENSE)
