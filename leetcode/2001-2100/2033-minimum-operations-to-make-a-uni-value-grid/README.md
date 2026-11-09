# 2033. Minimum Operations to Make a Uni-Value Grid

You are given an `m x n` integer grid and an integer `x`. In one operation
you can add `x` to or subtract `x` from any element of the grid. A
uni-value grid is a grid where all the elements are equal. Return the
minimum number of operations to make the grid uni-value, or -1 if that is
not possible.

```
grid = [[2,4],[6,8]],  x = 2  ->  4
grid = [[1,5],[2,3]],  x = 1  ->  5
grid = [[1,2],[3,4]],  x = 2  ->  -1
```

**Constraints:** `1 <= m, n <= 10^5`; `1 <= m * n <= 10^5`;
`1 <= x, grid[i][j] <= 10^4`.

An operation never changes a value's remainder mod `x`, so the values can
meet only when they all leave the same one. When they do, making them all
`t` costs `sum |v - t| / x`, and that sum is smallest at a median of the
values.

## Approaches

| file | mechanism |
|---|---|
| `grid.kara` ★ | the grid flattened with `flat_map`, the remainders checked with `any`, sorted, and the distances to the middle value summed. O(mn log mn) |
| `grid_select.kara` | the median by quickselect instead of a sort: a Lomuto partition around the middle of the range, through a `mut ref Vec`, keeping the side that holds the middle index. O(mn) expected |
| `grid_count.kara` | a count per value in an `[0; 10001]` array, since values are at most 10^4: the median found by walking the counts past half the cells, the cost read off the counts. O(mn + 10^4) |
| `grid_prefix.kara` | no median assumed: the remainders gathered into a `SortedSet`, the values sorted with prefix sums, and every value tried as the target, the cheapest kept. O(mn log mn) |
| `grid_sweep.kara` | the cost at the smallest value, then swept up the sorted values: a step of `d` changes it by `(2 i - len) d / x`, and the smallest cost seen is the answer. O(mn log mn) |
| `grid_solution.kara` | LeetCode's Rust template (a unit struct, `impl Solution`, `Vec<Vec<i32>>`, `into_iter().flatten()`, `|&a|` closures, `sort_unstable`, a `&Vec` wrapper), carried by `karac fix` to a clean check |
| `differential.kara` | all six arms against the statement read literally, six properties |

