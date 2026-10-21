# Writes data/: the jobs mini_pyjwt runs (data/jobs.jsonl) and the files
# its two programs read: an API gateway's JWK sets, routes and access log,
# and a token issuer's secret and user list. Tokens with odd headers or
# payloads are signed here with the standard library's hmac, so that
# PyJWT gets past the signature and reaches the check being exercised.
import base64
import hashlib
import hmac
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
os.makedirs(DATA, exist_ok=True)

T0 = 1761048000  # 2025-10-21 12:00:00 UTC
SECRET = "kara-demo-secret"
jobs = []


def job(name, ops):
    jobs.append({"name": name, "ops": ops})


def b64(b):
    return base64.urlsafe_b64encode(b).rstrip(b"=").decode()


def raw(header, payload, key=SECRET, digest="sha256"):
    h = header if isinstance(header, bytes) else header.encode()
    p = payload if isinstance(payload, bytes) else payload.encode()
    k = key if isinstance(key, bytes) else key.encode()
    si = b64(h) + "." + b64(p)
    sig = hmac.new(k, si.encode(), getattr(hashlib, digest)).digest()
    return si + "." + b64(sig)


HS = '{"alg":"HS256","typ":"JWT"}'


def claims(payload, **kw):
    op = {"op": "decode", "token": raw(HS, payload), "key": SECRET, "algorithms": ["HS256"], "now": T0}
    op.update(kw)
    return op


def write(rel, text):
    path = os.path.join(DATA, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)


# ------------------------------------------------------------ encoding

job("encode with each HMAC algorithm", [
    {"op": "encode", "payload": {"sub": "alice", "admin": True}, "key": SECRET},
    {"op": "encode", "payload": {"sub": "alice", "admin": True}, "key": SECRET, "algorithm": "HS384"},
    {"op": "encode", "payload": {"sub": "alice", "admin": True}, "key": SECRET, "algorithm": "HS512"},
    {"op": "encode", "payload": {}, "key": SECRET},
    {"op": "encode", "payload": {"sub": "bob"}, "key": ""},
    {"op": "encode", "payload": {"sub": "bob"}, "key": "k" * 64},
    {"op": "encode", "payload": {"sub": "bob"}, "key": "k" * 65},
    {"op": "encode", "payload": {"sub": "bob"}, "key": "x" * 200, "algorithm": "HS512"},
    {"op": "encode", "payload": {"sub": "bob"}, "key": "x" * 129, "algorithm": "HS384"},
    {"op": "encode", "payload": {"sub": "bob"}, "key": {"$bytes": "00ff10e2809c"}},
    {"op": "encode", "payload": {"sub": "bob"}, "key": "clé-secrète-日本"},
    {"op": "encode", "payload": {"sub": "bob"}, "key": SECRET, "algorithm": None},
    {"op": "decode", "token": {"ref": 0}, "key": SECRET, "algorithms": ["HS256"]},
    {"op": "decode", "token": {"ref": 1}, "key": SECRET, "algorithms": ["HS384"]},
    {"op": "decode", "token": {"ref": 2}, "key": SECRET, "algorithms": ["HS512"], "complete": True},
    {"op": "decode", "token": {"ref": 4}, "key": "", "algorithms": ["HS256"]},
    {"op": "decode", "token": {"ref": 9}, "key": {"$bytes": "00ff10e2809c"}, "algorithms": ["HS256"]},
    {"op": "decode", "token": {"ref": 10}, "key": "clé-secrète-日本", "algorithms": ["HS256"]},
])

job("payload values", [
    {"op": "encode", "payload": {"name": "Zoë", "city": "東京", "emoji": "🙂", "tab": "a\tb", "nl": "x\ny",
                                 "quote": "say \"hi\"", "apos": "it's", "both": "'\"", "slash": "a/b\\c",
                                 "ctl": "\u0001\u001f\u007f\u0085", "nbsp": "a\u00a0b", "zw": "\u200b"}, "key": SECRET},
    {"op": "encode", "payload": {"i": 0, "neg": -7, "big": 123456789012345678901234567890, "f": 1.5, "g": 0.1,
                                 "e": 1e16, "small": 1e-7, "neg0": -0.0, "third": 1 / 3, "whole": 3.0,
                                 "nan": float("nan"), "inf": float("inf"), "ninf": float("-inf")}, "key": SECRET},
    {"op": "encode", "payload": {"t": True, "f": False, "n": None, "list": [1, "two", [3, {"four": 4}], []],
                                 "obj": {"nested": {"deep": {}}}, "": "empty key"}, "key": SECRET},
    {"op": "encode", "payload": {"b": 2, "a": 1, "c": {"z": 1, "y": 2}}, "key": SECRET},
    {"op": "decode", "token": {"ref": 0}, "key": SECRET, "algorithms": ["HS256"]},
    {"op": "decode", "token": {"ref": 1}, "key": SECRET, "algorithms": ["HS256"]},
    {"op": "decode", "token": {"ref": 2}, "key": SECRET, "algorithms": ["HS256"]},
    {"op": "decode", "token": {"ref": 3}, "key": SECRET, "algorithms": ["HS256"], "complete": True},
    {"op": "encode", "payload": [1, 2], "key": SECRET},
    {"op": "encode", "payload": "sub", "key": SECRET},
    {"op": "encode", "payload": None, "key": SECRET},
])

