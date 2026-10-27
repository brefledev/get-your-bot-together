# Finish a report or a code change

Choose the procedure that fits the assignment. Both can be used directly in an existing conversation.

## A report with checked figures

> Read the original assignment, draft and source data. Confirm the client/property, periods, time zone, units and metric definitions. Recalculate material figures from original values with code or a spreadsheet. Use the agreed formula and rounding. For a zero baseline, show the absolute change and explain that percentage change is undefined.
>
> Check missing dates and denominators. Separate measured changes from proposed explanations. Revise the report into the requested format and preserve the original. Inspect the finished artifact and return it with material corrections and precise data gaps. Distribution follows the owner's applicable authorization.

The [report recipe](../recipes/check-a-report.md) includes executable calendar and percentage checks with fictional data. Adapt the schema to the actual source exports. The included source-list check verifies that references are present; a reviewer assesses whether those sources support the claims.

## A code change that satisfies the request

> Inspect the project instructions, current revision and uncommitted work. Read the original request and exact candidate. Preserve unrelated edits. Check the requested behavior, relevant failure cases and security. Reproduce material findings and fix in-scope defects.
>
> Discover the project's actual test, lint, type-check and build commands. Run the relevant checks and inspect generated UI or documents when they are the deliverable. Recheck affected behavior after a repair. Return the patch, material changes, commands and observed results. Name a specific blocker for any required check that could not run.
>
> Keep public commits, pushes, pull requests, merges, releases and deployments within the owner's explicit authorization for those actions.

An existing configured coding worker can complete the entire assignment when it has the necessary access.

[verified — GitHub documentation] Protected branches and rulesets can require checks before merging. Select the intended check producer and permissions, and review bypass access when configuring a required merge boundary. [Branch protection](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches).

A check establishes its evaluated condition. Review the actual change and authorize its destination separately.
