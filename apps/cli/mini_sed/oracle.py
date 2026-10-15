# The oracle: runs each job of jobs.tsv with GNU sed 4.9 in data/ and
# prints what mini_sed prints. Run from this directory after mk.py.
import re, subprocess, sys
def quote(a):
    if a != "" and re.fullmatch(r"[A-Za-z0-9_./=+:,%@-]+", a):
        return a
    return "'" + a.replace("'", "'\\''") + "'"
# Output that does not end in a newline is marked, so the next line starts
# on its own line.
def show(text):
    sys.stdout.write(text)
    if text != "" and not text.endswith("\n"):
        print("[no newline at end]")
for line in open("jobs.tsv").read().split("\n")[:-1]:
    args = line.split("\t")
    if args[0] == "@cat":
        print(f"$ cat {args[1]}")
        show(open("data/" + args[1]).read())
        continue
    print("$ sed " + " ".join(quote(a) for a in args))
    r = subprocess.run(["sed", *args], cwd="data", capture_output=True)
    show(r.stdout.decode()); show(r.stderr.decode())
    if r.returncode != 0:
        print(f"[exit {r.returncode}]")
