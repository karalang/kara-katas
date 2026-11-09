# 2048. Next Greater Numerically Balanced Number

An integer `x` is numerically balanced if for every digit `d` in the number
`x`, there are exactly `d` occurrences of that digit in `x`. Given an
integer `n`, return the smallest numerically balanced number strictly
greater than `n`.

```
n = 1     ->  22
n = 1000  ->  1333
n = 3000  ->  3133
```

**Constraints:** `0 <= n <= 10^6`.

A balanced number never holds a `0`, and each digit `d` in it fills `d`
places, so its digits are a set of values from 1 to 7 that sum to its
length. There are 278 balanced numbers up to 1224444, the smallest with
seven digits, and the gaps between them can be wide: from 666666, the
largest with six digits, the next is 1022333.

## Approaches

| file | mechanism |
|---|---|
| `beautiful.kara` ★ | count upward from `n + 1`, each number's digits counted into a `[0; 10]` array by `% 10` and `/ 10`, until every digit that occurs occurs as many times as its value. At most about 355000 numbers tested |
| `beautiful_table.kara` | every balanced number listed at each call: each set of digits 1 to 7 as a bit mask, those whose values sum to at most seven arranged every distinct way by a recursive `arrange` over a `mut ref Vec[i64]` of counts, sorted; then `partition_point` finds the first above `n` |
| `beautiful_perm.kara` | for the length of `n` and one more, each set of digits that fills it written smallest first and stepped through its arrangements in rising order by a hand-written next permutation (`swap` and `ds[i..n].reverse()`) until one passes `n`; the least over all sets |
| `beautiful_string.kara` | the upward walk again, each number tested through its text: `x.to_string().chars()` counted into a `Map[char, i64]`, and `counts.iter().all(..)` comparing each count with `c.to_digit(10)` |
| `beautiful_greedy.kara` | for each set of digits that could make the answer, its least arrangement above `n` built directly: one digit longer, the digits in rising order; as long, the longest prefix of `n` the set can keep, the least digit above `n`'s next, then the rest rising |
| `beautiful_solution.kara` | LeetCode's Rust template (`(n + 1..).find(\|&x\| Self::is_balanced(x)).unwrap()`, a `mut x: i32` parameter, `[0; 10]` counts indexed `as usize`, `(0..10).all(..)` with `\|\|` and `d as i32`), carried by `karac fix` in one round to a clean check |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 12 lines: LeetCode's three examples and seven
more, each `n` and its answer; then the sum and a checksum of the answers
for 300 values of `n` below 600000, and for 666666, 999999 and 10^6, from
which the next balanced number is furthest away. The walking arms test
about ten million numbers for these, which the interpreter takes most of
a minute over. `beautiful.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every number after `n` written out as text, and each of its
digits compared with how many times that digit occurs in the text, until
one number passes. It checks 100 values of `n` below 30000, drawn before
any arm answers; the walking arms make larger ones slow in the
interpreter.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | asked again from one below the answer, the answer is the same |
| P3 | asked from `n + 1`, the answer is the same unless `n + 1` was it, and then it is larger |
| P4 | the answer's digits, counted, are each used as many times as their value |
| P5 | the answer has as many digits as `n + 1` or one more |
| P6 | each arm agrees with at least three of the other five |

The differential prints `100 values: checksum 848291949, 3600 checks over
6 arms: 0 failures` under every lane in Verification. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Thirty-six edits to the differential, six to each of its arms, then four
more, two to each of the table and Rust arms, each run under `karac
__mir-run` and `karac __mir-llvm-run`. Seventeen are kept, three to each
Kāra arm and two to the Rust-template arm. Each kept one is killed, fails
the same way under both backends and not by a crash, and no two kept ones
fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a digit allowed fewer times than its value | P1 99, P4 99, P6 99 |
| M2 | ★: zeros not counted against (`1..10`) | P1 90, P4 90, P6 90 |
| M3 | ★: the walk stepping by two | P1 49, P3 99, P6 49 |
| M4 | table: the digit 1 never placed | P1 51, P6 51 |
| M5 | table: the list never sorted | P1 37, P6 37 |
| M6 | table: the second entry above `n` taken | P1 100, P2 100, P3 1, P6 100 |
| M7 | perm: the tail never reversed | P1 30, P6 30 |
| M8 | perm: the last set's arrangement taken, not the least | P1 100, P2 100, P6 100 |
| M9 | perm: only lengths one longer than `n` | P1 73, P2 100, P6 73 |
| M10 | string: each digit's first sight counted twice | P1 100, P4 100, P6 100 |
| M11 | string: the walk starting at `n` | P3 1 |
| M12 | string: the first character skipped | P1 96, P4 96, P6 96 |
| M13 | greedy: the shortest prefix tried first | P1 22, P2 95, P6 22 |
| M14 | greedy: an equal digit allowed where a larger one is needed | P1 46, P2 46, P3 47, P6 46 |
| M15 | greedy: the last set's candidate taken, not the least | P1 68, P2 27, P6 68 |
| M16 | solution: the adapter asking from n + 1 | P1 1, P2 100, P6 1 |
| M17 | solution: a leading 1 never counted (`x > 1`) | P1 36, P4 36, P6 36 |

P1 and P6 kill sixteen, P2 seven, P4 five, P3 four and P5 none. P4 counts
the answer's digits again, so it sees every edit that lets an unbalanced
number through (M1, M2, M10, M12, M17), and nothing else. P2 asks again
from one below the answer, which an honest arm answers with the same
number; an arm that returns a later balanced number (M6, M8, M9, M15) or
the wrong one of two near ones (M13, M14) is asked a different question and
gives a different answer. P3 sees an arm that skips or returns its own
starting point: the walk stepping by two (M3), and the walk starting at `n`
(M11), which none of the 100 random values can show, since none of them is
balanced, but asked from `n + 1` where `n + 1` is the answer, returns it
again instead of a larger one. M16 is the adapter's error, asking the
template from `n + 1`: it fails P1 only for the one value whose `n + 1` is
balanced, and P2 everywhere, where it is asked from one below the answer
and skips it.

Of the first thirty-six, three were not kept for not finishing cleanly. In
the table arm, no set longer than four digits and each digit used once
leave the list without an entry above some `n`, and the search reads past
its end. In the permutation arm, no length one longer than `n` finds no
answer for an `n` like 4444 and returns `i64.MAX`, and the properties that
ask again from there crash under the interpreter and run on past the time
limit under the compiled backend. That left the table and Rust arms short
of edits that fail on checks of their own, and four more were written: the
second entry above `n` (table) and a leading 1 never counted (Rust) are
kept, and an arrangement listed one digit short (table) and the second
balanced number taken (Rust) fail as M10 and M6.

The rest fail as a kept one does or on checks their arm has no room for.
The ★, string and Rust arms share their edits' failures, since they test
the same numbers the same way: a digit allowed fewer or more times than its
value (★, string, Rust), zeros not counted against (Rust) and one balanced
digit enough (string) fail as M1 or M2, every other digit counted (★, Rust)
and a count never more than one (Rust) as M10, the leading digit never
counted (★) as M12, the walk stepping by two (string) as M3, and the walk
or search starting at `n` (★, table, permutation, Rust) as M11. Each digit
written one less (table) fails as M10. The value read with its digits
reversed (permutation), no answer one digit longer, the rest written
largest first and a prefix digit allowed once too often (greedy) fail on
checks of their own.

## Verification

Every arm prints the same output as `beautiful.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error. `karac
run` and a `karac build` binary print the same output for every arm and the
differential. `karac check --output=json` reports nothing on any of them.
Under `karac __mir-run` the arms take 0.3 s (greedy) to 211 s (string),
the walking arms 44 s (★) and 73 s (Rust); the differential takes 47 s; on
kara 531a0f19a1.

