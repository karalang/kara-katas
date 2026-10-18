# The oracle: runs each command line of jobs.tsv with pkgconf 1.8.1 (as
# Ubuntu 24.04 ships it as pkg-config) in data/, with PKG_CONFIG_LIBDIR=pc
# and no other pkg-config or compiler variables set, and prints what
# mini_pkgconfig prints. Run from this directory after mk.py.
#
# `--list-all` and `--list-package-names` print in the order readdir()
# returns the files, which depends on the filesystem; their lines are
# sorted here, and mini_pkgconfig lists in name order.
import os, re, subprocess, sys
def quote(a):
    if a != "" and re.fullmatch(r"[A-Za-z0-9_./=+:,%@-]+", a):
        return a
    return "'" + a.replace("'", "'\\''") + "'"
def show(text):
    sys.stdout.write(text)
    if text != "" and not text.endswith("\n"):
        print("[no newline at end]")
for line in open("jobs.tsv").read().split("\n")[:-1]:
    args = line.split("\t")
    print("$ ", end="")
    env = {"PATH": os.environ["PATH"], "LC_ALL": "C", "PKG_CONFIG_LIBDIR": "pc"}
    shown = []
    while args and re.fullmatch(r"[A-Z_]+=.*", args[0]):
        k, v = args[0].split("=", 1)
        env[k] = v
        shown.append(quote(args[0]))
        args = args[1:]
    print(" ".join(shown + ["pkg-config"] + [quote(a) for a in args]))
    r = subprocess.run(["pkg-config"] + args, cwd="data", capture_output=True, env=env)
    out = r.stdout.decode()
    if "--list-all" in args or "--list-package-names" in args:
        out = "".join(sorted(out.splitlines(True)))
    show(out)
    show(r.stderr.decode())
    if r.returncode != 0:
        print(f"[exit {r.returncode}]")
