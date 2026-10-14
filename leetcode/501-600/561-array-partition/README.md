# 561. Array Partition

Given an integer array `nums` of `2n` integers, group these integers
into `n` pairs `(a1, b1), (a2, b2), ..., (an, bn)` such that the sum of
`min(ai, bi)` for all `i` is maximized. Return the maximized sum.

```
nums = [1,4,3,2]      ->  4
nums = [6,2,6,5,1,2]  ->  9
```

**Constraints:** `1 <= n <= 10^4`; `nums.length == 2 * n`; `-10^4 <=
nums[i] <= 10^4`.

## Approaches

Every arm is `fn array_pair_sum(nums: own Vec[i64]) -> i64`, owning its
argument because three of the four sort it or empty it into a queue. In
the best pairing the smallest number goes with the next smallest: the
smallest counts whatever it is paired with, and its partner is lost to
the sum, so the partner should be the least that can be lost. The same
holds for what is left, so the answer is every other number in rising
order, from the first.

| file | mechanism |
|---|---|
| `array_partition.kara` ★ | `sort`, then the numbers at even places, `for i in (0..n).step_by(2)`; O(n log n) |
| `array_partition_counts.kara` | a counting sort over -10^4 to 10^4: how often each value occurs, walked from the least, every other number met taken; O(n + range) |
| `array_partition_chunks.kara` | `sort`, then `nums.chunks(2).iter().map(\|pair\| pair[0]).sum()`, each pair's first; O(n log n) |
| `array_partition_heap.kara` | a `PriorityQueue` built from the vector, smallest first: the first of each two popped counts, the second is discarded with `let _ =`; O(n log n) |
| `differential.kara` | the four arms against the definition, five properties |

Every arm prints the same 11 lines: seven arrays at the edges (the two
examples, one pair unequal and equal, the problem's least and most twice
each, falling numbers and numbers all below zero), a total and checksum
over 300 random arrays of 1 to 20 pairs in -100 to 100, and the
problem's most, 20,000 numbers: all 10,000, falling from 10,000 to
-9,999, and random in -10,000 to 10,000. `array_partition.py` mirrors
the ★ arm and its output is byte-identical.

The chunks arm does not run under `karac __mir-run` today; see Compiler
findings. It is kept as written. A copy outside this directory that
takes the chunks of a slice of the vector, `nums[..].chunks(2)`, prints
the same output there.

## Differential

`differential.kara` holds copies of the four arms and the definition,
the statement read literally: every way to pair the numbers up, the
first number left paired with each of the others in turn and the rest
paired the same way, and the largest sum of the pairs' smaller numbers.
Each arm is held to the properties below on 1,000 random arrays of 1 to
5 pairs: numbers in -3 to 3, where ties are common, or in -9000 to
9000, in turn, the second kept inside the problem's range after P4's
shift.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | the answer is at most half the total, and at least n times the least number |
| P3 | the numbers rotated and reversed give the same answer |
| P4 | every number raised by c (5, or -1000 for the wider numbers) raises the answer by n * c |
| P5 | the answer is no less than the pairing the numbers came in |

