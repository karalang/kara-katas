# Runs data/jobs.txt with the real Info-ZIP unzip 6.0 and zipinfo, in a
# scratch copy of data/, with TZ=UTC. `tree` lists what extraction wrote.
import os, shutil, subprocess, sys, zlib
src = os.path.abspath("data")
work = os.path.abspath("realwork")
if os.path.isdir(work):
    shutil.rmtree(work)
shutil.copytree(src, work)
env = dict(os.environ, TZ="UTC", LC_ALL="C.UTF-8")
def tree(root, rootname):
    out = []
    if not os.path.isdir(root):
        return f"tree: {rootname}: no such directory\n"
    for dp, dns, fns in os.walk(root):
        dns.sort()
        rel = os.path.relpath(dp, root)
        for n in sorted(fns):
            p = os.path.join(dp, n)
            r = n if rel == "." else f"{rel}/{n}"
            data = os.readlink(p).encode() if os.path.islink(p) else open(p, "rb").read()
            out.append((r, f"{len(data):8}  {zlib.crc32(data):08x}  {r}\n"))
        for n in dns:
            r = (n if rel == "." else f"{rel}/{n}") + "/"
            out.append((r, f"     dir            {r}\n"))
    return "".join(l for _, l in sorted(out))
for line in open(os.path.join(src, "jobs.txt")).read().splitlines():
    if not line or line.startswith("#"):
        continue
    sys.stdout.write(f"$ {line}\n")
    w = line.split(" ")
    if w[0] == "tree":
        sys.stdout.write(tree(os.path.join(work, w[1]), w[1]))
    else:
        p = subprocess.run(w, cwd=work, env=env, capture_output=True)
        sys.stdout.write(p.stdout.decode("utf-8", "replace") + p.stderr.decode("utf-8", "replace"))
        if p.returncode:
            sys.stdout.write(f"[exit status {p.returncode}]\n")
    sys.stdout.write("\n")
    sys.stdout.flush()
