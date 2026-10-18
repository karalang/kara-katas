#!/usr/bin/env python3
"""The oracle: runs data/jobs.tsv with Python's cryptography library (and
hashlib/hmac for the hashes) and prints expected.out. The vault jobs keep
their state in data/*.vault, written in mini_vault's text format. Run
mk.py first."""
import base64
import hashlib
import hmac

from cryptography.exceptions import InvalidTag
from cryptography.fernet import Fernet, InvalidToken, MultiFernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def arg(s):
    """x:<hex>, t:<text> (\\n and \\t escaped), f:<file>, or - for empty."""
    if s == "-":
        return b""
    if s.startswith("x:"):
        return bytes.fromhex(s[2:])
    if s.startswith("t:"):
        return s[2:].replace("\\n", "\n").replace("\\t", "\t").encode()
    if s.startswith("f:"):
        with open("data/" + s[2:], "rb") as f:
            return f.read()
    raise ValueError("bad argument " + s)


def hexlines(b):
    if not b:
        return "  (0 bytes)"
    return "\n".join("  " + b[i:i + 32].hex() for i in range(0, len(b), 32))


def shown(b):
    """Text that is printable UTF-8 as itself, anything else as hex."""
    try:
        s = b.decode("utf-8")
        if all(c >= " " or c == "\n" for c in s):
            return "\n".join("  | " + line for line in s.split("\n"))
    except UnicodeDecodeError:
        pass
    return hexlines(b)


# ---------------------------------------------------------------- vault

def kdf(pw, salt, iters):
    return PBKDF2HMAC(hashes.SHA256(), 32, salt, iters).derive(pw)


def entry_nonce(seed, i):
    return hmac.new(seed, str(i).encode(), hashlib.sha256).digest()[:12]


class Vault:
    def __init__(self, path):
        self.path = "data/" + path

    def load(self):
        with open(self.path) as f:
            lines = f.read().split("\n")[:-1]
        if not lines or lines[0] != "kvault 1":
            raise VaultError("not a vault file")
        kdf_line = lines[1].split(" ")
        self.iters = int(kdf_line[2])
        self.salt = bytes.fromhex(kdf_line[3])
        c = lines[2].split(" ")
        self.check = (bytes.fromhex(c[1]), bytes.fromhex(c[2]))
        self.entries = []
        for line in lines[3:]:
            p = line.split(" ")
            self.entries.append([p[1], bytes.fromhex(p[2]), bytes.fromhex(p[3])])

    def save(self):
        out = ["kvault 1", "kdf pbkdf2-sha256 %d %s" % (self.iters, self.salt.hex()),
               "check %s %s" % (self.check[0].hex(), self.check[1].hex())]
        for name, nonce, ct in self.entries:
            out.append("entry %s %s %s" % (name, nonce.hex(), ct.hex()))
        with open(self.path, "w") as f:
            f.write("\n".join(out) + "\n")

    def unlock(self, pw):
        key = kdf(pw, self.salt, self.iters)
        try:
            AESGCM(key).decrypt(self.check[0], self.check[1], b"check")
        except InvalidTag:
            raise VaultError("wrong passphrase")
        return key


class VaultError(Exception):
    pass


