# 2476. Closest Nodes Queries in a Binary Search Tree

You are given the `root` of a **binary search tree** and an array
`queries` of size `n` consisting of positive integers.

Find a **2D** array `answer` of size `n` where `answer[i] = [min_i,
max_i]`:

- `min_i` is the **largest** value in the tree that is smaller than or
  equal to `queries[i]`. If such a value does not exist, add `-1`
  instead.
- `max_i` is the **smallest** value in the tree that is greater than or
  equal to `queries[i]`. If such a value does not exist, add `-1`
  instead.

Return *the array* `answer`.

```
root = [6,2,13,1,4,9,15,null,null,null,null,null,null,14], queries = [2,5,16]  ->  [[2,2],[4,6],[15,-1]]
root = [4,null,9], queries = [3]                                              ->  [[-1,4]]
```

**Constraints:** the number of nodes is in `[2, 10^5]`;
`1 <= Node.val <= 10^6`; `n == queries.length`; `1 <= n <= 10^5`;
`1 <= queries[i] <= 10^6`.

The tree is not balanced, so a walk down it per query can take `n`
steps; an in-order walk reads its values ascending once, and each query
is then a bisection.

## Approaches

| file | mechanism |
|---|---|
| `closest.kara` ★ | in order, then by bisection: the in-order values in a list, and a bisection by hand for the first value at least the query; the value there is the smallest at least it, and the one before the largest at most it, unless the first is the query itself. O(n + q log n) |
| `closest_walk.kara` | down the tree: each query walks from the root, left of a larger value and right of a smaller, keeping the last value seen on each side; an equal value answers both. O(q h), `h` the height |
| `closest_ordered.kara` | an ordered map: every value put in a `SortedMap` by a pre-order walk, each query answered by its `floor` and `ceiling`. O((n + q) log n) |
| `closest_stack.kara` | an explicit stack: the in-order walk without recursion, then each query by the place it would go. Written with Rust's `binary_search` matched on `Ok` and `Err`; Kāra's returns an `Option`, and `karac fix` carried it to `partition_point` and a test of the value there. O(n + q log n) |
| `closest_iter.kara` | iterators: the in-order values gathered by recursion that joins the two sides' lists, then the queries answered by `map`, each by `partition_point` and `get`. O(n + q log n) |
| `closest_solution.kara` | LeetCode's Rust template: `Option<Rc<RefCell<TreeNode>>>` and `Vec<i32>` in, `Vec<Vec<i32>>` out; an `inorder` nested in the method walks through `borrow()` into a `&mut Vec<i32>`, and the queries map through `partition_point` to `vec![min, max]`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 7 lines: LeetCode's two examples; then two
more, two nodes asked below, on, between and above them, and a left
path asked below, on and above it; then a search tree of `10^5` nodes,
the constraints' largest, from 1 to `10^6`, built by inserting in a
random order and asked `10^4` random values, and a path of 2000 nodes
asked `10^4`, each as a checksum of its answers; and 2000 random trees
of 2 to 40 nodes from 1 to 60, each asked 1 to 10 values from 1 to 61,
as a checksum. The queries stop at `10^4`, below the constraints'
`10^5`, and the path at 2000 nodes, because the walk arm is O(q h).
`closest.py` mirrors the ★ arm and its output is byte-identical, and
the mirror was checked on 20000 random trees of 2 to 15 nodes against
the largest and smallest values on each side of every query.

`check` first reports 19 errors on the template, and `karac fix`
carries it in one call, reporting 38 edits. The two `use` lines go;
`Rc<RefCell<TreeNode>>` becomes the `TreeNode` handle, declared a
`shared struct`, and `let n = n.borrow();` goes with it; the nested
`inorder` moves above the `impl`, since Kāra has no nested items; the
generic brackets of `Option<..>` and `Vec<..>`; the `&` on each
parameter and argument goes, and `&mut` becomes `mut ref` on the
parameter and `mut` on the argument; the `&` in each closure's pattern
goes; `&&` becomes `and`; `Vec::new` takes a `.`; `vec![min, max]`
becomes `[min, max]`; and `struct Solution;` is given its braces. The
`i32` values, the method chain over `queries` and `partition_point`
stand as Kāra.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: for each query, every node visited breadth first, keeping
the largest value at most the query and the smallest at least it, -1
where there is none. No order of the tree is used. It checks 360
random search trees, each built by inserting distinct values in a
random order: 300 of 2 to 12 nodes from 1 to 30, asked 1 to 6 values
from 1 to 31, then 60 of up to 30 nodes from 1 to 100, asked up to 12
from 1 to 101. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answers are the literal reading's |
| P2 | the tree mirrored, every value `v` written `1000 - v` and every query `q` asked as `1000 - q`: each pair swapped and written the same way, a -1 kept |
| P3 | every value of the tree asked: each answered by itself twice |
| P4 | every value `v` written `2v` and every query `q` asked as `2q + 1`: the largest at most it twice the one for `q`, and the smallest at least it twice the literal reading's for `q + 1` |
| P5 | 999 inserted: every -1 that stood for the smallest at least a query becomes 999, and nothing else changes |
| P6 | each arm agrees with at least three of the other five |

