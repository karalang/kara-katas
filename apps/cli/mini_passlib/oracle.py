"""Replay data/jobs.tsv against the vendored passlib 1.7.4.

Each job is one Python statement: `NAME = expr` binds a handler, context
or file, anything else is evaluated and its value printed. Salts and
varied rounds come from a seeded generator patched in for passlib's
`rng`, reseeded before every job, so the output is reproducible.
"""
import logging
import os
import sys
import warnings

HERE = os.path.dirname(os.path.abspath(__file__))
os.environ["PASSLIB_BUILTIN_BCRYPT"] = "enabled"
sys.path.insert(0, os.path.join(HERE, "vendor"))
os.chdir(HERE)

import passlib.hash as ph  # noqa: E402
import passlib.utils  # noqa: E402
import passlib.utils.handlers as uh  # noqa: E402
from passlib.context import CryptContext  # noqa: E402
from passlib.apache import HtpasswdFile, HtdigestFile  # noqa: E402


class FakeRng:
    """A 31-bit LCG standing in for random.SystemRandom."""

    def __init__(self):
        self.s = 1

    def seed(self, s):
        self.s = s & 0x7FFFFFFF

    def _byte(self):
        self.s = (self.s * 1103515245 + 12345) & 0x7FFFFFFF
        return (self.s >> 16) & 0xFF

    def getrandbits(self, k):
        v = 0
        for i in range((k + 7) // 8):
            v |= self._byte() << (8 * i)
        return v & ((1 << k) - 1)

    def randrange(self, a, b=None):
        if b is None:
            a, b = 0, a
        n = b - a
        if n <= 0:
            raise ValueError("empty range for randrange()")
        k = n.bit_length()
        while True:
            v = self.getrandbits(k)
            if v < n:
                return a + v

    def randint(self, a, b):
        return self.randrange(a, b + 1)


RNG = FakeRng()
import passlib.handlers.bcrypt  # noqa: E402
import passlib.handlers.django  # noqa: E402
import passlib.context  # noqa: E402
import passlib.crypto._blowfish  # noqa: E402

for mod in (passlib.utils, uh, passlib.handlers.bcrypt,
            passlib.handlers.django, passlib.context,
            passlib.crypto._blowfish):
    mod.rng = RNG

SCHEMES = """
md5_crypt apr_md5_crypt sha256_crypt sha512_crypt sha1_crypt
des_crypt bsdi_crypt bigcrypt crypt16 bcrypt bcrypt_sha256 scrypt
pbkdf2_sha1 pbkdf2_sha256 pbkdf2_sha512 cta_pbkdf2_sha1 dlitz_pbkdf2_sha1
grub_pbkdf2_sha512 atlassian_pbkdf2_sha1
ldap_md5 ldap_sha1 ldap_salted_md5 ldap_salted_sha1 ldap_salted_sha256
ldap_salted_sha512 ldap_plaintext ldap_hex_md5 ldap_hex_sha1
ldap_md5_crypt ldap_des_crypt ldap_sha512_crypt ldap_pbkdf2_sha256
hex_md4 hex_md5 hex_sha1 hex_sha256 hex_sha512 htdigest
phpass mysql323 mysql41 postgres_md5
nthash lmhash bsd_nthash msdcc
cisco_type7 cisco_pix cisco_asa ldap_hex_md5 ldap_hex_sha1 atlassian_pbkdf2_sha1
django_salted_sha1 django_salted_md5 django_pbkdf2_sha256
django_pbkdf2_sha1 django_disabled
plaintext unix_disabled
""".split()

NS = {"CryptContext": CryptContext, "HtpasswdFile": HtpasswdFile,
      "HtdigestFile": HtdigestFile, "sorted": sorted}


def read_text(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


NS["read_text"] = read_text
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    for name in SCHEMES:
        h = getattr(ph, name)
        if "builtin" in (getattr(h, "backends", None) or ()):
            h.set_backend("builtin")
        NS[name] = h


class Show(logging.Handler):
    def emit(self, record):
        print("  log %s: %s" % (record.levelname, record.getMessage()))


logging.getLogger("passlib").addHandler(Show())
logging.getLogger("passlib").propagate = False


def is_handler(v):
    return isinstance(v, uh.PrefixWrapper) or (
        isinstance(v, type) and hasattr(v, "name") and hasattr(v, "hash"))


def fmt(v):
    if is_handler(v):
        return "<handler %s>" % v.name
    if isinstance(v, CryptContext):
        return "<CryptContext>"
    if isinstance(v, (HtpasswdFile, HtdigestFile)):
        return "<%s>" % type(v).__name__
    if isinstance(v, tuple):
        if len(v) == 1:
            return "(%s,)" % fmt(v[0])
        return "(%s)" % ", ".join(fmt(x) for x in v)
    if isinstance(v, list):
        return "[%s]" % ", ".join(fmt(x) for x in v)
    if isinstance(v, dict):
        return "{%s}" % ", ".join("%s: %s" % (fmt(k), fmt(x))
                                  for k, x in v.items())
    return repr(v)


def show(v):
    if isinstance(v, str):
        for line in v.split("\n"):
            print("  " + line if line else "  |")
    else:
        print("  " + fmt(v))


def run(n, line):
    print("> " + line)
    RNG.seed(1000 + n)
    target = None
    expr = line
    head, sep, tail = line.partition(" = ")
    if sep and head.isidentifier():
        target, expr = head, tail
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        try:
            value = eval(expr, NS)
            err = None
        except Exception as e:  # noqa: BLE001
            err = e
    for w in caught:
        print("  warning %s: %s" % (w.category.__name__, w.message))
    if err is not None:
        print("  error %s: %s" % (type(err).__name__, err))
    elif target:
        NS[target] = value
    else:
        show(value)


def main():
    with open("data/jobs.tsv", encoding="utf-8") as f:
        jobs = [ln.rstrip("\n") for ln in f if ln.strip()]
    for n, line in enumerate(jobs):
        if line.startswith("#"):
            print(line)
            continue
        run(n, line)


main()