job("datetime claims", [
    {"op": "encode", "payload": {"exp": {"$naive": [2025, 10, 21, 13, 0, 0, 0]}}, "key": SECRET},
    {"op": "encode", "payload": {"iat": {"$dt": [2025, 10, 21, 12, 0, 0, 999999, 0]},
                                 "nbf": {"$dt": [2025, 10, 21, 14, 0, 0, 0, 120]},
                                 "exp": {"$dt": [2025, 10, 21, 8, 30, 0, 0, -330]}}, "key": SECRET},
    {"op": "encode", "payload": {"exp": {"$naive": [1969, 12, 31, 23, 59, 59, 0]}, "iat": {"$naive": [2000, 2, 29, 0, 0, 0, 0]}},
     "key": SECRET},
    {"op": "encode", "payload": {"exp": {"$naive": [2100, 3, 1, 0, 0, 0, 0]}, "when": "not converted"}, "key": SECRET},
    {"op": "decode", "token": {"ref": 0}, "key": SECRET, "algorithms": ["HS256"], "now": T0},
    {"op": "decode", "token": {"ref": 1}, "key": SECRET, "algorithms": ["HS256"], "now": T0},
    {"op": "decode", "token": {"ref": 1}, "key": SECRET, "algorithms": ["HS256"], "now": T0 + 7200},
    {"op": "decode", "token": {"ref": 2}, "key": SECRET, "algorithms": ["HS256"],
     "options": {"verify_exp": False}},
    {"op": "decode", "token": {"ref": 3}, "key": SECRET, "algorithms": ["HS256"]},
])

job("headers", [
    {"op": "encode", "payload": {"sub": "h"}, "key": SECRET, "headers": {"kid": "2025-10"}},
    {"op": "encode", "payload": {"sub": "h"}, "key": SECRET, "headers": {"kid": "k1", "zeta": 1, "cty": "JWT"},
     "sort_headers": False},
    {"op": "encode", "payload": {"sub": "h"}, "key": SECRET, "headers": {"typ": None}},
    {"op": "encode", "payload": {"sub": "h"}, "key": SECRET, "headers": {"typ": ""}},
    {"op": "encode", "payload": {"sub": "h"}, "key": SECRET, "headers": {"typ": "at+jwt"}},
    {"op": "encode", "payload": {"sub": "h"}, "key": SECRET, "headers": {"alg": "HS512"}},
    {"op": "encode", "payload": {"sub": "h"}, "key": SECRET, "algorithm": "HS384", "headers": {"alg": ""}},
    {"op": "encode", "payload": {"sub": "h"}, "key": SECRET, "headers": {"b64": True}},
    {"op": "encode", "payload": {"sub": "h"}, "key": SECRET, "headers": {"b64": 0}},
    {"op": "encode", "payload": {"sub": "h"}, "key": SECRET, "headers": {"x5u": "https://example.com/k", "jku": "é"}},
    {"op": "encode", "payload": {"sub": "h"}, "key": SECRET, "headers": {"kid": 7}},
    {"op": "encode", "payload": {"sub": "h"}, "key": SECRET, "headers": {"kid": None}},
    {"op": "encode", "payload": {"sub": "h"}, "key": SECRET, "headers": {"alg": 5}},
    {"op": "encode", "payload": {"sub": "h"}, "key": SECRET, "headers": {}},
    {"op": "header", "token": {"ref": 0}},
    {"op": "header", "token": {"ref": 1}},
    {"op": "header", "token": {"ref": 2}},
    {"op": "header", "token": {"ref": 5}},
    {"op": "decode", "token": {"ref": 5}, "key": SECRET, "algorithms": ["HS512"]},
    {"op": "decode", "token": {"ref": 6}, "key": SECRET, "algorithms": ["HS384"]},
    {"op": "decode", "token": {"ref": 7}, "key": SECRET, "algorithms": ["HS256"], "complete": True},
])

job("algorithm choice", [
    {"op": "encode", "payload": {"sub": "a"}, "key": SECRET, "algorithm": "RS256"},
    {"op": "encode", "payload": {"sub": "a"}, "key": SECRET, "algorithm": "ES256K"},
    {"op": "encode", "payload": {"sub": "a"}, "key": SECRET, "algorithm": "EdDSA"},
    {"op": "encode", "payload": {"sub": "a"}, "key": SECRET, "algorithm": "hs256"},
    {"op": "encode", "payload": {"sub": "a"}, "key": SECRET, "algorithm": "HS1"},
    {"op": "encode", "payload": {"sub": "a"}, "key": None, "algorithm": "none"},
    {"op": "encode", "payload": {"sub": "a"}, "key": "", "algorithm": "none"},
    {"op": "encode", "payload": {"sub": "a"}, "key": SECRET, "algorithm": "none"},
    {"op": "encode", "payload": {"sub": "a"}, "key": {"$bytes": ""}, "algorithm": "none"},
    {"op": "encode", "payload": {"sub": "a"}, "key": None},
    {"op": "encode", "payload": {"sub": "a"}, "key": 42},
    {"op": "encode", "payload": {"sub": "a"}, "key": ["k"]},
    {"op": "decode", "token": {"ref": 0}, "key": None, "algorithms": ["none"]},
    {"op": "decode", "token": {"ref": 0}, "algorithms": ["none"], "options": {"verify_signature": False}},
    {"op": "decode", "token": {"ref": 0}, "options": {"verify_signature": False}},
    {"op": "algorithms", "names": ["HS256", "none", "RS256", "PS512", "ES521", "HS1", "", 5, None]},
    {"op": "algorithms", "allowed": ["HS256", "HS512", "RS256", "nope"], "names": ["HS256", "HS384", "RS256", "nope"]},
    {"op": "jws_encode", "payload": "{}", "key": SECRET, "algorithm": "HS384", "allowed": ["HS256"]},
    {"op": "jws_encode", "payload": "{}", "key": SECRET, "allowed": ["HS256"]},
    {"op": "jws_decode", "token": {"ref": 1}, "key": SECRET, "algorithms": ["HS256"], "allowed": []},
])

# ------------------------------------------------------------ signatures

