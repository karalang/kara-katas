# 1143. Longest Common Subsequence

Given two strings `text1` and `text2`, return the length of their longest
common subsequence. If there is no common subsequence, return `0`.

A subsequence of a string is a new string generated from the original
string with some characters (can be none) deleted without changing the
relative order of the remaining characters. For example, `"ace"` is a
subsequence of `"abcde"`.

A common subsequence of two strings is a subsequence that is common to
both strings.

```
text1 = "abcde", text2 = "ace"  ->  3     ("ace")
text1 = "abc",   text2 = "abc"  ->  3     ("abc")
text1 = "abc",   text2 = "def"  ->  0
```

**Constraints:** `1 <= text1.length, text2.length <= 1000`; `text1` and
`text2` consist of only lowercase English characters.

The arms are `fn longest_common_subsequence(text1: String, text2:
String) -> i64`.

## Approaches

| file | mechanism |
|---|---|
| `longest_common_subsequence.kara` ★ | a table of the longest common subsequence of every two prefixes, in nested `Vec.filled` rows, filled row by row: one more than the two prefixes without their last letters when those letters match, and otherwise the longer of the two with one letter dropped. O(m * n) |
| `longest_common_subsequence_rows.kara` | the table kept one row at a time over the shorter text's bytes: the row so far and the one being filled, swapped with `mem.swap` after each letter. O(m * n) time, O(min(m, n)) space |
| `longest_common_subsequence_memo.kara` | recursion on the first letters, each pair of suffixes remembered in a `Map[(i64, i64), i64]` once found. O(m * n) |
| `longest_common_subsequence_hunt.kara` | as a longest increasing subsequence (Hunt and Szymanski): each letter of `text1` stands for the places its letter has in `text2`, latest first, and the longest strictly rising run of places is kept as the least last place of a run of every length, found by binary search. O((m + r) log n), r the matching pairs |
| `longest_common_subsequence_solution.kara` | a Rust solution as LeetCode's Rust users write it (`impl Solution`, `text1.as_bytes()`, a `vec![vec![0; n + 1]; m + 1]` table, `.max()` and an `i32` answer), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five properties |

Every arm prints the same 12 lines: LeetCode's three examples; one
letter each, alike and not; one text inside the other (3); a text and
itself backwards (1); `abab` and `baba` (3). Then over 2000 random pairs
of 1 to 40 letters from 2, 4 or 26 letters, the answers summed and a
checksum (`2000 random pairs: answers total 17620, checksum
180185282`), and three pairs of the longest the constraints allow, 1000
letters each: from 4 letters (648), from 26 (318), and a text against
itself with every tenth letter changed to `z` (903).
`longest_common_subsequence.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: of every subsequence of `text1`, every choice of its letters
kept in order, the longest that can also be read in order in `text2`. It
checks 2000 pairs of 1 to 8 letters in four kinds of 500: from 2
letters; from 3; from 26; and the second text the first with 0 to 4
letters put in among it, so the answer is the first text's length. Every
random choice, P4's renaming, P5's letter and P6's cut among them, is
drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal one |
| P2 | the texts the other way round give the same answer |
| P3 | both texts backwards give the same answer |
| P4 | every letter renamed alike, moved on 1 to 25 places round the alphabet, gives the same answer |
| P5 | one letter put after both texts gives one more |
| P6 | a letter taken out of `text1` gives the same answer or one less |

All 60,000 checks pass on every arm: `2000 pairs: checksum 815352339,
60000 checks over 5 arms: 0 failures`. A Python reading of the same
pairs, by the same search over subsequences, with the six properties
asserted against the ★ arm's mirror, gives the same line.

## Mutation testing

Thirty edits to the differential, six to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run` with `KARAC_HASH_SEED=1`,
each failing the same way under both. Twenty-seven are caught; three are
equivalent. The ★ arm's answer capped at `text1`'s length is never above
it. The rows arm copying the new row over the old instead of swapping
them leaves the row being filled holding old values, but every one it
reads has been written again first. The rows arm not ordering the texts
by length keeps its row over `text2` whatever its length, which costs
memory and changes no answer. Fifteen are kept, no two failing the same
checks; one of them stops the run.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a match adds to the row above | P1 522, P2 763, P5 184 |
| M2 | ★: a letter of `text2` never dropped | P1 1011, P2 1129, P3 899, P6 129 |
| M3 | ★: a mismatch counted as a match | P1 1058 |
| M4 | rows: a match adds to the row being filled | P1 305, P2 71, P5 119, P6 48 |
| M5 | rows: a letter of the short text never dropped | P1 410, P2 64, P3 462, P6 109 |
| M6 | rows: the row before the last read | P1 564, P2 37, P3 592, P5 1012, P6 14 |
| M7 | memo: the end only when both texts end | stops: index out of bounds |
| M8 | memo: a letter of `text2` never dropped | P1 1003, P2 1095, P3 899, P5 1383, P6 140 |
| M9 | memo: positions remembered the wrong way round | P1 520, P2 729, P3 633, P5 399, P6 97 |
| M10 | hunt: places taken earliest first | P1 519, P2 763, P5 242, P6 134 |
| M11 | hunt: the search over the first half | P1 1162, P5 1689 |
| M12 | hunt: a run's end lowered to one past the place | P1 724, P2 454, P3 189, P5 316, P6 28 |
| M13 | solution: a match counted twice | P1 1689, P5 2000, P6 967 |
| M14 | solution: the shorter of the two kept | P1 1357, P3 896, P6 154 |
| M15 | solution: never below 1 | P1 311, P5 311 |

