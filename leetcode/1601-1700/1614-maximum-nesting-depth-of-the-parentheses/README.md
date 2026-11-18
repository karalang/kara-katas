# 1614. Maximum Nesting Depth of the Parentheses

Given a **valid parentheses string** `s`, return the **nesting depth** of
`s`. The nesting depth is the **maximum** number of nested parentheses.

A valid parentheses string is defined over digits, `'+'`, `'-'`, `'*'`,
`'/'`, `'('` and `')'`; its nesting depth is `depth("") = 0`,
`depth(C) = 0` for a single character other than a parenthesis,
`depth(A + B) = max(depth(A), depth(B))` for two such strings side by
side, and `depth("(" + A + ")") = 1 + depth(A)`.

```
s = "(1+(2*3)+((8)/4))+1"  ->  3
s = "(1)+((2))+(((3)))"    ->  3
```

**Constraints:** `1 <= s.length <= 100`; `s` consists of digits
`0-9` and the characters `'+'`, `'-'`, `'*'`, `'/'`, `'('` and `')'`;
it is guaranteed that `s` is a valid parentheses string.

## Approaches

| file | mechanism |
|---|---|
| `depth.kara` ★ | one pass over `s.chars()`, counting the parentheses open and keeping the most: in a valid string the open count at a character is its nesting depth. O(n) |
| `depth_scan.kara` | an iterator chain over `s.bytes()`: each byte mapped to +1, -1 or 0 by a `match` on byte literals, a running sum by `scan`, and its `max`. O(n) |
| `depth_stack.kara` | a stack of the open parentheses' positions, from `char_indices`, pushed and popped as a parser would; the deepest the stack goes is the answer. O(n) time and space |
| `depth_solution.kara` | LeetCode's Rust template (`s.chars().fold` over a `(depth, most)` pair, `m.max(d + 1)`, `.1`), carried by `karac fix` and one hand edit |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's two examples and four more
(a bare digit, one pair, a chain six deep, and two pairs side by side),
then the characters, the deepest and a checksum for 3000 random
expressions of up to 6 terms, 300 of up to 1000 terms, and 3 of up to
100000 terms, past LeetCode's bound. Each expression is terms joined by
operators, each term a digit or, while the size allows, an expression in
parentheses. `depth.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: the four rules of the definition, the string split at the end
of its first character or first parenthesized group. It checks 3000
random expressions of 1 to 8 terms, every random choice drawn before any
arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the string in one more pair of parentheses is one deeper |
| P3 | the string twice, joined by `+`, leaves the answer |
| P4 | every character but the parentheses removed leaves the answer |
| P5 | the string reversed, each parenthesis turned round, leaves the answer |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 231023253, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. M2, M4 and M8, which never close a
parenthesis, give the count of `(` instead of the depth: P1 kills them
only where two groups stand side by side, and P3, the string twice, is
what kills them throughout.

The first M5, the scan arm's answer capped by `.min(3)`, did not compile
(the `min` settles the literal to `i64`, B-2026-11-17-129) and was
replaced.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the most never kept | P1 1938, P2 3000, P6 1938 |
| M2 | ★: a `)` closing nothing | P1 584, P3 1938, P6 584 |
| M3 | ★: the most kept before the count goes up | P1 1938, P2 1062, P6 1938 |
| M4 | scan: a `)` counted as 0 | P1 584, P3 1938, P6 584 |
| M5 | scan: each step's own size yielded, not the running sum | P1 867, P2 1938, P6 867 |
| M6 | stack: the last open parenthesis never popped | P1 373, P2 373, P3 1565, P5 215, P6 373 |
| M7 | stack: a `+` pushed as if it opened | P1 1401, P3 3000, P4 1401, P5 904, P6 1401 |
| M8 | template: a `)` leaving the depth | P1 584, P3 1938, P6 584 |
| M9 | template: the most taken before the step | P1 1938, P2 1062, P6 1938 |
| M10 | scan: a `(` counted as 2 | P1 1938, P2 3000, P3 1938, P5 252, P6 1938 |

## Benchmarks

The bench makes 10 random expressions of 200000 terms, all of it first. Then: each read 10 times by one pass counting open parentheses. Every implementation prints `10 expressions of 200000 terms, each read 10 times: 54333160 characters, checksum 359966919`.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `5bb1708545` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.145 s |
| Go | 0.154 s |
| Rust (`rustc -O`) | 0.182 s |
| Kāra (`karac build`) | 0.183 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.184 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.186 s |
| Python | 3.2 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its user time is not above its real time (0.195 s and 0.199 s on one run).

## Verification

All four arms print the same output as `depth.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them, the differential and the bench. `karac check` reports nothing on
any of them, and `karac fix` has nothing left to change. Checked at kara
`5bb1708545`.

## Writing it

The ★ arm wrote `let mut most = 0`, kept by `max` against an open count
and returned as `i32`, and `karac fix` typed it `let mut most: i32 = 0`.
The scan arm wrote two Rust habits: `s.bytes().map(..)`, and `karac fix`
added `.iter()` since `bytes()` is a `Slice[u8]`; and Rust's `scan`
closure, `|open, step| { *open += step; Some(*open) }`, which writes the
state in place, and `karac fix` rewrote it to Kāra's `scan`, which takes
the state by value and returns `Some((next_state, item))`:
`|open, step| { let open = open + step; Some((open, open)) }`. The stack
arm was written in Kāra and checked as written. The shared harness passed
`s.clone()` to a parameter that only borrows, and `karac fix` passed `s`
instead and dropped an `as i64` the call widens by itself.

The Rust template took `karac fix`'s edits (`struct Solution;` to
`struct Solution {}`, `Solution::` to `Solution.`) and was then refused
as a whole: the `(0, 0)` seed is settled to `i64` by the `m.max(d + 1)`
on the accumulator, and the chain returned as `i32` gets advice to
truncate with `as i32` and no fix. That is B-2026-11-17-129, filed from
kata 1598; the seed is written `(0i32, 0i32)` by hand.
