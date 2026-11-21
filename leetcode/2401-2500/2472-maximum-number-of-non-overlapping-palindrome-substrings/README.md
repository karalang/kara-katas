# 2472. Maximum Number of Non-overlapping Palindrome Substrings

You are given a string `s` and a **positive** integer `k`.

Select a set of **non-overlapping** substrings from the string `s` that
satisfy the following conditions:

- The **length** of each substring is **at least** `k`.
- Each substring is a **palindrome**.

Return *the **maximum** number of substrings in an optimal selection*.

A **substring** is a contiguous sequence of characters within a string.

```
s = "abaccdbbd", k = 3  ->  2
s = "adbcda", k = 2     ->  0
```

**Constraints:** `1 <= k <= s.length <= 2000`; `s` consists of
lowercase English letters.

A palindrome of `k` letters or more holds, about the same center, one of
exactly `k` or `k + 1` letters, so only those need be taken; and of the
palindromes that remain to choose from, the one that ends first is never
a worse choice than another.

## Approaches

| file | mechanism |
|---|---|
| `palindromes.kara` ★ | greedy: walking the starts, a palindrome of `k` letters from here ends sooner than any from a later start, and failing that one of `k + 1` ends no later than one from the next start; it is taken and the walk jumps past it, else moves on. O(nk) |
| `palindromes_table.kara` | dynamic programming over a palindrome table: `palindrome[i][j]` filled by length from the one inside, then `best[j]`, the most among the first `j` letters, the best of leaving the last letter out and of ending any palindrome of `k` letters or more there. O(n^2) |
| `palindromes_centers.kara` | by centers: from each of the `2n - 1` centers a palindrome grown one letter a side until it holds `k` letters or more, only that shortest one kept, listed by the letter it ends on, and the same `best` over them. O(nk) |
| `palindromes_manacher.kara` | Manacher's radii, then the greedy: the letters with a `#` between and around them, the longest palindrome about every center found in linear time by reusing the mirror's radius inside the rightmost palindrome seen, and each test of the walk one look at a radius. O(n) |
| `palindromes_iter.kara` | iterators: the greedy, the length to take at each start found by `find` over `k` and `k + 1`, a palindrome checked by `all` over the pairs of letters from both ends. O(nk) |
| `palindromes_solution.kara` | LeetCode's Rust template: `String` and `i32` in, `i32` out; the letters through `as_bytes()`, and `dp[i + 1]` the best of leaving letter `i` out and of ending a palindrome of `k` or `k + 1` letters there, each checked by two indices walked inward; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 12 lines: LeetCode's two examples; then five
more, `k` 1 with every letter its own, one letter six times with `k` 2,
a whole palindrome with `k` its length, a palindrome of `k` letters
only, and two that overlap with one more apart from them; then four
strings of 2000 letters, the constraints' longest, one letter with `k`
1 and 7, two letters with `k` 3, and the whole alphabet with `k` 2; and
3000 random strings of 1 to 40 letters from one to three kinds, with
`k` from 1 to their length, as a checksum. `palindromes.py` mirrors the
★ arm and its output is byte-identical, and the mirror was checked on
20000 random strings of 1 to 12 letters against a search over every
choice of palindromes.

`check` first reports 3 errors on the template, and `karac fix` carries
it in one call, reporting 8 edits: `let (mut l, mut r)` becomes `let
mut (l, r)`, three edits, since `mut` goes before the whole pattern;
`struct Solution;` is given its braces; `as_bytes()` becomes `bytes()`;
`k as usize` becomes `k as i64`; and `vec![0; n + 1]` becomes
`Vec.filled(n + 1, 0i32)`. The `for len in [k, k + 1]` over an array,
`continue`, the inner `break` and `dp[i + 1].max(..)` stand as Kāra.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: from each letter on, every choice tried, the letter left out
or every substring of `k` letters or more that starts there and equals
its own reverse taken, and the most that follow added, with no memo. No
center, table or greedy stands in for the search. It checks 300 random
strings of 1 to 10 letters, then 60 of up to 14, each from the first
one to three letters of the alphabet, with `k` from 1 to its length.
All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the count is the literal reading's |
| P2 | the string reversed: the same count |
| P3 | the string, `yz`, then the string again: twice the count, and two more when `k` is 1 |
| P4 | `k` raised by one: no more |
| P5 | `k` letters `x` and a `y` put in front: one more, or two when `k` is 1 |
| P6 | each arm agrees with at least three of the other five |

