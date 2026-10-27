import base64
import importlib.util
import json
from pathlib import Path
import re
import shlex
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]


def module(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "tools" / (name + ".py"))
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


maker = module("make_hook")
denier = module("deny_hook")


class HookTests(unittest.TestCase):
    def test_exact_escaped_match(self):
        entry = maker.render("codex", "posix", ["mcp__mail__send.email", "Write", "Write"],
                             "/usr/bin/python3", "/tmp/a script.py")["hooks"]["PreToolUse"][0]
        regex = entry["matcher"]
        self.assertIsNotNone(re.fullmatch(regex, "mcp__mail__send.email"))
        self.assertIsNone(re.fullmatch(regex, "mcp__mail__sendXemail"))
        self.assertIsNone(re.fullmatch(regex, "prefixWrite"))
        self.assertEqual(shlex.split(entry["hooks"][0]["command"]),
                         ["/usr/bin/python3", "/tmp/a script.py", "--runtime", "codex"])

    def test_powershell_literal_paths(self):
        path = "C:/a folder/it's $(literal)/deny.py"
        entry = maker.render("claude-code", "powershell", ["Write"],
                             "C:/Python/python.exe", path)["hooks"]["PreToolUse"][0]
        command = entry["hooks"][0]["command"]
        decoded = base64.b64decode(command.split()[-1]).decode("utf-16-le")
        self.assertEqual(decoded,
                         "& 'C:/Python/python.exe' 'C:/a folder/it''s $(literal)/deny.py' '--runtime' 'claude-code'")

    def test_reject_invalid_configuration(self):
        for names, python, script in (([], "/usr/bin/python3", "/tmp/a"),
                                      (["bad\nname"], "/usr/bin/python3", "/tmp/a"),
                                      (["Write"], "python3", "/tmp/a"),
                                      (["Write"], "/usr/bin/python3", "relative.py")):
            with self.assertRaises(ValueError):
                maker.render("codex", "posix", names, python, script)

    def test_runtime_responses(self):
        for runtime in ("claude-code", "codex", "grok-build"):
            run = subprocess.run([sys.executable, "-B", str(ROOT / "tools/deny_hook.py"),
                                  "--runtime", runtime], input='{"approved":true}',
                                 text=True, capture_output=True)
            self.assertEqual(run.returncode, 0)
            response = json.loads(run.stdout)
            actual = (response["decision"] if runtime == "grok-build"
                      else response["hookSpecificOutput"]["permissionDecision"])
            self.assertEqual(actual, "deny")
            self.assertEqual(run.stderr, "")

    @unittest.skipUnless(sys.platform == "win32", "Windows command execution")
    def test_generated_powershell_command_executes(self):
        script = str(ROOT / "tools/deny_hook.py")
        entry = maker.render("claude-code", "powershell", ["Write"],
                             sys.executable, script)["hooks"]["PreToolUse"][0]
        command = entry["hooks"][0]["command"].split()
        run = subprocess.run(command, input="{}", text=True, capture_output=True)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(json.loads(run.stdout)["hookSpecificOutput"]["permissionDecision"], "deny")

    @unittest.skipIf(sys.platform == "win32", "POSIX command execution")
    def test_generated_posix_command_executes(self):
        entry = maker.render("grok-build", "posix", ["write_file"],
                             sys.executable, str(ROOT / "tools/deny_hook.py"))["hooks"]["PreToolUse"][0]
        run = subprocess.run(["/bin/sh", "-c", entry["hooks"][0]["command"]],
                             input="{}", text=True, capture_output=True)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(json.loads(run.stdout)["decision"], "deny")


if __name__ == "__main__":
    unittest.main()
