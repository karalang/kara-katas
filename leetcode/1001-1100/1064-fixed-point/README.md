# 1064. Fixed Point

Given an array of distinct integers `arr` sorted in ascending order,
return the smallest index `i` with `arr[i] == i`, or `-1` if there is
none.

```
arr = [-10, -5, 0, 3, 7]      ->  3
arr = [0, 2, 5, 8, 17]        ->  0
arr = [-10, -5, 3, 4, 7, 9]   ->  -1
```

**Constraints:** `1 <= arr.length < 10^4`; `-10^9 <= arr[i] <= 10^9`.

The numbers are distinct integers in ascending order, so each is at least
one more than the last and `arr[i] - i` never falls. The fixed points are
where it is 0, one run of indices, and the answer is the first index
where it is not below 0, if it is 0 there. A binary search finds it in
O(log n).

## Approaches

| file | mechanism |
|---|---|
| `fixed.kara` ★ | a binary search for the first index whose number is not below it, then one comparison. O(log n) |
| `fixed_scan.kara` | every index in order, the first whose number is the index (`arr.iter().enumerate().find(..)`). O(n) |
| `fixed_partition.kara` | the numbers less their indices, then the library's binary search, `partition_point(\|d\| d < 0)`. O(n) to build the differences, O(log n) to search them |
| `fixed_recursive.kara` | divide and conquer: a number below its index at the middle rules out the left half; otherwise the left half is searched first. O(log n) |
| `fixed_walk.kara` | a walk from the front to the first number not below its index. O(n) |
| `fixed_solution.kara` | LeetCode's Rust template (`struct Solution;`, `Vec<i32>`, `let (mut lo, mut hi) = (0usize, ..)`, `&&`, `mid as i32`, `Solution::`), carried to Kāra by `karac fix`. O(log n) |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 17 lines: the answers for LeetCode's three
examples and seven more; the sum and a checksum of the answers for 3000
arrays of 1 to 12 numbers and 300 of 50 to 300; and the answers for
10000 numbers each its own index (0), each one past it (-1), meeting
their indices only at the end (9999), far apart (-1), and at random.
`fixed.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the indices in order, the first whose number is the index, or
-1. It checks 2000 arrays: 1000 of 1 to 12 numbers starting at most 5
from 0 with steps of 1 to 3, and 1000 of 1 to 40 starting at most 20 from
0 with steps of 1 to 4. 748 of them have a fixed point. Every random
choice of a problem is drawn before any arm answers, so a wrong arm
cannot change the problems the others see.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer is -1, or an index whose number is the index |
| P3 | every number raised by one, behind a negative number below them, moves the answer one index later |
| P4 | a number above every one and above the length, appended at the end, leaves the answer |
| P5 | the array cut in two: the front answers the answer when it falls before the cut and -1 otherwise; the back, every number lowered by the cut, answers the answer less the cut when it falls at or after the cut, -1 when there is none, and otherwise -1 or 0 |
| P6 | each arm agrees with at least three of the other five |

The differential prints `2000 problems: checksum 723180775, 84000 checks
over 6 arms: 0 failures` under every lane in Verification; a Python
reading of the same 2000 arrays gives the same checksum. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Thirty edits to the differential, five to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. Fifteen are kept, two or three to
each arm. All thirty are killed, each fails the same way under both
backends, none by a crash, and no two kept ones fail the same checks. Two
first edits survived and were replaced, both equivalent: the ★ search's
upper bound one short (`arr.len() - 1`) and the walk stopping before the
last index. Each stops at the last index instead of past it, and the
check after the search compares that index's number, which is below it
when nothing earlier qualified.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a fixed point searched past (`arr[mid] <= mid`) | P1 748, P6 748 |
| M2 | ★: the middle dropped with the right half | P1 149, P3 399, P4 104, P5 141, P6 149 |
| M3 | ★: a number one below its index taken as not below | P1 249, P3 117, P5 33, P6 249 |
| M4 | scan: the first number not below its index | P1 934, P2 934, P4 318, P6 934 |
| M5 | scan: the last fixed point | P1 357, P5 125, P6 357 |
| M6 | scan: no fixed point answered 0 | P1 1252, P2 1252, P3 1252, P5 376, P6 1252 |
| M7 | partition: each difference one short | P1 1073, P2 689, P4 181, P6 1073 |
| M8 | partition: the last index never answered | P1 56, P4 56, P5 79, P6 56 |
| M9 | recursive: the right half never searched | P1 183, P3 124, P4 52, P5 102, P6 183 |
| M10 | recursive: the left half never searched | P1 652, P3 142, P4 173, P5 322, P6 652 |
| M11 | recursive: the middle preferred to the left half | P1 314, P3 183, P4 120, P5 241, P6 314 |
| M12 | walk: from index 1 | P1 415, P3 415, P5 122, P6 415 |
| M13 | walk: two at a time | P1 179, P3 748, P5 66, P6 179 |
| M14 | solution: no fixed point answered by where it would go | P1 1252, P2 1252, P5 656, P6 1252 |
| M15 | solution: each number one higher crossing to `i32` | P1 943, P2 444, P3 437, P6 943 |

P1 and P6 kill all fifteen, P5 eleven, P3 nine, P4 seven and P2 five. P2
sees an answer whose number is not its index (M4, M6, M7, M14, M15). P3's
moved array shifts every index by one and puts a new number at 0, so it
sees the edits that treat index 0, an index's parity or the split of a
range unevenly (M2, M3, M6, M9 to M13, M15). P5's cut catches the edits that answer a fixed point
other than the first (M5, M11) and the ones that lose the end of the
array (M8). M1 is caught only by the literal reading and the vote: it
answers -1 for every array with a fixed point, and every property but P1
reads -1 as consistent, since an array with none keeps none under each
change.

Of the fifteen not kept, the ★ arm taking the first number not below its
index unchecked fails as M4, as do the partition arm taking any
difference not below 0 and the walk taking where it stops unchecked. The
partition search past the zeros, the walk past fixed points and the
solution's `<=` fail as M1, the recursive arm leaving out index 0 and the
scan skipping it as M12, and the walk stopping at a number one below its
index as M3. The ★ search leaving out the last index, the scan taking a
number one above its index, the partition's differences reversed, the
recursive right half searched from one past its start, the solution
stopping one step early and the solution searching only the first half
each fail in a way of their own.

## Verification

Every arm prints the same output as `fixed.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any file. Under `karac __mir-run` the arms take 0.3 s to 0.6 s and the
differential 1.8 s.

