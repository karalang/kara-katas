# 1208. Get Equal Substrings Within Budget

You are given two strings `s` and `t` of the same length and an integer
`maxCost`. You want to change `s` to `t`. Changing the `i`-th character
of `s` to the `i`-th character of `t` costs `|s[i] - t[i]|` (the absolute
difference between the ASCII values of the characters). Return the
maximum length of a substring of `s` that can be changed to be the same
as the corresponding substring of `t` with a cost less than or equal to
`maxCost`. If there is no substring from `s` that can be changed to its
corresponding substring from `t`, return `0`.

```
s = "abcd", t = "bcdf", maxCost = 3    ->  3
s = "abcd", t = "cdef", maxCost = 3    ->  1
s = "abcd", t = "acde", maxCost = 0    ->  1
```

**Constraints:** `1 <= s.length <= 10^5`; `t.length == s.length`; `0 <=
maxCost <= 10^6`; `s` and `t` consist of only lowercase English letters.

The arms are `fn equal_substring(s: String, t: String, max_cost: i64) ->
i64`. The two Rust arms keep the method LeetCode gives Rust users, on
`i32`, inside `impl Solution`, and a one-line `equal_substring` calls it.

## Approaches

| file | mechanism |
|---|---|
| `get_equal_substrings_within_budget.kara` ★ | a sliding window over the costs `\|s[i] - t[i]\|`: its right end steps on, its left end steps on while the window costs more than the budget, and the longest window is kept. O(n) |
| `get_equal_substrings_within_budget_prefix.kara` | prefix sums, `sum[i]` the cost of the first `i` letters, and for each right end the least left end whose window fits, by binary search over the rising sums. O(n log n) |
| `get_equal_substrings_within_budget_slide.kara` | a window that never shrinks: each step takes one more letter on the right, and when the window is over budget it drops one on the left, so its width grows only when a wider window fits; the answer is its width at the end. O(n), no maximum kept |
| `get_equal_substrings_within_budget_width.kara` | binary search on the answer: a width fits when the cheapest window of that width does, found by sliding a window of exactly that width; a narrower width only fits more easily. O(n log n) |
| `get_equal_substrings_within_budget_zip.kara` | a Rust solution as LeetCode's Rust users write it (the costs by `s.bytes().zip(t.bytes()).map(\|(a, b)\| (a as i32 - b as i32).abs())` collected into a `Vec<i32>`, then two pointers with `usize` indices and `ans = ans.max(r - l + 1)`), carried to Kāra by `karac fix` |
| `get_equal_substrings_within_budget_bytes.kara` | another Rust solution (`s.as_bytes()` and `t.as_bytes()` read by index, the budget itself spent and given back from `let mut budget = max_cost;`, and a window that never shrinks, its width `s.len() - start` at the end), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six more properties |

Every arm prints the same 14 lines: LeetCode's three examples; `a`
against `z` with budgets 25 and 24 (`1`, `0`); two more random pairs;
equal strings at budget 0 (`3`); `zzzz` against `aaaa` at 100 (`4`);
1000 random small cases (`1000 small cases: total 4811, checksum
732978269`); and four at the constraints' top, 100000 random letters
against 100000 more at budgets 0, 1000 and 1000000 (`5`, `151`,
`100000`), and 100000 letters of `a` and `b` against themselves at
budget 0 (`100000`). `get_equal_substrings_within_budget.py` mirrors the
★ arm, and its output is byte-identical. Every arm gives the same output
under `karac run` and `karac build`, and under the AddressSanitizer
build.