def vault_job(f):
    kind = f[0]
    v = Vault(f[1])
    if kind == "vault-init":
        pw, v.salt, v.iters, nonce = arg(f[2]), arg(f[3]), int(f[4]), arg(f[5])
        key = kdf(pw, v.salt, v.iters)
        v.check = (nonce, AESGCM(key).encrypt(nonce, b"kvault-check", b"check"))
        v.entries = []
        v.save()
        return "  created %s, %d iterations" % (f[1], v.iters)
    v.load()
    if kind == "vault-list":
        return "\n".join("  " + e[0] for e in v.entries) if v.entries else "  (no entries)"
    if kind == "vault-cat":
        with open(v.path) as fh:
            return "\n".join("  " + line for line in fh.read().split("\n")[:-1])
    if kind == "vault-flip":
        for e in v.entries:
            if e[0] == f[2]:
                ct = bytearray(e[2])
                ct[int(f[3])] ^= 1
                e[2] = bytes(ct)
                v.save()
                return "  flipped a bit of %s" % f[2]
        raise VaultError("no entry " + f[2])
    key = v.unlock(arg(f[2]))
    if kind == "vault-put":
        name, value, nonce = f[3], arg(f[4]), arg(f[5])
        ct = AESGCM(key).encrypt(nonce, value, name.encode())
        for e in v.entries:
            if e[0] == name:
                e[1], e[2] = nonce, ct
                v.save()
                return "  replaced %s (%d bytes)" % (name, len(value))
        v.entries.append([name, nonce, ct])
        v.entries.sort(key=lambda e: e[0])
        v.save()
        return "  added %s (%d bytes)" % (name, len(value))
    if kind == "vault-get":
        for e in v.entries:
            if e[0] == f[3]:
                try:
                    return shown(AESGCM(key).decrypt(e[1], e[2], e[0].encode()))
                except InvalidTag:
                    raise VaultError("entry %s is corrupt" % e[0])
        raise VaultError("no entry " + f[3])
    if kind == "vault-del":
        for i, e in enumerate(v.entries):
            if e[0] == f[3]:
                del v.entries[i]
                v.save()
                return "  deleted " + f[3]
        raise VaultError("no entry " + f[3])
    if kind == "vault-rekey":
        new_pw, salt, iters, seed = arg(f[3]), arg(f[4]), int(f[5]), arg(f[6])
        plain = []
        for e in v.entries:
            try:
                plain.append((e[0], AESGCM(key).decrypt(e[1], e[2], e[0].encode())))
            except InvalidTag:
                raise VaultError("entry %s is corrupt" % e[0])
        v.salt, v.iters = salt, iters
        nkey = kdf(new_pw, salt, iters)
        n0 = entry_nonce(seed, 0)
        v.check = (n0, AESGCM(nkey).encrypt(n0, b"kvault-check", b"check"))
        v.entries = []
        for i, (name, value) in enumerate(plain):
            n = entry_nonce(seed, i + 1)
            v.entries.append([name, n, AESGCM(nkey).encrypt(n, value, name.encode())])
        v.save()
        return "  rekeyed %d entries, %d iterations" % (len(plain), iters)
    raise ValueError(kind)


# ---------------------------------------------------------------- jobs

def run(f):
    kind = f[0]
    if kind.startswith("vault-"):
        return vault_job(f)
    a = [arg(x) for x in f[1:]] if kind not in ("pbkdf2", "hkdf", "fernet-seal", "fernet-open", "fernet-multi") else None
    if kind == "sha256":
        return "  " + hashlib.sha256(a[0]).hexdigest()
    if kind == "hmac":
        return "  " + hmac.new(a[0], a[1], hashlib.sha256).hexdigest()
    if kind == "pbkdf2":
        return hexlines(PBKDF2HMAC(hashes.SHA256(), int(f[4]), arg(f[2]), int(f[3])).derive(arg(f[1])))
    if kind == "hkdf":
        return hexlines(HKDF(hashes.SHA256(), int(f[4]), arg(f[2]), arg(f[3])).derive(arg(f[1])))
    if kind == "aes-ecb":
        e = Cipher(algorithms.AES(a[0]), modes.ECB()).encryptor()
        return hexlines(e.update(a[1]) + e.finalize())
    if kind == "aes-cbc":
        e = Cipher(algorithms.AES(a[0]), modes.CBC(a[1])).encryptor()
        return hexlines(e.update(a[2]) + e.finalize())
    if kind == "aes-ctr":
        e = Cipher(algorithms.AES(a[0]), modes.CTR(a[1])).encryptor()
        return hexlines(e.update(a[2]) + e.finalize())
    if kind == "gcm-seal":
        return hexlines(AESGCM(a[0]).encrypt(a[1], a[3], a[2] or None))
    if kind == "gcm-open":
        return shown(AESGCM(a[0]).decrypt(a[1], a[3], a[2] or None))
    if kind == "chacha-seal":
        return hexlines(ChaCha20Poly1305(a[0]).encrypt(a[1], a[3], a[2] or None))
    if kind == "chacha-open":
        return shown(ChaCha20Poly1305(a[0]).decrypt(a[1], a[3], a[2] or None))
    if kind == "fernet-seal":
        tok = Fernet(f[1].encode())._encrypt_from_parts(arg(f[4]), int(f[2]), arg(f[3]))
        return "  " + tok.decode()
    if kind == "fernet-open":
        return shown(Fernet(f[1].encode()).decrypt_at_time(f[2].encode(), int(f[3]), int(f[4])))
    if kind == "fernet-multi":
        m = MultiFernet([Fernet(k.encode()) for k in f[1].split(",")])
        return shown(m.decrypt_at_time(f[2].encode(), int(f[3]), int(f[4])))
    raise ValueError(kind)


def main():
    with open("data/jobs.tsv") as fh:
        jobs = fh.read().split("\n")[:-1]
    for job in jobs:
        f = job.split("\t")
        print("== " + " ".join(f))
        try:
            print(run(f))
        except Exception as e:
            msg = str(e)
            print("  " + type(e).__name__ + (": " + msg if msg else ""))


if __name__ == "__main__":
    main()
