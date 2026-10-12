# 424. Longest Repeating Character Replacement

You are given a string `s` and an integer `k`. You can choose any
character of the string and change it to any other uppercase English
character. You can perform this operation at most `k` times. Return the
length of the longest substring containing the same letter you can get
after performing the above operations.

```
s = "ABAB",    k = 2  -> 4
s = "AABABBA", k = 1  -> 4
```

**Constraints:** `1 <= s.length <= 10^5`; `s` holds only uppercase
English letters; `0 <= k <= s.length`.

## Approaches

| file | mechanism | time | space |
|---|---|---|---|
| `character_replacement.kara` ★ | a window that never shrinks: count the window's letters and the largest count seen so far; when the letters other than that count exceed `k`, slide the window right by one instead of shrinking it. The answer only grows when some count passes the best seen, so the stale best does no harm, and the final width is the answer | O(n) | O(1) |
| `character_replacement_shrink.kara` | the textbook window: after each letter, shrink from the left until the window minus its commonest count (read from all 26 counts) is at most `k`, and keep the widest | O(26 n) | O(1) |
| `character_replacement_letter.kara` | one letter at a time: for each letter, a two-pointer pass for the widest window with at most `k` other characters | O(26 n) | O(1) |
| `character_replacement_binary.kara` | binary search on the length: a window that works contains shorter ones that work, so test each length by sliding a window of exactly that many letters | O(26 n log n) | O(1) |
| `differential.kara` | the four arms on 2,000 random strings, five properties, one of them every window counted from scratch | — | — |

Every arm prints the same 11 lines: the two LeetCode examples, eight
edge cases (one letter with `k` 0 and 1, five different letters with
`k` 0 and 2, four equal letters, a run then another letter, and a run
between two other letters with `k` 1 and 2), and for 2,000 random strings of 1 to
60 letters from the first 1 to 5 letters, written in runs, with `k`
from 0 to 6, the total of the answers and a checksum.
`character_replacement.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms. Each of 2,000 random
cases is a string of 1 to 30 letters from the first 1 to 4 letters,
written in runs, with `k` from 0 to 5:

| | property |
|---|---|
| P1 | the answer is that of counting every window from scratch |
| P2 | renaming the letters (A to Z, B to Y, ...), or reversing the string, gives the same answer |
| P3 | one more replacement never lowers the answer; the answer is at least the longest run plus `k` and at most the commonest letter's count plus `k`, both capped at the length |
| P4 | the string written twice gives at least the answer; with as many replacements as letters other than the commonest, the answer is the whole length |
| P5 | one letter `m` times gives `m`; A and B alternating `m` times give the smaller of `m` and `2k + 1` |

It prints `2000 cases, 4 arms, 40000 checks, 0 failures` under
`karac __mir-run`, and a count for each property when anything fails.

## Mutation testing

Eight edits to `differential.kara`, each run under `karac __mir-run`.
All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | grow: the best count is the current letter's, not the best seen | P1 353, P2 548, P3 195, P4 904 |
| M2 | grow: the window is bad only with `k + 1` others too many | P1 1023, P3 442, P5 1623 |
| M3 | shrink: the window may hold `k + 1` others | P1 1023, P3 442, P5 1623 |
| M4 | shrink: the best width is one short | P1 2000, P3 1548, P4 2000, P5 2000 |
| M5 | letter: only the letters A to D are tried | P2 1812, P5 1829 |
| M6 | letter: a dropped other counts twice | P1 870, P2 657, P3 660, P5 1550 |
| M7 | binary: the letter leaving the window is not removed | P1 264, P2 381, P5 1550 |
| M8 | binary: a window needs fewer than `k` replacements | P1 1195, P3 903, P4 1923, P5 1719 |

M2 and M3 fail exactly the same checks: both arms then answer the
question for `k + 1`. Only P2 and P5 see M5, because the random strings
use only A to D; the renaming in P2 moves them to W to Z, and P5 writes
H. M1 is the one the ★ arm's comment argues against: keeping the
current letter's count instead of the best seen lets the window slide
when it should grow. P5 cannot see it, since a single letter or an
alternating pair reaches its best count again at every step.

Two first drafts of mutants were replaced: shrinking while the others
reach `k` (not exceed it) runs the window past its right end when `k`
is 0 and panics on an index, and moving the left end without dropping
its count never stops.

## Verification

All four arms print the same output as `character_replacement.py`
under `karac __mir-run` (the v2 MIR interpreter),
`karac __mir-llvm-run` and `karac run --interp`, and `karac check`
passes on every file. The differential prints `40000 checks, 0
failures` on the same three.

LLJIT, `karac build` and `KARAC_AUTO_PAR=1 karac build` stop in the
frozen legacy codegen, which has no `bytes()` on a `Str` parameter
(`no handler for method 'bytes' on variable 's'`), as in kata 420.
Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm on one text of 1,000,000 letters from
A to E written in runs of 1 to 8. Each of 3,000 calls reads a slice of
10,000 to 99,999 letters (the problem's limit) with `k` from 0 to 49;
each slice is a view, so no call copies the text. It folds the answers
into a total and a checksum. Every implementation prints `3000 calls:
total 237981, checksum 574365189`; a 20-call cut of the Kāra program
under `karac __mir-run` prints the same as the C program cut the same
way. Spot timings on a shared 4-core container, three runs each
(`bench.sh` timings need a quiet machine):

| | time |
|---|---|
| Rust (`rustc -O`) | 0.36 to 0.40 s |
| C (`clang -O3`) | 0.37 to 0.42 s |
| Go | 0.37 to 0.45 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.41 to 0.46 s |
| Python | 36 s |

No `karac build` time: the frozen legacy codegen has no `bytes()` on a
`Str` parameter (see Verification). The Kāra program prints the same
line under `karac __mir-llvm-run` in 2.8 s, compile included; that JITs
the MIR's IR without optimization passes, so it is not a benchmark.

## Compiler findings

No new findings.
