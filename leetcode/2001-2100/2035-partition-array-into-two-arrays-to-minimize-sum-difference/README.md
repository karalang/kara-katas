# 2035. Partition Array Into Two Arrays to Minimize Sum Difference

You are given an integer array `nums` of `2 * n` integers. You need to
partition `nums` into two arrays of length `n` to minimize the absolute
difference of the sums of the arrays. To partition `nums`, put each element
of `nums` into one of the two arrays. Return the minimum possible absolute
difference.

```
nums = [3,9,7,3]          ->  2     ([3,9] and [7,3])
nums = [-36,36]           ->  72    ([-36] and [36])
nums = [2,-1,0,4,-2,-9]   ->  0     ([2,4,-9] and [-1,0,-2])
```

**Constraints:** `1 <= n <= 15`; `nums.length == 2 * n`;
`-10^7 <= nums[i] <= 10^7`.

Choosing `n` of `30` values is up to `C(30, 15)`, about 1.55 x 10^8 ways,
too many to try. Meet in the middle: split the values into halves of `n`.
A side of the partition takes `k` values from the left half and `n - k`
from the right, so for each `k` the left half's `k`-subsets pair with the
right half's `(n - k)`-subsets, each list at most `C(15, 7) = 6435` long.
The side's sum `a + b` should be as near half the total as it can be, so
for each left sum the right list, sorted, is searched for the sums on
either side of `total / 2 - a`.

## Approaches

| file | mechanism |
|---|---|
| `partition.kara` ★ | each half's subset sums listed by size from bit masks, the right lists sorted, and `partition_point(\|b\| 2 * (a + b) < total)` for each left sum, with the sum at the point and the one before it tried. O(2^n n) |
| `partition_pointers.kara` | both lists sorted, and for each `k` the left sums walked up while one pointer walks the right sums down: no search. O(2^n n) |
| `partition_dfs.kara` | the subset sums from a recursive take-or-leave walk into `mut ref` lists by size, searched with a hand-written lower bound on `ceil((total - 2 a) / 2)` (`div_euclid`, `rem_euclid`). O(2^n n) |
| `partition_tuples.kara` | one sorted list of `(size, sum)` pairs for the right half instead of a list per size; `partition_point` on the pairs finds the first `(n - k, b)` that reaches half. O(2^n n) |
| `partition_sets.kara` | a `SortedSet` of the right half's sums per size; the nearest sums either side of the target from `range(want, i64.MAX).next()` and `range(i64.MIN, want).next_back()`. O(2^n n log) |
| `partition_solution.kara` | LeetCode's Rust template (`impl Solution`, `Vec<i32>`, `vec![vec![]; n + 1]`, `count_ones() as usize`, `sort_unstable`, `binary_search(..).unwrap_or_else(\|x\| x)`), carried by `karac fix` in four rounds to three errors it has no fix for: blocked by B-2026-11-09-14 and B-2026-11-09-15 |
| `differential.kara` | the five arms that check against the statement read literally, six properties |

