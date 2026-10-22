#!/usr/bin/env python3
r"""Writes data/jobs.tsv for mini_pyprimes (tab-separated: op then arg).

A stream of prime-number queries, each printing one line:

  nth <n>       the nth prime (1-based): nth_prime(n)
  first <n>     the first n primes, space-joined
  below <x>     every prime <= x, space-joined
  count <x>     how many primes are <= x (the prime-counting function pi(x))
  sum <n>       the sum of the first n primes
  isprime <n>   yes/no by exact trial division (isprime_division)
  factor <n>    prime factorisation as `p:count` pairs space-joined (factorise)
  factors <n>   the flat list of prime factors, space-joined

`factor`/`factors`/`isprime` take any integer: 0, 1 and -1 factor to themselves,
a negative number contributes a -1 factor, and `isprime` is false for n < 2.

mk.py writes only literal inputs (no library import); oracle.py replays every
job against the vendored `pyprimes` library. Inputs stay within the float-exact
range where the port's integer sqrt test matches the library. See README.md."""
import os

os.makedirs("data", exist_ok=True)

JOBS = [
    ("first", 15), ("nth", 1), ("nth", 10), ("nth", 100), ("nth", 500),
    ("below", 2), ("below", 30), ("below", 100), ("below", 1),
    ("count", 10), ("count", 100), ("count", 1000), ("count", 10000),
    ("sum", 9), ("sum", 49), ("sum", 100),
    ("isprime", -7), ("isprime", 0), ("isprime", 1), ("isprime", 2),
    ("isprime", 3), ("isprime", 4), ("isprime", 97), ("isprime", 561),
    ("isprime", 7919), ("isprime", 7920), ("isprime", 104729),
    ("isprime", 999983), ("isprime", 1000000), ("isprime", 100000007),
    ("factor", 0), ("factor", 1), ("factor", -1), ("factor", 2),
    ("factor", 12), ("factor", 360), ("factor", 1024), ("factor", -693),
    ("factor", 55614), ("factor", 999983), ("factor", 1000000),
    ("factor", 2 * 3 * 5 * 7 * 11 * 13), ("factor", 31607 * 70001),
    ("factors", -693), ("factors", 55614), ("factors", 1024),
    ("factors", 999983), ("factors", 5 * 5 * 5 * 7),
]

lines = ["%s\t%d" % (op, v) for op, v in JOBS]
with open("data/jobs.tsv", "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")
