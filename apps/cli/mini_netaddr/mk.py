#!/usr/bin/env python3
"""Writes data/jobs.tsv: one job per line, tab-separated <op>\t<arg>.

Multi-value args use `,` (merge / span / range endpoints) or `|` (exclude:
target|exclude). The set exercises netaddr's IPv4 CIDR algebra — cidr_merge,
spanning_cidr, iprange_to_cidrs, cidr_exclude and the glob<->CIDR conversions —
plus a few error paths.
"""
import os

JOBS = [
    ("net", "192.0.2.5/24"),
    ("net", "10.0.0.0/8"),
    ("net", "203.0.113.200/26"),
    ("merge", "192.0.2.0/24,192.0.3.0/24,10.0.0.1,10.0.0.2"),
    ("merge", "10.0.0.0/8,10.1.0.0/16,192.168.0.0/16"),
    ("merge", "192.0.2.0/25,192.0.2.128/25"),
    ("merge", "1.2.3.4,1.2.3.4,1.2.3.5"),
    ("span", "192.0.2.0/24,192.0.3.128/25"),
    ("span", "10.0.0.1,10.0.0.255,10.0.1.5"),
    ("span", "172.16.0.0/16,172.17.0.0/16,172.18.0.0/16"),
    ("range2cidr", "192.0.2.1,192.0.2.100"),
    ("range2cidr", "10.0.0.0,10.0.0.255"),
    ("range2cidr", "0.0.0.0,255.255.255.255"),
    ("range2cidr", "192.0.2.128,192.0.2.129"),
    ("exclude", "192.0.2.0/24|192.0.2.64/26"),
    ("exclude", "10.0.0.0/8|10.1.2.0/24"),
    ("exclude", "192.0.2.0/24|198.51.100.0/24"),
    ("glob2cidr", "192.0.2.0-31"),
    ("glob2cidr", "192.0.2.*"),
    ("glob2cidr", "10.0-1.*.*"),
    ("glob2cidr", "192.0.2.17-70"),
    ("cidr2glob", "192.0.2.0/24"),
    ("cidr2glob", "10.0.0.0/23"),
    ("cidr2glob", "192.0.2.128/26"),
    ("cidr2glob", "0.0.0.0/0"),
    ("glob2range", "10.0.*.*"),
    ("glob2range", "192.0.2.10-20"),
    ("range2glob", "192.0.2.1,192.0.3.254"),
    ("range2glob", "10.0.0.0,10.0.3.255"),
    ("validglob", "192.0.2.*"),
    ("validglob", "192.0.2.5-3"),
    ("validglob", "1.2.3.4-5"),
    ("validglob", "foo"),
    ("validglob", "1.2.3.4.5"),
    # error paths
    ("net", "not.an.ip/24"),
    ("glob2cidr", "1.2.3"),
    ("span", "10.0.0.1"),
]

os.makedirs("data", exist_ok=True)
with open("data/jobs.tsv", "w") as fh:
    for op, arg in JOBS:
        fh.write(op + "\t" + arg + "\n")
print("wrote data/jobs.tsv:", len(JOBS), "jobs")
