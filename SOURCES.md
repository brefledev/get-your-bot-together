# Sources and supported scope

Product documentation checked **27 October 2026**. During setup, inspect the installed version, available account features and actual execution route.

| Resource | Primary documentation |
|---|---|
| Grok Bot entry, rules and reusable work | [Tag @bot](https://docs.x.ai/grok-bot/tag-on-x) · [Approvals](https://docs.x.ai/grok-bot/approvals-security-and-privacy) · [Computers](https://docs.x.ai/grok-bot/computer-and-apps) · [Skills and routines](https://docs.x.ai/grok-bot/skills-routines-and-automations) |
| ChatGPT Dot controls and tasks | [Controls](https://learn.chatgpt.com/docs/dots/controls) · [Tasks and memory](https://learn.chatgpt.com/docs/dots/tasks-and-memory) |
| Claude Code instructions, roles and skills | [Memory](https://code.claude.com/docs/en/memory) · [Subagents](https://code.claude.com/docs/en/sub-agents) · [Skills](https://code.claude.com/docs/en/skills) · [Hooks](https://code.claude.com/docs/en/hooks) |
| Codex configuration and execution | [Profiles](https://learn.chatgpt.com/docs/config-file/config-advanced) · [Custom agents](https://learn.chatgpt.com/docs/agent-configuration/subagents) · [CLI](https://learn.chatgpt.com/docs/cli/reference) · [Hooks](https://learn.chatgpt.com/docs/hooks) · [Scheduled tasks](https://learn.chatgpt.com/docs/automations) |
| Cursor local roles and hooks | [Subagents](https://cursor.com/docs/subagents) · [Hooks](https://cursor.com/docs/hooks) |
| Grok Build execution and hooks | [Settings](https://docs.x.ai/build/settings) · [Headless CLI](https://docs.x.ai/build/cli/headless-scripting) · [Hook reference](https://github.com/xai-org/grok-build/blob/main/crates/codegen/xai-grok-pager/docs/user-guide/10-hooks.md) |
| Muse controls | [Permissions](https://www.meta.com/help/superintelligence/1385290430137537/) · [Memory](https://www.meta.com/help/superintelligence/995796179982326/) |
| Duet controls | [Getting started](https://support.claude.com/en/articles/17631495-get-started-with-claude-duet) · [Safety and privacy](https://claude.com/resources/articles/claude-duet-safety-privacy-and-security) |
| Email identity and access | [Gmail drafts](https://developers.google.com/workspace/gmail/api/guides/drafts) · [Gmail scopes](https://developers.google.com/workspace/gmail/api/auth/scopes) |

## Match the configuration to its runtime

[verified — documentation above]

- Codex named CLI profiles and custom agents use separate top-level TOML files for different purposes. Agent permissions come from the parent session.
- Claude Code subagent `tools` restricts its available tools. A skill's `allowed-tools` grants permission for listed tools during invocation; those fields have different jobs.
- Cursor's supplied recipient guard targets local `beforeMCPExecution` with JSON-string `tool_input`. Its configuration uses `failClosed: true`.
- Claude Code, Codex and Grok Build use their own hook response formats. The generator selects the format through `--runtime`.

Each setup guide includes a saved-configuration check and a harmless runtime exercise. [TESTING.md](TESTING.md) describes the executable checks, fixtures and expected results. Product controls determine the installed route's behavior; the owner chooses which resources to adopt.
