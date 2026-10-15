# Builds data/: files and archives made by XZ Utils 5.4.5, with several
# checks, filters, blocks and streams, plus damaged ones, for mini_xz.
import os, random, shutil, struct, subprocess
# data/jobs.txt is written by hand; keep it across the rebuild.
JOBS = open("data/jobs.txt").read()
if os.path.isdir("data"):
    shutil.rmtree("data")
os.makedirs("data")
random.seed(3)
def sh(c):
    subprocess.run(c, shell=True, check=True, cwd="data")
words = "alpha beta gamma delta kara stream block index check filter".split()
open("data/notes.txt", "w").write("".join(" ".join(random.choice(words) for _ in range(8)) + "\n" for _ in range(300)))
open("data/rand.bin", "wb").write(bytes(random.randrange(256) for _ in range(3000)))
# 16-bit stereo samples: the delta filter's case
samples = bytearray()
for i in range(3000):
    l = int(8000 * ((i % 100) / 50 - 1)); r = -l // 2
    samples += struct.pack("<hh", l, r)
open("data/audio.raw", "wb").write(samples)
open("data/hello.c", "w").write('#include <stdio.h>\n\nint main(int argc, char **argv) {\n    for (int i = 1; i < argc; i++)\n        printf("hello, %s\\n", argv[i]);\n    return argc > 1 ? 0 : 1;\n}\n')
open("data/empty.txt", "w").close()
sh("gcc -O2 -s -o hello hello.c")
sh("xz -k notes.txt")
sh("xz -c -1 --check=crc32 notes.txt > notes-crc32.xz")
sh("xz -c -0 --check=sha256 notes.txt > notes-sha256.xz")
sh("xz -c --check=none hello.c > none.xz")
sh("xz -c -T2 --block-size=4KiB notes.txt > multi.xz")
sh("xz -c --delta=dist=4 --lzma2=preset=6 audio.raw > audio.raw.xz && rm audio.raw")
sh("xz -c --x86 --lzma2=preset=6 hello > hello.xz && rm hello")
sh("xz -c rand.bin > rand.bin.xz && rm rand.bin")
sh("xz -c empty.txt > empty.xz")
sh("xz -c --format=lzma hello.c > legacy.lzma")
# two streams with stream padding between and after them
sh("xz -c --check=crc32 hello.c > s1 && printf 'two streams, one file\\n' | xz -c > s2")
s1 = open("data/s1", "rb").read(); s2 = open("data/s2", "rb").read()
open("data/concat.xz", "wb").write(s1 + b"\0" * 8 + s2 + b"\0" * 4)
os.remove("data/s1"); os.remove("data/s2")
notes = open("data/notes.txt.xz", "rb").read()
open("data/trunc.xz", "wb").write(notes[:400])
b = bytearray(notes); b[200] ^= 1
open("data/flip.xz", "wb").write(b)
# the CRC64 sits just before the index; change its first byte
b = bytearray(notes); b[len(notes) - 12 - 12 - 8] ^= 0x40
open("data/badcheck.xz", "wb").write(b)
b = bytearray(notes); b[-1] ^= 0xff
open("data/badfooter.xz", "wb").write(b)
open("data/plain.xz", "w").write("this was never compressed\n")
open("data/tiny.xz", "wb").write(b"\xfd7z")
open("data/jobs.txt", "w").write(JOBS)
