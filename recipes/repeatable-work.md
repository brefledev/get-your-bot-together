# Save a repeatable method

**Use this when:** you repeat a multi-step task and want a consistent method.
**Leave with:** a tailored procedure you can invoke again.

Use [PROCEDURE.md](../templates/PROCEDURE.md). Begin with a task that already produced a useful result. Capture its inputs, steps, checks, output and missing-information behavior.

## Example: a weekly project brief

> Read the approved project notes for the requested week. Identify completed work, decisions and specific blockers. Link each material claim to its source. Return a one-page brief with the next actions and owners. Keep information about other projects outside the brief. Ask about an unknown owner or date that affects the plan.

The assistant should fill the actual source locations and output convention before saving it.

## Choose a save location

A managed assistant may support a saved instruction or reusable procedure. Inspect the actual product's save mechanism. In a file project, a procedure document is a portable starting point. A [Claude Code skill](../runtimes/claude-code.md#save-a-repeated-procedure) provides a named invocation.

Saving the method records how the task works. Scheduling determines when it runs and requires an explicit cadence and action scope.

## Check and undo

Run the method on a familiar example. Then remove a required source from a copy and check that the assistant identifies the missing input without inventing a result.

Compare the finished artifact with the original task. Save the approved wording and location. To undo, restore the previous procedure or remove this one through the same save mechanism.
