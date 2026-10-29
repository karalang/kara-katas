# 1013. Partition Array Into Three Parts With Equal Sum

Given an array of integers `arr`, return `true` if it can be split into
three non-empty parts with equal sums: indexes `i + 1 < j` with

```
arr[0] + ... + arr[i] == arr[i + 1] + ... + arr[j - 1] == arr[j] + ... + arr[n - 1]
```

```
arr = [0,2,1,-6,6,-7,9,1,2,0,1]  ->  true    (0+2+1 == -6+6-7+9+1 == 2+0+1)
arr = [0,2,1,-6,6,7,9,-1,2,0,1]  ->  false
arr = [3,3,6,5,-2,2,5,1,-9,4]    ->  true    (3+3 == 6 == 5-2+2+5+1-9+4)
```

**Constraints:** `3 <= arr.length <= 5 * 10^4`, `-10^4 <= arr[i] <= 10^4`.

## Approaches

Each part holds a third of the total, so the total must divide by 3 and
the cuts sit after prefixes of one third and two thirds. The arms
differ in how they find, or count, such a pair of cuts.

| file | mechanism |
|---|---|
| `three_parts.kara` ★ | two cuts: the first part ends at the first prefix reaching a third, the second at the first later prefix reaching two thirds, before the last element. O(n) |
| `three_parts_ends.kara` | both ends: the first part grows from the front and the last from the back until each sums to a third, each leaving the other room; the split exists when both reached it with a value between them. O(n) |
| `three_parts_count.kara` | counting parts: cut greedily whenever the running part reaches a third and start the next empty; three or more parts make a split, the leftovers summing to zero. O(n) |
| `three_parts_ways.kara` | counting ways: every second cut, after a prefix of two thirds, pairs with each earlier first cut, after a prefix of a third; the array splits when there is at least one way. O(n) |
| `three_parts_map.kara` | prefix maps: where each prefix sum is first reached and where it is last reached before the final element; a split is the earliest third before the latest two thirds. O(n) expected |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 20 lines: LeetCode's three examples and ten
more (three zeros, four zeros, `[1,-1,1,-1]`, `[1,-1,0,0]`, `[1,1,1]`,
`[1,2,3]`, `[6,0,0]`, `[2,2,2,-2,2]`, LeetCode's extreme values
alternating, and `[1,2,-3,3,0,0,3,-6,6]`); how many of 3,000 random
arrays of 3 values, 3,000 of 8, 1,000 of 60, 200 of 1,000 and twice 6
of LeetCode's largest 50,000 split, with a checksum of the answers in
order; and 1,000 arrays built from three parts with equal sums, all of
which split, then the same arrays with one value moved by three, of
which 92 do. `three_parts.py` mirrors the ★ arm and its output is
byte-identical.

The two cuts can share a place only when the total is zero, a third
and two thirds being the same prefix then; several mutants below live
on that one case, and the examples with zero totals pin it.

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: every pair of cuts, each of the three parts summed on
its own, counting the pairs whose sums agree. It checks 4,984 arrays:
every array of 3 to 6 values from -1, 0 and 1 (1,080), 2,000 random of
3 to 12 values within 3, 1,000 built from three parts of 1 to 4 values,
500 random of 13 to 200 values, 300 built of parts up to 100 values,
100 random of up to 2,000 values within 20, and 4 of 50,000.

| | property |
|---|---|
| P1 | the statement, for arrays of up to 12 values; the ways arm's count of splits too |
| P2 | the reversed array splits the same way |
| P3 | no split when the total is not a multiple of 3; three values split exactly when equal; an array of zeros always splits |
| P4 | an array built from three parts with equal sums splits |
| P5 | multiplying every value by -1, 2, -3 or 5 changes nothing |
| P6 | each arm agrees with at least two of the other four |

It prints `4984 arrays: checksum 904978993, 114440 checks over 5 arms:
0 failures` under `karac __mir-run` (2.5 s) and `karac
__mir-llvm-run`, and the same under `karac __mir-llvm-asan` with no
error.

## Mutation testing

