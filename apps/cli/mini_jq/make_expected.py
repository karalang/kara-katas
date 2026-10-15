# The oracle: runs each job of jobs.tsv through the real jq and prints what
# mini_jq.kara prints. Run from this directory: python3 make_expected.py
import subprocess
for line in open("jobs.tsv").read().splitlines():
    flags, file, prog = line.split("\t")
    args = flags.split() if flags else []
    shown = (flags + " " if flags else "") + "'" + prog + "' " + file
    print(f"$ jq {shown}")
    p = subprocess.run(["jq", *args, prog, "data/" + file], capture_output=True, text=True)
    print(p.stdout, end="")
    print(p.stderr.replace("data/", ""), end="")
    if p.returncode != 0:
        print(f"[exit {p.returncode}]")
