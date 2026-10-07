---
name: forgot
description: Re-reads the rules the user set earlier in a long chat, redoes Claude's last answer so it follows all of them, and pins a short "Rules for this chat" block the user can copy. Use whenever the user runs /forgot, or says Claude forgot, ignored or stopped following something they said earlier ("you forgot my instructions", "I told you to use British spelling", "you're ignoring what I said at the start", "why did you stop doing X").
argument-hint: "[optional: the rule you think was broken]"
effort: medium
---

# Forgot

In a long chat, rules the user set early on get followed less and less. This skill fixes the last answer and puts every rule back at the end of the chat, where it is recent again.

Do not use tools. Everything needed is in the conversation. Do not read files, search, or run commands to find rules.

## Step 1: Collect the rules

Read the whole conversation from the first message, not just the recent part. Collect two kinds of item:

- Instructions: anything the user told you to do or not do in your answers. Language, spelling, tone, length, format, structure, what to include or leave out, how to address them, what never to suggest.
- Decisions: choices the user locked in that later answers must respect. The audience, the stack or tool, a name, a number, a deadline, an option they picked from several you offered.

An instruction counts even when it is said once, casually, or next to other text, without words like "always" or "rule" ("I'm learning Spanish. Explain grammar simply."). Count only what the user said or agreed to. A suggestion you made counts only if the user accepted it.

Leave out:
- One-off requests that are already done ("translate this paragraph").
- Anything that is not in the user's chat messages: the system prompt, project instructions, CLAUDE.md, custom instructions. Leave these out even when they read like rules. They are loaded again every turn and do not fade.
- Passwords, API keys, tokens, card numbers and other secrets. Never repeat one, not even partly. If a rule depends on one, write the rule with a placeholder, such as `<the API key you gave earlier>`.
- Personal details the user shared (health conditions, diagnoses, address, family, money). Never name them in the block. Word the rule by what it means for your answers: `Never suggest fasting or extreme diets.`, not `Avoid fasting because of diabetes.`

If the user changed a rule later in the chat, keep only the latest version and always mark it with the version it replaced: `Use prose, not bullet points (changed from: bullet points).` If it changed several times, name the version just before the latest: `Keep answers under 50 words (changed from: 200 words).` If the user dropped a rule ("forget the word limit"), leave it out. Keep only what they asked for instead, if anything ("Give detailed answers.").

If the user typed text after `/forgot`, treat it as a hint about which rule was broken. Check that rule first, then still go through the whole conversation. The hint adds to the list; it never replaces it. If the hint states a rule you cannot find earlier, the user is stating it now: follow it and include it.

If the conversation was summarized or compacted (you see a summary of earlier messages instead of the messages themselves), use the summary as well as the visible messages, and remember to add the summary line after the block in Step 3.

## Step 2: Redo the answer

Find the answer to fix: your last reply before this request. If the hint points to a different reply, fix that one instead.

If that answer sent, deleted, deployed, published or paid for something, never do it again on your own. Do not call the tool, do not write a tool call, and do not say it was done. Show the corrected version as a plain-text draft (the email as it should have been, for example), never in the form of a tool call, say in one sentence what the first attempt got wrong, and ask "Should I send it?" (or deploy, delete, and so on). Then go to Step 3. Other actions, such as editing files, you redo so they fit the rules, then give the reply the rules ask for.

Check that answer against each rule from Step 1, one by one, looking at the actual words: tense, spelling, units, length, format, names. If it broke none of them, do not rewrite it, not even to improve it. Write one line instead: `Your last answer already follows these rules.` Then go to Step 3.

If it broke at least one rule, write that answer again from scratch so it follows every rule from Step 1. Answer the same question the user asked, with the same substance, unless a rule changes the substance (for example a decision about the stack). This is the corrected answer.

- Output the corrected answer first and on its own. No apology, no "You're right", no note about what changed, no heading such as "Corrected answer". Its first line is the answer itself.
- It must obey every answer rule: language, length, format, tone. If the rules say "no markdown", the corrected answer has no markdown. Treat limits as hard: for "under N words", write at most three quarters of N (under 40 words: 30 words at most), and count before you finish. When a limit forces cuts, keep the core answer and drop side details. Apply every rule to every part of the answer: the lead-in sentence, code, commands (written for the user's stated system or shell) and examples. Follow each rule literally: a required closing line goes on its own line; "free tools only" rules out tools with paid plans.

If there is no earlier answer to fix (the request is the first message, or every earlier reply was about something else), skip the corrected answer and go straight to the block.

If you find no rules at all, do not write a block. Reply with one line: `I can't find any rules earlier in this chat. Tell me the rule and I'll follow it.`

## Step 3: Pin the rules

Below the corrected answer, output a line with `---` on its own, then one fenced `text` code block in this shape:

```text
Rules for this chat
1. <rule>
2. <rule>
```

- The first line is exactly `Rules for this chat`. Then one numbered rule per line, at most 10 rules. Count them before you finish; 11 or more is never allowed.
- Each rule is short, ideally under 15 words, and starts with a verb or names the decision: `Write in British English.`, `Audience: beginners with no coding experience.`
- Write the rules in the language the user typed them in, which is not always the language they asked you to reply in. Typed in English, "Always reply in French" becomes `1. Always reply in French.` Typed in German, "Antworte auf Deutsch, Code-Kommentare auf Englisch" becomes `1. Antworte auf Deutsch; Code-Kommentare auf Englisch.` The first line always stays `Rules for this chat`. Decide this before writing the block; never write the block twice. Spanish rules stay in Spanish, French rules in French: do not translate them into English.
- The block is a tool, not an answer, so answer rules about format or length (no markdown, under 50 words) do not apply to it.
- With more than 10 rules, first list every rule the last answer broke; those always stay. Then merge related ones ("Use British spelling and a formal tone.") and drop ones that no longer matter. Never drop a rule the hint named, or one the last answer broke, including how to address the user.
- Put the rules the last answer broke first.

After the block's closing fence, add at most one plain-text line each (not inside any code block), only when it applies:
- A secret was left out: `Left out: the API key from an earlier message.`
- The chat contains a summary of earlier messages: `Early messages were summarized. If a rule is missing, paste it in.`

Nothing else comes after the block. No offer to help, no question, no explanation.

Before you finish, check:
- The corrected answer breaks none of the rules, and any limit is met with room to spare.
- The block has 10 rules or fewer, in the language the user typed them in. Rules typed in French are in French, not English.
- No secret or private detail appears anywhere.
- If the chat contains a summary of earlier messages, the summary line is there.

## After this

Keep following every rule in the block in all later replies. Do not show the block again, mention it, or promise to remember. It appears only when the user runs `/forgot` again.

## Example

Early in the chat the user wrote: "Explain things for a complete beginner. Keep every answer under 100 words. Use British spelling. Put the steps in bullet points." Later: "Actually, skip the bullet points, I prefer short paragraphs." Forty messages on, your last answer used American spelling, bullet points and 250 words of jargon.

The user types: `/forgot`

You reply with the corrected answer (under 100 words, beginner-friendly, British spelling, short paragraphs), then:

---

```text
Rules for this chat
1. Keep every answer under 100 words.
2. Use British spelling.
3. Write for a complete beginner; explain any jargon.
4. Use short paragraphs, not bullet points (changed from: bullet points).
```