good = raw(HS, '{"sub":"carol"}')
job("signature checks", [
    {"op": "decode", "token": good, "key": SECRET, "algorithms": ["HS256"]},
    {"op": "decode", "token": good, "key": "other-secret", "algorithms": ["HS256"]},
    {"op": "decode", "token": good, "key": SECRET, "algorithms": ["HS384", "HS512"]},
    {"op": "decode", "token": good, "key": SECRET},
    {"op": "decode", "token": good, "key": SECRET, "algorithms": []},
    {"op": "decode", "token": good, "key": SECRET, "algorithms": "HS256"},
    {"op": "decode", "token": good, "key": SECRET, "algorithms": "xHS256x"},
    {"op": "decode", "token": good, "key": SECRET, "algorithms": ["HS256"], "options": {"verify_signature": False}},
    {"op": "decode", "token": good, "key": "wrong", "algorithms": ["HS256"], "options": {"verify_signature": 0}},
    {"op": "decode", "token": good, "key": "wrong", "algorithms": ["HS256"], "options": {"verify_signature": "no"}},
    {"op": "decode", "token": good[:-1], "key": SECRET, "algorithms": ["HS256"]},
    {"op": "decode", "token": good + "A", "key": SECRET, "algorithms": ["HS256"]},
    {"op": "decode", "token": good + "AA", "key": SECRET, "algorithms": ["HS256"]},
    {"op": "decode", "token": good.replace("-", "+").replace("_", "/"), "key": SECRET, "algorithms": ["HS256"]},
    {"op": "decode", "token": good[:-4] + "!" + good[-4:], "key": SECRET, "algorithms": ["HS256"]},
    {"op": "decode", "token": raw('{"alg":"HS384"}', '{"sub":"d"}', digest="sha384"), "key": SECRET,
     "algorithms": ["HS256", "HS384"]},
    {"op": "decode", "token": raw('{"alg":"HS384"}', '{"sub":"d"}', digest="sha384"), "key": SECRET,
     "algorithms": ["HS256"]},
    {"op": "decode", "token": raw('{"alg":"HS256"}', '{"sub":"d"}', digest="sha512"), "key": SECRET,
     "algorithms": ["HS256"]},
    {"op": "decode", "token": raw('{"typ":"JWT"}', '{"sub":"d"}'), "key": SECRET, "algorithms": ["HS256"]},
    {"op": "decode", "token": raw('{"alg":""}', '{"sub":"d"}'), "key": SECRET, "algorithms": ["HS256"]},
    {"op": "decode", "token": raw('{"alg":null}', '{"sub":"d"}'), "key": SECRET, "algorithms": ["HS256"]},
    {"op": "decode", "token": raw('{"alg":0}', '{"sub":"d"}'), "key": SECRET, "algorithms": [0]},
    {"op": "decode", "token": raw('{"alg":1}', '{"sub":"d"}'), "key": SECRET, "algorithms": [True]},
    {"op": "decode", "token": raw('{"alg":"XX256"}', '{"sub":"d"}'), "key": SECRET, "algorithms": ["XX256"]},
    {"op": "decode", "token": raw('{"alg":"RS256"}', '{"sub":"d"}'), "key": SECRET, "algorithms": ["RS256"]},
    {"op": "decode", "token": raw('{"alg":"none"}', '{"sub":"d"}'), "key": SECRET, "algorithms": ["none"]},
    {"op": "decode", "token": raw('{"alg":"HS256"}', '{"sub":"d"}', key=""), "key": "", "algorithms": ["HS256"]},
    {"op": "decode", "token": raw('{"alg":"HS256"}', '{"sub":"d"}', key=""), "algorithms": ["HS256"]},
    {"op": "decode", "token": good, "key": 99, "algorithms": ["HS256"]},
    {"op": "decode", "token": good, "key": "-----BEGIN PUBLIC KEY-----\nMFkw\n-----END PUBLIC KEY-----\n",
     "algorithms": ["HS256"]},
])

# ------------------------------------------------------------ token shape

job("malformed tokens", [
    {"op": "decode", "token": t, "key": SECRET, "algorithms": ["HS256"]} for t in [
        "", "abc", "a.b", "a.b.c", "..", "...", "a..", ".b.", "eyJ.eyJ.sig",
        b64(b'{"alg":"HS256"}') + ".." + "x",
        "!!!." + b64(b"{}") + ".",
        b64(b"[]") + "." + b64(b"{}") + ".",
        b64(b'"str"') + "." + b64(b"{}") + ".",
        b64(b"42") + "." + b64(b"{}") + ".",
        b64(b"null") + "." + b64(b"{}") + ".",
        "e" + "." + b64(b"{}") + ".",
        b64(b"{}") + "." + "e" + ".",
        b64(b"{}") + "." + b64(b"{}") + ".e",
        b64(b"{}") + ".e=e.",
        b64(b'{"alg":"HS256"}') + ".",
        b64(b'{"alg":"HS256"}') + " ." + b64(b"{}") + ".",
        b64(b'{"alg":"HS256"}') + "\n." + b64(b"{}") + ".",
        "  " + b64(b'{"alg":"HS256"}') + "." + b64(b"{}") + ".",
        "é." + b64(b"{}") + ".",
    ]
] + [
    {"op": "decode", "token": 5, "key": SECRET, "algorithms": ["HS256"]},
    {"op": "decode", "token": None, "key": SECRET, "algorithms": ["HS256"]},
    {"op": "decode", "token": {"$bytes": good.encode().hex()}, "key": SECRET, "algorithms": ["HS256"]},
])

