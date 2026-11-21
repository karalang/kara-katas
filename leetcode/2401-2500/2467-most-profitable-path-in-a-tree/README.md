# 2467. Most Profitable Path in a Tree

There is an undirected tree with `n` nodes labeled from `0` to `n - 1`,
rooted at node `0`. You are given a 2D integer array `edges` of length
`n - 1` where `edges[i] = [ai, bi]` indicates that there is an edge
between nodes `ai` and `bi` in the tree.

At every node `i`, there is a gate. You are also given an array of even
integers `amount`, where `amount[i]` represents:

- the price needed to open the gate at node `i`, if `amount[i]` is
  negative, or,
- the cash reward obtained on opening the gate at node `i`, otherwise.

The game goes on as follows:

- Initially, Alice is at node `0` and Bob is at node `bob`.
- At every second, Alice and Bob **each** move to an adjacent node.
  Alice moves towards some **leaf node**, while Bob moves towards node
  `0`.
- For **every** node along their path, Alice and Bob either spend money
  to open the gate at that node, or accept the reward. Note that:
  - If the gate is **already open**, no price will be required, nor
    will there be any cash reward.
  - If Alice and Bob reach the node **simultaneously**, they share the
    price/reward for opening the gate there. In other words, if the
    price to open the gate is `c`, then both Alice and Bob pay `c / 2`
    each. Similarly, if the reward at the gate is `c`, both of them
    receive `c / 2` each.
- If Alice reaches a leaf node, she stops moving. Similarly, if Bob
  reaches node `0`, he stops moving. Note that these events are
  **independent** of each other.

Return *the **maximum** net income Alice can have if she travels
towards the optimal leaf node*.

```
edges = [[0,1],[1,2],[1,3],[3,4]], bob = 3, amount = [-2,4,2,-4,6]  ->  6
edges = [[0,1]], bob = 1, amount = [-7280,2350]                      ->  -7280
```

**Constraints:** `2 <= n <= 10^5`; `edges.length == n - 1`; `edges`
represents a valid tree; `1 <= bob < n`; `amount.length == n`;
`amount[i]` is an even integer in the range `[-10^4, 10^4]`.

Bob's path to the root is fixed, the chain of parents from `bob`, so he
reaches the `t`th node on it at second `t`; Alice reaches every node at
its depth. A gate pays Alice all of its amount when she comes first,
half when they come together, and nothing when Bob came first, so the
answer is the best root-to-leaf sum of those gates.

## Approaches

| file | mechanism |
|---|---|
| `profit.kara` ★ | by levels: a breadth-first walk from 0 gives every node's parent and depth, Bob's seconds come from his parent chain, and each node's income is its parent's plus its gate, taken in the walk's order; the best leaf wins. O(n) |
| `profit_dfs.kara` | one depth-first walk: each call returns the best income below its node and the distance from its node down to Bob, which is the second he reaches it, so the gate is settled as the call returns. O(n), recursing as deep as the tree |
| `profit_distances.kara` | by distances: a breadth-first walk from 0 and one from Bob; a node is on Bob's path exactly when its two distances add to Bob's distance from 0, and each gate is settled alone from the two distances. O(n) |
| `profit_naive.kara` | one walk per leaf: Alice's path read off the parents, Bob's likewise, and the two walked second by second with a `Set` of the gates opened. O(leaves * depth) |
| `profit_iter.kara` | iterators: each level's unvisited children found by `filter`, Bob's seconds by `enumerate` over his parent chain collected into a `Map`, each gate by `map` with a guarded `match` on that map, and the best leaf by `filter` and `max`. O(n) |
| `profit_solution.kara` | LeetCode's Rust template: the ★ arm's walk over `usize` indices, `usize::MAX` marking a node not yet reached, Bob's seconds from a `loop` up his parents with `i32::MAX` off his path; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 11 lines: LeetCode's two examples; then four
more, Bob meeting Alice on a node, Bob a child of the root, a gate
shared at a half, and every gate a cost; then three of `10^5` nodes, the
constraints' largest, a path with Bob at its far end, a star with Bob on
a leaf, and a random tree, and a deep random tree of `10^4`, each node
joined to one of the three before it; and 3000 random trees of 2 to 40
nodes, as a checksum. The deep tree is kept to `10^4` nodes for the
naive arm, whose walks are as long as the tree is deep, and the dfs arm
recurses `10^5` deep on the path. `profit.py` mirrors the ★ arm and its
output is byte-identical, and the mirror was checked on 20000 random
trees of 2 to 9 nodes against both walks simulated second by second for
every leaf.

