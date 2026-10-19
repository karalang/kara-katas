# Runs data/jobs.jsonl through itsdangerous 2.2.0 (the package here) and
# prints what mini_itsdangerous prints. Run mk.py first.
#
# The timestamp signers read the job's clock instead of time.time().
import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import itsdangerous  # noqa: E402
from itsdangerous import exc  # noqa: E402
from itsdangerous.signer import NoneAlgorithm  # noqa: E402

CLOCK = [0]
itsdangerous.TimestampSigner.get_timestamp = lambda self: CLOCK[0]

DIGESTS = {"sha1": hashlib.sha1, "sha256": hashlib.sha256,
           "sha512": hashlib.sha512, "md5": hashlib.md5}
CLASSES = {
    "Signer": itsdangerous.Signer,
    "TimestampSigner": itsdangerous.TimestampSigner,
    "Serializer": itsdangerous.Serializer,
    "TimedSerializer": itsdangerous.TimedSerializer,
    "URLSafeSerializer": itsdangerous.URLSafeSerializer,
    "URLSafeTimedSerializer": itsdangerous.URLSafeTimedSerializer,
}


def kwargs_of(d):
    kw = {}
    for k, v in d.items():
        kw[k] = DIGESTS[v] if k == "digest_method" else v
    return kw


def build(cfg):
    cls = CLASSES[cfg["cls"]]
    kw = {}
    if "salt" in cfg:
        kw["salt"] = cfg["salt"]
    if cfg["cls"].endswith("Signer"):
        for k in ["sep", "key_derivation", "digest_method"]:
            if k in cfg:
                kw[k] = DIGESTS[cfg[k]] if k == "digest_method" else cfg[k]
        if cfg.get("algorithm") == "none":
            kw["algorithm"] = NoneAlgorithm()
    else:
        if "signer_kwargs" in cfg:
            kw["signer_kwargs"] = kwargs_of(cfg["signer_kwargs"])
        if "fallback" in cfg:
            fb = []
            for f in cfg["fallback"]:
                if "cls" in f and "kwargs" in f:
                    fb.append((CLASSES[f["cls"]], kwargs_of(f["kwargs"])))
                elif "cls" in f:
                    fb.append(CLASSES[f["cls"]])
                else:
                    fb.append(kwargs_of(f["kwargs"]))
            kw["fallback_signers"] = fb
    return cls(cfg["key"], **kw)


def err(e):
    s = f"{type(e).__name__}: {e}"
    if isinstance(e, exc.BadSignature):
        s += f" payload={e.payload!r}"
    if isinstance(e, exc.BadTimeSignature):
        s += f" date={e.date_signed}"
    if isinstance(e, exc.BadPayload):
        o = e.original_error
        s += f" orig={type(o).__name__ if o is not None else None}"
    return s


def show(v):
    if isinstance(v, float):
        raise SystemExit("a float reached the output")
    if isinstance(v, list):
        for x in v:
            show(x)
    if isinstance(v, dict):
        for x in v.values():
            show(x)
    return repr(v)


def mutate(b, muts):
    for m in muts:
        k = m[0]
        if k == "flip":
            p = m[1] % len(b) if b else 0
            if b:
                c = ord("B") if b[p] == ord("A") else ord("A")
                b = b[:p] + bytes([c]) + b[p + 1:]
        elif k == "cut":
            b = b[:max(0, len(b) - m[1])]
        elif k == "add":
            b = b + m[1].encode()
        elif k == "ins":
            p = m[1] % len(b) if b else 0
            b = b[:p] + m[2].encode() + b[p:]
        elif k == "repl":
            b = b.replace(m[1].encode(), m[2].encode(), 1)
    return b


def run(j):
    print(f"== {j['name']}")
    CLOCK[0] = j["now"]
    objs = {}
    for name, cfg in j["objs"].items():
        try:
            objs[name] = build(cfg)
        except Exception as e:
            objs[name] = e
    saved = {}
    lastt = [b""]
    for i, o in enumerate(j["ops"]):
        if "now" in o:
            CLOCK[0] = o["now"]
        if "value" in o:
            tok = o["value"].encode()
        elif "hex" in o:
            tok = bytes.fromhex(o["hex"])
        elif "use" in o:
            tok = saved[o["use"]]
        elif "last" in o:
            tok = lastt[0]
        else:
            tok = None
        if tok is not None and "mut" in o:
            tok = mutate(tok, o["mut"])
        tag = f"{i + 1}. {o['op']} {o['on']}"
        obj = objs[o["on"]]
        if isinstance(obj, Exception):
            print(f"{tag} -> {err(obj)}")
            continue
        kw = {}
        if "max_age" in o:
            kw["max_age"] = o["max_age"]
        if o.get("ts"):
            kw["return_timestamp"] = True
        try:
            n = o["op"]
            if n == "sign":
                r = obj.sign(tok)
                lastt[0] = r
                if "save" in o:
                    saved[o["save"]] = r
                out = repr(r)
            elif n == "dumps":
                r = obj.dumps(o["obj"], **({"salt": o["salt"]} if "salt" in o else {}))
                lastt[0] = r.encode() if isinstance(r, str) else r
                if "save" in o:
                    saved[o["save"]] = lastt[0]
                out = repr(r)
            elif n == "unsign":
                r = obj.unsign(tok, **kw)
                if isinstance(r, tuple):
                    out = f"{r[0]!r} @ {r[1]}"
                else:
                    out = repr(r)
            elif n == "validate":
                out = repr(obj.validate(tok, **kw))
            elif n == "get_signature":
                out = repr(obj.get_signature(tok))
            elif n == "derive_key":
                out = obj.derive_key().hex()
            elif n == "loads":
                if "salt" in o:
                    kw["salt"] = o["salt"]
                r = obj.loads(tok, **kw)
                if kw.get("return_timestamp"):
                    out = f"{show(r[0])} @ {r[1]}"
                else:
                    out = show(r)
            elif n == "loads_unsafe":
                if "salt" in o:
                    kw["salt"] = o["salt"]
                ok, r = obj.loads_unsafe(tok, **kw)
                out = f"({ok}, {show(r)})"
            else:
                raise SystemExit(f"unknown op {n}")
        except SystemExit:
            raise
        except Exception as e:
            out = err(e)
        print(f"{tag} -> {out}")


with open("data/jobs.jsonl") as f:
    for line in f:
        run(json.loads(line))
