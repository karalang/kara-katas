# 1216. Valid Palindrome III

Given a string `s` and an integer `k`, return `true` if `s` is a
`k`-palindrome.

A string is `k`-palindrome if it can be transformed into a palindrome by
removing at most `k` characters from it.

```
s = "abcdeca", k = 2      ->  true     remove 'b' and 'e'
s = "abbababa", k = 1     ->  true
```

**Constraints:** `1 <= s.length <= 1000`; `s` consists of only lowercase
English letters; `1 <= k <= s.length`.

The arms are `fn is_valid_palindrome(s: String, k: i64) -> bool`. The
two Rust arms keep the method LeetCode gives Rust users, on `k: i32`,
inside `impl Solution`, and a one-line `is_valid_palindrome` calls it.

## Approaches

Removing letters until the rest reads the same both ways leaves a
palindromic subsequence, so the fewest removals are the letters outside
the longest one.

| file | mechanism |
|---|---|
| `valid_palindrome_iii.kara` ★ | the longest palindromic subsequence, one row at a time: `row[j]` the longest in `s[i..=j]`; going down from the last `i`, a pair of equal ends adds two to the inside's answer, kept from the row before in `diagonal`, and otherwise the better of dropping either end. O(n^2) time, O(n) space |
| `valid_palindrome_iii_table.kara` | the fewest removals directly: `fewest[i][j]` the letters `s[i..=j]` must lose, filled by the span's length; equal ends cost what the inside does, and otherwise one more than the cheaper of dropping either end. O(n^2) time and space |
| `valid_palindrome_iii_common.kara` | a palindrome kept from `s` is a subsequence it shares with its own reverse, so the longest common subsequence of the two, by the textbook table kept to two rows exchanged with `swap`. O(n^2) time, O(n) space |
| `valid_palindrome_iii_budget.kara` | the removals spent from a budget: a recursion from both ends that walks in past equal letters and otherwise tries dropping either end, giving up once the budget is gone; a `Map` from `(i, j)` keeps, for each span reached, the fewest removals it needs when found within the budget, and otherwise a count it needs at least, so a span is worked again only when a larger budget reaches it |
| `valid_palindrome_iii_grid.kara` | a Rust solution as LeetCode's Rust users write it (`s.as_bytes()`, a `vec![vec![0; n]; n]` table of the longest palindromic subsequence of each span filled from the last row up, `dp[i + 1][j].max(dp[i][j - 1])` where the ends differ, and the answer `(n as i32 - dp[0][n - 1]) <= k`), carried to Kāra by `karac fix` |
| `valid_palindrome_iii_rows.kara` | another Rust solution (the longest common subsequence of the bytes and the bytes reversed, in two `vec![0usize; n + 1]` rows exchanged by `std::mem::swap(&mut prev, &mut curr)`, and the answer `n - prev[n] <= k as usize`), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six more properties |

Every arm prints the same 15 lines: LeetCode's two examples; `a`, `ab`
and `abc` with `k = 1` (`true`, `true`, `false`); `abcd` with `k = 2`
and 3 (`false`, `true`); `racecar` and `abacdcaba` with `k = 1` (`true`);
`abxcydzba` with `k = 2` (`false`); 1000 random small cases, 1 to 12
letters from the first two to four with `k` from 1 to the length
(`1000 small cases: 870 true, checksum 859636424`); and four at the
constraints' top, 1000 letters, each searched by halving for the least
`k` that answers true: random letters from 26 (`674`, and `673` false),
random `a` and `b` (`189`), 500 letters followed by their reverse, true
already at `k = 1`, and `a` to `z` over and over (`923`).
`valid_palindrome_iii.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac run` and
`karac build`, and under the AddressSanitizer build. The budget arm pays
for its budget on the four long lines, where the least `k` runs to
hundreds: its built binary takes about 18 s, against 24 ms for the ★
arm's, and `karac __mir-run` about 13 minutes, so its interpreter run was
checked with a longer timeout than the others.

The Mend loop: the ★, table, common and budget arms check clean as
written. The grid arm takes one round of 4 fixes (`struct Solution;` to
`struct Solution {}`, `s.as_bytes()` to `s.bytes()`, and `vec![vec![0;
n]; n]` to `Vec.filled(n, Vec.filled(n, 0))`), and the rows arm one round
of 16 (among them `Vec<u8>` to `Vec[u8]`, `s.bytes().rev().collect()` to
`s.bytes().iter().rev().collect()`, `vec![0usize; n + 1]` to
`Vec.filled(n + 1, 0)`, `std::mem::swap(&mut prev, &mut curr)` to
`swap(mut prev, mut curr)`, and `k as usize` to `k`). Both outputs match.