BAD_JSON = [
    "", " ", "{", "}", "[", "{\"alg\"", "{\"alg\":", "{\"alg\":\"HS256\"", "{\"alg\":\"HS256\",}",
    "{\"alg\" \"HS256\"}", "{alg:\"HS256\"}", "{'alg':'HS256'}", "{\"alg\":\"HS\\x\"}", "{\"alg\":\"\\u12\"}",
    "{\"alg\":\"\\u12g4\"}", "{\"alg\":\"a\tb\"}", "{\"a\":1}{}", "{\"a\":1} x", "{\"a\":[1,]}", "{\"a\":[1 2]}",
    "{\"a\":[1,,2]}", "{\"a\":tru}", "{\"a\":nul}", "{\"a\":-}", "{\"a\":01}", "{\"a\":1.}", "{\"a\":.5}",
    "{\"a\":+1}", "{\"a\":1e}", "{\n  \"a\": 1,\n  \"b\": ?\n}", "\n\n  {\"a\":\n x}", "{\"a\":\"unterminated",
    "{\"a\":\"\\", "{\"a\":\"\\u00e9\\ud83d\\ude42\"}", "{\"a\":NaN,\"b\":-Infinity,\"c\":Infinity}",
    "{\"a\":1,\"a\":2,\"b\":3,\"a\":4}", " {\"a\" : [ 1 , { } , \"x\" ] } ", "{\"a\":1e400,\"b\":-1e400,\"c\":-0}",
    "{\"a\":123456789012345678901234567890,\"b\":-0.0,\"c\":1E2,\"d\":2.50}",
]
BAD_BYTES = [b"\xff", b"{\"a\":\"\xe9\"}", b"{\"a\":\"\xe2\x82\"}", b"{\"a\":\"\xf0\x9f\x98\"}", b"\xef\xbb\xbf{}",
             b"\xef\xbb\xbf\xff{}", b"{\"a\":\"\xc0\xaf\"}", b"{\"a\":\"\xf4\x90\x80\x80\"}",
             b"{\"a\":\"\xe2\x82\xac\"}", b"{\"a\":\"\x80\"}"]
job("header json", [
    {"op": "header", "token": b64(h.encode()) + "." + b64(b"{}") + "."} for h in BAD_JSON
] + [
    {"op": "header", "token": b64(h) + "." + b64(b"{}") + "."} for h in BAD_BYTES
])
job("payload json", [
    {"op": "decode", "token": raw(HS, p), "key": SECRET, "algorithms": ["HS256"]} for p in BAD_JSON + ["[1,2]", "\"x\"", "7"]
] + [
    {"op": "decode", "token": raw(HS, p), "key": SECRET, "algorithms": ["HS256"]} for p in BAD_BYTES
] + [
    {"op": "decode", "token": raw(HS, "not json"), "key": SECRET, "algorithms": ["HS256"], "complete": True,
     "options": {"verify_signature": False}},
])

# ------------------------------------------------------------ claims

job("expiry and not-before", [
    claims('{"exp":%d}' % (T0 + 1)),
    claims('{"exp":%d}' % T0),
    claims('{"exp":%d}' % (T0 - 1)),
    claims('{"exp":%d}' % (T0 - 30), leeway=30),
    claims('{"exp":%d}' % (T0 - 30), leeway=29.5),
    claims('{"exp":%d}' % (T0 - 30), leeway={"$td": 31}),
    claims('{"exp":%d.9}' % T0),
    claims('{"exp":%d.9}' % (T0 + 1)),
    claims('{"exp":"%d"}' % (T0 + 10)),
    claims('{"exp":" %d "}' % (T0 + 10)),
    claims('{"exp":"1_761_048_100"}'),
    claims('{"exp":"+%d"}' % (T0 + 10)),
    claims('{"exp":"%d.0"}' % (T0 + 10)),
    claims('{"exp":"soon"}'),
    claims('{"exp":""}'),
    claims('{"exp":null}'),
    claims('{"exp":[1]}'),
    claims('{"exp":{"at":1}}'),
    claims('{"exp":true}'),
    claims('{"exp":false}'),
    claims('{"exp":NaN}'),
    claims('{"exp":Infinity}'),
    claims('{"exp":-Infinity}'),
    claims('{"exp":1e300}'),
    claims('{"exp":99999999999999999999999}'),
    claims('{"exp":-99999999999999999999999}'),
    claims('{"exp":%d}' % (T0 - 1), options={"verify_exp": False}),
    claims('{"exp":"soon"}', options={"verify_exp": 0}),
    claims('{"nbf":%d}' % T0),
    claims('{"nbf":%d}' % (T0 + 1)),
    claims('{"nbf":%d}' % (T0 + 60), leeway=60),
    claims('{"nbf":%d}' % (T0 + 61), leeway=60),
    claims('{"nbf":"later"}'),
    claims('{"nbf":%d}' % (T0 + 1), options={"verify_nbf": False}),
    claims('{"nbf":%d,"exp":%d}' % (T0 + 10, T0 - 10)),
    claims('{"exp":%d,"nbf":%d}' % (T0 - 10, T0 + 10)),
    claims('{"exp":%d}' % (T0 + 1), now=T0 + 0.5),
    claims('{"exp":%d}' % (T0 + 1), now=T0 + 1.25),
    claims('{"exp":%d}' % (T0 + 1), leeway=-1),
])

job("issued at", [
    claims('{"iat":%d}' % T0),
    claims('{"iat":%d}' % (T0 + 1)),
    claims('{"iat":%d}' % (T0 + 5), leeway=5),
    claims('{"iat":"yesterday"}'),
    claims('{"iat":"%d"}' % (T0 - 100)),
    claims('{"iat":%d.75}' % T0),
    claims('{"iat":NaN}'),
    claims('{"iat":null}'),
    claims('{"iat":%d}' % (T0 + 1), options={"verify_iat": False}),
    claims('{"iat":%d,"nbf":%d,"exp":%d}' % (T0 + 9, T0 + 9, T0 - 9)),
])

job("audience", [
    claims('{"aud":"api"}', audience="api"),
    claims('{"aud":"api"}', audience="web"),
    claims('{"aud":"api"}'),
    claims('{"aud":""}'),
    claims('{"aud":[]}'),
    claims('{"aud":null}'),
    claims('{"aud":0}'),
    claims('{"aud":["web","api"]}', audience="api"),
    claims('{"aud":["web","api"]}', audience=["mobile", "api"]),
    claims('{"aud":["web","api"]}', audience=["mobile"]),
    claims('{"aud":["web","api"]}', audience=[]),
    claims('{"aud":["web",7]}', audience="web"),
    claims('{"aud":{"web":1}}', audience="web"),
    claims('{"aud":7}', audience="7"),
    claims('{"aud":"apiv2"}', audience="api"),
    claims('{"sub":"x"}', audience="api"),
    claims('{"aud":""}', audience="api"),
    claims('{"aud":"api"}', audience=7),
    claims('{"aud":"api"}', audience=None),
    claims('{"aud":"api"}', audience={"api": True}),
    claims('{"aud":"api"}', audience="api", options={"strict_aud": True}),
    claims('{"aud":"api"}', audience="web", options={"strict_aud": True}),
    claims('{"aud":["api"]}', audience="api", options={"strict_aud": True}),
    claims('{"aud":"api"}', audience=["api"], options={"strict_aud": True}),
    claims('{"aud":"api"}', audience="web", options={"verify_aud": False}),
    claims('{"aud":"api"}', audience="web", options={"verify_signature": False}),
    claims('{"aud":"api"}', audience="web", options={"verify_signature": False, "verify_aud": True}),
])