`check` first reports 12 errors on the template, and `karac fix`
carries it in one call, reporting 23 edits: the brackets of `Vec<..>`,
five edits; `&edges`, `&adj[u]` and `&order` written `ref`; the `&` of
the patterns `&v` and `&u` dropped; `usize::MAX`, `i32::MAX` and
`i32::MIN` written with `.`, four edits; `&&` written `and`; the seven
`vec!`s written `Vec.filled(..)`, `Vec.new()` and a list; and `struct
Solution {}` added. `as usize`, `usize.MAX`, `0usize`, `0i32`, and `loop`
with `break` stand as Kāra.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: Bob's path found by a search from `bob` to 0 over the edges,
then every way Alice can walk down from 0 to a leaf tried, second by
second, with Bob a step along his path each second and a set of the
gates opened so far carried with her; a gate both reach together is
halved. No parent, depth or distance array stands in for the walk. It
checks 300 random trees of 2 to 10 nodes, then 60 of up to 14, with even
amounts from -5000 to 5000. All 360 are drawn before any arm answers,
each with a random renaming.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | every edge split by a new node of amount 0, the nodes but 0 then renamed: the same answer |
| P3 | every amount doubled: the answer doubled |
| P4 | a leaf of amount 0 hung on node 0: the larger of the answer and node 0's amount |
| P5 | every amount on Bob's path made 0: the best leaf's sum of the amounts down to it |
| P6 | each arm agrees with at least three of the other five |

P2 holds because splitting every edge doubles the second at which each
of them reaches each old node, so who comes first is unchanged, and the
new nodes pay nothing and are no leaves. P3 holds because every gate's
share is linear in its amount, the amounts being even. P4 holds because
Alice reaches node 0 first, Bob never at second 0, so the new leaf's
path pays node 0's amount whole. P5 holds because with nothing on Bob's
path he changes no gate.

Two properties of the first run killed no mutant and were replaced: P2
was every node but 0 renamed and the edges shuffled, and P5 bounded the
answer between the best leaf's sum of its costs and of its rewards.
No edit of that run failed either one.

The differential prints `360 cases: checksum 88183079, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and tries every walk with a set of the gates opened. On a
failure it prints the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: Alice two steps a second | P1 197, P2 35, P4 48, P5 104, P6 197 |
| M2 | ★: Bob a second late from the start | P1 266, P2 156, P6 266 |
| M3 | ★: a gate shared a second late | P1 265, P2 156, P6 265 |
| M7 | dfs: Bob no farther for a step up | P1 360, P4 114, P6 360 |
| M8 | dfs: a costly rest left unwalked | P1 117, P5 82, P6 117 |
| M10 | dfs: every child at the same second | P1 266, P6 266 |
| M12 | distances: every node on the path of Bob | P1 146, P5 148, P6 146 |
| M14 | distances: a shared gate quartered | P1 107, P3 62, P6 107 |
| M15 | distances: the distances of Bob from the root | P1 287, P5 33, P6 287 |
| M17 | naive: Alice walking up from the leaf | P1 323, P4 70, P6 323 |
| M18 | naive: no gate opened by Bob | P1 258, P6 258 |
| M19 | naive: every gate taken whole | P1 110, P6 110 |
| M22 | iter: a shared gate lost | P1 109, P6 109 |
| M24 | iter: the root among the leaves | P1 58, P5 40, P6 58 |
| M26 | iter: each income its own gate | P1 360, P4 131, P5 119, P6 360 |
| M27 | solution: Bob two steps a second | P1 151, P6 151 |
| M29 | solution: every node a leaf | P1 92, P2 48, P5 82, P6 92 |

P1 and P6 kill all seventeen, P5 seven, P2 and P4 four each, and P3
one, the distances arm's shared gate quartered (M14), whose rounding
P3's doubled amounts change.

Fourteen are not kept. Ten fail exactly as a kept one: the ★ and dfs
arms' shared gate taken whole (M4, M9) as the naive arm's every gate
taken whole (M19); the ★ arm's root a leaf when it has one child (M5)
as the iter arm's root among the leaves (M24); the ★ arm's gate Bob
opened still paying (M6) as the naive arm's no gate opened by Bob
(M18); the dfs and iter arms' Bob a second late (M11, M23) as the ★
arm's (M2); the distances arm's income taken from below (M13) as the
iter arm's each income its own gate (M26), each answering the best leaf
gate alone; the naive arm's Bob opening first and the template's
shared gate lost (M21, M28) as the iter arm's (M22); and the iter
arm's every node at second 0 (M25) as the dfs arm's every child at the
same second (M10). Three fail apart from every kept one: the distances
arm's node of two edges a leaf (M16), and the template's Bob starting a
step along and gate lost a second before Bob (M30, M31). The naive
arm's leaf 1 never tried (M20) ends in an overflow: in a tree whose
only leaf is node 1 it answers `i64.MIN`, and P3 doubles it. Every
edit is killed by some check.

## Verification

Every arm prints the same output as `profit.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 3.8 to 8.3 s, the naive arm 27.7 s, and the differential 1.3 s; under `karac __mir-llvm-asan` the arms take 1.2 to 4.8 s and the differential 1.1 s, and under `karac run` the differential takes 0.9 s.

## Benchmarks

The bench builds 10 random trees of `10^4` nodes once from its own
generator, each node joined to an earlier one, with even amounts from
`-10^4` to `10^4`, then makes 140 passes; each moves every tree's Bob
and sets one of its amounts from the checksum so far, so no answer
carries over, then answers it, folding the answer plus the pass into
the checksum. The bench uses the ★ arm in all five languages, with
adjacency lists of growable vectors in Kāra, Rust, Go and Python; C has
none, and packs the lists into one array by a counting sort. Every
implementation prints `140 passes over 10 trees of 10^4: checksum
786411425`.

BENCHTAB
