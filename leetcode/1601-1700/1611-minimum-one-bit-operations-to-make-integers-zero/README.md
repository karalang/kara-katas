# 1611. Minimum One Bit Operations to Make Integers Zero

Given an integer `n`, you must transform it into `0` using the following
operations any number of times:

- Change the rightmost (`0th`) bit in the binary representation of `n`.
- Change the `ith` bit in the binary representation of `n` if the
  `(i-1)th` bit is set to `1` and the `(i-2)th` through `0th` bits are
  set to `0`.

Return *the minimum number of operations to transform* `n` *into* `0`*.*

```
n = 3  ->  2
n = 6  ->  4
```

**Constraints:** `0 <= n <= 10^9`.

## Approaches

The two operations are the steps of the reflected Gray code: the first
flips bit 0, the second flips the bit just above the lowest set bit. So
`n` is the Gray code of some `k`, and the moves to zero are `k` steps.

| file | mechanism |
|---|---|
| `one_bit.kara` ★ | `n` turned back from Gray code: the XOR of `n` and all its right shifts, in a `while` loop. O(log n) |
| `one_bit_recursive.kara` | recursion on the top bit: `2^b` takes `2^(b+1) - 1` moves, so `2^b + r` takes `2^(b+1) - 1 - f(r)`; the top bit from `leading_zeros`. O(log n) |
| `one_bit_signs.kara` | that recursion unrolled: each set bit, highest first, adds or takes away `2^(b+1) - 1` in turn, as an iterator chain (`rev`, `filter`, `enumerate`, `map`, `sum`). O(log n) |
| `one_bit_solution.kara` | a Rust solution as LeetCode's Rust users write it (a loop down from `i32::BITS - n.leading_zeros()` with a sign that flips), carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 10 lines: LeetCode's two examples and six more
(0, 1, 2, a power of two, all ones and the largest `n` allowed), then the
most moves and a checksum for every `n` below 4096, and the total and a
checksum for 100000 random `n` up to 10^9. `one_bit.py` mirrors the ★
arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: a breadth-first search from 0 over the two operations on 13
bits, so every `n` below 8192 has its fewest moves in a table. It checks
3000 numbers, half below 8192 and half up to 10^9, every random choice
drawn before any arm answers.

| | property |
|---|---|
| P1 | below 8192, the answer is the statement read literally |
| P2 | with `n` below `2^b`, `b` its bit length and at most 29, `n + 2^b` takes `2^(b+1) - 1 - f(n)` |
| P3 | `n ^ (n >> 1)` takes `n` |
| P4 | the answer is odd exactly when `n` has an odd count of set bits |
| P5 | for `n` above 0, the answer has `n`'s bit length |
| P6 | each arm agrees with at least two of the other three |

P3 is the Gray code read forwards; P4 holds because each move flips one
bit; P5 because the moves never pass the top bit.

The differential prints `3000 problems: checksum 243141468, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two to three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. The first M4 tried, the top bit taken
one too low, recursed forever and overflowed the stack, so it was
replaced.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the shifts ORed in, not XORed | P1 1520, P2 2350, P3 2998, P4 1488, P6 2997 |
| M2 | ★: `n` shifted by two each time | P1 1523, P2 2350, P3 3000, P4 1543, P6 3000 |
| M3 | ★: the loop stopping at 1 | P1 1523, P3 3000, P4 3000, P6 3000 |
| M4 | recursive: the remainder shifted right before the call | P1 1520, P2 2350, P3 2998, P4 1476, P6 2997 |
| M5 | recursive: `2^(b+1)` taken for `2^(b+1) - 1` | P1 770, P2 2350, P3 1500, P4 1512, P5 3, P6 1512 |
| M6 | recursive: 0 taking one move | P1 1523, P3 3000, P4 3000, P6 3000 |
| M7 | signs: each bit worth `2^b - 1` | P1 1523, P2 2350, P3 3000, P4 1500, P5 3000, P6 3000 |
| M8 | signs: the signs the other way round | P1 1523, P2 2350, P3 3000, P4 1512, P5 3000, P6 3000 |
| M9 | template: the top bit skipped | P1 1523, P2 2350, P3 3000, P4 3000, P5 3000, P6 3000 |
| M10 | template: the sign never flipped | P1 1520, P2 2350, P3 2998, P5 2997, P6 2997 |

## Benchmarks

The bench makes 10000000 numbers up to 10^9, all of it first. Then: each turned back from Gray code by XOR of its right shifts. Every implementation prints `10000000 numbers up to 10^9: total 4909944541240361, checksum 249418745`.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `5bb1708545` on LLVM 22:

| | median |
|---|---|
| Rust (`rustc -O`) | 0.178 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.180 s |
| Kāra (`karac build`) | 0.182 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.183 s |
| C (`clang -O3`) | 0.199 s |
| Go | 0.244 s |
| Python | 15 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its user time is not above its real time (0.173 s and 0.201 s on one run).

## Verification

All four arms print the same output as `one_bit.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them, the differential and the bench. `karac check` reports nothing on
any of them, and `karac fix` has nothing left to change. Checked at kara
`5bb1708545`.

## Writing it

The template's `i32::BITS` was refused: the integer types had `MAX` and
`MIN` but not Rust's `BITS` ("no associated constant `BITS` on `i32`;
its constants are MAX, MIN"). It is now a constant of every integer type,
an `i64` as every count is in Kāra, so `i32.BITS - n.leading_zeros()`
needs no cast (B-2026-11-18-9).

The ★ arm wrote `let mut k = 0`, XORed with the `i32` `n` and returned,
and `karac fix` typed it `let mut k: i32 = 0`. The harness, the same in
every arm, walked `[3, 6, 0, ...]` and passed each to the `i32`
parameter, and `karac fix` wrote the first `3i32`; it also took off three
`ops as i64` casts, since an `i32` widens to `i64` by itself.

The Rust template took one `karac fix` of 9 edits: `struct Solution;` to
`struct Solution {}`, `let mut ans = 0` and `let mut sign = 1` typed
`i32`, `i32::BITS` and `Solution::` to `.`, and the harness's four. It
then checks and agrees with no hand edit.