## Gaps

None found.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every way to keep some of the letters, those that remove at
most `k`, each kept string read both ways. 2000 random cases: 1 to 12
letters from the first five to seven, `k` from 1 to a third of the
length and one more; 902 of them answer true.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the string reversed gives the same |
| P3 | true at `k` stays true at `k + 1` |
| P4 | one letter put at both ends gives the same |
| P5 | `a` and `b` exchanged give the same |
| P6 | a letter put at the end, with `k` one more, keeps a true answer true |
| P7 | the ★ arm's answer |

All 84,000 checks pass on every arm: `2000 cases: checksum 258131081,
84000 checks over 6 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and the AddressSanitizer build. A Python reading of
the same cases, trying every set of kept letters with
`itertools.combinations`, gives the same checksum.

## Mutation testing

Twelve edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac run`, each failing the same way under both. All
twelve are caught.

| # | mutation | failures by property |
|---|---|---|
| S1 | ★: a pair of equal ends counted as one letter | P1 416, P4 314, P7 2080 |
| S2 | ★: the inside's answer never carried along | P1 372, P4 371, P7 1860 |
| T1 | table: a mismatched end dropped for nothing | P1 1098, P7 1098 |
| T2 | table: the whole string's span never filled | P1 1098, P7 1098 |
| C1 | common: the string matched against itself, not its reverse | P1 1098, P7 1098 |
| C2 | common: only the row above consulted | P1 317, P2 200, P4 273, P7 317 |
| B1 | budget: every count stored as exact | P1 11, P2 25, P6 1, P7 11 |
| B2 | budget: only the left end ever dropped | P1 235, P2 283, P6 142, P7 235 |
| G1 | grid: a single letter counted as none | P1 406, P7 406 |
| G2 | grid: only the left end ever dropped | P1 235, P2 283, P6 142, P7 235 |
| W1 | rows: the rows never exchanged | P1 743, P4 159, P7 743 |
| W2 | rows: a match extends the cell above | P1 137, P4 204, P7 137 |

A mutation of the ★ arm fails P7 on all six arms, the ★ arm against the
other five. Of the 2000 cases 1098 answer false. T1, T2 and C1 answer
true every time, T1 dropping a mismatched end for nothing, T2 never
filling the span of the whole string, which stays at 0, and C1 matching
the string against itself, all of which it keeps; each fails exactly the
1098. B2 and G2 are one fault in two arms, only the left end of a span
ever dropped, and fail alike. B1 stores a count found beyond the budget,
only a bound below the true one, as if it were exact, so a span reached
again by a path with more budget left takes the bound for its cost; it
answers true in 11 false cases, the cases a Python copy of the mutated
arm gets wrong, which needed spans reached twice with different budgets:
at first the cases held at most 10 letters and `k` at most a quarter of
the length plus one, and caught nothing, so the lengths and budgets were
raised to what they are. P3, true at `k` staying true at `k + 1`, and
P5, `a` and `b` exchanged, catch none of the twelve: no edit makes an
arm's answer fall as the budget grows, or treat one letter differently
from another.

## Benchmarks

`bench/` runs the same workload in Kāra, C, Rust, Go and Python: the ★
arm (the longest palindromic subsequence, one row at a time) on 48
strings of 1000 letters, the constraints' most, drawn once from 2, 4, 8
or 26 letters, each asked with k = 200, 400, 600 and 800; every answer
folded into a checksum. Every program prints `48 strings of 1000
letters, 4 budgets each: 119 true, checksum 130735515`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `684b860a50`
on LLVM 22. A plain `karac build` targets x86-64-v2, so the C and
overflow-checked Rust programs are also built at x86-64-v3 for
comparison:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 0.141 to 0.168 s | 0.151 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.141 to 0.153 s | 0.147 s |
| Rust (`rustc -O`) | 0.108 to 0.139 s | 0.116 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.092 to 0.152 s | 0.102 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.093 to 0.149 s | 0.107 s |
| C (`clang -O3`) | 0.171 to 0.240 s | 0.183 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.268 to 0.326 s | 0.282 s |
| Go | 0.317 to 0.395 s | 0.334 s |
| Python | 10.07 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Rust with overflow checks on is about 31% ahead of Kāra (0.102 s
against 0.147 s), and the two ranges overlap. Kāra is about 20% ahead of
C (0.147 s against 0.183 s); Go takes about 2.3x Kāra's time. Python
takes about 69x Kāra's time. No profile was taken.
