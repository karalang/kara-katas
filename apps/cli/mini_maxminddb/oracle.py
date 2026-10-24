#!/usr/bin/env python3
"""Runs data/jobs.txt against the real maxminddb 2.6.2 and geoip2 4.8.1
(the pure-Python Reader in MODE_MEMORY) and prints what mini_maxminddb.kara
must print. The libraries come from vendor/, or from MMDB_VENDOR.

Run: python3 -I -B oracle.py > expected.out"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.environ.get("MMDB_VENDOR", os.path.join(HERE, "vendor"))]

import ipaddress  # noqa: E402

import geoip2.database  # noqa: E402
import geoip2.errors  # noqa: E402
import maxminddb  # noqa: E402
from maxminddb.const import MODE_MEMORY  # noqa: E402


def exc(e):
    return f"{type(e).__name__}: {e}"


def show(v):
    return "-" if v is None else str(v)


def place(rec):
    """A place record as `name (iso)`, or `-`."""
    iso = getattr(rec, "iso_code", None)
    if rec.name is None and iso is None:
        return "-"
    return f"{show(rec.name)} ({show(iso)})" if iso is not None else show(rec.name)


def traits_text(t):
    flags = [k for k in ["is_anonymous_proxy", "is_anycast", "is_satellite_provider", "is_legitimate_proxy"]
             if getattr(t, k)]
    return f"ip {t.ip_address} network {t.network} flags {','.join(flags) or '-'}"


def country_lines(c):
    rep = c.represented_country
    out = [f"country {place(c.country)} eu={c.country.is_in_european_union} geoname={show(c.country.geoname_id)}",
           f"continent {show(c.continent.code)} {show(c.continent.name)}",
           f"registered {place(c.registered_country)}",
           f"represented {place(rep)} type={show(rep.type)}",
           f"traits {traits_text(c.traits)}"]
    return out


def city_lines(c):
    loc = c.location
    subs = c.subdivisions
    ms = subs.most_specific
    out = [f"city {show(c.city.name)} geoname={show(c.city.geoname_id)}",
           f"subdivision {place(ms)} of {len(subs)}" + "".join(f" / {s.iso_code}" for s in subs),
           f"location {show(loc.latitude)},{show(loc.longitude)} radius={show(loc.accuracy_radius)}"
           f" tz={show(loc.time_zone)} metro={show(loc.metro_code)}",
           f"postal {show(c.postal.code)}"]
    return out + country_lines(c)


def open_db(path):
    return maxminddb.open_database(path, MODE_MEMORY)


def job_meta(path):
    r = open_db(path)
    m = r.metadata()
    print(repr(m))
    print(f"node_byte_size={m.node_byte_size} search_tree_size={m.search_tree_size}")


def job_get(path, ip):
    r = open_db(path)
    rec, plen = r.get_with_prefix_len(ip)
    print(f"/{plen} {rec!r}")


def job_dump(path):
    r = open_db(path)
    n = 0
    for net, rec in r:
        print(f"{net} {rec!r}")
        n += 1
    print(f"{n} networks")


def job_networks(path):
    r = open_db(path)
    n = 0
    for net, rec in r:
        country = rec.get("country", {}).get("iso_code", "--")
        city = rec.get("city", {}).get("names", {}).get("en", "-")
        print(f"{net} {country} {city}")
        n += 1
    print(f"{n} networks")


def geo(path, locales):
    return geoip2.database.Reader(path, locales.split(","), mode=MODE_MEMORY)


def job_city(path, ip, locales):
    for ln in city_lines(geo(path, locales).city(ip)):
        print(ln)


def job_country(path, ip, locales):
    for ln in country_lines(geo(path, locales).country(ip)):
        print(ln)


def job_asn(path, ip, locales):
    a = geo(path, locales).asn(ip)
    print(f"AS{show(a.autonomous_system_number)} {show(a.autonomous_system_organization)}"
          f" network {a.network} ip {a.ip_address}")


def not_found(e):
    return f"not found ({e.network})"


def job_annotate(log):
    city = geo("city.mmdb", "en")
    asn = geo("asn.mmdb", "en")
    by_country = {}
    by_asn = {}
    unknown = 0
    with open(log) as f:
        lines = f.read().split("\n")
    for no, line in enumerate(lines, 1):
        if not line:
            continue
        ip = line.split(" ")[0]
        size = line.rsplit(" ", 1)[1]
        size = int(size)
        try:
            ipaddress.ip_address(ip)
        except ValueError as e:
            print(f"line {no}: {e}")
            continue
        try:
            c = city.city(ip)
            where = f"{show(c.country.iso_code)} {show(c.city.name)}"
            key = c.country.iso_code or "--"
        except geoip2.errors.AddressNotFoundError as e:
            where = not_found(e)
            key = "??"
            unknown += 1
        try:
            a = asn.asn(ip)
            who = f"AS{a.autonomous_system_number}"
            akey = a.autonomous_system_number
        except geoip2.errors.AddressNotFoundError:
            who = "AS?"
            akey = 0
        print(f"{no} {ip} {where} {who}")
        cnt = by_country.setdefault(key, [0, 0])
        cnt[0] += 1
        cnt[1] += size
        cnt = by_asn.setdefault(akey, [0, 0])
        cnt[0] += 1
        cnt[1] += size
    for k, (n, b) in sorted(by_country.items(), key=lambda kv: (-kv[1][0], kv[0])):
        print(f"country {k}: {n} requests, {b} bytes")
    for k, (n, b) in sorted(by_asn.items(), key=lambda kv: (-kv[1][0], kv[0]))[:6]:
        print(f"asn {k}: {n} requests, {b} bytes")
    print(f"{unknown} addresses not in the city database")


def parse_policy(path):
    rules = []
    with open(path) as f:
        for no, line in enumerate(f.read().split("\n"), 1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            words = line.split(" ")
            if words[0] not in ("allow", "deny", "default"):
                raise ValueError(f"policy line {no}: unknown action {words[0]!r}")
            rules.append((no, line, words))
    return rules


def matches(words, c, a):
    what = words[1]
    if what == "allow" or what == "deny":
        return True
    arg = words[2] if len(words) > 2 else ""
    if what == "country":
        return c is not None and c.country.iso_code == arg
    if what == "registered":
        return c is not None and c.registered_country.iso_code == arg
    if what == "represented":
        return c is not None and c.represented_country.type == arg
    if what == "continent":
        return c is not None and c.continent.code == arg
    if what == "asn":
        return a is not None and str(a.autonomous_system_number) == arg
    if what == "anycast":
        return c is not None and c.traits.is_anycast
    if what == "satellite":
        return c is not None and c.traits.is_satellite_provider
    if what == "unknown":
        return c is None
    raise ValueError(f"unknown condition {what!r}")


def job_firewall(policy, log):
    rules = parse_policy(policy)
    city = geo("city.mmdb", "en")
    asn = geo("asn.mmdb", "en")
    hits = {no: 0 for no, _, _ in rules}
    allowed = 0
    denied = 0
    with open(log) as f:
        lines = f.read().split("\n")
    for no, line in enumerate(lines, 1):
        if not line:
            continue
        ip = line.split(" ")[0]
        path = line.split('"')[1].split(" ")[1]
        try:
            ipaddress.ip_address(ip)
        except ValueError:
            print(f"line {no}: skipped, bad address {ip!r}")
            continue
        try:
            c = city.city(ip)
        except geoip2.errors.AddressNotFoundError:
            c = None
        try:
            a = asn.asn(ip)
        except geoip2.errors.AddressNotFoundError:
            a = None
        for rno, text, words in rules:
            if matches(words, c, a):
                hits[rno] += 1
                action = words[0] if words[0] != "default" else words[1]
                if action == "deny":
                    denied += 1
                    print(f"line {no}: deny {ip} {path} (rule {rno}: {text})")
                else:
                    allowed += 1
                break
    for rno, text, _ in rules:
        print(f"rule {rno} {text}: {hits[rno]}")
    print(f"{allowed} allowed, {denied} denied")


def main():
    os.chdir(os.path.join(HERE, "data"))
    with open("jobs.txt") as f:
        jobs = [ln.split("\t") for ln in f.read().split("\n") if ln]
    for job in jobs:
        print("== " + " | ".join(job))
        kind, args = job[0], job[1:]
        fn = {"meta": job_meta, "get": job_get, "dump": job_dump, "networks": job_networks, "city": job_city,
              "country": job_country, "asn": job_asn, "annotate": job_annotate, "firewall": job_firewall}[kind]
        try:
            fn(*args)
        except Exception as e:  # noqa: BLE001
            print(exc(e))


main()