The five Kāra arms met no compiler gap and checked as written.

The Rust arm was written as LeetCode's Rust template. `karac fix` carries
it in one round of six edits to a clean check: `struct Solution;` to
`struct Solution {}`, `|&x|` to `|x|`, `Self::is_balanced` to
`Solution.is_balanced`, the `mut x: i32` parameter to `x: own i32` with a
`let mut x = x;`, and `||` to `or`. The counts stay indexed `as usize`,
which Kāra accepts. The adapter hands the harness's `i64` to it `as i32`
and takes the `i32` back widened.

## Benchmarks

The bench answers 1000 values of `n` spread over the constraints' range,
0 to 10^6, with the ★ arm in all five languages: about 150 million numbers
tested. Every implementation prints `1000 calls: sum 650519857, checksum
836958313`.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with kara `531a0f19a1` on LLVM 22:

| | time | median |
|---|---|---|
| Rust (`rustc -O`) | 1.108 to 1.603 s | 1.219 s |
| C (`clang -O3`) | 1.152 to 1.339 s | 1.223 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.229 to 1.436 s | 1.353 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 1.448 to 1.785 s | 1.502 s |
| Go | 1.486 to 1.848 s | 1.637 s |
| Kāra (`karac build`) | 1.548 to 1.777 s | 1.670 s |
| Python | 102.1 s |  |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`, the
sequential lane. A plain `karac build` parallelizes nothing here: its user
time (1.659 s) is not above its real time (1.670 s).

The sequential Kāra program is 1.11x Rust under overflow checks and 1.23x
C.
