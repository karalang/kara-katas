# Builds data/: a small release directory and checksum files made with
# GNU coreutils 9.4, some of them damaged, for mini_hashsum.
import os, random, shutil, subprocess
if os.path.isdir("data"):
    shutil.rmtree("data")
os.makedirs("data/release")
random.seed(5)
def sh(c):
    subprocess.run(c, shell=True, check=True, cwd="data")
open("data/README", "w").write("kara 1.4.0\n\nA compiler for the Kara language.\nSee release/notes.md for what changed.\n")
lic = "Permission is hereby granted, free of charge, to any person obtaining a copy of this software.\n"
open("data/LICENSE", "w").write(lic * 12)
open("data/empty.dat", "w").close()
open("data/odd\\name.txt", "w").write("a file whose name has a backslash\n")
open("data/release/kara-1.4.0.tar", "wb").write(bytes(random.randrange(256) for _ in range(20000)))
open("data/release/notes.md", "w").write("".join(f"- change {i}: fixed item {random.randrange(1000)}\n" for i in range(150)))
open("data/release/kara.sig", "wb").write(bytes(random.randrange(256) for _ in range(129)))
sh("sha256sum README LICENSE release/kara-1.4.0.tar release/notes.md release/kara.sig > SHA256SUMS")
# a wrong digest, a missing file, a malformed line and a blank line
lines = open("data/SHA256SUMS").read().splitlines()
bad = lines[:2]
bad.append("0" * 64 + "  release/kara-1.4.0.tar")
bad.append(lines[3])
bad.append("e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  release/kara-1.3.9.tar")
bad.append("this is not a checksum line")
bad.append("")
bad.append(lines[4])
open("data/SHA256SUMS.bad", "w").write("\n".join(bad) + "\n")
sh("md5sum --tag README LICENSE empty.dat > MD5SUMS")
sh("b2sum README release/notes.md > B2SUMS")
sh("sha1sum 'odd\\name.txt' README > SHA1SUMS")
# one file of every algorithm cksum -c reads, untagged ones excepted
sh("cksum -a sha512 README > CHECKSUMS && cksum -a sha256 --base64 LICENSE >> CHECKSUMS"
   " && cksum -a blake2b -l 256 empty.dat >> CHECKSUMS && cksum -a sha1 release/kara.sig >> CHECKSUMS"
   " && cksum -a sha224 release/notes.md >> CHECKSUMS && cksum -a sha384 README >> CHECKSUMS")
# change the SHA384 digest's first digit
c = open("data/CHECKSUMS").read().replace("SHA384 (README) = 5", "SHA384 (README) = 6")
open("data/CHECKSUMS", "w").write(c + "MD5 (release/notes.md) = deadbeef\n")
shutil.copy("jobs.txt", "data/jobs.txt")
