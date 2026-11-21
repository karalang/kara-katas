# 2392. Build a Matrix With Conditions

You are given a **positive** integer `k`. You are also given:

- a 2D integer array `rowConditions` of size `n` where `rowConditions[i]
  = [abovei, belowi]`, and
- a 2D integer array `colConditions` of size `m` where `colConditions[i]
  = [lefti, righti]`.

The two arrays contain integers from `1` to `k`.

You have to build a `k x k` matrix that contains each of the numbers
from `1` to `k` **exactly once**. The remaining cells should have the
value `0`.

The matrix should also satisfy the following conditions:

- The number `abovei` should appear in a **row** that is strictly
  **above** the row at which the number `belowi` appears for all `i`
  from `0` to `n - 1`.
- The number `lefti` should appear in a **column** that is strictly
  **left** of the column at which the number `righti` appears for all
  `i` from `0` to `m - 1`.

Return ***any** matrix that satisfies the conditions*. If no answer
exists, return an empty matrix.

```
k = 3, rowConditions = [[1,2],[3,2]], colConditions = [[2,1],[3,2]]
    ->  [[3,0,0],[0,0,1],[0,2,0]]
k = 3, rowConditions = [[1,2],[2,3],[3,1],[2,3]], colConditions = [[2,1]]
    ->  []
```

**Constraints:** `2 <= k <= 400`; `1 <= rowConditions.length,
colConditions.length <= 10^4`; `rowConditions[i].length ==
colConditions[i].length == 2`; `1 <= abovei, belowi, lefti, righti <=
k`; `abovei != belowi`; `lefti != righti`.

The rows and the columns are independent: each number gets its own row
and its own column, so a matrix exists exactly when the row conditions
and the column conditions each have a topological order, and the two
orders place each number.

## Approaches

| file | mechanism |
|---|---|
| `matrix.kara` ★ | Kahn's algorithm twice: the numbers with no condition left before them taken a `VecDeque` at a time, a number never taken meaning a cycle. O(k + conditions), and the k by k matrix |
| `matrix_dfs.kara` | depth-first search with three colours and an explicit stack of (number, next edge): the finishing order reversed, a number met while still on the path a cycle |
| `matrix_heap.kara` | Kahn's algorithm with a `PriorityQueue`, so the smallest free number goes first: the least topological order. O((k + conditions) log k) |
| `matrix_scan.kara` | no graph: each round scans the unplaced numbers for one no unplaced number must precede, checking every condition, and a round that finds none is a cycle. O(k^2 * conditions) at worst |
| `matrix_iter.kara` | ranks by iterators: each number's longest chain of conditions, relaxed a `fold` a round for k rounds, a chain still growing a cycle; the numbers ordered by `sort_by_key`, the matrix built by `map` and `collect` |
| `matrix_solution.kara` | LeetCode's Rust template: Kahn's algorithm in a nested `fn topo` returning `Option<Vec<usize>>`, a `VecDeque` collected from a filtered `1..=k`, both orders matched as a pair; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Answers are not unique, and the arms give different matrices, so every
arm prints what its matrix is rather than the matrix: `empty`, `valid`
when it is k by k, holds each of 1 to k once and 0 elsewhere and keeps
every condition, or `INVALID`. The same 6 lines: LeetCode's two
examples; no conditions; a chain one way down the rows and the other
way across; then `k = 400` with `10^4` conditions each way that agree
with one order, and the same with one column condition turned around to
close a cycle; then 3000 random cases of `k` from 2 to 12 with up to
`3k` conditions each way, a third of them drawn freely, counting the
empty answers and the valid ones. `matrix.py` mirrors the ★ arm and its
output is byte-identical, and the mirror was checked on 3000 random
cases of `k` up to 6 against every order of the numbers.

`check` first reports 18 errors on the template, and `karac fix`
carries it in one call, reporting 44 edits: `struct Solution;` given
its braces; `use std::collections::VecDeque;` deleted, `VecDeque` being
in the prelude; every `Vec<..>`, `Option<..>` and `VecDeque<..>` its
brackets; the nested `fn topo` moved above the `impl`, as it captures
nothing; `usize` made `i64`; the `&` of `&Vec<..>` made `ref`, and the
`&` of each `|&v|`, `for &v`, and `&row_conditions` argument dropped;
`Vec::with_capacity` written with a dot; and each `vec![..; n]` written
`Vec.filled`. The `while let`, the `match` on a pair of `Option`s with
`return` in an arm, `filter` and `collect` into a `VecDeque`, and the
`as` casts stand as Kāra.

