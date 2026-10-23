# 918. Maximum Sum Circular Subarray

Given a circular integer array `nums` of length `n`, return the maximum
possible sum of a non-empty subarray of `nums`.

A circular array means the end of the array connects to the beginning
of the array. Formally, the next element of `nums[i]` is
`nums[(i + 1) % n]` and the previous element of `nums[i]` is
`nums[(i - 1 + n) % n]`.

A subarray may only include each element of the fixed buffer `nums` at
most once. Formally, for a subarray `nums[i], nums[i + 1], ...,
nums[j]`, there does not exist `i <= k1, k2 <= j` with
`k1 % n == k2 % n`.

```
nums = [1,-2,3,-2]  ->  3    (the subarray [3])
nums = [5,-3,5]     ->  10   (the subarray [5,5], wrapping around)
nums = [-3,-2,-3]   ->  -2   (the subarray [-2])
```

**Constraints:** `n == nums.length`, `1 <= n <= 3 * 10^4`,
`-3 * 10^4 <= nums[i] <= 3 * 10^4`.

## Approaches

A circular subarray either sits inside the array or wraps around its
end, and a wrapping one is the whole array less a subarray in the
middle.

| file | mechanism |
|---|---|
| `max_subarray_sum_circular.kara` ★ | one Kadane pass for both the largest and the smallest subarray sum; the answer is the larger of the largest and the total less the smallest, except that when every value is negative the smallest is the whole array and the largest alone answers. O(n) |
| `max_subarray_sum_circular_deque.kara` | the array laid out twice, with prefix sums `p`; a circular subarray is `p[j] - p[i]` with `j - n <= i < j`, and a `VecDeque` of starts with increasing prefix sums gives the smallest `p[i]` in each window. O(n) |
| `max_subarray_sum_circular_suffix.kara` | a wrapping subarray is a front part `nums[0..i]` joined to a back part after it: a table of the largest back-part sum starting at `j` or later, tried against every front part, beside Kadane for the ordinary subarrays. O(n) |
| `max_subarray_sum_circular_halves.kara` | divide and conquer: a `Stretch` struct holds a stretch's total and its largest and smallest prefix, suffix and subarray sums, two neighbours combine in O(1), and the array is split in halves down to single values. O(n) summaries, O(log n) deep |
| `max_subarray_sum_circular_sparse.kara` | the doubled prefix sums again, with a sparse table of the minimum over every run of 2^k of them, so each window's smallest start is read from two runs that cover it. O(n log n) to build, O(1) a query |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 16 lines: LeetCode's three examples and eight
more (a wrap that beats the middle, a wrap that does not, all negative,
one positive value, one negative value, all zeros, a wrap over one
negative value, and two peaks either side of a dip); for 500 random
arrays of 1 to 1,000 values, leaning from negative to positive, the
answers' sum (773,163,856) and a checksum; and four of LeetCode's
largest, 30,000 values: all -30,000, all 30,000, random, and with a
valley in the middle so that the best subarray wraps.
`max_subarray_sum_circular.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: try every start and every length from 1 to `n`, sum
`nums[(start + t) % n]` for each, and keep the largest. It checks 3,200
random arrays: 3,000 of 1 to 8 values from -5 to 5, one in four of them
all negative, against the statement; and 200 of 1 to 1,000 values from
-30,000 to 30,000, leaning negative or positive, against the other
properties; 109,433 values in all.

| | property |
|---|---|
| P1 | the statement's largest sum, on the small arrays |
| P2 | the same answer for the array rotated by a random amount |
| P3 | the same answer for the array reversed |
| P4 | every value times k (2 to 4), the answer times k |
| P5 | at least the largest value and the total, and at most the larger of the largest value and the sum of the positive values |
| P6 | each arm agrees with at least two of the other four |

It prints `3200 arrays, 109433 values, answers summing to 291199943,
95000 checks over 5 arms: 0 failures` under `karac __mir-run` (18 s)
and `karac __mir-llvm-run`, and the same under `karac __mir-llvm-asan`
with no error.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-llvm-run`. All fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the largest sum never used alone when all values are negative | P1 977, P6 977 |
| M2 | ★: the smallest run never restarted | P1 423, P2 586, P6 514 |
| M3 | ★: the wrap taken as the total plus the smallest | P1 651, P2 586, P5 228, P6 742 |
| M4 | deque: windows one value too long | P1 663, P5 595, P6 666 |
| M5 | deque: equal prefix sums kept at the back, and only a much smaller one dropping them | P1 1748, P2 1588, P3 2130, P4 4, P5 1249, P6 1754 |
| M6 | deque: only single values compared | P1 1190, P5 600, P6 1388 |
| M7 | suffix: the front part only its last value | P1 328, P2 542, P3 622, P6 421 |
| M8 | suffix: the back part only its first value | P1 352, P2 529, P3 622, P6 446 |
| M9 | suffix: Kadane never restarted | P1 1260, P2 1495, P3 1752, P5 1135, P6 1368 |
| M10 | halves: a crossing subarray left out of the largest | P1 287, P2 293, P5 126, P6 394 |
| M11 | halves: the right prefix ignored in the smallest crossing | P1 167, P2 317, P3 138, P6 251 |
| M12 | halves: the left total forgotten in the largest prefix | P1 283, P2 392, P3 404, P5 55, P6 388 |
| M13 | sparse: the window one value shorter | P1 348, P5 126, P6 348 |
| M14 | sparse: only the run from the window start read | P1 277, P2 460, P3 529, P5 270, P6 360 |
| M15 | sparse: each level copying its left run only | P1 1430, P2 1376, P3 1771, P5 1097, P6 1627 |

