# Writes data/jobs.jsonl: scripts of signing and loading operations,
# written out by hand and drawn at random from a fixed seed.
#
# A job names its signers and serializers in "objs" and then runs "ops"
# against them. A token comes from "value" (text), "hex" (bytes), "use"
# (a token saved earlier with "save") or "last" (the last token signed or
# dumped), and "mut" edits it before use. "now" sets the job's clock,
# which the timestamp signers read.
import base64
import json
import os
import random
import zlib

os.makedirs("data", exist_ok=True)
jobs = []


def job(name, objs, ops, now=1700000000):
    jobs.append({"name": name, "now": now, "objs": objs, "ops": ops})


def last(*mut, **kw):
    d = {"last": True}
    if mut:
        d["mut"] = [list(m) for m in mut]
    d.update(kw)
    return d


def use(name, *mut, **kw):
    d = {"use": name}
    if mut:
        d["mut"] = [list(m) for m in mut]
    d.update(kw)
    return d


def op(name, on, src=None, **kw):
    d = {"op": name, "on": on}
    if src is not None:
        d.update(src)
    d.update(kw)
    return d


# ------------------------------------------------------------ signers

job("signer basics", {
    "s": {"cls": "Signer", "key": "correct horse battery staple"},
}, [
    op("sign", "s", {"value": "hello"}),
    op("unsign", "s", last()),
    op("validate", "s", last()),
    op("unsign", "s", last(["flip", -1])),
    op("unsign", "s", last(["flip", 0])),
    op("unsign", "s", last(["cut", 1])),
    op("unsign", "s", last(["add", "="])),
    op("unsign", "s", last(["add", "x"])),
    op("unsign", "s", {"value": "no separator here"}),
    op("unsign", "s", {"value": "hello."}),
    op("unsign", "s", {"value": "."}),
    op("unsign", "s", {"value": ""}),
    op("validate", "s", {"value": "hello.abc"}),
    op("get_signature", "s", {"value": "hello"}),
    op("derive_key", "s"),
    op("sign", "s", {"value": "a.b.c"}),
    op("unsign", "s", last()),
    op("sign", "s", {"value": ""}),
    op("unsign", "s", last()),
    op("sign", "s", {"value": "caf\u00e9 \u65e5\u672c \U0001f600"}),
    op("unsign", "s", last()),
    op("sign", "s", {"hex": "00ff80fe2e41"}),
    op("unsign", "s", last()),
    op("unsign", "s", last(["repl", "-", "+"])),
    op("unsign", "s", last(["repl", "_", "/"])),
])

job("signature encodings", {
    "s": {"cls": "Signer", "key": "dev-only-key", "salt": "enc"},
}, [
    op("sign", "s", {"value": "x"}, save="t"),
    op("unsign", "s", use("t", ["add", "=="])),
    op("unsign", "s", use("t", ["add", "==="])),
    op("unsign", "s", use("t", ["add", "\u00e9"])),
    op("unsign", "s", use("t", ["add", "!"])),
    op("unsign", "s", use("t", ["add", "A"])),
    op("unsign", "s", use("t", ["add", "AA"])),
    op("unsign", "s", use("t", ["ins", -3, "="])),
    op("unsign", "s", use("t", ["ins", -5, "="])),
    op("unsign", "s", use("t", ["ins", -5, " "])),
    op("unsign", "s", use("t", ["ins", -10, "\n"])),
    op("unsign", "s", use("t", ["cut", 2])),
    op("unsign", "s", use("t", ["cut", 3])),
    op("unsign", "s", use("t", ["cut", 4])),
    op("unsign", "s", use("t", ["cut", 27])),
    op("unsign", "s", use("t", ["cut", 28])),
])

for kd in ["concat", "django-concat", "hmac", "none", "sha1-ish"]:
    for dg in ["sha1", "sha256", "sha512", "md5"]:
        job(f"derivation {kd} with {dg}", {
            "s": {"cls": "Signer", "key": "derive me " * (1 + len(dg) % 3 * 5),
                  "salt": "deriv", "key_derivation": kd, "digest_method": dg},
        }, [
            op("derive_key", "s"),
            op("sign", "s", {"value": "payload-" + kd}),
            op("unsign", "s", last()),
            op("unsign", "s", last(["flip", -2])),
        ])

