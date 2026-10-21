# Runs data/jobs.jsonl through PyJWT itself (the copy in jwt/, unchanged)
# and prints what mini_pyjwt prints. Without the `cryptography` package
# PyJWT offers only HMAC and "none", which is what mini_pyjwt ports, so a
# finder here makes `import cryptography` fail as it would on a machine
# without it. The clock is set by the jobs: the `datetime` that
# jwt.api_jwt asks for the time is replaced by one whose now() returns
# the job's time.
import importlib.abc
import json
import os
import sys
from datetime import datetime, timedelta, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.dont_write_bytecode = True
DATA = os.path.join(HERE, "data")


class NoCryptography(importlib.abc.MetaPathFinder):
    def find_spec(self, name, path=None, target=None):
        if name == "cryptography" or name.startswith("cryptography."):
            raise ModuleNotFoundError(f"No module named {name!r}", name=name)
        return None


sys.meta_path.insert(0, NoCryptography())

import jwt  # noqa: E402
import jwt.api_jwt  # noqa: E402
from jwt.algorithms import HMACAlgorithm, has_crypto  # noqa: E402
from jwt.api_jws import PyJWS  # noqa: E402
from jwt.api_jwt import PyJWT  # noqa: E402
from jwt.utils import base64url_decode, base64url_encode, is_pem_format, is_ssh_key  # noqa: E402

assert not has_crypto

NOW = [0.0]


class FixedDT(datetime):
    @classmethod
    def now(cls, tz=None):
        return cls.fromtimestamp(NOW[0], tz)


jwt.api_jwt.datetime = FixedDT


def failure(e):
    return f"{type(e).__name__}: {e}"


# Job values: a dict with one "$" key stands for a Python value JSON has
# no form for.
def conv(v):
    if isinstance(v, dict):
        if len(v) == 1:
            (k, x), = v.items()
            if k == "$dt":
                y, mo, d, h, mi, s, us, off = (list(x) + [0] * 8)[:8]
                tz = None if off is None else timezone(timedelta(minutes=off))
                return FixedDT(y, mo, d, h, mi, s, us, tzinfo=tz)
            if k == "$naive":
                y, mo, d, h, mi, s, us = (list(x) + [0] * 7)[:7]
                return FixedDT(y, mo, d, h, mi, s, us)
            if k == "$bytes":
                return bytes.fromhex(x)
            if k == "$td":
                return timedelta(seconds=x)
            if k == "$jwk":
                return jwt.PyJWK(conv(x))
        if len(v) == 2 and "$jwk" in v and "$alg" in v:
            return jwt.PyJWK(conv(v["$jwk"]), v["$alg"])
        return {k: conv(x) for k, x in v.items()}
    if isinstance(v, list):
        return [conv(x) for x in v]
    return v


def show(v):
    if isinstance(v, bytes):
        return v.hex()
    return repr(v)


class Job:
    def __init__(self):
        self.tokens = []

    def token(self, spec):
        if isinstance(spec, dict) and "ref" in spec:
            t = self.tokens[spec["ref"]]
            if "seg" in spec:
                parts = t.split(".")
                parts[spec["seg"]] = spec["value"]
                t = ".".join(parts)
            if "append" in spec:
                t = t + spec["append"]
            return t
        return conv(spec)

    def kw(self, op, names):
        out = {}
        for n in names:
            if n in op:
                out[n] = conv(op[n])
        return out


def jws_of(op):
    if "allowed" in op:
        return PyJWS(algorithms=op["allowed"])
    return jwt.api_jws._jws_global_obj


