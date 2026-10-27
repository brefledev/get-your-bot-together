# Improve a task with your ChatGPT Dot

Give the Dot [START-HERE.md](../START-HERE.md) and one example of the work you want to improve. A recurring correction can become a [short procedure](../recipes/repeated-mistakes.md); scattered work can use a [project home](../recipes/project-home.md); a new task can start with a [complete handoff](../recipes/handoff.md).

## Choose the behavior you want

For someone who wants to inspect client emails before sending, propose:

**Action:** Send an external email to a client on my behalf.  
**Behavior:** Ask before taking action.

[verified — OpenAI documentation] Custom rules are under Settings → Personalization → Permissions on desktop/web, and Customize → Custom rules on mobile. **Hand off to you** reserves the action for the owner. **Take action when you say so** and **Take action without asking** provide other choices. Rules guide behavior and may make mistakes; connected-app permissions apply separately. [Dot controls](https://learn.chatgpt.com/docs/dots/controls).

Inspect existing entries, explain the exact proposed change and save it through the supported editor after approval. Confirm the saved behavior. A matching working instruction could be:

> Prepare the full client email from the authorized sources. Check recipient identity, commitments and attachments. Return the subject, body and attachment list. Save an unsent draft when I authorize that step. Keep the send for my review under my chosen action rule.

Use the [email workflow](../workflows/draft-to-finish.md) when this addresses the owner's actual task. A one-off writing instruction can stay in the current conversation.

## Prepare a worker's task

[verified — OpenAI documentation] Dots can work with local tasks and prepared Codex cloud environments. Discover the available environment and launch options before proposing a worker. [Tasks and memory](https://learn.chatgpt.com/docs/dots/tasks-and-memory).

A local task needs files on the selected computer. A cloud task needs transferred files or an accessible repository. Include the original request, current draft, later corrections, source material, approved work and expected output.

Use [Codex roles and profiles](../runtimes/codex.md) when the selected route can load them. Inspect the actual selection. The Dot can also prepare work for [Claude Code](../runtimes/claude-code.md) or another environment the owner already uses, through an available authorized route.

Open the returned artifact, check that it fulfills the request, and resolve defects within scope. For recurring work, separately agree the project and cadence in the [scheduled review guide](../runtimes/scheduled-codex.md).
