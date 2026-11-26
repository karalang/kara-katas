# 1499. Max Value of Equation

You are given an array `points` containing the coordinates of points on
a 2D plane, sorted by the x-values, where `points[i] = [xi, yi]` such
that `xi < xj` for all `1 <= i < j <= points.length`. You are also given
an integer `k`. Return the maximum value of the equation `yi + yj +
|xi - xj|` where `|xi - xj| <= k` and `1 <= i < j <= points.length`. It
is guaranteed that there exists at least one pair of points that satisfy
the constraint `|xi - xj| <= k`.

```
points = [[1,3],[2,0],[5,10],[6,-10]], k = 1   ->  4
points = [[0,0],[3,0],[9,2]], k = 3            ->  3
```

**Constraints:** `2 <= points.length <= 10^5`, `points[i].length == 2`,
`-10^8 <= xi, yi <= 10^8`, `0 <= k <= 2 * 10^8`, and the `xi` strictly
increase.

The arms are `fn find_max_value_of_equation(points: Vec[Vec[i32]], k:
i32) -> i32`.

## Approaches

With `i < j`, the value is `(yi - xi) + (yj + xj)`, so each point `j`
wants the largest `yi - xi` among the earlier points no more than `k` to
its left.

| file | mechanism |
|---|---|
| `find_max_value_of_equation.kara` ★ | a `VecDeque` window of `(y - x, x)`, largest `y - x` first: points too far left leave at the front, the front pairs with each new point, and an entry no better than the new point's leaves at the back. O(n) |
| `find_max_value_of_equation_heap.kara` | a `PriorityQueue.max_first()` of `(y - x, x)`; the top is popped while it is too far left, and nothing else ever leaves. O(n log n) |
| `find_max_value_of_equation_sparse.kara` | a sparse table of `y - x`, the window's left end found with `partition_point`, and its largest read from two runs of the same power of two. O(n log n) |
| `find_max_value_of_equation_segment.kara` | an iterative segment tree of `y - x`, the window's left end moved by a second pointer, and its largest read by walking up from both ends. O(n log n) |
| `find_max_value_of_equation_solution.kara` | a Rust solution as LeetCode's Rust users write it (`VecDeque` and `while let Some(&(_, xi)) = dq.front()`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 4 lines: LeetCode's two examples (`4 3`); five
edges, two points exactly `k` apart, the best pair not beside each
other, a far point too far to pair, every `y` negative, and the most
values at the widest `k` (`16 22 3 -4 400000000`); the constraints'
most, 100000 points with `k` small, middling and as wide as the whole
span (`100000 points: 68358766 69500016 166328751`); and 3000 random
cases of 2 to 30 points with `k` never less than the largest rise (`3000
random cases: checksum 503842650`). `find_max_value_of_equation.py`
mirrors the ★ arm, and its output is byte-identical. Every arm gives the
same output under `karac __mir-run`, `karac run`, `karac build` and
`karac __mir-llvm-run`.

The Mend loop: the ★, heap and segment arms check clean as first
written. The sparse arm's `(i64.BITS - (j - from).leading_zeros() - 1)
as i64` took 1 fix, the cast dropped. The Rust solution takes one round
of 19 fixes by `karac fix`'s count, and its diff is: the `use
std::collections::VecDeque;` line dropped, `struct Solution;` to `struct
Solution {}`, `Vec<Vec<i32>>` and `VecDeque<(i32, i32)>` to
`Vec[Vec[i32]]` and `VecDeque[(i32, i32)]`, `VecDeque::new()` to
`VecDeque.new()`, `i32::MIN` to `i32.MIN`, the three `Some(&(..))`
patterns on `dq.front()` and `dq.back()` to `Some((..))` on `.cloned()`,
and `Solution::` to `Solution.`. Every arm's output matches on the first
run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every pair `i < j` no more than `k` apart, and the largest
`yi + yj + |xi - xj|` among them. LeetCode's examples, the edges, and
1994 random cases of 2 to 12 points, `x` rising by 1 to 6, `y` from -40
to 40, and `k` never less than the largest rise. Each arm meets six
properties on each case:

| property | what it checks |
|---|---|
| P1 | the statement read literally |
| P2 | no less than any two neighbours within `k` give |
| P3 | the points mirrored, `x` to `-x` and the order reversed, give the same |
| P4 | every `y` raised by the same amount raises the answer by twice that |
| P5 | a wider `k` gives no less |
| P6 | the ★ arm's answer |

The fixed cases are a `let` annotated `Vec[(Vec[Vec[i32]], i32)]`, as
for kata 1498 (B-2026-11-26-9). P4 compares in `i64`, so an arm that
finds no pair fails it rather than overflowing: written with three
casts, `karac fix` dropped two as implied by the third. All 60,000
checks pass on every arm: `2000 cases: checksum 469219283, 60000 checks
over 5 arms: 0 failures`, under `karac __mir-run`, `karac run`, `karac
build` and `karac __mir-llvm-run`. Python, reading every pair, gives the
same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: a pair exactly k apart refused | P1 153, P2 52, P4 27, P6 612 |
| M2 | ★: the window kept smallest first, so its front is the worst | P1 1563, P2 1165, P3 1550, P5 98, P6 6252 |
| M3 | heap: the x test turned around, so no point ever leaves | P1 457, P6 457 |
| M4 | heap: each entry remembers y where it should remember x | P1 455, P2 1, P3 1328, P4 4, P6 455 |
| M5 | segment: a pair exactly k apart refused | P1 153, P2 52, P4 27, P6 153 |
| M6 | segment: each node keeps only its left child | P1 730, P2 344, P3 991, P5 88, P6 730 |
| M7 | sparse: a pair exactly k apart refused | P1 153, P2 52, P4 27, P6 153 |
| M8 | sparse: only the first of the two runs read | P1 169, P2 141, P3 263, P5 27, P6 169 |
| M9 | solution: a pair k + 1 apart allowed | P1 124, P6 124 |
| M10 | solution: xj dropped from the value | P1 2000, P2 5, P3 2000, P6 2000 |

## Benchmarks

The bench keeps one list of 200000 points, `x` rising by 1 to 10 and `y`
up to 100000000 either way, and makes 400 calls of the ★ arm, each with
a `k` from 10 to 2009 chosen from the checksum so far and first moving
one point's `y`. Kāra, Rust and Go keep a vector per point, as
LeetCode's signature does, and a double-ended queue (Go a slice with a
moving head); C keeps a flat array of pairs and a ring buffer the size
of the points. Every implementation prints `400 calls over 200000
points: checksum 914920365`. The Kāra bench took 1 fix, an `as i64` on
the arm's answer dropped.

BENCHTAB

Measured by hand, best of three on a machine shared with a test run,
Kāra takes 1.3 s against Rust's 1.2 s (1.3 s with overflow checks on),
C's 0.80 s and Go's 1.4 s; Python takes 28.6 s.
