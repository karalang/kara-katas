# 1573. Number of Ways to Split a String

Given a binary string `s`, you can split `s` into 3 non-empty strings
`s1`, `s2`, and `s3` where `s1 + s2 + s3 = s`. Return the number of ways
`s` can be split such that the number of ones is the same in `s1`, `s2`,
and `s3`. Since the answer may be too large, return it modulo
`10^9 + 7`.

```
s = "10101"   ->  4
s = "1001"    ->  0
s = "0000"    ->  3
```

**Constraints:** `3 <= s.length <= 10^5`; `s[i]` is either `'0'` or
`'1'`.

## Approaches

| file | mechanism |
|---|---|
| `split.kara` ★ | the positions of the ones collected; with `t` of them each part holds `t / 3`, the first cut falls anywhere in the gap after the (t/3)-th one and the second in the gap after the (2t/3)-th, so the answer is the product of the two gaps. With no ones, every pair of the `n - 1` cut points works: `(n - 1)(n - 2) / 2`. O(n) |
| `split_cuts.kara` | one pass over the cut points: a first cut is good where the ones so far are `t / 3`, and a second cut where they are `2t / 3` pairs with every good first cut before it. No special case for a string of zeros. O(n) |
| `split_runs.kara` | `s.split("1")` into the runs of zeros between the ones: a cut has one place more than the run after the (t/3)-th one is long, and the same after the (2t/3)-th. O(n) |
| `split_solution.kara` | LeetCode's Rust template (`num_ways(s: String) -> i32`, over `as_bytes()`), carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 12 lines: LeetCode's three examples, then
`100100010100110`, `111`, `000`, `1101010` and `1001001`; then the sum
of the answers and a checksum for 3000 random strings of 3 to 12
characters, 300 of up to 1000 and 30 of up to 100000, each string with
its own odds of a `'1'`; and 100000 zeros, whose answer is reduced by the
modulus. `split.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every pair of cuts tried, the ones in each of the three
non-empty parts counted, and the pairs that leave them equal counted. It
checks 3000 strings of 3 to 12 characters, each with its own odds of a
`'1'`, every random choice drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the string reversed leaves the answer |
| P3 | every `'1'` written twice leaves the answer |
| P4 | the answer is at most `(n - 1)(n - 2) / 2`, and exactly that when there is no `'1'` |
| P5 | a `'0'` put in front leaves the answer when there is a `'1'`, and gives `n(n - 1) / 2` when there is none |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 928810798, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends.

The first M3 returned 0 only when `t % 3` is 2, which with `t % 3 == 1`
indexed past the ones: killed by an index out of bounds rather than by a
property, so it was replaced.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a string of zeros counted as `n(n - 1) / 2` | P1 106, P4 106, P5 106, P6 106 |
| M2 | ★: the second gap measured inside the middle part | P1 775, P2 83, P3 925, P6 775 |
| M3 | ★: the first gap one too wide | P1 925, P2 358, P4 133, P6 925 |
| M4 | cuts: a first cut counted before the second cut at the same point is tested | P1 106, P4 106, P5 106, P6 106 |
| M5 | cuts: a second cut allowed after the last character | P1 106, P4 106, P5 106, P6 106 |
| M6 | cuts: a `'1'` in first place not counted | P1 315, P2 204, P3 311, P5 315, P6 315 |
| M7 | runs: the second gap one too narrow | P1 925, P2 358, P6 925 |
| M8 | runs: the second gap read from the run after the first | P1 72, P2 83, P3 271, P6 72 |
| M9 | template: the second gap counted one `'1'` early | P1 289, P2 357, P3 52, P6 289 |
| M10 | template: the product halved | P1 925, P6 925 |

M4 and M5 change only strings of zeros, where `t / 3` and `2t / 3` are
both 0, which is the cuts arm's one shape without a special case.

## Benchmarks

The bench builds 20 strings of 500000 characters, each with its own odds
of a `'1'` from 1 in 1 to 1 in 1000, once, then answers all 20 ten times
over, 200 answers, by the ★ arm, in all five languages. Every
implementation prints `200 answers over 20 strings of 500000 characters:
ways total 5344490, checksum 537339295`.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `572956a03` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.077 s |
| Rust (`rustc -O`) | 0.104 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.111 s |
| Go | 0.178 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.268 s |
| Kāra (`karac build`) | 0.268 s |
| Python | 6.1 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time is below its real time (0.254 s and 0.262 s on one run).

Kāra is 2.41x Rust under overflow checks by median. Running 0 and 30
rounds splits it: building the strings costs 0.054 s against Rust's
0.030 s, and each 200 answers 0.21 s against 0.076 s, so the gap is the
walk over the chars. The same chain over `s.bytes().iter()` takes 0.083
s, Rust's time, and even a plain `for c in s.chars()` takes 0.148 s.
Filed as B-2026-11-15-2. The bench keeps `chars()`, which is how the
problem reads.

## Verification

All four arms print the same output as `split.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them and the differential. `karac check` reports nothing on any of them,
and `karac fix` has nothing left to change. Checked at kara `572956a03`.

## Writing it

The ★, cuts and runs arms were written in Kāra and checked as written.

The Rust template took three rounds of `karac fix`, 4 changed lines, then
3, then 2:

1. `|&&c|` and `for &c in b` to `|c|` and `for c in b`,
   `let (mut first, mut second)` to `let mut (first, second)`, and
   `Solution::` to `Solution.`;
2. `s.as_bytes()` to `s.bytes()`, the `0i64` suffixes dropped, and the
   wrapper's `as i64` dropped (an `i32` widens to `i64` on its own);
3. the `as i64` casts on `b.len()` and `count()` dropped.

It then checks and agrees with no hand edit.