def run_op(job, op):
    kind = op["op"]
    NOW[0] = op.get("now", NOW[0])
    if kind == "encode":
        args = job.kw(op, ["algorithm", "headers", "sort_headers"])
        try:
            t = jwt.encode(conv(op["payload"]), conv(op.get("key")), **args)
        except Exception as e:
            print(f"  error: {failure(e)}")
            return
        job.tokens.append(t)
        print(f"  token: {t}")
    elif kind == "decode":
        args = job.kw(op, ["algorithms", "options", "audience", "issuer", "subject", "leeway"])
        if "key" in op:
            args["key"] = conv(op["key"])
        if "detached" in op:
            args["detached_payload"] = op["detached"].encode()
        obj = PyJWT(conv(op["instance"])) if "instance" in op else jwt.api_jwt._jwt_global_obj
        try:
            if op.get("complete"):
                d = obj.decode_complete(job.token(op["token"]), **args)
                print(f"  header: {d['header']!r}")
                print(f"  payload: {d['payload']!r}")
                print(f"  signature: {d['signature'].hex()}")
            else:
                print(f"  payload: {obj.decode(job.token(op['token']), **args)!r}")
        except Exception as e:
            print(f"  error: {failure(e)}")
    elif kind == "header":
        try:
            print(f"  header: {jwt.get_unverified_header(job.token(op['token']))!r}")
        except Exception as e:
            print(f"  error: {failure(e)}")
    elif kind == "jws_encode":
        args = job.kw(op, ["algorithm", "headers", "sort_headers"])
        if op.get("detached"):
            args["is_payload_detached"] = True
        try:
            t = jws_of(op).encode(op["payload"].encode(), conv(op.get("key")), **args)
        except Exception as e:
            print(f"  error: {failure(e)}")
            return
        job.tokens.append(t)
        print(f"  token: {t}")
    elif kind == "jws_decode":
        args = job.kw(op, ["algorithms", "options"])
        if "key" in op:
            args["key"] = conv(op["key"])
        if "detached" in op:
            args["detached_payload"] = op["detached"].encode()
        try:
            d = jws_of(op).decode_complete(job.token(op["token"]), **args)
            print(f"  header: {d['header']!r}")
            print(f"  payload: {d['payload']!r}")
        except Exception as e:
            print(f"  error: {failure(e)}")
    elif kind == "algorithms":
        w = jws_of(op)
        print(f"  algorithms: {sorted(w.get_algorithms())}")
        for name in op["names"]:
            try:
                print(f"  {name!r}: {type(w.get_algorithm_by_name(conv(name))).__name__}")
            except Exception as e:
                print(f"  {name!r}: {failure(e)}")
    elif kind == "jwk":
        try:
            d = op["data"]
            k = jwt.PyJWK.from_json(d, op.get("algorithm")) if isinstance(d, str) \
                else jwt.PyJWK(conv(d), op.get("algorithm"))
        except Exception as e:
            print(f"  error: {failure(e)}")
            return
        print(f"  alg={k.algorithm_name} kty={k.key_type!r} kid={k.key_id!r} use={k.public_key_use!r}"
              f" {type(k.Algorithm).__name__} key={k.key!r}")
    elif kind == "jwks":
        try:
            d = op["data"]
            ks = jwt.PyJWKSet.from_json(d) if isinstance(d, str) else jwt.PyJWKSet.from_dict(conv(d))
        except Exception as e:
            print(f"  error: {failure(e)}")
            return
        print(f"  keys: {[k.key_id for k in ks.keys]}")
        for kid in op.get("kids", []):
            try:
                k = ks[kid]
                print(f"  {kid!r}: {k.algorithm_name} {k.key!r}")
            except Exception as e:
                print(f"  {kid!r}: {failure(e)}")
    elif kind == "to_jwk":
        try:
            print(f"  jwk: {HMACAlgorithm.to_jwk(conv(op['key']), op.get('as_dict', False))!r}")
        except Exception as e:
            print(f"  error: {failure(e)}")
    elif kind == "from_jwk":
        try:
            print(f"  key: {HMACAlgorithm.from_jwk(conv(op['jwk']))!r}")
        except Exception as e:
            print(f"  error: {failure(e)}")
    elif kind == "b64":
        for s in op.get("decode", []):
            try:
                print(f"  {s!r} -> {base64url_decode(s).hex()}")
            except Exception as e:
                print(f"  {s!r} -> {failure(e)}")
        for h in op.get("encode", []):
            print(f"  {h} -> {base64url_encode(bytes.fromhex(h)).decode()}")
    elif kind == "keys":
        alg = HMACAlgorithm(HMACAlgorithm.SHA256)
        for k in op["keys"]:
            v = conv(k)
            b = v.encode() if isinstance(v, str) else v
            try:
                alg.prepare_key(v)
                verdict = "ok"
            except Exception as e:
                verdict = failure(e)
            if isinstance(b, bytes):
                print(f"  pem={is_pem_format(b)} ssh={is_ssh_key(b)} {verdict}")
            else:
                print(f"  {verdict}")
    elif kind == "gateway":
        gateway(op)
    elif kind == "issue":
        issue(op)
    else:
        raise SystemExit(f"unknown op {kind}")


# ------------------------------------------------------------ programs

