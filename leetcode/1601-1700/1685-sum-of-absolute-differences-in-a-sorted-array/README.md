# 1685. Sum of Absolute Differences in a Sorted Array

You are given an integer array `nums` sorted in **non-decreasing** order.

Build and return *an integer array* `result` *with the same length as*
`nums` *such that* `result[i]` *is equal to the **summation of absolute
differences** between* `nums[i]` *and all the other elements in the
array.*

In other words, `result[i]` is equal to `sum(|nums[i]-nums[j]|)` where
`0 <= j < nums.length` and `j != i` (**0-indexed**).

```
nums = [2,3,5]          ->  [4,3,5]
nums = [1,4,6,8,10]     ->  [24,15,13,15,21]
```

**Constraints:** `2 <= nums.length <= 10^5`; `1 <= nums[i] <= nums[i + 1] <= 10^4`.

## Approaches

| file | mechanism |
|---|---|
| `absolute.kara` ★ | the values before i are at most `nums[i]` and those after at least, so the answer is `nums[i] * i` less the sum before plus the sum after less `nums[i] * (n - 1 - i)`; one pass carries the sum before, and the sum after is the total less it and `nums[i]`. O(n) |
| `absolute_steps.kara` | the first answer is the sum less n times the first value; a step of d from i - 1 to i takes i values d further and n - i values d nearer, so each answer is the one before plus `d * (2i - n)`. O(n) |
| `absolute_prefix.kara` | a prefix-sum table built by `scan` (`once(0).chain(..)`), and every answer read from it in one `map` over the values with their indexes. O(n) |
| `absolute_solution.kara` | a Rust solution as LeetCode's Rust users write it, the total by `sum()` and the sum to the left carried through a `map` closure, carried to Kāra by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 8 lines: LeetCode's two examples, three equal
values, the two values furthest apart, and a run of each of three
values; then the answers' values summed and a checksum for 3000 random
sorted arrays of up to 12 values up to 10, 300 of up to 1000 up to
`10^4` and 10 of up to `10^5` up to `10^4`. `absolute.py` mirrors the ★
arm and its output is byte-identical.

```
[4, 3, 5]
[24, 15, 13, 15, 21]
[0, 0, 0]
[9999, 9999]
[11, 11, 9, 9, 9, 37]
3000 arrays of up to 12 values up to 10: answers sum to 523712, checksum 193761311
300 arrays of up to 1000 values up to 10000: answers sum to 350509665266, checksum 387356436
10 arrays of up to 100000 values up to 10000: answers sum to 10406158883254, checksum 708036931
```

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: for each i, `|nums[i] - nums[j]|` summed over every j (the
j = i term is 0). It checks 3000 random sorted arrays of 2 to 12 values
from 1 to between 1 and 20, each with an amount from 1 to 100 to raise
them by. Every case is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | every value raised by the same amount gives the same answer |
| P3 | the array mirrored, v written top + 1 - v in reverse order, gives the answer reversed |
| P4 | every value written twice gives every answer doubled, twice |
| P5 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 916948683, 60000 checks
over 4 arms: 0 failures` under every lane in Verification, and a Python
reading of the statement gives the same checksum. On a failure it prints
the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. A first M8 kept only the newest value
as the prefix table's running state (`let sum = x;`), a `ref i32` where
the state is an `i32`; `karac check` refuses it on both backends before
any check runs (E0200), so it was replaced by one that compiles.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the sum before holds only the last value | P1 2741, P2 2741, P3 2741, P4 3000, P5 2741 |
| M2 | ★: the sum after counts `nums[i]` too | P1 3000, P2 3000, P3 2852, P4 3000, P5 3000 |
| M3 | ★: one value too many after i | P1 3000, P2 3000, P3 2852, P4 3000, P5 3000 |
| M4 | steps: the first answer takes n - 1 times the first value | P1 3000, P2 3000, P3 1740, P4 3000, P5 3000 |
| M5 | steps: each step grows by `d * (2i - n + 1)` | P1 2807, P3 2807, P4 2807, P5 2807 |
| M6 | steps: d measured from the first value | P1 2550, P3 2599, P4 2807, P5 2550 |
| M7 | prefix: the sum after counts `nums[i]` too | P1 3000, P2 3000, P3 2852, P4 3000, P5 3000 |
| M8 | prefix: the running state counts each value twice | P1 3000, P2 3000, P3 3000, P4 3000, P5 3000 |
| M9 | solution: one value too many to the right | P1 3000, P2 3000, P3 2852, P4 3000, P5 3000 |
| M10 | solution: the index one more | P1 3000, P2 3000, P3 2852, P4 3000, P5 3000 |

## Benchmarks

The bench draws 50 sorted arrays of `10^5` values up to `10^4`,
LeetCode's largest, all of them first, then answers each 20 times by the
★ arm in all five languages, each building a new array per answer; the
sink folds each answer's first, middle and last values. Every
implementation prints `50 arrays of 100000 values, 20 rounds: middles
sum to 257522275080, checksum 291226947`. The C build also runs clean
under gcc's AddressSanitizer and UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `9b0b5eb92c` on LLVM 22:

| | median |
|---|---|
| Rust (`rustc -O`) | 0.181 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.261 s |
| Kāra (`karac build`) | 0.267 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.285 s |
| Go | 0.530 s |
| C (`clang -O3`) | 0.538 s |
| Python | 21 s |

The sequential Kāra build takes 1.44x Rust's time and 0.92x that of Rust
with overflow checks on, the equal-safety comparison (BENCHMARKS.md).

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here:
its user time is not above its real time (0.279 s and 0.285 s on one
run).

## Verification

All four arms print the same output as `absolute.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `9b0b5eb92c`.

## Writing it

The ★ arm's first draft began `let mut before = 0` and an unannotated
`Vec.with_capacity(n)`, and pushed `x * i - ..`, an `i32` value times an
`i64` index. The product widens to `i64`, so the vector took `i64`
elements and the return refused it (E0200, naming the binding);
`karac fix` annotated `before: i32` and `result: Vec[i32]`. The push of
an `i64` into it was then refused as a narrowing, which `karac fix`
leaves to the author by design, and an `as i32` was written by hand.

The steps arm wrote Rust's `vec![0; n]` and `sum::<i32>()`; `karac fix`
wrote `Vec.filled(n, 0)` and dropped the turbofish (E0001), the type
coming from the subtraction.

The prefix arm's `scan` closure wrote its state through `*sum`, as
Rust's lends it; Kāra's takes the state by value and returns
`Some((next_state, item))`, the refusal names that rewrite, and `karac
fix` wrote it with a `0i32` seed. Its `map` then made `i64` values, the
same `i64` index, and the `collect` into `Vec[i32]` was refused
(`FromIterator[i64]`); an `as i32` was written by hand.

LeetCode's Rust solution took one `karac fix` of 8 edits:
`struct Solution {}` added, both `Vec<i32>` written `Vec[i32]`, the
`&x` pattern written `x`, `let mut left = 0` given `: i32`, and the
harness's `nums.clone()` passed as `nums` (`redundant_clone`); its
`as i32` on the index made every product an `i32` already.

The differential's literal summed into `let mut sum = 0` the same way,
and `karac fix` gave it `: i32` and its vector `Vec[i32]`. `arm_name`
indexes a list of string literals for a `Str`, as #1662's differential
does (B-2026-11-19-131).
