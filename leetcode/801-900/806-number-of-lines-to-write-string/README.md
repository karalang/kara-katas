# 806. Number of Lines To Write String

Given a string `s` of lowercase letters and an array `widths` of 26
numbers, where `widths[0]` is how many pixels wide `a` is, `widths[1]`
`b`, and so on, write `s` across lines of at most 100 pixels each: put
as many letters as fit on the first line, then go on with the next line,
and so on. Return `[lines, width]`, the number of lines and the width of
the last line in pixels.

```
widths = [10, 10, ..., 10], s = "abcdefghijklmnopqrstuvwxyz"          ->  [3, 60]
widths = [4, 10, 10, ..., 10], s = "bbbcccdddaaa"                     ->  [2, 4]
```

**Constraints:** `widths.length == 26`, `2 <= widths[i] <= 10`, `1 <=
s.length <= 1000`, and `s` is lowercase letters.

## Approaches

| file | mechanism |
|---|---|
| `number_of_lines.kara` ★ | write the letters left to right, keeping the width of the line so far; a letter that would take the line past 100 pixels starts a new line instead. O(len) |
| `number_of_lines_lines.kara` | build the lines themselves as strings, each letter added to the last line if it fits and starting a new one if not; then count the lines and add up the widths of the last one's letters |
| `number_of_lines_recurse.kara` | a function that places the letters from `i` on, given the lines used so far and the width of the last, calling itself for the next letter |
| `number_of_lines_fold.kara` | fold the letters' widths into the pair (lines, width of the last line), starting from (1, 0) |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 8 lines: LeetCode's two examples; `"a"`, one
letter; ten letters of 10 pixels, which fill one line exactly, and
eleven, which go on to a second; 50 letters of 2 pixels, which fill one
line exactly; `z` of 9 pixels and `y` of 10 written in turn, where each
line takes five pairs and stops at 95, the next `z` not fitting; and 300
random strings of up to 200 letters, each with widths of its own from 2
to 10, with how many lines they take in all and a checksum.
`number_of_lines.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition:
add up the widths of the letters before each place in the string, and
from the start of each line find, by halving, the last place whose sum
is at most 100 more than the line's start; the next line starts there.
Its 1,600 cases come in four kinds of 400: widths from 2 to 10 and up to
100 letters; every width 10, so that lines fill exactly; widths of 4, 5
and 10, which often add up to 100; and widths of 9 and 10 with up to 300
letters.

| | property |
|---|---|
| P1 | the definition's answer |
| P2 | the last line holds 1 to 100 pixels, and the lines hold at least the total, at most 100 each; every line but the last holds more than 90, since the next letter, at most 10, did not fit |
| P3 | one more letter goes on the last line if it fits, and starts a new line with its width if not |
| P4 | the alphabet turned round, `a` for `z` and `z` for `a`, with the widths turned round with it, gives the same answer |

It prints `1600 cases (11268 lines), 4 arms, 25600 checks, 0 failures`
under `karac __mir-run` and `karac __mir-llvm-run`, and the same under
`karac __mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a letter that makes the line exactly 100 put on a new line | P1 665, P2 366, P3 61 |
| M2 | ★: a new line started empty, without the letter's width | P1 1412, P2 559, P3 123 |
| M3 | ★: each letter read as the one after it | P1 1083, P2 289, P3 812, P4 1083 |
| M4 | lines: a new line started with the letter's width counted twice | P1 1244, P2 598, P3 130 |
| M5 | lines: the first line's width given, not the last's | P1 1354, P2 829, P3 1427 |
| M6 | lines: the last line's width taken from its last letter alone | P1 1473, P3 1600 |
| M7 | recurse: the last letter never written | P1 1600, P2 70, P3 768 |
| M8 | recurse: a new line started empty, without the letter's width | P1 1412, P2 559, P3 123 |
| M9 | recurse: the letters read from the end | P1 909, P3 796 |
| M10 | fold: the first line started one pixel full | P1 619, P2 219 |
| M11 | fold: a new line given the old line's width | P1 1412, P2 1412, P3 1423 |
| M12 | fold: every letter taken as 10 wide when deciding to wrap | P1 584, P3 32 |