job("salts and separators", {
    "a": {"cls": "Signer", "key": "k1", "salt": "activate"},
    "b": {"cls": "Signer", "key": "k1", "salt": "reset"},
    "n": {"cls": "Signer", "key": "k1", "salt": None},
    "d": {"cls": "Signer", "key": "k1"},
    "c": {"cls": "Signer", "key": "k1", "sep": ":"},
    "w": {"cls": "Signer", "key": "k1", "sep": "--"},
    "x": {"cls": "Signer", "key": "k1", "sep": "ab"},
    "y": {"cls": "Signer", "key": "k1", "sep": "az"},
    "z": {"cls": "Signer", "key": "k1", "sep": ""},
    "u": {"cls": "Signer", "key": "k1", "sep": "\u00a7"},
    "m": {"cls": "Signer", "key": "k1", "sep": "::"},
}, [
    op("sign", "a", {"value": "user:7"}),
    op("unsign", "b", last()),
    op("unsign", "a", last()),
    op("sign", "n", {"value": "user:7"}),
    op("unsign", "d", last()),
    op("sign", "c", {"value": "user:7"}),
    op("unsign", "c", last()),
    op("unsign", "d", last()),
    op("sign", "w", {"value": "x"}),
    op("sign", "x", {"value": "x"}),
    op("sign", "y", {"value": "lazy"}),
    op("unsign", "y", last()),
    op("sign", "y", {"value": "q"}),
    op("unsign", "y", last()),
    op("sign", "z", {"value": "x"}),
    op("sign", "u", {"value": "s\u00a7t"}),
    op("unsign", "u", last()),
    op("sign", "m", {"value": "a::b"}),
    op("unsign", "m", last()),
    op("unsign", "m", last(["repl", "::", ":"])),
])

job("key rotation", {
    "old": {"cls": "Signer", "key": "first key"},
    "both": {"cls": "Signer", "key": ["first key", "second key"]},
    "new": {"cls": "Signer", "key": ["second key"]},
    "none": {"cls": "Signer", "key": []},
}, [
    op("sign", "old", {"value": "ticket-1"}, save="t1"),
    op("sign", "both", {"value": "ticket-2"}, save="t2"),
    op("unsign", "both", use("t1")),
    op("unsign", "both", use("t2")),
    op("unsign", "new", use("t1")),
    op("unsign", "new", use("t2")),
    op("unsign", "old", use("t2")),
    op("sign", "none", {"value": "x"}),
    op("unsign", "none", use("t1")),
    op("derive_key", "none"),
])

job("no algorithm", {
    "s": {"cls": "Signer", "key": "k", "algorithm": "none"},
    "h": {"cls": "Signer", "key": "k"},
}, [
    op("sign", "s", {"value": "open"}),
    op("unsign", "s", last()),
    op("unsign", "s", {"value": "anything."}),
    op("unsign", "s", {"value": "anything.AA"}),
    op("unsign", "s", {"value": "anything.A"}),
    op("unsign", "s", {"value": "anything.===="}),
    op("unsign", "h", {"value": "open."}),
    op("get_signature", "s", {"value": "z"}),
])

# ------------------------------------------------------------ timestamps

