# The oracle: runs each script of data/jobs.txt through GNU bc 1.07.1
# on stdin and prints what mini_bc prints. Run from this directory after
# mk.py.
import os, subprocess, sys
env = {k: v for k, v in os.environ.items() if not k.startswith("BC_") and k != "POSIXLY_CORRECT"}
def show(text):
    sys.stdout.write(text)
    if text != "" and not text.endswith("\n"):
        print("[no newline at end]")
for name in open("data/jobs.txt").read().split():
    print(f"$ bc < {name}")
    r = subprocess.run(["bc"], stdin=open("data/" + name, "rb"), capture_output=True, env=env)
    show(r.stdout.decode())
    show(r.stderr.decode())
    if r.returncode != 0:
        print(f"[exit {r.returncode}]")
