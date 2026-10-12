# 434. Number of Segments in a String

Given a string `s`, return the number of segments in it. A segment is a
contiguous sequence of non-space characters.

```
s = "Hello, my name is John"   ->  5
s = "Hello"                    ->  1
```

**Constraints:** `0 <= s.length <= 300`; `s` holds lowercase and
uppercase English letters, digits and the characters
`"!@#$%^&*()_+-=',.:"`; the only space character in `s` is `' '`.

## Approaches

Every segment has exactly one first character, so counting segments is
counting the non-spaces that start one. The arms find them in
different ways; all four are O(n).

| file | mechanism |
|---|---|
| `count_segments.kara` ★ | one pass over the bytes, counting each non-space that is the first byte or follows a space. O(1) space |
| `count_segments_split.kara` | `s.split(" ")`, counting the pieces that are not empty: two spaces in a row, or a space at either end, leave an empty piece. The pieces are views into the string, made lazily |
| `count_segments_state.kara` | a walk over the characters remembering whether it is inside a segment; a non-space outside one enters it and counts it |
| `count_segments_gaps.kara` | trims the spaces at both ends, then counts the runs of spaces left between the first and last non-space: one segment more than runs, and none for a string of only spaces |
| `differential.kara` | the four arms on 1,500 random strings, five properties |

Every arm prints the same 11 lines: the two LeetCode examples, eight
edge cases (the empty string, one space, only spaces, spaces at both
ends, runs of spaces between letters, one segment of every symbol, and
a lone letter with and without spaces around it), and for 1,000 random
strings of up to 60 characters, a third of them spaces, the total
count and a checksum of the counts. `count_segments.py` mirrors the ★
arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and runs them on
1,500 random strings of 0 to 80 characters, with a space in every 2, 3
or 8 characters on average.

| | property |
|---|---|
| P1 | the count is the reference's, which counts segment ends (a non-space followed by a space or by the end) rather than starts |
| P2 | joining two strings with a space between them adds their counts |
| P3 | doubling every space and padding both ends with 0 to 3 spaces changes nothing |
| P4 | replacing every non-space with `x` changes nothing, and a string of length n has at most (n + 1) / 2 segments |
| P5 | k spaces have no segments, k copies of `"w "` have k, and k letters with no space have one (none when k is 0) |

It prints `1500 cases, 4 arms, 30000 checks, 0 failures` under
`karac __mir-run`, and a count for each property when anything fails.

## Mutation testing

Eight edits to `differential.kara`, two to each arm, each run under
`karac __mir-run`. All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | starts: a segment at the start of the string is not counted | P1 1001, P2 1030, P3 746, P5 1368 |
| M2 | starts: a leading space counts as a segment | P1 481, P2 458, P3 763, P4 3, P5 1368 |
| M3 | split: empty pieces are counted | P1 1236, P3 1486, P4 308, P5 1500 |
| M4 | split: one-letter pieces are not counted | P1 1129, P5 1368 |
| M5 | state: a space does not end a segment | P1 1371, P2 1450, P5 1239 |
| M6 | state: every letter starts a segment | P1 1425, P4 1119, P5 1239 |
| M7 | gaps: trailing spaces are not trimmed | P1 488, P2 500, P3 733, P4 7, P5 1368 |
| M8 | gaps: every space is a gap, not every run of them | P1 1039, P2 770, P3 1371, P4 132 |

P1 kills all eight; the others each see a part. P2 cannot see a
mutant that stays additive over a joining space: counting every piece
(M3), only the longer ones (M4) or every letter (M6) still adds up. P3 misses
mutants that the padding and doubled spaces cannot move (M4, M5, M6):
a run of spaces that is longer, or starts or ends the string, changes
nothing they count. P4's flattening keeps every space where it was, so
it only catches mutants whose count can exceed the (n + 1) / 2 bound,
and P5 catches all but M8, whose spaces in `"w "` are all single.

## Verification

All four arms print the same output as `count_segments.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run` and
`karac run --interp` (the legacy tree-walk interpreter), and
`karac check` passes on every file. The differential prints
`30000 checks, 0 failures` under all three. The four arms and the
differential also run clean under `karac __mir-llvm-asan`
(AddressSanitizer and LeakSanitizer): output identical, no error, no
leak.

The frozen legacy code generator (LLJIT, `karac build` and
`KARAC_AUTO_PAR=1 karac build`) compiles none of the files, the bench
program and the differential included. It has no handler for `bytes()`
or `split` on a `Str` parameter (`no handler for method 'bytes' on
variable 's'`, as in kata 430), and it panics in `control_flow_for.rs`
on the state arm's `for c in s.chars()` over one. Legacy is frozen, so
this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It builds one text of 1,000,000
characters, words of 1 to 8 random letters between runs of 1 to 3
spaces, then counts the segments in 10,000 windows of it, each of a
random length below 32,768 at a random place. A window is a `Str` view
of the text, `text[start..start + length]`, so nothing is copied; the
work is the counting, about 164 million bytes in all. Every
implementation prints `10000 windows of a text of 1000000: 25053507
segments, checksum 675042431`; a 20-window cut of the Kāra program
under `karac __mir-run` prints the same as the C program cut the same
way.

The mirrors count over a borrowed slice of the text too: `&str` in
Rust, a substring in Go (which shares the bytes), a pointer and length
in C. Python's slice copies, which is cheap beside its loop. Spot
timings on a shared 4-core container, three runs each (`bench.sh`
timings need a quiet machine):

| | time |
|---|---|
| Rust (`rustc -O`) | 0.28 to 0.30 s |
| Go | 0.42 to 0.46 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.45 to 0.48 s |
| C (`clang -O3`) | 0.46 to 0.51 s |
| Python | 9.5 to 10.1 s |

The frozen legacy `karac build` cannot build the program (see
Verification), so there is no legacy time. The Kāra program prints the
same line under `karac __mir-llvm-run` in 1.5 s, compile included; that
JITs the MIR's IR without optimization passes, so it is not a
benchmark.

## Compiler findings

No new findings.