job("timestamp signer", {
    "t": {"cls": "TimestampSigner", "key": "tick tock", "salt": "ts"},
}, [
    op("sign", "t", {"value": "session-9"}, save="a"),
    op("unsign", "t", use("a")),
    op("unsign", "t", use("a"), ts=True),
    op("unsign", "t", use("a"), max_age=60),
    op("unsign", "t", use("a"), max_age=60, now=1700000060),
    op("unsign", "t", use("a"), max_age=60, now=1700000061),
    op("validate", "t", use("a"), max_age=60),
    op("unsign", "t", use("a"), max_age=0, now=1699999999),
    op("validate", "t", use("a")),
    op("unsign", "t", use("a"), max_age=60, ts=True, now=1700000030),
    op("unsign", "t", use("a", ["flip", -1]), max_age=60),
    op("unsign", "t", use("a", ["flip", -30])),
    op("unsign", "t", use("a", ["flip", -30]), max_age=5),
    op("unsign", "t", {"value": "plain"}),
    op("unsign", "t", {"value": "plain.sig"}),
    op("unsign", "t", {"value": "a.b.c"}),
    op("sign", "t", {"value": "zero"}, now=0),
    op("unsign", "t", last(), ts=True),
    op("unsign", "t", last(), max_age=10, now=10),
    op("unsign", "t", last(), max_age=10, now=11),
    op("sign", "t", {"value": "past"}, now=-1),
    op("sign", "t", {"value": "far"}, now=2 ** 40),
    op("unsign", "t", last()),
    op("unsign", "t", last(), ts=True),
    op("unsign", "t", last(), max_age=5, now=1),
    op("unsign", "t", last(["flip", -1]), now=1),
    op("sign", "t", {"value": "y9999"}, now=253402300799),
    op("unsign", "t", last(), ts=True),
    op("sign", "t", {"value": "y10000"}, now=253402300800),
    op("unsign", "t", last(), ts=True),
    op("unsign", "t", last(["flip", -1]), now=1),
    op("sign", "t", {"value": "wrap"}, now=67768036191676799),
    op("unsign", "t", last(), ts=True),
    op("sign", "t", {"value": "eov"}, now=67768036191676800),
    op("unsign", "t", last(), ts=True),
    op("unsign", "t", last(["flip", -1])),
    op("sign", "t", {"value": "max"}, now=2 ** 63 - 1),
    op("unsign", "t", last(), ts=True),
    op("sign", "t", {"value": "big"}, now=2 ** 63),
    op("unsign", "t", last(), ts=True),
    op("unsign", "t", last(), max_age=1),
    op("unsign", "t", last(["flip", -1])),
    op("sign", "t", {"value": "top"}, now=2 ** 64 - 1),
    op("unsign", "t", last(), ts=True),
    op("sign", "t", {"value": "over"}, now=2 ** 64),
    op("validate", "t", {"value": "x.AAAAAAAAAAAA.sig"}),
    op("unsign", "t", {"value": "x.AAAAAAAAAAAA.sig"}),
    op("unsign", "t", {"value": "x.!!!.sig"}),
    op("unsign", "t", {"value": "x.A.sig"}),
    op("unsign", "t", {"value": "x..sig"}),
    op("unsign", "t", {"value": "x.AAAAAAAAAAAA.sig"}, now=5),
], now=1700000000)

job("timestamp edges", {
    "t": {"cls": "TimestampSigner", "key": "edge", "sep": "|"},
    "p": {"cls": "Signer", "key": "edge", "sep": "|"},
}, [
    op("sign", "p", {"value": "nostamp"}),
    op("unsign", "t", last()),
    op("sign", "p", {"value": "v|AAAAAAAAAAAA"}),
    op("unsign", "t", last()),
    op("unsign", "t", last(), ts=True),
    op("sign", "p", {"value": "v|_____w"}),
    op("unsign", "t", last(), ts=True),
    op("sign", "p", {"value": "v|AQIDBAUGBwgJ"}),
    op("unsign", "t", last()),
    op("sign", "p", {"value": "v|"}),
    op("unsign", "t", last(), ts=True),
    op("sign", "p", {"value": "v|A"}),
    op("unsign", "t", last()),
    op("sign", "p", {"value": "v|AAAAAAABAAAA"}),
    op("unsign", "t", last(), ts=True),
    op("sign", "t", {"value": "a|b"}),
    op("unsign", "t", last(), ts=True),
    op("unsign", "p", last()),
])

# ------------------------------------------------------------ serializers

USER = {"id": 42, "email": "ada@example.org", "roles": ["admin", "ops"], "active": True}
UNI = {"name": "Zo\u00eb \u00c5ngstr\u00f6m", "city": "\u6771\u4eac", "mood": "\U0001f642",
       "q": "say \"hi\"\\", "ctl": "a\tb\nc\u0001\u007f"}

