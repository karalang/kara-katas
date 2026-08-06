#!/usr/bin/env python3
"""Self-test for scripts/bench-compare.py's workload/sink guard.

B-2026-08-05-34. The guard exists because the cell join matches on
(kata, lang, approach, lane, mode, metric) and nothing else, so it will divide
a 500,000-iteration run by a 50,000-iteration one and call the quotient a
regression. Three katas in this repo's own feed had changed both workload and
sink, and their bogus ratios were the top three entries in a corpus median that
was read as a compiler regression for two months.

A guard nobody tests is how the next one rots, so this asserts BOTH directions:
a changed identity is excluded, and an unchanged one still compares.

Run: python3 scripts/test-bench-compare.py
"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
COMPARE = HERE / "bench-compare.py"


def feed(kata_id, workload, sink, mean_ms, binary_bytes=1000):
    """One consolidated-feed doc with a single runtime + binary cell."""
    return {
        "katas": [
            {
                "schema_version": 1,
                "kata": {"id": kata_id, "workload": workload, "sink": sink},
                "measurements": [
                    {
                        "lang": "kara",
                        "approach": "a",
                        "lane": "seq",
                        "mode": "native",
                        "runtime": {"mean_ms": mean_ms},
                        "binary_bytes": binary_bytes,
                    }
                ],
            }
        ]
    }


def run(base_doc, cur_doc):
    with tempfile.TemporaryDirectory() as td:
        b, c = Path(td) / "b.json", Path(td) / "c.json"
        b.write_text(json.dumps(base_doc))
        c.write_text(json.dumps(cur_doc))
        p = subprocess.run(
            [sys.executable, str(COMPARE), "--baseline", str(b), "--current", str(c)],
            capture_output=True,
            text=True,
        )
        return p.stdout + p.stderr


FAILURES = []


def check(cond, what):
    if cond:
        print(f"  ok   {what}")
    else:
        print(f"  FAIL {what}")
        FAILURES.append(what)


def main():
    print("bench-compare workload/sink guard:")

    # 1. Changed SINK — the strongest signal, since the sink is the program's
    #    own output: a different answer means it did not run the same thing.
    out = run(feed("7", "N=100", "42", 100.0), feed("7", "N=100", "420", 1000.0))
    check("NOT COMPARABLE" in out, "changed sink is reported as not comparable")
    check(
        "REGRESSIONS" not in out,
        "changed sink does NOT produce a 10x regression line",
    )

    # 2. Changed WORKLOAD with the SAME sink — more work for the same answer,
    #    which a sink-only check would wave through.
    out = run(feed("7", "N=100", "42", 100.0), feed("7", "N=100000", "42", 1000.0))
    check("NOT COMPARABLE" in out, "changed workload is reported even when sink matches")
    check("REGRESSIONS" not in out, "changed workload does NOT produce a regression line")

    # 3. UNCHANGED identity — the guard must not swallow real regressions.
    #    This is the direction that makes the guard safe rather than merely quiet.
    out = run(feed("7", "N=100", "42", 100.0), feed("7", "N=100", "42", 100.0, 5000))
    check("NOT COMPARABLE" not in out, "unchanged identity is not excluded")
    check(
        "REGRESSIONS" in out,
        "unchanged identity still reports a real binary-size regression",
    )

    # 4. A changed kata must not suppress an UNRELATED kata's regression.
    base = feed("7", "N=100", "42", 100.0)
    cur = feed("7", "N=999", "420", 100.0)
    base["katas"].append(feed("8", "N=1", "1", 10.0)["katas"][0])
    cur["katas"].append(feed("8", "N=1", "1", 10.0, 9000)["katas"][0])
    out = run(base, cur)
    check("kata 7" in out, "the changed kata is named")
    check("8/kara" in out, "a sibling kata's regression still reports")

    print(
        f"\n{'FAILED: ' + str(len(FAILURES)) if FAILURES else 'all guard checks passed'}"
    )
    return 1 if FAILURES else 0


if __name__ == "__main__":
    sys.exit(main())
