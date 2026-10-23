# 910. Smallest Range II

You are given an integer array `nums` and an integer `k`.

For each index `i` where `0 <= i < nums.length`, change `nums[i]` to be
either `nums[i] + k` or `nums[i] - k`.

The **score** of `nums` is the difference between the maximum and
minimum elements in `nums`.

Return the minimum **score** of `nums` after changing the values at
each index.

```
nums = [1],      k = 0  ->  0
nums = [0,10],   k = 2  ->  6    (change nums to [2,8])
nums = [1,3,6],  k = 3  ->  3    (change nums to [4,6,3])
```

**Constraints:** `1 <= nums.length <= 10^4`, `0 <= nums[i] <= 10^4`
and `0 <= k <= 10^4`.

## Approaches

| file | mechanism |
|---|---|
| `smallest_range_ii.kara` ★ | the sorted values split in two: in some best answer the values that go up are the smallest ones (if a larger value goes up while a smaller goes down, swapping their moves keeps both inside the range), so sort and try every split; the largest result is the larger of `a[i] + k` and the top value less k, the smallest the smaller of `a[0] + k` and `a[i + 1] - k`. O(n log n) |
| `smallest_range_ii_counts.kara` | the same split over the distinct values, found by counting: the values are at most 10^4, so count them and walk the counts upward instead of sorting. O(n + 10^4) |
| `smallest_range_ii_window.kara` | the narrowest window holding a choice for every index: all 2n choices `nums[i] ± k` sorted, and a window slid over them that stays as narrow as it can while every index has a choice inside. O(n log n) |
| `smallest_range_ii_heap.kara` | raising the lowest value, with a heap: every value starts moved down in a min-first heap with the largest known; the lowest is popped and pushed back moved up, until the lowest is one already moved up and nothing can rise. O(n log n) |
| `smallest_range_ii_prefix.kara` | every split's extremes read from arrays: the largest and smallest of every sorted prefix moved up and of every suffix moved down, combined for every split including the empty ones, without relying on the order to name them. O(n log n) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 11 lines: LeetCode's three examples and five
more (`[7,7,7]` with k = 0, `[0,10000]` with k = 0 and k = 10000, and
`[2,9,4,13,5]` with k = 2 and k = 5); for 300 random cases of up to
2,000 numbers below 10, 1,000 or 10,001, with k up to half of that, the
sum and a checksum of the scores; and two of LeetCode's largest, 10,000
numbers up to 10,000 with k = 0 and with k = 2500.
`smallest_range_ii.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every way to add or subtract k at each index tried, each
result scored, and the least score kept. It checks 3,200 random cases:
3,000 of up to 8 numbers below 12 with k up to 4 against the statement
(up to 256 ways each), and 200 of up to 500 numbers below 10, 1,000 or
10,001, with k up to half of that, against the other properties; 61,812
numbers in all.

| | property |
|---|---|
| P1 | the statement's least score, on the small cases |
| P2 | at least 0 and at least `max - min - 2k`, and at most `max - min` (everything moved the same way) |
| P3 | the same score with every value raised by the same random amount, staying at most 10^4 |
| P4 | the same score for the values reversed |
| P5 | the same score with every value `v` reflected to `10^4 - v` |
| P6 | each arm agrees with at least two of the other four |

P2 to P6 are checked on every case. It prints `3200 cases, 61812
numbers, 95000 checks over 5 arms: 0 failures` under `karac __mir-run`
and `karac __mir-llvm-run`, and the same under `karac __mir-llvm-asan`
with no error.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-llvm-run`. All fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the largest taken as the top raised value | P1 1740, P2 1721, P5 971, P6 1866 |
| M2 | ★: the smallest taken as the lowest lowered value | P1 1756, P2 1739, P5 971, P6 1883 |
| M3 | ★: the last split never tried | P1 383, P5 419, P6 384 |
| M4 | counts: the top raised value never advanced | P1 658, P6 753 |
| M5 | counts: the split below the largest never tried | P1 456, P5 463, P6 457 |
| M6 | counts: a value that occurs once never a split | P1 1326, P5 712, P6 1398 |
| M7 | window: the raised values one too high | P1 1956, P2 1531, P6 2135 |
| M8 | window: an index counted again for its second choice | P1 2046, P2 1790, P4 300, P5 557, P6 2227 |
| M9 | window: the choices never sorted | P1 2361, P2 2525, P4 2574, P5 2574, P6 2561 |
| M10 | heap: the largest never updated after a raise | P1 1221, P2 727, P6 1316 |
| M11 | heap: the largest taken before moving down | P1 1709, P5 330, P6 1857 |
| M12 | heap: a raised value pushed one too low | P1 1314, P5 301, P6 1413 |
| M13 | prefix: the raised values' largest kept as their smallest | P1 2521, P2 2179, P6 2721 |
| M14 | prefix: the lowered values' smallest read as raised | P1 883, P6 978 |
| M15 | prefix: the lowered values taken one value early | P1 1282, P6 1361 |

