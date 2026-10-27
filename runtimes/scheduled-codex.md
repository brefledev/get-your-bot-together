# Have Codex review recurring drafts

Use a schedule when drafts arrive repeatedly and you want revised work waiting for you. Start by running the procedure once on an actual draft.

## Prepare the project and prompt

Choose an existing private project. Show the owner the input folder, output folder, cadence, time zone, model, source access and permission settings before creating the task.

A practical arrangement is:

```text
review/
  HANDOFF.md
  input/
  output/
```

Adapt this saved prompt to the actual project:

> Read review/HANDOFF.md, the current draft, the owner's corrections and the original sources. Compare the current input identity with the last completed review. Reuse the existing result when the inputs are unchanged. If another run is active or files are being replaced, report the conflict and preserve the current work.
>
> Check the required facts, calculations and acceptance criteria. Make the authorized revisions and preserve review/input. Save the complete artifact in review/output with its input identity, material changes and performed checks. Keep owner-edited outputs intact by saving a distinct revision. Report precise missing inputs or failed checks. Return the draft for owner review; additional external actions require their applicable authorization.

Include the relevant [email](../workflows/draft-to-finish.md), [article](../workflows/editorial.md) or [report](../workflows/reports-and-code.md) procedure.

## Create and verify the task

[verified — OpenAI documentation] Local scheduled tasks require the app, computer and project to remain available. Scheduled runs have their own permission settings and can run without interactive approval. [Scheduled tasks](https://learn.chatgpt.com/docs/automations).

1. Run the prompt on the real draft and inspect the result.
2. Use the desktop app's supported scheduled-task flow and the owner's chosen project and cadence.
3. Inspect the saved prompt, source access, permissions and output location.
4. Inspect the first scheduled run and its resulting file. Verify any required hooks through that execution route.

Select local-project mode for the shared private layout above. A worktree needs an explicit route to inputs held in another checkout. A CLI profile also needs explicit selection through a route that supports it.

Keep one writer responsible for an output. The unchanged-input check reduces repeated work; the destination's records resolve uncertain external actions. When the computer will be offline, use on-demand review or a separately configured cloud workflow.
