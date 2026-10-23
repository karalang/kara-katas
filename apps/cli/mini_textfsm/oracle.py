#!/usr/bin/env python3
r"""Replays data/jobs.tsv through the vendored textfsm library and writes
expected.out. Each @JOB block is a (name, template, input) triple; the oracle
builds a TextFSM from the template, parses the input, and renders the table
under a `=== <name> ===` header as

    HEADER\t<col>\t<col>...
    ROW\t<cell>\t<cell>...        (a List cell is rendered [a, b, c])

or, when the FSM raises, `ERROR\t<message>`. mini_textfsm.kara reproduces this
byte-for-byte on every backend; the FSM walks rules by index and matches by
key/name, never iterating a hash map, so the output is deterministic."""
import sys

sys.path.insert(0, "vendor")
import textfsm  # noqa: E402


def read_blocks(path):
    jobs = []
    name = None
    tmpl = None
    inp = None
    cur = None
    for line in open(path, encoding="utf-8").read().split("\n"):
        if line.startswith("@JOB "):
            name = line[5:]
            tmpl, inp = [], []
            cur = None
        elif line == "@TEMPLATE":
            cur = tmpl
        elif line == "@INPUT":
            cur = inp
        elif line == "@END":
            jobs.append((name, tmpl, inp))
            cur = None
        elif cur is not None:
            cur.append(line)
    return jobs


def render(name, header, rows):
    out = ["=== %s ===" % name, "HEADER\t" + "\t".join(header)]
    for row in rows:
        cells = []
        for v in row:
            if isinstance(v, list):
                cells.append("[" + ", ".join(v) + "]")
            else:
                cells.append(v)
        out.append("ROW\t" + "\t".join(cells))
    return out


def run(name, tmpl_lines, inp_lines):
    import io
    template = "\n".join(tmpl_lines)
    text = "\n".join(inp_lines)
    try:
        fsm = textfsm.TextFSM(io.StringIO(template))
        rows = fsm.ParseText(text)
        return render(name, fsm.header, rows)
    except textfsm.TextFSMError as e:
        return ["=== %s ===" % name, "ERROR\t" + str(e)]


def main():
    out = []
    for (name, tmpl, inp) in read_blocks("data/jobs.tsv"):
        out.extend(run(name, tmpl, inp))
    sys.stdout.write("\n".join(out) + "\n")


main()