The harness's examples are an array literal of tuples, one of them
`(2, [], [])`, bound as `let examples: Vec[(..)] = [..];`. Written with
`.to_vec()` after the literal, as an array is turned into a `Vec`
elsewhere, `check` refuses the `[]` with the internal "a type that
failed to check is not lowered yet" (B-2026-11-21-49).

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: a matrix exists when some order of 1 to k down the rows
keeps every row condition and some order across keeps every column
condition, each found by trying all `k!` orders. No graph. Each arm's
matrix is checked rather than compared. It checks 300 random cases of
`k` from 2 to 6, which the literal reading answers; then 30 of `k` up
to 60 with conditions that agree with an order; then 30 of `k` up to 60
with conditions drawn freely. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | `k` up to 6: a matrix exactly when the literal reading finds one |
| P2 | a matrix returned is k by k, holds 1 to k once each and 0 elsewhere, and keeps every condition |
| P3 | the conditions listed in reverse: a matrix exactly when before, and a valid one |
| P4 | the row and column conditions swapped: the same |
| P5 | every condition given twice: the same |
| P6 | each arm agrees with at least three of the other five on whether there is a matrix |

P3 and P5 hold because a condition's place in the list and how often it
is given change no order that keeps it, and P4 because rows and columns
are chosen the same way.

The differential prints `360 cases: checksum 307139692, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and tries every permutation. On a failure it prints the
first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: an edge never counted into its end | P1 60, P2 317, P3 317, P4 317, P5 317, P6 76 |
| M3 | ★: the columns from the row conditions | P1 12, P2 222, P3 220, P4 244, P5 222, P6 16 |
| M4 | ★: every number on the diagonal | P2 206, P3 204, P4 183, P5 206 |
| M9 | dfs: a finished number left on the path | P1 227, P5 14, P6 262 |
| M10 | dfs: each new number's first edge skipped | P1 32, P2 124, P3 132, P4 124, P5 39, P6 39 |
| M11 | dfs: the searches started from 2 | P1 202, P6 231 |
| M12 | heap: each edge taken off twice | P1 224, P2 6, P3 6, P4 6, P5 284, P6 259 |
| M13 | heap: the number popped pushed again | P1 121, P2 120, P3 120, P4 120, P5 120, P6 156 |
| M15 | heap: the rows upside down | P2 241, P3 241, P4 254, P5 241 |
| M19 | scan: a found number never marked | P1 20, P2 320, P3 320, P4 320, P5 320, P6 36 |
| M20 | scan: 1 found when nothing is | P1 60, P2 76, P3 76, P4 76, P5 76, P6 76 |
| M21 | scan: one number never placed | P1 248, P6 284 |
| M23 | iter: one round too few | P1 56, P3 19, P5 12, P6 56 |
| M24 | iter: the ranks from the highest | P2 276, P3 276, P4 276, P5 276 |
| M26 | iter: every number in the first column | P2 254, P3 254, P4 241, P5 254 |
| M30 | solution: k never queued at the start | P1 205, P6 234 |
| M31 | solution: the two orders swapped | P2 228, P3 228, P4 228, P5 228 |

P5 kills fourteen of the seventeen, P3 thirteen, and P1, P2, P4 and P6
twelve each. The edits split two ways. Those that misjudge whether an
order exists (M9, M11, M21, M30) fail only P1 and P6: they answer
"empty" for a matrix that exists, and every matrix they do return is
valid, so P2 to P5 hold. Those that return a matrix breaking a
condition (M4, M15, M24, M26, M31) fail only P2 to P5: every verdict
on whether there is a matrix is still right, so P1 and P6 hold. The
rest fail both ways. M23, one round too few, fails P1 on the cases its
missing round leaves unordered but P2 on none, since the rows it does
rank are ranked right.

Of the thirty-one, fourteen were not kept. An edge counted twice into
its end (M14), a number placed still blocking (M17), a rank never grown
(M22), an edge counted into its start (M27) and the ★ arm's number
freed one edge late (M2) all fail alike; a number on the path not seen
as a cycle (M7), a cycle let through (M25), a short order kept (M28)
and 1 found when nothing is (M20, kept) alike; every edge turned
around, the finishing order not reversed and the scan's number blocked
by what follows it (M5, M8, M18) as the ranks from the highest (M24,
kept); every column the first (M29) as every number in the first
column (M26, kept); and k never free at the start (M6) as k never
queued (M30, kept). The heap arm's first condition ignored (M16) fails
apart from every kept one and was left out to keep three to an arm.
The ★ arm's M2 was first a number freed one edge early: freed before
its last edge, a number can be queued again and again, and the queue
grew until the compiled run was killed for memory and the interpreted
one stopped with exit 101. A crash is not kept, so it was replaced by the number freed one edge late (M2).

## Verification

Every arm prints the same output as `matrix.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.91 to 5.1 s, except the scan
arm, which looks for a free number by scanning every number left each
round and takes 37.6 s. The differential takes 3.5 s there and 0.8 s
under `karac __mir-llvm-run`.

## Benchmarks

The bench builds 20 cases of `k = 200`, each with 4000 conditions each
way that agree with an order, once from the harness's generator, then
makes 500 passes, building every matrix and folding each number by
where it sits, with the ★ arm in all five languages; every language
runs the same Kahn's algorithm with each number's conditions in the
order given, so all five build the same matrices. Every implementation
prints `500 passes over 20 matrices of k = 200: checksum 680214059`.
C keeps the conditions as one flat array indexed by number and the
matrix as one flat block; the others build a list per number and a row
per row, afresh in each call.

BENCHTAB
