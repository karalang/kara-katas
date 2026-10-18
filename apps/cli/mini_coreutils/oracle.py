# The oracle: runs each pipeline of jobs.tsv with GNU coreutils 9.4 in
# data/ (LC_ALL=C) and prints what mini_coreutils prints. Run from this
# directory after mk.py.
import os, re, subprocess, sys
env = dict(os.environ, LC_ALL="C")
def quote(a):
    if a != "" and re.fullmatch(r"[A-Za-z0-9_./=+:,%@-]+", a):
        return a
    return "'" + a.replace("'", "'\\''") + "'"
def show(text):
    sys.stdout.write(text)
    if text != "" and not text.endswith("\n"):
        print("[no newline at end]")
for line in open("jobs.tsv").read().split("\n")[:-1]:
    args = [a.replace("\v", "\t") for a in line.split("\t")]
    print("$ " + " ".join("|" if a == "\x1d" else quote(a) for a in args))
    stages = [[]]
    for a in args:
        if a == "\x1d":
            stages.append([])
        else:
            stages[-1].append(a)
    data = b""
    errs = []
    status = 0
    for st in stages:
        r = subprocess.run(st, cwd="data", input=data, capture_output=True, env=env)
        data = r.stdout
        errs.append(r.stderr.decode())
        status = r.returncode
    show(data.decode())
    for e in errs:
        show(e)
    if status != 0:
        print(f"[exit {status}]")
