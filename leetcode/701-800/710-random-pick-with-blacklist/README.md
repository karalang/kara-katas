# 710. Random Pick with Blacklist

You are given an integer `n` and an array of unique integers
`blacklist`. Design an algorithm to pick a random integer in the range
`[0, n - 1]` that is not in `blacklist`. Any integer that is in the
mentioned range and not in `blacklist` should be equally likely to be
returned. Optimize your algorithm such that it minimizes the number of
calls to the built-in random function of your language.

Implement the `Solution` class: `Solution(int n, int[] blacklist)`
initializes the object with the integer `n` and the blacklisted integers
`blacklist`; `int pick()` returns a random integer in the range `[0, n -
1]` and not in `blacklist`.

```
Solution(7, [2, 3, 5]), then pick() seven times  ->  0, 4, 1, 6, 1, 0, 4
(any of 0, 1, 4 and 6, each equally likely)
```

**Constraints:** 1 <= `n` <= 10^9; 0 <= `blacklist.length` <=
min(10^5, `n` - 1); 0 <= `blacklist[i]` < `n`; all the values of
`blacklist` are unique; at most 2 * 10^4 calls are made to `pick`.

## Approaches

Of the `n` numbers, bound = `n` - `blacklist.length` are allowed. Every
arm makes one draw r from 0 to bound - 1 per pick and maps it to an
allowed number, a mapping that takes each draw to a different allowed
number, so each is equally likely. Kāra has no random function in its
standard library, so the draw comes from a seeded generator the harness
defines, `random_below`, two steps of a linear congruential generator
making 30 bits; `Solution.new` takes the seed as a third argument. Each
arm also has `fn pick_from(ref self, r: i64) -> i64`, the allowed number
a draw of r stands for, which `pick` calls and the harness and
differential test directly.

| file | mechanism |
|---|---|
| `random_pick_with_blacklist.kara` ★ | the usual answer: an allowed draw is its own answer, and each blacklisted number below bound is remapped, in a `Map`, to an allowed number at or above bound, handed out from the top down; O(1) per pick, O(B) to build |
| `random_pick_with_blacklist_rank.kara` | the r-th allowed number in order: sort the blacklist; the blacklisted number at index i has black[i] - i allowed numbers below it, so a binary search for the first index with more than r gives r plus that index; O(log B) per pick |
| `random_pick_with_blacklist_intervals.kara` | the runs of allowed numbers between the blacklisted ones, each with its first number and how many allowed numbers come before it; a binary search finds the run a draw falls in; O(log B) per pick |
| `random_pick_with_blacklist_remap_vec.kara` | the ★ arm's remap without a hash map: the blacklisted numbers below bound and the allowed numbers at or above bound, both in order, paired in two sorted `Vec`s and looked up by binary search; O(log B) per pick |
| `differential.kara` | the four arms against the definition, four properties |

The remap arms and the rank arms map the same draw to different allowed
numbers, and the problem asks only that each be equally likely, so the
harness prints nothing that depends on which: whether every draw, taken
once, gives every allowed number exactly once; how many picks were not
allowed; and how many different numbers the picks came to and how often,
as a checksum of the counts sorted. The draws are the same in every arm
and the mappings differ only by a reordering of the allowed numbers, so
the sorted counts are the same in all four. Where `n` is too large to
take every draw, it takes each blacklisted number below bound and the
last 1,000 draws instead.

