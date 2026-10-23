# 923. 3Sum With Multiplicity

Given an integer array `arr`, and an integer `target`, return the number
of tuples `i, j, k` such that `i < j < k` and
`arr[i] + arr[j] + arr[k] == target`.

As the answer can be very large, return it modulo `10^9 + 7`.

```
arr = [1,1,2,2,3,3,4,4,5,5], target = 8  ->  20
arr = [1,1,2,2,2,2], target = 5          ->  12
arr = [2,1,3], target = 6                ->  1
```

In the first example, (1, 2, 5) occurs 8 times, (1, 3, 4) 8 times,
(2, 2, 4) twice and (2, 3, 3) twice. In the second, a 1 is chosen in 2
ways and two of the four 2s in 6 ways. In the third, (1, 2, 3) occurs
once.

**Constraints:** `3 <= arr.length <= 3000`; `0 <= arr[i] <= 100`;
`0 <= target <= 300`.

## Approaches

The values lie between 0 and 100, far fewer than the indices, so each
arm counts by value rather than trying index triples.

| file | mechanism |
|---|---|
| `three_sum_multi.kara` ★ | each value's count in an `Array[i64, 101]`, then every `x <= y <= z` with `x + y + z = target`, counted with binomial coefficients: `c(x) c(y) c(z)` when all three differ, `C(c(x), 2) c(z)` or `c(x) C(c(y), 2)` when two are equal, `C(c(x), 3)` when all three are. As `y` grows `z` falls, so the walk over `y` stops once `z < y`. O(n + 101^2) |
| `three_sum_multi_pointers.kara` | a sorted copy, and for each `i` two pointers closing in on the pairs after it that make up the rest: two different values multiply the lengths of their runs, and two equal ones give `C(m, 2)` for the `m` between them. O(n^2) |
| `three_sum_multi_pairs.kara` | a `Vec` of 201 counts of the pair sums seen so far: each value `arr[k]` first adds the pairs that sum to `target - arr[k]`, then puts its own pairs with every earlier value in. O(n^2) |
| `three_sum_multi_choose.kara` | three rows indexed by sum, `one`, `two` and `three`, counting the ways to choose one, two or three of the values seen so far: a new value `v` adds `two[s - v]` to `three[s]` and `one[s - v]` to `two[s]`, with `s` taken down from the target, then counts itself in `one[v]`. O(n * target) |
| `three_sum_multi_between.kara` | for each `i`, an `Array[i64, 101]` counting the values between `i` and `j` as `j` moves right: each `j` adds the middles that complete `arr[i] + arr[j]`. O(n^2) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 10 lines: LeetCode's three examples and five
more (no triple, four zeros for 0, five 100s for 300, a mix of values for
150, and three 3s for 10, which no triple reaches); for 200 random arrays
of 3 to 300 values, by turns below 101 and below 11, the answers' sum
(4,756,449) and a checksum; and LeetCode's largest, 3,000 values: all 1
for 3, random values for 150, and 0, 1 and 2 repeating for 3, where the
first and the last answers pass 10^9 + 7 and are reduced. `three_sum_multi.py` mirrors the
★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: try every `i < j < k` and count the triples whose values sum
to the target. It checks 3,200 random arrays with values below 6, 11 or
101 by turns and a target the values can reach: 3,000 of 3 to 12 values
against the statement, and 200 of 3 to 200 values against the other
properties; 41,365 values in all.