P2 holds because a palindrome reversed is the same palindrome. P3 and
P5 hold because a palindrome that holds the single `y` or `z` must have
it at its center, with the same letter on both sides, which neither
has, so no palindrome of two letters or more crosses them, and each is
one of its own when `k` is 1. P4 holds because every selection allowed
with `k + 1` is allowed with `k`.

The differential prints `360 cases: checksum 452552065, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and runs the same search with slices. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M2 | ★: a k + 1 palindrome jumped only k | P1 10, P2 12, P6 10 |
| M3 | ★: the last start never tried | P1 177, P2 35, P3 177, P6 177 |
| M5 | ★: a k palindrome jumped one letter more | P1 97, P2 1, P3 106, P5 106, P6 97 |
| M7 | table: pairs of letters never palindromes | P1 68, P5 138, P6 68 |
| M8 | table: the inner test skipped | P1 36, P3 111, P6 36 |
| M10 | table: the letter left out never carried | P1 42, P2 49, P3 153, P5 254, P6 42 |
| M12 | centers: only odd centers | P1 128, P2 37, P3 255, P5 259, P6 128 |
| M14 | centers: the length one short | P1 210, P3 106, P5 360, P6 210 |
| M16 | centers: each center grown on one side | P1 58, P6 58 |
| M17 | manacher: the mirror radius taken whole | P1 4, P2 6, P3 28, P6 4 |
| M18 | manacher: the radius never grown | P1 293, P3 106, P5 360, P6 293 |
| M19 | manacher: the k test against the center one along | P1 211, P3 106, P4 15, P5 360, P6 211 |
| M23 | iter: the check one pair short | P1 60, P3 106, P5 53, P6 60 |
| M25 | iter: a found palindrome jumped one letter | P1 112, P6 112 |
| M26 | iter: the longer length tried first | P1 73, P2 1, P6 73 |
| M28 | solution: the letter left out never carried | P1 51, P2 52, P3 144, P4 4, P5 254, P6 51 |
| M31 | solution: the best before the palindrome read one late | P1 54, P6 54 |

P1 and P6 kill all seventeen, P3 eleven, P5 nine, P2 eight, and P4
two.

Fourteen are not kept. Three fail exactly as a kept one: the ★ arm's
`k + 1` test before the `k` one (M6) as the iter arm's longer length
tried first (M26), the same mistake; the table arm's palindrome of
exactly `k` refused (M9) as the centers arm's length one short (M14),
each wanting `k + 1` letters; and the centers arm's letter left out
never carried (M15) as the template's (M28). Eight fail alike, apart
from every kept one: the ★ and manacher arms' `k + 1` test dropped and
the iter arm's and template's only `k` tried (M1, M20, M22, M27); the
★ arm's palindrome check one pair short and the template's walk
stopped at the center pair (M4, M30); and the table arm's only starts
after the first tried and the template's whole string never tried
(M11, M29), each never taking a palindrome that starts at the first
letter. Two survive and are equivalent: the centers arm's walk not
stopped at the first (M13), which lists the longer palindromes about
each center too, never a better choice than the shortest inside them;
and the manacher arm's rightmost never moved (M21), which only stops
reusing radii, so every radius is grown from 0 to the same value. The
iter arm's length overrun allowed (M24) ends with an index out of
bounds, as the check reads one letter past the end. Every other edit
is killed.

## Verification

Every arm prints the same output as `palindromes.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.4 to 0.8 s, the table arm 13.0 s, and the differential 1.1 s; under `karac __mir-llvm-asan` the arms take 0.4 to 0.6 s, the table arm 2.2 s, and the differential 0.9 s, and under `karac run` the differential takes 0.5 s.

## Benchmarks

The bench builds 20 strings of 2000 letters from `ab` once from its own
generator, then makes 2400 passes; each sets one letter of every string
from the checksum so far, so no answer carries over, then answers it
with `k` from 2 to 6 by the pass, folding the count plus the pass into
the checksum. The bench uses the ★ arm in all five languages, the
string a list of letters in each. Every implementation prints `2400
passes over 20 strings of 2000: checksum 860912275`.

BENCHTAB
