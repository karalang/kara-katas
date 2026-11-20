# 1691. Maximum Height by Stacking Cuboids

Given `n` `cuboids` where the dimensions of the `i`th cuboid is
`cuboids[i] = [widthi, lengthi, heighti]` (**0-indexed**). Choose a
**subset** of `cuboids` and place them on each other.

You can place cuboid `i` on cuboid `j` if `widthi <= widthj` and
`lengthi <= lengthj` and `heighti <= heightj`. You can rearrange any
cuboid's dimensions by rotating it to put it on another cuboid.

Return *the **maximum height** of the stacked* `cuboids`.

```
cuboids = [[50,45,20],[95,37,53],[45,23,12]]                                 ->  190
cuboids = [[38,25,45],[76,35,3]]                                             ->  76
cuboids = [[7,11,17],[7,17,11],[11,7,17],[11,17,7],[17,7,11],[17,11,7]]      ->  102
```

**Constraints:** `n == cuboids.length`; `1 <= n <= 100`;
`1 <= widthi, lengthi, heighti <= 100`.

## Approaches

| file | mechanism |
|---|---|
| `cuboids.kara` ★ | a best stack stands every cuboid on its two shorter sides, so with each cuboid's sides sorted one fits on another when each side is no longer; sorted as lists, a cuboid can only stand on one before it, and `best[i]`, the tallest stack with cuboid i on top, is its height plus the best of those it fits on. O(n^2) |
| `cuboids_memo.kara` | sides sorted, the cuboids left in their order: the tallest stack above each cuboid searched by recursion and kept in a table of `Option[i32]`, equal cuboids ordered by index so the search cannot go round. O(n^2) |
| `cuboids_kahn.kara` | the graph of fits, an edge from j to i when j fits on i, its longest path in Kahn's order: a cuboid comes off a `VecDeque` once every cuboid that fits on it has, and passes its tallest stack up. O(n^2) |
| `cuboids_solution.kara` | a Rust solution as LeetCode's Rust users write it, the parameter taken `mut cuboids`, each sorted with `sort_unstable`, a `vec![0; n]` table and `*dp.iter().max().unwrap()`, carried to Kāra by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 7 lines: LeetCode's three examples and one
cuboid; then the answers summed and a checksum for 3000 random sets of
up to 6 cuboids with sides up to 5, 300 of up to 30 up to 50 and 30 of
up to 100 up to 100. `cuboids.py` mirrors the ★ arm and its output is
byte-identical.

```
190
76
102
3
3000 sets of up to 6 cuboids up to 5: answers sum to 35852, checksum 853140951
300 sets of up to 30 cuboids up to 50: answers sum to 56314, checksum 761032851
30 sets of up to 100 cuboids up to 100: answers sum to 21533, checksum 962299153
```

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every cuboid turned each of its six ways, placed on the floor
or on the one below only where its width, length and height are each no
more, every unused cuboid tried next, with a table over the cuboids used
and the one on top. It does not sort sides or assume the longest side
goes up. It checks 3000 random sets of 1 to 5 cuboids with sides from 1
to between 1 and 6. Every case is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the cuboids in reverse order give the same answer |
| P3 | each cuboid's sides listed in another order give the same answer |
| P4 | every side doubled doubles the answer |
| P5 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 131470312, 60000 checks
over 4 arms: 0 failures` under every lane in Verification, and a Python
reading of the statement, a search over every turn of every cuboid,
gives the same checksum. On a failure it prints the first ten and then
the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. P4 fails for no mutant: every edit is
as wrong at twice the sides. M2 and M8 both leave the cuboids unsorted
and fail the same checks.

Two first drafts were replaced. A first M5 left the middle side out of
the memo arm's fit, so two cuboids could each fit on the other and the
search went round until the stack ran out, on both backends. A first M9
started each table entry at 0 rather than the cuboid's height; the bare
`0` written into the table made its elements `i64`, and the arm no
longer checked (E0200), so it tested nothing.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the sides left unsorted | P1 2021, P3 1912, P5 2021 |
| M2 | ★: the cuboids left unsorted | P1 1323, P2 1549, P5 1323 |
| M3 | ★: the stack grows by the lower cuboid's height | P1 1163, P5 1163 |
| M4 | memo: each cuboid stood on its long side, its shortest up | P1 2432, P5 2432 |
| M5 | memo: the last stack that fits, not the tallest | P1 882, P2 1033, P5 882 |
| M6 | kahn: the last cuboid below sets the height, not the tallest | P1 109, P2 206, P5 109 |
| M7 | kahn: a cuboid's wait never counted down | P1 1615, P5 1615 |
| M8 | solution: the cuboids left unsorted | P1 1323, P2 1549, P5 1323 |
| M9 | solution: each cuboid's middle side up | P1 1734, P5 1734 |
| M10 | kahn: the first side must be strictly shorter | P1 1942, P5 1942 |

## Benchmarks

The bench draws 3000 sets of 100 cuboids with sides up to 100,
LeetCode's largest, all of them first, then answers each 5 times by the
★ arm in all five languages: each sorts a copy's sides and the copy as
lists, by `sort` in Kāra and Rust, `slices.Sort` and `slices.SortFunc`
with `slices.Compare` in Go, `sorted` in Python, and an insertion sort
of the three sides and `qsort` of the rows in C. Every implementation
prints `3000 sets of 100 cuboids, 5 rounds: answers sum to 14655885,
checksum 625992380`. The C build also runs clean under gcc's
AddressSanitizer and UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `9b0b5eb92c` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.412 s |
| Rust (`rustc -O`) | 0.476 s |
| Kāra (`karac build`) | 0.489 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.489 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.491 s |
| Go | 0.556 s |
| Python | 8.1 s |

The sequential Kāra build is level with Rust and level with Rust with
overflow checks on, the equal-safety comparison (BENCHMARKS.md). C is
the fastest here at 0.412 s.

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here:
its user time is not above its real time (0.592 s and 0.607 s on one
run).

## Verification

All four arms print the same output as `cuboids.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `9b0b5eb92c`.

## Writing it

The ★, memo and Kahn arms checked clean as first written: `Vec[Vec[i32]]`
sorts as lists, `Vec.filled(n, Vec.new())` takes its element type from
the pushes, and `Vec.filled(n, None)` from the `mut ref Vec[Option[i32]]`
it is handed to.

LeetCode's Rust solution took one `karac fix` of 11 edits:
`struct Solution {}` added; the `mut cuboids` parameter, which Kāra
writes in the type, taken `cuboids: own Vec[Vec[i32]]` with
`let mut cuboids = cuboids;` at the body's start (E0002 names both that
and `mut ref`, and the fix takes the owned one, as Rust's is);
`Vec<Vec<i32>>` written `Vec[Vec[i32]]`; each `sort_unstable` written
`sort`; `vec![0; n]` written `Vec.filled(n, 0)`; and `&&` written `and`.
The table's `0` took `i32` from the heights written into it, so
`*dp.iter().max().unwrap()` needed no change.

`arm_name` in the differential indexes a list of string literals for a
`Str`, as #1662's does (B-2026-11-19-131).
