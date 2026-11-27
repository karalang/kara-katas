# 1834. Single-Threaded CPU

You are given `n` tasks labeled from `0` to `n - 1` represented by a 2D
integer array `tasks`, where `tasks[i] = [enqueueTime_i,
processingTime_i]` means that the `i`th task will be available to
process at `enqueueTime_i` and will take `processingTime_i` to finish
processing. You have a single-threaded CPU that can process at most one
task at a time and will act in the following way: if the CPU is idle and
there are no available tasks to process, the CPU remains idle; if the
CPU is idle and there are available tasks, the CPU will choose the one
with the shortest processing time, and if multiple tasks have the same
shortest processing time, it will choose the task with the smallest
index; once a task is started, the CPU will process the entire task
without stopping; the CPU can finish a task then start a new one
instantly. Return the order in which the CPU will process the tasks.

```
tasks = [[1,2],[2,4],[3,2],[4,1]]                 ->  [0,2,3,1]
tasks = [[7,10],[7,12],[7,5],[7,4],[7,2]]         ->  [4,3,2,0,1]
```

**Constraints:** `tasks.length == n`, `1 <= n <= 10^5`, `1 <=
enqueueTime_i, processingTime_i <= 10^9`.

The arms are `fn get_order(tasks: Vec[Vec[i64]]) -> Vec[i64]`.

## Approaches

| file | mechanism |
|---|---|
| `get_order.kara` ★ | the tasks taken in order of when they come in, each put in a `PriorityQueue` of (processing time, index) once the clock reaches it; the queue pops the shortest, the smaller index on a tie, and the clock runs on by its processing time, or jumps ahead to the next task when the queue is empty. O(n log n) |
| `get_order_set.kara` | the ★ arm's clock with the tasks that have come in kept in a `SortedSet` of (processing time, index), the next to run its least, taken by `min` and removed. O(n log n) |
| `get_order_heap.kara` | the ★ arm's clock over a binary heap written out: a `Vec` of (processing time, index) whose parent at k is at most its children at 2k + 1 and 2k + 2, a task sifted up on push and the last sifted down from the root on pop. O(n log n) |
| `get_order_segment.kara` | the tasks sorted by when they come in, and a segment tree over that order holding the least (processing time, index) of each range: the tasks come in as a prefix of the order, so the next to run is the least over the prefix the clock has reached, and a task run is set to a value larger than any. O(n log n) |
| `get_order_solution.kara` | a Rust solution as LeetCode's Rust users write it (a `BinaryHeap` of `Reverse((processing, index))` over a `usize` index sorted by coming-in time), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 4 lines: LeetCode's two examples; five edges,
one task, an idle gap before the second task, a tie on processing time,
every task the same, and times of 10^9, whose sum passes 2^31 (`[0] [0,
2, 1] [0, 3, 1, 2] [0, 1, 2] [0, 3, 1, 2]`); the constraints' most, 10^5
tasks coming in from 1 to 10^9 and taking 1 to 10^9, and 10^5 tasks all
coming in at once, each order folded to one number (`the most: 788285496
603191660`); and 3000 random cases of 1 to 8 tasks coming in from 1 to
10 and taking 1 to 5 (`3000 random cases: checksum 9029832`).
`get_order.py` mirrors the ★ arm, and its output is byte-identical.
Every arm gives the same output under `karac __mir-run`, `karac run`,
`karac build` and `karac __mir-llvm-run`.

