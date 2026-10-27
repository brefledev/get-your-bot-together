#!/usr/bin/env python3
"""Print one proposed exact-tool hook entry; installation is a separate action."""
import argparse
import base64
import json
from pathlib import Path, PurePosixPath, PureWindowsPath
import re
import shlex
import sys


def clean(value):
    if (not isinstance(value, str) or not value or value != value.strip()
            or any(ord(c) < 32 or ord(c) == 127 for c in value)):
        raise ValueError("use nonempty values without control characters")
    return value


def ps_literal(value):
    return "'" + value.replace("'", "''") + "'"


def render(runtime, shell, names, python_path, script_path):
    if runtime not in ("claude-code", "codex", "grok-build"):
        raise ValueError("unsupported runtime")
    if shell not in ("posix", "powershell"):
        raise ValueError("choose posix or powershell")
    if not names:
        raise ValueError("supply observed exact tool names")
    names = sorted(set(clean(n) for n in names))
    python_path, script_path = clean(python_path), clean(script_path)
    path_type = PurePosixPath if shell == "posix" else PureWindowsPath
    if not all(path_type(p).is_absolute() for p in (python_path, script_path)):
        raise ValueError("interpreter and script paths must be absolute for the selected shell")
    if shell == "posix":
        command = " ".join(shlex.quote(x) for x in
                           (python_path, script_path, "--runtime", runtime))
    else:
        payload = "& " + " ".join(ps_literal(x) for x in
                                 (python_path, script_path, "--runtime", runtime))
        encoded = base64.b64encode(payload.encode("utf-16-le")).decode("ascii")
        command = "powershell.exe -NoProfile -NonInteractive -EncodedCommand " + encoded
    return {"hooks": {"PreToolUse": [{
        "matcher": "^(?:" + "|".join(re.escape(n) for n in names) + ")$",
        "hooks": [{"type": "command", "command": command, "timeout": 10}]
    }]}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runtime", required=True,
                        choices=["claude-code", "codex", "grok-build"])
    parser.add_argument("--shell", required=True, choices=["posix", "powershell"])
    parser.add_argument("--tool", action="append", required=True)
    parser.add_argument("--python", default=sys.executable)
    parser.add_argument("--script", default=str(Path(__file__).with_name("deny_hook.py").resolve()))
    args = parser.parse_args()
    try:
        print(json.dumps(render(args.runtime, args.shell, args.tool,
                                args.python, args.script), indent=2))
    except ValueError as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