The Mend loop: the ★, prefix, slide and width arms check clean as
written. The zip arm takes one round of 15 fixes (among them `struct
Solution;` to `struct Solution {}`, `Vec<i32>` to `Vec[i32]`,
`s.bytes().zip(t.bytes())` to `s.bytes().iter().zip(t.bytes().iter())`,
as Kāra's `bytes()` gives a `Vec[u8]` rather than an iterator, and `let
(mut l, mut sum, mut ans) = (0usize, 0i32, 0usize)` to `let mut (l, sum,
ans) = (0, 0i32, 0)`), and the bytes arm one round of 7 (among them
`as_bytes()` to `bytes()` on both strings). Both outputs match.

## Gaps

None found.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every substring tried, its cost summed letter by letter, and
the longest within the budget. 2000 random cases: 1 to 10 letters from
the first 2, 5 or 25, and a budget below 30; 1911 of them have an
answer of at least 1.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | `s` and `t` swapped give the same |
| P3 | both reversed give the same |
| P4 | a budget one more gives as long or longer |
| P5 | at most the length, and at least 1 just when some letter's cost fits |
| P6 | every letter of both one later gives the same |
| P7 | the ★ arm's answer |

All 84,000 checks pass on every arm: `2000 cases: checksum 533899537,
84000 checks over 6 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and the AddressSanitizer build. A Python reading of
the same cases, summing every substring's costs, gives the same
checksum.

## Mutation testing

Twelve edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac run`, each failing the same way under both. All
twelve are caught.

| # | mutation | failures by property |
|---|---|---|
| S1 | ★: the window measured before it is brought within the budget | P1 720, P3 273, P5 89, P7 3600 |
| S2 | ★: the window measured one short | P1 1911, P5 338, P7 9555 |
| F1 | prefix: a window costing the budget exactly refused | P1 248, P5 52, P7 248 |
| F2 | prefix: the last window taken, not the longest | P1 392, P3 496, P5 158, P7 392 |
| L1 | slide: a budget spent to zero taken for overspent | P1 248, P5 52, P7 248 |
| L2 | slide: the cost of a letter left behind never given back | P1 381, P3 496, P5 146, P7 381 |
| W1 | width: the first window taken for the cheapest | P1 381, P3 496, P5 146, P7 381 |
| W2 | width: a width costing the budget exactly refused | P1 248, P5 52, P7 248 |
| Z1 | zip: the window measured one short | P1 1911, P5 338, P7 1911 |
| Z2 | zip: a letter's cost taken signed | P1 757, P2 585, P3 289, P5 61, P7 757 |
| B1 | bytes: the window's start never moved | P1 860, P5 89, P7 860 |
| B2 | bytes: the window shrunk until it fits | P1 392, P3 496, P5 158, P7 392 |

A mutation of the ★ arm fails P7 on all six arms, the ★ arm against the
other five. The first S1 tried, the `while` that shrinks the window made
an `if`, was not a fault: the window then never shrinks, which is the
slide arm's method, and every answer stayed right. The counts below are
from a Python reading of the cases. S2 and Z1 answer one short, so they
fail the 1911 cases whose answer is at least 1. F1, L1 and W2 refuse a
window costing the budget exactly, and fail the 248 cases where every
longest window does. F2 and B2 give the longest window ending at the
last letter, and L2 and W1 the longest starting at the first: L2's
budget, never given back, keeps the window at the width it had when the
budget first ran out, and W1 judges each width by its first window. They
fail the 392 and the 381 cases where that window is not the longest.
B1 answers the whole length every time and fails the 860 cases where
the whole string does not fit. Z2's signed costs can cancel, so it is
the one P2 catches: swapping `s` and `t` flips every sign. P4 and P6,
a larger budget and every letter one later, catch none of the twelve:
no edit makes an answer shrink with the budget or depend on the letters
rather than their differences.

## Benchmarks

`bench/` runs the same workload in Kāra, C, Rust, Go and Python: the ★
arm (a window over the letters, widened one letter a step and shrunk
from the left while it costs more than the budget) on 16 pairs of
strings of 100000 letters, the constraints' most, drawn once, each pair
close in some stretches and far in others; then 10 rounds over the
pairs, each with the budgets 0, 1000, 100000 and 1000000, every answer
folded into a checksum. Every program prints `10 rounds over 16 pairs of
100000 letters: checksum 745150377`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `684b860a50`
on LLVM 22. A plain `karac build` targets x86-64-v2, so the C and
overflow-checked Rust programs are also built at x86-64-v3 for
comparison:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 0.338 to 0.402 s | 0.352 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.335 to 0.419 s | 0.356 s |
| Rust (`rustc -O`) | 0.352 to 0.434 s | 0.377 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.357 to 0.437 s | 0.376 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.360 to 0.409 s | 0.376 s |
| C (`clang -O3`) | 0.363 to 0.435 s | 0.377 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.367 to 0.421 s | 0.391 s |
| Go | 0.396 to 0.482 s | 0.407 s |
| Python | 14.31 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Kāra is about 5% ahead of Rust with overflow checks on (0.356 s
against 0.376 s), and the two ranges overlap. Kāra is about 6% ahead of
C (0.356 s against 0.377 s); Kāra is about 13% ahead of Go (0.356 s
against 0.407 s). Python takes about 40x Kāra's time. No profile was
taken.
