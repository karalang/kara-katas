# Checks mini_shadow.py against the real tools: shadow 4.13's pwck,
# chage and passwd (run with -R on a copy of each root, which they
# need as an absolute path), OpenSSL 3.0's `openssl passwd`, and
# libxcrypt's crypt() through perl. After each job the two copies of
# data/sys/etc/shadow must be identical. `login` and `htpasswd` have no
# real counterpart here and are not checked.
import os, shlex, shutil, subprocess, tempfile
import mk, mini_shadow

os.environ["LC_ALL"] = "C"
here = os.getcwd()
if os.path.isdir("data"):
    shutil.rmtree("data")
mk.write_all()
mini_shadow.build_roots()
other = tempfile.mkdtemp()
shutil.copytree("data", other + "/data", symlinks=True)
bad = 0
checked = 0
for line in mini_shadow.read_lines("data/jobs.txt"):
    if line == "" or line.startswith("#"):
        continue
    w = shlex.split(line)
    if w[0] in ("login", "htpasswd"):
        job = mini_shadow.Job()
        mini_shadow.run_line(job, line)
        continue
    job = mini_shadow.Job()
    mini_shadow.run_line(job, line)
    if w[0] == "crypt":
        r = subprocess.run(["perl", "-e", 'print crypt($ARGV[0], $ARGV[1]), "\n"', w[1], w[2]],
                           capture_output=True, text=True)
    else:
        args = [a.replace("data/", other + "/data/") if a.startswith("data/") else a for a in w]
        r = subprocess.run(args, capture_output=True, text=True, cwd=other)
    checked += 1
    same = (job.out, job.err, job.status) == (r.stdout, r.stderr, r.returncode)
    a = open("data/sys/etc/shadow").read()
    b = open(other + "/data/sys/etc/shadow").read()
    if not same or a != b:
        bad += 1
        print("DIFFERS:", line)
        print("  real   :", repr(r.stdout[:500]), repr(r.stderr[:300]), r.returncode)
        print("  mirror :", repr(job.out[:500]), repr(job.err[:300]), job.status)
        if a != b:
            print("  shadow files differ")
shutil.rmtree(other)
print("jobs checked:", checked, "differing:", bad)
