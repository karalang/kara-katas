# 2440. Create Components With Same Value

There is an undirected tree with `n` nodes labeled from `0` to `n - 1`.

You are given a **0-indexed** integer array `nums` of length `n` where
`nums[i]` represents the value of the `i`th node. You are also given a
2D integer array `edges` of length `n - 1` where `edges[i] = [ai, bi]`
indicates that there is an edge between nodes `ai` and `bi` in the tree.

You are allowed to **delete** some edges, splitting the tree into
multiple connected components. Let the **value** of a component be the
sum of **all** `nums[i]` for which node `i` is in the component.

Return *the **maximum** number of edges you can delete, such that every
connected component in the tree has the same value.*

```
nums = [6,2,2,2,6], edges = [[0,1],[1,2],[1,3],[3,4]]  ->  2
nums = [2], edges = []                                ->  0
```

**Constraints:** `1 <= n <= 2 * 10^4`; `nums.length == n`;
`1 <= nums[i] <= 50`; `edges.length == n - 1`; `edges[i].length == 2`;
`0 <= edges[i][0], edges[i][1] <= n - 1`; `edges` represents a valid
tree.

Deleting `k - 1` edges leaves `k` components, each then summing to
`total / k`, so `k` must divide the total. For one `k` the cuts are
forced: rooted anywhere, a subtree whose remaining sum reaches the target
must be cut off above, and one that passes it means `k` cannot be had.
So each divisor is checked in O(n), from `n` down, and the first that
fits is the answer, `k - 1`. The values are at least 1, so the total is
at most `10^6` and has at most 240 divisors.

## Approaches

| file | mechanism |
|---|---|
| `components.kara` ★ | the tree walked once in breadth-first order from node 0, each node's parent kept; for each `k` from `n` down dividing the total, the sums gathered in reverse order, children before parents, with no recursion. O(n d) |
| `components_dfs.kara` | a recursive depth-first search: each node returns what is left of its subtree's sum, 0 when it reaches the target and is cut, -1 when it passes it. O(n d) |
| `components_peel.kara` | leaves peeled from a queue by degree, as in a topological sort: a full leaf cut away, a lighter one passing its sum to its one remaining neighbour. No root is chosen. O(n d) |
| `components_count.kara` | counted once: every subtree's whole sum from one stack walk, and `k` components of sum `t` exist exactly when `k` subtrees sum to a multiple of `t`. No cut is simulated. O(n d) |
| `components_iter.kara` | iterators: the counts from `n` down by `rev` and `filter`, the first that fits by `find`, each fit a `fold` over the reverse order carrying the sums and a verdict. O(n d) |
| `components_solution.kara` | LeetCode's Rust template: the graph by `vec![vec![]; n]` with `usize` indices, a `fn dfs` nested in the method over `&Vec<..>` references with `usize::MAX` for the root's parent, and `(1..=n as i32).rev()`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's two examples; then `10^4`
nodes: a path of 1s, a path of 50s with a 1 at each end, a random tree
of 5s, a random tree of random values from 1 to 50, and a star of 2s
round a centre of 50; and 3000 random trees of 1 to 10 nodes, values
from 1 to 4, as a checksum and the total. The random trees join each
node to a random earlier one, shuffle the edges and write each either
way round. `components.py` mirrors the ★ arm and its output is
byte-identical, and the mirror was checked on 20000 random trees of 1
to 9 nodes against every set of edges deleted.

`check` first reports 15 errors on the template, and `karac fix`
carries it in one call, reporting 25 edits: the brackets of each
`Vec<..>`; each `&` dropped or written `ref`, on `&edges`, on the
parameters `&Vec<..>`, on `&g[u]` and on the arguments `&g` and `&nums`;
the `&` dropped from the pattern `&v`; the nested `fn dfs` moved above
the `impl`, since Kāra has no nested items and it captures nothing;
`vec![vec![]; n]` written `Vec.filled(n, Vec.new())`; `&&` written
`and`; `usize::MAX` written `usize.MAX`; `struct Solution;` given its
braces; and, once the template parses, the harness's `as i64` on the
`i64` the template returns. The casts `e[0] as usize`, the tuple `let
(a, b) = (..)`, `nums.iter().sum()` into an `i32` and `(1..=n as
i32).rev()` stand as Kāra.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every set of edges tried as the deleted ones, the components
left found by merging the ends of each edge kept, and the set counted
when every component has the same sum; the most edges in such a set is
the answer. No divisor of the total is formed and no subtree summed. It
checks 300 random trees of 1 to 8 nodes, values from 1 to 1, 2 or 3;
then 30 of 8 to 10 nodes, all 1 but two from 1 to 4; then 30 of 6 to 10
nodes, values 1 and 2. The trees stay small because the literal reading
tries every set of edges. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | the nodes renamed by a random permutation, each edge turned round and the edges shuffled: the same answer |
| P3 | every value times `k` from 2 to 4: the same answer |
| P4 | the answer plus one divides the total, and the answer is below `n` |
| P5 | two copies joined by an edge between their nodes 0: at least twice the answer plus one |
| P6 | each arm agrees with at least three of the other five |