Every arm prints the same 10 lines: the answers for LeetCode's three
examples and five more; then the sum and a checksum of the answers for 2000
arrays of 2 to 12 values up to 50 either side, and for 4 arrays of 30
values, the most the constraints allow (values up to 10^7, 1000 and 3 either
side). `partition.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms that check and the
statement read literally: every mask of the `2 n` values that chooses `n`,
the smallest difference between the chosen sum and the rest. It checks
1500 arrays of 2 to 10 values up to 1 to 60 either side. Every random
choice of a problem (the values, a shuffle of them, a shift) is drawn
before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the values shuffled leave the answer |
| P3 | every value negated leaves the answer |
| P4 | the same amount (up to 1000 either way) added to every value leaves the answer: each side takes it `n` times |
| P5 | every value tripled triples the answer |
| P6 | each arm agrees with at least two of the other four |

The differential prints `1500 arrays: checksum 842881287, 45000 checks
over 5 arms: 0 failures` under every lane in Verification. On a failure it
prints the first ten and then the count by property. The Rust-template arm
joins it, as a sixth, once it checks.

## Mutation testing

Twenty-five edits to the differential, five to each of its arms, each run
under `karac __mir-run` and `karac __mir-llvm-run`. Fifteen are kept, three
to each arm. All twenty-five are killed, each fails the same way under both
backends, none by a crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the right lists left unsorted | P1 383, P2 561, P3 639, P6 383 |
| M2 | ★: the search boundary at a single sum (`a + b < total`) | P1 200, P2 256, P3 15, P4 221, P6 200 |
| M3 | ★: the empty subset left out | P1 425, P2 172, P5 315, P6 425 |
| M4 | pointers: the pointer moved one step at most | P1 3, P2 5, P6 3 |
| M5 | pointers: the pointer's sum compared with the total, not twice it | P1 150, P2 185, P3 151, P4 204, P6 150 |
| M6 | pointers: the left sums walked from the largest | P1 137, P2 199, P6 137 |
| M7 | dfs: a taken value not counted in the size | P1 1500, P5 1500, P6 1500 |
| M8 | dfs: a taken value added twice | P1 1098, P4 1493, P6 1098 |
| M9 | dfs: the target from the total less one sum | P1 75, P2 127, P3 13, P4 359, P6 75 |
| M10 | tuples: the right pairs left unsorted | P1 427, P2 547, P3 636, P6 427 |
| M11 | tuples: the size test dropped from the pair below | P1 140, P2 147, P3 277, P4 143, P6 140 |
| M12 | tuples: the sizes searched the wrong way round | P1 760, P2 528, P3 337, P5 619, P6 760 |
| M13 | sets: each left size paired with its own size | P1 604, P2 191, P4 762, P5 79, P6 604 |
| M14 | sets: the target from the total alone | P1 192, P2 260, P3 47, P4 346, P5 15, P6 192 |
| M15 | sets: the largest sum above taken for the nearest | P1 224, P2 195, P5 113, P6 224 |

P1 and P6 kill all fifteen, P2 thirteen, P3 eight, P4 seven and P5 six.
P2 misses M7 and M8. M7 puts every sum in the size-0 list, so no `k`
finds a partner and every arm answers `i64.MAX` whatever the order. M8
weighs every value twice, which no order of the values changes. P4 sees
the edits that weigh a value differently from the size it adds to (M8
counts a value twice, M9 drops one `a` from the target, M2 halves the
boundary), since a shift then moves the answer and not the true one. P5
sees the edits whose error does not scale with the values: a size
mismatch (M3, M7, M12, M13) or a nearest sum that is not the nearest (M14,
M15).

The other ten fail as a kept one does, or with a signature of their own
that adds nothing. The ★ arm pairing each left size with its own size and
the tuples arm wanting the left pair's own size fail alike; the pointers
arm and the tuples arm reading their left sums from the right half fail
alike; the DFS arm dropping its skip branch and the sets arm never counting
the size fail as M7. The ★ arm's last value of each half never taken, the
pointers arm's sums never sorted, the DFS arm's right half read from the
left and the sets arm's target three past half fail with counts of their
own.

Seven first drafts survived every check and were replaced. Four drop or
spoil the sum below the search point: the ★ and pointers arms never trying
it, the DFS arm trying only the bound, and the sets arm taking the smallest
sum below instead of the nearest. They are equivalent by the problem's
symmetry. The partition's other side is a `(n - k, k)` choice whose sum is
`total` minus this one, and its search finds as the sum above the point
what this one would have found below it. The pointers arm's pointer
starting at the middle survived too; the sum it misses above the middle is
the other side's sum below the middle, which it does reach. Two are
equivalent outright: the pointer stopping at 1 still tries index 0 as
`j - 1`, and the DFS arm's lower bound searching one short of the end
lands on the last index, whose sum is the one the true bound's `at - 1`
tries. Six more first drafts crashed: an arm that finds no pair answers
`i64.MAX`, and P5's `3 * a` overflowed on it. P5 now divides the tripled
answer back instead, and all six are among the twenty-five.

## Verification

Every arm prints the same output as `partition.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error. `karac
run` and a `karac build` binary print the same output for every arm and the
differential. `karac check --output=json` reports nothing on any of them.
Under `karac __mir-run` the arms take 1.6 s (pointers) to 5.3 s (sets) and
the differential 6.1 s, on kara 6a852dc7b7.

The five arms were written in Kāra. The sets arm first stopped at lowering:
`range(want, i64.MAX)` and `range(i64.MIN, want)` lend their bounds to a
`ref` parameter, and `i64.MAX` was lowered as a place, a field of a local
`i64`, so the program was refused with "an expression with no recorded
type is not lowered yet". The same held for `v.contains(i64.MAX)` and for
a function taking `ref T`. A primitive's constant is now built in a
temporary that is lent (kara 0820c45a7f, `tests/kata_2035_limit_args.rs`).
`karac fix` also moved the arm's `let (mut a, mut b, mut size)` to `let mut
(a, b, size)`.

The Rust arm was written as LeetCode's Rust template. `karac fix` carries
it in four rounds (15, 4, 2 and 1 edits) to three errors it has no fix for.
Rust's `binary_search` returns `Result<usize, usize>`, and the template
takes the insertion point with `unwrap_or_else(|x| x)`; Kāra's returns
`Option[i64]`, so the closure is refused as the wrong shape, with no edit
and no word that `partition_point` is the translation. B-2026-11-09-14
tracks it (kata 2034's Vec arm met the `Ok`/`Err` match form of the same
gap). The other two are where the subset sums meet the `i32` answer. The
template's `let mut a = 0; a += nums[i];` over a `Vec[i32]` keeps the
literal's `i64` default in Kāra (design.md §8: an operator does not fix a
literal's type), and `best.min(..)` with `best: i32` was refused with
nothing to apply. The fourth round's edit had no fix before this kata: an
argument that reads a defaulted binding now gets the binding's annotation,
`a: i32`, as a defaulted receiver already did (kara 8e910189e8,
`tests/kata_2035_check_gaps.rs`). The right half's `b` reaches the `min`
only through the list it is pushed into, and that case, the binding two
hops from the refusal, is B-2026-11-09-15.

## Benchmarks

The bench builds 40 arrays of 30 values once in all five languages (values
up to 10^7, 1000, 100 or 50 either side), and runs the ★ arm on each for 5
rounds, one value negated before each call: 200 calls, each over 2 x 32768
subset sums. Every implementation prints `200 calls: sum 140, checksum
479134508`.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with kara `6a852dc7b7` on LLVM 22:

| | time | median |
|---|---|---|
| Rust (`rustc -O`) | 1.090 to 1.193 s | 1.120 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.154 to 1.222 s | 1.183 s |
| Kāra (`karac build`) | 1.460 to 1.547 s | 1.477 s |
| C (`clang -O3`) | 1.505 to 1.557 s | 1.525 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 1.508 to 1.585 s | 1.531 s |
| Go | 2.298 to 2.440 s | 2.355 s |
| Python | 24.5 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`, the
sequential lane. A plain `karac build` parallelizes nothing here: its user
time (1.470 s) is not above its real time (1.477 s).

The sequential Kāra program is 1.29x Rust under overflow checks and 1.00x
C.