Every arm prints the same 12 lines: the answers for LeetCode's three
examples and seven more; then the count answered, the total and a checksum
for 3000 grids of 1 to 6 by 1 to 6 values up to 30, three in four of them
aligned (every value a base plus a multiple of `x`); and the total and a
checksum for 6 grids of about 100000 values up to 10^4, the most the
constraints allow, one a single row and one a single column, the last not
aligned. `grid.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every target from the smallest value to the largest tried, a
target some value cannot reach in steps of `x` passed over, the fewest
operations kept, -1 if no target is reachable. It checks 2000 grids of 1 to
5 by 1 to 5 values up to 30, `x` from 1 to 5, three in four aligned. Every
grid, and the lift P2 uses, is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | every value raised by the same amount leaves the answer |
| P3 | the grid transposed leaves the answer |
| P4 | every value `v` turned into `31 - v` leaves the answer |
| P5 | every row written twice doubles the answer, -1 staying -1 |
| P6 | each arm agrees with at least three of the other five |

P2 holds because a lift moves every value and every target alike. P3
because the answer depends only on the values, not on where they sit. P4
because `v -> 31 - v` keeps every distance and maps the remainders mod `x`
to one remainder exactly when they were one. P5 because a median of the
values is still a median of the values twice over, and each costs twice.

The differential prints `2000 problems: checksum 917670021, 72000 checks
over 6 arms: 0 failures` under every lane in Verification. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Thirty edits to the differential, five to each of its arms, each run under
`karac __mir-run` and `karac __mir-llvm-run`. Seventeen are kept, three to
each of the five Kāra arms and two to the Rust arm. All thirty are killed,
each fails the same way under both backends, none by a crash, and no two
kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the median taken unsorted | P1 687, P3 493, P5 870, P6 687 |
| M2 | ★: the smallest value as the target | P1 1027, P4 1073, P6 1027 |
| M3 | ★: the median one above the middle | P1 613, P4 767, P5 374, P6 613 |
| M4 | select: the middle index rounded up | P1 239, P4 290, P5 239, P6 239 |
| M5 | select: the pivot never swapped into place | P1 401, P3 338, P4 595, P5 502, P6 401 |
| M6 | select: the cost summed with the signed distance | P1 1234, P4 1071, P5 153, P6 1234 |
| M7 | count: the count of a value never added | P1 946, P2 851, P4 1080, P5 1430, P6 946 |
| M8 | count: each value counted once in the cost | P1 885, P4 230, P5 1327, P6 885 |
| M9 | count: the median walk starting at 1 past an empty prefix | P1 1112, P4 771, P6 1112 |
| M10 | prefix: the values below costed from the wrong side | P1 1327, P4 1073, P5 67, P6 1327 |
| M11 | prefix: the target itself counted above | P1 1374, P2 1636, P4 1604, P5 1374, P6 1374 |
| M12 | prefix: any number of remainders allowed but x | P1 343, P5 158, P6 343 |
| M13 | sweep: the gap taken from the first value unsorted | P1 1209, P3 459, P4 1156, P5 797, P6 1209 |
| M14 | sweep: a step's change with the sign flipped | P1 1132, P4 1073, P5 18, P6 1132 |
| M15 | sweep: the values below counted one short | P1 1234, P4 935, P5 1234, P6 1234 |
| M16 | Rust: the distance squared | P1 1293, P4 328, P6 1293 |
| M17 | Rust: the median one below the middle | P1 242, P4 290, P5 242, P6 242 |

P1 and P6 kill all seventeen, P4 fifteen, P5 fourteen, P3 three and P2
two. P4 mirrors every value, so it sees each edit that leans to one side
of the median or of the sorted order: a target at the smallest value (M2),
a median one place off (M3, M4, M9, M17), costs taken from the wrong side
(M6, M10, M14, M15) and the rest. It misses only the unsorted median (M1)
and the remainders let through (M12), which treat both sides alike. P5
writes every row twice, which moves the middle index and doubles every
count, so it sees the middles one place off (M3, M4, M17) and the
miscounted cells (M7, M8). P3
transposes the grid, which changes only the order the values arrive in,
so it sees just the edits that depend on that order: the median read from
the values unsorted (M1, M13) and the quickselect's pivot left out of
place (M5). P2 lifts every value, so it sees only the edits that read a
value's size rather than its distance: a count never added past the first
(M7) and the target counted among the values above it (M11).

The other thirteen fail as a kept one does, or with counts of their own.
The Rust arm's median read before the sort fails as M1. Three edits fail
alike with the cost of the smallest or the largest value rather than the
median's: the prefix arm's best never lowered, the sweep arm's best taken
as the last cost, and the Rust arm's largest value as the target. The
remainder check skipped fails alike in the ★ and Rust arms. The ★ arm's
distance not divided by `x`, the quickselect comparing only the last
remainder or stopping with two values left, the count arm's median past
half the cells rounded down or its cells counted once a row, the prefix
arm's values above taking one target too many, and the sweep arm's first
step skipped fail with counts of their own. Six drafts were replaced
after a run: four changed no answer (a Lomuto partition keeping equal
values left, the remainder taken from another cell, the sweep's last step
never taken, and the distance rounded up, when every distance is a
multiple of `x`), and two crashed (the prefix arm's last value never tried
and the sweep's cost at the smallest never a candidate both leave a
one-value grid at `i64.MAX`, which the harness then doubles). Three more
were replaced before running: the lower of two middle values, which costs
the same; a middle index one too low, which indexes -1 on one value; and a
quickselect stepping onto its pivot, which can loop forever.

## Verification

Every arm prints the same output as `grid.py` under `karac __mir-run` (the
v2 MIR interpreter), `karac __mir-llvm-run`, and `karac __mir-llvm-asan`
(AddressSanitizer and LeakSanitizer) with no error. `karac run` and a
`karac build` binary print the same output for every arm and the
differential. `karac check --output=json` reports nothing on any of them.
Under `karac __mir-run` the arms take 2.1 s (select) to 8.5 s (count),
most of it the six grids of 100000 values, and the differential 30 s, most
of it the count arm walking its 10001 counts twice in each of its 12000
calls.

The five arms were written in Kāra and checked clean but two. The ★ arm
first flattened the grid with `grid.iter().flatten()`, as Rust does; Kāra's
`flatten` needs items that are themselves iterators (docs/library/
iterators.md), and a `ref Vec[i64]` is not one, so the check refused it with
a machine fix to `.flat_map(|v| v.iter())`, which `karac fix` applied. The
prefix arm first wrote `collect::[SortedSet[i64]]().len()`, a Rust
turbofish in Kāra's brackets. Kāra has no call-site type arguments, and
the parse error said so and gave the shape to use instead, a typed `let`
bound first; there is no machine fix, since the binding needs a name, and
the arm was edited by hand to that shape.

The Rust arm was written as LeetCode's Rust template and reaches a clean
check through `karac fix` alone, in two rounds (17 and 3 edits). The first
carries the unit struct, the `Vec<..>` types, the `|&a|` and `|&v|`
closures, the `&Vec` parameter and the `::` path. The second turns
`sort_unstable` into `sort` (the library has only the stable sort, which is
also an unstable one), turns `into_iter().flatten()` into
`into_iter().flat_map(|v| v.into_iter())`, and, since a bare parameter
borrows in Kāra, consumes a `clone()` of `grid`.

## Benchmarks

The bench builds 20 grids of 200 by 250 values up to 10^4 once in all five
languages, each grid's values one remainder apart modulo its `x` (1 to 7),
and runs the ★ arm on each for 30 rounds, one cell moved by `x` before each
call: 600 calls, 3 x 10^7 values flattened and sorted. Every implementation
prints `600 calls: sum 28612380578, checksum 279900403`.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with kara `7a9ac8e23f` on LLVM 22:

| | time | median |
|---|---|---|
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.576 to 0.619 s | 0.598 s |
| Kāra (`karac build`) | 0.594 to 0.665 s | 0.627 s |
| Rust (`rustc -O`) | 0.782 to 0.861 s | 0.802 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.766 to 0.849 s | 0.817 s |
| Go | 3.763 to 3.933 s | 3.811 s |
| C (`clang -O3`) | 3.785 to 3.881 s | 3.815 s |
| Python | 9.4 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`, the
sequential lane. A plain `karac build` parallelizes nothing here: its user
time (0.619 s) is not above its real time (0.627 s).

The sequential Kāra program is 0.73x Rust under overflow checks and 0.16x
C. The sort is each language's own library sort, and it is nearly all the
time: C's `qsort` calls its comparator through a pointer for every
comparison and Go's `sort.Slice` through a closure, while Kāra's and Rust's
`sort` are compiled for `i64`.
