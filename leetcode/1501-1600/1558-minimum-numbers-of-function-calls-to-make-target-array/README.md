# 1558. Minimum Numbers of Function Calls to Make Target Array

You are given an integer array `nums`. You have an integer array `arr` of
the same length with all values set to `0` initially. In one function
call you can either add `1` to one value of `arr`, or double every value
of `arr`. Return the minimum number of function calls to make `arr` equal
to `nums`.

```
nums = [1, 5]         ->  5
nums = [2, 2]         ->  3
nums = [4, 2, 5]      ->  6
```

**Constraints:** `1 <= nums.length <= 10^5`; `0 <= nums[i] <= 10^9`.

## Approaches

A doubling is shared by every value and an increment belongs to one, so
each value's 1 bits are its increments, and the doublings are as many as
the widest value needs: its length in bits less one.

| file | mechanism |
|---|---|
| `calls.kara` ★ | `count_ones` of every value summed, and `64 - leading_zeros` of the widest nonzero value, less one. O(n) |
| `calls_backward.kara` | the calls run backwards from the target: every odd value has 1 taken off (one call each), and while anything is left everything is halved (one call). O(n log max) |
| `calls_fold.kara` | one `fold` over the values with `(ones, most)` as its state, each value taken apart bit by bit with `& 1` and `>>= 1`, its 1 bits added and its shifts kept at the most. O(n log max) |
| `calls_solution.kara` | LeetCode's Rust template (`min_operations(nums: Vec<i32>) -> i32`, the ★ arm with `u32` counts and `saturating_sub(1)`), carried by `karac fix` and one hand edit |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 12 lines: LeetCode's five examples, then `[0]`,
`[0, 0, 1]`, `[10^9]` and `[10^9, 10^9 - 1, 1]`; then the total and a
checksum of the answers for 3000 random arrays of up to 8 values up to
30, 300 of up to 1000 values up to `10^9` and 30 of up to 100000.
`calls.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: from all zeros, the two calls searched breadth first, every
array that still fits under the target kept, and the first time the
target comes out the answer. It checks 3000 arrays of 1 to 3 values from
0 to at most 12, every random choice drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer is 0 exactly when every value is, and at most their sum |
| P3 | the values reversed leave the answer |
| P4 | every value doubled needs one call more (none, when all are 0) |
| P5 | a 0 put after the values leaves the answer, and a 1 adds one call |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 178205738, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. Three first choices were equivalent and
were replaced: the ★ arm skipping a value of 1 as well as 0 (its length
less one is 0 either way), and the backward arm stopping when every value
is at most 1, or halving `(v + 1) / 2` (both see only even values).

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: every length one bit short | P1 2299, P4 458, P6 2299 |
| M2 | ★: the doublings the widest length, not one less | P1 2757, P2 964, P5 243, P6 2757 |
| M3 | ★: the last value's length kept, not the widest | P1 568, P3 973, P5 2069, P6 568 |
| M4 | backward: stopping when every value is at most 2 | P1 2299, P2 248, P4 458, P6 2299 |
| M5 | backward: a decrement costing no call | P1 2757, P2 458, P5 3000, P6 2757 |
| M6 | backward: a halving costing a call per value | P1 1675, P2 688, P4 1957, P5 2299, P6 1675 |
| M7 | fold: a shift counted past the top bit | P1 2757, P2 964, P5 243, P6 2757 |
| M8 | fold: the shifts summed, not the most kept | P1 1147, P4 1587, P6 1147 |
| M9 | template: `saturating_sub(0)` | P1 2757, P2 964, P5 243, P6 2757 |
| M10 | template: one increment per value | P1 2083, P2 584, P4 243, P5 3000, P6 2083 |

## Benchmarks

The bench builds 20 arrays of 100000 values once, each value below
`2^b` for its own `b` from 1 to 30, and asks each 30 times by the ★ arm,
in all five languages. C uses `__builtin_popcountll` and
`__builtin_clzll`, Go `math/bits`. Every implementation prints `30 passes
over 20 arrays of 100000 values: 464728800 calls, checksum 976600641`.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `5a1b79539` on LLVM 22:

| | median |
|---|---|
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.104 s |
| Kāra (`karac build`) | 0.106 s |
| C (`clang -O3`) | 0.141 s |
| Go | 0.141 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.142 s |
| Rust (`rustc -O`) | 0.145 s |
| Python | 15.9 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time is below its real time (0.095 s and 0.100 s on one run).

Kāra is 0.73x Rust under overflow checks by median, and that is the
instruction set, not the code: Kāra builds for x86-64-v3, which has
`popcnt` and `lzcnt`, and the baseline C and Rust count bits in software.
Built for x86-64-v3 too (`bench.sh`'s matched-ISA twins), in a separate
run of eight, C was 0.094 s, Rust 0.094 s, Rust under overflow checks
0.096 s and Kāra 0.103 s: 1.07x Rust under overflow checks. Not traced.

## Verification

All four arms print the same output as `calls.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them and the differential. `karac check` reports nothing on any of them,
and `karac fix` has nothing left to change. Checked at kara `5a1b79539`.

## Writing it

The ★, backward and fold arms were written in Kāra and checked as
written.

The Rust template took 4 changed lines, then 1 added, then 1 changed,
over three rounds of `karac fix`: the `Vec<i32>` type to `Vec[i32]`,
`for &x` to `for x`, the wrapper's `|&x|` to `|x|` and `Solution::` to
`Solution.`; then `struct Solution {}` added; then the wrapper's closing
`as i64` dropped. Two refusals were left that `karac fix` does not
change, because Kāra's `count_ones` and `leading_zeros` give an `i64`
where Rust's give a `u32`:

- `ones += x.count_ones()` into the template's `ones: u32` is refused as
  an implicit narrowing, the message asking for an explicit `as u32`;
- `max_bits.max(32 - x.leading_zeros())` is refused with `max expects an
  argument of type u32, got i64`, naming nothing.

A bit count always fits a `u32`, so `as u32` keeps the port's meaning and
is a safe fix-it, but neither refusal carries one; filed as
B-2026-11-14-14. The two lines were edited by hand to `as u32`. The other
way out, the counts retyped to `i64`, checks but is wrong: the template's
closing `max_bits.saturating_sub(1)` then saturates at `i64::MIN`, not 0,
so `[0]` answers -1. It checks and agrees after the hand edit.
