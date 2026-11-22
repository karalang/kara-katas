# 2842. Count K-Subsequences of a String With Maximum Beauty

You are given a string `s` and an integer `k`.

A **k-subsequence** is a **subsequence** of `s`, having length `k`,
and all its characters are **unique**, i.e., every character occurs
once.

Let `f(c)` denote the number of times the character `c` occurs in `s`.

The **beauty** of a **k-subsequence** is the sum of `f(c)` for every
character `c` in the k-subsequence.

Return *the number of k-subsequences whose **beauty** is the
**maximum** among all k-subsequences*. Since the answer may be too
large, return it modulo `10^9 + 7`.

A subsequence of a string is a new string formed from the original
string by deleting some (possibly none) of the characters without
disturbing the relative positions of the remaining characters.

**Notes:** `f(c)` is the number of times a character `c` occurs in
`s`, not a k-subsequence; two k-subsequences are considered different
if one is formed by an index that is not present in the other, so two
k-subsequences may form the same string.

```
s = "bcca", k = 2   ->  4
s = "abbcd", k = 4  ->  2
```

**Constraints:** `1 <= s.length <= 2 * 10^5`; `1 <= k <= s.length`;
`s` consists only of lowercase English letters.

## Approaches

| file | mechanism |
|---|---|
| `beauty.kara` ★ | the letters' counts sorted, most first: the best k take the k largest, every letter counted above the k-th must be in, and the rest are chosen among the letters tied with it, C(tied, wanted) ways, each letter taken at any of its places; the binomial by a running product and an inverse from Fermat's little theorem |
| `beauty_knapsack.kara` | a knapsack over the 26 letters: the most beauty j of the letters so far can give, and the subsequences that reach it, each letter present either joining a set of j - 1 or not |
| `beauty_heap.kara` | the counts in a `PriorityQueue.max_first()`, popped a whole tie at a time by `peek()`; a tie that fits takes all its letters, the one that does not is chosen from by a row of Pascal's triangle |
| `beauty_grouped.kara` | the letters counted in a `Map` and grouped by count in a `SortedMap` from each count to how many letters have it, walked from the largest by `iter().rev()`; the binomial exact in `i64`, a tie holding at most 26 letters |
| `beauty_solution.kara` | a Rust solution as LeetCode's Rust users write it: a `[0i64; 26]` of counts, the nonzero ones filtered with `\|&&c\|` and sorted by `sort_unstable_by(\|a, b\| b.cmp(a))`, and the binomial over the tie by a running product and a `pow` by squaring with `mut` parameters, the answer as `i32`, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 4 lines: LeetCode's two examples, k above
the distinct letters, and one letter; 2 x 10^5 letters, LeetCode's
most, over all 26, with k = 26 and k = 13; then 3000 random strings of
1 to 10 letters over a to e with k up to 6, and 100 of up to 20000
letters over the first 3 to 26 with k up to 26, as a count with none
and a checksum. `beauty.py` mirrors the ★ arm and its output is
byte-identical.

```
4 2 0 1
25475410 433618054
3000 short strings: 1387 with none, checksum 117008446
100 long strings: 45 with none, checksum 214952337
```

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: every choice of k places in s by a bitmask, kept when
its letters are all different, its beauty the sum of their counts in
s, and the choices of the most beauty counted. It draws 2000 random
strings of 1 to 10 letters over a to e with k up to 6, then 50 of up
to 2000 over the first 3 to 26 letters with k up to 26, all before any
arm answers; the literal reading is asked only of the first 2000.

| | property |
|---|---|
| P1 | up to 10 letters, the answer is the literal reading's |
| P2 | the string reversed: the same answer |
| P3 | every letter moved on one, z to a: the same answer |
| P4 | the string written twice: the answer times 2^k |
| P5 | k = 1: the most common letter's count times the letters that have it |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2050 cases: checksum 278333136, 61500 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases gives the same checksum. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the tie chosen from one letter too few | P1 1121, P5 2050, P6 1149 |
| M2 | ★: the letters above the tie left out | P1 592, P4 614, P6 614 |
| M3 | ★: the k-th count read one place early | P1 364, P6 376 |
| M4 | knapsack: a tie for the best not added | P1 417, P5 745, P6 425 |
| M5 | knapsack: each letter usable twice | P1 1618, P6 1662 |
| M6 | heap: only one letter of a tie popped | P1 417, P5 745, P6 425 |
| M7 | heap: Pascal's row shifted | P1 218, P5 272, P6 222 |
| M8 | grouped: groups walked from the smallest | P1 631, P5 1307, P6 657 |
| M9 | grouped: the count's power left out | P1 957, P4 1149, P5 1560, P6 985 |
| M10 | solution: the tie's own count above | P1 1121, P5 2050, P6 1149 |

## Benchmarks

The bench draws 100 strings of 2 x 10^5 letters, LeetCode's most, each
over the first 3 to 26 letters with k up to 26, all of them first,
then answers each 40 times by the ★ arm in all five languages; each
answer counts the string's letters afresh. Every implementation prints
`100 strings of 200000, 40 rounds: 1840 with none, checksum
466129891`.

BENCHTAB

## Verification

All five arms print the same output as `beauty.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The heap arm, as first written, compared `heap.peek() == Some(f)`, and
`karac check` reported E0208, "cannot compare 'Option[ref i64]' and
'Option[i64]': one side views its item"; `karac fix` wrote
`heap.peek().cloned() == Some(f)`, where Rust would want `Some(&f)`.
The other own arms checked clean.

LeetCode's Rust template took 25 `karac fix` edits in one run, the
wrapper included: `struct Solution {}` added for the `impl`; `fn
pow(mut b: i64, mut e: i64)` became plain parameters rebound with `let
mut b = b;` and `let mut e = e;`; the `i64` suffixes went, `i64` being
the default; `(b - b'a') as usize` as an index lost its cast and its
parentheses; `Vec<i64>` became `Vec[i64]`, `k as usize` `as i64`, and
`sort_unstable_by` `sort_by`; `|&&c|` and `|&&x|` lost their `&&`, and
`for &x in &f` became `for x in ref f`; the redundant `as i64` casts
went from `(need - i) as i64` and from `Self::pow((i + 1) as i64, ..)`,
and `Self::` became `Solution.`; in the wrapper `&str` became `Str`,
`Solution::` took `.`, and the `as i64` went. The `.cloned()` over
`i64`s and `1_000_000_007` were accepted as written.

Before kara 0d28296389 (B-2026-11-21-202) the two casts in the loop lost their `as i64` and
left their operands' parentheses behind, `c * ((need - i)) % MOD` and
`Solution.pow((i + 1), MOD - 2)`, which nothing needs. A cast in
parentheses of its own now goes with them while a parenthesized
operand keeps its own pair, and a cast that is a whole argument takes
its operand's parentheses too, as a `let`'s value and an index already
did.