Thirty edits to the differential, each run under `karac __mir-run` and
`karac __mir-llvm-run`; fifteen are kept, three to each arm, all
fifteen are killed, and each fails the same checks under both.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the second cut at a third instead of two thirds | P1 702, P2 801, P3 19, P4 730, P6 989 |
| M2 | ★: a total that is not a multiple of 3 let through | P1 660, P2 998, P3 944, P5 584, P6 944 |
| M3 | ★: the first cut taken again at a later third | P1 293, P3 10, P4 135, P6 301 |
| M4 | ends: the first part leaving no room for the others | P1 32, P2 59, P3 4, P6 32 |
| M5 | ends: an empty middle | P1 92, P2 59, P3 3, P6 93 |
| M6 | ends: the last value counted twice | P1 699, P2 821, P4 807, P6 1001 |
| M7 | count: more than three parts refused | P1 166, P2 139, P3 4, P4 81, P6 229 |
| M8 | count: the running sum not restarted after a cut | P1 1039, P2 321, P3 19, P4 1072, P6 1390 |
| M9 | count: a part closed once its sum passes a third | P1 520, P2 822, P4 244, P5 609, P6 581 |
| M10 | ways: a first cut paired with a second at the same place | P1 417, P3 7, P6 125 |
| M11 | ways: a second cut counted without a first | P1 904, P2 273, P3 20, P6 297 |
| M12 | ways: a first part of one value never counted | P1 580, P2 516, P3 25, P4 201, P6 321 |
| M13 | map: the last first cut kept, not the earliest | P1 435, P2 268, P3 10, P4 275, P6 476 |
| M14 | map: both cuts at the same place | P1 124, P3 7, P6 125 |
| M15 | map: the earliest second cut kept, not the latest | P1 356, P2 268, P3 10, P4 207, P6 414 |

P1 and P6 kill all fifteen, P3 thirteen, P2 twelve, P4 nine and P5
two. P5 sees only the edits that let a total through that is not a
multiple of 3 or compare a sum against a third by size, since scaling
keeps every equality and so every cut. M10 and M14 touch only zero
totals, where a third and two thirds are one prefix; the exhaustive
small arrays and the zero examples carry them. The checks draw no
random number that depends on an answer, so every mutant sees the same
arrays and their counts can be compared.

Fifteen other edits were tried and set aside. One changes no answer:
the ways arm counting at most one first cut, which leaves its count
wrong (P1's count check fails 525 times) but never turns a positive
count into zero. Seven failed exactly the same checks as a kept one: ★
allowing the second cut at the last element and putting both cuts at
one place, count accepting two parts, and map allowing the second cut
at the last element, all as M14; ways allowing the second cut at the
last element, as M10; ways letting a total through that is not a
multiple of 3, as M2; and map comparing the earliest second cut, as
M15. The other seven were killed too, beyond three per arm: ★
restarting the prefix at the first cut and leaving out the first value;
ends letting a short first part through, leaving out the first value
and never checking the last part; count letting a total through that is
not a multiple of 3; and ways never counting a last part of one value.

## Verification

Every arm prints the same output as `three_parts.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer)
with no error; the differential prints its line under all three.
`karac check` passes all five arms, the differential and the bench
program. `karac run` and a `karac build` binary print the same output
for every arm and the differential. The release build is kara
`852f593fdc` with the effect-variable checker of `5efc032bff`, the
runtime archives rebuilt at `8b6e8a9088`. Under `karac
__mir-run` the arms take 1.0 s to 1.8 s (map).

No compiler gap turned up writing this kata.

The legacy compiler was removed from kara at M3, so there is no legacy
lane.

## Benchmarks

The bench runs the ★ arm in all five languages on one array of 50,000
values from -2 to 4, drawn once, its last value adjusted so the total is
a multiple of 3; then 10,000 rounds each move one value by -3, 0 or +3,
which keeps the total a multiple of 3, ask again, and fold the answer
into a checksum. The values lean positive so the prefix sums climb: the
cuts fall about a third and two thirds of the way along, and the
question is mostly decided by whether the climbing sums hit the third
and two thirds exactly. Every implementation prints `10000 rounds over
50000 values: 3291 split, checksum 638361044`.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with karac as above:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.316 to 0.406 s | 0.335 s |
| Rust (`rustc -O`) | 0.328 to 0.389 s | 0.354 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.517 to 0.560 s | 0.523 s |
| Go | 0.494 to 0.611 s | 0.521 s |
| Python | 41.2 s | |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.479 to 0.587 s | 0.489 s |
| Kāra (`karac build`) | 0.477 to 0.526 s | 0.491 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. Python's run is about 84 times Kāra's. A plain
`karac build` parallelizes nothing here (its user time equals its real
time) and runs as fast as the sequential one; it was linked against
runtime archives rebuilt at `852f593fdc`, which changed only the
file-system providers.

v2 took 0.93 times Rust's median time under overflow checks and 1.46
times C's. Under valgrind's cachegrind v2 ran 7,311 million
instructions and 2,158 million branches, Rust with overflow checks
9,319 million and 2,531 million, Rust without them 5,316 million and
1,056 million, and C 5,654 million and 1,050 million. Every version
mispredicted about 33,000 branches in all, so the loops are predictable
and the difference is instruction count: the checked builds test each
addition for overflow, which unchecked Rust and C do not. We did not
look further into where v2 saves over checked Rust.
