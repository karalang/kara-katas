# The reference run for mini_docopt: the same jobs through docopt 0.6.2
# (docopt.py here is the file from its release, unchanged) on Python 3.13.
# A job prints what the program would: the dict docopt returns, or the
# help, version or usage error it exits with.
import io
import json
import os
import sys
import warnings

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
warnings.filterwarnings("ignore", category=SyntaxWarning)
from docopt import docopt, DocoptExit  # noqa: E402

D = "data"
OUT = []


def say(s=""):
    OUT.append(s)


def doc_of(name):
    with open(os.path.join(D, "docs", name + ".txt"), encoding="utf-8") as f:
        return f.read()


def call(doc, argv, opts):
    """Run docopt as a script would: (result or None, stdout, stderr, exit status)."""
    out, err = io.StringIO(), io.StringIO()
    saved = sys.stdout
    sys.stdout = out
    try:
        r = docopt(doc, argv, help=opts.get("help", True), version=opts.get("version"),
                   options_first=opts.get("options_first", False))
        return r, out.getvalue(), "", 0
    except SystemExit as e:
        if e.code is None:
            return None, out.getvalue(), "", 0
        if isinstance(e.code, int):
            return None, out.getvalue(), "", e.code
        return None, out.getvalue(), str(e.code) + "\n", 1
    except Exception as e:
        return None, out.getvalue() + "uncaught %s: %s\n" % (type(e).__name__, e), "", 1
    finally:
        sys.stdout = saved


def show(r, out, err, code):
    for l in out.splitlines():
        say(l)
    for l in err.splitlines():
        say("stderr: " + l)
    if r is not None:
        for l in repr(r).splitlines():
            say(l)
    if code:
        say("exit %d" % code)


def job_docopt(name, argv, opts):
    say("== %s %s" % (name, json.dumps(argv, ensure_ascii=False)))
    show(*call(doc_of(name), argv, opts))


def job_case(label, doc, argv, opts):
    say("== case %s %s" % (json.dumps(label), json.dumps(argv, ensure_ascii=False)))
    show(*call(doc, argv, opts))


def job_git(argv):
    say("== git %s" % json.dumps(argv, ensure_ascii=False))
    r, out, err, code = call(doc_of("git"), argv, {"version": "git version 1.7.4.4", "options_first": True})
    if r is None:
        show(r, out, err, code)
        return
    sub = [r["<command>"]] + r["<args>"]
    cmd = r["<command>"]
    if cmd in "add branch checkout clone commit push remote".split():
        say("-> git_%s %s" % (cmd, json.dumps(sub, ensure_ascii=False)))
        show(*call(doc_of("git_" + cmd), sub, {}))
    elif cmd in ["help", None]:
        say("-> git --help")
        show(*call(doc_of("git"), ["--help"], {"version": "git version 1.7.4.4", "options_first": True}))
    else:
        show(None, "", "%r is not a git.py command. See 'git help'.\n" % cmd, 1)


def job_naval(lines):
    say("== naval session (%d commands)" % len(lines))
    doc = doc_of("naval_fate")
    ships = []  # [name, x, y]
    mines = []  # [x, y, kind]
    for line in lines:
        say("$ naval_fate.py " + line)
        r, out, err, code = call(doc, line.split(), {"version": "Naval Fate 2.0"})
        if r is None:
            show(r, out, err, code)
            continue
        try:
            x = int(r["<x>"]) if r["<x>"] is not None else None
            y = int(r["<y>"]) if r["<y>"] is not None else None
        except ValueError:
            say("  bad coordinates: %s %s" % (r["<x>"], r["<y>"]))
            continue
        if r["ship"] and r["new"]:
            for n in r["<name>"]:
                if any(s[0] == n for s in ships):
                    say("  ship %s already exists" % n)
                else:
                    ships.append([n, 0, 0])
                    say("  launched %s at (0, 0)" % n)
        elif r["ship"] and r["move"]:
            n = r["<name>"][0]
            found = [s for s in ships if s[0] == n]
            if not found:
                say("  no ship named %s" % n)
                continue
            try:
                speed = int(r["--speed"])
            except ValueError:
                say("  bad speed: %s" % r["--speed"])
                continue
            s = found[0]
            dist = abs(x - s[1]) + abs(y - s[2])
            say("  %s moves from (%d, %d) to (%d, %d) at %d knots, %d miles" % (n, s[1], s[2], x, y, speed, dist))
            s[1], s[2] = x, y
            hit = [m for m in mines if m[0] == x and m[1] == y]
            if hit:
                say("  %s hits a %s mine at (%d, %d) and sinks" % (n, hit[0][2], x, y))
                ships.remove(s)
                mines.remove(hit[0])
        elif r["ship"] and r["shoot"]:
            sunk = [s for s in ships if s[1] == x and s[2] == y]
            if sunk:
                say("  shot at (%d, %d) sinks %s" % (x, y, ", ".join(s[0] for s in sunk)))
                for s in sunk:
                    ships.remove(s)
            else:
                say("  shot at (%d, %d) hits nothing" % (x, y))
        elif r["mine"]:
            here = [m for m in mines if m[0] == x and m[1] == y]
            if r["set"]:
                kind = "drifting" if r["--drifting"] else "moored"
                if here:
                    say("  a mine is already at (%d, %d)" % (x, y))
                else:
                    mines.append([x, y, kind])
                    say("  %s mine set at (%d, %d)" % (kind, x, y))
            elif here:
                mines.remove(here[0])
                say("  mine removed from (%d, %d)" % (x, y))
            else:
                say("  no mine at (%d, %d)" % (x, y))
    say("fleet: " + (", ".join("%s (%d, %d)" % tuple(s) for s in ships) or "none"))
    say("mines: " + (", ".join("(%d, %d) %s" % tuple(m) for m in mines) or "none"))


with open(os.path.join(D, "jobs.jsonl"), encoding="utf-8") as f:
    jobs = [json.loads(l) for l in f if l.strip()]
for j in jobs:
    if j[0] == "docopt":
        job_docopt(j[1], j[2], j[3])
    elif j[0] == "case":
        job_case(j[1], j[2], j[3], j[4])
    elif j[0] == "git":
        job_git(j[1])
    elif j[0] == "naval":
        job_naval(j[1])
sys.stdout.write("\n".join(OUT) + "\n")
