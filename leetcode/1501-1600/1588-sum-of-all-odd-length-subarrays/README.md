# 1588. Sum of All Odd Length Subarrays

Given an array of positive integers `arr`, return the sum of all possible
odd-length subarrays of `arr`.

A subarray is a contiguous subsequence of the array.

```
arr = [1,4,2,5,3]  ->  58
arr = [1,2]        ->  3
arr = [10,11,12]   ->  66
```

**Constraints:** `1 <= arr.length <= 100`; `1 <= arr[i] <= 1000`.

## Approaches

| file | mechanism |
|---|---|
| `odd_subarrays.kara` ★ | each value counted once for every odd-length subarray holding it: of the `(i + 1) (n - i)` subarrays through place `i`, `((i + 1) (n - i) + 1) / 2` have odd length. O(n) |
| `odd_subarrays_prefix.kara` | prefix sums in a `Vec.filled`, every odd length from every start, each sum one subtraction. O(n^2) |
| `odd_subarrays_windows.kara` | the statement as one iterator chain: `(1..n + 1).step_by(2)`, every `windows(len)`, each window summed. O(n^3) |
| `odd_subarrays_solution.kara` | LeetCode's Rust template (a running sum from each start, `(j - i) % 2 == 0` for an odd length), carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's three examples and three
more (one value, four ones, a hundred values of 1000), then the total and
a checksum for 3000 random arrays of up to 10 values up to 10, 300 of up
to 100 values up to 1000, and 30 of exactly 100. `odd_subarrays.py`
mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every subarray, its length tested, its values added one by
one. It checks 3000 arrays of 1 to 12 values from 1 to 9, each with a
second array of the same length for P5, every random choice drawn before
any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the array reversed leaves the answer |
| P3 | every value doubled doubles the answer |
| P4 | every value raised by 1 adds the answer for `n` ones |
| P5 | the answer for two arrays added place by place is the sum of theirs |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 820862779, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the count of odd subarrays rounded down without the `+ 1` | P1 1502, P6 1502 |
| M2 | ★: `i` for `i + 1` subarray starts | P1 3000, P2 2615, P6 3000 |
| M3 | ★: the value left out of each term | P1 2969, P3 3000, P4 3000, P5 3000, P6 2969 |
| M4 | prefix: every length, not every odd one | P1 2750, P6 2750 |
| M5 | prefix: each sum one place short | P1 3000, P2 2401, P6 3000 |
| M6 | prefix: the longest odd length skipped | P1 1502, P6 1502 |
| M7 | windows: `step_by(1)`, every length | P1 2750, P6 2750 |
| M8 | windows: the whole array never taken | P1 1502, P6 1502 |
| M9 | template: even lengths added, not odd | P1 1502, P6 1502 |
| M10 | template: each start's own value skipped | P1 3000, P2 2401, P6 3000 |

## Benchmarks

The bench runs the ★ arm on 200000 arrays of 1 to 100 values up to 1000,
all drawn first, in all five languages. Every implementation prints
`200000 arrays of 1 to 100 values: total 2204633607827, checksum
397965496`. In the C mirror each array is its own malloc.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `5dc4418bbd` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.062 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.072 s |
| Rust (`rustc -O`) | 0.077 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.087 s |
| Kāra (`karac build`) | 0.091 s |
| Go | 0.132 s |
| Python | 4.1 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here:
its user time is below its real time (0.052 s and 0.084 s on one run).

## Verification

All four arms print the same output as `odd_subarrays.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them, the differential and the bench. `karac check` reports nothing on
any of them, and `karac fix` has nothing left to change. Checked at kara
`5dc4418bbd`.

## Writing it

The ★ and prefix arms each took one `karac fix`: `let mut total = 0`
typed `i32` (an integer literal keeps the `i64` default when only an
operator uses it, so returning it as the `i32` answer is a narrowing),
and the prefix arm's `Vec.filled(n + 1, 0)` given `0i32`. The harness
first passed `arr.clone()`, which `karac fix` dropped: the parameter only
borrows.

The windows arm first wrote Rust's `sum::<i32>()` turbofish twice and
`arr.windows(len).map(..)`; `karac fix` took two rounds, dropping the
turbofish and then adding the `.into_iter()` that a `Vec` of windows
needs before `map`.

The Rust template took two rounds of `karac fix`:

1. `struct Solution;` to `struct Solution {}`, `Vec<i32>` to `Vec[i32]`
   in both signatures, and `Solution::` to `Solution.`;
2. `let mut ans = 0` and `let mut sum = 0` typed `i32`.

It then checks and agrees with no hand edit.
