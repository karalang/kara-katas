# 1027. Longest Arithmetic Subsequence

Given an array `nums` of integers, return the length of the longest
arithmetic subsequence in it: a sequence picked out of `nums` in order,
not necessarily next to each other, whose neighbouring terms all differ
by the same amount.

```
nums = [3,6,9,12]            ->  4   (difference 3)
nums = [9,4,7,2,10]          ->  3   ([4,7,10])
nums = [20,1,15,3,10,5,8]    ->  4   ([20,15,10,5])
```

**Constraints:** `2 <= nums.length <= 1000`, `0 <= nums[i] <= 500`.

## Approaches

A run of two terms is always arithmetic, so every answer is at least 2,
and a run ending at `nums[i]` with difference `d` extends the longest
one ending at an earlier `nums[j] = nums[i] - d` with the same `d`.

| file | mechanism |
|---|---|
| `longest_arith.kara` ★ | a table by difference: `run[i][d + 500]` is the longest run ending at `nums[i]` with difference `d`; values lie in 0 to 500, so every difference indexes a row of 1,001 directly. O(n^2) time, O(n * 1001) space |
| `longest_arith_map.kara` | a map per index: the common form, a `Map` from difference to length for each index, an earlier `j` giving one more than its own entry or 2. O(n^2) |
| `longest_arith_pairs.kara` | the last two terms: a run of at least two terms is fixed by its last two, `j` and `i`, and the term before them must be `2 * nums[j] - nums[i]`; the latest place holding that value gives the longest run, so `pair[j][i]` is one more than `pair[k][j]` for it. O(n^2) |
| `longest_arith_by_difference.kara` | one difference at a time: for every difference no wider than the spread of the values, walk the array once, the longest run ending at a value `v` one more than the longest ending at `v - d`, kept in an array indexed by value. O(spread * n) |
| `longest_arith_extend.kara` | every pair extended: each pair `i < j` fixes a difference, and taking the earliest next term each time is never worse; a table of where each value next occurs after each place makes every step a lookup. O(n^2 * length) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 14 lines: the answers for seven arrays,
LeetCode's three examples among them; for six groups of random arrays
(500 of 8 values up to 10, down to 2 of 1,000 values up to 50), the sum
of the answers, the longest and a checksum; and the answers for 0 to 500
rising, 200 values alternating between 0 and 500, and 0 to 500 in steps
of 7 with every value twice. `longest_arith.py` mirrors the ★ arm and
its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: over every subsequence, picked out by the bits of a mask,
the most terms of one whose neighbouring terms all differ by the same
amount. It checks 989 arrays: every array of 2 to 4 values below 4 and
of 5 values below 3 (579), then 400 random arrays of 6 to 10 values and
10 of 60 to 150, with values up to 3, 20, 100 or 500. The 979 arrays of
at most 10 values are searched in full. Each array is also asked read
backwards, with every value `v` turned into `500 - v`, with its first or
last value taken off (when it has three or more), and with a random
value no more than one above its largest put on its front or back.

| | property |
|---|---|
| P1 | the statement read literally, on the arrays of at most 10 values |
| P2 | read backwards, the answer does not change |
| P3 | with every value `v` turned into `500 - v`, the answer does not change |
| P4 | taking off an end value loses at most one term, since a run that used it is still arithmetic without it |
| P5 | putting a value on an end gains at most one term |
| P6 | each arm agrees with at least two of the other four |

P4 and P5 hold only at the ends: taking a value out of the middle can
break a long run into short ones, and putting one in can join two.

The differential prints `989 arrays (979 searched in full): checksum
605422067, 29540 checks over 5 arms: 0 failures` under `karac __mir-run`
(18 s) and `karac __mir-llvm-run`, and the same under `karac
__mir-llvm-asan` with no error.

## Mutation testing

Thirty-four edits to the differential, each run under `karac __mir-run`
and `karac __mir-llvm-run`; fifteen are kept, three to each arm, all
fifteen are killed, each fails the same checks under both, and no two
kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a new pair counted as one term | P1 515, P6 525 |
| M2 | ★: the term just before never paired | P1 413, P6 416 |
| M3 | ★: no run ending at the second value | P1 137, P2 231, P6 137 |
| M4 | map: differences without their sign | P1 291, P6 300 |
| M5 | map: the opposite difference looked up | P1 329, P6 333 |
| M6 | map: a repeated value counted twice | P1 572, P4 189, P5 200, P6 579 |
| M7 | pairs: 500 never the term before | P3 121 |
| M8 | pairs: the term after sought, not the one before | P1 209, P2 227, P6 213 |
| M9 | pairs: the earliest place of each value kept | P1 81, P2 10, P4 3, P5 3, P6 84 |
| M10 | by difference: falling runs never tried | P1 98, P2 204, P3 204, P6 99 |
| M11 | by difference: the widest difference never tried | P1 27, P4 30, P5 9, P6 27 |
| M12 | by difference: runs carried over from one difference to the next | P1 964, P2 331, P3 708, P4 203, P5 177, P6 974 |
| M13 | extend: only the very next value looked up | P1 164, P2 216, P6 174 |
| M14 | extend: never extended to 500 | P3 118 |
| M15 | extend: the run going on by 1 | P1 128, P2 124, P3 146, P4 11, P5 15, P6 134 |

