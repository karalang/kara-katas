# 727. Minimum Window Subsequence

Given strings `s1` and `s2`, return the shortest contiguous substring of
`s1` of which `s2` is a subsequence. If there is no such window, return
the empty string, and if several windows are equally short, return the
one that starts furthest left.

```
s1 = "abcdebdde", s2 = "bde"                           ->  "bcde"
s1 = "jmeqksfrsdcmsiwvaovztaqenprpvnbstl", s2 = "u"   ->  ""
```

In the first, "bdde" is as short but starts later, and "deb" is no
window since the letters must come in order.

**Constraints:** 1 <= `s1.length` <= 2 * 10^4; 1 <= `s2.length` <=
100; both are lowercase English letters.

## Approaches

The shortest window ending at a given place starts at the latest place
from which s2 can still be matched up to there, so every arm looks for
windows by their ends or by their starts and keeps the shortest,
comparing strictly so that the first of equal windows stays.

| file | mechanism |
|---|---|
| `minimum_window_subsequence.kara` ★ | forward, then back: walk s1 matching s2 in order until its last letter is matched, then walk back from there matching s2 from its last letter to find the latest start for that end; keep the window if shorter and begin again one place after its start; O(n * m) time, O(1) space |
| `minimum_window_subsequence_dp.kara` | for every prefix of s2, the latest place in s1 from which it can be matched up to here, -1 if none, updated at each letter of s1 from the longest prefix down; O(n * m) time, O(m) space |
| `minimum_window_subsequence_table.kara` | a table of the first place at or after each place of each letter, filled from the right; from every place holding s2's first letter, jumps through the table to each next letter of s2; O(26 n + n * m) time, O(26 n) space |
| `minimum_window_subsequence_bisect.kara` | each letter's places in s1, in order; from every place holding s2's first letter, a binary search finds each next letter of s2 after the current one; O(n * m * log n) time, O(n) space |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 14 lines: the two LeetCode examples; s2 equal
to s1, and longer than it; two equal windows, of which the first is
kept; four more short pairs, among them a window at the very end;
20,000 random letters, the problem's longest, searched for 100 random
letters, the most; 20,000 and 100 drawn from three letters; 20,000 a's
searched for 100; ab 10,000 times then c, searched for ab 50 times then
c, whose only window is at the end; each of the last four with the
window's length and where it starts; and 300 random pairs with how many
have a window and a checksum. `minimum_window_subsequence.py` mirrors
the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
which tries every window of s1, shortest first and leftmost first among
those, and returns the first of which s2 is a subsequence. 3,000 random
pairs are checked, s1 of 1 to 14 letters and s2 of 1 to 4, both drawn
from the same 1 to 3 letters, so windows, equal windows and no window
are all common; 804 have none.

| | property |
|---|---|
| P1 | the window is the definition's |
| P2 | the window is a piece of s1 of which s2 is a subsequence, and is empty only when s2 is not a subsequence of s1 |
| P3 | both strings reversed give a window of the same length |
| P4 | a window searched for s2 again gives itself back |

It prints `3000 pairs (804 with no window), 4 arms, 44784 checks,
0 failures` under `karac __mir-run` and `karac __mir-llvm-run`, and the
same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed. Three more edits, E1 to
E3, change nothing that can be seen, and the differential rightly
reports no failure for them.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: of windows as short, the last kept | P1 14 |
| M2 | ★: the next search begun after the window's end, not its start | P1 79, P3 126 |
| M3 | ★: the walk back begun from s2's second last letter | P1 1664, P2 1664, P3 117, P4 944 |
| M4 | dp: of windows as short, the last kept | P1 14 |
| M5 | dp: the whole of s2 never given a start from a shorter prefix | P1 1476, P2 1476 |
| M6 | dp: the first letter's start set first, so one letter of s1 counts twice | P1 1191, P2 1191, P3 311 |
| M7 | table: each place knowing only its own letter | P1 533, P2 533, P3 251 |
| M8 | table: a letter of s1 used again for the next letter of s2 | P1 1634, P2 1634, P3 327, P4 1634 |
| M9 | table: of windows as short, the last kept | P1 14 |
| M10 | bisect: a letter of s1 used again for the next letter of s2 | P1 1450, P2 1450 |
| M11 | bisect: every letter searched for after the start, not the letter before | P1 1086, P2 1086, P3 181, P4 320 |
| M12 | bisect: windows started at s2's last letter | P1 524, P2 407, P3 413 |
| E1 | ★: the length test as end - start < best_len - 1 | 0 |
| E2 | table: a start that cannot finish skipped rather than ending the search | 0 |
| E3 | dp: a start tested as != -1 | 0 |