The Rust arm was written as LeetCode's Rust template and reaches a clean
check through `karac fix` in two rounds: the syntax (`struct Solution
{}`, `Vec[i32]`, `let mut (lo, hi)`, `and`, `Solution.`), then the
`0usize` suffix and the bridge's `as i64` the widening return no longer
needs. Nothing was left by hand.

## Benchmarks

The bench builds 8 sorted arrays of 1000000 distinct numbers once, in
all five languages, each starting 100000 lower than the last and rising by
1 or 2, then answers each on its first 500000 suffixes with the ★ arm's
binary search: 4000000 calls of about 20 steps each. Rust searches
`&arr[p..]` with `usize` indices, Go a slice, C a pointer and a length,
and Python passes the start instead, since a slice copy would cost more
than the search. Every implementation prints `4000000 calls: 1566566
found, checksum 552226380`.

Timings on a 4-core container, twelve interleaved runs of each compiled
program and one of Python, with kara `3565136cc1` on LLVM 22:

| | time | median |
|---|---|---|
| Rust (`rustc -O -C overflow-checks=on`) | 0.176 to 0.238 s | 0.186 s |
| Rust (`rustc -O`) | 0.178 to 0.213 s | 0.187 s |
| C (`clang -O3`) | 0.207 to 0.227 s | 0.218 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.286 to 0.446 s | 0.300 s |
| Kāra (`karac build`) | 0.282 to 0.453 s | 0.303 s |
| Go | 0.327 to 0.372 s | 0.341 s |
| Python | 9.9 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time (0.273 s) is below its real time.

Kāra takes 1.61x the time of Rust under overflow checks, and all of the
gap is the midpoint. Building the arrays takes 0.044 s in both. Written
`(lo + hi) / 2`, the same program runs in 0.189 s, and written `lo + ((hi
- lo) >> 1)` in 0.197 s. Kāra halves a sum of non-negative values with a
shift, but not `hi - lo`, which is non-negative only under the loop's `lo
< hi`, so the search keeps a signed division's sign fixup, the overflow
branch on `lo + half` and the index check against the length. That is
kara B-2026-11-08-1 (open). The kata keeps `lo + (hi - lo) / 2`, the
overflow-safe form the problem's references and LeetCode's Rust template
write.
