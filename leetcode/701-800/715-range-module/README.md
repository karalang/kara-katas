# 715. Range Module

A Range Module is a module that tracks ranges of numbers. Design a data
structure to track the ranges represented as half-open intervals and
query about them. A half-open interval `[left, right)` denotes all the
real numbers `x` where `left <= x < right`.

`RangeModule()` makes an empty module. `addRange(left, right)` adds the
half-open interval, tracking every number in it, including those already
tracked. `queryRange(left, right)` returns true if every number in
`[left, right)` is currently tracked. `removeRange(left, right)` stops
tracking every number in `[left, right)` that is currently tracked.

```
addRange(10, 20); removeRange(14, 16)
queryRange(10, 14)  ->  true
queryRange(13, 15)  ->  false   (14 and 15 are no longer tracked)
queryRange(16, 17)  ->  true
```

**Constraints:** 1 <= `left` < `right` <= 10^9; at most 10^4 calls in
all.

## Approaches

Three arms keep the tracked numbers as the fewest disjoint ranges, so no
two ranges overlap or touch; they differ in how those ranges are stored
and found. The fourth keeps no ranges at all.

| file | mechanism |
|---|---|
| `range_module.kara` ★ | the ranges' starts and ends in two parallel sorted lists; a binary search on the ends finds the first range a call reaches, adding merges every range it overlaps or touches into one, removing trims or splits the ranges it meets, and inserts and removals shift the rest of the list |
| `range_module_sorted.kara` | the ranges in a `SortedMap` from start to end; `floor` finds the range that starts at or before a number and `range` walks the ranges that start inside a span |
| `range_module_rebuild.kara` | the ranges as a list of (start, end) pairs, rebuilt by one pass on every change, and scanned by a query; O(n) per call |
| `range_module_tree.kara` | a segment tree over [0, 2^30), each node empty, full or mixed, whose two halves are made only when a call first cuts it; O(log C) per call |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 11 lines: the LeetCode example; two ranges
that touch, merged, and a removal that splits them; removals that trim
both ends of a range and one from its middle; four ranges bridged by one
add; removals outside a range, then of everything; calls on an empty
module, and a gap filled and opened again; the problem's widest range
with one number taken out; and four sets of 10,000 random calls, with
spans anywhere up to 10^9, numbers up to 100, short spans up to 10^6 and
spans of up to 10^6 anywhere up to 10^9, each printing its number of
queries, how many held, and a checksum. `range_module.py` mirrors the ★
arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
which keeps one flag for every number, sets or clears the flags of a
span one by one, and answers a query by reading every flag in it.
3,000 random sequences of up to 30 calls are checked, each on numbers
from 1 to between 2 and 24, so ranges overlap, touch and nest often.

| | property |
|---|---|
| P1 | every query answers as the definition does |
| P2 | after the calls, a query of every span from 1 to the top answers as the definition does |
| P3 | every number raised by the same amount, up to 9 * 10^8, gives the same answers |
| P4 | every span reflected, x to top + 1 - x, gives the same answers |

It prints `3000 call sequences (13552 queries), 4 arms, 48000 checks,
0 failures` under `karac __mir-run` and `karac __mir-llvm-run`, and the
same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed. Three more edits, E1 to
E3, change nothing that can be seen, and the differential rightly
reports no failure for them.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a range ending at left not merged | P1 63, P2 204, P4 106 |
| M2 | ★: a range starting at right not merged | P1 54, P2 189, P4 106 |
| M3 | ★: a query ending where the range ends refused | P1 773, P2 2561, P4 878 |
| M4 | sorted: a range ending at left not merged | P1 61, P2 197, P4 103 |
| M5 | sorted: a range starting at the merged end not merged | P1 57, P2 197, P4 115 |
| M6 | sorted: a range starting at left not removed | P1 335, P2 826, P4 435 |
| M7 | rebuild: a range ending at left not merged | P1 57, P2 193, P4 102 |
| M8 | rebuild: a query starting where the range starts refused | P1 827, P2 2554, P4 878 |
| M9 | rebuild: a tail of one number dropped by a remove | P1 51, P2 369, P4 101 |
| M10 | tree: an empty node not handing its state down | P1 132, P2 618, P3 137, P4 130 |
| M11 | tree: a node outside the query counted as not held | P1 1556, P2 2607 |
| M12 | tree: a whole node handing its state to one half only | P1 239, P2 841, P3 221, P4 368 |
| E1 | rebuild: a range touching the removed span trimmed instead of copied | 0 |
| E2 | sorted: an empty range left where a removal ends a range | 0 |
| E3 | tree: two mixed halves collapsed to mixed by the same test | 0 |

