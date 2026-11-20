# 1284. Minimum Number of Flips to Convert Binary Matrix to Zero Matrix

Given an `m x n` binary matrix `mat`, one step chooses a cell and flips it
and its four neighbours, those that exist (a 1 becomes 0 and a 0 becomes
1). Return the minimum number of steps to turn `mat` into the zero
matrix, or `-1` if it cannot be done.

```
mat = [[0,0],[0,1]]        ->  3
mat = [[0]]                ->  0
mat = [[1,0,0],[1,0,0]]    ->  -1
```

**Constraints:** `1 <= m, n <= 3`, `mat[i][j]` is 0 or 1.

The arms are `fn min_flips(mat: Vec[Vec[i64]]) -> i64`.

## Approaches

| file | mechanism |
|---|---|
| `min_flips.kara` ★ | breadth-first search over the matrix's states, each a bit mask of its cells, in a `VecDeque`; a step XORs the mask of a cell and its neighbours, and the zero state's distance is the answer. O(2^(mn) mn) |
| `min_flips_subsets.kara` | by subsets: steps commute and a cell chosen twice is not chosen, so an answer is a set of cells. Every set is applied to a copy of the matrix, and the smallest that clears it is kept |
| `min_flips_chase.kara` | by chasing the lights down: once the first row's steps are chosen, a cell still lit can only be cleared from the row below, so every later row's steps are forced. Each first-row choice is followed down by `chase`, which answers an `Option`, and the lightest that leaves the last row dark is kept. O(2^n mn) |
| `min_flips_gauss.kara` | by linear algebra over GF(2): which cells to step on is a vector x with A x = b. Gaussian elimination on bit-mask equations finds the pivots, every setting of the free unknowns gives one solution, and the lightest is the answer |
| `min_flips_solution.kara` | a Rust solution as LeetCode's Rust users write it (a `VecDeque` of (state, steps), a `HashSet` of seen states whose `insert` answers whether the state is new, `i32` offsets checked against `usize` bounds), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 11 lines: LeetCode's three examples (`3 0
-1`); for each shape from 1 by 1 to 3 by 3, over every matrix of that
shape, how many are solvable, their steps in all and the most any needs
(`2 by 3: 16 of 64 solvable, 26 flips, at most 3`, `3 by 3: 512 of 512
solvable, 2304 flips, at most 9`); and a checksum over all 682 answers
(`checksum 156260449`). `min_flips.py` mirrors the ★ arm, and its output
is byte-identical. Every arm gives the same output under `karac run` and
`karac build`, and under the AddressSanitizer build.

The Mend loop: the ★ and chase arms checked clean as first written. The
subsets arm's first draft held the sizes as `i32`; `redundant_cast` on
its `r as i64` showed that `i32 + (an i64 offset)` is already an `i64`
(lossless widening in an operator, design.md §5), and the `i32` was
dropped. The gauss arm wrote Rust's `!(1 << u)`; `karac fix` made it
`~(1 << u)` and, once that parsed, dropped the `*` from `*e` and `*u` in
the closures of `find` and `filter` over a range, which take the number
itself: 3 fixes in one round. The solution arm takes one round of 17
fixes by `karac fix`'s count: the `use std::collections::{HashSet,
VecDeque}` line deleted, `Vec<..>` became `Vec[..]` and `HashSet` became
`Set`, `::` paths took `.`, `&&` became `and`, the `as usize` casts on
the bounds were dropped as widenings (`(x as usize) < m` became `(x) <
m`, keeping its parentheses), the wrapper's `as i64` was dropped, and
`struct Solution;` became `struct Solution {}`. No gap was met.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the matrices reachable in exactly k steps, a `Set` of them for
k = 0, 1, 2, ..., until one is the zero matrix; a step taken twice
undoes itself, so the set k + 2 steps away holds the one k away, and once
it is no larger no number of steps will reach zero. Each step's change
is found by taking that step on the zero matrix. Every matrix of every
shape is checked, 682 in all, each property on every arm.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the matrix transposed: the same answer |
| P3 | the rows in reverse order: the same answer |
| P4 | one step taken on a random cell: solvable exactly when the matrix is, and the answer within 1 |
| P5 | the cellwise XOR with a random matrix of the shape: solvable when both are, in at most their two answers' sum |
| P6 | the ★ arm's answer |

All 20,460 checks pass on every arm: `682 matrices: checksum 156260449,
20460 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and the AddressSanitizer build. The checksum runs
over the ★ arm's answers in the harness's order, so it is the harness's
own, and Python's.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac run`, each failing the same way under both.

