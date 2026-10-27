import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools/check_report.py"
spec = importlib.util.spec_from_file_location("report", SCRIPT)
report = importlib.util.module_from_spec(spec)
spec.loader.exec_module(report)
BASE = json.loads((ROOT / "examples/report/valid.json").read_text())


class ReportTests(unittest.TestCase):
    def test_valid(self):
        self.assertTrue(report.evaluate(BASE, "2026-09")["passed"])

    def test_wrong_period(self):
        self.assertFalse(report.evaluate(BASE, "2026-10")["passed"])

    def test_wrong_percentage(self):
        data = dict(BASE, reported_change_percent=21)
        self.assertFalse(report.evaluate(data, "2026-09")["passed"])

    def test_missing_reference(self):
        self.assertFalse(report.evaluate(dict(BASE, sources=[]), "2026-09")["passed"])

    def test_zero_baseline(self):
        data = dict(BASE, previous=0, reported_change_percent=None)
        result = report.evaluate(data, "2026-09")
        self.assertTrue(result["passed"])
        self.assertEqual(result["absolute_change"], 120)
        self.assertFalse(report.evaluate(dict(data, reported_change_percent=0), "2026-09")["passed"])

    def test_leap_and_year_boundaries(self):
        self.assertEqual(report.month_bounds("2024-02")[1], "2024-02-29")
        self.assertEqual(report.month_bounds("2026-01")[2:], ("2025-12-01", "2025-12-31"))

    def test_half_up(self):
        data = dict(BASE, previous=4000, current=4002, reported_change_percent=0.1)
        self.assertTrue(report.evaluate(data, "2026-09")["passed"])

    def test_invalid_values(self):
        for value in (-1, True, "100", 1.5, 10**16):
            with self.subTest(value=value):
                self.assertFalse(report.evaluate(dict(BASE, current=value), "2026-09")["passed"])
        for value in (True, "20", float("inf"), float("nan")):
            self.assertFalse(report.evaluate(dict(BASE, reported_change_percent=value), "2026-09")["passed"])

    def test_invalid_periods(self):
        for period in ("2026-13", "26-09", "0000-01", "2026-00", "2026-9", "2026-09\n"):
            with self.subTest(period=period), self.assertRaises(ValueError):
                report.month_bounds(period)

    def test_missing_and_unknown_fields(self):
        data = copy.deepcopy(BASE)
        del data["sources"]
        self.assertFalse(report.evaluate(data, "2026-09")["passed"])
        self.assertFalse(report.evaluate(dict(BASE, approved=True), "2026-09")["passed"])

    def test_duplicate_and_nonfinite_json(self):
        for raw in ('{"current":1,"current":2}', '{"current":NaN}'):
            with self.assertRaises(ValueError):
                report.decode(raw)

    def test_input_identity_changes(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "report.json"
            raw = json.dumps(BASE).encode()
            path.write_bytes(raw)
            first = report.inspect_file(path, "2026-09")
            self.assertEqual(first["input_sha256"], hashlib.sha256(raw).hexdigest())
            path.write_text(json.dumps(dict(BASE, current=125)))
            second = report.inspect_file(path, "2026-09")
            self.assertNotEqual(first["input_sha256"], second["input_sha256"])
            self.assertFalse(second["passed"])

    def test_real_cli_status_and_errors(self):
        for name, code in (("valid.json", 0), ("wrong-month.json", 1), ("wrong-percentage.json", 1)):
            run = subprocess.run([sys.executable, "-B", str(SCRIPT),
                                  str(ROOT / "examples/report" / name), "--period", "2026-09"],
                                 capture_output=True, text=True)
            self.assertEqual(run.returncode, code, run.stderr)
            self.assertEqual(json.loads(run.stdout)["passed"], code == 0)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.json"
            path.write_text("{secret-invalid")
            run = subprocess.run([sys.executable, "-B", str(SCRIPT), str(path),
                                  "--period", "2026-09"], capture_output=True, text=True)
            self.assertEqual(run.returncode, 2)
            self.assertNotIn("secret-invalid", run.stdout + run.stderr)

    def test_oversized_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "large.json"
            path.write_bytes(b" " * (report.MAX_BYTES + 1))
            with self.assertRaises(ValueError):
                report.inspect_file(path, "2026-09")


if __name__ == "__main__":
    unittest.main()
