# Runs jobs.tsv through dnspython itself (the copy in dns/, unchanged)
# and prints what mini_dnspython prints.
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.dont_write_bytecode = True

import dns.exception  # noqa: E402
import dns.flags  # noqa: E402
import dns.ipv6  # noqa: E402
import dns.message  # noqa: E402
import dns.name  # noqa: E402
import dns.rcode  # noqa: E402
import dns.rdataclass  # noqa: E402
import dns.rdatatype  # noqa: E402
import dns.reversename  # noqa: E402
import dns.ttl  # noqa: E402
import dns.zone  # noqa: E402

DATA = os.path.join(HERE, "data")
IN = dns.rdataclass.IN
NS = dns.rdatatype.NS
MX = dns.rdatatype.MX
SRV = dns.rdatatype.SRV
CNAME = dns.rdatatype.CNAME
SOA = dns.rdatatype.SOA
ANY = dns.rdatatype.ANY


def read(name):
    with open(os.path.join(DATA, name), encoding="utf-8", newline="") as f:
        return f.read()


def fail(e):
    return "! %s: %s" % (type(e).__name__, e)


def indent(text):
    for line in text.split("\n"):
        print("  " + line)


def opt_name(text):
    if text == "-":
        return None
    return dns.name.from_text(text, None)


def try_line(label, f):
    try:
        print("  %s %s" % (label, f()))
    except Exception as e:
        print("  %s %s" % (label, fail(e)))


def zone_job(name, origin, mode):
    z = dns.zone.from_text(read(name), origin, relativize=(mode != "abs"),
                           check_origin=(mode != "nocheck"))
    if mode == "abs":
        text = z.to_text(relativize=False)
    elif mode == "comments":
        text = z.to_text(want_comments=True)
    elif mode == "origin":
        text = z.to_text(want_origin=True)
    else:
        text = z.to_text()
    sys.stdout.write(text)
    count = sum(len(rds) for node in z.values() for rds in node)
    print("  (%d names, %d records)" % (len(z.nodes), count))


def name_job(text, origin):
    n = dns.name.from_text(text, opt_name(origin))
    print("  text %s omit %s absolute %s wild %s labels %d" % (
        n.to_text(), n.to_text(True), n.is_absolute(), n.is_wild(), len(n)))
    print("  canonical %s" % n.canonicalize())
    try_line("wire", lambda: n.to_wire().hex())
    try_line("digest", lambda: n.to_digestable(dns.name.from_text("example.")).hex())


def cmp_job(a, b):
    x = dns.name.from_text(a, None)
    y = dns.name.from_text(b, None)
    rel, order, common = x.fullcompare(y)
    print("  %s %d %d" % (rel.name, order, common))
    print("  subdomain %s superdomain %s equal %s less %s" % (
        x.is_subdomain(y), x.is_superdomain(y), x == y, x < y))
    print("  relativize %s" % x.relativize(y))
    try_line("derelativize", lambda: x.derelativize(y))


def split_job(text, depth):
    n = dns.name.from_text(text, None)
    prefix, suffix = n.split(int(depth))
    print("  %s | %s" % (prefix, suffix))


def concat_job(a, b):
    print("  %s" % dns.name.from_text(a, None).concatenate(dns.name.from_text(b, None)))


def parent_job(text):
    print("  %s" % dns.name.from_text(text, None).parent())


def ip6_job(text):
    wire = dns.ipv6.inet_aton(text)
    print("  %s %s" % (wire.hex(), dns.ipv6.inet_ntoa(wire)))


def add(r, section, name, rds):
    rrset = r.find_rrset(section, name, rds.rdclass, rds.rdtype, create=True)
    rrset.update(rds)


def glue(zone, r, rds):
    for rd in rds:
        if rds.rdtype == MX:
            target = rd.exchange
        else:
            target = rd.target
        if target.is_subdomain(zone.origin):
            node = zone.get_node(target)
            if node is not None:
                for t in (dns.rdatatype.A, dns.rdatatype.AAAA):
                    s = node.get_rdataset(IN, t)
                    if s is not None:
                        add(r, r.additional, target, s)


def soa(zone, r):
    add(r, r.authority, zone.origin, zone.get_rdataset(zone.origin, SOA))


