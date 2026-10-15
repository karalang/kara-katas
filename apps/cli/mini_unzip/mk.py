# Builds data/: zip archives made by Info-ZIP zip 3.0 and Python's
# zipfile, and damaged ones, for mini_unzip to read.
import io, os, random, shutil, struct, subprocess, zipfile
os.environ["TZ"] = "UTC"
W = "w"
for d in (W, "data"):
    if os.path.isdir(d):
        shutil.rmtree(d)
os.makedirs(f"{W}/proj/src")
os.makedirs(f"{W}/proj/docs")
os.makedirs("data")
random.seed(7)
words = "alpha beta gamma delta epsilon zeta eta theta iota kappa lambda mu".split()
open(f"{W}/proj/src/main.kara", "w").write('fn main() {\n    println("hello");\n}\n')
open(f"{W}/proj/src/util.kara", "w").write("".join(f"fn f{i}(x: i64) -> i64 {{ x * {i} + {i * i} }}\n" for i in range(40)))
open(f"{W}/proj/docs/guide.md", "w").write("\n".join(" ".join(random.choice(words) for _ in range(12)) for _ in range(120)) + "\n")
open(f"{W}/proj/logo.bin", "wb").write(bytes(random.randrange(256) for _ in range(700)))
open(f"{W}/proj/empty.txt", "w").close()
os.symlink("src/main.kara", f"{W}/proj/link.kara")
def sh(cmd, cwd=W):
    subprocess.run(cmd, shell=True, check=True, cwd=cwd)
sh("touch -h -d '2026-10-01 09:30:12' proj/src/main.kara proj/src/util.kara proj/docs/guide.md proj/logo.bin "
   "proj/empty.txt proj/link.kara proj/src proj/docs proj")
sh("zip -q -r -y infozip.zip proj && echo 'release 1.4' | zip -q -z infozip.zip")
sh("zip -q -P hunter2 secret.zip proj/src/main.kara proj/docs/guide.md")
sh("zip -q -0 -X plain.zip proj/src/main.kara proj/empty.txt")
for n in ("infozip.zip", "secret.zip", "plain.zip"):
    shutil.copy(f"{W}/{n}", f"data/{n}")

# Python's zipfile writing to a stream it cannot seek, so every entry
# has a data descriptor; UTF-8 names, comments.
class NoSeek(io.RawIOBase):
    def __init__(self):
        self.buf = bytearray()
    def writable(self):
        return True
    def write(self, b):
        self.buf += b
        return len(b)
ns = NoSeek()
with zipfile.ZipFile(ns, "w", zipfile.ZIP_DEFLATED) as z:
    zi = zipfile.ZipInfo("café/naïve.txt", (2026, 10, 2, 11, 45, 8))
    zi.compress_type = zipfile.ZIP_DEFLATED
    z.writestr(zi, "déjà vu\n" * 30)
    zi = zipfile.ZipInfo("notes/readme.txt", (2026, 10, 2, 11, 46, 0))
    zi.comment = b"the readme"
    z.writestr(zi, "Read me first.\n", compress_type=zipfile.ZIP_STORED)
    zi = zipfile.ZipInfo("notes/", (2026, 10, 2, 11, 40, 0))
    zi.external_attr = 0o40755 << 16 | 0x10
    z.writestr(zi, "")
    z.comment = b"made by zipfile"
open("data/stream.zip", "wb").write(ns.buf)
with zipfile.ZipFile("data/zip64.zip", "w") as z:
    zi = zipfile.ZipInfo("big/part1.dat", (2026, 10, 3, 8, 0, 0))
    zi.external_attr = 0o100644 << 16
    with z.open(zi, "w", force_zip64=True) as f:
        f.write(b"0123456789abcdef" * 64)
    zi = zipfile.ZipInfo("big/part2.dat", (2026, 10, 3, 8, 0, 2))
    zi.external_attr = 0o100644 << 16
    z.writestr(zi, b"tail\n" * 9, compress_type=zipfile.ZIP_DEFLATED)

# A zip-slip archive: names that climb out of the target directory.
with zipfile.ZipFile("data/evil.zip", "w") as z:
    for name, body in [("ok.txt", "fine\n"), ("../escape.txt", "outside\n"),
                       ("sub/../../../tmp/evil.sh", "rm -rf ~\n"), ("/etc/cron.d/job", "* * * * * root id\n"),
                       ("sub/inner.txt", "inside\n")]:
        zi = zipfile.ZipInfo(name, (2026, 10, 4, 12, 0, 0))
        zi.external_attr = 0o100644 << 16
        z.writestr(zi, body)

good = open("data/infozip.zip", "rb").read()
# A flipped byte inside the stored main.kara: a bad CRC.
bad = bytearray(good)
at = bad.index(b'println("hello")')
bad[at] = ord("P")
open("data/badcrc.zip", "wb").write(bad)
# A self-extractor's stub in front of the archive.
open("data/sfx.zip", "wb").write(b"#!/bin/sh\necho 'self-extracting stub'\nexit 0\n" + b"\0" * 83 + good)
# The end cut off: no end-of-central-directory record.
open("data/trunc.zip", "wb").write(good[:2000])
open("data/notes.txt", "w").write("not a zip file, just notes\n" * 4)
open("data/jobs.txt", "w").write("""# mini_unzip jobs: each line is a command run from data/
zipinfo infozip.zip
zipinfo stream.zip
zipinfo zip64.zip
zipinfo secret.zip
zipinfo evil.zip
unzip -l infozip.zip
unzip -l stream.zip
unzip -l infozip.zip nosuch.txt proj/logo.bin
unzip -l infozip.zip nosuch.txt
unzip -v infozip.zip nosuch.txt proj/*.bin
unzip -t infozip.zip nosuch.txt proj/logo.bin
unzip -v infozip.zip
unzip -v zip64.zip
unzip -v plain.zip
unzip -t infozip.zip
unzip -t stream.zip
unzip -t zip64.zip
unzip -t badcrc.zip
unzip -t -P hunter2 secret.zip
unzip -t -P letmein secret.zip
unzip -t sfx.zip
unzip -l sfx.zip
unzip -t trunc.zip
unzip -l trunc.zip
unzip -l missing.zip
unzip -l notes.txt
unzip -p stream.zip café/naïve.txt
unzip -p -P hunter2 secret.zip proj/src/main.kara
unzip -p stream.zip nosuch
unzip -d out/nested plain.zip
unzip -d out-infozip infozip.zip
tree out-infozip
unzip -d out-stream stream.zip
tree out-stream
unzip -d out-evil evil.zip
tree out-evil
unzip -P hunter2 -d out-secret secret.zip
tree out-secret
unzip -d out-bad badcrc.zip proj/src/main.kara proj/src/util.kara
tree out-bad
""")
