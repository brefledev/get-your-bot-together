# Use Codex for a focused task

Choose a source finder, reviewer, or finisher according to the work. Start with the [role guide](../agents/README.md) and a [complete handoff](../templates/HANDOFF.md).

## Add a role to a project

[verified — Codex documentation] Custom agents use standalone TOML files under `.codex/agents/` in a project, or `~/.codex/agents/` for personal use. Required fields are `name`, `description` and `developer_instructions`. They inherit the parent session's permissions. [Custom agents](https://learn.chatgpt.com/docs/agent-configuration/subagents).

| Copy this file after approval | Purpose |
|---|---|
| [source-finder.toml](../setup/codex/source-finder.toml) | Return exact quotes and file locations |
| [reviewer.toml](../setup/codex/reviewer.toml) | Compare an artifact with the request |
| [finisher.toml](../setup/codex/finisher.toml) | Make authorized revisions and return the work |

Show the selected file and destination, preserve an existing definition, then ask the parent session to use the named role. Inspect the selected agent and its actual model. The source finder's instruction asks it to leave files unchanged; enforce filesystem access with the parent sandbox and control connected apps separately.

For a cheaper worker, propose a model available in the owner's account and compare its result with the [source-finder example](../examples/source-finder/expected.md). Exact quotation and correction handling decide whether the choice works.

## Use a separate finishing session

[verified — Codex documentation] A named CLI profile is a top-level file such as `~/.codex/finisher.config.toml`, selected with `--profile finisher`. [Profiles](https://learn.chatgpt.com/docs/config-file/config-advanced).

The supplied [finisher.config.toml](../setup/codex/finisher.config.toml) requests workspace edits and on-request approvals. Show the owner the merged profile before saving it. Keep the existing model, effort, credentials and unrelated settings.

In PowerShell or a POSIX terminal, open the approved project containing the prepared `review/HANDOFF.md`. This command launches an interactive finishing session:

```text
codex --profile finisher -C . "Read review/HANDOFF.md and finish."
```

The CLI must be installed and authenticated. The handoff carries the complete scope and output location. Inspect the returned file and actual checks. [CLI reference](https://learn.chatgpt.com/docs/cli/reference).

A Dot's task tool exposes its own launch options. Use a route that can select the intended configuration, then inspect what it selected. Local computer selection, CLI profile selection and hook loading are separate settings.

## Add an exact tool check

The shared [hook recipe](../recipes/useful-hooks.md) uses [make_hook.py](../tools/make_hook.py) with `--runtime codex` and the observed canonical tool name. It supports PowerShell and POSIX command generation. Merge the proposal into the selected `hooks.json` after approval.

[verified — Codex documentation] Codex `PreToolUse` supports a `deny` response. Its supported response values exclude `ask`; an unsupported value can fail while the call continues. Use `/hooks` to inspect and trust the current definition, then verify a harmless covered denial. [Hooks](https://learn.chatgpt.com/docs/hooks).

Coverage follows the exact named tool on that execution route. Credential and destination permissions control other routes. For recurring drafts, use the [scheduled review guide](scheduled-codex.md).
