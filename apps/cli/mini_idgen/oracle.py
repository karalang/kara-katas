# Runs data/jobs.jsonl through Python 3.13's uuid module, hashids 1.3.1
# and shortuuid 1.0.13 (the packages here, unchanged) and prints what
# mini_idgen prints. Run mk.py first.
#
# uuid1 reads the clock and uuid4 reads os.urandom, so for those jobs the
# clock and the random bytes are replaced by the job's own values; the rest
# of uuid1 and uuid4 runs as it is.
import json
import os
import sys
import time
import uuid

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hashids  # noqa: E402
import shortuuid  # noqa: E402


def emit(s):
    print(s)


def err(e):
    emit("  %s: %s" % (type(e).__name__, e))


def show(u):
    emit("  str %s" % u)
    emit("  repr %r" % u)
    emit("  hex %s int %d" % (u.hex, u.int))
    emit("  urn %s" % u.urn)
    emit("  fields %r" % (u.fields,))
    emit("  time %d clock_seq %d node %d" % (u.time, u.clock_seq, u.node))
    emit("  variant %r version %r" % (u.variant, u.version))
    emit("  bytes %r" % u.bytes)
    emit("  bytes_le %r" % u.bytes_le)


def run_uuid(j):
    kw = {}
    for k in ["hex", "fields", "version"]:
        if k in j:
            kw[k] = j[k]
    if "bytes" in j:
        kw["bytes"] = bytes(j["bytes"])
    if "bytes_le" in j:
        kw["bytes_le"] = bytes(j["bytes_le"])
    if "int" in j:
        kw["int"] = int(j["int"])
    if "fields" in kw:
        kw["fields"] = tuple(kw["fields"])
    try:
        u = uuid.UUID(**kw)
    except (ValueError, TypeError) as e:
        err(e)
        return
    show(u)


def run_sort(j):
    us = [uuid.UUID(h) for h in j["uuids"]]
    for u in sorted(us):
        emit("  %s" % u)
    emit("  %d distinct" % len(set(us)))
    a, b = us[0], us[1]
    emit("  first two: == %r < %r <= %r > %r >= %r" % (a == b, a < b, a <= b, a > b, a >= b))


NS = {"@dns": uuid.NAMESPACE_DNS, "@url": uuid.NAMESPACE_URL, "@oid": uuid.NAMESPACE_OID,
      "@x500": uuid.NAMESPACE_X500}


def run_hashed(j):
    ns = NS[j["namespace"]] if j["namespace"] in NS else uuid.UUID(j["namespace"])
    name = bytes(j["name_bytes"]) if "name_bytes" in j else j["name"]
    f = uuid.uuid3 if j["op"] == "uuid3" else uuid.uuid5
    u = f(ns, name)
    emit("  %s version %r" % (u, u.version))


def run_uuid1(j):
    real = time.time_ns
    try:
        for ns, node, seq in j["calls"]:
            time.time_ns = lambda ns=ns: ns
            try:
                u = uuid.uuid1(node, seq)
            except ValueError as e:
                err(e)
                continue
            emit("  %s time %d clock_seq %d node %012x" % (u, u.time, u.clock_seq, u.node))
    finally:
        time.time_ns = real


def run_uuid4(j):
    real = os.urandom
    os.urandom = lambda n: bytes(j["bytes"])
    try:
        u = uuid.uuid4()
    finally:
        os.urandom = real
    emit("  %s variant %r version %r" % (u, u.variant, u.version))


def make_hashids(cfg):
    kw = {}
    for k in ["salt", "min_length", "alphabet"]:
        if k in cfg:
            kw[k] = cfg[k]
    return hashids.Hashids(**kw)


def run_hashids(j):
    try:
        h = make_hashids(j["config"])
    except ValueError as e:
        err(e)
        return
    emit("  alphabet %r separators %r guards %r" % (h._alphabet, h._separators, h._guards))
    for v in j["encode"]:
        s = h.encode(*v)
        emit("  encode%r = %r" % (tuple(v), s))
        if j["roundtrip"] and s:
            emit("    decode = %r" % (h.decode(s),))
    for s in j["decode"]:
        emit("  decode(%r) = %r" % (s, h.decode(s)))
    for x in j["encode_hex"]:
        s = h.encode_hex(x)
        emit("  encode_hex(%r) = %r decode_hex = %r" % (x, s, h.decode_hex(s)))


def run_shortuuid(j):
    try:
        su = shortuuid.ShortUUID(j["alphabet"])
    except ValueError as e:
        err(e)
        return
    emit("  alphabet %r length %d" % (su.get_alphabet(), su._length))
    for h, pad in j["encode"]:
        s = su.encode(uuid.UUID(h), pad)
        emit("  encode(%s, %r) = %r" % (h, pad, s))
        emit("    decode = %s" % su.decode(s))
    for s, legacy in j["decode"]:
        try:
            emit("  decode(%r, legacy=%r) = %s" % (s, legacy, su.decode(s, legacy)))
        except ValueError as e:
            emit("  decode(%r, legacy=%r): ValueError: %s" % (s, legacy, e))
    for name, pad in j["names"]:
        emit("  uuid(%r, %r) = %r" % (name, pad, su.uuid(name, pad)))
    for n in j["lengths"]:
        emit("  encoded_length(%d) = %d" % (n, su.encoded_length(n)))


