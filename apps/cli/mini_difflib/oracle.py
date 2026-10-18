#!/usr/bin/env python3
"""Runs data/jobs.tsv through Python 3.13's difflib; prints expected.out.

Each job prints `== ` and its fields joined by ` | `, then its output.
"""
import difflib, os, sys

os.chdir("data")
FROM_DATE = "2024-02-29 13:45:10"
TO_DATE = "2024-03-01 09:00:00"


def lines(name):
    with open(name, newline="") as f:
        return f.readlines()


def opcode_lines(s):
    out = []
    for tag, i1, i2, j1, j2 in s.get_opcodes():
        out.append(f"{tag:7} a[{i1}:{i2}] --> b[{j1}:{j2}] {s.a[i1:i2]!r:>8} --> {s.b[j1:j2]!r}\n")
    return "".join(out)


def run(f):
    cmd = f[0]
    if cmd == "opcodes":
        return opcode_lines(difflib.SequenceMatcher(None, f[1], f[2]))
    if cmd == "blocks":
        s = difflib.SequenceMatcher(None, f[1], f[2])
        return "".join(f"{m}\n" for m in s.get_matching_blocks())
    if cmd == "ratios":
        s = difflib.SequenceMatcher(None, f[1], f[2])
        return f"{s.ratio()} {s.quick_ratio()} {s.real_quick_ratio()}\n"
    if cmd == "junk":
        s = difflib.SequenceMatcher(lambda x: x == " ", f[1], f[2])
        return f"{s.ratio()}\n" + opcode_lines(s)
    if cmd == "longest":
        a = difflib.SequenceMatcher(None, f[1], f[2]).find_longest_match()
        b = difflib.SequenceMatcher(lambda x: x == " ", f[1], f[2]).find_longest_match()
        return f"{a}\n{b}\n"
    if cmd == "close":
        words = [w.rstrip("\n") for w in lines("words.txt")]
        try:
            return f"{difflib.get_close_matches(f[1], words, int(f[2]), float(f[3]))}\n"
        except ValueError as e:
            return f"ValueError: {e}\n"
    if cmd == "unified":
        return "".join(difflib.unified_diff(lines(f[1]), lines(f[2]), f[1], f[2],
                                            FROM_DATE, TO_DATE, int(f[3])))
    if cmd == "context":
        return "".join(difflib.context_diff(lines(f[1]), lines(f[2]), f[1], f[2],
                                            FROM_DATE, TO_DATE, int(f[3])))
    if cmd == "ndiff":
        return "".join(difflib.ndiff(lines(f[1]), lines(f[2])))
    if cmd == "ndiff_linejunk":
        return "".join(difflib.ndiff(lines(f[1]), lines(f[2]), linejunk=difflib.IS_LINE_JUNK))
    if cmd == "restore":
        delta = list(difflib.ndiff(lines(f[1]), lines(f[2])))
        return "".join(difflib.restore(delta, int(f[3])))
    if cmd == "line_ratio":
        s = difflib.SequenceMatcher(None, lines(f[1]), lines(f[2]), autojunk=f[3] == "true")
        return (f"ratio {s.ratio()}, {len(s.bpopular)} popular, "
                f"{len(s.get_matching_blocks()) - 1} blocks, {len(s.get_opcodes())} opcodes\n")
    raise SystemExit(f"unknown job {cmd}")


out = []
for job in lines("jobs.tsv"):
    f = job.rstrip("\n").split("\t")
    out.append("== " + " | ".join(f) + "\n")
    try:
        text = run(f)
    except OSError as e:
        text = f"{type(e).__name__}: {e}\n"
    except ValueError as e:
        text = f"ValueError: {e}\n"
    if text and not text.endswith("\n"):
        text += "\n"
    out.append(text)
sys.stdout.write("".join(out))
