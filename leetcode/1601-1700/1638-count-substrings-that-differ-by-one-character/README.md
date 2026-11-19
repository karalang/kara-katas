# 1638. Count Substrings That Differ by One Character

Given two strings `s` and `t`, find the number of ways you can choose a
non-empty substring of `s` and replace a **single character** by a
different character such that the resulting substring is a substring of
`t`. In other words, find the number of substrings in `s` that differ
from some substring in `t` by **exactly** one character.

For example, the underlined substrings in `"computer"` and
`"computation"` only differ by the `'e'`/`'a'`, so this is a valid way.

Return *the number of substrings that satisfy the condition above.*

A **substring** is a contiguous sequence of characters within a string.

```
s = "aba", t = "baba"   ->  6
s = "ab", t = "bb"      ->  3
```

**Constraints:** `1 <= s.length, t.length <= 100`; `s` and `t` consist
of lowercase English letters only.

## Approaches

| file | mechanism |
|---|---|
| `differ.kara` ★ | every counted pair has one mismatched position (i, j); a `left` table of matching runs ending just before it and a `right` table of runs starting just after it, each filled in one pass, give (left + 1) * (right + 1) pairs for every mismatch. O(nm) |
| `differ_brute.kara` | from every pair of starts, both substrings extended one letter at a time while the mismatches are counted: each length with exactly one is a pair, and a second ends the walk. O(nm min(n, m)) |
| `differ_diagonal.kara` | a pair of equal-length substrings lies on one diagonal, i - j fixed; one walk per diagonal keeps the run of matches before the latest mismatch and the run since, and each step past a mismatch adds the earlier run plus one. O(nm) time, O(1) extra space |
| `differ_solution.kara` | LeetCode's Rust template: for each mismatch, walk left and right over matching letters and add (l + 1) * (r + 1). Carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's two examples, one letter
alike (0), `"abe"` against `"bbc"` (10), and words with no letter in
common; then the counts summed and a checksum for 3000 random pairs of
up to 6 letters from a and b, 300 of up to 100 letters from a to c, and
20 of up to 100 letters from the whole alphabet. `differ.py` mirrors the
★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every substring of `s` against every substring of `t` of the
same length, counted when exactly one position differs. It checks 3000
random pairs of words of 1 to 6 letters, every other pair from the
letters a and b, so long runs match, the rest from a to e. Every pair is
drawn before any arm answers.

| | property |
|---|---|
| P1 | the count is the statement read literally |
| P2 | the two words swapped give the same count |
| P3 | both words reversed give the same count |
| P4 | the letters renamed alike in both words, a to b and so on round to a, give the same count |
| P5 | the count is at least the number of mismatched letter pairs, and at most the number of pairs of substrings of equal length |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 184901474, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. The first M4 tried, the brute arm
stopping its walk at a third mismatch rather than a second, survived and
is equivalent: past the second mismatch nothing more is counted, so the
walk only runs longer. It was replaced. A walk capped at three letters
(M5) is the hardest to catch: only 241 pairs have a counted pair longer
than that among words of up to six letters.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the two runs added, not multiplied | P1 2903, P5 1199, P6 2903 |
| M2 | ★: the right run read at the mismatch itself | P1 1500, P3 1377, P6 1500 |
| M3 | ★: every left run 1 | P1 477, P3 561, P6 477 |
| M4 | brute: pairs with no mismatch counted too | P1 2582, P6 2582 |
| M5 | brute: no pair longer than three letters | P1 241, P6 241 |
| M6 | diagonal: the run before a mismatch never kept | P1 1494, P3 1377, P6 1494 |
| M7 | diagonal: the run since the mismatch added, not the one before | P1 1437, P3 1416, P6 1437 |
| M8 | diagonal: the last diagonal never walked | P1 1941, P2 1204, P3 1204, P5 803, P6 1941 |
| M9 | template: the left walk not bounded by j | panics on both backends: index out of bounds |
| M10 | template: l * r + 1, not (l + 1) * (r + 1) | P1 1790, P6 1790 |

## Benchmarks

The bench draws 5000 random pairs of 100-letter words over the letters a
to c, LeetCode's longest, all of them first, then counts each pair by the
★ arm in all five languages, the two run tables allocated per call:
nested `Vec`s in Kāra, Rust and Go, lists in Python, and one flat
`calloc` each in C. Every implementation prints `5000 pairs of 100
letters: counts sum to 73505353, checksum 493819250`. The C build also
runs clean under gcc's AddressSanitizer and UndefinedBehaviorSanitizer.

TIMINGS

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. PARNOTE

## Verification

All four arms print the same output as `differ.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `SHA`.

## Writing it

The ★ arm first took the words' bytes with Rust's `s.as_bytes()`, which
the check refused with the name of Kāra's: `.bytes()`, a `Slice[u8]`
(library/strings.md). `karac fix` wrote it, and the harness's
`'a' as u8` became the byte literal `b'a'`, since a `char` does not
narrow to a `u8` by a plain cast. The diagonal arm's
`let (mut i, mut j) = ..` became `let mut (i, j) = ..`. The brute arm
checked clean as first written.

LeetCode's Rust template takes one `karac fix` of 8 edits:
`as_bytes()` to `bytes()`, `&&` to `and`, `Solution::` to `Solution.`,
and the harness wrapper's `Solution::count_substrings(s, t) as i64`
lost its cast, which the `lossless_cast` lint calls unnecessary: an
`i32` widens to the wrapper's `i64` result by itself. The arm then
checks and agrees with no hand edit.
