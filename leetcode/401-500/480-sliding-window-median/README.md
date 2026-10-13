# 480. Sliding Window Median

The median is the middle value in an ordered integer list. If the size
of the list is even, there is no middle value, so the median is the
mean of the two middle values.

You are given an integer array `nums` and an integer `k`. There is a
sliding window of size `k` which is moving from the very left of the
array to the very right. You can only see the `k` numbers in the
window. Each time the sliding window moves right by one position.

Return the median array for each window in the original array. Answers
within `10^-5` of the actual value will be accepted.

```
nums = [1,3,-1,-3,5,3,6,7], k = 3  ->  [1.0,-1.0,-1.0,3.0,5.0,6.0]
nums = [1,2,3,4,2,3,1,4,2], k = 3  ->  [2.0,3.0,3.0,3.0,2.0,3.0,2.0]
```

**Constraints:** `1 <= k <= nums.length <= 10^5`; `-2^31 <= nums[i] <=
2^31 - 1`.

## Approaches

Every arm is `fn median_sliding_window(nums: Vec[i64], k: i64) ->
Vec[f64]`, and borrows the list. The mean of two middle values is
`(a + b) as f64 / 2.0`; the sum is taken in `i64`, so two numbers near
`2^31` do not overflow, and it is exact in `f64`.

| file | mechanism |
|---|---|
| `sliding_window_median.kara` ★ | the lower half in a largest-first `PriorityQueue`, the upper half in a smallest-first one; a number leaving the window is counted in a `Map` and thrown away only when it reaches the top of its heap, and the live sizes are kept apart from the heaps' lengths. O(n log n) |
| `sliding_window_median_sorted.kara` | the window as a sorted `Vec`: the new number inserted where a binary search says, the leaving one found with `binary_search` and removed, the median read from the middle. O(n × k) for the shifting |
| `sliding_window_median_halves.kara` | the two halves as `SortedMap`s from a number to its count, with their sizes; the largest of the lower half is its `floor(i64.MAX)`, the smallest of the upper half its `ceiling(i64.MIN)`. O(n log k) |
| `sliding_window_median_naive.kara` | every window copied out (`nums[start..start + k].to_vec()`) and sorted. O(n × k log k) |
| `differential.kara` | the four arms on 1,500 random lists, five properties |

Every arm prints the same 9 lines: the two LeetCode examples, the first
again with `k = 4`, one number, two of `2^31 - 1` (whose sum passes
`i32`), `-2^31` twice and then `2^31 - 1` with `k = 2` (a median of
`-0.5`), five equal numbers, one window of six, and for 300 random cases
(1 to 40 numbers from -50 to 50, or from `-2^31` to `2^31 - 1` for one
case in five, with `k` from 1 to the length) the number of windows and
a checksum of twice each median. `sliding_window_median.py` mirrors the
★ arm.

Its output differs from the Kāra arms' in the seven lines with a
whole-number median: Kāra prints `1`, `-1`, `2147483647` where the v1
spec (kara `docs/library/core-types.md` § Printing) and Python print
`1.0`, `-1.0`, `2147483647.0`. That is kara B-2026-10-13-9, open. The
other two lines, the random checksum among them, are byte-identical.

## Differential

`differential.kara` holds copies of the four arms and runs them on
1,500 random lists of 1 to 30 numbers from -50 to 50 (from `-2^31` to
`2^31 - 1` for one list in five), with `k` from 1 to the length.

| | property |
|---|---|
| P1 | every median is the window's middle element, or the mean of its two middle ones, found by counting for each element how many are below it and at or below it |
| P2 | every number negated negates every median |
| P3 | every number plus `d` (from -1000 to 1000) adds `d` to every median |
| P4 | the list reversed reverses the medians |
| P5 | every number doubled doubles every median |

Every value involved is a whole number or a half below `2^33`, so the
comparisons are exact. It prints `1500 cases, 4 arms, 30000 checks, 0
failures` under `karac __mir-run`, in 5.6 s, and a count for each
property when anything fails.

## Mutation testing

Eight edits to `differential.kara`, two to each arm, each run under
`karac __mir-run`. All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: an even window's median is the low top twice over | P1 673, P2 673 |
| M2 | ★: a leaving number equal to the low top is counted out of the high half | the run stops: `unwrap()` on `None` |
| M3 | sorted: an even window's median is the upper middle twice over | P1 673, P2 673 |
| M4 | sorted: the first number never leaves | P1 853, P2 1290, P4 1151 |
| M5 | halves: a number there twice is taken out altogether | the run stops: integer overflow |
| M6 | halves: the high half may hold one more than the low | P1 644, P2 759, P3 30, P4 682, P5 131 |
| M7 | naive: the last window is left out | P1 1500, P4 1209 |
| M8 | naive: an even window's mean in integer division | P1 582, P3 338, P5 582 |

