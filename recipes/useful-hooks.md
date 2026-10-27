# Add a useful hook

**Use this when:** the same exact action or check should happen at a supported point in the app's work.
**Leave with:** one scoped configuration, a script, and an observed example.

Choose the job first. A hook is code your selected app runs when a supported event happens.

| Job | Useful event | Resource |
|---|---|---|
| Keep edited files consistently formatted | After an edit | [Claude Code formatting examples](https://code.claude.com/docs/en/hooks-guide), [Cursor afterFileEdit](https://cursor.com/docs/hooks) |
| Tell you when input is needed | Notification event | [Claude Code notifications](https://code.claude.com/docs/en/hooks-guide#get-notified-when-claude-needs-input) |
| Check a report's exact fields | A defined validation step before returning it | [Working report checker](check-a-report.md) |
| Keep a named final-action tool outside a review session | Before that exact tool call | The exact-tool example below |
| Inspect recipients on a local Cursor MCP route | Before the mapped MCP call | [Advanced recipient guard](../runtimes/cursor.md) |

For formatting and notifications, adapt the official example to the actual operating system and existing formatter. Explain its effect before saving it. A report check can be run directly before choosing automation.

## Exact-tool denial

The [generator](../tools/make_hook.py) prints a configuration entry for Claude Code, Codex or Grok Build. The [denial script](../tools/deny_hook.py) returns that runtime's documented denial response.

The assistant inspects the actual tool inventory and chooses exact canonical names. The matcher selects those calls. The script performs no file writes or network operations.

From the repository folder, this PowerShell example prepares a Claude Code proposal that denies the Write tool:

```powershell
python tools/make_hook.py --runtime claude-code --shell powershell --tool Write
```

For a POSIX shell, use `--shell posix`. For Codex or Grok Build, use the matching `--runtime` value and an observed tool name. Defaults point at the current Python interpreter and the included script; `--python` and `--script` accept the actual absolute destinations.

PowerShell proposals invoke an encoded command. Decode the proposal during review or inspect the generator and the actual interpreter/script paths. The command contains those paths and the selected runtime. The script's sole job is to return a denial.

## Save the chosen configuration

| Runtime | Project configuration | Review/loading step |
|---|---|---|
| Claude Code | Merge the entry into .claude/settings.json | Use /hooks and inspect the selected entry |
| Codex | Merge into .codex/hooks.json | Use /hooks to review and trust the definition |
| Grok Build | Save a named JSON file in .grok/hooks/ | Review project trust and inspect /hooks |

Preserve existing configuration. Keep the script at the approved absolute location or regenerate the entry after moving it. These are local command-hook examples. Follow each runtime guide for its working environment and trust rules.

## Check the actual event

Use a harmless scratch file and a tool matching the selected name. Inspect the denial and confirm that the file stayed unchanged. Also try an unrelated harmless permitted action. For failure behavior, temporarily select a missing script in the isolated example and observe how the app handles that failure; then restore the working entry.

[verified — vendor references] Ordinary hook failures can allow continuation in [Grok Build](https://github.com/xai-org/grok-build/blob/main/crates/codegen/xai-grok-pager/docs/user-guide/10-hooks.md) and covered [Codex paths](https://learn.chatgpt.com/docs/hooks). A valid denial controls the matched call. Other tools and credentials have their own permissions.

To remove the hook, restore the previous configuration or remove this exact entry, then inspect the loaded hooks again. Keep the script until the configuration no longer references it.