job("json serializer", {
    "s": {"cls": "Serializer", "key": "serial key"},
    "o": {"cls": "Serializer", "key": "serial key", "salt": "other"},
    "n": {"cls": "Serializer", "key": "serial key", "salt": None},
    "sg": {"cls": "Signer", "key": "serial key", "salt": "itsdangerous"},
}, [
    op("dumps", "s", obj=USER),
    op("loads", "s", last()),
    op("loads", "o", last()),
    op("loads_unsafe", "o", last()),
    op("loads", "s", last(), salt="other"),
    op("dumps", "s", obj=USER, salt="other"),
    op("loads", "o", last()),
    op("dumps", "s", obj=UNI),
    op("loads", "s", last()),
    op("dumps", "s", obj=[1, -2, 0, None, False, "", [], {}, [[{"a": []}]]]),
    op("loads", "s", last()),
    op("dumps", "s", obj="just a string"),
    op("loads", "s", last()),
    op("dumps", "s", obj=9007199254740993),
    op("loads", "s", last()),
    op("dumps", "n", obj={"k": 1}),
    op("loads", "n", last()),
    op("loads", "s", last()),
    op("loads_unsafe", "s", last(["flip", -1])),
    op("loads_unsafe", "s", {"value": "nothing"}),
    op("loads_unsafe", "s", {"value": "{\"a\": 1}.bad"}),
    op("loads_unsafe", "s", {"value": "{\"a\": 1.bad"}),
    op("loads", "s", {"value": "{\"a\": 1}.bad"}),
    op("sign", "sg", {"value": "{\"a\": 1, \"a\": 2, \"b\": [true , null] }"}),
    op("loads", "s", last()),
    op("sign", "sg", {"value": " \t\n[\"\\ud83d\\ude00\", \"\\udc80\", \"\\u00E9\\/\"]\r\n"}),
    op("loads", "s", last()),
    op("sign", "sg", {"value": "[1,]"}),
    op("loads", "s", last()),
    op("loads_unsafe", "s", last()),
    op("sign", "sg", {"value": "\"tab\there\""}),
    op("loads", "s", last()),
    op("sign", "sg", {"value": "01"}),
    op("loads", "s", last()),
    op("sign", "sg", {"value": "-0"}),
    op("loads", "s", last()),
    op("sign", "sg", {"hex": "22c328"}),
    op("loads", "s", last()),
    op("loads_unsafe", "s", last(["flip", -1])),
    op("sign", "sg", {"value": "\ufeff{}"}),
    op("loads", "s", last()),
    op("sign", "sg", {"value": "{\"x\": \"\\q\"}"}),
    op("loads", "s", last()),
    op("sign", "sg", {"value": "[\"\\ud83d\", \"\\ude00\\ud83d\"]"}),
    op("loads", "s", last()),
    op("sign", "sg", {"value": "{\"a\":{\"b\":{\"c\":[-12345678901234,\"\u00e9\"]}}}"}),
    op("loads", "s", last()),
    op("sign", "sg", {"value": "truex"}),
    op("loads", "s", last()),
    op("sign", "sg", {"value": "{1: 2}"}),
    op("loads", "s", last()),
    op("sign", "sg", {"value": ""}),
    op("loads", "s", last()),
])

job("timed serializer", {
    "s": {"cls": "TimedSerializer", "key": "timed key", "salt": "t"},
}, [
    op("dumps", "s", obj={"cart": [3, 5, 8]}, save="a"),
    op("loads", "s", use("a")),
    op("loads", "s", use("a"), max_age=100, now=1700000100),
    op("loads", "s", use("a"), max_age=100, now=1700000101),
    op("loads", "s", use("a"), max_age=100, now=1699999000),
    op("loads", "s", use("a"), ts=True),
    op("loads", "s", use("a"), salt="u"),
    op("loads_unsafe", "s", use("a"), salt="u"),
    op("loads_unsafe", "s", use("a"), max_age=1, now=1800000000),
    op("loads_unsafe", "s", use("a", ["flip", -1])),
    op("loads_unsafe", "s", use("a", ["flip", -1]), max_age=1, now=1800000000),
    op("loads_unsafe", "s", {"value": "{}"}),
    op("loads_unsafe", "s", {"value": "{}.sig"}),
    op("loads", "s", {"value": "{}.sig"}),
    op("dumps", "s", obj=[], now=2 ** 40),
    op("loads", "s", last()),
    op("loads_unsafe", "s", last()),
    op("loads", "s", last(["flip", -1])),
    op("dumps", "s", obj=[], now=2 ** 63),
    op("loads", "s", last()),
    op("loads", "s", last(), max_age=10),
])

def b64(b):
    return base64.urlsafe_b64encode(b).rstrip(b"=").decode()