# An API gateway: each request's bearer token is checked against the JWK
# set by its kid, then against the route's audience and scope.
def gateway(op):
    base = os.path.join(DATA, op["dir"])
    with open(os.path.join(base, op["jwks"]), encoding="utf-8") as f:
        text = f.read()
    try:
        keyset = jwt.PyJWKSet.from_json(text)
        print(f"  keyset: {len(keyset.keys)} keys")
    except Exception as e:
        keyset = None
        print(f"  keyset: {failure(e)}")
    routes = []
    with open(os.path.join(base, "routes.txt"), encoding="utf-8") as f:
        for line in f:
            if line.strip() and not line.startswith("#"):
                prefix, aud, scope = line.split()
                routes.append((prefix, aud, scope))
    issuer = op["issuer"]
    leeway = op["leeway"]
    counts = {}
    by_sub = {}
    with open(os.path.join(base, "access.log"), encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line:
                continue
            ts, method, path, token = line.split(" ")
            NOW[0] = float(ts)
            status, why = handle(keyset, routes, issuer, leeway, path, token)
            print(f"  {ts} {method} {path} -> {status} {why}")
            counts[status] = counts.get(status, 0) + 1
            if status == 200:
                by_sub[why] = by_sub.get(why, 0) + 1
    print(f"  statuses: {', '.join(f'{k}={v}' for k, v in sorted(counts.items()))}")
    print(f"  callers: {', '.join(f'{k}={v}' for k, v in sorted(by_sub.items()))}")


def handle(keyset, routes, issuer, leeway, path, token):
    best = None
    for r in routes:
        if path.startswith(r[0]) and (best is None or len(r[0]) > len(best[0])):
            best = r
    if best is None:
        return 404, "no route"
    if token == "-":
        if best[1] == "-" and best[2] == "-":
            return 200, "anonymous"
        return 401, "missing token"
    if keyset is None:
        return 503, "no keys"
    try:
        header = jwt.get_unverified_header(token)
    except jwt.PyJWTError as e:
        return 401, failure(e)
    kid = header.get("kid")
    if kid is None:
        return 401, "no kid"
    try:
        key = keyset[kid]
    except KeyError:
        return 401, f"unknown kid {kid}"
    if key.public_key_use not in (None, "sig"):
        return 401, f"key {kid} is for {key.public_key_use}"
    aud = None if best[1] == "-" else best[1]
    try:
        payload = jwt.decode(token, key, audience=aud, issuer=issuer, leeway=leeway,
                             options={"require": ["exp", "sub"]})
    except jwt.PyJWTError as e:
        return 401, failure(e)
    scope = payload.get("scope", "")
    if not isinstance(scope, str):
        return 403, "scope is not a string"
    if best[2] != "-" and best[2] not in scope.split():
        return 403, f"needs {best[2]}"
    return 200, payload["sub"]


# A token issuer: one token per user in users.csv, written to a file,
# read back and checked at three times.
def issue(op):
    base = os.path.join(DATA, op["dir"])
    with open(os.path.join(base, "secret.key"), "rb") as f:
        secret = f.read().rstrip(b"\n")
    NOW[0] = op["now"]
    now = FixedDT.now(timezone.utc)
    lines = []
    with open(os.path.join(base, "users.csv"), encoding="utf-8") as f:
        rows = [line.rstrip("\n").split(",") for line in f if line.strip()]
    for user, roles, ttl, aud, alg in rows[1:]:
        payload = {"sub": user, "iss": op["issuer"], "iat": now, "nbf": now,
                   "exp": FixedDT.fromtimestamp(NOW[0] + int(ttl), timezone.utc), "roles": roles.split("|") if roles else []}
        if aud:
            payload["aud"] = aud.split("|") if "|" in aud else aud
        try:
            t = jwt.encode(payload, secret, algorithm=alg, headers={"kid": op["kid"]})
        except Exception as e:
            print(f"  {user}: {failure(e)}")
            continue
        lines.append(f"{user} {t}\n")
    os.makedirs(os.path.join(base, "out"), exist_ok=True)
    with open(os.path.join(base, "out", "tokens.txt"), "w", encoding="utf-8") as f:
        f.write("".join(lines))
    with open(os.path.join(base, "out", "tokens.txt"), encoding="utf-8") as f:
        issued = [line.split() for line in f]
    print(f"  issued {len(issued)} tokens")
    for at in op["checks"]:
        NOW[0] = op["now"] + at
        for user, t in issued:
            try:
                p = jwt.decode(t, secret, algorithms=["HS256", "HS384", "HS512"],
                               audience=op["audience"], issuer=op["issuer"])
                print(f"  +{at} {user}: ok roles={p['roles']}")
            except jwt.PyJWTError as e:
                print(f"  +{at} {user}: {failure(e)}")


def main():
    with open(os.path.join(DATA, "jobs.jsonl"), encoding="utf-8") as f:
        for line in f:
            spec = json.loads(line)
            print(f"== {spec['name']}")
            job = Job()
            for op in spec["ops"]:
                run_op(job, op)


main()