# ------------------------------------------------------------ reports

def read(name):
    with open(os.path.join("data", name), encoding="utf-8") as fh:
        return fh.read()


def tenants():
    out = {}
    for line in read("tenants.txt").splitlines():
        name, salt = line.split(" ", 1)
        out[name] = salt
    return out


def minted():
    salts = tenants()
    out = []
    lines = read("orders.csv").splitlines()
    for n, line in enumerate(lines[1:], 2):
        tenant, order, customer, amount = line.split(",")
        if tenant not in salts:
            out.append((n, tenant, None, "unknown tenant %r" % tenant))
            continue
        try:
            oid = int(order)
        except ValueError:
            out.append((n, tenant, None, "bad order id %r" % order))
            continue
        h = hashids.Hashids(salts[tenant], min_length=8)
        public = h.encode(oid, int(customer))
        if not public:
            out.append((n, tenant, None, "order id %d cannot be encoded" % oid))
            continue
        out.append((n, tenant, (oid, int(customer), int(amount), public), None))
    return out


def run_orders(j):
    totals = {}
    for n, tenant, row, problem in minted():
        if problem:
            emit("  line %d: %s" % (n, problem))
            continue
        oid, customer, amount, public = row
        emit("  %-8s order %5d customer %3d %9.2f -> %s" % (tenant, oid, customer, amount / 100, public))
        t = totals.setdefault(tenant, [0, 0])
        t[0] += 1
        t[1] += amount
    for tenant in sorted(totals):
        emit("  total %-8s %2d orders %10.2f" % (tenant, totals[tenant][0], totals[tenant][1] / 100))


def utc(ticks):
    # ticks are 100 ns since 1970-01-01
    secs, frac = divmod(ticks, 10**7)
    t = time.gmtime(secs)
    return "%04d-%02d-%02d %02d:%02d:%02d.%07d" % (t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour,
                                                   t.tm_min, t.tm_sec, frac)


def run_events(j):
    good = []
    for line in read("events.log").splitlines():
        ident, kind = line.split(" ", 1)
        try:
            u = uuid.UUID(ident)
        except ValueError:
            emit("  skipped %r: not a UUID" % ident)
            continue
        if u.version != 1:
            emit("  skipped %s: version %r, not a time-based id" % (u, u.version))
            continue
        good.append((u.time - 0x01b21dd213814000, u.node, u.clock_seq, kind, u))
    good.sort(key=lambda e: (e[0], e[1]))
    prev = None
    hosts = {}
    for ticks, node, seq, kind, u in good:
        mac = ":".join("%02x" % ((node >> s) & 0xff) for s in range(40, -8, -8))
        gap = "" if prev is None else " +%dms" % ((ticks - prev) // 10**4)
        emit(("  %s %s seq %5d %-13s%s" % (utc(ticks), mac, seq, kind, gap)).rstrip())
        prev = ticks
        hosts[mac] = hosts.get(mac, 0) + 1
    for mac in sorted(hosts):
        emit("  host %s %d events" % (mac, hosts[mac]))


def run_links(j):
    seen = set()
    for url in read("links.txt").splitlines():
        short = shortuuid.uuid(name=url)
        ns = "url" if url.lower().startswith(("http://", "https://")) else "dns"
        mark = " (seen)" if short in seen else ""
        seen.add(short)
        emit("  %s %s %s%s" % (short, ns, url, mark))
        emit("    = %s" % shortuuid.decode(short))


def run_incoming(j):
    salts = tenants()
    for n, tenant, row, problem in minted():
        if problem or n % 3 != 0:
            continue
        oid, customer, amount, public = row
        h = hashids.Hashids(salts[tenant], min_length=8)
        other = sorted(t for t in salts if t != tenant)[0]
        wrong = hashids.Hashids(salts[other], min_length=8)
        cases = [public, public[:-1] + ("a" if public[-1] != "a" else "b"), public.swapcase(),
                 public + public[0], public[1:]]
        for c in cases:
            emit("  %s %-22r -> %r, under %s -> %r" % (tenant, c, h.decode(c), other, wrong.decode(c)))


OPS = {"uuid": run_uuid, "sort": run_sort, "uuid3": run_hashed, "uuid5": run_hashed,
       "uuid1": run_uuid1, "uuid4": run_uuid4, "hashids": run_hashids,
       "shortuuid": run_shortuuid, "orders": run_orders, "events": run_events,
       "links": run_links, "incoming": run_incoming}

with open("data/jobs.jsonl", encoding="utf-8") as fh:
    for n, line in enumerate(fh):
        j = json.loads(line)
        rest = " ".join("%s=%r" % (k, v) for k, v in j.items() if k != "op")
        emit(("== %d %s %s" % (n, j["op"], rest)).rstrip())
        OPS[j["op"]](j)