| # | mutation | failures by property |
|---|---|---|
| S1 | ★: a step in the first column never flips the cell below | P1 420, P2 438, P3 326, P4 76, P6 1680 |
| S2 | ★: the queue read from the back, a depth-first search | P1 492, P2 424, P3 444, P4 356, P5 100, P6 1968 |
| B1 | subsets: the left neighbour replaced by a second right one, which undoes the first | P1 532, P2 506, P4 261, P6 532 |
| B2 | subsets: the largest clearing set kept, not the smallest | P1 30, P6 30 |
| C1 | chase: a cell lit in the first column never cleared from below | P1 509, P2 434, P3 254, P4 89, P6 509 |
| C2 | chase: half the first-row choices tried (`1 << (cols - 1)`) | P1 275, P2 276, P3 272, P4 58, P6 275 |
| G1 | gauss: a pivot never cleared from the other equations | P1 491, P2 34, P3 50, P4 291, P6 491 |
| G2 | gauss: a step added to every weight when the free unknowns are odd in number | P1 4, P6 4 |
| O1 | solution: the start answered only when reached after a step | P1 9, P4 17, P5 10, P6 9 |
| O2 | solution: a step no longer flips its own cell | P1 663, P4 198, P6 663 |

All ten are caught by P1, the statement read literally. B2 and G2 are
the faint ones because most matrices here have one clearing set at
most: a shape whose step matrix is invertible, as 3 by 3 is (512 of 512
solvable), has exactly one, so the largest and the smallest are the
same set. Only matrices with several clearing sets see B2 (30 of 682)
and only those with an odd number of free unknowns see G2 (4). O1
fails on the nine dark matrices, one per shape: the dark start is in the seen set
before the search begins, so it is never popped again and reads as
unsolvable, -1 for 0. S2 keeps
finding the zero state, by a longer path, and P6 fails on all four
other arms. O2 is the one edit P2 and P3 cannot see: a step that flips
only its neighbours is still symmetric under transposing and under
reversing the rows. B1 leaves a step flipping its cell and the
ones above and below it, which reversing the rows also keeps, so P3
misses it too; transposing turns it into a step along the row, and P2
sees it.

## Benchmarks

`bench/` runs the same workload in Kāra, C, Rust, Go and Python: the ★
arm (breadth-first search over bit masks) on every matrix of every
shape, 1 by 1 to 3 by 3, 3000 rounds, every answer folded into a
checksum. Every program prints `3000 rounds of every matrix: checksum
475470399`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `684b860a50`
on LLVM 22. A plain `karac build` targets x86-64-v2, so the C and
overflow-checked Rust programs are also built at x86-64-v3 for
comparison:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 4.080 to 4.476 s | 4.256 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 4.111 to 4.470 s | 4.346 s |
| Rust (`rustc -O`) | 5.156 to 6.508 s | 5.461 s |
| Rust (`rustc -O -C overflow-checks=on`) | 5.516 to 6.157 s | 5.704 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 4.884 to 5.851 s | 5.011 s |
| C (`clang -O3`) | 2.824 to 2.949 s | 2.891 s |
| C (`clang -O3 -march=x86-64-v3`) | 2.236 to 2.425 s | 2.312 s |
| Go | 11.57 to 13.82 s | 12.17 s |
| Python | 225.08 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Kāra is about 24% ahead of Rust with overflow checks on (4.346 s
against 5.704 s). Kāra takes about 1.5x C's time (4.346 s against 2.891
s); Go takes about 2.8x Kāra's time. Python takes about 52x Kāra's time.
No profile was taken.