def zvariants():
    # Compressed payloads the way URLSafeSerializer would write them, and
    # broken copies of them.
    out = []
    body = json.dumps({"user": "ada", "roles": ["admin"] * 4}, separators=(",", ":")).encode()
    z = zlib.compress(body)
    stored = zlib.compress(body, 0)
    fixed = zlib.compressobj(9, zlib.DEFLATED, 15, 9, zlib.Z_FIXED)
    fixed = fixed.compress(body) + fixed.flush()
    for v in [z, stored, fixed, zlib.compress(body, 1), zlib.compress(body, 9),
              z[:-1], z[:-4], z[:2], z[:-4] + bytes(4), z + b"junk", z[:1],
              bytes([0x78, 0x9d]) + z[2:], bytes([0x88, 0x9c]) + z[2:],
              bytes([0x78, 0xbb]) + z[2:], bytes([0x79, 0x9c - 0x1f + 0x18]) + z[2:],
              z[:2] + bytes([z[2] | 6]) + z[3:], stored[:3] + bytes([stored[3] ^ 1]) + stored[4:],
              zlib.compress(b"\xff\xfe"), zlib.compress(b"[1,2,3"), zlib.compress(b""),
              zlib.compress(body * 40)]:
        out.append(op("sign", "sg", {"value": "." + b64(v)}))
        out.append(op("loads", "s", last()))
    return out


zops = zvariants()

SESSION = {"_fresh": True, "_id": "f" * 40, "user_id": "1234", "csrf_token": "c" * 40,
           "cart": [{"sku": "apple", "qty": 2}, {"sku": "pear", "qty": 1},
                    {"sku": "apple", "qty": 2}], "flash": []}

job("url-safe serializer", {
    "s": {"cls": "URLSafeSerializer", "key": "url key", "salt": "unsubscribe"},
    "sg": {"cls": "Signer", "key": "url key", "salt": "unsubscribe"},
}, [
    op("dumps", "s", obj={"list": "news", "user": 7}),
    op("loads", "s", last()),
    op("dumps", "s", obj=SESSION),
    op("loads", "s", last()),
    op("loads_unsafe", "s", last(["flip", -1])),
    op("loads_unsafe", "s", last(["flip", 5])),
    op("loads_unsafe", "s", last(["cut", 40])),
    op("dumps", "s", obj=UNI),
    op("loads", "s", last()),
    op("dumps", "s", obj="a" * 30),
    op("loads", "s", last()),
    op("dumps", "s", obj="ab" * 7),
    op("dumps", "s", obj="abc" * 6),
    op("dumps", "s", obj=[0] * 5),
    op("dumps", "s", obj=[0] * 6),
    op("dumps", "s", obj=[0] * 7),
    op("dumps", "s", obj=[]),
    op("loads", "s", last()),
    op("sign", "sg", {"value": "!!!"}),
    op("loads", "s", last()),
    op("sign", "sg", {"value": ".!!!"}),
    op("loads", "s", last()),
] + zops + [
    op("sign", "sg", {"value": "eyJhIjoxfQ"}),
    op("loads", "s", last()),
    op("sign", "sg", {"value": "eyJhIjoxfQ=="}),
    op("loads", "s", last()),
    op("sign", "sg", {"value": "e-yJh_Ijo+xf/Q"}),
    op("loads", "s", last()),
    op("sign", "sg", {"value": "eyJhIjoxf"}),
    op("loads", "s", last()),
    op("sign", "sg", {"value": "eyJhIjox"}),
    op("loads", "s", last()),
    op("sign", "sg", {"value": "_w"}),
    op("loads", "s", last()),
])

job("password reset", {
    "s": {"cls": "URLSafeTimedSerializer", "key": "not-a-real-secret", "salt": "password-reset"},
    "e": {"cls": "URLSafeTimedSerializer", "key": "not-a-real-secret", "salt": "email-confirm"},
}, [
    op("dumps", "s", obj={"user": 42, "pw": "5f4dcc3b"}, save="r", now=1700000000),
    op("loads", "s", use("r"), max_age=3600, now=1700000600),
    op("loads", "s", use("r"), max_age=3600, now=1700003600),
    op("loads", "s", use("r"), max_age=3600, now=1700003601),
    op("loads", "s", use("r"), max_age=3600, ts=True, now=1700001000),
    op("loads", "e", use("r"), max_age=3600, now=1700000600),
    op("loads_unsafe", "e", use("r")),
    op("loads", "s", use("r"), max_age=3600, now=1600000000),
    op("loads_unsafe", "s", use("r"), max_age=3600, now=1800000000),
    op("dumps", "e", obj="ada@example.org", save="c"),
    op("loads", "e", use("c"), max_age=86400, ts=True, now=1700050000),
    op("dumps", "s", obj=SESSION, now=1700000123),
    op("loads", "s", last(), ts=True),
    op("loads_unsafe", "s", last(["flip", 3])),
])

