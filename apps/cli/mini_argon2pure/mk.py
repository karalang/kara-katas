"""Write data/jobs.txt: the jobs mini_argon2pure and oracle.py both play.

A job is a title line and steps. Values are written as
  b:<text>       bytes from ASCII text, ~XX for byte XX
  h:<hex>        bytes
  r:<n>:<hex>    bytes: the hex pattern repeated to n bytes
Steps:
  a2 k=v ...           argon2() with type, v, t, m, p, tag, pw, salt,
                       secret, ad and threads
  b2 <value> k=v ...   a one-shot Blake2b with key and len
  new <name> k=v ...   a Blake2b object; up <name> <value>; dig <name>
  chain <which>        one of the Blake2b chains in test_argon2pure.py
  hp <tag> <value>     argon2pure's H' (_H_prime)
  policy k=v ...       the password store's hashing policy
  pepper <value>       the store's secret
  reg <user> <pw>      register a user; login <user> <pw>; forget <user>
  check <hash> <pw>    verify a PHC string
  save <file>; drop; load <file>
Run: python3 -s -P -B mk.py"""
import os
import random

R = random.Random(20261025)
out = []


def job(title):
    out.append("job " + title)


def step(*parts):
    out.append(" ".join(parts))


def esc(text):
    s = ""
    for c in text:
        if c == " " or c == "~" or ord(c) < 33 or ord(c) > 126:
            s += "~%02x" % ord(c)
        else:
            s += c
    return s


def b(text):
    return "b:" + esc(text)


def h(data):
    return "h:" + data.hex()


# ---------------------------------------------------------------- known answers

job("argon2pure's README example")
step("a2 t=1 m=16 p=2 pw=b:password salt=b:randomsalt")

job("RFC 9106 test vectors: Argon2d, Argon2i and Argon2id")
for ty in ("d", "i", "id"):
    step("a2 type=%s t=3 m=32 p=4 pw=r:32:01 salt=r:16:02 secret=r:8:03 ad=r:12:04" % ty)

job("argon2pure's tests: base parameters")
for m in range(8, 18):
    for ty in ("d", "i", "id"):
        for v in ("16", "19"):
            step("a2 type=%s v=%s t=1 m=%d p=1" % (ty, v, m))

job("argon2pure's tests: high memory")
for e in range(4):
    for ty in ("d", "i", "id"):
        for v in ("16", "19"):
            step("a2 type=%s v=%s t=2 m=%d p=2" % (ty, v, 16 + 4 ** e))

job("Tag lengths")
for tag in (4, 16, 31, 32, 33, 63, 64, 65, 96, 97, 100, 128, 200):
    step("a2 type=id t=1 m=8 p=1 tag=%d" % tag)

job("Lanes, passes, secrets and associated data")
for p in (1, 2, 3, 4):
    for t in (1, 3):
        step("a2 type=id t=%d m=%d p=%d pw=b:correct~20horse~20battery~20staple salt=b:NaCl-and-pepper" % (t, 8 * p + 3, p))
step("a2 type=id t=2 m=16 p=2 secret=b:server-side-key")
step("a2 type=id t=2 m=16 p=2 ad=b:user:42")
step("a2 type=id t=2 m=16 p=2 secret=b:server-side-key ad=b:user:42")
step("a2 type=id t=2 m=16 p=2 threads=1")
step("a2 type=id t=2 m=16 p=2 threads=2")
step("a2 type=id t=2 m=16 p=2 threads=8")
step("a2 type=d t=1 m=8 p=1 pw=b: salt=b:")
step("a2 type=i t=1 m=8 p=1 pw=r:300:a5 salt=r:200:5a")
step("a2 type=d t=4 m=24 p=3 v=16")

job("Parameter errors")
step("a2 t=1 m=8 p=0")
step("a2 t=1 m=8 p=-1")
step("a2 t=1 m=8 p=1 threads=0")
step("a2 t=0 m=8 p=1")
step("a2 t=1 m=15 p=2")
step("a2 t=1 m=7 p=1")
step("a2 t=1 m=8 p=1 type=3")
step("a2 t=1 m=8 p=1 v=18")
step("a2 t=0 m=0 p=0 type=9 v=0")
step("a2 t=0 m=0 p=1 type=9 v=0")
step("a2 t=1 m=8 p=1 type=9 v=0")
step("a2 t=1 m=16 p=2 threads=1 tag=8")

# ---------------------------------------------------------------- Blake2b

job("BLAKE2b one-shot")
step("b2 b:")
step("b2 b:abc")
step("b2 b:The~20quick~20brown~20fox~20jumps~20over~20the~20lazy~20dog")
step("b2 b:abc len=32")
step("b2 b:abc len=1")
step("b2 b:abc key=b:k")
for n in (63, 64, 127, 128, 129, 255, 256, 257, 1000):
    step("b2 r:%d:%02x" % (n, n % 256))
step("b2 r:64:00 key=h:%s" % bytes(range(64)).hex())
step("b2 h:%s key=h:%s" % (bytes(range(255)).hex(), bytes(range(64)).hex()))
step("b2 b:abc key=r:128:6b len=64")
step("b2 b:abc key=r:129:6b")
step("b2 b:abc len=0")
step("b2 b:abc len=65")

