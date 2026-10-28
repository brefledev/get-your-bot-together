# Checks and examples

On 27 October 2026, the local Windows/Python 3.11.15 run completed with 64 passing cases and one POSIX-shell execution case selected for POSIX hosts. The resource check passed for 56 Markdown files, 203 local links, five JSON files, four TOML files and nine role definitions. [verified — commands below]

The executable checks use Python 3.11 or later and its standard library. Run them from the downloaded repository folder in PowerShell or a POSIX terminal. Use the Python command installed on your computer.

## Run the suite

```text
python -B -m unittest discover -s tests -v
```

The suite exercises report calculations, calendar boundaries, invalid inputs, hook JSON, exact tool matching, shell quoting, recipient policy decisions and the scripts' actual command-line entrypoints. Native command execution uses the host's shell: PowerShell on Windows, POSIX shell on Linux/macOS. Each host skips the other shell's execution case.

Check the resource files:

```text
python -B tools/check_resources.py
```

This checks local Markdown links and headings, HTML image sources, JSON/TOML syntax, required fields in the supplied agent definitions, and common private-path or credential patterns in public resources. Success returns `"passed": true` with checked counts. Review content and privacy as part of every contribution.

The [CI workflow](.github/workflows/checks.yml) runs both commands on Windows and Ubuntu with Python 3.11 and 3.13.

## Try useful examples

| Example | Expected result |
|---|---|
| [Valid September report](examples/report/valid.json) | Correct months, 120 versus 100, +20.0% |
| [Wrong month](examples/report/wrong-month.json) | Reject the reporting period |
| [Wrong percentage](examples/report/wrong-percentage.json) | Reject the claimed change |
| [Source finder](examples/source-finder/notes.md) | Exact quotes, latest owner correction, quoted third-party instruction identified |
| [Reviewer: complete](examples/reviewer/complete.md) | Report that the supplied criteria are met |
| [Reviewer: needs work](examples/reviewer/needs-work.md) | Identify the wrong comparison month and unsupported causal claim |
| [Improvement conversation](examples/newsletter-session.md) | Specific proposed files, owner choice and an observable check |

The report fixtures run through [check_report.py](tools/check_report.py). The source-finder and reviewer examples are task/expected-answer pairs for evaluating the actual assistant and model you choose. Use the [expected source-finder answer](examples/source-finder/expected.md) and [expected reviewer findings](examples/reviewer/expected.md).

## Verify an adopted configuration

After the owner approves a change:

1. Read back the saved file or setting and compare it with the proposal.
2. Confirm the intended app, project, role, model and loaded configuration.
3. Exercise a harmless case that should pass and a case the chosen control should reject.
4. Run the real task and inspect the resulting artifact against its acceptance criteria.

Use an isolated tool or destination for a sending-related check. Keep the test within the owner's approved scope. The [runtime guides](README.md#use-your-existing-tools) provide the relevant paths and inspection steps.

For generated or copied instructions, compare the affected source, generated output and installed files in one scoped pass. Record file agreement separately from observed loading and behavior. An unchanged file can reuse its existing evidence; repeat a check after a relevant change, failure or unresolved concern. This keeps stale copies visible without repeatedly sending the same trial to every bot.

On 28 October 2026, the project-home, handoff and configuration-check guidance was expanded to cover instruction propagation, concise operating rules and continuity ownership. The resource check passed for 56 Markdown files, 203 local links, five JSON files, four TOML files and nine role definitions. The existing script-suite result retains its October 27 date.

A useful first conversation should also handle a user with no project or GitHub account, unavailable chat history, conflicting existing instructions, declined changes and missing tool access. [START-HERE.md](START-HERE.md) gives the response procedure: use accessible evidence, show a concrete proposal, preserve the owner's choice and return a usable next step.

## Template usability revision, 28 October 2026

The proposed PROJECT, HANDOFF and PROCEDURE revisions include context-first filling instructions and compact fictional examples. A single scoped resource/content check passed for these three templates, the handoff recipe alignment and this record: base-file identities, allowed changed paths, local link targets, public-content hygiene, required template guidance and patch application against the reviewed base. No executable configuration changed; the script suite and live bot trials were not rerun. The examples explain usage rather than requiring additional practice tasks.