job("issuer, subject and id", [
    claims('{"iss":"https://auth.example.com"}', issuer="https://auth.example.com"),
    claims('{"iss":"https://auth.example.com"}', issuer="https://auth.example.com/"),
    claims('{"iss":"https://auth.example.com"}', issuer=["https://a.example.com", "https://auth.example.com"]),
    claims('{"iss":"https://auth.example.com"}', issuer=["https://a.example.com"]),
    claims('{"iss":"https://auth.example.com"}', issuer=[]),
    claims('{"sub":"x"}', issuer="https://auth.example.com"),
    claims('{"iss":1}', issuer=[1.0]),
    claims('{"iss":true}', issuer=[1]),
    claims('{"iss":["a"]}', issuer=[["a"]]),
    claims('{"iss":null}', issuer="x"),
    claims('{"iss":"anyone"}'),
    claims('{"sub":"u-1"}', subject="u-1"),
    claims('{"sub":"u-1"}', subject="u-2"),
    claims('{"sub":42}'),
    claims('{"sub":null}', subject="u-1"),
    claims('{"jti":"0f8e"}', subject="u-1"),
    claims('{"jti":17}'),
    claims('{"jti":null}'),
    claims('{"sub":42,"jti":17}', options={"verify_sub": False}),
    claims('{"sub":42,"jti":17}', options={"verify_sub": False, "verify_jti": False}),
])

job("required claims", [
    claims('{"exp":%d,"sub":"a"}' % (T0 + 9), options={"require": ["exp", "sub"]}),
    claims('{"sub":"a"}', options={"require": ["exp", "sub"]}),
    claims('{"exp":null,"sub":"a"}', options={"require": ["exp"]}),
    claims('{"exp":%d}' % (T0 + 9), options={"require": ["exp", "iat", "nbf"]}),
    claims('{"exp":%d}' % (T0 + 9), options={"require": "exp"}),
    claims('{"e":1,"x":2,"p":3}', options={"require": "exp"}),
    claims('{"sub":"a"}', options={"require": []}),
    claims('{"sub":"a"}', options={"require": ["sub", "sub"]}),
])

job("decoder options", [
    claims('{"exp":%d}' % (T0 - 1), instance={"verify_exp": False}),
    claims('{"exp":%d}' % (T0 - 1), instance={"verify_exp": False}, options={"verify_exp": True}),
    claims('{"sub":"a"}', instance={"require": ["exp"]}),
    claims('{"sub":"a"}', instance={"require": ["exp"]}, options={"require": []}),
    {"op": "decode", "token": raw(HS, '{"exp":1}', key="nope"), "key": SECRET, "algorithms": ["HS256"],
     "instance": {"verify_signature": False}},
    {"op": "decode", "token": raw(HS, '{"exp":1}', key="nope"), "key": SECRET, "algorithms": ["HS256"],
     "options": {"verify_signature": False}},
    {"op": "decode", "token": raw(HS, '{"exp":1}', key="nope"), "key": SECRET, "algorithms": ["HS256"],
     "options": {"verify_signature": False, "verify_exp": True}},
    {"op": "decode", "token": raw(HS, '{"iat":"bad"}', key="nope"), "algorithms": ["HS256"],
     "options": {"verify_signature": False, "verify_iat": 1}},
    claims('{"exp":%d}' % (T0 - 1), options={"verify_exp": "", "unknown_option": True}),
])

# ------------------------------------------------------------ JWS

job("raw JWS payloads", [
    {"op": "jws_encode", "payload": "hello world", "key": SECRET},
    {"op": "jws_encode", "payload": "", "key": SECRET, "algorithm": "HS512"},
    {"op": "jws_encode", "payload": "{\"a\":1}", "key": SECRET, "headers": {"cty": "json"}},
    {"op": "jws_encode", "payload": "line1\nline2 ✓", "key": SECRET},
    {"op": "jws_decode", "token": {"ref": 0}, "key": SECRET, "algorithms": ["HS256"]},
    {"op": "jws_decode", "token": {"ref": 1}, "key": SECRET, "algorithms": ["HS512"]},
    {"op": "jws_decode", "token": {"ref": 3}, "key": SECRET, "algorithms": ["HS256"]},
    {"op": "decode", "token": {"ref": 0}, "key": SECRET, "algorithms": ["HS256"]},
    {"op": "decode", "token": {"ref": 2}, "key": SECRET, "algorithms": ["HS256"]},
    {"op": "jws_decode", "token": {"ref": 0, "seg": 1, "value": b64(b"hellO world")}, "key": SECRET, "algorithms": ["HS256"]},
    {"op": "jws_decode", "token": {"ref": 0, "seg": 1, "value": b64(b"hellO world")}, "key": SECRET, "algorithms": ["HS256"],
     "options": {"verify_signature": False}},
])

