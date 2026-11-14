# 1541. Minimum Insertions to Balance a Parentheses String

Given a parentheses string `s` of `'('` and `')'`, it is balanced if every
`'('` has a corresponding two consecutive `'))'`, and every `'('` comes
before its `'))'`. So `"())"`, `"())(())))"` and `"(())())))"` are
balanced, while `")()"`, `"()))"` and `"(()))"` are not. In one move you
can insert a `'('` or a `')'` anywhere. Return the minimum number of
insertions that balance `s`.

```
s = "(()))"   ->  1   (one ')' at the end: "(())))")
s = "())"     ->  0
s = "))())("  ->  3   ('(' at the front and "))" at the end)
```

**Constraints:** `1 <= s.length <= 10^5`; `s` consists of `'('` and `')'`
only.

## Approaches

| file | mechanism |
|---|---|
| `balance.kara` ★ | one pass over `chars()` keeping `need`, the `')'` the open `'('` still want. A `'('` that arrives while an odd number is wanted closes that pair early with one inserted `')'`; a `')'` with nothing wanted gets an inserted `'('` and leaves one more `')'` wanted. What is still wanted at the end is inserted too. O(n) |
| `balance_pairs.kara` | the string read in tokens over `bytes()`: a `'('` opens; a `')'` takes the next `')'` with it when there is one and an inserted one when not, and the pair closes an open `'('` or, with none open, an inserted one. Each `'('` left open wants two. O(n) |
| `balance_fold.kara` | every `"))"` turned into one closer by `replace`, then a `fold` over the characters with `(open, inserted)` as its state: a lone `')'` costs one inserted `')'` and acts as a closer, and a closer with nothing open costs an inserted `'('`. O(n) |
| `balance_solution.kara` | LeetCode's Rust template (`min_insertions(s: String) -> i32`, the ★ arm over `s.as_bytes()` with `let (mut inserted, mut need)`), carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 17 lines: LeetCode's three examples, then
`((((((`, `)))))))`, `(`, `)`, `()`, `())())`, `)()` and `(()))(()))))`;
100000 `'('`, 100000 `')'` and `"())"` 33333 times; then checksums of the
answers for 3000 random strings of up to 12 parentheses, 300 of up to
1000 and 30 of up to 100000, each with its own chance of a `'('`.
`balance.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every balanced string built from the definition, `S = ""` or
`'(' S "))" S`, up to 18 characters, shortest first; the answer is how
much longer than `s` the shortest one holding `s` as a subsequence is.
It checks 3000 strings of 1 to 6 parentheses, each with its own chance
of a `'('`, every random choice drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer plus the length is a multiple of 3, and the answer is at most twice the length |
| P3 | `"())"` put after the string leaves the answer |
| P4 | `"())"` put before the string leaves the answer |
| P5 | the string twice over needs at most twice the answer |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 967250270, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a `'('` closes the pair early on an even, not odd, number wanted | P1 34, P6 34 |
| M2 | ★: a `')'` with nothing wanted leaves two wanted | P1 1536, P2 1536, P6 1536 |
| M3 | ★: half of what is still wanted inserted at the end | P1 2538, P2 2153, P3 956, P5 362, P6 2538 |
| M4 | pairs: a `')'` takes the next character with it whatever it is | P1 632, P3 155, P6 632 |
| M5 | pairs: a `'('` left open wants one | P1 1786, P2 1439, P6 1786 |
| M6 | pairs: a pair with nothing open inserts no `'('` | P1 1536, P2 1355, P6 1536 |
| M7 | fold: the closer, not the lone `')'`, charged | P1 1832, P2 1731, P3 3000, P4 3000, P6 1832 |
| M8 | fold: `"()"`, not `"))"`, replaced | P1 1411, P3 2314, P4 3000, P6 1411 |
| M9 | template: a `'('` wants one `')'` | P1 2158, P2 1749, P3 3000, P4 3000, P6 2158 |
| M10 | template: a `')'` that meets exactly nothing wanted pays for a `'('` | P1 1110, P2 926, P3 1214, P4 3000, P6 1110 |

## Benchmarks

The bench builds 100 strings of 1 to 100000 parentheses once, each with
its own chance of a `'('`, and asks each 10 times by the ★ arm, in all
five languages. Rust and Go walk the characters, as the Kāra arm does;
C walks the bytes. Every implementation prints `10 passes over 100
strings of up to 100000 parentheses: checksum 298868561`.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `3d1fc8e26` on LLVM 22:

| | median |
|---|---|
| Rust (`rustc -O`) | 0.165 s |
| C (`clang -O3`) | 0.170 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.198 s |
| Kāra (`karac build`) | 0.202 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.207 s |
| Go | 0.240 s |
| Python | 3.9 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time equals its real time (0.20 s and 0.20 s on one run).

Kāra is 1.05x Rust under overflow checks by median. Not traced. The pass
is a branch per character on a random string, so the time is mostly
mispredicted branches and building the five million random characters,
and the rows sit close together.

## Verification

All four arms print the same output as `balance.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them and the differential. `karac check` reports nothing on any of them,
and `karac fix` has nothing left to change. Checked at kara `3d1fc8e26`.

## Writing it

The ★, pairs and fold arms were written in Kāra and checked as written.
The differential took two edits from `karac fix` that `karac check` does
not report: `"".to_string()` in a list literal to `""`, and
`"())".to_string() + s.clone()` to `"())" + s.clone()`.

The Rust template took 3, 1 and 2 changed lines over three rounds:
`let (mut inserted, mut need)` to `let mut (inserted, need)`,
`for &c in s.as_bytes()` to `for c in s.as_bytes()` and `Solution::` to
`Solution.`; then `struct Solution {}` added; then `s.as_bytes()` to
`s.bytes()` and the closing `as i64` dropped (an `i32` widens). It checks
and agrees with no hand edit.
