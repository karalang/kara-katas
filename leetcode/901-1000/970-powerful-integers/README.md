# 970. Powerful Integers

Given three integers `x`, `y`, and `bound`, return a list of all the
powerful integers that have a value less than or equal to `bound`. An
integer is powerful if it can be represented as `x^i + y^j` for some
integers `i >= 0` and `j >= 0`. You may return the answer in any order.
In your answer, each value should occur at most once.

```
x = 2, y = 3, bound = 10  ->  [2,3,4,5,7,9,10]
x = 3, y = 5, bound = 15  ->  [2,4,6,8,10,14]
```

**Constraints:** `1 <= x, y <= 100`; `0 <= bound <= 10^6`.

## Approaches

| file | mechanism |
|---|---|
| `powerful_integers.kara` ★ | every pair of powers, in a set: the powers of x up to bound are 1, x, x^2, ... while they fit, and only 1 when x is 1; likewise for y. Every sum of one of each that is at most bound is powerful, and a `Set` keeps each sum once. Fewer than 20 powers of a base of 2 or more fit under 10^6, so at most 400 sums |
| `powerful_integers_sorted.kara` | no hashing: every sum goes into a `Vec`, which is sorted, and `dedup` then drops each value equal to the one before it |
| `powerful_integers_ordered.kara` | a `SortedSet`, a B-tree, keeps each sum once and hands them back in ascending order; the powers of y are made once and walked for every power of x until a sum passes bound |
| `powerful_integers_heap.kara` | the sums in order from a heap: with the powers of x and of y ascending, each row x^i + y^0, x^i + y^1, ... ascends, so a `PriorityQueue` holding the next sum of each row merges them into one ascending list, and a sum equal to the last one taken is a duplicate |
| `powerful_integers_merge.kara` | sorted rows merged two at a time: for each power a of x, the sums a + 1, a + y, a + y^2, ... up to bound form an ascending row, and the answer so far is merged with each row the way merge sort merges two runs, a value in both kept once. No hashing and no heap |
| `differential.kara` | the five arms against the statement read literally, six properties |

