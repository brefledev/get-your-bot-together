# Check a monthly report

**Use this when:** a monthly report needs a repeatable check of dates and arithmetic.
**Leave with:** a result naming every check and the input bytes examined.

The included [Python checker](../tools/check_report.py) compares the supplied reporting dates with the month you requested, checks the preceding comparison month, requires non-negative integer counts and source references, and recalculates the percentage change.

It uses one decimal place with half-up rounding. A zero prior count produces an absolute change and requires a null percentage.

## Try the working example

Requires Python 3.11 or later. In PowerShell, Terminal or a shell, open the downloaded repository folder. Use your installed Python command; the examples use `python`.

```text
python tools/check_report.py examples/report/valid.json --period 2026-09
```

The result includes `"passed": true` and a computed change of 20.0.

Now try the deliberately shortened reporting period:

```text
python tools/check_report.py examples/report/wrong-month.json --period 2026-09
```

The result includes `"passed": false` and the expected September 30 end date. The command exits 1 for a failed check. Invalid input exits 2. A passing check exits 0.

## Use your own values

Copy [valid.json](../examples/report/valid.json) into your private project and adapt its fields. Give the checker the expected month separately from the report. Use the exact original source values.

The output includes a SHA-256 identifier for the file examined. Run the check again after the input changes. The code checks the supplied fields and arithmetic; source authenticity, metric definitions, explanations and the final document remain separate review requirements.

## Put the result to work

Have the assistant correct a failed input from the original sources, then run the check again. Keep the result beside the draft. A publishing workflow should apply its own owner-approved completion and destination controls.

The script reads one local file and prints a result. Use the [report handoff](../examples/report/HANDOFF.md) to pass the example to another worker.