P1 and P6 kill all fifteen; P5 kills nine, P2 seven, P4 two and P3
none. Every arm, mutated or not, uses the values only through their
differences (the counting arm indexes by value, but only to put them in
order), so raising them all by the same amount can never change an
answer. P4 sees only the two mutants that depend on where values sit:
M9 slides its window over the choices in the order they were listed,
and M8, which marks an index covered by either of its choices, depends
on which of an index's choices the window meets first, and ties among
equal choices are broken by index. P5 swaps moving up with moving
down, but that is not enough to see every mutant that treats them
differently: M7's choices `v - k` and `v + k + 1` reflect to the same
pair moved down by one, which scores the same.

One mutant was replaced. The first M15 took the lowered values' largest
from one value early, which adds `a[ups - 1] - k`; that is below
`a[ups - 1] + k`, already among the raised values, so the larger of the
two largests never changed and the mutant was equivalent.
## Verification

Every arm prints the same output as `smallest_range_ii.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build and the runtime archives are both at
kara `5502146bed`. Under `karac __mir-run` the arms take 0.8 to 7.1 s
each (the heap the longest) and the differential 10.5 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

Every arm and the differential also print the same output under the
frozen legacy interpreter, the legacy JIT and both legacy builds, with
and without auto-par. The legacy builds of the five arms warn that
`big` is moved into the first call and used again, under legacy's older
rule that a bare parameter takes ownership; the programs run correctly
all the same. Legacy is frozen, so none of this is filed.

## Benchmarks

The bench program uses the ★ arm on 500,000 numbers up to 10,000, built
once. Each round solves them with k = `round * 373 % 5001`, folds the
score into a checksum and changes one number; 40 rounds, each sorting a
fresh copy. Every implementation prints `40 rounds over 500000 numbers:
scores summing to 299667, checksum 303762099`.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 2.80 to 3.09 s | 2.92 s |
| Rust (`rustc -O`) | 0.44 to 0.57 s | 0.49 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.44 to 0.56 s | 0.50 s |
| Go | 1.48 to 1.73 s | 1.66 s |
| Python | 11.4 s | |
| Kāra (`karac build --mir`) | 0.29 to 0.40 s | 0.34 s |
| Kāra (legacy `karac build`) | 0.31 to 0.38 s | 0.33 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does.

Most of the time is the sort, and each language uses its own library
sort: C `qsort` with a comparison function, Rust's stable `sort`, Go's
`slices.Sort` and Python's `sorted`. v2 sorts a `Vec` of integers with
Rust's unstable sort (`karac_mir_sort_int` in the runtime). v2 takes
0.68 times Rust's median time under overflow checks, and C takes 8.6
times v2's. Under valgrind's cachegrind v2 runs 3.41 billion
instructions and 0.26 billion branches, legacy about the same, Rust
with overflow checks 4.25 billion and 0.78 billion, and C 10.7 billion
and 2.43 billion, 0.38 billion of them indirect: about one indirect
branch for each comparison `qsort` makes through its function pointer,
which is where C loses. C also mispredicts 173 million branches, against
6 million for Rust and 2 million for both Kāra builds. The gap between
Rust and Kāra fits the stable sort against the unstable one, but that
was not profiled.
