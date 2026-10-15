# Builds data/: text and binary inputs and archives made by bzip2 1.0.8,
# plus damaged ones, for mini_bzip2.
import os, random, shutil, subprocess
# data/jobs.txt is written by hand; keep it across the rebuild.
JOBS = open("data/jobs.txt").read()
if os.path.isdir("data"):
    shutil.rmtree("data")
os.makedirs("data")
random.seed(11)
paths = ["/", "/index.html", "/api/v1/items", "/api/v1/items/42", "/static/app.js", "/login", "/search?q=kara"]
agents = ["curl/8.5.0", "Mozilla/5.0 (X11; Linux x86_64)", "kube-probe/1.30"]
lines = []
for i in range(400):
    ip = f"10.0.{random.randrange(4)}.{random.randrange(1, 60)}"
    t = f"15/Oct/2026:{8 + i // 400:02}:{(i // 7) % 60:02}:{i % 60:02} +0000"
    p = random.choice(paths)
    st = random.choice([200] * 8 + [304, 404, 500])
    lines.append(f'{ip} - - [{t}] "GET {p} HTTP/1.1" {st} {random.randrange(80, 9000)} "-" "{random.choice(agents)}"\n')
open("data/access.log", "w").write("".join(lines))
words = "the quick brown fox jumps over lazy dogs while kara compiles every block twice".split()
open("data/poem.txt", "w").write("".join(" ".join(random.choice(words) for _ in range(9)) + "\n" for _ in range(60)))
# long runs: run-length stage one and RUNA/RUNB codes
open("data/runs.bin", "wb").write(b"a" * 300 + b"b" * 3 + b"c" * 4 + b"d" * 5 + b"\0" * 1000 + bytes(range(256)) * 3 + b"z" * 255)
open("data/empty.txt", "w").close()
# a file of nearly one 100k block at -1
big = []
for i in range(2900):
    big.append(f"{i:05} {random.choice(words)} {random.random():.6f} {''.join(random.choice('abcdef0123') for _ in range(12))}\n")
open("data/big.txt", "w").write("".join(big))
def sh(c):
    subprocess.run(c, shell=True, check=True, cwd="data")
sh("bzip2 -k -9 access.log && bzip2 -k -1 big.txt && rm big.txt && bzip2 -k empty.txt && mv empty.txt.bz2 empty.bz2")
open("data/second.txt", "w").write("a second stream, appended with cat\n")
sh("bzip2 -c poem.txt > poem1.bz2 && bzip2 -c second.txt > second.bz2 && cat poem1.bz2 second.bz2 > concat.bz2 && rm poem1.bz2 second.bz2 second.txt")
acc = open("data/access.log.bz2", "rb").read()
open("data/trunc.bz2", "wb").write(acc[:len(acc) // 2])
bad = bytearray(acc)
bad[len(bad) // 3] ^= 0x10
open("data/flipped.bz2", "wb").write(bad)
open("data/trailing.bz2", "wb").write(acc + b"garbage after the stream\n")
open("data/notes.bz2", "w").write("not compressed at all\n")
open("data/jobs.txt", "w").write(JOBS)
