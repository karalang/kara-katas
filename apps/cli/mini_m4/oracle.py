# The oracle: runs each line of data/jobs.txt with GNU m4 1.4.19 in data/
# and prints what mini_m4 prints. Run it from this directory after mk.py.
import subprocess, sys
def show(text):
    sys.stdout.write(text)
    if text != "" and not text.endswith("\n"):
        print("[no newline at end]")
for line in open("data/jobs.txt").read().split("\n")[:-1]:
    args = line.split()
    print("$ m4 " + line)
    r = subprocess.run(["m4", *args], cwd="data", capture_output=True, timeout=20)
    show(r.stdout.decode())
    if r.stderr:
        print("-- stderr")
        show(r.stderr.decode())
    if r.returncode != 0:
        print(f"[exit {r.returncode}]")
