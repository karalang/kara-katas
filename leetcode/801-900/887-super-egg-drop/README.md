# 887. Super Egg Drop

You are given `k` identical eggs and you have access to a building with
`n` floors labeled from `1` to `n`. You know that there exists a floor
`f` where `0 <= f <= n` such that any egg dropped at a floor higher than
`f` will break, and any egg dropped at or below floor `f` will not
break. Each move, you may take an unbroken egg and drop it from any
floor `x` (where `1 <= x <= n`). If the egg breaks, you can no longer
use it. However, if the egg does not break, you may reuse it in future
moves. Return the minimum number of moves that you need to determine
with certainty what the value of `f` is.

```
k = 1, n = 2  ->  2
k = 2, n = 6  ->  3
k = 3, n = 14  ->  4
```

**Constraints:** `1 <= k <= 100`, `1 <= n <= 10^4`.

## Approaches

| file | mechanism |
|---|---|
| `super_egg_drop.kara` ★ | the floors a number of moves can cover: with m moves and k eggs the first drop splits the floors into those m - 1 moves and k - 1 eggs settle below it and those m - 1 moves and k eggs settle above, so floors(m, k) = floors(m - 1, k - 1) + floors(m - 1, k) + 1; one row of k entries a move, until the row reaches n. O(k * answer) |
| `super_egg_drop_search.kara` | the game's recursion, moves(e, f) = 1 + the least over first floors x of the worse of moves(e - 1, x - 1) and moves(e, f - x), as a table over eggs and floors; the first term rises with x and the second falls, so the best x is where they cross, found by binary search, with the floor below it tried too. O(k * n log n) |
| `super_egg_drop_pointer.kara` | the same table, but the best first floor never moves down as f grows, so for each number of eggs one pointer walks up the floors once, stepping while the next floor does at least as well. O(k * n) |
| `super_egg_drop_binomial.kara` | the floors as a sum of binomials: floors(m, k) = C(m, 1) + ... + C(m, k), one term for each number of eggs that may break; m = 1, 2, ... is tried, each binomial built from the one before, the sum stopping once it reaches n so that nothing overflows. O(k * answer) |
| `super_egg_drop_bisect.kara` | a binary search on the moves between 1 and n, each probe building the ★ arm's table for m moves, capped at n. O(k * n log n) at worst |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 13 lines: LeetCode's three examples and eight
more (one egg and one floor; one egg, two eggs, three eggs, 14 eggs and
100 eggs for 10^4 floors; and 13 eggs for 8,191 and 8,192 floors, where
a binary search's 13 moves stop being enough); the moves for 3,000 cases
of up to 5 eggs and 80 floors, 39,754 in all; and for 20 cases of up to
12 eggs and 10^4 floors, 3,534 in all, with a checksum.
`super_egg_drop.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the game played out for every number of eggs and floors in
doubt, a drop from each floor in turn, the egg breaking or not, the
worse of the two outcomes counted and the best drop taken, with one egg
climbing a floor at a time. It checks 3,040 cases: 3,000 of up to 4 eggs
and 40 floors against the statement, and 40 of up to 12 eggs and 2,000
floors against the other properties. The ★ arm's answers sum to 31,108.

| | property |
|---|---|
| P1 | the statement's answer, on up to 4 eggs and 40 floors |
| P2 | no fewer moves than a binary search needs, no more than one a floor, and one a floor with one egg |
| P3 | one more egg never needs more moves, and one more floor never fewer |
| P4 | two eggs need the least m with m (m + 1) / 2 >= n, and eggs enough for a binary search need its moves |
| P5 | with two eggs or more, a first drop from the floor just above all that one egg fewer settles in one move less leaves both outcomes settled in one move less |
| P6 | each arm agrees with at least two of the other four |

P2 to P6 are checked on every case. It prints `3040 cases, 31108 moves
in all, 87145 checks over 5 arms: 0 failures` under `karac __mir-run`
and `karac __mir-llvm-run`, and the same under `karac __mir-llvm-asan`
with no error.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-llvm-run`. All fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a drop counted as telling two floors apart | P1 2828, P2 2339, P4 996, P5 962, P6 2867 |
| M2 | ★: the eggs updated from one up, reading this move's row | P1 2070, P2 1620, P4 988, P5 1061, P6 2107 |
| M3 | ★: at most two eggs used | P1 1160, P4 139, P5 549, P6 1189 |
| M4 | search: the drop itself not counted | P1 2232, P2 2269, P4 1150, P5 2269, P6 2269 |
| M5 | search: one egg fewer used | P1 1374, P4 706, P5 1382, P6 1392 |
| M6 | search: one egg taking a move more than the floors | P1 2526, P2 817, P4 920, P5 2163, P6 2547 |
| M7 | pointer: one egg taking a move more than the floors | P1 2526, P2 817, P4 920, P5 2163, P6 2547 |
| M8 | pointer: the better outcome counted, not the worse | P1 2070, P2 1620, P3 167, P4 988, P5 973, P6 2107 |
| M9 | pointer: the broken-egg outcome read one floor too high | P1 2232, P2 256, P3 1418, P4 1150, P5 764, P6 2269 |
| M10 | binomial: one egg more counted | P1 1400, P2 743, P4 538, P5 457, P6 1419 |
| M11 | binomial: each binomial built one row down | P1 3000, P2 872, P4 1169, P5 2104, P6 3040 |
| M12 | binomial: the count starting at two moves | P1 71, P2 71, P4 71, P5 105, P6 71 |
| M13 | bisect: the search ending one move short of n | P1 798, P2 801, P4 49, P5 49, P6 801 |
| M14 | bisect: the floors capped one below n | P1 2131, P4 1049, P6 2168 |
| M15 | bisect: each probe one move short | P1 2131, P4 1049, P5 1386, P6 2168 |

P1 and P6 kill all fifteen. M6 and M7 are one fault in two arms, the
one-egg row of the table starting a move too high, and fail the same
cases. M14 and M15 fail as many cases under P1, P4 and P6, though only M15
also breaks P5. P3 is
the weakest property here, killing only M8 and M9: an arm wrong by the
same amount everywhere still grows the right way with more eggs and
more floors. Two pointer mutants survived and were replaced: stepping
only to a strictly better floor, and judging the next floor by the
floors above this one rather than above the next. A Python model of
each agrees with the ★ arm on every case of up to 8 eggs and 3,000
floors, so both are most likely equivalent (not proved; the reason is
inferred: a pointer that stops at a tie, or compares one floor further
on, still lands on a floor as good as the best, since the worse outcome
first falls and then rises as the first floor goes up).

## Verification

Every arm prints the same output as `super_egg_drop.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build and the runtime archives are both at
kara `fe44986b7e`. Under `karac __mir-run` the arms take 0.2 to 9.3 s
each (the search arm, a binary search for every number of eggs and
floors, the slowest) and the differential 9 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The frozen legacy backends' interpreter, JIT and `karac build
--legacy`, with and without auto-par, print the same output for all five
arms. For the differential the legacy interpreter prints the same line,
and the JIT and `karac build --legacy` refuse it: "chained indexed
receivers (`a[i][j].max(...)`) are deferred to v1.x", for the statement
read literally's `table[e - 1][x - 1].max(row[f - x])`. Legacy is
frozen, so this is not filed.

## Benchmarks

The bench program uses the ★ arm, in all five languages: 30,000 cases
of 2 to 9 eggs and up to 10^9 floors, far past LeetCode's 10^4 so that
each case takes thousands of moves; most of the time goes to the cases
with two eggs, which need up to about 44,700. The table is a `Vec` in
Kāra and Rust, a slice in Go, an array from `calloc` in C and a list in
Python. Every implementation prints `30000
cases of 2 to 9 eggs and up to 10^9 floors: 114125578 moves, checksum
588377993`.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.30 to 0.32 s | 0.32 s |
| Rust (`rustc -O`) | 0.32 to 0.39 s | 0.33 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.36 to 0.45 s | 0.39 s |
| Go | 0.31 to 0.35 s | 0.33 s |
| Python | 22.4 s | |
| Kāra (`karac build --mir`) | 0.31 to 0.36 s | 0.33 s |
| Kāra legacy (`karac build --legacy`) | 0.30 to 0.34 s | 0.31 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 886's does.

v2 takes 0.84 times Rust's median time under overflow checks, 1.06
times legacy's and 1.02 times C's. Under valgrind's cachegrind C runs
2.37 billion instructions, Rust with overflow checks 4.94 billion,
legacy 3.95 billion and v2 3.46 billion, yet all five compiled programs
take about the same time. Each move's update runs down a chain, every
entry the sum of two others, so the time is most likely set by that
chain of additions and loads rather than by the instruction count
(inferred from the counts and timings, not profiled). The comparison
with C and Rust waits until after M4.
