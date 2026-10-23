# 915. Partition Array into Disjoint Intervals

Given an integer array `nums`, partition it into two contiguous
subarrays `left` and `right` so that:

- every element in `left` is less than or equal to every element in
  `right`;
- `left` and `right` are non-empty;
- `left` has the smallest possible size.

Return the length of `left` after such a partitioning. Test cases are
generated such that a partitioning exists.

```
nums = [5,0,3,8,6]     ->  3   (left = [5,0,3], right = [8,6])
nums = [1,1,1,0,6,12]  ->  4   (left = [1,1,1,0], right = [6,12])
```

**Constraints:** `2 <= nums.length <= 10^5`, `0 <= nums[i] <= 10^6`,
and there is at least one valid answer.

## Approaches

A split after the first `k` values works when the largest of them is at
most the smallest of the rest; the answer is the first such `k`.

| file | mechanism |
|---|---|
| `partition_disjoint.kara` ★ | a table of every suffix's smallest value, filled from the right, then a walk from the left keeping the largest so far, stopping at the first k where it is at most the smallest after k. O(n) time and space |
| `partition_disjoint_onepass.kara` | one pass with a candidate split, the left side's largest and the largest seen: a value below the left side's largest pulls the split past it, and the left side's largest becomes the largest seen. O(n) time, O(1) space |
| `partition_disjoint_sums.kara` | a sorted copy, and the first k at which the running sum of the array equals the running sum of the sorted copy: k values can stand left of the rest exactly when they are k of the smallest, and only those reach the least sum. O(n log n) |
| `partition_disjoint_chunks.kara` | the array cut into the most chunks that sort independently, with a stack of chunks (largest value, length): each value starts a chunk and swallows the chunks below whose largest exceeds it; the bottom chunk's length is the answer. O(n) |
| `partition_disjoint_sparse.kara` | a sparse table of minimums over runs of 2^j values, and the smallest of each suffix read in O(1) as the smaller of two runs covering it, against the largest so far. O(n log n) to build |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 13 lines: LeetCode's two examples and seven
more (two equal values, 0 and 10^6, a dip, a tie across the split,
rising, falling then a peak, all equal); for 500 random arrays of up to
1,000 values built from a block at most a cut value and a block at least
it, the left sides' sum (106,628) and a checksum; and three of
LeetCode's largest, 10^5 values rising, with the smallest second to
last, and in two halves. `partition_disjoint.py` mirrors the ★ arm and
its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: for each `k` from 1, compare every value of `nums[0..k]` with
every value of `nums[k..]`, and return the first `k` where none is
larger. It checks 3,200 random arrays: 3,000 of 2 to 10 values below 4
or 10, drawn at random and kept only when the statement finds a split,
against the statement; and 200 of up to 1,000 values in two blocks split
at a random value below 5, 1,000 or 10^6 against the other properties;
120,915 values in all, left sides summing to 55,130.

| | property |
|---|---|
| P1 | the statement's smallest left side, on the small arrays |
| P2 | the same answer with every value raised by the same amount (within 10^6) |
| P3 | the same answer with a value at least the largest appended |
| P4 | a value at most the smallest put in front makes the answer 1 |
| P5 | the same answer with the values right of the ★ arm's split shuffled |
| P6 | each arm agrees with at least two of the other four |