job("detached payloads", [
    {"op": "jws_encode", "payload": "{\"amount\":100}", "key": SECRET, "detached": True},
    {"op": "jws_encode", "payload": "{\"amount\":100}", "key": SECRET, "headers": {"b64": False, "crit": ["b64"]}},
    {"op": "encode", "payload": {"amount": 100}, "key": SECRET, "headers": {"b64": False}},
    {"op": "jws_decode", "token": {"ref": 0}, "key": SECRET, "algorithms": ["HS256"], "detached": "{\"amount\":100}"},
    {"op": "jws_decode", "token": {"ref": 0}, "key": SECRET, "algorithms": ["HS256"], "detached": "{\"amount\":999}"},
    {"op": "jws_decode", "token": {"ref": 0}, "key": SECRET, "algorithms": ["HS256"]},
    {"op": "jws_decode", "token": {"ref": 1}, "key": SECRET, "algorithms": ["HS256"], "detached": "{\"amount\":100}"},
    {"op": "decode", "token": {"ref": 2}, "key": SECRET, "algorithms": ["HS256"], "detached": "{\"amount\":100}"},
    {"op": "decode", "token": {"ref": 2}, "key": SECRET, "algorithms": ["HS256"], "detached": "[100]"},
    {"op": "jws_decode", "token": {"ref": 2, "seg": 1, "value": "ignored"}, "key": SECRET, "algorithms": ["HS256"],
     "detached": "{\"amount\":100}"},
    {"op": "jws_decode", "token": good, "key": SECRET, "algorithms": ["HS256"], "detached": "unused"},
    {"op": "header", "token": {"ref": 0}},
])

# ------------------------------------------------------------ JWK

K1 = b64(b"gateway-key-one-32-bytes-long!!!")
job("JWKs", [
    {"op": "jwk", "data": {"kty": "oct", "k": K1, "kid": "gw-1", "use": "sig"}},
    {"op": "jwk", "data": {"kty": "oct", "k": K1, "alg": "HS512"}},
    {"op": "jwk", "data": {"kty": "oct", "k": K1, "alg": "HS512"}, "algorithm": "HS384"},
    {"op": "jwk", "data": {"kty": "oct", "k": K1}, "algorithm": "HS999"},
    {"op": "jwk", "data": {"kty": "oct", "k": K1, "alg": "none"}},
    {"op": "jwk", "data": {"kty": "oct", "k": K1, "alg": ""}},
    {"op": "jwk", "data": {"kty": "oct"}},
    {"op": "jwk", "data": {"kty": "oct", "k": 12}},
    {"op": "jwk", "data": {"kty": "oct", "k": "a"}},
    {"op": "jwk", "data": {"kty": "oct", "k": ""}},
    {"op": "jwk", "data": {"kty": "oct", "k": "+/=="}},
    {"op": "jwk", "data": {"kty": "RSA", "n": "0vx7", "e": "AQAB"}},
    {"op": "jwk", "data": {"kty": "EC", "crv": "P-384"}},
    {"op": "jwk", "data": {"kty": "EC", "crv": "P-999"}},
    {"op": "jwk", "data": {"kty": "EC"}},
    {"op": "jwk", "data": {"kty": "OKP", "x": "11qY"}},
    {"op": "jwk", "data": {"kty": "OKP", "crv": "Ed448"}},
    {"op": "jwk", "data": {"kty": "OKP", "crv": "Ed25519"}},
    {"op": "jwk", "data": {"kty": "OCT", "k": K1}},
    {"op": "jwk", "data": {"kty": "", "k": K1}},
    {"op": "jwk", "data": {"k": K1, "note": "it's \"quoted\"", "n": None, "t": True, "f": 1.5}},
    {"op": "jwk", "data": {"kty": "RSA"}, "algorithm": "HS256"},
    {"op": "jwk", "data": "{\"kty\":\"oct\",\"k\":\"" + K1 + "\",\"kid\":\"from-json\"}"},
    {"op": "jwk", "data": "{\"kty\":\"oct\",\"k\":"},
    {"op": "jwk", "data": "[1]"},
    {"op": "encode", "payload": {"sub": "jwk-user"}, "key": {"$jwk": {"kty": "oct", "k": K1, "alg": "HS512"}}},
    {"op": "encode", "payload": {"sub": "jwk-user"}, "key": {"$jwk": {"kty": "oct", "k": K1}}},
    {"op": "encode", "payload": {"sub": "jwk-user"}, "key": {"$jwk": {"kty": "oct", "k": K1}}, "algorithm": "HS384"},
    {"op": "encode", "payload": {"sub": "jwk-user"}, "key": {"$jwk": {"kty": "oct", "k": K1}}, "algorithm": "none"},
    {"op": "decode", "token": {"ref": 0}, "key": {"$jwk": {"kty": "oct", "k": K1, "alg": "HS512"}}},
    {"op": "decode", "token": {"ref": 0}, "key": {"$jwk": {"kty": "oct", "k": K1}}},
    {"op": "decode", "token": {"ref": 0}, "key": {"$jwk": {"kty": "oct", "k": K1}}, "algorithms": ["HS512"]},
    {"op": "decode", "token": {"ref": 2}, "key": {"$jwk": {"kty": "oct", "k": K1}}},
    {"op": "decode", "token": {"ref": 1}, "key": {"$jwk": {"kty": "oct", "k": K1}, "$alg": "HS256"}},
    {"op": "decode", "token": {"ref": 1}, "key": {"$jwk": {"kty": "oct", "k": b64(b"other")}}},
])

job("HMAC JWK conversion", [
    {"op": "to_jwk", "key": SECRET},
    {"op": "to_jwk", "key": SECRET, "as_dict": True},
    {"op": "to_jwk", "key": ""},
    {"op": "to_jwk", "key": "é?>"},
    {"op": "to_jwk", "key": {"$bytes": "fbff00"}},
    {"op": "to_jwk", "key": 5},
    {"op": "from_jwk", "jwk": "{\"kty\": \"oct\", \"k\": \"" + b64(SECRET.encode()) + "\"}"},
    {"op": "from_jwk", "jwk": {"kty": "oct", "k": "-_8A"}},
    {"op": "from_jwk", "jwk": {"kty": "RSA", "k": "AA"}},
    {"op": "from_jwk", "jwk": {"k": "AA"}},
    {"op": "from_jwk", "jwk": {"kty": "oct"}},
    {"op": "from_jwk", "jwk": "{\"kty\": \"oct\", \"k\": 5}"},
    {"op": "from_jwk", "jwk": "not json"},
    {"op": "from_jwk", "jwk": "[]"},
    {"op": "from_jwk", "jwk": "\"oct\""},
    {"op": "from_jwk", "jwk": 7},
    {"op": "from_jwk", "jwk": {"kty": "oct", "k": "abcde"}},
])

