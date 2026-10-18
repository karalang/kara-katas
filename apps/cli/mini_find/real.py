# Checks mini_find.py against GNU find: builds the tree moved to this
# machine's clock, runs each job under the real find and under the
# mirror with the same "now", and compares. find lists a directory in
# readdir order and the mirror in sorted order, so stdout is compared
# as a sorted list of lines; stderr and the exit status exactly.
import os, shlex, subprocess, sys, time
os.environ["TZ"] = "UTC"
os.environ["LC_ALL"] = "C"
time.tzset()
import mk, mini_find

now = int(time.time() * 1000)
mini_find.SHIFT_MS = now - mini_find.NOW_MS
mini_find.NOW_MS = now
mk.write_all()
mini_find.build_tree()
bad = 0
for line in mk.FILES["jobs.txt"].split("\n"):
    if line == "" or line.startswith("#"):
        continue
    w = shlex.split(line)
    if w[0] == "reset":
        mini_find.build_tree()
        continue
    # The mirror's deletions would leave nothing for find, so each job
    # that deletes runs on a fresh tree for both.
    deletes = "-delete" in w
    if deletes:
        mini_find.build_tree()
    r = subprocess.run(["find"] + w[1:], capture_output=True, text=True)
    if deletes:
        mini_find.build_tree()
    job = mini_find.Job()
    mini_find.find(job, w[1:])
    if "-quit" in w:
        # Which file comes first is readdir order.
        key = lambda s: s.count("\n")
    elif "\\c" in line:
        key = lambda s: sorted(s)
    else:
        key = lambda s: sorted(s.split("\n"))
    same = key(job.out) == key(r.stdout) and job.err == r.stderr and job.status == r.returncode
    if not same:
        bad += 1
        print("DIFFERS:", line)
        print("  real   :", repr(r.stdout[:600]), repr(r.stderr), r.returncode)
        print("  mirror :", repr(job.out[:600]), repr(job.err), job.status)
print("jobs differing:", bad)