The arms return their values in different orders, so the harness sorts
them. Every arm prints the same 17 lines: LeetCode's two examples and
eight more (both bases 1 with bounds 1 and 2, a bound of 0, one base 1
on either side, equal bases, bases of 100 at LeetCode's largest bound,
where 100^3 is exactly 10^6, and bases 10 and 7); for every x and y from
1 to 100, with bounds 100 and 10^6, how many powerful integers there are
in all (39,080 and 220,633), their sum and a checksum of the sorted
lists; and five cases at bound 10^6, x = 2 with y = 3 (254 powerful
integers), 2 and 1, both bases 1, and x = 3 with y = 99.
`powerful_integers.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every v from 1 to bound for which some x^i below v leaves a
power of y, tested by dividing by y while it divides. It checks 3,200
random cases: 3,000 with bases up to 10 and bounds up to 200 against the
statement, and 200 with bases up to 100 (half of them up to 6) and
bounds up to 10^6 against the other properties; 36,225 powerful
integers in all. Every arm's answer is sorted before it is compared.

| | property |
|---|---|
| P1 | the statement's answer, on the small cases |
| P2 | strictly increasing once sorted, so each value once, and every value between 2 and bound and a power of x plus a power of y |
| P3 | the same answer with x and y swapped |
| P4 | the answer for half the bound is this answer's values up to it |
| P5 | 1 is a power of every base, and every power of x * x is a power of x, so the answers with y replaced by 1, with x replaced by 1, and with x replaced by x * x are all within this one |
| P6 | each arm agrees with at least two of the other four |

It prints `3200 cases: 36225 powerful integers, checksum 374354033,
95000 checks over 5 arms: 0 failures` under `karac __mir-run` (5.6 s)
and `karac __mir-llvm-run`, and the same under `karac __mir-llvm-asan`
with no error.

## Mutation testing

Thirty-three edits to the differential, each run under `karac
__mir-run` and `karac __mir-llvm-run`; fifteen are kept, three to each
arm, all fifteen are killed, and each fails the same checks under both.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: no power equal to its bound, so no sum equal to bound | P1 210, P4 312, P6 210 |
| M2 | ★: the powers of y up to the whole bound | P1 1205, P2 1258, P4 1239, P6 1258 |
| M3 | ★: the powers of x taken for y | P1 2610, P2 2348, P3 2823, P6 2799 |
| M4 | sorted: a power of x equal to bound - 1 left out | P1 58, P3 79, P4 89, P6 58 |
| M5 | sorted: duplicates kept | P1 860, P2 902, P6 902 |
| M6 | sorted: duplicates dropped before sorting | P1 781, P2 823, P3 82, P4 78, P6 823 |
| M7 | ordered: y = 2 given only the power 1 | P1 296, P3 578, P6 311 |
| M8 | ordered: y^0 left out | P1 2651, P3 2837, P5 2826, P6 2826 |
| M9 | ordered: the largest power of x left out | P1 2491, P3 2833, P4 1329, P5 84, P6 2672 |
| M10 | heap: only the first row | P1 2558, P3 2823, P6 2743 |
| M11 | heap: each row one short | P1 2386, P3 2807, P4 1196, P6 2555 |
| M12 | heap: every row from 1 | P1 2245, P2 2277, P3 2187, P4 1182, P6 2408 |
| M13 | merge: only the even powers of y | P1 2567, P3 2823, P6 2742 |
| M14 | merge: each row replacing the answer | P1 2564, P3 2819, P4 1404, P5 2749, P6 2749 |
| M15 | merge: x^0 left out | P1 2648, P3 2837, P5 2833, P6 2833 |

P1 and P6 kill all fifteen, P3 twelve (all but M1, M2 and M5), P4 eight
(M1, M2, M4, M6, M9, M11, M12, M14), P2 five (M2, M3, M5, M6, M12) and
P5 four (M8, M9, M14, M15). P3 misses the edits that treat x and y
alike. P2 sees only a value that is out of range, repeated, or not a sum
of powers; the commoner failure, a value missing, passes it. P5 sees a
missing value only when the smaller case still has it, so it catches
the edits that lose y^0, x^0 or the last power of x, and none of those
that lose a sum equal to bound, which every case loses alike.

Eighteen other edits were tried and set aside. Ten failed exactly the
same checks as a kept one: sorted, ordered and merge losing a sum equal
to bound, as M1; heap keeping duplicates, and merge keeping a value in
both runs twice or taking an equal value from the old run alone, as M5;
merge leaving out a power of x equal to bound - 1, as M4; merge taking
only the even powers of x, as M10; and sorted and merge leaving y^0 out,
as M8. Five were sound but beyond three an arm: ★ leaving out the
zeroth power and the last power that fits, sorted leaving x^0 out and
taking the powers of y + 1, and heap giving y = 2 only the power 1.
Three never finished and were not counted: sorted taking the powers of
x for y never stops when x is 1, appending sums until the memory runs
out; ordered taking the powers of y for x never stops when y is 1; and
sorted adding x where it should multiply runs up to half a million
rows for a bound of 10^6, which `karac __mir-llvm-run` finished
(failing P1, P2, P3 and P6) and `karac __mir-run` did not within 200 s.

## Verification

Every arm prints the same output as `powerful_integers.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and under
`karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `e04ae2b46b`, the runtime
archives rebuilt at the same commit. Under `karac __mir-run` the arms
take 0.40 s (sorted) to 3.4 s (heap), the ★ arm 0.85 s, and the
differential 5.6 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The legacy compiler was removed from kara at M3, so there is no legacy
lane.

## Benchmarks

The bench program runs the ★ arm for every x and y from 1 to 100 in
each of 100 rounds, the bound 10^6 less the round's number, and folds
every value into a count and a checksum of their squares, which does
not depend on the order a set hands them back in. Every implementation
prints `100 rounds over x and y from 1 to 100: 22063300 powerful
integers, checksum 509816852`. Kāra, Rust, Go and Python build a hash
set per call, Kāra's and Rust's under SipHash-1-3. C uses one
open-addressing table of 1,024 slots for every call, each slot stamped
with the call that filled it, so it neither clears nor allocates a table
per call; like the others it allocates its powers and its answer.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python, with karac at `e04ae2b46b`:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.19 to 0.30 s | 0.22 s |
| Rust (`rustc -O`) | 1.06 to 1.25 s | 1.16 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.02 to 1.22 s | 1.15 s |
| Go | 2.44 to 2.73 s | 2.66 s |
| Python | 7.1 s | |
| Kāra (`karac build --mir`) | 1.24 to 1.71 s | 1.33 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Python's run is about 33 times
C's.

v2 took 1.15 times Rust's median time under overflow checks and 6.1
times C's. Under valgrind's cachegrind v2 ran 13.3 billion instructions
and 1.90 billion branches with 82 million mispredicted, Rust with
overflow checks 11.2 billion, 1.04 billion and 37 million, and C 2.0
billion, 271 million and 9.3 million. The gap to C is the hash set the
other languages build, hash and free on every call, which C replaces
with one table it never clears.