job("BLAKE2b incremental")
for sizes in ((1, 2, 3), (127, 1), (128,), (128, 1), (64, 64, 64), (129, 127, 128), (200, 56), (0, 0, 128, 0)):
    step("new s")
    data = bytes(R.randrange(256) for _ in range(sum(sizes)))
    i = 0
    for n in sizes:
        step("up s " + h(data[i:i + n]) if n else "up s b:")
        i += n
    step("dig s")
    step("b2 " + h(data))
step("new k key=b:secret len=20")
step("up k b:message")
step("dig k")
step("dig k")
step("up k b:more")
step("new z len=99")

job("BLAKE2b chains from argon2pure's tests")
step("chain keyed")
step("chain unkeyed")
step("chain various")

job("Argon2's variable-length hash H'")
for tag in (1, 4, 32, 63, 64, 65, 96, 128, 129, 1024):
    step("hp %d b:password" % tag)
step("hp 72 h:%s" % bytes(range(72)).hex())

# ---------------------------------------------------------------- the password store

USERS = ["alice", "bob", "carol", "dave", "erin", "frank"]
PWS = {u: "%s-%d-%s" % (u, R.randrange(1000, 9999), R.choice(["Tulip", "Ember", "Quartz", "Fjord", "Lumen"]))
       for u in USERS}

job("A login service's password store")
step("policy type=id t=1 m=8 p=1")
step("pepper b:not-a-real-pepper")
for u in USERS[:4]:
    step("reg %s %s" % (u, b(PWS[u])))
step("reg alice " + b("again"))
step("login alice " + b(PWS["alice"]))
step("login alice " + b(PWS["alice"] + "!"))
step("login bob " + b(PWS["bob"].upper()))
step("login mallory b:guess")
step("save users.db")
step("drop")
step("login carol " + b(PWS["carol"]))
step("load users.db")
step("login carol " + b(PWS["carol"]))

job("The policy is raised and logins rehash")
step("policy type=id t=2 m=16 p=2")
step("login alice " + b(PWS["alice"]))
step("login alice " + b(PWS["alice"]))
step("login bob " + b("wrong"))
step("login bob " + b(PWS["bob"]))
for u in USERS[4:]:
    step("reg %s %s" % (u, b(PWS[u])))
step("forget dave")
step("login dave " + b(PWS["dave"]))
step("save users.db")
step("drop")
step("load users.db")
for u in USERS:
    step("login %s %s" % (u, b(PWS[u])))

job("A new pepper locks out every old hash")
step("pepper b:another-fake-pepper")
step("login erin " + b(PWS["erin"]))
step("pepper b:not-a-real-pepper")
step("login erin " + b(PWS["erin"]))

job("Hashes from elsewhere")
step("policy type=i t=1 m=8 p=1")
step("pepper b:")
# argon2pure's README example and the RFC's Argon2id vector as PHC strings
step("check $argon2i$v=19$m=16,t=1,p=2$cmFuZG9tc2FsdA$AWPF+okoGQVesHuKy5T9L/UnPmibNBB9qqrO2mSPHhs b:password")
step("check $argon2i$v=19$m=16,t=1,p=2$cmFuZG9tc2FsdA$AWPF+okoGQVesHuKy5T9L/UnPmibNBB9qqrO2mSPHhs b:Password")
step("check $argon2i$m=16,t=1,p=2$cmFuZG9tc2FsdA$AWPF+okoGQVesHuKy5T9L/UnPmibNBB9qqrO2mSPHhs b:password")
step("check $argon2i$v=16$m=16,t=1,p=2$cmFuZG9tc2FsdA$AWPF+okoGQVesHuKy5T9L/UnPmibNBB9qqrO2mSPHhs b:password")
step("check argon2i$v=19$m=16,t=1,p=2$cmFuZG9tc2FsdA$AWPF b:password")
step("check $argon2x$v=19$m=16,t=1,p=2$cmFuZG9tc2FsdA$AWPF b:password")
step("check $argon2i$v=20$m=16,t=1,p=2$cmFuZG9tc2FsdA$AWPF b:password")
step("check $argon2i$v=19$t=1,m=16,p=2$cmFuZG9tc2FsdA$AWPF b:password")
step("check $argon2i$v=19$m=16,t=1,p=2$cmFuZG9tc2FsdA b:password")
step("check $argon2i$v=19$m=16,t=1,p=2$cmFuZG9tc2Fsd$AWPF+okoGQVesHuKy5T9L/UnPmibNBB9qqrO2mSPHhs b:password")
step("check $argon2i$v=19$m=16,t=1,p=2$cmFuZG9tc2FsdA$AWPF*okoGQVesHuKy5T9L/UnPmibNBB9qqrO2mSPHhs b:password")
step("check $argon2i$v=19$m=4,t=1,p=1$cmFuZG9tc2FsdA$AWPF+okoGQVesHuKy5T9L/UnPmibNBB9qqrO2mSPHhs b:password")
step("check $argon2i$v=19$m=16,t=1,p=2$cmFuZG9tc2FsdA$ b:password")
step("check $argon2i$v=19$m=016,t=1,p=2$cmFuZG9tc2FsdA$AWPF+okoGQVesHuKy5T9L/UnPmibNBB9qqrO2mSPHhs b:password")

os.makedirs("data", exist_ok=True)
with open("data/jobs.txt", "w") as f:
    f.write("\n".join(out) + "\n")
print(len(out), "lines")
