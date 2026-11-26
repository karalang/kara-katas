# 1439. Find the Kth Smallest Sum of a Matrix With Sorted Rows

You are given an `m x n` matrix `mat` that has its rows sorted in
non-decreasing order and an integer `k`. You are allowed to choose
exactly one element from each row to form an array. Return the `k`th
smallest array sum among all possible arrays.

```
mat = [[1,3,11],[2,4,6]], k = 5                ->  7
mat = [[1,3,11],[2,4,6]], k = 9                ->  17
mat = [[1,10,10],[1,4,5],[2,3,6]], k = 7       ->  9
mat = [[1,1,10],[2,2,9]], k = 7                ->  12
```

**Constraints:** `m == mat.length`, `n == mat[i].length`, `1 <= m, n <=
40`, `1 <= mat[i][j] <= 5000`, `1 <= k <= min(200, n^m)`, `mat[i]` is a
non-decreasing array.

Each arm is `fn kth_smallest(mat: Vec[Vec[i32]], k: i32) -> i32`.

## Approaches

| file | mechanism |
|---|---|
| `kth_smallest.kara` ★ | the k smallest sums of the rows so far, each next row added to every one of them, the new sums sorted and cut back to k by `truncate`: a sum among the k smallest of all the rows comes from one among the k smallest of the rows before. O(m · k n log(k n)) |
| `kth_smallest_heap.kara` | the rows taken in one at a time, each time the k smallest sums of the sums so far and the next row, by a `PriorityQueue` holding each sum's next pairing with the row, popped through `let Some(..) = heap.pop() else`. O(m · k log k) |
| `kth_smallest_search.kara` | the answer searched for by halves between the smallest sum and the largest, the least sum with at least k sums at or below it, each count by a search over the rows that stops at k. O(m n k log S) for a sum range S |
| `kth_smallest_states.kara` | the sums met in order from the smallest, each a choice of a place in every row as a `Vec[i64]`: a heap of choices by their sums, each one popped leading on to the choices with one place moved on, a `Set[Vec[i64]]` keeping each choice to one visit. O(k · m² log(k m)) |
| `kth_smallest_solution.kara` | a Rust solution as LeetCode's Rust users write it (`let k = k as usize`, the sums so far in `vec![0]`, each row merged in by `Vec::with_capacity`, `for &a in cur.iter()`, `sort_unstable()` and `truncate(k)`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 3 lines: LeetCode's four examples and four
more (`7 17 9 12 5 4 6 15000`); the constraints' most, 40 rows of 40
drawn numbers up to 5000 with k = 1 and 200, and 40 rows of 40 numbers
all 5000 with k = 200 (`40 rows of 40: 4386 4415 200000`); and 2000
random cases of 1 to 6 rows of 1 to 6 numbers up to 10, 100 or 5000, k
up to how many sums there are, at most 200 (`2000 random cases: 5020926
in all, checksum 349980153`). `kth_smallest.py` mirrors the ★ arm, and
its output is byte-identical. Every arm gives the same output under
`karac __mir-run`, `karac run`, `karac build` and `karac
__mir-llvm-run`.

The Mend loop: the ★, heap and states arms check clean as first written.
The search arm wrote its two bounds as `let (mut low, mut high) = ..`,
which `karac check` refuses, saying `mut` goes before the whole pattern
in Kāra, and `karac fix` writes `let mut (low, high) = ..`, 3 fixes by
its count. The Rust solution takes one round of 16 fixes by `karac
fix`'s count: `struct Solution;` to `struct Solution {}`, `Vec<..>` to
`Vec[..]`, `k as usize` to `k as i64`, `vec![0]` to `[0i32]`,
`Vec::with_capacity` to `Vec.with_capacity`, the `&a` and `&b` patterns
to `a` and `b`, `sort_unstable()` to `sort()`, and `Solution::` to
`Solution.`. Every arm's output matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every array of one number from each row, its sum, all of them
sorted, and the k-th, while there are at most 50,000 sums. LeetCode's
examples, four edge cases (one number, one row, one column, and the
largest numbers in every other place), the constraints' most three ways
(40 rows of 40 drawn numbers with k = 1 and 200, and 40 rows of 40
numbers all 5000), and 1992 random cases drawn as the harness draws
them.

P5 adds a row of one 1 to each case. Written
`longer.push([1].to_vec())`, it is refused, "expected 'Vec[i32]', found
'Vec[i64]'", with no fix, as in
[B-2026-11-26-6](https://github.com/karalang/kara/blob/main/docs/bugs-v2.jsonl):
the numbers in a `.to_vec()` list pushed to a `Vec[Vec[i32]]` keep the
default `i64`. The differential binds the row first under a `Vec[i32]`
annotation, which checks clean.

| | property |
|---|---|
| P1 | the statement read literally, while there are at most 50,000 sums |
| P2 | the rows in the other order give the same sum |
| P3 | k = 1 gives the sum of the rows' first numbers, and k one more never gives less |
| P4 | every number of the first row 7 more gives 7 more |
| P5 | a row more of one 1 gives 1 more |
| P6 | the ★ arm's answer |

All 60,075 checks pass on every arm: `2003 cases: checksum 342556784,
60075 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and `karac __mir-llvm-run`. Python, each row merged
in by `heapq.nsmallest`, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: the sums cut back to k unsorted | P1 1185, P2 1083, P3 297, P6 4744 |
| M2 | ★: the sum halfway to the k-th given | P1 1498, P6 5996 |
| M3 | heap: each number's first sum one too large | P1 1276, P2 546, P3 1684, P5 2003, P6 1278 |
| M4 | heap: each next sum made with the number just used | P1 1320, P2 759, P6 1321 |
| M5 | search: a number that just fits the room left out | P1 1529, P3 1659, P6 1531 |
| M6 | search: the least sum with more than k sums at or below it | P1 1529, P3 1659, P6 1531 |
| M7 | states: each choice visited as often as it is reached | P1 1149, P6 1150 |
| M8 | states: a moved choice's sum keeping the number it moved from | P1 1538, P4 1311, P6 1540 |
| M9 | solution: the sums cut back to k unsorted | P1 1185, P2 1083, P3 297, P6 1186 |
| M10 | solution: the larger of the two numbers taken for their sum | P1 1681, P3 1684, P4 1278, P5 2003, P6 1684 |

## Benchmarks

The bench runs the ★ arm on 300 matrices of 40 rows of 40 sorted numbers
up to 5000, each with a k from 1 to 200 drawn, folding the answers to a
checksum. Each implementation sorts the merged sums with its own
library's sort; C's is `qsort`, through a comparison function on every
pair. Every implementation prints `300 matrices of 40 by 40: checksum
412524233`.

BENCHTAB

Kāra is ahead of Rust here, measured by hand at 0.63 to 0.67 s against
Rust's 0.69 to 0.70 s (0.69 to 0.75 s with overflow checks on), C's 2.0
s and Go's 2.7 s; Python takes 3.8 s.
