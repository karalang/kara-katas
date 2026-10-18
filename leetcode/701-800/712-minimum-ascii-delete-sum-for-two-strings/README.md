# 712. Minimum ASCII Delete Sum for Two Strings

Given two strings `s1` and `s2`, return the lowest ASCII sum of deleted
characters to make two strings equal.

```
s1 = "sea",    s2 = "eat"   ->  231   (delete "s" and "t": 115 + 116)
s1 = "delete", s2 = "leet"  ->  403   (keep "let")
```

**Constraints:** 1 <= `s1.length`, `s2.length` <= 1000; `s1` and
`s2` consist of lowercase English letters.

## Approaches

Every arm is the same O(m * n) recurrence over prefixes or suffixes: an
empty string costs the whole of the other; equal next bytes cost what
the rest costs; otherwise delete one of the two bytes, whichever leaves
the cheaper total.

| file | mechanism |
|---|---|
| `minimum_ascii_delete_sum_for_two_strings.kara` ★ | the full (m + 1) by (n + 1) table of prefix costs, filled row by row |
| `minimum_ascii_delete_sum_for_two_strings_rolling.kara` | the same table one row at a time, keeping the one diagonal value each cell overwrites; O(n) space |
| `minimum_ascii_delete_sum_for_two_strings_memo.kara` | top-down recursion over suffixes with a memo table of -1 until computed |
| `minimum_ascii_delete_sum_for_two_strings_keep.kara` | the other side of the problem: what is kept is a common subsequence, so the cost is both sums less twice the heaviest common subsequence's, a weighted longest common subsequence one row at a time |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 13 lines: the two LeetCode examples; one equal
and one different letter; a string against the empty string and two
empty strings, beyond the constraints; a string against itself and its
reverse; a run against one of its letters; a swapped pair; two random
strings of the problem's most, 1,000 letters, from the whole alphabet
and from three letters; and 500 random pairs of 0 to 39 letters with a
checksum. `minimum_ascii_delete_sum_for_two_strings.py` mirrors the ★
arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
which uses no table at all: it tries every subsequence of `s1` as what
is kept and, if it is also a subsequence of `s2`, found by a greedy
left-to-right match, costs the two sums less twice its sum; the answer
is the least. 3,000 random pairs are checked, each string 0 to
10 letters from an alphabet of 1 to 5, so equal letters and equal
strings are common.

| | property |
|---|---|
| P1 | the cost is the definition's |
| P2 | swapping the strings costs the same |
| P3 | a string against itself costs 0, and against the empty string its whole sum |
| P4 | the same letter added to the front of both strings, or to the end of both, costs nothing more |

