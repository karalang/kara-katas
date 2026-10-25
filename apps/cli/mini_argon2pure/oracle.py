"""Play data/jobs.txt through the vendored argon2pure 1.3 and print what each
step returned or raised. Its output is expected.out.

The password store (PHC strings, logins, rehashing, the users file) is
this app's own code, the same here as in mini_argon2pure.kara; argon2pure
does the hashing.

Run: python3 -I -B oracle.py > expected.out"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "vendor"))

import argon2pure  # noqa: E402

TYPES = {"d": argon2pure.ARGON2D, "i": argon2pure.ARGON2I, "id": argon2pure.ARGON2ID}
TYPE_NAMES = {0: "argon2d", 1: "argon2i", 2: "argon2id"}
B64 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"


def unesc(text):
    out = []
    i = 0
    while i < len(text):
        if text[i] == "~":
            out.append(int(text[i + 1:i + 3], 16))
            i += 3
        else:
            out.append(ord(text[i]))
            i += 1
    return bytes(out)


def value(tok):
    if tok.startswith("h:"):
        return bytes.fromhex(tok[2:])
    if tok.startswith("b:"):
        return unesc(tok[2:])
    if tok.startswith("r:"):
        _, n, pat = tok.split(":")
        n = int(n)
        p = bytes.fromhex(pat)
        return (p * (n // len(p) + 1))[:n]
    raise ValueError("bad value " + tok)


def fnv(data):
    h = 2166136261
    for c in data:
        h = ((h ^ c) * 16777619) & 0xFFFFFFFF
    return h


def err(e):
    msg = str(e)
    if msg:
        return "! %s: %s" % (type(e).__name__, msg)
    return "! %s" % type(e).__name__


def opts(toks):
    d = {}
    for t in toks:
        k, v = t.split("=", 1)
        d[k] = v
    return d


# ---------------------------------------------------------------- PHC strings

class BadHash(Exception):
    pass


def b64e(data):
    out = ""
    for i in range(0, len(data), 3):
        chunk = data[i:i + 3]
        n = int.from_bytes(chunk + b"\0" * (3 - len(chunk)), "big")
        for k in range(len(chunk) + 1):
            out += B64[(n >> (18 - 6 * k)) & 63]
    return out


def b64d(text):
    if len(text) % 4 == 1:
        return None
    bits = 0
    nbits = 0
    out = bytearray()
    for ch in text:
        k = B64.find(ch)
        if k < 0:
            return None
        bits = (bits << 6) | k
        nbits += 6
        if nbits >= 8:
            nbits -= 8
            out.append((bits >> nbits) & 255)
    return bytes(out)


def number(text):
    if not text or len(text) > 10 or not all("0" <= c <= "9" for c in text):
        return None
    if len(text) > 1 and text[0] == "0":
        return None
    return int(text)


def phc_encode(type_code, version, m, t, p, salt, digest):
    return "$%s$v=%d$m=%d,t=%d,p=%d$%s$%s" % (TYPE_NAMES[type_code], version, m, t, p, b64e(salt), b64e(digest))


def phc_decode(s):
    parts = s.split("$")
    if len(parts) < 2 or parts[0] != "":
        raise BadHash("not a PHC string")
    names = {v: k for k, v in TYPE_NAMES.items()}
    if parts[1] not in names:
        raise BadHash("unknown type '%s'" % parts[1])
    type_code = names[parts[1]]
    idx = 2
    version = 0x10
    if len(parts) > idx and parts[idx].startswith("v="):
        version = number(parts[idx][2:])
        if version not in (0x10, 0x13):
            raise BadHash("bad version '%s'" % parts[idx][2:])
        idx += 1
    if len(parts) != idx + 3:
        raise BadHash("expected %d fields, found %d" % (idx + 3, len(parts)))
    fields = parts[idx].split(",")
    vals = []
    if len(fields) == 3:
        for name, f in zip(("m=", "t=", "p="), fields):
            if f.startswith(name) and number(f[2:]) is not None:
                vals.append(number(f[2:]))
    if len(vals) != 3:
        raise BadHash("bad parameters '%s'" % parts[idx])
    salt = b64d(parts[idx + 1])
    if salt is None:
        raise BadHash("bad salt")
    digest = b64d(parts[idx + 2])
    if digest is None or len(digest) < 4:
        raise BadHash("bad hash")
    return type_code, version, vals[0], vals[1], vals[2], salt, digest


# ---------------------------------------------------------------- the store

class Store:
    def __init__(self):
        self.users = {}
        self.policy = (argon2pure.ARGON2ID, 1, 8, 1)
        self.pepper = b""
        self.salts = 0
        self.objs = {}

    def new_salt(self, user):
        self.salts += 1
        return argon2pure.Blake2b(b"salt:" + user.encode() + b":" + str(self.salts).encode(),
                                  digest_length=16).digest()

    def make(self, user, pw):
        type_code, t, m, p = self.policy
        salt = self.new_salt(user)
        digest = argon2pure.argon2(pw, salt, t, m, p, 32, self.pepper, b"", type_code, use_threads=True)
        return phc_encode(type_code, 0x13, m, t, p, salt, digest)

    def verify(self, phc, pw):
        type_code, version, m, t, p, salt, digest = phc_decode(phc)
        got = argon2pure.argon2(pw, salt, t, m, p, len(digest), self.pepper, b"", type_code, version=version,
                                use_threads=True)
        stale = (type_code, version, m, t, p, len(digest)) != (self.policy[0], 0x13, self.policy[2],
                                                              self.policy[1], self.policy[3], 32)
        return got == digest, stale


def run_step(st, line):
    toks = line.split(" ")
    op = toks[0]
    if op == "a2":
        o = opts(toks[1:])
        type_code = TYPES[o["type"]] if o.get("type") in TYPES else int(o.get("type", "1"))
        args = dict(tag_length=int(o.get("tag", "32")), secret=value(o.get("secret", "b:")),
                    associated_data=value(o.get("ad", "b:")), type_code=type_code,
                    version=int(o["v"]) if "v" in o else argon2pure.ARGON2_DEFAULT_VERSION, use_threads=True)
        if "threads" in o:
            args["threads"] = int(o["threads"])
        try:
            r = argon2pure.argon2(value(o.get("pw", "b:password")), value(o.get("salt", "b:saltysaltsaltysalt")),
                                  int(o["t"]), int(o["m"]), int(o["p"]), **args)
            print(line + " = " + r.hex())
        except argon2pure.Argon2Error as e:
            print(line + " = " + err(e))
    elif op == "b2":
        data = value(toks[1])
        o = opts(toks[2:])
        key = value(o.get("key", "b:"))
        n = int(o.get("len", "64"))
        label = "b2 %d bytes, key %d, len %d = " % (len(data), len(key), n)
        try:
            print(label + argon2pure.Blake2b(data, key=key, digest_length=n).hexdigest().decode())
        except AssertionError as e:
            print(label + err(e))
    elif op == "new":
        o = opts(toks[2:])
        try:
            st.objs[toks[1]] = argon2pure.Blake2b(key=value(o.get("key", "b:")), digest_length=int(o.get("len", "64")))
            print("new %s = ok" % toks[1])
        except AssertionError as e:
            print("new %s = %s" % (toks[1], err(e)))
    elif op == "up":
        data = value(toks[2])
        try:
            st.objs[toks[1]].update(data)
            print("up %s +%d = ok" % (toks[1], len(data)))
        except AssertionError as e:
            print("up %s +%d = %s" % (toks[1], len(data), err(e)))
    elif op == "dig":
        print("dig %s = %s" % (toks[1], st.objs[toks[1]].hexdigest().decode()))
    elif op == "chain":
        which = toks[1]
        if which == "keyed":
            cur = b"!"
            for i in range(1, 10):
                cur = argon2pure.Blake2b(cur, key=cur[:i]).digest()
        elif which == "unkeyed":
            cur = b""
            for i in range(100):
                cur = argon2pure.Blake2b(cur).digest()
            cur = argon2pure.Blake2b(cur).digest()
        else:
            cur = b"!"
            for i in range(1, 64):
                cur = argon2pure.Blake2b(cur, digest_length=i, key=cur[:i]).digest()
        print("chain %s = %s" % (which, cur.hex()))
    elif op == "hp":
        n = int(toks[1])
        r = argon2pure._H_prime(value(toks[2]), n)
        if n > 128:
            print("hp %d = %d bytes, fnv %08x, starts %s" % (n, len(r), fnv(r), r[:16].hex()))
        else:
            print("hp %d = %s" % (n, r.hex()))
    elif op == "policy":
        o = opts(toks[1:])
        st.policy = (TYPES[o["type"]], int(o["t"]), int(o["m"]), int(o["p"]))
        print("policy = %s t=%s m=%s p=%s" % (TYPE_NAMES[st.policy[0]], o["t"], o["m"], o["p"]))
    elif op == "pepper":
        st.pepper = value(toks[1])
        print("pepper = %d bytes" % len(st.pepper))
    elif op == "reg":
        user = toks[1]
        if user in st.users:
            print("reg %s: already registered" % user)
            return
        st.users[user] = st.make(user, value(toks[2]))
        print("reg %s = %s" % (user, st.users[user]))
    elif op == "login":
        user = toks[1]
        if user not in st.users:
            print("login %s: no such user" % user)
            return
        ok, stale = st.verify(st.users[user], value(toks[2]))
        if not ok:
            print("login %s: denied" % user)
        elif stale:
            st.users[user] = st.make(user, value(toks[2]))
            print("login %s: ok, rehashed to %s" % (user, st.users[user]))
        else:
            print("login %s: ok" % user)
    elif op == "forget":
        del st.users[toks[1]]
        print("forget %s: %d users left" % (toks[1], len(st.users)))
    elif op == "check":
        try:
            ok, stale = st.verify(toks[1], value(toks[2]))
            print("check: %s" % (("ok, needs rehash" if stale else "ok") if ok else "denied"))
        except BadHash as e:
            print("check: ! bad hash: %s" % e)
        except argon2pure.Argon2Error as e:
            print("check: " + err(e))
    elif op == "save":
        text = "".join("%s:%s\n" % (u, p) for u, p in st.users.items())
        with open(toks[1], "w") as f:
            f.write(text)
        print("save %s: %d users, %d bytes, fnv %08x" % (toks[1], len(st.users), len(text), fnv(text.encode())))
    elif op == "drop":
        st.users = {}
        print("drop: 0 users")
    elif op == "load":
        with open(toks[1]) as f:
            text = f.read()
        st.users = {}
        for ln in text.split("\n"):
            if ln:
                k = ln.index(":")
                st.users[ln[:k]] = ln[k + 1:]
        print("load %s: %d users" % (toks[1], len(st.users)))
    else:
        raise ValueError("bad step " + line)


def main():
    with open(os.path.join(HERE, "data", "jobs.txt")) as f:
        lines = f.read().split("\n")
    st = Store()
    for line in lines:
        if not line:
            continue
        if line.startswith("job "):
            st.objs = {}
            print("== " + line[4:])
            continue
        run_step(st, line)
    if os.path.exists("users.db"):
        os.remove("users.db")


main()
