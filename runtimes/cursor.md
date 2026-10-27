# Use Cursor for a focused task

These resources target Cursor Desktop's local Agent. Begin with the role that matches the job.

## Source finder, reviewer or finisher

[verified — Cursor documentation] Custom subagents use Markdown files with YAML frontmatter in `.cursor/agents/` for a project or `~/.cursor/agents/` for personal use. `readonly: true` restricts file edits and state-changing shell commands. `model: inherit` selects the parent model. [Subagents](https://cursor.com/docs/subagents).

| Copy after approval | Task |
|---|---|
| [source-finder.md](../setup/cursor/source-finder.md) | Locate exact quotes and corrections |
| [reviewer.md](../setup/cursor/reviewer.md) | Compare the work with the request |
| [finisher.md](../setup/cursor/finisher.md) | Make authorized revisions |

Preserve existing files. Invoke `/source-finder`, `/reviewer` or `/finisher` with the actual sources and assignment. Inspect the task card for the selected agent and model. For a cheaper model, select a supported account model and check the [source-finder example](../examples/source-finder/expected.md) before using it on larger work.

## Optional local MCP recipient guard

The [review guard](../setup/cursor/review_guard.py) inspects calls through the local `beforeMCPExecution` event. It allows explicitly listed reads, checks mapped recipient fields, and asks about other well-formed MCP calls. Malformed input, missing identities, blocked tools and disallowed recipients are denied. A mapped send with approved recipients still asks the owner.

The starting policy asks about every well-formed call. The assistant fills the policy using the actual connected tool schemas and the owner's chosen recipients.

| Supplied file | Project destination |
|---|---|
| [hooks.json](../setup/cursor/hooks.json) | Merge into `.cursor/hooks.json` |
| [review_guard.py](../setup/cursor/review_guard.py) | `.cursor/hooks/review_guard.py` |
| [review-policy.json](../setup/cursor/review-policy.json) | `.cursor/hooks/review-policy.json` |

[verified — Cursor documentation] Project commands run from the project root; personal hooks run from `~/.cursor`. Use the actual installed Python executable in the command. The supplied project command uses `python3`; on a Windows setup where `python` is the available command, change that field before saving. The entry requests `failClosed: true`. [Hooks](https://cursor.com/docs/hooks).

## Map the exact schema

`read_tools` and `blocked_tools` contain observed `server` and `tool` identities. Each `send_tools` entry also includes `recipient_fields` for every top-level recipient field, including Cc/Bcc, and `input_fields` for every accepted top-level argument. Unexpected arguments are denied so a changed schema gets reviewed.

`allowed_recipients` contains the owner's exact approved email addresses. The script accepts plain address strings or lists of plain strings. Display names, comma-separated strings and nested address objects need a reviewed adapter. Tool inputs containing only a draft/message ID belong in `blocked_tools` for this workflow, because the call lacks current recipient details.

Review the mapping when a provider changes its schema. A prompt on an unknown tool leaves its decision with the owner; recipient validation applies only to mapped send tools.

## Apply and check

Show the complete merged hook, script and policy before installation. After approval, save them and inspect Cursor's Hooks settings/output. Exercise a harmless covered call and a denied case with a non-sending test tool or isolated target. Read back the active configuration and observe the decision.

The guard reads JSON and emits a decision to standard output. Its tests cover malformed inputs, schema changes, recipient fields and policy handling; see [TESTING.md](../TESTING.md).

Coverage applies to the local MCP event. Shell, browser and other assistants use separate controls. Protect important policy files with the environment's filesystem permissions. Factual accuracy and attachments require their own review.

[verified — Cursor documentation] Cloud event coverage differs, and early cloud exploration runs without hooks. Select the supported cloud event and decision semantics when configuring a cloud project. [Local and cloud coverage](https://cursor.com/docs/hooks).