P1 and P6 kill all fifteen; P2 eleven, P5 ten, P3 eight and P4 one.
P4 sees only M5, whose fixed margin of 1,000 does not scale with the
values; every other mutant is a wrong choice of subarray, and the same
wrong choice scales with them. P3 misses the mutants that lose the wrap
or misjudge a window's length (M1 to M4, M6, M10, M13), since a mistake
that ignores direction makes the same mistake on the reversed array.

Three mutants were replaced because each failed exactly the same checks
as another, so told nothing new: the first M6 (the array laid out once,
not twice) and the first M8 (the best back part not carried from later
starts) both reduce the answer to the best subarray that does not wrap,
exactly as M2 does; and the first M7 (a back part allowed to start one
value before the front part ends) counts one value twice in a wrap, as
M4's over-long window does.

## Verification

Every arm prints the same output as `max_subarray_sum_circular.py`
under `karac __mir-run` (the v2 MIR interpreter) and `karac
__mir-llvm-run`, and under `karac __mir-llvm-asan` (AddressSanitizer)
with no error; the differential prints its line under all three.
`karac check` passes all five arms, the differential and the bench
program. `karac run` and a `karac build --mir` binary print the same
output for every arm and the differential. The release build is at kara
`9913c68556` and the runtime archives at `5502146bed`, with no change to
the runtime between them. Under `karac __mir-run` the arms take 1.5 to
7.8 s each (the sparse table the longest) and the differential 18 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The halves arm prints the same output under the frozen legacy
interpreter, the legacy JIT and both legacy builds, with and without
auto-par; the builds also warn that `nums` is moved and then used again,
which v2's borrowing parameters make untrue. The sparse arm does under
the legacy interpreter, but the legacy JIT and builds refuse
`table[k][lo].min(...)`: "chained indexed receivers (`a[i][j].min(...)`)
are deferred to v1.x". The deque arm fails on legacy everywhere: the
interpreter stops at runtime with "method 'front' not found on type
'Vec'", and the JIT and builds refuse it with "Vec/String method 'front'
is not yet supported in codegen", the `VecDeque` read as a `Vec`. Legacy
refuses the ★ and suffix arms, the differential and the bench program
at the first `*` on an element of a `Vec[i64]`'s `.iter()` ("unary '*'
requires 'ref T', ... found 'i64'"), legacy's older rule; under v2 the
element is a reference and the `*` is required. Legacy is frozen, so
none of this is filed.

## Benchmarks

The bench program uses the ★ arm on 30,000 random values from -30,000
to 30,000, built once. Each of 4,000 rounds rewrites one value at
random, finds the answer and puts the value back. Every implementation
prints `4000 rounds over 30000 values: answers summing to 1641739273,
checksum 291516557`.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.12 to 0.19 s | 0.14 s |
| Rust (`rustc -O`) | 0.13 to 0.16 s | 0.13 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.18 to 0.20 s | 0.19 s |
| Go | 0.16 to 0.21 s | 0.18 s |
| Python | 18.0 s | |
| Kāra (`karac build --mir`) | 0.18 to 0.24 s | 0.20 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Legacy cannot build it (see
Verification). Python's run is about a hundred times C's; fewer rounds
would leave the compiled programs too short to time.

v2 takes 1.04 times Rust's median time under overflow checks and 1.34
times C's. Under valgrind's cachegrind v2 runs 2.28 billion instructions
and 0.48 billion branches, against 2.16 billion and 0.48 billion for
Rust with overflow checks; both mispredict about 12,000. C runs 2.03
billion instructions but only 0.18 billion branches, and mispredicts 12
million of them, 6.7%.