P1 catches all fourteen edits that let the run finish. P5 and P6 catch
ten each: they compare texts one letter apart, so they see answers that
step by other than one. A match counted twice (M13) fails P5 on every
pair, and the search over half the runs (M11) on 1689; an answer of 1
where there is none (M15) fails P5 exactly where it fails P1, since one
letter put after both gives 1 either way. P2 catches nine, the edits that treat the two texts unlike: one text's
letters never dropped (M2, M5, M8), a match added to one neighbour
rather than the diagonal (M1, M4), positions remembered the wrong way
round (M9), the row before the last read (M6), and the hunt arm's places, which only `text2` has (M10,
M12). P3 catches seven, the edits whose answers depend on which end the
texts are read from. Only P1 sees a mismatch counted as a match (M3): it
answers the shorter text's length, which is symmetric, the same read
backwards, one more with a letter put after both, and at most one less
without a letter. P4 catches none of the thirty: every arm, and every
edit, compares letters only with each other, so no answer can see what
the letters are. The edit that stops the run is the memo arm's end
taken only when both texts end, which reads one text's letter past its
last.

Of the twelve caught and not kept, two fail exactly as a kept one: the
memo arm keeping its letter of `text2` on a match, and the hunt arm
letting a run stay in place, as M1. The other ten each fail in a way of
their own and were not needed, though two of them fail alike: the last
letter of `text2` never read in the ★ arm and the last letter of `text1`
never read in the solution arm. The rest are a match at equal places
ignored (★), the first letter of the short text never read (rows),
remembered answers capped at 3 and the two first letters never matched
(memo), each letter's last place only and its two last places only
(hunt), and a letter of `text1` never dropped and `text2` read backwards
(solution).

## Verification

Every arm prints the same output as `longest_common_subsequence.py`
under `karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`,
and `karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
every arm and the differential. `karac check --output=json` reports
nothing on any file, and `karac fix` has nothing to apply.

The ★, memo and hunt arms were written as Kāra and checked clean as
written. `karac fix` carried the rows arm in two rounds: `std.mem.swap`
to `mem.swap`, then `short.bytes().collect()` to
`short.bytes().iter().collect()`, since `bytes()` is a `Slice[u8]` and
not an iterator (`docs/library/strings.md`). It carried the solution arm
in five rounds: `Solution::` to `Solution.`; then `struct Solution {}`
declared; then `as_bytes()` to `bytes()` on both texts, `0i32` on the
table's literal and the `as i64` that widens the call's `i32` for
nothing dropped; then the table's inner `vec!` to `Vec.filled`; then its
outer `vec!`. In the differential, `karac check` refuses `*i` on an
`enumerate` index in a `filter` closure, an `i64` the closure has by
value, and `karac fix` drops the `*`; the differential is written
without it.

The kata found no gaps.

## Benchmarks

The bench builds 20 texts of 1000 letters from `a` to `d` once,
LeetCode's longest, as 10 pairs. Each of 10 rounds draws one letter of
every text again and answers every pair with the ★ arm: 100 calls, each
filling a 1001 by 1001 table. Every implementation prints `10 rounds over
10 pairs of 1000 letters: answers total 64893, checksum 77796719`. Each
makes the table row by row in every call: nested `Vec.filled` in Kāra,
`vec![vec![0; n + 1]; m + 1]` in Rust, `calloc` in C, `make` in Go and
list repetition in Python.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `5ebdf9b7d9`
on LLVM 22. karac builds for the x86-64-v3 baseline, so the C and
overflow-checked Rust programs are also built at `-march=x86-64-v3`:

| | time | median |
|---|---|---|
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.189 to 0.359 s | 0.259 s |
| Kāra (`karac build`) | 0.225 to 0.349 s | 0.269 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.374 to 0.630 s | 0.403 s |
| C (`clang -O3`) | 0.360 to 0.488 s | 0.405 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.425 to 0.587 s | 0.460 s |
| Rust (`rustc -O`) | 0.410 to 0.635 s | 0.464 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.431 to 0.564 s | 0.469 s |
| Go | 0.352 to 0.546 s | 0.505 s |
| Python | 14.1 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. C takes about 1.56x Kāra's median time and Rust about 1.8x, but
most of that is not their own work: each call frees 8 MB of rows, glibc
gives the top of its heap back to the kernel, and the next call faults
it in again, 6003 `brk` calls in C's run under `strace` to Kāra's 126 in
all. By user time C takes about 0.6x Kāra's (0.155 to 0.159 s to 0.254
s) and Rust about 0.9x. Go takes about 1.95x Kāra's median time and
Python about 54x.
