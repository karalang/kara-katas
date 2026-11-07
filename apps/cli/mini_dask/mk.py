"""Writes data/ for mini_dask: a script for a small task graph with values,
calls, chains to fuse, fan-in, failures upstream of other keys, type and
overflow errors, persisting, dropping, a cycle and a missing dependency,
with a few mistakes.

Run from this directory: python3 -s -P -B mk.py"""
import os

os.makedirs("data", exist_ok=True)


def put(name, text):
    with open(os.path.join("data", name), "w", encoding="utf-8", newline="") as fh:
        fh.write(text)


put("script.txt", """\
# Two inputs, a chain of calls on one of them, and a fan-in.
value x 10
value y 3
task a inc x
task b mul a 2
task c neg b
task d add c y 100
task e div d y
task back div -7 2

# Lists, and two CPU-heavy calls the workers can share.
task r range 20
task big range 5000
task s sum r
task l len big
task both concat r r big
task n len both
task p1 primes 150000
task p2 primes 250000
task p3 primes 100000
task ptot add p1 p2 p3

# Failures, and what lies downstream of them.
task zero div x 0
task after inc zero
task later add after s
task wrong sum x
task m1 mul 999999999 999999999
task m2 mul m1 10
task m3 inc m2
task tail add m3 wrong
@ graph

compute d
compute --nofuse d
compute e back s l n
compute ptot d
compute later e
compute tail m1 r
compute big both
task oddly inc r
task kaboom boom
task huge range 100001
task lots primes 2000001
value minus -5
task flip neg minus
compute oddly kaboom huge lots flip
@ deps later
@ dependents s

persist e s
@ graph
compute later d e
drop s
compute later
@ deps later
task s range 4
compute later
persist big
compute n

# A cycle and a missing input.
task cy1 inc cy2
task cy2 inc cy3
task cy3 inc cy1
task top add x cy1
compute top
task self inc self
compute self
task needs add ghost 1
compute needs
compute x
persist x y
compute r --nofuse r

# Mistakes, each reported and skipped.
value x 5
value Bad 1
value z 1234567890
value z
task q
task q sqrt x
task q inc x y
task q add 1
task q boom 1
task q inc Bad-Arg
task q mul 1 12345678901
task 9q inc 1
compute
compute --fast x
compute nowhere
compute x x
persist
drop
drop ghost
frobnicate
@
@ graph x
@ deps
@ dependents ghost
@ frob
""")
