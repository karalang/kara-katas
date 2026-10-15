# Runs data/jobs.txt with the real OpenSSL 3.0.13, putting each command's
# stdout before its stderr. OpenSSL's error-stack lines start with a thread
# id that changes from run to run, so they are left out.
import os, re, subprocess, sys
src = os.path.abspath("data")
for line in open(os.path.join(src, "jobs.txt")).read().splitlines():
    if not line or line.startswith("#"):
        continue
    sys.stdout.write(f"$ openssl {line}\n")
    p = subprocess.run(["openssl"] + line.split(" "), cwd=src, capture_output=True, env=dict(os.environ, TZ="UTC"))
    text = p.stdout.decode("utf-8", "replace") + p.stderr.decode("utf-8", "replace")
    sys.stdout.write("".join(l for l in text.splitlines(True) if not re.match(r"[0-9A-F]{16}:error:", l)))
    if p.returncode:
        sys.stdout.write(f"[exit status {p.returncode}]\n")
    sys.stdout.write("\n")