P2 holds because the components do not depend on the names. P3 holds
because scaling every value scales every component's sum alike. P4
holds because `k` equal components divide the total, and a tree of `n`
nodes has `n - 1` edges. P5 holds because each copy can be cut as the
original is and the joining edge deleted too.

The differential prints `360 cases: checksum 642633630, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and tries every set of edges. On a failure it prints the
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
| M4 | ★: two components never tried | P1 48, P5 188, P6 48 |
| M5 | ★: each node passing up only its own value | P1 21, P2 15, P5 122, P6 21 |
| M6 | ★: a sum past the target cut | P1 76, P2 47, P3 102, P6 76 |
| M7 | dfs: a failed subtree added in | P1 57, P2 30, P3 68, P6 57 |
| M9 | dfs: every node its own component never tried | P1 109, P5 31, P6 109 |
| M11 | dfs: the children aiming one lower | P1 161, P2 16, P3 12, P5 342, P6 161 |
| M14 | peel: a neighbour queued at degree 0 | P1 91, P3 81, P6 91 |
| M15 | peel: a sum past the target cut | P1 20, P2 3, P5 7, P6 20 |
| M16 | peel: the target one higher | P1 122, P3 50, P5 255, P6 122 |
| M17 | count: only sums of exactly the target | P1 159, P5 360, P6 159 |
| M18 | count: one subtree short | P1 231, P3 97, P5 360, P6 231 |
| M19 | count: each node folding only its own value | P1 167, P2 104, P3 37, P4 56, P5 296, P6 167 |
| M22 | iter: the last count that fits | P1 36, P5 159, P6 36 |
| M23 | iter: the components counted, not the cuts | P1 159, P4 147, P5 159, P6 159 |
| M26 | iter: one passed up for each node | P1 40, P2 22, P3 52, P5 119, P6 40 |
| M28 | solution: a failed subtree cut instead | P1 87, P2 57, P3 80, P6 87 |
| M30 | solution: the components counted, not the cuts | P1 360, P4 289, P5 347, P6 360 |


P1 and P6 kill all seventeen, P5 thirteen, P3 nine, P2 eight and P4
three.

Fourteen are not kept. Eight fail exactly as a kept one: the ★ arm's
sum at the target never cut, the DFS arm's full subtree passed up, the
peel arm's full leaf passed on and the template's fewest components
first (M1, M8, M13, M27) as the count arm's only sums of exactly the
target (M17), each answering 0 for every tree; the ★ arm's every node
its own component never tried (M3) as the DFS arm's (M9); the count
arm's sums folded in the order taken (M20) as its each node folding only
its own value (M19); the count arm's fewest components first (M21) as
the iter arm's last count that fits (M22), both the fewest components
above one; and the template's sum past the target cut (M29) as the ★
arm's (M6). One fails apart from every kept one and was left out because
the template keeps its share already: the sum replaced by each child's
(M31).

Five survive, and are equivalent. Every piece cut off sums to exactly
the target, so what reaches the root, or the peel arm's last node, is
the total less a multiple of the target: a multiple itself, and at
least the node's own value, which is 1 or more, so never below the
target. That makes the ★ and iter arms' root left unchecked (M2, M24)
and the peel arm's last node never checked (M12) change nothing. The
DFS arm's one past the target allowed (M10) passes a sum of the target
plus one up as it is, and the parent it reaches then sums to at least
the target plus two, past what is allowed, or is the root and is not 0,
so it fails as -1 would. And the iter arm's every count tried at `n`
(M25) tries a target `total / n` rounded down when `n` does not divide
the total; components of exactly that sum would number more than `n`,
so it never fits.

## Verification

Every arm prints the same output as `components.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.8 to 2.4 s, and the
differential 1.5 s; under `karac __mir-llvm-asan` the differential
takes 1.1 s and under `karac run` 1.0 s. The DFS arm and the template
recurse once per node, 10^4 deep on the path cases, under every lane.

## Benchmarks

The bench builds 10 random trees of `2 * 10^4` nodes, the constraints'
largest, values from 1 to 50, once from its own generator. It then
makes 50 passes; each sets one value of every tree, so the total and
its divisors change and no answer can be carried from one pass to the
next, then answers every tree, folding the answer plus the pass into
the checksum. The bench uses the ★ arm, the breadth-first order and the
sums gathered in reverse, in all five languages. Every implementation
prints `50 passes over 10 trees of 2 * 10^4 nodes: checksum 977536881`.
Each answer builds its adjacency lists afresh, growable lists in every
language and in C a list per node grown by doubling with `realloc`.

BENCHTAB