P1 kills all twelve. P4 sees only the ★ edit that reads each letter as
the one after it (M3), the one edit that treats one letter unlike
another: every other edit goes wrong the same way for any letters of the
same widths, and turning the alphabet round with its widths leaves the
widths in the same order. P3 sees every edit but the fold that starts
its first line one pixel full (M10), whose answers stay consistent with
one more letter; P2 sees M10, which can start a second line with only 90
pixels on the first. P2 misses three: the last line's width taken from
its last letter alone (M6), which makes the last width smaller while the
bounds still hold; the letters read from the end (M9), which lays out
the same letters validly in the other order; and the fold that wraps
whenever the line is past 90 (M12), every letter taken as 10 wide, whose
lines all hold more than 90 and at most 100 as P2 asks.

## Verification

Every arm prints the same output as `number_of_lines.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The debug build that
runs `__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` and the
release build that runs `check` and `__mir-run` are both at kara
`b03f2bc51f`, which is its last compiler change. The runtime archives
were built after the last runtime change, `b03f2bc51f`.

Since kara `3c8e763161` (B-2026-10-18-31) the sanitizer lane sees leaks
itself. The leak check also copied each arm's and the differential's
lane executable as it was linked and ran it with the preloaded shim from
kata 708, which refuses the lane's hand-made stack so that LeakSanitizer
sees `main`: all five print their output and report no leak.

The frozen legacy interpreter (`karac run --interp`) prints the same
output for all four arms and the differential, unchanged. The legacy JIT
(`karac run`), `karac build` and an auto-par build print the same output
for the ★, lines and recurse arms, with a warning that `s` is used after
a move, and refuse the fold arm and the differential at the fold arm's
`s.bytes().iter().map(...).fold(...)`: `codegen: no handler for method
'fold' on non-identifier receiver`. Legacy refuses the bench program at
`number_of_lines(all_widths[r % 64], strings[r % 64])`, a move out of an
index, legacy taking a bare parameter as owned rather than borrowed; a
copy with `ref` parameters and the widths and string bound by `ref`
first builds and prints the same line, and the bench timing below is of
it. Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. 64 strings of
1,000 letters, LeetCode's longest, are made once, each with widths of
its own from 2 to 10. Each of 1,000,000 rounds counts the lines of the
next string. Every implementation prints `1000000 rounds of 1000
letters: 62500000 lines in all, checksum 630237933`, the Kāra program
under `karac __mir-run` included (in 487 s).

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and two of Python (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 1.19 to 1.35 s |
| Rust (`rustc -O`) | 1.10 to 1.24 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.50 to 1.74 s |
| Go | 1.72 to 1.87 s |
| Python | 39.14 to 42.66 s |
| Kāra (`karac build --mir`) | 1.63 to 1.73 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, since the legacy `karac build` refuses it (see
Verification); that edit is by hand, on top of the
`scripts/new-bench.sh` output. Under `karac __mir-llvm-run` the program
prints the same line in 5.6 s, compile included; that JITs the MIR's IR
without optimization passes, so it is not a benchmark.

At the medians of the interleaved runs the v2 build takes 1.66 s,
against C's 1.23, Rust's 1.13 (1.57 under overflow checks) and Go's
1.78. Under valgrind's cachegrind v2 runs 16.3 billion instructions and
5.07 billion branches, against Rust's 15.0 billion and 2.00 billion and
C's 12.0 billion and 1.00 billion. The legacy build of the copy ran 1.85
to 2.08 s, a median of 1.93 s in the interleaved runs, with 15.2 billion
instructions and 6.07 billion branches, so v2 takes 0.86 times legacy.
v2 and legacy each mispredict 62.5 million branches, one for each of the
62,500,000 lines written, where C and Rust mispredict about a million in
all; that reads as their compilers making the test for a new line a
select rather than a branch, which is inferred, not read from the
assembly. The comparison with C and Rust waits until after M4.

## Compiler findings

Nothing new in v2.
