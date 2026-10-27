# Reusable roles

| Role | Job | Output |
|---|---|---|
| [Source finder](source-finder.md) | Find relevant original wording | Exact quotes and locations |
| [Reviewer](reviewer.md) | Compare the actual work with the assignment | Material findings or a clean review |
| [Finisher](../setup/finish-work.md) | Make authorized revisions and checks | The complete revised artifact |

Use a role directly in a chat, or install the matching example in your chosen runtime after reviewing its scope.

## Configuration examples

- Claude Code: [source finder](../setup/claude-code/agents/source-finder.md), [reviewer](../setup/claude-code/agents/reviewer.md), [finisher](../setup/claude-code/agents/finisher.md).
- Codex: [source finder](../setup/codex/source-finder.toml), [reviewer](../setup/codex/reviewer.toml), [finisher](../setup/codex/finisher.toml).
- Cursor: [source finder](../setup/cursor/source-finder.md), [reviewer](../setup/cursor/reviewer.md), [finisher](../setup/cursor/finisher.md).

Each runtime guide explains destination, loading and permissions. Role instructions describe behavior. The runtime's tool restrictions, parent permissions and credentials establish available actions.

For bounded retrieval, compare an available lower-cost model on the [quote fixture](../examples/source-finder/notes.md). Inspect the selected model and verify exact quotes. Keep high-judgment review on a model suited to the task.