The Mend loop: the ★, set and heap arms and the harness check clean as
first written. The segment arm was first written with
`best.min(tree[lo])` and `tree[2 * node].min(tree[2 * node + 1])`, four
calls of `min` on a tuple; check refused each with E0236, no method
`min` on type `(i64, i64)`, and gave no hint and no fix. `min` and `max`
are methods on numbers only, and a tuple, which compares, takes the free
`min(a, b)` (`docs/library/core-types.md`), which the arm uses; the
diagnostic that names it is B-2026-11-27-4. The Rust solution takes 35
fixes by `karac fix`'s count, and its diff is: `struct Solution {}`
added above the `impl`; the `Reverse` and `BinaryHeap` imports taken
off; `Vec<Vec<i32>>` to `Vec[Vec[i32]]`; `Vec<usize>` to `Vec[i64]` for
the index, and `|&i|` to `|i|`; `BinaryHeap::new()` to
`PriorityQueue.new()`, which pops the smallest first, and `Reverse(..)`
taken off at the push and the pop; `Vec::with_capacity` to
`Vec.with_capacity`; `&&` to `and`; `as i64` taken off the three reads
of a task's time, an `i32` widening to the `i64` clock without a cast;
`Solution::` to `Solution.` at the harness's 10 calls; and the harness's
fold, `|check, &i| (check * 31 + i as i64)`, to `|check, i|
(check * 31 + i)`. `ans.push(j as i32)` is Kāra as it stands. The
solution takes a `Vec[Vec[i32]]`, so its harness builds its tasks as
`i32`. Every arm's output matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the clock ticks one unit at a time, and at each tick an idle
CPU takes, of the tasks come in and not yet done, the one with the
shortest processing time, the smaller index on a tie, and is busy until
that time has passed. It runs 2000 random cases of 1 to 10 tasks, each
coming in at 1 to 20 and taking 1 to 10. Each arm meets six properties
on each case:

| property | what it checks |
|---|---|
| P1 | the statement read literally |
| P2 | every task done once |
| P3 | every task coming in 7 later gives the same order |
| P4 | every task coming in at once, the order is by processing time, the smaller index on a tie |
| P5 | every time doubled gives the same order |
| P6 | the ★ arm's answer |

Check warned that `vec![..]` is deprecated at the four places the
differential builds a task, and `karac fix` wrote the list literal `[a,
b]`, 4 fixes. All 60,000 checks pass on every arm: `2000 cases: checksum
163986075, 60000 checks over 5 arms: 0 failures`, under `karac
__mir-run`, `karac run`, `karac build` and `karac __mir-llvm-run`.
Python, over the same cases, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash. The segment
arm's first edit was first to read the right end of a range one leaf too
far; it stopped on an index out of bounds, a crash, and it now gives
each leaf its task's coming-in time in place of its processing time.

| | edit | failures by property |
|---|---|---|
| M1 | ★: the tasks queued by when they came in, not by processing time | P1 1237, P4 1607, P6 4948 |
| M2 | ★: the clock run on one unit for each task | P1 1142, P5 249, P6 4568 |
| M3 | set: the task run left in the set, another removed | P1 1718, P2 1718, P4 1785, P6 1718 |
| M4 | set: an idle clock set to the next task's time even when it has passed | P1 899, P6 899 |
| M5 | heap: sift_up raising a larger task over its parent | P1 1374, P4 1785, P6 1374 |
| M6 | heap: sift_down looking only at the left child | P1 448, P4 1127, P6 448 |
| M7 | segment: each leaf holding when its task came in, not its processing time | P1 1237, P4 1607, P6 1237 |
| M8 | segment: a task run put back with one more unit | P1 1699, P2 1699, P4 1742, P5 1101, P6 1699 |
| M9 | solution: the clock run on one unit too far for each task | P1 591, P5 417, P6 591 |
| M10 | solution: the tasks taken in by processing time, not by when they come in | P1 1618, P6 1618 |

## Benchmarks

The bench builds one list of 10^5 tasks once, each coming in at 1 to
10^6 and taking 1 to 10^4, and makes 50 calls of the ★ arm on its first
50000 to 99999 tasks, each run's length drawn from the checksum so far,
and folds each order into the checksum. Each call copies its run, a list
of two-number lists, as the arm takes its list by value; C, which has no
priority queue, writes the queue out as a binary heap, and copies each
task as its own two-number array, as LeetCode's C signature takes them.
It checks clean as first written. Every implementation prints `50 calls:
checksum 389402089`.

BENCHTAB

Measured by hand, best of three on a machine shared with a test run,
Kāra takes 0.91 s against Rust's 0.87 s (0.89 s with overflow checks
on), C's 1.5 s and Go's 3.5 s; Python takes 8.5 s.