P1 kills all twelve, and three of them only P1 sees. M1, M4 and M9 keep
the last of the shortest windows rather than the first, and fail only
14 pairs each: two windows of the same length usually read the same
letters here, so most ties change nothing that can be seen, and only
pairs whose shortest windows differ show it. P2 misses those three and
M2, whose windows hold s2 but are not the shortest, since starting the
next search after a window's end skips the windows that overlap it;
P3 sees M2, since the reversed strings skip different windows. P3 misses
M1, M4, M5, M9 and M10. M5 never gives the whole of s2 a start when it
has more than one letter, and so finds no window, which the reversed
strings do not find either, and P4 checks only a window that was found,
which is why the check counts differ from edit to edit. P4 sees only
M3, M8 and M11. E1 writes the ★ length test as end - start < best_len -
1; E2 skips a start that cannot finish instead of ending the search,
which finds the same window since no later start can finish either;
E3 tests a start as != -1 rather than >= 0.

## Verification

Every arm prints the same output as `minimum_window_subsequence.py`
under `karac __mir-run` (the v2 MIR interpreter) and `karac
__mir-llvm-run`, and under `karac __mir-llvm-asan` (AddressSanitizer)
with no error; the differential prints its line under all three. `karac
check` passes all four arms, the differential and the bench program. The
debug build that runs `__mir-llvm-run`, `__mir-llvm-asan` and `build
--mir` and the release build that runs `check` and `__mir-run` are both
at kara `a4b0967495`, whose last compiler change is `d2fb23c673`. The
runtime archives were built after the last runtime change, `3c8e763161`.

Since kara `3c8e763161` (B-2026-10-18-31) the sanitizer lane sees leaks
itself. The leak check also copied each arm's and the differential's
lane executable as it was linked and ran it with the preloaded shim from
kata 708, which refuses the lane's hand-made stack so that LeakSanitizer
sees `main`: all five print their output and report no leak.

The frozen legacy backends refuse all four arms, the differential and
the bench program at type checking: in the harness at `*c` over a
window's `bytes().iter()`, since legacy gives those by value where
v2 gives references, and in the bisect arm also at `*s` over a letter's
places and at `first_after(places[c], p)`, which legacy reads as moving
a vector out of the vector of places (E_INDEX_MOVE_NON_COPY). It refuses
the bench program at `min_window(texts[d], word)` for the same reason;
v2 borrows bare parameters. Legacy is frozen, so this is noted, not
filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. It makes
10 random texts of 20,000 letters from a to h once, and in each of
300 rounds searches every text for a fresh random word of 20 letters
from the same eight, summing the windows' lengths. The C program copies
the window out, as the Kāra program's slice does. Every implementation
prints `300 rounds of 10 texts of 20000 letters: sum 203518`, the Kāra
program under `karac __mir-run` included (in 3.0 minutes).

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and two of Python (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.69 to 0.73 s |
| Rust (`rustc -O`) | 0.67 to 0.76 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.72 to 0.77 s |
| Go | 0.51 to 0.68 s |
| Python | 15.5 to 15.8 s |
| Kāra (`karac build --mir`) | 0.70 to 0.81 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend; the legacy `karac build` refuses it (above). That
edit is by hand, on top of the `scripts/new-bench.sh` output. Under
`karac __mir-llvm-run` the program prints the same line in 3.1 s,
compile included; that JITs the MIR's IR without optimization passes, so
it is not a benchmark.

So the v2 build is close to C and Rust here, about a tenth behind them
at the medians of the interleaved runs (0.78 s against 0.72 for both,
and 0.73 for Rust under overflow checks), and a quarter behind Go
(0.62). Under valgrind's cachegrind it runs 4.3 billion instructions
against Rust's 3.1 and C's 3.0, and 1.4 billion branches against 0.9 and
0.5. Rust and Kāra mispredict the same 26 million times, the letter
comparisons on random text, where C mispredicts 2.2 million, likely
because clang turned some of those comparisons into branch-free code;
where Kāra's extra instructions come from was not traced. The comparison
with C and Rust waits until after M4.

## Compiler findings

None new.
