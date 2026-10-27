# Give the project a home

**Use this when:** the goal, current draft and next action keep getting lost.
**Leave with:** a short project brief and a place for the work.

Begin with [PROJECT.md](../templates/PROJECT.md). Ask your assistant to fill it from the current task and name any missing information. An ordinary chat can hold this brief until you choose persistent storage.

For a private file project, use:

```text
my-project/
  PROJECT.md
  AGENTS.md
  sources/
  work/
  output/
```

Keep source material in sources/, evolving drafts in work/, and deliverables in output/. The folders are ordinary file organization. The chosen application determines how instructions load.

## Working instructions

Adapt [AGENTS.md](../templates/AGENTS.md) after inspecting existing project instructions. Include only conventions this project needs. The [Claude Code guide](../runtimes/claude-code.md) explains its AGENTS.md and CLAUDE.md choices; the [Codex guide](../runtimes/codex.md) covers its own configuration.

A bot with limited file access can prepare the complete contents in chat. The owner can save the files or approve a supported file operation.

## Check and undo

Open the project in the selected app. Inspect its loaded instruction sources where available, then ask it to identify the current goal and draft from the actual files. Try a harmless task that uses one specific convention. Keep the observed result with the project.

A correct answer demonstrates that particular use of the instructions. Permissions and code checks handle their own boundaries.

To undo the setup, restore the prior instruction files and move new folders only after confirming their contents. Keep existing owner work.