KS = {"keys": [{"kty": "oct", "kid": "a", "k": b64(b"key-a")}, {"kty": "oct", "kid": "b", "k": b64(b"key-b"), "alg": "HS384"},
               {"kty": "oct", "k": b64(b"no-kid")}, {"kty": "bogus", "kid": "c"}, {"kty": "oct", "kid": "a", "k": b64(b"dup-a")},
               {"kty": "oct", "kid": "x", "alg": "HS999", "k": "AA"}]}
job("JWK sets", [
    {"op": "jwks", "data": KS, "kids": ["a", "b", "c", "x", "zz", None, "it's"]},
    {"op": "jwks", "data": json.dumps(KS), "kids": ["b"]},
    {"op": "jwks", "data": {"keys": []}},
    {"op": "jwks", "data": {}},
    {"op": "jwks", "data": {"keys": {"kty": "oct"}}},
    {"op": "jwks", "data": {"keys": "abc"}},
    {"op": "jwks", "data": {"keys": [{"kty": "bogus"}]}},
    {"op": "jwks", "data": {"keys": [{"kty": "oct", "kid": "a", "k": "AA"}, {"kty": "RSA", "n": "AQAB"}]}},
    {"op": "jwks", "data": {"keys": [{"kty": "oct", "kid": "a", "k": "AA"}, "not-a-dict"]}},
    {"op": "jwks", "data": {"keys": [7]}},
    {"op": "jwks", "data": {"keys": [[]]}},
    {"op": "jwks", "data": {"keys": [None]}},
    {"op": "jwks", "data": "{\"keys\": [1, 2"},
    {"op": "jwks", "data": "\ufeff{\"keys\": []}"},
    {"op": "jwks", "data": "[]"},
])

# ------------------------------------------------------------ helpers

job("base64url", [
    {"op": "b64", "decode": ["", "a", "ab", "abc", "abcd", "abcde", "YQ", "YQ=", "YQ==", "YQ===", "Y=Q", "ab=x=", "a=b",
                            "====", "-_-_", "+/+/", "Zm9v YmFy", "Zm9v\nYmFy", "Zm9v!YmFy", "é", "Zm9vé", "zz", "zz=="],
     "encode": ["", "00", "ff", "fbff", "fbffbf", "000000", "68656c6c6f"]},
])

job("HMAC key checks", [
    {"op": "keys", "keys": [
        SECRET, "", "-----BEGIN PUBLIC KEY-----\nMFkw\n-----END PUBLIC KEY-----\n",
        "-----BEGIN PUBLIC KEY-----\nMFkw\n-----END PUBLIC KEY-----",
        "-----BEGIN PUBLIC KEY-----\r\nMFkw\r\n-----END PUBLIC KEY-----\r\n",
        "notes\n-----BEGIN CERTIFICATE-----\nMIIB\nMIIC\n-----END CERTIFICATE-----\ntrailer",
        "-----BEGIN CERTIFICATE REQUEST-----\nMII\n-----END CERTIFICATE REQUEST-----",
        "-----BEGIN CERTIFICATE-----\nMII\n-----END CERTIFICATE REQUEST-----",
        "-----BEGIN PUBLIC KEY-----\n\n-----END PUBLIC KEY-----",
        "-----BEGIN PUBLIC KEY-----\n\r\n-----END PUBLIC KEY-----",
        "---- BEGIN SSH2 PUBLIC KEY ----\nAAAA\n---- END SSH2 PUBLIC KEY ----",
        "-----BEGIN MY KEY-----\nAAAA\n-----END MY KEY-----",
        "-----BEGIN PUBLIC KEY----- MFkw -----END PUBLIC KEY-----",
        "-----BEGIN PUBLIC KEY-----\nMFkw\n-----END PRIVATE KEY-----\n-----END PUBLIC KEY-----",
        "ssh-rsa AAAAB3NzaC1yc2E user@host", "ssh-ed25519 AAAA", " ssh-rsa AAAA", "ecdsa-sha2-nistp384 AAAA",
        "ssh-dss", "SSH-RSA AAAA", {"$bytes": "2d2d2d2d2d424547494e205253412050524956415445204b45592d2d2d2d2d0aff0a2d2d2d2d2d454e44205253412050524956415445204b45592d2d2d2d2d"},
        5, None,
    ]},
])

# ------------------------------------------------------------ programs

# The gateway's JWK sets: the current one, and one that adds an RSA key,
# which needs the cryptography package that is not installed.
GW = [
    {"kty": "oct", "kid": "gw-2025-09", "alg": "HS256", "use": "sig", "k": b64(b"september-signing-key")},
    {"kty": "oct", "kid": "gw-2025-10", "alg": "HS512", "use": "sig", "k": b64(b"october-signing-key-512")},
    {"kty": "oct", "kid": "enc-1", "alg": "HS256", "use": "enc", "k": b64(b"encryption-only")},
    {"kty": "oct", "kid": "legacy", "k": b64(b"legacy key")},
]
write("gateway/jwks.json", json.dumps({"keys": GW}, indent=2) + "\n")
write("gateway/jwks-rsa.json", json.dumps({"keys": GW + [{"kty": "RSA", "kid": "rsa-1", "n": "sXch", "e": "AQAB"}]}) + "\n")
write("gateway/routes.txt", "# prefix audience scope\n/api/orders orders orders:read\n/api/orders/admin orders admin\n"
      "/api/billing billing billing\n/api/public - -\n/health - -\n")
ISS = "https://auth.example.com"


