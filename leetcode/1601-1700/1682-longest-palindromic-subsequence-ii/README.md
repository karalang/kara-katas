# 1682. Longest Palindromic Subsequence II

A subsequence of a string `s` is considered a **good palindromic
subsequence** if:

- It is a subsequence of `s`.
- It is a palindrome (has the same value if reversed).
- It has an **even** length.
- No two consecutive characters are equal, except the two middle ones.

For example, if `s = "abcabcabb"`, then `"abba"` is considered a **good
palindromic subsequence**, while `"bcb"` (not even length) and `"bbbb"`
(has equal consecutive characters) are not.

Given a string `s`, return *the **length** of the **longest good
palindromic subsequence** in* `s`.

```
s = "bbabab"       ->  4    ("baab")
s = "dcbccacdb"    ->  4    ("dccd")
```

**Constraints:** `1 <= s.length <= 250`; `s` consists of lowercase
English letters.

## Approaches

| file | mechanism |
|---|---|
| `palindrome.kara` ★ | `best[i][j][c]`, the longest good palindromic subsequence of s[i..=j] whose outer letter is c, in a `Vec[Vec[Array[i32, 26]]]`: when s[i] and s[j] are both c they are its outer pair, around the longest of the stretch inside whose outer letter is not c; else one end is not used. O(n^2 * 26) |
| `palindrome_memo.kara` | a memoized search, `longest(i, j, outer)`: the longest in s[i..=j] whose outer letter is not `outer`, the layer around it (26 for none); equal ends of another letter are its outer pair, else either end is dropped. A flat `Vec[i32]` memo of n * n * 27. O(n^2 * 27) |
| `palindrome_outermost.kara` | a layer of letter c is best taken as far out as it goes, the first c at or after the stretch's start and the last at or before its end, from tables of the next and previous place of each letter; each stretch tries every letter but the one around it, memoized in a `Map` keyed by a tuple. O(n^2 * 26) states at worst |
| `palindrome_solution.kara` | a Rust solution as LeetCode's Rust users write it, the ★ arm's table as `vec![vec![vec![0; 26]; n]; n]` over `s.as_bytes()` with `usize` letters, carried to Kāra by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 8 lines: LeetCode's two examples, one letter
(0), one letter four times (2), and a palindrome whose layers alternate
(6); then the answers summed and a checksum for 3000 random strings of
up to 10 letters from the first 3 of the alphabet, 300 of up to 60 from
4, and 10 of up to 250, LeetCode's longest, from all 26. `palindrome.py`
mirrors the ★ arm and its output is byte-identical.

```
4
4
0
2
6
3000 strings of up to 10 letters from 3: answers sum to 8220, checksum 26694227
300 strings of up to 60 letters from 4: answers sum to 4866, checksum 821709786
10 strings of up to 250 letters from 26: answers sum to 436, checksum 603013834
```

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every subsequence, from all `2^n` choices of places, is kept
when it is even, a palindrome, and has no two equal neighbours but the
middle two; the longest wins. It checks 3000 random strings of 1 to 12
letters from the first 1 to 4 of the alphabet, each with a shift to
rename its letters by. Every case is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the string reversed gives the same answer |
| P3 | every letter moved along the alphabet by one shift gives the same answer |
| P4 | a `z`, which the string does not hold, at both ends gives two more |
| P5 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 227571566, 60000 checks
over 4 arms: 0 failures` under every lane in Verification, and a Python
reading of the statement, by `itertools.combinations`, gives the same
checksum. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Ten edits to the differential, two to four to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. A first M9 read the solution arm's
inside from `dp[i + 1][j]` for `dp[i + 1][j - 1]`; with s[j] the outer
letter c and the inside's outer letter not c, the stretch to j holds
nothing more, so it changed no answer, and it was replaced. M1, M4 and
M6 all let a layer repeat the letter around it and fail the same
checks. M10 never tries `z` as an outer letter, and only P4, which puts
a `z` at both ends, sees it.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the inside may have the same outer letter | P1 1178, P5 1178 |
| M2 | ★: an outer pair counted as one | P1 2585, P4 3000, P5 2585 |
| M3 | ★: only the start dropped, never the end | P1 871, P2 954, P5 871 |
| M4 | memo: equal ends taken whatever the layer around | P1 1178, P5 1178 |
| M5 | memo: a single letter's stretch searched on | P1 1226, P5 1226 |
| M6 | memo: the inside told the old layer, not the new | P1 1178, P5 1178 |
| M7 | outermost: the last place looked for one before the end | P1 942, P2 563, P4 2460, P5 942 |
| M8 | outermost: a letter's first and last place may be one | P1 671, P5 671 |
| M9 | solution: the inside's best read at the outer letter itself | P1 1442, P4 2585, P5 1442 |
| M10 | solution: the letter `z` never tried | P4 3000 |

## Benchmarks

The bench draws 200 random strings of 250 letters, LeetCode's longest,
from the first 4 of the alphabet, all of them first, then answers each
2 times by the ★ arm in all five languages. Every implementation prints
`200 strings of 250 letters, 2 rounds: answers sum to 53400, checksum
659453338`. The C build also runs clean under gcc's AddressSanitizer
and UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `9b0b5eb92c` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.301 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.675 s |
| Kāra (`karac build`) | 0.696 s |
| Go | 1.196 s |
| Rust (`rustc -O`) | 1.307 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.343 s |
| Python | 36 s |

The sequential Kāra build is 48% faster than Rust and 50% faster than
Rust with overflow checks on, the equal-safety comparison
(BENCHMARKS.md). C is the fastest here at 0.301 s.

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here:
its user time is not above its real time (0.638 s and 0.643 s on one
run).

## Verification

All four arms print the same output as `palindrome.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `9b0b5eb92c`.

## Writing it

The ★, memo and outermost arms checked clean as first written.

LeetCode's Rust template took `karac fix` twice. The first run wrote
`struct Solution {}`, `s.as_bytes()` as `s.bytes()`, the nested `vec!`s
as `Vec.filled(n, Vec.filled(n, Vec.filled(26, 0)))`, and `&&` as
`and`. That left the answer, `*dp[0][n - 1].iter().max().unwrap()`, an
`i64` returned as `i32`: the fill's `0` kept the default, since nothing
the loops write fixes it. `karac check` refused the return (E0200, a
narrowing coercion) with no fix until kara `93fd9b2078` (B-2026-11-20-36); since
then the walk of a row of a fill of fills reads its elements, and the
second run wrote `0i32` in the fill, `inner: i32` at the inner `let`,
and dropped the two `as usize` casts, which compare with `c` as they
are.

`arm_name` in the differential indexes a list of string literals for a
`Str`, as #1662's does (B-2026-11-19-131).
