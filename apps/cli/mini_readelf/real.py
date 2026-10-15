# The readelf half of expected.out, from GNU readelf itself.
import subprocess, shlex, sys
out = []
for line in open("data/jobs.txt"):
    line = line.rstrip("\n")
    if not line.startswith("readelf"):
        continue
    p = subprocess.run(shlex.split(line), cwd="data", capture_output=True, text=True)
    out.append(f"$ {line}\n")
    out.append(p.stdout)
    out.append(p.stderr)
    if p.returncode:
        out.append(f"[exit status {p.returncode}]\n")
    out.append("\n")
sys.stdout.write("".join(out))
