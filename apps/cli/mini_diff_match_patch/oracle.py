# Runs the jobs in data/jobs.txt through diff-match-patch 20241021 (the
# copy in diff_match_patch/, unchanged) and prints what
# mini_diff_match_patch prints.
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import mk  # noqa: E402
from diff_match_patch import diff_match_patch  # noqa: E402

DATA = os.path.join(HERE, "data")
SETTINGS = {
    "Diff_Timeout": float,
    "Diff_EditCost": int,
    "Match_Threshold": float,
    "Match_Distance": int,
    "Patch_DeleteThreshold": float,
    "Patch_Margin": int,
    "Match_MaxBits": int,
}


def read(rel):
    with open(os.path.join(DATA, rel), encoding="utf-8", newline="") as f:
        return f.read()


def unescape(s):
    out = []
    i = 0
    while i < len(s):
        c = s[i]
        if c == "\\" and i + 1 < len(s):
            n = s[i + 1]
            if n == "n":
                out.append("\n")
            elif n == "t":
                out.append("\t")
            elif n == "r":
                out.append("\r")
            elif n == "\\":
                out.append("\\")
            elif n == "u":
                out.append(chr(int(s[i + 2:i + 6], 16)))
                i += 4
            else:
                out.append(c + n)
            i += 2
            continue
        out.append(c)
        i += 1
    return "".join(out)


def arg(s):
    return read(s[5:]) if s.startswith("file:") else unescape(s)


def show_text(t):
    print(t)
    print("--- end")


def run_job(dmp, kind, raw):
    words = kind.split(" ")
    op = words[0]
    a = [arg(x) for x in raw]
    if op == "set":
        name, value = raw
        setattr(dmp, name, SETTINGS[name](value))
        print("%s = %s" % (name, value))
    elif op == "prefix":
        print(dmp.diff_commonPrefix(a[0], a[1]))
    elif op == "suffix":
        print(dmp.diff_commonSuffix(a[0], a[1]))
    elif op == "overlap":
        print(dmp.diff_commonOverlap(a[0], a[1]))
    elif op == "halfmatch":
        print(repr(dmp.diff_halfMatch(a[0], a[1])))
    elif op == "lines":
        print(repr(dmp.diff_linesToChars(a[0], a[1])))
    elif op == "bisect":
        print(repr(dmp.diff_bisect(a[0], a[1], sys.maxsize)))
    elif op == "xindex":
        diffs = dmp.diff_main(a[0], a[1])
        print(repr(diffs))
        print(dmp.diff_xIndex(diffs, int(a[2])))
    elif op == "diff":
        diffs = dmp.diff_main(a[0], a[1], "nolines" not in words)
        if "semantic" in words:
            dmp.diff_cleanupSemantic(diffs)
        if "efficiency" in words:
            dmp.diff_cleanupEfficiency(diffs)
        if "lossless" in words:
            dmp.diff_cleanupSemanticLossless(diffs)
        print("diffs: %d" % len(diffs))
        for d in diffs:
            print("  %r" % (d,))
        ok1 = dmp.diff_text1(diffs) == a[0]
        ok2 = dmp.diff_text2(diffs) == a[1]
        print("text1: %s, text2: %s" % (ok1, ok2))
        delta = dmp.diff_toDelta(diffs)
        print("delta: %r" % delta)
        back = dmp.diff_fromDelta(a[0], delta)
        print("delta back: %s" % (back == diffs))
        print("levenshtein: %d" % dmp.diff_levenshtein(diffs))
        html = dmp.diff_prettyHtml(diffs)
        if len(html) <= 2000:
            print("html: %s" % html)
        else:
            print("html: %d characters" % len(html))
    elif op == "fromdelta":
        print(repr(dmp.diff_fromDelta(a[0], a[1])))
    elif op == "match":
        print(dmp.match_main(a[0], a[1], int(a[2])))
    elif op == "patch":
        patches = dmp.patch_make(a[0], a[1])
        text = dmp.patch_toText(patches)
        print("patches: %d" % len(patches))
        sys.stdout.write(text)
        print("--- end")
        again = dmp.patch_toText(dmp.patch_fromText(text))
        print("text back: %s" % (again == text))
        result, applied = dmp.patch_apply(patches, a[0])
        print("applied: %r, gives text2: %s" % (applied, result == a[1]))
    elif op == "fromtext":
        patches = dmp.patch_fromText(a[0])
        print("patches: %d" % len(patches))
        sys.stdout.write(dmp.patch_toText(patches))
        print("--- end")
    elif op == "sync":
        patches = dmp.patch_make(a[0], a[1])
        print("patches: %d" % len(patches))
        result, applied = dmp.patch_apply(patches, a[2])
        print("applied: %r" % (applied,))
        if result == a[1]:
            print("gives the edited text")
        else:
            show_text(result)
    elif op == "applytext":
        patches = dmp.patch_fromText(a[0])
        result, applied = dmp.patch_apply(patches, a[1])
        print("applied: %r" % (applied,))
        show_text(result)
    else:
        raise SystemExit("unknown job " + op)


def main():
    mk.main()
    dmp = diff_match_patch()
    lines = read("jobs.txt").split("\n")
    for n, line in enumerate(lines, 1):
        if not line or line.startswith("#"):
            continue
        parts = line.split(" | ")
        print("== jobs.txt:%d %s" % (n, line))
        try:
            run_job(dmp, parts[0], parts[1:])
        except Exception as e:  # the type is printed
            print("error: %s: %s" % (type(e).__name__, e))


if __name__ == "__main__":
    main()
