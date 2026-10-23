# 904. Fruit Into Baskets

You are visiting a farm that has a single row of fruit trees arranged
from left to right. The trees are represented by an integer array
`fruits` where `fruits[i]` is the type of fruit the `i`th tree produces.

You want to collect as much fruit as possible. However, the owner has
some strict rules that you must follow:

- You only have two baskets, and each basket can only hold a single
  type of fruit. There is no limit on the amount of fruit each basket
  can hold.
- Starting from any tree of your choice, you must pick exactly one
  fruit from every tree (including the start tree) while moving to the
  right. The picked fruits must fit in one of your baskets.
- Once you reach a tree with fruit that cannot fit in your baskets, you
  must stop.

Given the integer array `fruits`, return the maximum number of fruits
you can pick.

```
fruits = [1,2,1]      ->  3
fruits = [0,1,2,2]    ->  3    (trees 1 to 3)
fruits = [1,2,3,2,2]  ->  4    (trees 1 to 4)
```

**Constraints:** `1 <= fruits.length <= 10^5` and
`0 <= fruits[i] < fruits.length`.

## Approaches

The fruit picked is a stretch of consecutive trees with at most two
types on it, so the answer is the longest such stretch.

| file | mechanism |
|---|---|
| `total_fruit.kara` ★ | a sliding window over a map of counts: the right end moves one tree at a time, and while the map holds three types the left end moves on, a type whose count reaches 0 leaving the map. O(n) |
| `total_fruit_counts.kara` | the same window with the counts in an array indexed by type, since every type is below n, and the number of types in the window kept alongside. O(n) |
| `total_fruit_last.kara` | the last two types and the last run: a tree of either type extends the stretch ending at it, a tree of a third type starts a new one made of the last run and itself. O(n) time, O(1) space |
| `total_fruit_blocks.kara` | the trees squeezed into runs of one type; a longest stretch is whole runs, so a window of consecutive runs with at most two types, a run of a third type restarting it at the run before. O(n) |
| `total_fruit_search.kara` | a binary search on the length, since a stretch that fits holds shorter ones that fit; a length fits when a window of that many trees, slid along the row, ever holds two types or fewer. O(n log n) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 12 lines: LeetCode's three examples, an
earlier one (`[3,3,3,1,2,1,1,2,3,3,4]`) and five more (`[0]`,
`[0,0,0,0]`, `[0,1,0,1,0,1]`, `[0,1,2,3,4,5]` and
`[1,0,1,4,1,4,1,2,3]`); for 300 random cases of up to 1,000 trees, of
2, 3 or 5 types or as many as trees, in runs of up to 1 to 5 trees, the
sum and a checksum of the answers; and two of LeetCode's largest,
100,000 trees of 3 types in runs of up to 50, and 100,000 trees of 2
types with a third every 30,000. `total_fruit.py` mirrors the ★ arm and
its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every stretch of trees tried, its types listed afresh, and
the longest with at most two types kept. It checks 3,200 random cases:
3,000 of up to 10 trees against the statement and 200 of up to 500
trees against the other properties, of 2 types to as many as trees, in
runs of up to 1 to 5; 64,826 trees in all.

| | property |
|---|---|
| P1 | the statement's longest stretch, on the small cases |
| P2 | at least the longest run of one type, and at least 2 trees when there are two types; at most n, and all n when there are at most two types |
| P3 | the same answer for the row read backwards |
| P4 | the same answer with every type moved on by the same amount round n |
| P5 | two rows joined give at least the larger of their two answers and at most their sum; one more tree adds at most 1 |
| P6 | each arm agrees with at least two of the other four |

