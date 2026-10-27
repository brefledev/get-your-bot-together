# Claude Code: project instructions and focused workers

Use this guide in the actual local Claude Code project. Inspect existing instructions and settings before adding a file.

## Project instructions

[verified — Claude Code documentation] Current [instruction loading](https://code.claude.com/docs/en/memory#agents-md) can read AGENTS.md directly in eligible sessions from version 2.1.277. Existing CLAUDE.md or CLAUDE.local.md files and the Project instructions setting affect which files load.

Start with the project's existing convention. For a shared AGENTS.md setup, inspect the actual selection. Where an import is appropriate, [the CLAUDE.md template](../templates/CLAUDE.md) contains `@AGENTS.md`. Merge useful instructions into the existing project; preserve current content.

Inspect the loaded sources and exercise one harmless project convention. The [project-home recipe](../recipes/project-home.md) supplies a complete small layout.

## Choose a focused role

Copy only the approved role into the chosen project's .claude/agents/ folder:

| Supplied role | Project destination | Scope |
|---|---|---|
| [Source finder](../setup/claude-code/agents/source-finder.md) | .claude/agents/source-finder.md | Read, Grep and Glob; Sonnet selected |
| [Reviewer](../setup/claude-code/agents/reviewer.md) | .claude/agents/reviewer.md | Read, Grep and Glob; inherited model |
| [Finisher](../setup/claude-code/agents/finisher.md) | .claude/agents/finisher.md | File reading and editing; inherited model |

[verified — [subagent documentation](https://code.claude.com/docs/en/sub-agents)] The tools field selects the role's available tools. These examples use local file tools. The source finder deliberately selects Sonnet; explain the model choice and confirm availability before saving. The review and finishing roles inherit the parent model.

In Claude Code, ask for the named role with the assignment and actual accessible files. Inspect the selected role and its tools. Use the [source fixture](../examples/source-finder/notes.md) or [review fixture](../examples/reviewer/brief.md) to check the result. The finisher's file-tool set suits document edits; add execution tools only when the task calls for them and the owner approves that scope.

A role file can be removed to undo the addition. Restore an existing file from its saved copy when replacing one.

## Save a repeated procedure

The included [project-brief skill](../setup/claude-code/skills/project-brief/SKILL.md) can be copied to .claude/skills/project-brief/SKILL.md after review. It supports an explicit `/project-brief` invocation and returns a concise, sourced project brief.

Adapt its source scope and output requirements to the actual job. [verified — [skills documentation](https://code.claude.com/docs/en/skills)] Claude Code uses skill metadata to control discovery and invocation. Review the available entry, invoke it on the chosen files, and inspect its result before using it routinely.

## Add a scoped hook

The [exact-tool hook recipe](../recipes/useful-hooks.md) prepares a complete PreToolUse entry and script. Merge the entry into .claude/settings.json, inspect it with /hooks, and trigger a harmless matched call.

[verified — [hook reference](https://code.claude.com/docs/en/hooks)] PreToolUse supports a denial before the matched tool runs. PostToolUse runs after the tool. Each event has its own output and exit behavior.

Keep the selected script at its approved path. Test normal behavior, a denied event and an internal failure in an isolated example. Final-action permissions belong to the actual service and execution paths.