P5 holds because every value right of the true split is at least every
value left of it, so a smaller split always fails on a value inside the
left side, which the shuffle does not touch. It prints `3200 arrays,
120915 values, left sides summing to 55130, 95000 checks over 5 arms: 0
failures` under `karac __mir-run` (8 s) and `karac __mir-llvm-run`, and
the same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-llvm-run`. All fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a tie across the split refused | P1 1705, P3 495, P4 2258, P6 1772 |
| M2 | ★: each suffix minimum missing its own value | P1 1090, P5 3870, P6 1260 |
| M3 | ★: only the latest value kept as the left side's largest | P1 639, P5 2500, P6 807 |
| M4 | onepass: a value equal to the left side's largest pulled in | P1 1722, P3 530, P4 2252, P5 418, P6 1794 |
| M5 | onepass: the left side's largest taken from the undercutting value | P1 628, P6 792 |
| M6 | onepass: the split moved to just before the undercutting value | P1 1094, P6 1260 |
| M7 | sums: sums one apart taken as equal | P1 498, P6 523 |
| M8 | sums: the array's sum one value ahead | P1 2557, P3 1923, P4 1864, P5 354, P6 2737 |
| M9 | sums: the sorted sum one value ahead | P1 1987, P3 1170, P4 948, P5 174, P6 2156 |
| M10 | chunks: the top chunk's length returned | P1 1973, P3 1251, P4 1251, P5 1046, P6 2165 |
| M11 | chunks: a swallowed chunk counted as one value | P1 753, P6 918 |
| M12 | chunks: a value one below a chunk's largest not merging | P1 587, P6 622 |
| M13 | sparse: only the run from k read | P1 26, P3 20, P6 26 |
| M14 | sparse: the second run starting one value early | P1 930, P3 378, P5 71, P6 937 |
| M15 | sparse: each level copying its left half only | P1 345, P3 420, P6 474 |

P1 and P6 kill all fifteen; P3 eight, P5 seven, P4 five and P2 none.
Every mutant compares values only with one another (the sums arm's two
sums both grow by k times the amount), so raising them all changes
nothing; P2 would catch an arm that compares with a constant, which no
mutant here introduces. P5 shuffles the values right of the ★ arm's own
split, so when ★ is wrong (M2, M3) the shuffle can move values across
the true split and the other four arms fail P5 too, which is why those
counts pass 3,200.

Four mutants were replaced. The first M13 used a run one level shorter
when the suffix's length is a power of two; two runs of half the length
still cover it, so it was equivalent and survived. Three more failed
exactly the same checks as an earlier mutant and so told nothing new:
the first M8 (the copy never sorted, which answers 1 like M6's split),
the first M10 (an equal value merging chunks, the same mistake as M4)
and two successive M12s (a swallowed chunk's largest forgotten, as in
M5, then the bottom chunk never swallowed, again as M6).

## Verification

Every arm prints the same output as `partition_disjoint.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build and the runtime archives are both at
kara `5502146bed`. Under `karac __mir-run` the arms take 0.9 to 7.1 s
each (the sparse table the longest) and the differential 8 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The ★, onepass and sums arms print the same output under the frozen
legacy interpreter, the legacy JIT and both legacy builds, with and
without auto-par. The sparse arm does under the legacy interpreter, but
the legacy JIT and builds refuse `table[below][i].min(...)`: "chained
indexed receivers (`a[i][j].min(...)`) are deferred to v1.x; bind the
inner element to a temporary first". Legacy refuses the chunks arm and
the differential at the first `*v` on an element of a `Vec[i64]`'s
`.iter()` ("unary '*' requires 'ref T', ... found 'i64'"), legacy's
older rule; under v2 the element is a reference and the `*` is required.
Legacy is frozen, so none of this is filed.

## Benchmarks

The bench program uses the ★ arm on 10^5 values, the first half below
500,000 and the second at or above it, built once. Each round rewrites
one value at random, finds the split and puts the value back; 2,000
rounds. Every implementation prints `2000 rounds over 100000 values:
left sides summing to 150100000, checksum 515416602`.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.18 to 0.23 s | 0.19 s |
| Rust (`rustc -O`) | 0.21 to 0.27 s | 0.24 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.21 to 0.29 s | 0.23 s |
| Go | 1.04 to 1.14 s | 1.07 s |
| Python | 24.5 s | |
| Kāra (`karac build --mir`) | 0.22 to 0.29 s | 0.23 s |
| Kāra (legacy `karac build`) | 0.22 to 0.27 s | 0.24 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Python's run is a hundred times
C's; fewer rounds would leave the compiled programs too short to time.

v2 takes 1.00 times Rust's median time under overflow checks, 1.19
times C's and 0.97 times legacy's. Under valgrind's cachegrind v2 runs
3.70 billion instructions and 1.98 billion branches, the same as legacy
and Rust with overflow checks, against 2.25 billion and 0.38 billion for
C; all four mispredict fewer than 40,000. Go takes 5.5 times C's time;
why was not profiled.
