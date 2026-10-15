# The reference: the same program written with Python 3.13's ipaddress.
import ipaddress
from ipaddress import (IPv4Address, IPv6Address, IPv4Network, IPv6Network,
                       ip_address, ip_network, ip_interface, collapse_addresses,
                       summarize_address_range)
from itertools import islice


def lines(path):
    return open(path, encoding="utf-8").read().splitlines()


FLAGS = ["private", "global", "multicast", "loopback", "link_local",
         "reserved", "unspecified", "site_local"]


def flags(x):
    on = [f for f in FLAGS if getattr(x, "is_" + f, False)]
    return " ".join(on) if on else "-"


def err(e):
    return f"{type(e).__name__}: {e}"


def show_addresses():
    print("== addresses")
    for s in lines("data/addresses.txt"):
        print(repr(s))
        try:
            a = ip_address(s)
        except ValueError as e:
            print(f"  {err(e)}")
            for cls in (IPv4Address, IPv6Address):
                try:
                    cls(s)
                except ValueError as e:
                    print(f"  {cls.__name__}: {err(e)}")
            continue
        print(f"  {a!r} v{a.version} int={int(a)}")
        print(f"  exploded={a.exploded} compressed={a.compressed}")
        print(f"  reverse={a.reverse_pointer}")
        print(f"  packed={a.packed!r}")
        print(f"  {flags(a)}")
        if a.version == 6:
            for name in ("ipv4_mapped", "sixtofour", "teredo", "scope_id"):
                v = getattr(a, name)
                if v is not None:
                    print(f"  {name}={v!r}")


def show_networks():
    print("== networks")
    for line in lines("data/networks.txt"):
        s, _, mode = line.partition(" ")
        strict = mode != "loose"
        print(repr(line))
        try:
            n = ip_network(s, strict)
        except ValueError as e:
            print(f"  {err(e)}")
            for cls in (IPv4Network, IPv6Network):
                try:
                    cls(s, strict)
                except ValueError as e:
                    print(f"  {cls.__name__}: {err(e)}")
            continue
        print(f"  {n!r} prefixlen={n.prefixlen} num_addresses={n.num_addresses}")
        print(f"  netmask={n.netmask} hostmask={n.hostmask}")
        print(f"  with_netmask={n.with_netmask} with_hostmask={n.with_hostmask}")
        print(f"  network={n.network_address} broadcast={n.broadcast_address} last={n[-1]}")
        print(f"  hosts={' '.join(str(h) for h in islice(n.hosts(), 3))}")
        try:
            print(f"  exploded={n.exploded}")
        except ValueError as e:
            # CPython re-parses str(network_address), which carries the scope
            print(f"  exploded: {err(e)}")
        print(f"  {flags(n)}")
        print(f"  supernet={n.supernet()} subnets={' '.join(str(x) for x in islice(n.subnets(), 2))}")


def addr_or_net(s):
    return ip_network(s) if "/" in s else ip_address(s)


def op(words):
    cmd = words[0]
    if cmd == "subnets":
        n = ip_network(words[1])
        subs = list(n.subnets(new_prefix=int(words[2])))
        for x in subs[:4]:
            print(f"  {x}")
        if len(subs) > 4:
            print(f"  ... {subs[-1]}")
        print(f"  ({len(subs)} subnets)")
    elif cmd == "supernet":
        print(f"  {ip_network(words[1]).supernet(prefixlen_diff=int(words[2]))}")
    elif cmd == "exclude":
        for x in ip_network(words[1]).address_exclude(ip_network(words[2])):
            print(f"  {x}")
    elif cmd == "collapse":
        print(f"  {' '.join(str(x) for x in collapse_addresses(addr_or_net(w) for w in words[1:]))}")
    elif cmd == "summarize":
        r = summarize_address_range(ip_address(words[1]), ip_address(words[2]))
        print(f"  {' '.join(str(x) for x in r)}")
    elif cmd == "contains":
        print(f"  {ip_address(words[2]) in ip_network(words[1])}")
    elif cmd == "overlaps":
        print(f"  {ip_network(words[1]).overlaps(ip_network(words[2]))}")
    elif cmd == "subnet_of":
        print(f"  {ip_network(words[1]).subnet_of(ip_network(words[2]))}")
    elif cmd == "sort":
        print(f"  {' '.join(str(x) for x in sorted(ip_network(w) for w in words[1:]))}")
    elif cmd == "add":
        print(f"  {ip_address(words[1]) + int(words[2])!r}")
    elif cmd == "interface":
        i = ip_interface(words[1])
        print(f"  {i!r} ip={i.ip} network={i.network}")
        print(f"  with_prefixlen={i.with_prefixlen} with_netmask={i.with_netmask} with_hostmask={i.with_hostmask}")
        print(f"  exploded={i.exploded}")
    elif cmd == "format":
        print(f"  {format(ip_address(words[1]), words[2])}")


def show_ops():
    print("== operations")
    for line in lines("data/ops.txt"):
        print(f"> {line}")
        try:
            op(line.split())
        except (ValueError, TypeError) as e:
            print(f"  {err(e)}")


# ------------------------------------------------------------ IPAM

class Space:
    def __init__(self, version):
        self.version = version
        self.pools = []
        self.free = []

    def add_free(self, nets):
        self.free = list(collapse_addresses(self.free + nets))


