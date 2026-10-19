# Runs data/jobs.jsonl through wcwidth 0.2.13 (the package here,
# unchanged) and prints what mini_wcwidth prints. Run mk.py first.
#
# wcwidth caches its answers, and a version string only warns the first
# time it is matched, so the caches are cleared before each job. Each
# job's UNICODE_VERSION comes from its "env" key, and is unset without one.
import json
import os
import sys
import warnings

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wcwidth  # noqa: E402
from wcwidth import wcswidth  # noqa: E402

out = []


def emit(s):
    out.append(s)


caught = []


def flush_warnings():
    for w in caught:
        emit("    warning: %s" % w.message)
    del caught[:]


def run_wcwidth(j):
    v = j.get("version")
    for t in j["texts"]:
        try:
            r = wcwidth.wcwidth(t) if v is None else wcwidth.wcwidth(t, v)
            emit("  %r %d" % (t, r))
        except TypeError as e:
            emit("  %r TypeError: %s" % (t, e))
        flush_warnings()


def run_wcswidth(j):
    v = j.get("version", "auto")
    n = j.get("n")
    for t in j["texts"]:
        try:
            emit("  %r %d" % (t, wcswidth(t, n, v)))
        except IndexError as e:
            emit("  %r IndexError: %s" % (t, e))
        flush_warnings()


def run_match(j):
    for g in j["given"]:
        emit("  %r -> %r" % (g, wcwidth._wcmatch_version(g)))
        flush_warnings()


# ---------------------------------------------------------- the reports

def width(s):
    return wcswidth(s)


def clean(s):
    return "".join("?" if wcwidth.wcwidth(c) < 0 else c for c in s)


def read_lines(name):
    with open(os.path.join("data", name), encoding="utf-8", newline="") as f:
        text = f.read()
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    return lines


def run_columns(j):
    names = [clean(n) for n in read_lines(j["file"])]
    ws = [width(n) for n in names]
    n = len(names)
    w = j["width"]
    chosen = None
    for cols in range(n, 0, -1):
        rows = (n + cols - 1) // cols
        if (cols - 1) * rows >= n:
            continue
        colw = []
        for c in range(cols):
            colw.append(max(ws[c * rows:(c + 1) * rows]))
        if sum(colw) + 2 * (cols - 1) <= w or cols == 1:
            chosen = (cols, rows, colw)
            break
    cols, rows, colw = chosen
    emit("  %d columns, %d rows, widths %s" % (cols, rows, colw))
    for r in range(rows):
        line = ""
        for c in range(cols):
            i = c * rows + r
            if i >= n:
                break
            line += names[i]
            if (c + 1) * rows + r < n:
                line += " " * (colw[c] - ws[i] + 2)
        emit("  |" + line)


def fit(s, w):
    if width(s) <= w:
        return s
    if w <= 0:
        return ""
    k = 0
    while k < len(s) and width(s[:k + 1]) <= w - 1:
        k += 1
    return s[:k] + "…"


def pad(s, w, how):
    gap = w - width(s)
    if gap <= 0:
        return s
    if how == "<":
        return s + " " * gap
    if how == ">":
        return " " * gap + s
    left = gap // 2
    return " " * left + s + " " * (gap - left)


def run_table(j):
    rows = [[clean(c) for c in line.split(",")] for line in read_lines(j["file"])]
    ws = list(j["widths"])
    for c in range(len(ws)):
        if ws[c] == 0:
            ws[c] = max(width(r[c]) for r in rows)
    align = j["align"]

    def rule(a, m, b):
        return a + m.join("─" * (w + 2) for w in ws) + b

    emit("  " + rule("┌", "┬", "┐"))
    for k, r in enumerate(rows):
        cells = [pad(fit(r[c], ws[c]), ws[c], align[c]) for c in range(len(ws))]
        emit("  │ " + " │ ".join(cells) + " │")
        if k == 0:
            emit("  " + rule("├", "┼", "┤"))
    emit("  " + rule("└", "┴", "┘"))


def wrap(text, w):
    lines = []
    line = ""
    for word in text.split(" "):
        if word == "":
            continue
        cand = word if line == "" else line + " " + word
        if width(cand) <= w:
            line = cand
            continue
        if line != "":
            lines.append(line)
            line = ""
        while width(word) > w:
            take = 1
            while take < len(word) and width(word[:take + 1]) <= w:
                take += 1
            lines.append(word[:take])
            word = word[take:]
        line = word
    if line != "":
        lines.append(line)
    return lines


def run_wrap(j):
    for msg in read_lines(j["file"]):
        msg = clean(msg)
        k = msg.index(": ")
        who = msg[:k + 2]
        indent = width(who)
        w = max(1, j["width"] - indent)
        lines = wrap(msg[k + 2:], w)
        if not lines:
            lines = [""]
        emit("  " + who + lines[0])
        for l in lines[1:]:
            emit("  " + " " * indent + l)


def expand(s):
    o = ""
    col = 0
    for c in s:
        u = ord(c)
        if c == "\t":
            n = 8 - col % 8
            o += " " * n
            col += n
            continue
        if u < 32:
            t = "^" + chr(u + 64)
        elif u == 0x7F:
            t = "^?"
        elif 0x80 <= u < 0xA0:
            t = "\\x%02x" % u
        else:
            t = c
        o += t
        col = width(o)
    return o


def run_tail(j):
    w = j["width"]
    for line in read_lines(j["file"]):
        s = fit(expand(line), w)
        emit("  |" + pad(s, w, "<") + "|")


RUN = {
    "wcwidth": run_wcwidth,
    "wcswidth": run_wcswidth,
    "match": run_match,
    "columns": run_columns,
    "table": run_table,
    "wrap": run_wrap,
    "tail": run_tail,
}


def describe(j):
    parts = [j["kind"]]
    for k in ["version", "env", "n", "file", "width", "widths", "align"]:
        if k in j:
            parts.append("%s=%r" % (k, j[k]))
    return " ".join(parts)


def main():
    emit("wcwidth %s, Unicode %s" % (wcwidth.__version__, ", ".join(wcwidth.list_versions())))
    with open("data/jobs.jsonl", encoding="utf-8") as f:
        jobs = [json.loads(l) for l in f if l.strip()]
    with warnings.catch_warnings(record=True) as rec:
        warnings.simplefilter("always")
        for k, j in enumerate(jobs):
            wcwidth.wcwidth.cache_clear()
            wcwidth._wcmatch_version.cache_clear()
            if "env" in j:
                os.environ["UNICODE_VERSION"] = j["env"]
            else:
                os.environ.pop("UNICODE_VERSION", None)
            emit("job %d: %s" % (k + 1, describe(j)))
            global caught
            caught = rec
            RUN[j["kind"]](j)
            flush_warnings()
    sys.stdout.write("\n".join(out) + "\n")


main()