It prints `1000 cases, 4 arms, 20000 checks, 0 failures` under `karac
__mir-llvm-run`, and runs clean under `karac __mir-llvm-asan`. Under
`karac __mir-run` it stops at its copy of the chunks arm, as the arm
does; the copy outside this directory with `nums[..].chunks(2)` prints
`0 failures` there.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac
__mir-llvm-run`, since the chunks arm stops `karac __mir-run`. All eight
that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: every other number from the second | P1 971, P2 971 |
| M2 | ★: no sort | P1 785, P2 454, P3 461 |
| M3 | counts: the first number met not taken | P1 971, P2 971 |
| M4 | counts: each value counted once, however often it occurs | P1 276, P2 104, P4 273, P5 28 |
| M5 | chunks: each pair's second | P1 971, P2 971 |
| M6 | chunks: the numbers reversed, not sorted | P1 799, P2 511, P3 461 |
| M7 | heap: largest first | P1 971, P2 971 |
| M8 | heap: the second of each two not popped | P1 929, P2 489, P4 1000, P5 158 |
| E1 | ★: the range stops one short of the end | 0 |
| E2 | counts: one count too many | 0 |
| E3 | chunks: each pair's smaller, compared | 0 |
| E4 | heap: `sum += smaller` written `sum = sum + smaller` | 0 |

M1, M3, M5 and M7 are one mistake made four ways: each adds up the
larger of every pair. That is more than half the total unless every pair
is two equal numbers, which happens in 29 of the 1,000 cases, all small
ones; there the answer is right. M2 and M6 add up one number from each
pair the input happens to make, so the order matters and P3 sees them,
but each is at least the smaller of its pair, so P5 does not. M4 drops
repeats, so it takes too few numbers and P4's shift counts them short.
M8 adds up every number, so P4 fails on every case. E1 is safe because
the length is even, so the last place is odd; E3 because after sorting
the first of a pair is the smaller.

## Verification

Every arm prints the same output as `array_partition.py` under `karac
__mir-llvm-run` and runs clean under `karac __mir-llvm-asan`
(AddressSanitizer and LeakSanitizer): output identical, no error, no
leak. The ★, counts and heap arms print it under `karac __mir-run` (the
v2 MIR interpreter) too. `karac check` passes on every arm, the
differential and the bench program, with no warnings.

The frozen legacy backends: every arm prints the same output under
`karac run --interp`, `karac run` and `karac build`, and under
`KARAC_AUTO_PAR=1 karac build`. The differential prints `0 failures`
under `karac build`; under `karac run --interp` it does not finish
within 120 s.

## Benchmarks

The bench program uses the ★ arm. It builds 100 random arrays of
20,000 numbers in -10,000 to 10,000, the problem's most, once; then
50 times over every array is answered, each time on a fresh copy, since
the answer sorts what it is given. Every implementation prints
`100 arrays of 20000, 50 rounds: total -70424357350, checksum
454774072`, the Kāra program under `karac __mir-run` included (134 s).

Every implementation copies the array and sorts the copy with its
standard library's sort: `Vec.sort` in Rust, `slices.Sort` in Go,
`list.sort` in Python, and the C library's `qsort` with a comparison
function. Spot timings on a shared 4-core container, three runs each
(two for Python; `bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 10.4 to 10.8 s |
| Rust (`rustc -O`) | 2.19 to 2.42 s |
| Rust (`rustc -O -C overflow-checks=on`) | 2.23 to 2.41 s |
| Go | 7.16 to 7.54 s |
| Python | 16.9 s |
| Kāra (`karac build`, legacy) | 1.47 to 1.53 s |
| Kāra (`karac build --mir`) | 1.43 to 1.47 s |

The legacy `karac build` builds the bench program and prints the same
line, so `bench.sh` is as `scripts/new-bench.sh` wrote it. The `--mir`
row is timed at kara `136e218505` and is outside `bench.sh`. Under
`karac __mir-llvm-run` the program prints the same line in 49 s, compile
included; that JITs the MIR's IR without optimization passes, so it is
not a benchmark.

This bench measures each library's sort more than the language. Kāra's
`sort` is specified as stable, and on a `Vec` of integers, where
stability cannot be seen, the compiled MIR backend hands the buffer to
Rust's `sort_unstable` (`karac_mir_sort_int` in kara's
runtime/src/mir.rs). The Rust mirror's `sort` is Rust's stable sort;
with `sort_unstable` instead it takes 1.54 to 1.64 s, level with Kāra.
Go's `slices.Sort` alone, on 5,000 fresh copies of one of these arrays,
takes 7.6 s, and glibc's `qsort` calls the comparison function through a
pointer for every comparison.

## Compiler findings

| id | status | what |
|---|---|---|
| B-2026-10-14-15 | open | The MIR interpreter has no `chunks` or `windows` on a `Vec` receiver: `nums.chunks(2)` stops `karac __mir-run` with "call of unknown function Vec[i64].chunks", while `karac check` passes it, `karac __mir-llvm-run` runs it, and the same call on a `Slice` runs on `__mir-run`. The chunks arm and the differential keep the natural spelling; `nums[..].chunks(2)` runs. Recheck both once it is fixed. |

The legacy failure above is not filed because legacy is frozen.