The two heap-based arms keep invariants that one wrong step breaks for
good, so their mutants mostly stop the run: under M2 the size counts
drift until a heap is read empty, and under M5 a half loses a number it
still counts, until a `floor` or `ceiling` finds nothing and its
`i64.MIN` or `i64.MAX` stand-in overflows in the mean. Several more
first drafts did the same, and one survived and was replaced: "a number
equal to the low top goes to the high half", which keeps every
invariant, since equal numbers may sit on either side. M1 and M3 fail
exactly the even windows whose two middle values differ, and P2 sees
them because negating swaps which middle is read twice; P3 to P5 move
both middles alike and cannot. M8 is wrong exactly when the two middle
values have an odd sum; integer division rounds toward zero, down for a
positive sum and up for a negative one, so P2 (negation) never sees it,
P5 (doubling, which makes every sum even) sees every case P1 does, and
P3 only those where adding `d` flips the sign of the sum.

A first draft of the ★ arm wrote `self.gone[x] = self.gone.get(x) ?? 0 +
1;`. `??` binds loosest of all operators (design.md), so that is `?? (0
+ 1)`: a number leaving twice is counted once. It printed a different
random checksum, `886893296`, and was caught by the Python mirror before
the differential existed; the arm writes `(self.gone.get(x) ?? 0) + 1`.
That is the language working as specified, not a finding.

## Verification

All four arms print the same output under `karac __mir-run` (the v2
MIR interpreter) and `karac __mir-llvm-run`, and `karac check` passes
on every file, the bench program included. The differential prints
`30000 checks, 0 failures` on both. The four arms and the differential
also run clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak.

The frozen legacy backends do not agree. `karac run --interp` prints
the eight fixed lines right on the ★ and naive arms and then a
different last line (`3192 windows, checksum 947632941`): as on kata
475, legacy calls `next_random` twice for the bound of `for _ in 0..1 +
next_random(mut seed) % 40 { .. }`, so it draws other lists. LLJIT and
legacy `karac build` crash on the ★ arm and its bench program with a
segmentation fault. The halves arm and the differential do not
type-check on legacy (it reads the keys `SortedMap.floor` returns as
`i64` and refuses `*key`), and its ownership checker refuses the sorted
arm (`cannot move window while a borrow into it ... is still live`).
Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It builds 1,000,000 numbers from
`-2^31` to `2^31 - 1` once, then takes the medians of every window of
1,000 and of 1,001. Every implementation prints `1998001 windows:
checksum 326442419`, the Kāra program under `karac __mir-run` included
(in 180 s).

Every mirror keeps two binary heaps and a hash map of counts for the
numbers that have left: Rust `BinaryHeap` (with `Reverse`) and
`HashMap`, Go `container/heap` and a map, Python `heapq` and a dict,
and in C a heap and an open-addressing table written out by hand,
since C has neither. Spot timings on a shared 4-core container, three
runs each (two for Python; `bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.53 to 0.63 s |
| Rust (`rustc -O`) | 0.76 to 0.82 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.76 to 0.86 s |
| Go | 1.75 to 1.97 s |
| Python | 6.0 to 6.6 s |
| Kāra (`karac build --mir`) | 1.27 to 1.58 s |

The legacy `karac build` builds this program and the binary crashes
with a segmentation fault (see Verification), so `bench.sh` builds the
Kāra program with `karac build --mir`, the v2 compiled backend. That
edit is by hand, on top of the `scripts/new-bench.sh` output. The
`--mir` row is timed at kara `b0b1557b39`. Under
`karac __mir-llvm-run` the program prints the same line in 5.8 s,
compile included; that JITs the MIR's IR without optimization passes,
so it is not a benchmark.

## Compiler findings

- **B-2026-10-13-11** (open): `PriorityQueue.peek` is typed
  `Option[T]` by value, where `docs/library/collections.md` says
  `Option[ref T]`, so `*pq.peek().unwrap()` and `Some(x) => *x` are
  refused by `karac check` and both MIR backends. The ★ arm writes
  `Some(x) => x` and `self.low.peek().unwrap()`, which are accepted;
  they go back to `*` when the row is fixed.
- B-2026-10-13-9 (open), see Approaches: whole-number floats print
  without `.0`.