job("flask session", {
    "s": {"cls": "URLSafeTimedSerializer", "key": "dev",
          "salt": "cookie-session",
          "signer_kwargs": {"key_derivation": "hmac", "digest_method": "sha1"}},
}, [
    op("dumps", "s", obj={}),
    op("loads", "s", last(), max_age=2678400),
    op("dumps", "s", obj=SESSION),
    op("loads", "s", last(), max_age=2678400, now=1702678400),
    op("loads", "s", last(), max_age=2678400, now=1702678401),
    op("dumps", "s", obj={"_flashes": [["message", "Saved."], ["error", "Saved?"]] * 3}),
    op("loads", "s", last()),
])

job("fallback signers", {
    "old": {"cls": "URLSafeSerializer", "key": ["k-2023", "k-2024"], "salt": "api",
            "signer_kwargs": {"digest_method": "sha1"}},
    "new": {"cls": "URLSafeSerializer", "key": ["k-2023", "k-2024"], "salt": "api",
            "signer_kwargs": {"digest_method": "sha256"},
            "fallback": [{"kwargs": {"digest_method": "sha1"}}]},
    "tup": {"cls": "URLSafeSerializer", "key": ["k-2023", "k-2024"], "salt": "api",
            "signer_kwargs": {"digest_method": "sha512"},
            "fallback": [{"cls": "Signer", "kwargs": {"key_derivation": "concat"}},
                         {"cls": "Signer"},
                         {"kwargs": {"digest_method": "sha1"}}]},
    "only": {"cls": "URLSafeSerializer", "key": ["k-2023"], "salt": "api",
             "signer_kwargs": {"digest_method": "sha1"}},
    "t": {"cls": "URLSafeTimedSerializer", "key": ["k-2023", "k-2024"], "salt": "api",
          "signer_kwargs": {"digest_method": "sha256"},
          "fallback": [{"kwargs": {"digest_method": "sha1"}}]},
    "tsg": {"cls": "TimestampSigner", "key": "k-2023", "salt": "api"},
}, [
    op("dumps", "old", obj={"scope": "read"}, save="o"),
    op("dumps", "only", obj={"scope": "write"}, save="w"),
    op("loads", "new", use("o")),
    op("loads", "new", use("w")),
    op("loads", "tup", use("o")),
    op("loads", "tup", use("w")),
    op("dumps", "new", obj={"scope": "admin"}),
    op("loads", "old", last()),
    op("loads", "tup", last()),
    op("loads", "new", last()),
    op("loads", "new", use("o", ["flip", -1])),
    op("loads_unsafe", "tup", use("o", ["flip", -1])),
    op("sign", "tsg", {"value": "eyJ4IjoxfQ"}, save="ts", now=1700000500),
    op("loads", "t", use("ts"), max_age=100, now=1700000550),
    op("loads", "t", use("ts"), max_age=10, now=1700000550),
    op("loads", "t", use("ts", ["flip", -1]), max_age=10, now=1700000550),
    op("loads_unsafe", "t", use("ts"), max_age=10, now=1700000550),
])

job("constructor errors", {
    "bad": {"cls": "Signer", "key": "k", "sep": "a"},
    "eq": {"cls": "Signer", "key": "k", "sep": "="},
    "kd": {"cls": "Signer", "key": "k", "key_derivation": "pbkdf2"},
    "ser": {"cls": "Serializer", "key": "k", "signer_kwargs": {"sep": "-"}},
    "ok": {"cls": "Serializer", "key": "k", "signer_kwargs": {"sep": "~"}},
    "kds": {"cls": "TimedSerializer", "key": "k", "signer_kwargs": {"key_derivation": "pbkdf2"}},
}, [
    op("sign", "bad", {"value": "x"}),
    op("sign", "eq", {"value": "x"}),
    op("sign", "kd", {"value": "x"}),
    op("unsign", "kd", {"value": "x.abc"}),
    op("unsign", "kd", {"value": "x.a"}),
    op("validate", "kd", {"value": "x.abc"}),
    op("dumps", "ser", obj=1),
    op("loads", "ser", {"value": "1-abc"}),
    op("dumps", "ok", obj=[1, 2]),
    op("loads", "ok", last()),
    op("dumps", "kds", obj=1),
    op("loads", "kds", {"value": "1.AAAA.abc"}),
])

