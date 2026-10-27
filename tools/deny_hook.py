#!/usr/bin/env python3
"""Return a denial for an already matched tool call. No file or network access."""
import argparse
import json


def decision(runtime):
    reason = "This review returns work to its owner. Use the separately approved final-action route."
    if runtime in ("claude-code", "codex"):
        return {"hookSpecificOutput": {"hookEventName": "PreToolUse",
                "permissionDecision": "deny", "permissionDecisionReason": reason}}
    if runtime == "grok-build":
        return {"decision": "deny", "reason": reason}
    raise ValueError("unsupported runtime")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runtime", choices=["claude-code", "codex", "grok-build"],
                        required=True)
    args = parser.parse_args()
    print(json.dumps(decision(args.runtime)))


if __name__ == "__main__":
    main()
