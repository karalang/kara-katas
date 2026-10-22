#!/usr/bin/env python3
r"""Replays data/jobs.tsv against the vendored `pyprimes` library and writes
expected.out. See mk.py for the op grammar.

Only the library's deterministic surface is used: nth_prime, nprimes,
primes_below, prime_count, primesum, isprime_division and factorise. The
probabilistic isprime and the base-dependent fermat/miller_rabin are not
exercised. mini_pyprimes.kara reproduces this byte-for-byte."""
import sys

sys.path.insert(0, "vendor")
import pyprimes  # noqa: E402

out = []
for line in open("data/jobs.tsv", encoding="utf-8").read().split("\n"):
    if not line:
        continue
    op, _, arg = line.partition("\t")
    v = int(arg)
    if op == "nth":
        out.append(str(pyprimes.nth_prime(v)))
    elif op == "first":
        out.append(" ".join(str(p) for p in pyprimes.nprimes(v)))
    elif op == "below":
        out.append(" ".join(str(p) for p in pyprimes.primes_below(v)))
    elif op == "count":
        out.append(str(pyprimes.prime_count(v)))
    elif op == "sum":
        out.append(str(pyprimes.primesum(v)))
    elif op == "isprime":
        out.append("yes" if pyprimes.isprime_division(v) else "no")
    elif op == "factor":
        out.append(" ".join("%d:%d" % (p, c) for p, c in pyprimes.factorise(v)))
    elif op == "factors":
        out.append(" ".join(str(p) for p in pyprimes.factors(v)))
    else:
        raise SystemExit("unknown op %r" % op)

sys.stdout.write("\n".join(out) + "\n")