def gw_token(kid, digest, keybytes, payload, header=None):
    h = {"alg": {"sha256": "HS256", "sha512": "HS512"}[digest], "kid": kid, "typ": "JWT"}
    if header is not None:
        h = header
    return raw(json.dumps(h, separators=(",", ":")), json.dumps(payload, separators=(",", ":")), keybytes, digest)


def p(sub, exp, aud="orders", scope="orders:read", **kw):
    d = {"iss": ISS, "sub": sub, "aud": aud, "exp": exp, "scope": scope}
    d.update(kw)
    return {k: v for k, v in d.items() if v is not None}


SEPT = b"september-signing-key"
OCT = b"october-signing-key-512"
reqs = []
t = T0
for line in [
    ("GET", "/health", "-"),
    ("GET", "/api/orders/17", gw_token("gw-2025-10", "sha512", OCT, p("alice", T0 + 3600))),
    ("GET", "/api/orders/17", gw_token("gw-2025-09", "sha256", SEPT, p("bob", T0 + 3600))),
    ("POST", "/api/orders/admin/refund", gw_token("gw-2025-10", "sha512", OCT, p("alice", T0 + 3600))),
    ("POST", "/api/orders/admin/refund", gw_token("gw-2025-10", "sha512", OCT, p("root", T0 + 3600, scope="orders:read admin"))),
    ("GET", "/api/billing/invoices", gw_token("gw-2025-10", "sha512", OCT, p("alice", T0 + 3600))),
    ("GET", "/api/billing/invoices", gw_token("gw-2025-10", "sha512", OCT, p("carol", T0 + 3600, aud=["billing", "orders"], scope="billing"))),
    ("GET", "/api/orders/18", gw_token("gw-2025-10", "sha512", OCT, p("dave", T0 - 5))),
    ("GET", "/api/orders/18", gw_token("gw-2025-10", "sha512", OCT, p("dave", T0 + 100))),
    ("GET", "/api/orders/19", gw_token("gw-2025-10", "sha512", OCT, p("eve", T0 + 3600, iss="https://evil.example.com"))),
    ("GET", "/api/orders/19", gw_token("gw-2025-10", "sha512", b"guessed", p("eve", T0 + 3600))),
    ("GET", "/api/orders/19", gw_token("gw-2025-11", "sha512", OCT, p("eve", T0 + 3600))),
    ("GET", "/api/orders/19", gw_token("enc-1", "sha256", b"encryption-only", p("eve", T0 + 3600))),
    ("GET", "/api/orders/19", gw_token(None, "sha256", SEPT, p("eve", T0 + 3600), header={"alg": "HS256"})),
    ("GET", "/api/orders/19", gw_token(9, "sha256", SEPT, p("eve", T0 + 3600), header={"alg": "HS256", "kid": 9})),
    ("GET", "/api/orders/19", gw_token("gw-2025-09", "sha512", SEPT, p("eve", T0 + 3600),
                                       header={"alg": "HS512", "kid": "gw-2025-09"})),
    ("GET", "/api/orders/20", gw_token("gw-2025-09", "sha256", SEPT, p("frank", None))),
    ("GET", "/api/orders/20", gw_token("gw-2025-09", "sha256", SEPT, {"iss": ISS, "aud": "orders", "exp": T0 + 60})),
    ("GET", "/api/orders/21", gw_token("gw-2025-09", "sha256", SEPT, p("gina", T0 + 3600, scope=["orders:read"]))),
    ("GET", "/api/orders/21", gw_token("gw-2025-09", "sha256", SEPT, p("gina", T0 + 3600, scope="orders:readwrite"))),
    ("GET", "/api/public/catalog", gw_token("gw-2025-09", "sha256", SEPT, p("hal", T0 + 3600))),
    ("GET", "/api/public/catalog", gw_token("gw-2025-09", "sha256", SEPT, p("hal", T0 + 3600, aud=None))),
    ("GET", "/api/public/catalog", "-"),
    ("GET", "/api/orders/22", "not-a-token"),
    ("GET", "/api/orders/22", "a.b.c"),
    ("GET", "/static/logo.png", "-"),
    ("GET", "/api/orders/23", gw_token("legacy", "sha256", b"legacy key", p("ivan", T0 + 3600))),
    ("GET", "/api/orders/24", gw_token("gw-2025-10", "sha512", OCT, p("judy", T0 + 3600, nbf=T0 + 50))),
    ("GET", "/api/orders/24", gw_token("gw-2025-10", "sha512", OCT, p("judy", T0 + 3600, nbf=T0 + 50))),
]:
    t += 25
    reqs.append(f"{t} {line[0]} {line[1]} {line[2]}\n")
write("gateway/access.log", "".join(reqs))
job("api gateway", [
    {"op": "gateway", "dir": "gateway", "jwks": "jwks.json", "issuer": ISS, "leeway": 30},
])
job("api gateway with an RSA key in the set", [
    {"op": "gateway", "dir": "gateway", "jwks": "jwks-rsa.json", "issuer": ISS, "leeway": 30},
])

write("issuer/secret.key", "issuer-signing-secret-2025\n")
write("issuer/users.csv", "user,roles,ttl,aud,alg\nalice,admin|ops,3600,console,HS256\nbob,,600,console|cli,HS384\n"
      "carol,ops,60,cli,HS512\ndave,viewer,7200,,HS256\nerin,viewer,1800,console,RS256\nfrank,ops,0,console,HS256\n")
job("token issuer", [
    {"op": "issue", "dir": "issuer", "issuer": "https://issuer.example.com", "kid": "issuer-1", "now": T0,
     "audience": ["console", "cli"], "checks": [0, 59, 60, 600, 3600, 7200]},
])

with open(os.path.join(DATA, "jobs.jsonl"), "w", encoding="utf-8") as f:
    for j in jobs:
        f.write(json.dumps(j) + "\n")
print(f"{len(jobs)} jobs, {sum(len(j['ops']) for j in jobs)} operations")
