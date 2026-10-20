# Runs what mini_cbor runs, through cbor2 5.6.5 itself (the copy in
# cbor2/, unchanged, which runs its pure-Python decoder and encoder):
# each test vector and each file is decoded and printed, encoded again
# with each encoder option, and read back; then the jobs run
# `python -m cbor2.tool` on the files.
import datetime
import os
import sys
from binascii import hexlify
from decimal import Decimal
from fractions import Fraction
from ipaddress import IPv4Address, IPv4Network, IPv6Address, IPv6Network
from uuid import UUID

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import mk  # noqa: E402
import cbor2  # noqa: E402
from cbor2 import tool  # noqa: E402
from cbor2._types import BreakMarkerType, CBORSimpleValue, CBORTag, FrozenDict, UndefinedType  # noqa: E402

DATA = os.path.join(HERE, "data")


# repr(), except that a set's items are sorted by how they print, since
# a set's own order is its hash order
def show(v, seen=()):
    if isinstance(v, (list, tuple, dict, CBORTag, FrozenDict)) and id(v) in seen:
        if isinstance(v, list):
            return "[...]"
        if isinstance(v, tuple):
            return "(...)"
        if isinstance(v, dict):
            return "{...}"
        return "..."
    inner = seen + (id(v),)
    if isinstance(v, list):
        return "[" + ", ".join(show(x, inner) for x in v) + "]"
    if isinstance(v, tuple):
        if len(v) == 1:
            return "(" + show(v[0], inner) + ",)"
        return "(" + ", ".join(show(x, inner) for x in v) + ")"
    if isinstance(v, dict):
        return "{" + ", ".join(show(k, inner) + ": " + show(x, inner) for k, x in v.items()) + "}"
    if isinstance(v, FrozenDict):
        return "FrozenDict(" + show(v._d, seen) + ")"
    if isinstance(v, CBORTag):
        return f"CBORTag({v.tag}, {show(v.value, inner)})"
    if isinstance(v, (set, frozenset)):
        items = sorted(show(x, inner) for x in v)
        name = type(v).__name__
        if not items:
            return name + "()"
        body = "{" + ", ".join(items) + "}"
        return body if name == "set" else f"{name}({body})"
    return repr(v)


def hexs(b):
    return hexlify(b).decode()


def err(e):
    return f"error: {type(e).__name__}: {e}"


def has_set(v, seen=()):
    if id(v) in seen:
        return False
    seen = seen + (id(v),)
    if isinstance(v, (set, frozenset)):
        return True
    if isinstance(v, (list, tuple)):
        return any(has_set(x, seen) for x in v)
    if isinstance(v, (dict, FrozenDict)):
        return any(has_set(k, seen) or has_set(x, seen) for k, x in v.items())
    if isinstance(v, CBORTag):
        return has_set(v.value, seen)
    return False


OPTIONS = [
    ("canonical", {"canonical": True}),
    ("value_sharing", {"value_sharing": True}),
    ("string_referencing", {"string_referencing": True}),
    ("timestamps", {"datetime_as_timestamp": True, "timezone": datetime.timezone.utc}),
    ("dates_as_datetimes", {"date_as_datetime": True, "timezone": datetime.timezone.utc}),
]


def encode(v, opts):
    try:
        return hexs(cbor2.dumps(v, **opts))
    except Exception as e:
        return err(e)


def report(raw):
    try:
        v = cbor2.loads(raw)
    except Exception as e:
        print(err(e))
        return
    print("value: " + show(v))
    if has_set(v):
        # an encoded set lists its items in hash order
        print("dumps: (not shown: the value holds a set)")
        base = None
    else:
        base = encode(v, {})
        print("dumps: " + base)
    for name, opts in OPTIONS:
        if name != "canonical" and base is None:
            continue
        got = encode(v, opts)
        print(f"{name}: " + ("same" if got == base else got))
    again_hex = base if base is not None else encode(v, {"canonical": True})
    if again_hex.startswith("error:"):
        return
    try:
        again = cbor2.loads(bytes.fromhex(again_hex))
        print("read back: " + ("same" if show(again) == show(v) else "differs: " + show(again)))
    except Exception as e:
        print("read back: " + err(e))


def run_job(cmd):
    args = cmd.split(" ")[1:]
    old = os.getcwd()
    os.chdir(os.path.join(DATA, "files"))
    sys.argv = ["python -m cbor2.tool"] + args
    sys.stdout.flush()
    try:
        tool.main()
    except SystemExit as e:
        sys.stdout.flush()
        print(f"exit 1: {e.code}")
    except Exception as e:
        sys.stdout.flush()
        print(err(e))
    finally:
        sys.stdout.flush()
        os.chdir(old)


def main():
    mk.main()
    with open(os.path.join(DATA, "vectors.txt"), encoding="utf-8") as f:
        vectors = [l for l in f.read().split("\n") if l]
    for n, h in enumerate(vectors, 1):
        print(f"== vectors.txt:{n} {h if len(h) <= 64 else h[:64] + '...'}")
        report(bytes.fromhex(h))
    with open(os.path.join(DATA, "files.txt"), encoding="utf-8") as f:
        names = [l for l in f.read().split("\n") if l]
    for rel in names:
        with open(os.path.join(DATA, "files", rel), "rb") as f:
            raw = f.read()
        print(f"== {rel} ({len(raw)} bytes)")
        report(raw)
    with open(os.path.join(DATA, "jobs.txt"), encoding="utf-8") as f:
        jobs = [l for l in f.read().split("\n") if l]
    for n, cmd in enumerate(jobs, 1):
        print(f"== jobs.txt:{n} {cmd}")
        run_job(cmd)


if __name__ == "__main__":
    main()
