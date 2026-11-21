# 1708. Largest Subarray Length K

An array `A` is larger than some array `B` if for the first index `i`
where `A[i] != B[i]`, `A[i] > B[i]`. For example, `[1,3,2,4] > [1,2,2,4]`,
since at index `1`, `3 > 2`, and `[1,4,4,4] < [2,1,1,1]`, since at index
`0`, `1 < 2`.

A subarray is a contiguous subsequence of the array.

Given an integer array `nums` of **distinct** integers, return *the
**largest** subarray of* `nums` *of length* `k`.

```
nums = [1,4,5,2,3], k = 3   ->  [5,2,3]
nums = [1,4,5,2,3], k = 4   ->  [4,5,2,3]
nums = [1,4,5,2,3], k = 1   ->  [5]
```

**Constraints:** `1 <= k <= nums.length <= 10^5`; `1 <= nums[i] <= 10^9`;
all the integers of `nums` are unique. A premium problem: LeetCode gives
no public Rust template, so all four arms are written in Kāra.

## Approaches

| file | mechanism |
|---|---|
| `largest.kara` ★ | the values are distinct, so two subarrays of length k differ at their first values unless they start at the same place: the answer starts at the largest value among the starts 0 to n - k. O(n) |
| `largest_compare.kara` | every window of length k collected into a `Vec` and kept if it is `>` the best so far; `Vec`s compare the way the statement defines. O(n * k) |
| `largest_windows.kara` | `nums.windows(k).iter().max()`, slices comparing by their first differing value. O(n * k) at worst |
| `largest_scan.kara` | a candidate start against the best one, a value at a time until they differ, by hand; the follow-up's answer, as it does not need the values distinct. O(n * k) at worst |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 8 lines: LeetCode's three examples, all of an
array, and an array whose largest value is last; then the first values
summed and a checksum of every answer for 3000 random arrays of up to
10 distinct values, 300 of up to 1000 and 10 of up to `10^5`, each with
a random k. `largest.py` mirrors the ★ arm and its output is
byte-identical.

```
[5, 2, 3]
[4, 5, 2, 3]
[5]
[3, 1, 2]
[2, 9]
3000 arrays of up to 10 values: first values sum to 157711, checksum 757585065
300 arrays of up to 1000 values: first values sum to 1459432, checksum 166434442
10 arrays of up to 100000 values: first values sum to 6518304, checksum 346461742
```

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every contiguous subarray of length k, each compared with the
best so far at the first index where they differ, the larger value there
deciding. It checks 3000 random arrays, a shuffle of 1 to n for n from 1
to 8, each with a random k. Every case is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | every value raised by 1000 raises every value of the answer by 1000 |
| P3 | the answer holds k values and is a subarray of `nums` |
| P4 | a value below all the others put in front changes nothing |
| P5 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 147790085, 60000 checks
over 4 arms: 0 failures` under every lane in Verification, and a Python
reading of the statement, the `max` of the slices, gives the same
checksum. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. None fails P2, since adding the same
to every value keeps every comparison. M1, M4 and M6 each choose the
smallest subarray, and fail the very same checks; M2 and M5 both never
look at the last start, and fail the same checks too.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: `<` for `>` | P1 1973, P4 3000, P5 1973 |
| M2 | ★: the last start left out | P1 654, P4 1027, P5 654 |
| M3 | ★: the answer taken from the first start | P1 1335, P4 3000, P5 1335 |
| M4 | compare: `<` for `>` | P1 1973, P4 3000, P5 1973 |
| M5 | compare: each window one start early | P1 654, P4 1027, P5 654 |
| M6 | windows: `min()` for `max()` | P1 1973, P4 3000, P5 1973 |
| M7 | windows: the last window taken | P1 1319, P5 1319 |
| M8 | scan: the last value never compared | P1 434, P4 1014, P5 434 |
| M9 | scan: a smaller value read as equal | P1 784, P5 784 |
| M10 | scan: every value of the answer its first | P1 1986, P3 1986, P5 1986 |

## Benchmarks

The bench draws 50 random arrays of `10^5` distinct values below `10^9`,
LeetCode's largest, each with a random k, all of them first, then
answers each 100 times by the ★ arm in all five languages; the sink
folds each answer's length and its first and last values. Every
implementation prints `50 arrays of 100000 values, 100 rounds:
262345100 chosen, checksum 665913215`. The C mirror copies the answer
into a new array, as the other languages return one. The C build also
runs clean under gcc's AddressSanitizer and UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `9b0b5eb92c` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.168 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.260 s |
| Kāra (`karac build`) | 0.263 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.293 s |
| Rust (`rustc -O`) | 0.323 s |
| Go | 0.503 s |
| Python | 33 s |

The sequential Kāra build is 20% faster than Rust and 11% faster than
Rust with overflow checks on, the equal-safety comparison
(BENCHMARKS.md). C is the fastest here at 0.168 s.

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here:
its user time is not above its real time (0.204 s and 0.213 s on one
run).

## Verification

All four arms print the same output as `largest.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `21cdf88b69`.

## Writing it

The ★, compare and scan arms and the differential checked clean as first
written.

The windows arm's first draft called `max()` on `nums.windows(k)`
straight. `karac check` said `max` is an iterator method and to write
`.iter().max()`, and `karac fix` did; with it, `max()` over the
`Slice[i32]` windows compares them as the statement does. The same
check also said `max()` needs a numeric or `String` element, found
`Slice[i32]`, which the fix shows is not so. Since kara `93fd9b2078`
(B-2026-11-20-41) that second error is not reported.

`arm_name` in the differential indexes a list of string literals for a
`Str`, as #1662's does (B-2026-11-19-131).
