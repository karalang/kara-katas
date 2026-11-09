# 2003. Smallest Missing Genetic Value in Each Subtree

There is a family tree rooted at `0` of `n` nodes numbered `0` to `n - 1`.
You are given a 0-indexed integer array `parents`, where `parents[i]` is the
parent of node `i`. Since node `0` is the root, `parents[0] == -1`. There
are `10^5` genetic values, each an integer in `[1, 10^5]`. You are given a
0-indexed integer array `nums`, where `nums[i]` is a distinct genetic value
of node `i`. Return an array `ans` of length `n` where `ans[i]` is the
smallest genetic value that is missing from the subtree rooted at node `i`.
The subtree rooted at `x` contains `x` and all of its descendants.

```
parents = [-1,0,0,2],         nums = [1,2,3,4]          ->  [5,1,1,1]
parents = [-1,0,1,0,3,3],     nums = [5,4,6,2,1,3]      ->  [7,1,1,4,2,1]
parents = [-1,2,3,0,2,4,1],   nums = [2,3,4,5,6,7,8]    ->  [1,1,1,1,1,1,1]
```

**Constraints:** `n == parents.length == nums.length`; `2 <= n <= 10^5`;
`0 <= parents[i] <= n - 1` for `i != 0`; `parents[0] == -1`; `parents`
represents a valid tree; `1 <= nums[i] <= 10^5`; each `nums[i]` is distinct.

A subtree that does not hold the value 1 answers 1. Only the nodes on the
chain from the node holding 1 up to the root hold it, so every other node
answers 1, and up that chain the subtrees only grow, so the answer only
climbs.

## Approaches

| file | mechanism |
|---|---|
| `genetic.kara` ★ | up the chain from the node holding 1, a recursive DFS marks each new subtree's values once (nodes already visited are skipped), and the smallest unmarked value climbs. O(n) |
| `genetic_stack.kara` | the ★ walk with an explicit stack, and the chain drawn by `successors`. O(n) |
| `genetic_merge.kara` | every node's values in a `Set`, merged smaller into larger in reverse BFS order (`Option.take`, `swap`); a node's answer starts at its children's largest and climbs while its set holds it. O(n log² n) |
| `genetic_euler.kara` | preorder numbers from an iterative DFS make each subtree a run `tin[u] ..= tout[u]`; a value is in the subtree when its node's number falls in the run. O(n) |
| `genetic_bfs.kara` | a `VecDeque` BFS from each ancestor that skips the child the walk came from, values gathered in a `Set`, no visited marks. O(n) |
| `genetic_solution.kara` | LeetCode's Rust template (`impl Solution`, `Vec<i32>`, a nested recursive `fn dfs`, `usize` indices, `match` on `position`), carried by `karac fix` in six rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: the answers for LeetCode's three
examples and four more; then the sum and a checksum of the answers for 2000
trees of 1 to 12 nodes, and for 8 trees of 20000 nodes (paths, bushy trees
and the cases in between, with and without a value above `n`).
`genetic.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: for each node, the nodes whose chain of parents
reaches it, then the smallest positive value missing from theirs. It checks
1500 trees of 1 to 14 nodes, each parent among the 1 to 5 nodes before it,
the values a shuffle of `1..n + extra` for `extra` up to 2. Every random
choice of a problem (the tree, the values, a renumbering) is drawn before
any arm answers.

| | property |
|---|---|
| P1 | each answer is the statement read literally |
| P2 | the nodes renumbered (the root kept at 0) renumber the answers |
| P3 | a parent's answer is at least each child's |
| P4 | a node off the chain from the node holding 1 to the root answers 1 |
| P5 | the root answers the smallest positive value missing from all of `nums` |
| P6 | each arm agrees with at least three of the other five on every node |

The differential prints `1500 problems: checksum 475751248, 54000 checks
over 6 arms: 0 failures` under every lane in Verification. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Thirty edits to the differential, five to each of its arms, each run
under `karac __mir-run` and `karac __mir-llvm-run`. Seventeen are kept,
three to each Kāra arm and two to the Rust arm. All thirty are killed, each fails the same way under both
backends, none by a crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the chain stopped below the root | P1 1285, P3 1011, P5 1285, P6 1285 |
| M2 | ★: a child's subtree left unmarked after the first | P1 496, P2 265, P5 496, P6 496 |
| M3 | ★: the answer stepped once too far | P1 1285, P5 1285, P6 1285 |
| M4 | stack: the stack's children pushed only at the chain node | P1 734, P5 734, P6 734 |
| M5 | stack: the chain's last step never taken | P1 1011, P3 1011, P5 1011, P6 1011 |
| M6 | stack: only the first two links of the chain | P1 695, P3 695, P5 695, P6 695 |
| M7 | merge: a child's answer taken as one more than it is | P1 1243, P4 1089, P5 966, P6 1243 |
| M8 | merge: the first child skipped | P1 1160, P2 287, P3 873, P5 1160, P6 1160 |
| M9 | merge: the climb stopping after one step | P1 959, P5 889, P6 959 |
| M10 | euler: the run's start one past the node | P1 1285, P5 947, P6 1285 |
| M11 | euler: the clock not moved for a child | P1 863, P6 863 |
| M12 | euler: the last child skipped | P1 695, P2 183, P6 695 |
| M13 | bfs: the chain climbed two links at a time | P1 1011, P3 1011, P5 587, P6 1011 |
| M14 | bfs: the present set cleared at every step | P1 592, P5 592, P6 592 |
| M15 | bfs: the node holding 1 taken as the last with value 1 or 2 | P1 165, P2 270, P6 165 |
| M16 | rust: only children numbered above their parent followed | P2 764 |
| M17 | rust: a node off the chain answering 0 | P1 1365, P4 1365, P5 215, P6 1365 |

P1 and P6 kill sixteen, P5 thirteen, P2 five, P3 five and P4 two. P4
sees M7, the one edit that lets an answer above 1 reach a node off the
chain, and M17, which changes the answer every arm starts with: every other
arm's edit acts on the chain itself, and off it each arm leaves the 1 it
started with. P2 sees the edits that depend on which child comes first
(M2, M8, M12), which node is found first (M15), or how the nodes are
numbered (M16). M16 is the only edit P2 alone kills: every drawn parent
comes before its child, so a child numbered below its parent appears only
once the nodes are renumbered. P3 sees the
edits that cut the chain short, leaving a parent at 1 above a child that
climbed.

The other ten fail as a kept one does, or with a signature of their own
that adds nothing. The ★ arm's node 0 left unmarked and the merge arm's
own value left out fail alike; the ★ arm's largest two values never
marked, the stack arm's value cap one too low and the BFS arm's values from
`n` up left out fail alike; the merge arm's smaller set kept and the Euler
arm's run ending at its own number fail alike. The Euler arm reading the
chain from the root's child fails as M1, the stack arm's own value left out
as M10, and the BFS arm skipping every ancestor's children with counts of
its own. Of the Rust arm's other three, the chain stopped below the root
fails as M1, and the walk started at the root and the last three values
left unmarked each with counts of their own.

Seven first drafts survived every check or did not count, and were
replaced. Five are equivalent: the ★ arm restarting the missing value at 1
per node (the marks only grow, so it climbs back to the same place), the
stack arm never setting `visited` (a tree has no cycles, so the stack
still ends), the merge arm ignoring its children's best (the set holds
every child's values, so climbing from 1 lands at the same place), the BFS
arm not skipping the child it came from, and the BFS arm never updating
`from` (in both, values seen again go into a `Set` that already holds
them). One crashed: the merge arm's order walked forward takes a child's
set before it exists, and `unwrap` fails. One was refused by the checker:
the stack arm's chain as `chain.iter().skip(1)` makes `u` a `ref i64`, so
the stack becomes a `Vec[ref i64]`, and the items `filter` adds to it
borrow what the filter borrows, its predicate's `visited` included
(core-semantics §5.4, "Items borrow what the receiver borrows"); writing
`visited` while the stack lives is then E0516. That is the rule as written,
not a gap: no body-dependent precision is allowed.

## Verification

Every arm prints the same output as `genetic.py`
under `karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`,
and `karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
every arm and the differential. `karac check --output=json` reports
nothing on any of them. Under `karac __mir-run` the arms take 0.97 s (★)
to 2.07 s (merge) and the differential 1.01 s, before the Rust arm
joined; on a debug karac at kara 7a9ac8e23f the Rust arm takes 5.1 s and
the six-arm differential 4.0 s.