P1 and P6 kill thirteen, P2 seven, and P3, P4 and P5 five each. Only P3
sees M7 and M14, which mishandle the value 500: the random arrays hold
500 rarely, and turning every value round makes every 0 a 500. Four
kept edits fail only P1 and P6, since they go wrong the same way
whichever way round the array is read or its values are turned: M1
answers one short of every run longer than two, on the 525 arrays that
have one; M2 never pairs neighbours; and M4 and M5 confuse a run with
one going the other way. P2 sees the edits that treat the two
directions of the array differently, and P4 and P5 the ones whose
answer moves by more than one when an end changes. The checks draw a
random number for every array whatever the answers, so every mutant
sees the same arrays and their counts can be compared.

Nineteen other edits were tried and set aside. Four change no answer.
★ turning every difference round: every run then looks up runs turned
round the same way. Map keeping the last `j`'s run for a difference
rather than the longest, and map reading the earlier terms backwards:
for a fixed `i` and difference every such `j` holds the same value, and
a run ending at an earlier one can end at a later one instead, so the
last is the longest. By difference keeping a value's latest run rather
than its longest: the run it extends only grows, so its run does too.
The other fifteen were killed too, beyond three per arm. Six answer one
short of every run longer than two, or 2 everywhere, and fail exactly as
M1: ★ never writing its table and reading the run before the new term,
map counting a new pair as one term and being one term short, pairs
counting a pair as one term, and extend counting a pair as one term.
Nine fail on their own: ★ never pairing the first value and never
counting runs ending at the last; map answering at least 3; pairs
setting a value's latest place before its pairs are read and counting
every extension as three terms; by difference counting a value out of
range as a term and skipping the first value; and extend skipping a term
after the pair and never starting from neighbours.

## Verification

Every arm prints the same output as `longest_arith.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and under
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error; the differential prints its line under all three. `karac check
--output=json` reports no diagnostic for the five arms, the differential
and the bench program, so `karac fix` had nothing to do. `karac run` and
a `karac build` binary print the same output for every arm and the
differential. The release build is kara `56c60bdf7c`, with runtime
archives rebuilt at `ce706dd131`, the last commit before it to change
the runtime. Under `karac __mir-run` the arms take
3.1 s (pairs) to 14.3 s (map). No compiler gap turned up.

The first harness took up to 144 s per arm under the interpreter, the
by-difference arm walking all 1,001 differences for every array; it
now tries only differences within the spread of the values, and the
groups are smaller.

The legacy compiler was removed from kara at M3, so there is no legacy
lane.

## Benchmarks

The bench builds 40 random arrays of 1,000 values once in all five
languages, values up to 5, 50, 500 and 500 in turn, and answers each
three times with the ★ arm: every call allocates its own table of 1,000
by 1,001 cells, as LeetCode's function does, and fills it over half a
million pairs. The table is a `Vec` of `Vec`s in Kāra and Rust, a slice
of slices in Go, a list of lists in Python and one `calloc`'d block in
C. Every implementation prints `40 arrays of 1000 values, 3 rounds: sum
7056, checksum 90626939`.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with karac as above:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.292 to 0.463 s | 0.353 s |
| Rust (`rustc -O`) | 0.635 to 0.721 s | 0.674 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.850 to 1.122 s | 0.915 s |
| Go | 0.889 to 1.138 s | 1.044 s |
| Python | 12.2 s | |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.605 to 0.850 s | 0.700 s |
| Kāra (`karac build`) | 0.615 to 0.762 s | 0.673 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here
(its user time stays below its real time) and runs as fast as the
sequential one.

v2 took 0.76 times Rust's median time under overflow checks and 1.98
times C's. Rust's user time is well below its real time, 0.36 of 0.67 s
at the median (0.58 of 0.92 s with overflow checks), where the other
programs' user and real times are close; we did not record system time,
so where the rest goes is not measured, nor where Kāra's gap to C goes.
