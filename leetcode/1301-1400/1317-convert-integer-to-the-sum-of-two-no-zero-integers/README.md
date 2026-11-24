# 1317. Convert Integer to the Sum of Two No-Zero Integers

**No-Zero integer** is a positive integer that **does not contain any
`0`** in its decimal representation.

Given an integer `n`, return a list of two integers `[a, b]` where:

- `a` and `b` are **No-Zero integers**, and
- `a + b = n`.

The test cases are generated so that there is at least one valid
solution. If there are many valid solutions, you can return any of them.

```
n = 2   ->  [1,1]
n = 11  ->  [2,9]
```

**Constraints:** `2 <= n <= 10^4`.

The arms are `fn get_no_zero_integers(n: i64) -> Vec[i64]`. Any valid
pair is accepted; every arm here gives the one with the smallest `a`, so
that they can be compared answer for answer.

## Approaches

| file | mechanism |
|---|---|
| `get_no_zero_integers.kara` ★ | the first number tried from 1 up, each pair's digits read off by `% 10` and `/ 10`, until neither number has a 0. O(n log n) at worst, a few steps in fact |
| `get_no_zero_integers_text.kara` | the first numbers from 1 up, each pair written out with an f-string and searched for a `"0"` by `contains`; the first pair with none is the answer |
| `get_no_zero_integers_table.kara` | which numbers up to n have no 0, filled from the smaller ones, since x has none when its last digit is not 0 and x / 10 has none; then the first a with both a and n - a in the table, by `find`. O(n) |
| `get_no_zero_integers_solution.kara` | a Rust solution as LeetCode's Rust users write it (`(1..n).find(\|&a\| !a.to_string().contains('0') && !(n - a).to_string().contains('0'))`, the pair returned as `vec![a, n - a]`), carried to Kāra by `karac fix` |
| `get_no_zero_integers_loop.kara` | a second Rust solution as LeetCode's Rust users write it (a `fn no_zero(mut x: i32) -> bool` beside the method, stripping digits by `x % 10` and `x /= 10`, and a `for a in 1..n` loop returning the first pair), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 2 lines: LeetCode's two examples, then 10, 100
and 1010, with a 0 in n, 9999, and `10^4`, the constraints' most
(`1,1 2,9 1,9 1,99 11,999 1,9998 1,9999`); then every n from 2 to `10^4`
(`every n from 2 to 10^4: first numbers total 72783, checksum
281260451`). `get_no_zero_integers.py` mirrors the ★ arm, and its output
is byte-identical. Every arm gives the same output under `karac
__mir-run`, `karac run` and `karac __mir-llvm-run`. The table arm takes about 20 s
under `karac __mir-run`, a table up to n made afresh for each n.

The Mend loop: the ★ and table arms checked clean as first written. The
text arm searched for `'0'`, a `char`, and `contains` takes a `Str`
pattern in Kāra; the diagnostic says so and `karac fix` wrote `"0"` (1
fix). The first Rust arm takes one round of 14 fixes by `karac fix`'s
count, from 9 errors: `struct Solution;` to `struct Solution {}`,
`Vec<..>` to `Vec[..]`, `|&a|` and `|&x|` to `|a|` and `|x|`, `!` to
`not`, `&&` to `and`, `contains('0')` to `contains("0")`, `vec![a, n -
a]` to `[a, n - a]`, `::` to `.`, and the wrapper's `as i64` dropped as a
widening. The second takes one round of 14 fixes from 9 errors: the same
rewrites, `mut x: i32` to `x: i32` with `let mut x = x;` at the body's
start, `Self::no_zero` to `Solution.no_zero`, and `vec![]` to
`Vec.new()`. Both outputs match on the first run. No gap was met.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: an answer is two numbers of at least 1, each written out with
no `'0'` among its digits, that add up to n. 2000 values of n in four
kinds, 500 each: 2 to 100; 2 to `10^4`; within 12 of a multiple of 100
or 1000; and the digits 0 and 1 after a leading 1. Every case also draws
two no-zero integers whose sum is asked for P4. Every n and pair is drawn
before any arm answers.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | no smaller first number makes an answer, by trying them all |
| P3 | n + 1, when the second number plus 1 has no 0, so that the same first number answers it too: a valid answer with a first number no larger |
| P4 | the sum of two drawn no-zero integers: a valid answer with a first number no larger than the smaller of them |
| P5 | the first number at most half of n, since the pair turned round answers too |
| P6 | the ★ arm's answer |

P3 asks only where its condition holds, 970 of the 2000 cases. All 54,850
checks pass on every arm: `2000 values of n: checksum 854026460, 54850
checks over 5 arms: 0 failures`, under `karac __mir-run` and `karac
__mir-llvm-run`. Python gives the same checksum and the same count.

## Mutation testing

Thirteen edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`. Three are left out: the ★ arm
reading only each number's last digit fails the same way the table arm
does with the same mistake; the Rust arm reading the second number one
too small dies on an `unwrap()` of `None`; and the Rust arm seeing a 0 in
the second number only at its end fails as many checks under every
property as the table arm's last-digit edit (M5). The ten kept, two to each arm, are
each killed, fail the same way under both backends and not by a crash,
and no two fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the second number never looked at | P1 787, P2 787, P4 523, P6 3148 |
| M2 | ★: the first number tried from 0 | P1 1211, P2 1211, P3 1071, P4 1462, P6 4844 |
| M3 | text: the first number tried from 2 | P1 4, P2 1213, P3 4, P5 4, P6 1213 |
| M4 | text: n written out in place of the pair | P1 1068, P2 1068, P3 910, P4 705, P6 1068 |
| M5 | table: a number clean when its last digit is not 0, whatever comes before | P1 492, P2 492, P4 350, P6 492 |
| M6 | table: the tens digit skipped | P1 314, P2 314, P3 3, P4 188, P6 314 |
| M7 | solution: the second number taken one too large | P1 305, P2 1030, P3 849, P4 168, P6 1030 |
| M8 | solution: the search from the top down | P2 1996, P3 1275, P4 2000, P5 1996, P6 1996 |
| M9 | loop: a number's last digit never read | P1 365, P2 365, P3 61, P4 222, P6 365 |
| M10 | loop: the first number's 0s let through | P1 86, P2 86, P4 55, P6 86 |

P2 and P6 kill all ten, P1 and P4 nine, P3 seven and P5 two. Every edit
either lets a number with a 0 through or passes over a valid pair, and
either way the first number is no longer the least that works (P2). The
statement read literally (P1) misses only M8, whose answers are all valid
but the largest first number rather than the smallest; P4 and P5 bound
the first number from above and so catch it. P4 misses only M3, whose
first number, the next one after 1, still stays under the smaller of the
two drawn numbers. P3 asks n + 1 only where
the answer for n carries over, and catches the edits whose wrong answers
move between neighbouring n. The bound of half of n (P5) sees only the
two edits that can answer with a first number past it: M8, and M3 at
the smallest n, where 1 is the only choice.

## Benchmarks

The bench asks every n from 2 to `10^4`, the constraints' range, 300
times: each pass starts its walk through the range at a place chosen by
the checksum so far and folds both numbers of every answer, plus the
pass, into the checksum. Each answer is a fresh two-number list in every
language, a `malloc` in C. Every implementation prints `300 passes over
every n from 2 to 10^4: checksum 528048330`.

BENCHTAB
