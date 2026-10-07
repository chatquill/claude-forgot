---
name: claude-forgot
description: Re-reads the rules the user set earlier in a long chat, redoes Claude's last answer so it follows all of them, and pins a short "Rules for this chat" block the user can copy. Use whenever the user runs /claude-forgot, or says Claude forgot, ignored or stopped following something they said earlier ("you forgot my instructions", "I told you to use British spelling", "you're ignoring what I said at the start", "why did you stop doing X").
argument-hint: "[optional: the rule you think was broken]"
effort: medium
---

# Claude forgot

In a long chat, rules the user set early on get followed less and less. This skill fixes the last answer and puts every rule back at the end of the chat, where it is recent again.

Do not use tools. Everything needed is in the conversation. Do not read files, search, or run commands to find rules.

## Step 1: Collect the rules

Read the whole conversation from the first message, not just the recent part. Collect two kinds of item:

- Instructions: anything the user told you to do or not do in your answers. Language, spelling, tone, length, format, structure, what to include or leave out, how to address them, what never to suggest.
- Decisions: choices the user locked in that later answers must respect. The audience, the stack or tool, a name, a number, a deadline, an option they picked from several you offered.

Count only what the user said or agreed to. A suggestion you made counts only if the user accepted it.

Leave out:
- One-off requests that are already done ("translate this paragraph").
- Anything that is not in the user's chat messages: the system prompt, project instructions, CLAUDE.md, custom instructions. Leave these out even when they read like rules. They are loaded again every turn and do not fade.
- Passwords, API keys, tokens, card numbers and other secrets. Never repeat one, not even partly. If a rule depends on one, write the rule with a placeholder, such as `<the API key you gave earlier>`.
- Personal details the user shared that are not rules (health, address, family). Keep only what changes how you answer, worded generally.

If the user changed a rule later in the chat, keep only the latest version and always mark it with the version it replaced: `Use prose, not bullet points (changed from: bullet points).` If it changed several times, name the version just before the latest: `Keep answers under 50 words (changed from: 200 words).` If the user dropped a rule ("forget the word limit"), leave it out. Keep only what they asked for instead, if anything ("Give detailed answers.").

If the user typed text after `/claude-forgot`, treat it as a hint about which rule was broken. Check that rule first, then still go through the whole conversation. The hint adds to the list; it never replaces it. If the hint states a rule you cannot find earlier, the user is stating it now: follow it and include it.

If the conversation was summarized or compacted (you see a summary of earlier messages instead of the messages themselves), use the summary as well as the visible messages, and remember to add the summary line after the block in Step 3.

## Step 2: Redo the answer

Find the answer to fix: your last reply before this request. If the hint points to a different reply, fix that one instead.

Check that answer against each rule from Step 1, one by one. If it broke none of them, do not rewrite it, not even to improve it. Write one line instead: `Your last answer already follows these rules.` Then go to Step 3.

If it broke at least one rule, write that answer again from scratch so it follows every rule from Step 1. Answer the same question the user asked, with the same substance, unless a rule changes the substance (for example a decision about the stack). This is the corrected answer.

- Output the corrected answer first and on its own. No apology, no "You're right", no note about what changed, no heading such as "Corrected answer". Its first line is the answer itself.
- It must obey every answer rule: language, length, format, tone. If the rules say "no markdown", the corrected answer has no markdown.
- If the last answer was an action rather than text (files edited, a command run), redo the action so it fits the rules, then give the reply the rules ask for. Do not redo anything that cannot be undone (deploying, deleting, sending a message or email, a payment). Instead, say briefly what you would redo and ask before doing it.

If there is no earlier answer to fix (the request is the first message, or every earlier reply was about something else), skip the corrected answer and go straight to the block.

If you find no rules at all, do not write a block. Reply with one line: `I can't find any rules earlier in this chat. Tell me the rule and I'll follow it.`

## Step 3: Pin the rules

Below the corrected answer, output a line with `---` on its own, then one fenced `text` code block in this shape:

```text
Rules for this chat
1. <rule>
2. <rule>
```

- The first line is exactly `Rules for this chat`. Then one numbered rule per line, at most 10 rules.
- Each rule is short, ideally under 15 words, and starts with a verb or names the decision: `Write in British English.`, `Audience: beginners with no coding experience.`
- Write each rule in the language the user wrote it in. If the user wrote the rules in German, the rules in the block are in German, even when they are about another language. Only the first line stays `Rules for this chat`.
- The block is a tool, not an answer, so answer rules about format or length (no markdown, under 50 words) do not apply to it.
- With more than 10 rules, merge related ones ("Use British spelling and a formal tone.") and drop ones that no longer matter. Never drop a rule the hint named, or one the last answer broke.
- Put the rules the last answer broke first.

After the block, add at most one line each, only when it applies:
- A secret was left out: `Left out: the API key from an earlier message.`
- The chat contains a summary of earlier messages: `Early messages were summarized. If a rule is missing, paste it in.`

Nothing else comes after the block. No offer to help, no question, no explanation.

## After this

Keep following every rule in the block in all later replies. Do not show the block again, mention it, or promise to remember. It appears only when the user runs `/claude-forgot` again.

## Example

Early in the chat the user wrote: "Explain things for a complete beginner. Keep every answer under 100 words. Use British spelling. Put the steps in bullet points." Later: "Actually, skip the bullet points, I prefer short paragraphs." Forty messages on, your last answer used American spelling, bullet points and 250 words of jargon.

The user types: `/claude-forgot`

You reply with the corrected answer (under 100 words, beginner-friendly, British spelling, short paragraphs), then:

---

```text
Rules for this chat
1. Keep every answer under 100 words.
2. Use British spelling.
3. Write for a complete beginner; explain any jargon.
4. Use short paragraphs, not bullet points (changed from: bullet points).
```