P2 holds because mirroring a search tree and writing `1000 - v` keeps it
a search tree, and the largest value at most `q` becomes the smallest
at least `1000 - q`. P4 holds because the odd query `2q + 1` equals no
doubled value, so its largest at most is the double of the largest at
most `q` and its smallest at least the double of the smallest above
`q`; it is the one property where an equal value never occurs. P5 holds because every query is below 999, so the
new value is only ever the smallest at least a query, and only where
there was none.

P4 first reversed the queries and asked for the answers reversed, and it
killed no mutation: every arm answers each query on its own. The odd
queries over doubled values replaced it.

The differential prints `360 cases: checksum 608651039, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and takes the `max` and `min` of the values on each side
of every query. On a failure it prints the first ten and then the count
by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the walk pre-order | P1 329, P2 358, P3 342, P4 290, P5 96, P6 329 |
| M5 | ★: the bisection stopped a place short | P1 269, P2 320, P3 360, P4 295, P5 174, P6 269 |
| M6 | ★: the floor the value two before | P1 271, P2 318, P4 157, P6 271 |
| M7 | walk: an equal value not stopping | P1 184, P2 184, P3 360, P4 114, P5 81, P6 184 |
| M8 | walk: right of a smaller value, floor kept | P1 329, P2 348, P4 184, P6 329 |
| M9 | walk: left of a larger value, ceiling kept | P1 326, P2 348, P4 343, P5 348, P6 326 |
| M12 | ordered: floor for both | P1 348, P2 348, P4 360, P5 105, P6 348 |
| M13 | ordered: ceiling for both | P1 348, P2 348, P4 184, P5 132, P6 348 |
| M16 | ordered: the root not gathered | P1 313, P3 360, P4 247, P5 173, P6 313 |
| M19 | stack: the last value never a ceiling | P1 102, P2 159, P4 120, P5 195, P6 102 |
| M20 | stack: the first place past equal values | P1 184, P2 184, P3 360, P6 184 |
| M21 | stack: the stack walked from the root down only | P1 309, P2 351, P3 342, P4 270, P6 309 |
| M22 | iter: the right side read before the left | P1 360, P2 66, P3 360, P4 343, P5 360, P6 360 |
| M23 | iter: the ceiling read a place late | P1 346, P2 348, P3 360, P4 346, P5 132, P6 346 |
| M24 | iter: the right side dropped | P1 316, P2 351, P3 345, P4 278, P5 270, P6 316 |
| M29 | solution: the last value never a max | P1 130, P2 193, P3 360, P4 120, P5 211, P6 130 |
| M30 | solution: min and max swapped | P1 348, P4 360, P5 196, P6 348 |

P1 and P6 kill all seventeen, P4 sixteen, P2 fifteen, P5 thirteen, and
P3 ten.

Fourteen are not kept. Seven fail exactly as a kept one: the ★ arm's
first place above the query, the ordered arm's query one up and the
iter arm's first place past equal values (M2, M15, M25) as the stack
arm's first place past equal values (M20), each wrong only on a query
equal to a value; the ★ arm's last value never a ceiling (M4) as the
template's (M29); and the ordered arm's right side not gathered, the
stack arm's right side never taken and the template's right side never
walked (M14, M17, M31) as the iter arm's right side dropped (M24).
Four fail alike, apart from every kept one: the ★ and iter arms' equal
value never its own floor, the walk arm's equal value its ceiling only
and the template's equal value never its own min (M3, M26, M11, M28).
Two fail apart from every kept one, their arms having three kept
already or the template its two: the walk arm's sides swapped (M10) and
the template's walk pre-order (M27), which fails a few checks other
than the ★ arm's (M1). The stack arm's floor at the place itself (M18)
ends with an index out of bounds once the place is past the end. Every
edit is killed by some check.

Two edits were replaced before this table was drawn: the iter arm's
root put first, which `check` refuses, its `[n.val].to_vec()` an `i32`
list where an `i64` one is wanted, and its floor the place itself,
which crashes as M18 does.

## Verification

Every arm prints the same output as `closest.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 4.4 to 7.1 s, the walk arm 22.2 s, and the differential 2.2 s; under `karac __mir-llvm-asan` the arms take 1.0 to 1.6 s and the differential 1.0 s, and under `karac run` the differential takes 0.7 s.

## Benchmarks

The bench builds 10 random search trees of `10^4` nodes once from its
own generator, each by inserting distinct values from 1 to `10^6` in
the order drawn, then makes 220 passes; each asks every tree 1000
values stepped from the checksum so far, so no answer carries over,
folding every answer and the pass into the checksum. The bench uses the
★ arm in all five languages, the in-order walk recursive in each.
Every implementation prints `220 passes over 10 trees of 10^4: checksum
430064066`.

BENCHTAB