P2 to P6 are checked on every case. It prints `3200 cases, 64826 trees,
95000 checks over 5 arms: 0 failures` under `karac __mir-run` and
`karac __mir-llvm-run`, and the same under `karac __mir-llvm-asan` with
no error.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-llvm-run`. All fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: three types allowed in the window | P1 907, P6 1055 |
| M2 | ★: the last window kept, not the longest | P1 483, P2 165, P3 791, P5 1497, P6 621 |
| M3 | ★: the window measured one short | P1 3000, P2 2199, P5 1424, P6 3200 |
| M4 | counts: a new type never counted | P1 907, P6 1055 |
| M5 | counts: the window cut down to one type | P1 2085, P2 1334, P6 2282 |
| M6 | counts: the first tree never the right end | P1 786, P2 297, P3 554, P5 762, P6 850 |
| M7 | last: a third type starting a stretch of itself alone | P1 2085, P2 1281, P3 595, P5 82, P6 2282 |
| M8 | last: the type before the last never remembered | P1 745, P2 506, P6 890 |
| M9 | last: only the last type extending the stretch | P1 745, P2 506, P6 890 |
| M10 | blocks: the run before dropped from a new window | P1 401, P3 751, P5 179, P6 543 |
| M11 | blocks: a third type let into a window of two runs | P1 713, P3 381, P5 22, P6 823 |
| M12 | blocks: each repeat counted twice | P1 2503, P2 2094, P5 1069, P6 2699 |
| M13 | search: one type taken as the limit | P1 2085, P2 1334, P6 2282 |
| M14 | search: the whole row never tried | P1 1796, P2 1848, P5 787, P6 1848 |
| M15 | search: the window one tree too long | P1 310, P3 614, P5 149, P6 405 |

P1 and P6 kill all fifteen; P2 kills ten, P5 nine and P3 six. P4 kills
none: every arm compares types only for equality (the counts arms also
index by them, and a renaming round n keeps them below n), and none of
the edits changes that. M1 and M4 fail exactly the same cases. M4
never shrinks the window, so it answers n; M1 allows three types. A
longest stretch of two types that is not the whole row can always take
one more tree into a stretch of three, so M1 is wrong exactly when the
row has three types, which is when M4 is. Both keep every relation P2
to P5 states, as n is within all their bounds. M8 and M9 are the same
edit in effect: with the type before never set, only the last type
extends the stretch. M5 and M13 both answer the longest run of one
type.

Four mutants were replaced because they crashed rather than gave a
wrong answer: a spent type kept in the ★ map at count 0, each tree's
count in the ★ map set to 1, each new type counted twice in the counts
arm, and a type dropped from the counts arm while one tree of it was
left. Each leaves the window believing it holds three types, so its
left end runs past the end of the row and the read there stops the
program with an index out of bounds.

## Verification

Every arm prints the same output as `total_fruit.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build and the runtime archives are both at
kara `5502146bed`. Under `karac __mir-run` the arms take 0.7 to 2.5 s
each (the binary search the longest) and the differential 5.3 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The frozen legacy lanes split. The ★, counts and search arms print the
same output under the legacy interpreter, the legacy JIT and both legacy
builds, with and without auto-par. Every legacy lane refuses the last
and blocks arms, the differential and the bench program: `*f` on an
element of `.iter()` is rejected, because legacy's iterator gives the
value itself. Legacy is frozen, so none of this is filed.

## Benchmarks

The bench program uses the last arm, the O(1)-space one, on one row of
1,000,000 trees of 3 types in runs of 1 to 50, built once. Each round
finds the most fruit, folds it into a checksum and changes one tree's
type; 240 rounds. Every implementation prints `240 rounds over 1000000
trees: answers summing to 187440, checksum 181860875`.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.37 to 0.47 s | 0.39 s |
| Rust (`rustc -O`) | 0.41 to 0.45 s | 0.43 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.36 to 0.40 s | 0.38 s |
| Go | 0.36 to 0.39 s | 0.37 s |
| Python | 18.6 s | |
| Kāra (`karac build --mir`) | 0.40 to 0.46 s | 0.41 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Legacy refuses the bench program
(above), so it has no row.

v2 takes 1.06 times Rust's median time under overflow checks and 1.03
times C's. Under valgrind's cachegrind C runs 3.25 billion instructions
and 0.12 billion branches, Rust with overflow checks 3.86 billion and
1.20 billion, and v2 4.81 billion and 1.20 billion; C mispredicts 66
thousand, Rust and v2 6.4 million each. So C makes the loop nearly
branch-free, and v2 runs 25% more instructions than Rust with overflow
checks for 6% more time; neither was profiled further. Plain Rust
(`rustc -O`) is slower here than Rust with overflow checks, 0.43 s
against 0.38 s; that was not looked into either. The comparison with C
and Rust waits until after M4.
