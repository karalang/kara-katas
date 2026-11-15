# 1574. Shortest Subarray to be Removed to Make Array Sorted

Given an integer array `arr`, remove a subarray (can be empty) from `arr`
such that the remaining elements in `arr` are non-decreasing. Return the
length of the shortest subarray to remove. A subarray is a contiguous
subsequence of the array.

```
arr = [1,2,3,10,4,2,3,5]   ->  3
arr = [5,4,3,2,1]          ->  4
arr = [1,2,3]              ->  0
```

**Constraints:** `1 <= arr.length <= 10^5`; `0 <= arr[i] <= 10^9`.

## Approaches

| file | mechanism |
|---|---|
| `shortest.kara` ★ | what is kept is a sorted prefix and a sorted suffix that joins it: the longest sorted prefix and suffix found, then two pointers, the suffix's start moved right for each end of the prefix until its first value is not below the prefix's last. O(n) |
| `shortest_search.kara` | the same prefix and suffix, the suffix joined by `partition_point` over `arr[right..]` in place of a pointer that walks. O(n log n) |
| `shortest_window.kara` | a binary search on the answer: a window of length `L` can go when one starts inside the sorted prefix's reach, ends inside the sorted suffix's, and joins a prefix value to a suffix value not below it; a longer window works whenever a shorter one does. O(n log n) |
| `shortest_solution.kara` | LeetCode's Rust template (`find_length_of_shortest_subarray(arr: Vec<i32>) -> i32`, the suffix first, then one loop that walks the prefix), carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 10 lines: LeetCode's three examples, then
`[1]`, `[2, 2, 2, 1, 1, 1]` and two longer ones; then the sum of the
answers and a checksum for 3000 random arrays of 1 to 10 values, 300 of
up to 1000 and 30 of up to 100000, each a rising run with its own odds
of a fall at each step. `shortest.py` mirrors the ★ arm and its output
is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every subarray removed in turn, the empty one included, and
the shortest whose removal leaves the rest sorted. It checks 3000 arrays
of 1 to 10 values from 0 to 5, every random choice drawn before any arm
answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer is at most `n - 1`, and 0 exactly when the array is sorted |
| P3 | every value doubled leaves the answer |
| P4 | the array reversed and each value `v` made `5 - v` leaves the answer |
| P5 | a value at least the largest put at the end leaves the answer |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 233807587, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends.

Two first tries at M5 were equivalent and were replaced: the suffix
search stopping at index 1 rather than 0 (the whole array sorted has
already returned 0), and the removed suffix starting one value longer
(the loop's last prefix end finds it anyway).

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the suffix pointer passes equal values | P1 280, P5 276, P6 280 |
| M2 | ★: the start the larger of the two one-sided removals | P1 427, P4 835, P6 427 |
| M3 | ★: the prefix's last value never tried | P1 299, P4 262, P5 408, P6 299 |
| M4 | search: the search passes equal values | P1 280, P5 276, P6 280 |
| M5 | search: the prefix's first value never tried | P1 176, P4 281, P6 176 |
| M6 | window: the join wants a strict rise | P1 280, P5 276, P6 280 |
| M7 | window: the suffix not required sorted | P1 2418, P2 2418, P6 2418 |
| M8 | window: the search steps one past a length that fails | P1 1765, P2 321, P5 642, P6 1765 |
| M9 | template: the prefix walk wants a strict rise | P1 419, P4 811, P6 419 |
| M10 | template: each window counted one longer | P1 1168, P4 1350, P6 1168 |

## Benchmarks

The bench builds 20 arrays of 500000 values once, each a rising first
half, a stretch of up to 1000 random values, and a rising second half
that starts low, so about half of each array goes and the two pointers
walk all of it; then it answers all 20 three times over, 60 answers, by
the ★ arm, in all five languages. Every implementation prints `60
answers over 20 arrays of 500000 values: lengths total 14986209,
checksum 968275709`.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `572956a03` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.238 s |
| Rust (`rustc -O`) | 0.264 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.275 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.275 s |
| Kāra (`karac build`) | 0.269 s |
| Go | 0.538 s |
| Python | 7.7 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time is below its real time (0.224 s and 0.262 s on one run).

Kāra is 1.00x Rust under overflow checks by median.

## Verification

All four arms print the same output as `shortest.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them and the differential. `karac check` reports nothing on any of them,
and `karac fix` has nothing left to change. Checked at kara `572956a03`.

## Writing it

The ★ and search arms were written in Kāra and checked as written. The
window arm was first written with Rust's `|len: i64| -> bool { .. }`,
whose return type `karac check` refuses as a parse error naming the
edit, and `karac fix` removed it in one round. The differential's
`is_sorted` was first written `v.windows(2).all(..)`; `windows` gives a
`Vec`, and `karac fix` added the `.into_iter()` the message names.

The Rust template took two rounds of `karac fix`, 6 changed lines, then
1:

1. the `Vec<..>` types to `[..]`, `&&` and `||` to `and` and `or`, the
   wrapper's `|&x|` to `|x|`, and `Solution::` to `Solution.`;
2. the wrapper's `as i64` dropped (an `i32` widens to `i64` on its own).

It then checks and agrees with no hand edit.