P1 and P2 kill all twelve. P4 kills all but M11: reflecting the spans
turns a mistake at a range's left edge into one at its right, and the
arms handle the two edges with different code. P3 sees only the tree's
mutants, M10 and M12, since raising every number moves the spans across
the tree's node boundaries, where for the three list arms it changes
nothing. M11 counts the part of the tree outside a query as not held, so
every query that is not the whole tree answers false; reflected or
raised, they all answer false again, which is why only P1 and P2 see it.
E1 sends a range that only touches the removed span to the trimming
branch, which keeps it whole. E2 leaves an empty range where a removal
ends a range: no query can be held by it, the next add or removal that
reaches it takes it away, and where `floor` finds it instead of the
range before it, that range ends before it and could not have answered
either. E3 also collapses two mixed halves, which leaves the node mixed
as before.

## Verification

Every arm prints the same output as `range_module.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The debug build that
runs `__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` and the
release build that runs `check` and `__mir-run` are both at kara
`9ddda04add`, whose last compiler change is `fa73802a05`. No
`runtime/src` change has landed since the runtime archives were built.

The sanitizer lane cannot see a leak (kara B-2026-10-18-31), so the leak
check copied each arm's and the differential's lane executable as it was
linked and ran it with the preloaded shim from kata 708, which refuses
the lane's hand-made stack so that LeakSanitizer sees `main` (kata
708 showed it reporting a leak the lane misses): all five print their
output and report no leak.

The frozen legacy backends refuse all four arms, the differential and
the bench program at type checking: the ★ and tree arms and the bench
program at `next_random(mut seed)` inside `random_below`, whose argument
is already a `mut ref`, where legacy wants the marker dropped and
design.md § Call-site `mut` markers now requires it (kara
B-2026-10-14-25); the rebuild arm at `*span` over `iter()` and the
sorted-map arm at `*e` on what `floor` finds, since legacy gives those
by value where v2 gives references; and the differential at both. Legacy
is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages: C has no sorted
map, so the sorted-map arm could not be the same algorithm in all of
them. It makes ten lists of 100,000 random calls once, a third of each
kind, on numbers up to 10^7 with spans of up to 10^4, and runs each list
on a fresh module in 10 rounds, counting the queries that hold. Once
settled, a module holds about 1,000 ranges. Every implementation prints
`10 rounds of 10 lists of 100000 calls: 700760 queries held`, the Kāra
program under `karac __mir-run` included (in 59 s).

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and three of Python (`bench.sh`
timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.79 to 1.06 s |
| Rust (`rustc -O`) | 0.79 to 1.07 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.80 to 1.10 s |
| Go | 1.34 to 1.49 s |
| Python | 9.7 to 11.0 s |
| Kāra (`karac build --mir`) | 0.83 to 1.07 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend; the legacy `karac build` refuses it (above). That
edit is by hand, on top of the `scripts/new-bench.sh` output. Under
`karac __mir-llvm-run` the program prints the same line in 2.8 s,
compile included; that JITs the MIR's IR without optimization passes, so
it is not a benchmark.

So the v2 build is level with C and Rust, and Go trails. Under
valgrind's cachegrind C and Rust run 3.85 billion instructions and the
v2 build 4.41, and all three mispredict 80 to 86 million branches: where
a binary search turns depends on the data, so those misses, which every
implementation shares, appear to set the time. That reading is inferred
from the counts, not traced. The comparison with C and Rust waits until
after M4.

## Compiler findings

None new.
