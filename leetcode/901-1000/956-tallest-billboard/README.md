# 956. Tallest Billboard

You are installing a billboard and want it to have the largest height.
The billboard will have two steel supports, one on each side. Each steel
support must be an equal height. You are given a collection of `rods`
that can be welded together. For example, if you have rods of lengths
`1`, `2`, and `3`, you can weld them together to make a support of
length `6`. Return *the largest possible height of your billboard
installation*. If you cannot support the billboard, return `0`.

```
rods = [1,2,3,6]          ->  6
rods = [1,2,3,4,5,6]      ->  10
rods = [1,2]              ->  0
```

**Constraints:** `1 <= rods.length <= 20`; `1 <= rods[i] <= 1000`;
`sum(rods[i]) <= 5000`.

## Approaches

| file | mechanism |
|---|---|
| `tallest_billboard.kara` ★ | the shorter side by difference: each rod goes on the left support, the right one or nowhere. For every difference d between the two sides, the tallest shorter side any choice so far reaches; a rod either widens the difference on the taller side or goes on the shorter side, which grows by the smaller of the rod and d. Each rod reads a copy of the table as it stood before it. The answer is the shorter side at difference 0. O(n s) for n rods adding up to s |
| `tallest_billboard_map.kara` | the same choice per rod with only the reachable differences kept, in a `Map` from difference to tallest shorter side, each rod extending a copy of the map. O(n s) |
| `tallest_billboard_halves.kara` | meet in the middle: every placement of each half's rods tried by recursion, keeping for each signed difference, left minus right, the tallest left side; two placements make equal supports when their differences cancel, and the billboard is the sum of their left sides. O(3^(n/2)) |
| `tallest_billboard_table.kara` | a full table, a row per prefix of the rods: entry d of row i is the tallest shorter side the first i rods reach with the sides d apart, and row i + 1 takes each entry with the next rod left out, on the taller side, or on the shorter one. O(n s) time and space |
| `tallest_billboard_memo.kara` | a memoised search: from rod i with the left side d ahead of the right, the most the left side can still grow and end level, with rod i left out, on the left or on the right; each pair of rod and difference is worked out once, in a `Map`. O(n s) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 16 lines: LeetCode's three examples and six
more (one rod, two equal rods, four rods of 1, five rods split 11 and
11, one rod longer than the rest together, and powers of 2, which never
balance); for 300 random cases of 1 to 10 rods from 1 to 20, 1,682 rods
in all, the total of the heights and a checksum; and six cases of
LeetCode's largest size, 20 rods: random up to 250 (1,181), random odd
rods up to 249 (1,403), 20 rods of 250 (2,500), the rods 1 to 20 (105),
the powers of 2 from 1 to 2,048 (0), and one rod of 4,981 with 19 of 1
(9). `tallest_billboard.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every way to give each rod to the left support, the right one
or neither, 3^n of them, and the tallest pair of equal supports. It
checks 3,200 random cases: 3,000 of 1 to 6 rods from 1 to 10 against the
statement, and 200 of 1 to 8 rods from 1 to 120 against the other
properties, 11,528 rods in all, so that every property stays within
LeetCode's 20 rods adding to at most 5,000.

| | property |
|---|---|
| P1 | the statement's answer, on the small cases |
| P2 | the rods in another order give the same answer |
| P3 | every rod times k, k from 2 to 4 (2 when the total would pass 5,000), gives k times the answer |
| P4 | a rod longer than all the others together, put in anywhere, can never be matched, and gives the same answer |
| P5 | every rod twice gives the sum of the rods: each rod against its copy uses them all |
| P6 | each arm agrees with at least two of the other four |

It prints `3200 cases of 11528 rods: heights adding to 30510, checksum
924810581, 95000 checks over 5 arms: 0 failures` under `karac __mir-run`
(29 s) and `karac __mir-llvm-run`, and the same under
`karac __mir-llvm-asan` with no error. The cases were made smaller, from up
to 7 small rods and up to 10 large rods from 1 to 240, to bring the
interpreter run from 63 s to about 30 s.

## Mutation testing

Thirty-two edits to the differential, each run under
`karac __mir-llvm-run`; fifteen are kept, three to each arm, and all
fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a rod never on the taller side | P1 729, P2 796, P5 1684, P6 783 |
| M2 | ★: the shorter side grows by the whole rod | P1 1696, P2 920, P5 3200, P6 1777 |
| M3 | ★: the shorter side grows by the larger of the rod and the difference | P1 1696, P2 1158, P5 3200, P6 1777 |
| M4 | map: the answer read at difference 1 | P1 1811, P3 1924, P4 684, P5 3200, P6 1917 |
| M5 | map: a rod on the taller side adds itself to the shorter side | P1 1696, P2 729, P5 3200, P6 1777 |
| M6 | map: a rod on the taller side widens the difference by twice its length | P1 1252, P2 1143, P4 1307, P5 2327, P6 1326 |
| M7 | halves: a rod never on the right | P1 1696, P5 3200, P6 1777 |
| M8 | halves: the differences matched without negating | P1 1582, P2 1140, P4 594, P5 3200, P6 1657 |
| M9 | halves: the first left side kept for each difference, not the tallest | P1 376, P2 546, P4 320, P6 387 |
| M10 | table: a rod never left out | P1 2402, P3 2591, P4 609, P6 2591 |
| M11 | table: the new difference taken as the rod when the rod is the shorter | P1 865, P2 1068, P4 623, P5 1742, P6 931 |
| M12 | table: the answer read from the row before the last | P1 1252, P2 857, P4 225, P5 3200, P6 1309 |
| M13 | memo: the end accepts any difference | P1 3000, P4 3200, P5 3200, P6 3200 |
| M14 | memo: the key leaves out the rod | P1 1039, P2 954, P4 255, P5 2677, P6 1093 |
| M15 | memo: the key leaves out the difference | P1 2426, P2 1745, P4 3200, P5 2677, P6 2610 |

P1 and P6 kill all fifteen, P5 thirteen (all but M9 and M10), P2 eleven
(all but M4, M7, M10 and M13), P4 ten (M4, M6, M8 to M15) and P3 two
(M4, M10).

Seventeen other edits were tried and set aside. Seven failed exactly the
same checks as a kept one: map and table never putting a rod on the
taller side, as M1; map growing the shorter side by the whole rod, as
M2; table growing it by the larger of the rod and the difference, as M3; and ★ never putting a rod
on the shorter side and memo never putting one on the left or counting
the right side, as M7. Eight were sound but beyond three an arm: ★ not
taking the difference's absolute value and keeping the last height for a
difference rather than the tallest, map keeping the last entry, halves
adding only the left side of the first half, letting the second half
overlap the first and never leaving a rod out, table growing the
shorter side by the difference in both cases, and memo scoring an
impossible end as -1. The move checker refused one, as it should: ★
updating the table in place with `let prev = best;`, which moves `best`
and then uses it. And one crashed with a stack overflow: halves ending
the first half one rod early, which for a single rod puts that end at
-1, where the recursion never stops.

## Verification

Every arm prints the same output as `tallest_billboard.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `46c2e7477d`, the runtime
archives rebuilt at the same commit. Under `karac __mir-run` ★ and table
take 0.3 s, map 0.5 s, memo 1.0 s and halves 1.4 s, and the
differential 29 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The legacy compiler was removed from kara at M3, so there is no legacy
lane.

## Benchmarks

The bench program builds 200 sets of 20 random rods from 1 to 250 once.
In each of 30 rounds it runs the ★ arm on every set, each round starting
from a different one, and folds the heights into a checksum. Every
implementation prints `30 rounds over 200 sets of 20 rods up to 250:
heights adding to 7517130, checksum 274355334`. Each call allocates the
table of differences and copies it once per rod: `clone` in Kāra and
Rust, `copy` into a second slice in Go, `list` in Python, and `memcpy`
into a second array in C.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.44 to 0.56 s | 0.47 s |
| Rust (`rustc -O`) | 0.74 to 0.88 s | 0.81 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.85 to 0.93 s | 0.88 s |
| Go | 0.64 to 0.77 s | 0.68 s |
| Python | 29.7 s | |
| Kāra (`karac build --mir`) | 0.66 to 0.74 s | 0.69 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Python's run is about 64 times
C's.

v2 takes 0.78 times Rust's median time under overflow checks and 1.48
times C's. Under valgrind's cachegrind v2 runs 8.79 billion
instructions and 4.39 billion branches with 28.0 million mispredicted,
Rust with overflow checks 9.57 billion, 4.82 billion and 28.6 million,
and C 6.27 billion, 3.49 billion and 25.0 million.