Every arm prints the same 14 lines: the LeetCode example, with its
7 picks and again with 10,000; one number; two numbers with either
blacklisted; ten numbers with none, with all but one and with the top or
the bottom half blacklisted; 10^9 numbers with the two ends blacklisted,
and with 100,000 random numbers blacklisted, the problem's most;
200,000 numbers with half blacklisted; 300,000 numbers with all but
10 blacklisted; and 300 random small cases folded into one checksum.
`random_pick_with_blacklist.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
which tests each number from 0 to `n` - 1 against every blacklisted
number and keeps those on none of them. 3,000 cases are checked, `n` up
to 40 or, one case in four, up to 200, with a blacklist of a random size
that is drawn at random or is a run at the bottom, the top or the
middle, in either order.

| | property |
|---|---|
| P1 | every draw, taken once, gives every allowed number once: `pick_from` over 0 to bound - 1, sorted, is the definition's list |
| P2 | 20 picks from a seed are what the draws from that seed stand for under `pick_from` |
| P3 | the arm's own rule: for the remap arms an allowed draw is its own answer, and for the rank arms draw r gives the definition's r-th number |
| P4 | P1 holds with the blacklist in reverse order |

It prints `3000 cases (60093 draws), 4 arms, 48000 checks, 0 failures`
under `karac __mir-run` and `karac __mir-llvm-run`, and the same under
`karac __mir-llvm-asan` with no error.

## Mutation testing

Thirteen edits to the differential, three or four to each arm, each run
under `karac __mir-run`. All thirteen are killed. Four more edits, E1 to
E4, change nothing that can be seen, and the differential rightly
reports no failure for them.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a blacklisted bound remapped too | P1 655, P4 664 |
| M2 | ★: the same target handed out twice | P1 1703, P4 1703 |
| M3 | ★: only one blacklisted target skipped in a row | P1 426, P4 426 |
| M4 | rank: a count equal to r taken as above it | P1 2039, P3 2039, P4 2039 |
| M5 | rank: the blacklisted number itself, not the count below it | P1 1907, P3 1907, P4 1907 |
| M6 | intervals: one too few counted in each gap | P1 1292, P3 1292, P4 1292 |
| M7 | intervals: the next run starting on the blacklisted number | P1 2039, P3 2039, P4 2039 |
| M8 | intervals: a run with exactly r before it passed over | P1 1292, P3 1292, P4 1292 |
| M9 | remap-vec: the blacklisted bound paired too | P1 1140, P4 1140 |
| M10 | remap-vec: only one blacklisted target skipped in a row | P1 1164, P4 1164 |
| M11 | remap-vec: the same target handed out twice | P1 1703, P4 1703 |
| M12 | ★: `pick` drawing from one past bound | P2 2977 |
| M13 | rank: `pick` reading its draw from the top down | P2 2733 |
| E1 | intervals: an empty run kept before a blacklisted number | 0 |
| E2 | remap-vec: the match tested as at most r, not equal | 0 |
| E3 | rank: the midpoint as lo + (hi - lo) / 2 | 0 |
| E4 | ★: a blacklisted bound left out of the numbers skipped | 0 |

P1 kills the eleven that break the mapping, and P4 kills the same eleven
from the reversed blacklist, which for the ★ arm is a different remap,
so M1's counts differ there. P3 adds the rank arms' five: a rank arm
that is off by one is wrong at almost every draw, while a remap arm's
mistakes fall only on the blacklisted draws, which P3 does not pin. Only
P2 sees M12 and M13, which leave `pick_from` alone and change the draw
`pick` makes: M13 still reaches every allowed number once over all
draws, so nothing but replaying the draws can tell. E1 keeps an empty
run before a blacklisted number that follows another, which the search
for the last run with at most r before it always passes over; E2 tests
the match found by the search as at most r, which the search already
makes the same as equal to r; E3 is the same midpoint; and E4 leaves a
blacklisted bound out of the numbers the ★ arm skips, which it never
reaches, since the walk down stops at the lowest allowed number at or
above bound that it needs.

## Verification

Every arm prints the same output as `random_pick_with_blacklist.py`
under `karac __mir-run` (the v2 MIR interpreter) and `karac
__mir-llvm-run`, and under `karac __mir-llvm-asan` (AddressSanitizer)
with no error; the differential prints its line under all three. `karac
check` passes all four arms, the differential and the bench program. The
debug build that runs `__mir-llvm-run`, `__mir-llvm-asan` and `build
--mir` is at kara `6dc5c61842`; the release build that runs `check` and
`__mir-run` is built from the tree at `6f256df19a`, and the one compiler
commit between them, `24740acba2`, changes only how the sanitizer lane
builds its object. No `runtime/src` change has landed since the runtime
archives were built.

The sanitizer lane cannot see a leak (kara B-2026-10-18-31), so the leak
check ran each arm's and the differential's lane executable with the
preloaded shim from kata 708, which refuses the lane's hand-made stack
so that LeakSanitizer sees `main` (kata 708 showed it reporting a leak
the lane misses): all five print their output and report no leak.

The frozen legacy backends refuse all four arms and the differential at
type checking, at `*b` and the like over `iter()`, since legacy gives
those items by value where v2 gives references, and at `next_random(mut
seed)` inside `random_below`, whose `seed` is already a `mut ref`, where
legacy wants the marker dropped and design.md § Call-site `mut` markers
now requires it (kara B-2026-10-14-25). They refuse the bench program at
that same marker. Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the rank arm, which needs no hash map and so is
the same algorithm in all five languages; the ★ arm's `Map` has no
counterpart in C. It makes 100,000 different numbers below 10^9 once,
one in each block of 10,000, and shuffles them. Each of five rounds
builds a picker, sorting its own copy of the blacklist, and makes
1,000,000 picks, each a draw and a binary search of 17 steps, all
summed. Every implementation prints `5 rounds of 1000000 picks,
100000 of 1000000000 blacklisted: sum 2340652259270874`, the Kāra
program under `karac __mir-run` included (in 33 s).

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and two of Python (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.58 to 0.74 s |
| Rust (`rustc -O`) | 0.56 to 0.63 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.58 to 0.71 s |
| Go | 0.62 to 0.78 s |
| Python | 11.2 s |
| Kāra (`karac build --mir`) | 0.55 to 0.69 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend; the legacy `karac build` refuses it (above). That
edit is by hand, on top of the `scripts/new-bench.sh` output. Under
`karac __mir-llvm-run` the program prints the same line in 2.6 s,
compile included; that JITs the MIR's IR without optimization passes, so
it is not a benchmark.

So the v2 build is level with C, Rust and Go, inside the spread of the
runs. Under valgrind's cachegrind it runs more instructions than C or
Rust (1.76 billion, against 1.52 and 1.40) and more branches
(442 million, against 233 and 278), but mispredicts fewer of them
(44 million, against 51 and 47), and all three take about 28 million
first-level data-cache misses, five or six a pick. The time is the
binary search's unpredictable branches and its reads across a 800 KB
array, which every implementation pays alike. The comparison with C and
Rust waits until after M4.

## Compiler findings

None new.
