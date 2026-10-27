# Use Grok Build for a focused task

Grok Build can work from a prepared project and [handoff](../templates/HANDOFF.md). Use the [source finder](../agents/source-finder.md), [reviewer](../agents/reviewer.md), or [finishing procedure](../setup/finish-work.md) as the task instruction.

## Prepare the actual workspace

[verified — xAI documentation] Inspect the installed CLI, authentication, directory and supported settings on the execution computer. `grok inspect` and `/settings` expose configuration. Keep credentials out of logs. [Settings](https://docs.x.ai/build/settings).

The assistant should place the actual draft and source files in the approved workspace. For a local job, a cloud path needs a supported file transfer before the worker can read its contents.

In PowerShell or a POSIX terminal, open the approved project containing `review/HANDOFF.md`. This launches a headless task:

```text
grok --no-auto-update --cwd . -p "Read review/HANDOFF.md. Finish the authorized work and return the artifact." --output-format json
```

[verified — xAI documentation] This route requires an installed, authenticated CLI and authorized command execution. [Headless CLI](https://docs.x.ai/build/cli/headless-scripting).

Keep the current model and effort unless the owner chooses a change. Inspect the completed artifact, sources and checks. A repeatable procedure can use the supported [skills mechanism](https://docs.x.ai/build/features/skills-plugins-marketplaces).

## Add a small pre-action check

The [hook recipe](../recipes/useful-hooks.md) generates an exact-tool proposal with `--runtime grok-build`. It uses the same readable denial script with Grok Build's response format.

[verified — xAI hook reference] Personal definitions live under `~/.grok/hooks/`. Project definitions under `.grok/hooks/` require trust. `PreToolUse` uses `toolName` and `toolInput`, and the denial response is `{"decision":"deny","reason":"..."}`. `/hooks` shows loaded sources. [Hook reference](https://github.com/xai-org/grok-build/blob/main/crates/codegen/xai-grok-pager/docs/user-guide/10-hooks.md).

Show the complete merged configuration before installation. Verify a harmless matching tool call is denied in the intended session. Ordinary hook errors and timeouts allow execution to continue; a required final-action restriction belongs in the destination or credential permissions as well.

## Use it from Grok Bot

[verified — xAI documentation] Local computer access is a separately enabled route. An authorized Bot can use an available command route on that computer. [Computer access](https://docs.x.ai/grok-bot/computer-and-apps).

When command access is unavailable, the Bot can return the prepared handoff for the owner's existing worker, or complete the task in the conversation. Choose the route that delivers the useful result with the available access.
