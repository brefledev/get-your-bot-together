#!/usr/bin/env python3
"""Check a monthly report's supplied fields and arithmetic. Standard library only."""
import argparse
import calendar
from datetime import date
from decimal import Decimal, ROUND_HALF_UP
import hashlib
import json
from pathlib import Path
import re
import sys

MAX_BYTES = 1_048_576
FIELDS = {"period_start", "period_end", "comparison_start", "comparison_end",
          "current", "previous", "reported_change_percent", "sources"}


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key")
        result[key] = value
    return result


def decode(raw):
    return json.loads(raw, object_pairs_hook=unique_object,
                      parse_constant=lambda value: (_ for _ in ()).throw(
                          ValueError("non-finite JSON number")))


def month_bounds(period):
    if not isinstance(period, str) or not re.fullmatch(r"\d{4}-\d{2}", period):
        raise ValueError("expected period must use YYYY-MM")
    year, month = map(int, period.split("-"))
    if year < 2 or year > 9999 or month < 1 or month > 12:
        raise ValueError("expected period is outside the supported calendar")
    end = calendar.monthrange(year, month)[1]
    prior_year, prior_month = (year - 1, 12) if month == 1 else (year, month - 1)
    prior_end = calendar.monthrange(prior_year, prior_month)[1]
    return (date(year, month, 1).isoformat(), date(year, month, end).isoformat(),
            date(prior_year, prior_month, 1).isoformat(),
            date(prior_year, prior_month, prior_end).isoformat())


def evaluate(data, period):
    dates = month_bounds(period)
    checks = []
    def check(name, passed, detail):
        checks.append({"check": name, "passed": bool(passed), "detail": detail})

    if not isinstance(data, dict):
        raise ValueError("report input must be a JSON object")
    check("fields", set(data) == FIELDS, "Use exactly the documented input fields.")
    for name, expected in zip(
            ("period_start", "period_end", "comparison_start", "comparison_end"), dates):
        check(name, data.get(name) == expected, "Expected " + expected)
    counts_ok = all(type(data.get(k)) is int and 0 <= data[k] <= 10**15
                    for k in ("current", "previous"))
    check("counts", counts_ok, "Counts must be non-negative integers up to 10^15.")
    sources = data.get("sources")
    sources_ok = (isinstance(sources, list) and bool(sources)
                  and all(isinstance(x, str) and bool(x.strip()) for x in sources))
    check("source_references", sources_ok, "At least one source reference is required.")

    change = None
    if counts_ok:
        previous, current = data["previous"], data["current"]
        if previous == 0:
            check("percentage", data.get("reported_change_percent") is None
                  and "reported_change_percent" in data,
                  "A zero baseline requires null; use the absolute change.")
        else:
            expected = (Decimal(current - previous) / Decimal(previous) * 100).quantize(
                Decimal("0.1"), rounding=ROUND_HALF_UP)
            change = float(expected)
            value = data.get("reported_change_percent")
            is_number = type(value) in (int, float)
            actual = Decimal(str(value)) if is_number else Decimal("NaN")
            check("percentage", is_number and actual.is_finite() and actual == expected,
                  "Expected " + str(expected) + "%, rounded to one decimal.")
    else:
        check("percentage", False, "Correct the counts before checking arithmetic.")
    return {"passed": all(x["passed"] for x in checks), "expected_period": period,
            "computed_change_percent": change,
            "absolute_change": data["current"] - data["previous"] if counts_ok else None,
            "checks": checks,
            "scope": "Supplied dates, counts, source-reference presence and arithmetic."}


def inspect_file(path, period):
    with Path(path).open("rb") as stream:
        raw = stream.read(MAX_BYTES + 1)
    if len(raw) > MAX_BYTES:
        raise ValueError("input exceeds 1 MiB")
    result = evaluate(decode(raw.decode("utf-8")), period)
    result["input_sha256"] = hashlib.sha256(raw).hexdigest()
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="Local JSON report input")
    parser.add_argument("--period", required=True, help="Expected month, YYYY-MM")
    args = parser.parse_args()
    try:
        result = inspect_file(args.input, args.period)
        print(json.dumps(result, indent=2, allow_nan=False))
        return 0 if result["passed"] else 1
    except (OSError, ValueError, TypeError, OverflowError):
        print(json.dumps({"passed": False, "error":
              "Input could not be checked. Verify the local JSON, size and expected month."}))
        return 2


if __name__ == "__main__":
    sys.exit(main())