def show_plan():
    print("== plan")
    spaces = {4: Space(4), 6: Space(6)}
    allocs = {}

    def take(name, net):
        sp = spaces[net.version]
        for b in sp.free:
            if net.subnet_of(b):
                sp.free.remove(b)
                sp.add_free(list(b.address_exclude(net)))
                allocs[name] = net
                return True
        return False

    def show():
        for v in (4, 6):
            sp = spaces[v]
            print(f"  IPv{v}:")
            for p in sp.pools:
                inside = sorted((n, name) for name, n in allocs.items()
                                if n.version == v and n.subnet_of(p))
                used = sum(n.num_addresses for n, _ in inside)
                print(f"    pool {p}: {used}/{p.num_addresses} used ({used * 100 // p.num_addresses}%)")
                for n, name in inside:
                    print(f"      {n} {name}")
                for b in sp.free:
                    if b.subnet_of(p):
                        print(f"      {b} free")

    for line in lines("data/plan.txt"):
        w = line.split()
        if w[0] == "pool":
            n = ip_network(w[1])
            spaces[n.version].pools.append(n)
            spaces[n.version].add_free([n])
            print(f"pool {n} ({n.num_addresses} addresses)")
        elif w[0] == "reserve":
            name, n = w[1], ip_network(w[2])
            clash = [(o, nm) for nm, o in allocs.items() if o.version == n.version and o.overlaps(n)]
            if clash:
                print(f"reserve {name}: {n} overlaps {clash[0][1]} ({clash[0][0]})")
            elif take(name, n):
                print(f"reserve {name} {n}")
            else:
                print(f"reserve {name}: {n} is outside every pool")
        elif w[0] == "alloc":
            name, v, p = w[1], int(w[2][1:]), int(w[3][1:])
            if not 0 <= p <= (32 if v == 4 else 128):
                print(f"alloc {name}: /{p} is not a valid IPv{v} prefix")
                continue
            sp = spaces[v]
            fits = [b for b in sp.free if b.prefixlen <= p]
            if not fits:
                print(f"alloc {name}: no free /{p} in the IPv{v} pools")
                continue
            best = max(b.prefixlen for b in fits)
            block = [b for b in fits if b.prefixlen == best][0]
            net = next(block.subnets(new_prefix=p))
            take(name, net)
            print(f"alloc {name} {net} (from {block})")
        elif w[0] == "free":
            name = w[1]
            if name not in allocs:
                print(f"free {name}: no such allocation")
                continue
            n = allocs.pop(name)
            spaces[n.version].add_free([n])
            print(f"free {name} {n}")
        elif w[0] == "show":
            print("show")
            show()
    return allocs


# ------------------------------------------------------------ the firewall

def parse_ports(s):
    if s == "any":
        return None
    out = []
    for part in s.split(","):
        lo, _, hi = part.partition("-")
        out.append((int(lo), int(hi or lo)))
    return out


def ports_str(p):
    if p is None:
        return "any"
    return ",".join(str(a) if a == b else f"{a}-{b}" for a, b in p)


def endpoint(s, allocs):
    if s == "any":
        return None
    if s.startswith("@"):
        if s[1:] not in allocs:
            raise ValueError(f"no allocation named {s[1:]!r}")
        return allocs[s[1:]]
    return ip_network(s)


def split_hostport(s):
    if s.startswith("["):
        host, sep, port = s[1:].partition("]:")
    else:
        host, sep, port = s.rpartition(":")
    if not sep:
        raise ValueError(f"no port in {s!r}")
    return ip_address(host), int(port)


def hostport(a, port):
    return f"[{a}]:{port}" if a.version == 6 else f"{a}:{port}"


def show_firewall(allocs):
    print("== firewall")
    rules = []
    k = 0
    for line in lines("data/acl.txt"):
        if line.startswith("#"):
            continue
        k += 1
        w = line.split()
        try:
            src, dst = endpoint(w[2], allocs), endpoint(w[3], allocs)
        except ValueError as e:
            print(f"rule {k}: {err(e)}, skipped")
            continue
        rule = (k, w[0], w[1], src, dst, parse_ports(w[4]))
        rules.append(rule)
        print(f"rule {k}: {w[0]} {w[1]} {src or 'any'} -> {dst or 'any'} ports {ports_str(rule[5])}")
    hits = {}
    denied = {4: [], 6: []}
    for line in lines("data/conns.txt"):
        proto, s, _, d = line.split()
        try:
            src, sport = split_hostport(s)
            dst, dport = split_hostport(d)
        except ValueError as e:
            print(f"  error   {line}: {err(e)}")
            continue
        verdict, which = "deny", "-"
        for (k, action, rproto, rsrc, rdst, rports) in rules:
            if rproto not in ("any", proto):
                continue
            if rsrc is not None and src not in rsrc:
                continue
            if rdst is not None and dst not in rdst:
                continue
            if rports is not None and not any(a <= dport <= b for a, b in rports):
                continue
            verdict, which = action, str(k)
            break
        hits[which] = hits.get(which, 0) + 1
        scope = "global" if src.is_global else "private" if src.is_private else "shared"
        print(f"  {verdict:<7} rule {which} {proto} {hostport(src, sport)} -> {hostport(dst, dport)} ({scope})")
        if verdict == "deny" and src.is_global:
            denied[src.version].append(src)
    print("hits: " + " ".join(f"{k}={v}" for k, v in sorted(hits.items())))
    for v in (4, 6):
        print(f"blocklist v{v} (global sources): {' '.join(str(x) for x in collapse_addresses(denied[v])) or '-'}")


show_addresses()
show_networks()
show_ops()
show_firewall(show_plan())
