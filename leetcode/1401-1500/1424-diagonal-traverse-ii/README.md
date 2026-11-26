# 1424. Diagonal Traverse II

Given a 2D integer array `nums`, return all elements of `nums` in
diagonal order as shown in the below images.

```
nums = [[1,2,3],[4,5,6],[7,8,9]]
  ->  [1,4,2,7,5,3,8,6,9]
nums = [[1,2,3,4,5],[6,7],[8],[9,10,11],[12,13,14,15,16]]
  ->  [1,6,2,8,7,3,9,4,12,10,5,13,11,14,15,16]
```

The images walk each diagonal `i + j` in turn, from the corner, and each
from the bottom left up to the top right.

**Constraints:** `1 <= nums.length <= 10^5`, `1 <= nums[i].length <=
10^5`, `1 <= sum(nums[i].length) <= 10^5`, `1 <= nums[i][j] <= 10^5`.

Each arm is `fn find_diagonal_order(nums: Vec[Vec[i32]]) -> Vec[i32]`.

## Approaches

| file | mechanism |
|---|---|
| `find_diagonal_order.kara` ★ | a bucket for each diagonal i + j, the rows walked from the last up so that each bucket fills from the bottom left, then the buckets in turn. O(N) for N values |
| `find_diagonal_order_sort.kara` | every value keyed by its diagonal and then its column, `(i + j, j, x)` through `enumerate`, the keys sorted and the values read off: along a diagonal the column grows as the row falls. O(N log N) |
| `find_diagonal_order_bfs.kara` | a breadth-first walk from the corner over a `VecDeque` of places: each cell leads on to the one to its right, and a cell in the first column to the one below it too, so the queue holds one diagonal after another, each from the bottom left. O(N) |
| `find_diagonal_order_map.kara` | a `SortedMap` from each diagonal to its values, filled through `entry().or_insert`, the rows walked from the top, so each diagonal is read back to front. O(N log N) |
| `find_diagonal_order_solution.kara` | a Rust solution as LeetCode's Rust users write it (a group for each diagonal filled row by row through `enumerate`, a new group pushed when a cell reaches past the last, each group read back to front by `for &x in g.iter().rev()`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 7 lines: LeetCode's two examples and three
more, one row, one column, and rows that grow, shrink and grow again
(`1,4,2,7,5,3,8,6,9`, `1,6,2,8,7,3,9,4,12,10,5,13,11,14,15,16`, `1,2,3`,
`1,2,3`, `1,2,5,3,6,4,7`); the constraints' most, 10^5 values in one
row, in 10^5 rows of one, and in drawn rows of 1 to 600, each order
folded to a number (`10^5 values: 682358314 682358314 99681 93331505`);
and 2000 random cases of 1 to 12 rows of 1 to 1, 4 or 12 values (`2000
random cases: 44975 values, checksum 697519330`).
`find_diagonal_order.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac __mir-run`,
`karac run`, `karac build` and `karac __mir-llvm-run`.

The Mend loop: the ★, sort, bfs and map arms check clean as first
written. TOVEC The harness's column, `(1..=100000).map(|x|
[x]).collect()` into a `Vec[Vec[i32]]`, is refused, the `i64` named as
the range's, since a range of literals keeps the default (design.md §8
Literals), and `karac fix` writes `1i32..=100000`, 1 fix. The Rust
solution takes one round of 23 fixes by `karac fix`'s count: `struct
Solution;` to `struct Solution {}`, `Vec<..>` to `Vec[..]`, `Vec::new`
to `Vec.new`, the `&x` patterns to `x`, and `Solution::` to `Solution.`.
Every arm's output matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the diagonals in turn, from the corner, and on each the rows
from the bottom up, a value taken wherever the row reaches the diagonal,
while rows times diagonals are at most 10^6. LeetCode's examples, seven
edge cases (one value, one row, one column, rows that grow, rows that
shrink, a long row under short ones, equal values), the constraints'
most three ways (one row, one column, and drawn rows of 1 to 600), and
1991 random cases, up to 12 rows of up to 1, 4 or 12 values two times in
three and up to 300 rows of up to 300 otherwise, of up to 100 or 10^5.
Each case also draws a value for P4.

| | property |
|---|---|
| P1 | the statement read literally, while it is cheap |
| P2 | every value once: the answer sorted is the values sorted |
| P3 | with each cell's place as its value, the diagonals in turn and along each the row falling, while the places fit |
| P4 | a row of one value more below the rest puts that value first on its diagonal, after every cell of the diagonals before it |
| P5 | each value flipped, x to 100001 - x, flips the answer in place: the order is the cells', whatever the values |
| P6 | the ★ arm's answer |

All 57,890 checks pass on every arm: `2003 cases: checksum 449357918,
57890 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and `karac __mir-llvm-run`. The differential first
tested its `Option`s with Python's `if want is Some(ref w)`, which
`karac check` names as Python's identity test, and then checks clean
written `if let Some(ref w) = want`. Python, by sorting the cells on `(i
+ j, j)`, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: the rows walked from the top, so each diagonal fills from the top right | P1 1443, P3 1011, P4 1470, P6 5772 |
| M2 | ★: each value put in its row's bucket, not its diagonal's | P1 1443, P3 1011, P4 1470, P6 5772 |
| M3 | sort: along a diagonal the values keyed by their row, not their column | P1 1443, P3 1011, P4 1470, P6 1443 |
| M4 | sort: the keys left unsorted | P1 1443, P3 1011, P4 1470, P6 1443 |
| M5 | bfs: a cell's right neighbour queued before the cell below it | P1 1443, P3 1011, P4 1470, P6 1443 |
| M6 | bfs: a cell's right neighbour queued at the front | P1 1443, P3 1011, P4 1470, P6 1443 |
| M7 | map: each diagonal read front to back | P1 1443, P3 1011, P4 1470, P6 1443 |
| M8 | map: each value keyed by its column, not its diagonal | P1 1893, P3 1457, P4 2003, P6 1894 |
| M9 | solution: each group read front to back | P1 1443, P3 1011, P4 1470, P6 1443 |
| M10 | solution: the rows numbered from the bottom | P1 1893, P3 1457, P4 2003, P6 1894 |

## Benchmarks

The bench draws a pool of 10^5 rows of 1 to 9 values of 1 to 10^5 and
runs the ★ arm, taking its window as a `Slice[Vec[i32]]`, on 300 windows
of 2 * 10^4 rows, each window's start drawn, folding each order to a
number. The C bench keeps each bucket and each row as an array of its
own, grown by doubling, as the Kāra and Rust programs keep a `Vec` of
`Vec`s. Every implementation prints `300 windows of 2 * 10^4 rows:
checksum 524264054`.

BENCHTAB

Kāra is level with Rust and C here, measured by hand at 0.69 to 0.71 s
against Rust's 0.71 to 0.79 s (0.71 to 0.72 s with overflow checks on),
C's 0.69 to 0.70 s and Go's 1.58 to 1.64 s; Python takes 6.9 s.