The five arms were written in Kāra and checked clean. The Rust arm was
written as LeetCode's Rust template. `karac fix` carries it in six rounds
(44, 2, 9, 2, 1 and 1 edits) to two errors it has no fix for:
`Vec.filled(n, 1)` takes `Vec[i64]` on the spot, so the `Vec[i32]` return
is refused where `ans` is returned and where it returns early. Rust types
that literal `i32` from its later uses; design.md §8 says Kāra's literals
default last too. B-2026-11-07-3 made them do so (kara 87e598fee9) for a
let, an operand and a `Vec` push, but not for the element of a
`Vec.filled(n, 1)` that a return fixes; B-2026-11-08-57 made that case
fixed by its use too (kara 8da3c36f75), and the arm now checks clean with
no further round and passes every lane.
The last round's edit had no fix before this kata: `(nums[u] as usize) <
seen.len()`, with `nums` a `Vec[i32]`, was refused for mixing `usize` and
`i64` with nothing to apply, since the fix that drops a redundant `as
usize` only knew an `i64` operand. A narrower integer's `as usize` now
becomes `as i64` in one edit, and an `i64`'s is still dropped
(kara c2c1c98fa5, `tests/kata_2003_check_gaps.rs`).

## Benchmarks

The bench builds 40 trees of 20000 nodes once in all five languages (each
parent among the 2, 5, 50 or 20000 nodes before it, half with a value above
`n`) and runs the ★ arm on each 25 times: 1000 calls, 20 million nodes
marked. Every implementation prints `1000 calls: sum 74205125, checksum
9207764`. Every language allocates the children lists, the marks and the
answer per call, as the Kāra program does, and marks recursively.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with kara `64bba595f2` on LLVM 22:

| | time | median |
|---|---|---|
| Rust (`rustc -O`) | 1.235 to 1.371 s | 1.284 s |
| C (`clang -O3`) | 1.212 to 1.406 s | 1.290 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.263 to 1.368 s | 1.298 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 1.273 to 1.360 s | 1.307 s |
| Kāra (`karac build`) | 1.242 to 1.452 s | 1.320 s |
| Go | 1.270 to 1.461 s | 1.341 s |
| Python | 18.3 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`, the
sequential lane. A plain `karac build` parallelizes nothing here: its user
time (1.301 s) is not above its real time (1.320 s).

The sequential Kāra program is 1.01x Rust under overflow checks and 1.01x
C.