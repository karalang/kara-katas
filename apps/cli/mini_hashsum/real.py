# Runs data/jobs.txt with the real GNU coreutils 9.4 checksum tools in a scratch
# copy of data/, putting each command's stdout before its stderr.
import os, shutil, subprocess, sys
src = os.path.abspath("data")
work = os.path.abspath("realwork")
if os.path.isdir(work):
    shutil.rmtree(work)
shutil.copytree(src, work)
for line in open(os.path.join(src, "jobs.txt")).read().splitlines():
    if not line or line.startswith("#"):
        continue
    sys.stdout.write(f"$ {line}\n")
    p = subprocess.run(line.split(" "), cwd=work, capture_output=True)
    sys.stdout.write(p.stdout.decode("utf-8", "replace") + p.stderr.decode("utf-8", "replace"))
    if p.returncode:
        sys.stdout.write(f"[exit status {p.returncode}]\n")
    sys.stdout.write("\n")