def respond(zone, q):
    r = dns.message.make_response(q)
    r.flags |= dns.flags.AA
    if len(q.question) != 1:
        r.set_rcode(dns.rcode.FORMERR)
        return r
    qrr = q.question[0]
    qname = qrr.name
    qtype = qrr.rdtype
    if qrr.rdclass != IN or not qname.is_subdomain(zone.origin):
        r.flags &= ~dns.flags.AA
        r.set_rcode(dns.rcode.REFUSED)
        return r
    # a delegation between the apex and the name answers with a referral
    path = []
    n = qname
    while n != zone.origin:
        path.append(n)
        n = n.parent()
    for n in reversed(path):
        node = zone.get_node(n)
        if node is not None:
            ns = node.get_rdataset(IN, NS)
            if ns is not None:
                r.flags &= ~dns.flags.AA
                add(r, r.authority, n, ns)
                glue(zone, r, ns)
                return r
    name = qname
    chain = 0
    while True:
        node = zone.get_node(name)
        if node is None:
            if chain == 0:
                r.set_rcode(dns.rcode.NXDOMAIN)
            soa(zone, r)
            return r
        if qtype == ANY:
            for rds in node:
                add(r, r.answer, name, rds)
            return r
        rds = node.get_rdataset(IN, qtype)
        if rds is not None:
            add(r, r.answer, name, rds)
            if qtype in (NS, MX, SRV):
                glue(zone, r, rds)
            return r
        cname = node.get_rdataset(IN, CNAME)
        if cname is not None and chain < 8:
            add(r, r.answer, name, cname)
            target = cname[0].target
            if not target.is_subdomain(zone.origin):
                return r
            name = target
            chain += 1
            continue
        soa(zone, r)
        return r


def answer(zone, wire, udp):
    q = dns.message.from_wire(wire)
    r = respond(zone, q)
    if udp:
        try:
            out = r.to_wire(max_size=512, want_shuffle=False)
        except dns.exception.TooBig as e:
            print("  " + fail(e))
            out = r.to_wire(max_size=512, prefer_truncation=True, want_shuffle=False)
    else:
        out = r.to_wire(want_shuffle=False)
    print("  wire %d %s" % (len(out), out.hex()))
    indent(dns.message.from_wire(out).to_text())


def serve_job(name, origin, qname, qtype, qid, udp):
    zone = dns.zone.from_text(read(name), origin, relativize=False)
    q = dns.message.make_query(qname, qtype, id=int(qid))
    answer(zone, q.to_wire(), udp)


def wire_job(hexwire):
    m = dns.message.from_wire(bytes.fromhex(hexwire))
    indent(m.to_text())
    print("  rewire %s" % m.to_wire(want_shuffle=False).hex())


def line(n, rds, rd):
    return "%s %d %s %s %s" % (n, rds.ttl, dns.rdataclass.to_text(rds.rdclass),
                               dns.rdatatype.to_text(rds.rdtype), rd.to_text())


def diff_job(old, new, origin):
    a = dns.zone.from_text(read(old), origin)
    b = dns.zone.from_text(read(new), origin)
    names = set(a.keys())
    for n in b.keys():
        if n not in names:
            names.add(n)
    removed = added = changed = 0
    for n in sorted(names):
        na = a.get_node(n)
        nb = b.get_node(n)
        for rds in (na if na is not None else []):
            other = nb.get_rdataset(rds.rdclass, rds.rdtype) if nb is not None else None
            for rd in rds:
                if other is None or rd not in other:
                    print("  - " + line(n, rds, rd))
                    removed += 1
            if other is not None and other.ttl != rds.ttl:
                print("  ~ %s %s ttl %d -> %d" % (n, dns.rdatatype.to_text(rds.rdtype), rds.ttl, other.ttl))
                changed += 1
        for rds in (nb if nb is not None else []):
            other = na.get_rdataset(rds.rdclass, rds.rdtype) if na is not None else None
            for rd in rds:
                if other is None or rd not in other:
                    print("  + " + line(n, rds, rd))
                    added += 1
    print("  %d removed, %d added, %d ttl changes" % (removed, added, changed))


def run(job):
    kind = job[0]
    if kind == "zone":
        zone_job(job[1], job[2], job[3])
    elif kind == "name":
        name_job(job[1], job[2])
    elif kind == "cmp":
        cmp_job(job[1], job[2])
    elif kind == "split":
        split_job(job[1], job[2])
    elif kind == "concat":
        concat_job(job[1], job[2])
    elif kind == "parent":
        parent_job(job[1])
    elif kind == "ttl":
        print("  %d" % dns.ttl.from_text(job[1]))
    elif kind == "ip6":
        ip6_job(job[1])
    elif kind == "rev":
        print("  %s" % dns.reversename.from_address(job[1]))
    elif kind == "unrev":
        print("  %s" % dns.reversename.to_address(dns.name.from_text(job[1])))
    elif kind == "query":
        q = dns.message.make_query(job[1], job[2], id=int(job[3]))
        print("  wire %s" % q.to_wire().hex())
        indent(q.to_text())
    elif kind == "serve":
        serve_job(job[1], job[2], job[3], job[4], job[5], len(job) > 6)
    elif kind == "servewire":
        answer(dns.zone.from_text(read(job[1]), job[2], relativize=False), bytes.fromhex(job[3]), False)
    elif kind == "wire":
        wire_job(job[2])
    elif kind == "diff":
        diff_job(job[1], job[2], job[3])


with open(os.path.join(DATA, "jobs.tsv"), encoding="utf-8") as f:
    jobs = [line_.split("\t") for line_ in f.read().split("\n")[:-1]]
for job in jobs:
    print("-- " + " ".join(job))
    try:
        run(job)
    except Exception as e:
        print(fail(e))