# ------------------------------------------------------------ at random

rng = random.Random(20261019)
WORDS = ["ada", "grace", "linus", "ken", "edsger", "barbara", "admin", "viewer", "cart",
         "\u00e9t\u00e9", "\u65e5\u672c", "\U0001f680", "a\"b", "x\\y", "tab\t", "nl\n"]


def rand_obj(depth=0):
    k = rng.random()
    if depth > 2 or k < 0.35:
        c = rng.randrange(6)
        if c == 0:
            return rng.randint(-10 ** 12, 10 ** 12)
        if c == 1:
            return rng.choice([True, False, None])
        if c == 2:
            return rng.randint(0, 99)
        return " ".join(rng.choice(WORDS) for _ in range(rng.randint(0, 4)))
    if k < 0.65:
        return [rand_obj(depth + 1) for _ in range(rng.randint(0, 6))]
    d = {}
    for _ in range(rng.randint(0, 7)):
        d[rng.choice(WORDS[:9]) + rng.choice(["", "_id", "s", "2"])] = rand_obj(depth + 1)
    return d


def rand_mut(tok_len):
    kind = rng.choice(["flip", "flip", "cut", "add", "ins", "repl"])
    if kind == "flip":
        return ["flip", rng.randint(-tok_len, tok_len - 1)]
    if kind == "cut":
        return ["cut", rng.randint(1, 6)]
    if kind == "add":
        return ["add", rng.choice(["A", "=", ".", "x", "AA", "_-", "\u00e9"])]
    if kind == "ins":
        return ["ins", rng.randint(-tok_len, tok_len - 1), rng.choice(["=", ".", "A", "-"])]
    return ["repl", rng.choice([".", "A", "e", "-", "_"]), rng.choice(["", ".", "B", "+", "/"])]


CLASSES = ["Serializer", "TimedSerializer", "URLSafeSerializer", "URLSafeTimedSerializer"]
for n in range(24):
    cls = CLASSES[n % 4]
    keys = [f"rk{n}-{i}" for i in range(rng.randint(1, 3))]
    cfg = {"cls": cls, "key": keys if len(keys) > 1 else keys[0], "salt": rng.choice(["r", "app", None])}
    sk = {}
    if rng.random() < 0.5:
        sk["key_derivation"] = rng.choice(["concat", "django-concat", "hmac", "none"])
    if rng.random() < 0.5:
        sk["digest_method"] = rng.choice(["sha1", "sha256", "sha512", "md5"])
    if rng.random() < 0.3:
        sk["sep"] = rng.choice([":", "|", "~", "!"])
    if sk:
        cfg["signer_kwargs"] = sk
    if rng.random() < 0.3:
        cfg["fallback"] = [{"kwargs": {"digest_method": rng.choice(["sha1", "md5"])}}]
    ops = []
    now = 1700000000 + rng.randint(0, 10 ** 6)
    for i in range(rng.randint(5, 9)):
        ops.append(op("dumps", "s", obj=rand_obj(), now=now))
        est = 60
        timed = "Timed" in cls
        for _ in range(rng.randint(1, 4)):
            src = last() if rng.random() < 0.4 else last(*[rand_mut(est) for _ in range(rng.randint(1, 2))])
            name = rng.choice(["loads", "loads_unsafe"])
            kw = {}
            if timed and rng.random() < 0.6:
                kw["max_age"] = rng.choice([0, 30, 600])
                kw["now"] = now + rng.choice([-5, 0, 10, 30, 31, 700])
            if timed and rng.random() < 0.3 and name == "loads":
                kw["ts"] = True
            ops.append(op(name, "s", src, **kw))
    job(f"random {n} {cls}", {"s": cfg}, ops, now=now)

with open("data/jobs.jsonl", "w") as f:
    for j in jobs:
        f.write(json.dumps(j, ensure_ascii=False) + "\n")