| | property |
|---|---|
| P1 | the statement's count, on the small arrays |
| P2 | the same answer for the array shuffled |
| P3 | the same answer with every value `v` turned into `100 - v` and the target into `300 - target` |
| P4 | one more value `x` at the end adds the pairs before it that `x` makes up to the target |
| P5 | `n` copies of the first value `v` give `C(n, 3)` for the target `3v` and 0 for any other (asked for `3v` and for the case's target by turns) |
| P6 | each arm agrees with at least two of the other four |

It prints `3200 arrays, 41365 values, answers summing to 2277867, 95000
checks over 5 arms: 0 failures` under `karac __mir-run` (25 s) and
`karac __mir-llvm-run`, and the same under `karac __mir-llvm-asan` with
no error.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-llvm-run`. All fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: `C(c, 2)` for `x = y` taken as `c * c / 2` | P1 369, P3 759, P4 25, P6 522 |
| M2 | ★: `C(c, 3)` divided by 2, not 6 | P1 65, P4 3, P5 1640, P6 117 |
| M3 | ★: the walk over `y` stopped once `z < x`, not `z < y` | P1 1226, P3 1397, P4 247, P6 1404 |
| M4 | pointers: `j` starting at `i`, not after it | P1 1020, P3 1349, P4 85, P5 1640, P6 1205 |
| M5 | pointers: two runs' lengths added, not multiplied | P1 917, P3 914, P4 198, P6 1094 |
| M6 | pointers: equal ends counted as one pair | P1 122, P3 365, P4 17, P5 1493, P6 270 |
| M7 | pairs: a need of 200 ignored | P2 2, P3 124, P4 1, P5 6, P6 3 |
| M8 | pairs: a need of 0 ignored | P1 70, P2 96, P3 124, P4 7, P5 160, P6 121 |
| M9 | pairs: each pair counted twice | P1 1114, P4 229, P5 1640, P6 1305 |
| M10 | choose: `two` updated before `three` | P1 205, P2 200, P3 264, P4 7, P5 160, P6 258 |
| M11 | choose: a value counted in `one` before the rows are updated | P1 1433, P2 1011, P4 268, P5 1640, P6 1625 |
| M12 | choose: `s` stopping above `v` | P1 293, P2 404, P3 424, P4 44, P5 160, P6 407 |
| M13 | between: `j` counted among the middles before it is asked | P1 1439, P2 1011, P4 253, P5 1640, P6 1631 |
| M14 | between: a middle of 100 ignored | P1 1, P2 23, P3 445, P4 7, P5 6, P6 25 |
| M15 | between: the counts kept from one `i` to the next | P1 1375, P2 1586, P4 252, P5 1640, P6 1566 |

P4 and P6 kill all fifteen; P1 fourteen, P5 twelve, P3 ten and P2 eight.
P1 misses M7: a need of 200 takes two 100s, which three to twelve values
below 101 seldom hold. P2 misses every mutant in ★, pointers and M9: ★
counts the values and pointers sorts them first, so a shuffle cannot
change their answers, and M9 doubles every pair in any order. P3 misses
the five whose mistake comes out the same on the mirrored array (M2,
M9, M11, M13, M15). P5 asks only about equal values, so it misses the
three mistakes that need two different values (M1, M3, M5).

Twelve other edits were tried and set aside. Two stopped at runtime on an
index out of bounds (pairs taking only the pair with the value just
before, and choose updating its rows with `s` rising). Four failed
exactly the same checks as another: in ★, `x` stopping once `3x` reaches
the target, as M2 does, since both lose the triples of three equal
values; in choose, zeros never counted alone, as M12 does; and pairs
counting the pairs with `k` before `k` is asked and between's `j`
starting at `i`, as each other, since both count a value twice in one
triple. The other six were sound but beyond three an arm.

## Verification

Every arm prints the same output as `three_sum_multi.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and under
`karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `9913c68556` and the runtime
archives at `5502146bed`, with no change to the runtime between them.
Under `karac __mir-run` the arms take 0.3 to 15 s each (between, which
walks every pair of the 3,000-value arrays three times, the longest) and
the differential 25 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The pointers, pairs and between arms print the same output under the
frozen legacy interpreter, the legacy JIT and both legacy builds, with
and without auto-par. Legacy refuses the ★ arm, the choose arm, the
differential and the bench program at the first `*` on an element of a
`Vec[i64]`'s `.iter()` ("unary '*' requires 'ref T', ... found 'i64'"),
legacy's older rule; under v2 the element is a reference and the `*` is
required. Legacy is frozen, so none of this is filed.

## Benchmarks

The bench program builds 100 arrays of 3,000 random values from 0 to
100 once, LeetCode's largest, and in each of 500 rounds runs the ★ arm
on every array, each with a different target up to 300. Every
implementation prints `500 rounds over 100 arrays of 3000: answers
summing to 763561278325, checksum 636284711`.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.28 to 0.35 s | 0.29 s |
| Rust (`rustc -O`) | 0.29 to 0.39 s | 0.31 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.30 to 0.42 s | 0.34 s |
| Go | 0.29 to 0.37 s | 0.32 s |
| Python | 15.2 s | |
| Kāra (`karac build --mir`) | 0.31 to 0.37 s | 0.34 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Legacy cannot build it (see
Verification). Python's run is about 52 times C's.

v2 takes 1.02 times Rust's median time under overflow checks and 1.17
times C's. Under valgrind's cachegrind v2 runs 3.84 billion instructions
and 0.93 billion branches, against 4.14 billion and 0.87 billion for
Rust with overflow checks and 2.35 billion and 0.39 billion for C; all
three mispredict about 3.8 million. Each call is a pass over 3,000
values and then a walk over at most 2,600 pairs of values, so the
counting loop and its bounds checks, which C does not make, are the
likely difference; that is inferred, not profiled.