It prints `3000 pairs (84 equal), 4 arms, 48000 checks, 0 failures`
under `karac __mir-run` and `karac __mir-llvm-run`, and the same under
`karac __mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed. Three more edits, E1 to
E3, change nothing that can be seen, and the differential rightly
reports no failure for them.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the first column left at 0 | P1 1977, P2 2867, P3 2740, P4 1170 |
| M2 | ★: equal bytes charged the cell to the left | P1 2279, P2 2058, P3 2740, P4 2900 |
| M3 | ★: the costlier deletion taken | P1 1704, P4 2029 |
| M4 | rolling: the first row counted from the wrong byte | P1 553, P2 1110, P4 553 |
| M5 | rolling: the diagonal not carried along the row | P1 2112, P2 2305, P3 2485, P4 2744 |
| M6 | rolling: deleting from s1 charged s2's byte | P1 1292, P2 1724, P4 726 |
| M7 | memo: s2's rest summed from its start | P1 1141, P2 1889, P3 2740, P4 1740 |
| M8 | memo: equal bytes skipped in s1 only | P1 2292, P2 2058, P3 2740, P4 2901 |
| M9 | memo: deleting from s2 not charged | P1 1549, P2 1809, P4 468 |
| M10 | keep: a match kept without the heaviest before it | P1 1814, P3 2485, P4 2411 |
| M11 | keep: a match not allowed to be skipped from the row above | P1 1195, P2 1607, P4 1257 |
| M12 | keep: what is kept subtracted once, not twice | P1 2411, P3 2740, P4 3000 |
| E1 | ★: a tie broken towards deleting from s2 | 0 |
| E2 | memo: a stored 0 treated as not stored | 0 |
| E3 | keep: a tie between keeping and skipping broken the other way | 0 |

P1 kills all twelve, and P4 does too: a letter added at both ends moves
every cell of the recurrence onto a neighbour, so a mistake anywhere in
it shows. P3 misses five, M3, M4, M6, M9 and M11: a string against
itself takes only matches and a string against the empty string has
nothing to choose, and these five go wrong only off those paths.
P2 misses M3, M10 and M12, whose mistakes are the same with the strings
either way round. E1 and E3 break ties the other way, which gives the
same number; E2 treats a stored cost of 0 as not stored and recomputes
it, which is slower but the same.

## Verification

Every arm prints the same output as
`minimum_ascii_delete_sum_for_two_strings.py` under `karac __mir-run`
(the v2 MIR interpreter) and `karac __mir-llvm-run`, and under `karac
__mir-llvm-asan` (AddressSanitizer) with no error; the differential
prints its line under all three. `karac check` passes all four arms, the
differential and the bench program. The debug build that runs
`__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` is at kara
`6dc5c61842`; the release build that runs `check` and `__mir-run` also
has `500dff0834`, a parser fix for a postfix on a parenthesized
block-like statement, which these programs do not write. No
`runtime/src` change has landed since the runtime archives were built.

The sanitizer lane cannot see a leak (kara B-2026-10-18-31), so the leak
check ran each arm's and the differential's lane executable with the
preloaded shim from kata 708, which refuses the lane's hand-made stack
so that LeakSanitizer sees `main` (kata 708 showed it reporting a leak
the lane misses): all five print their output and report no leak.

The frozen legacy backends refuse all four arms and the differential at
type checking: at `next_random(mut seed)` inside the harness's
`random_string`, and at the memo arm's recursive `cost(a, b, ..., mut
memo)`, whose argument is already a `mut ref`, where legacy wants the
marker dropped and design.md § Call-site `mut` markers now requires it
(kara B-2026-10-14-25), and at `*x` over `iter()` in the keep arm, since
legacy gives those items by value where v2 gives references. They refuse
the bench program at `minimum_delete_sum(words[2 * p], ...)`, an element
passed to a borrowing parameter, which legacy reads as a move out of the
`Vec`. Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages, the table
allocated as rows on each call. It makes 20 random strings of
1,000 lowercase letters once and costs each of their 10 pairs ten times,
summing the costs, 10^8 cells in all. Every implementation prints
`10 rounds of 10 pairs of 1000 letters: sum 14872680`, the Kāra program
under `karac __mir-run` included (in 96 s).

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and two of Python (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.44 to 0.55 s, one run at 0.86 s |
| Rust (`rustc -O`) | 0.54 to 0.63 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.55 to 0.64 s |
| Go | 0.80 to 0.88 s |
| Python | 17.1 to 17.7 s |
| Kāra (`karac build --mir`) | 0.43 to 0.54 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend; the legacy `karac build` refuses it (above). That
edit is by hand, on top of the `scripts/new-bench.sh` output. Under
`karac __mir-llvm-run` the program prints the same line in 2.8 s,
compile included; that JITs the MIR's IR without optimization passes, so
it is not a benchmark.

So the v2 build is level with C and ahead of Rust and Go. It is not
doing less: under valgrind's cachegrind it runs 5.18 billion
instructions, against C's 2.12 and Rust's 3.41, and 1.46 billion
branches against C's 0.99 and Rust's 1.29, all well predicted. It gets
more done per cycle, for reasons not measured. The comparison with C and
Rust waits until after M4.

## Compiler findings

None new.
