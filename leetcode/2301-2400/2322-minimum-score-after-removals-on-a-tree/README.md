# 2322. Minimum Score After Removals on a Tree

There is an undirected connected tree with `n` nodes labeled from `0`
to `n - 1` and `n - 1` edges.

You are given a **0-indexed** integer array `nums` of length `n` where
`nums[i]` represents the value of the `i`th node. You are also given a
2D integer array `edges` of length `n - 1` where `edges[i] = [ai, bi]`
indicates that there is an edge between nodes `ai` and `bi` in the
tree.

Remove two **distinct** edges of the tree to form three connected
components. For a pair of removed edges, the following steps are
defined:

1. Get the XOR of all the values of the nodes for **each** of the three
   components respectively.
2. The **difference** between the **largest** XOR value and the
   **smallest** XOR value is the **score** of the pair.

- For example, say the three components have the node values: `[4,5,7]`,
  `[1,9]`, and `[3,3,3]`. The three XOR values are `4 ^ 5 ^ 7 = 6`,
  `1 ^ 9 = 8`, and `3 ^ 3 ^ 3 = 3`. The largest XOR value is `8` and
  the smallest XOR value is `3`. The score is then `8 - 3 = 5`.

Return *the **minimum** score of any possible pair of edge removals on
the given tree*.

```
nums = [1,5,5,4,11], edges = [[0,1],[1,2],[1,3],[3,4]]          ->  9
nums = [5,5,2,4,4,2], edges = [[0,1],[1,2],[5,2],[4,3],[1,3]]   ->  0
```

**Constraints:** `n == nums.length`; `3 <= n <= 1000`; `1 <= nums[i]
<= 10^8`; `edges.length == n - 1`; `edges[i].length == 2`; `0 <= ai,
bi < n`; `ai != bi`; `edges` represents a valid tree.

Rooted at node 0, every edge joins a node to its parent and cuts off
that node's subtree, so a pair of edges is a pair of nodes other than
the root. With each subtree's XOR known, the three parts of a pair
`a`, `b` are `xor[b]`, `xor[a] ^ xor[b]` and the rest when `a` is
above `b`, and `xor[a]`, `xor[b]` and the rest when neither is above
the other; entry and exit times from one walk tell which. O(n^2), about
`5 * 10^5` pairs.

## Approaches

| file | mechanism |
|---|---|
| `tree.kara` ★ | a recursive `visit` through `mut ref` tables of subtree XORs and entry and exit times, then every pair of nodes from 1 with the ancestor test by times |
| `tree_naive.kara` | every pair of edges taken out in turn, the three parts found by a flood fill with a stack over the edges left, each part's XOR added up by label. O(n^3) |
| `tree_parents.kara` | no recursion: a breadth-first order gives parents and depths, the XORs are added up in that order backwards, and the ancestor test climbs a closure from the deeper node to the other's depth |
| `tree_sets.kara` | each node's subtree gathered into a `Set[i64]` by the walk back up, so the ancestor test is a `contains`. O(n^2) space |
| `tree_iter.kara` | the walk `filter`s a node's neighbours to its children and keeps each node's span as a tuple; every pair from `flat_map`, `map`ped to its score over an array of the three parts, and the `min` |
| `tree_solution.kara` | LeetCode's Rust template: `i32` values, a `dfs` nested in the method over `&Vec<Vec<usize>>` and four `&mut` tables, `usize` nodes and `usize::MAX` for no parent; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 6 lines: LeetCode's two examples; a path of
three; a star of six; a random tree of 200 nodes with values up to
`10^8`; then 500 random trees of 3 to 15 nodes with values up to 30,
with a checksum and the scores in all. `tree.py` mirrors the ★ arm and
its output is byte-identical.

`karac fix` carries the template in one call, reporting 63 edits.
`check` first offers 49 edits: `struct Solution;` to `struct Solution
{}`; the brackets of every `Vec<..>` in the method, `dfs` and the
harness's wrapper; `&edges`,
`&g[u]` and the two `&Vec` parameters to `ref`, and the four `&mut` to
`mut ref`; the pattern `&v` to `v`, and the `&x` of the wrapper's two
closures to `x`; the six `&` at the outer call to `dfs` dropped;
`usize::MAX` and `i32::MAX` to `.MAX`; the two `&&` to `and`; and, in
the wrapper, `Solution::` to `Solution.`. The other fourteen follow from
those: the nested `fn dfs`, which captures nothing, moved above `impl
Solution`, one edit to write it there and one to delete it here; the
`ref` on its two read-only parameters dropped, since a bare parameter
already borrows; `mut` written before the four tables at the call
inside `dfs`; the four `vec!` tables to `Vec.filled`, and the inner
`vec![]` to `Vec.new()`; and the wrapper's `as
i64` on the `i32` answer dropped. The `usize` nodes, `as usize` and
`usize.MAX` stand as Kāra.

The template was first written as a Rust user might, with `let (x, y,
z);` and each of the three branches assigning the three. Kāra allows a
declaration without a value only for a single name with its type
(`let x: T;`), and `karac check` says the `let` needs a type
annotation; written with one, `let (x, y, z): (i32, i32, i32);`, it is
then refused for binding a pattern. The first message should be the
second, which ledger row B-2026-11-18-91 records; `karac fix` applies its other
51 edits and stops there. The template above is the same code with an
`if` that yields the three as a tuple.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every pair of distinct edges taken out, each node labelled
with the least node it can still reach, by passing labels along the
edges left until none changes, the values XORed by label in a
`SortedMap`, and the largest XOR less the smallest; the answer is the
least of those. No rooting and no subtrees. It checks 300 random trees
of 3 to 15 nodes with values up to 30; then 30 paths of 3 to 15 nodes
with values up to 8; then 30 trees of up to 60 nodes with values up to
`10^8`. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | the answer is at least 0 and below the least power of two above every value |
| P3 | every node `i` renamed `n - 1 - i`: the same answer |
| P4 | every edge written the other way round, and the edges in reverse order: the same answer |
| P5 | every value doubled: the answer doubled |
| P6 | each arm agrees with at least three of the other five |

P3 moves the root: every arm hangs the tree from node 0, so after the
renaming it hangs from the node that was `n - 1`.

The differential prints `360 cases: checksum 875112434, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that
builds the same cases and finds the parts with a union-find. On a
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
| M1 | ★: a subtree's XOR not taken into its parent | P1 312, P3 292, P6 312 |
| M5 | ★: the clock never moved | P1 191, P3 229, P6 191 |
| M6 | ★: the smaller of two parts for the least | P1 228, P3 152, P6 228 |
| M7 | naive: the second edge left in | P1 334, P4 33, P6 334 |
| M8 | naive: each edge walked one way only | P1 290, P3 302, P4 301, P6 290 |
| M9 | naive: no fill begun at node 0 | P1 58, P3 137, P6 58 |
| M13 | parents: the XORs added up in breadth-first order, not backwards | P1 293, P3 301, P6 293 |
| M15 | parents: the rest the whole less the first node's subtree | P1 214, P3 175, P6 214 |
| M16 | parents: the first node never above the second | P3 133 |
| M19 | sets: the first test turned round | P1 134, P3 232, P6 134 |
| M20 | sets: only the last child's XOR kept | P1 276, P3 264, P4 260, P6 276 |
| M21 | sets: the whole tree's XOR the root's value | P1 290, P3 280, P6 290 |
| M23 | iter: inside judged by the start alone | P1 181, P3 156, P4 199, P6 181 |
| M24 | iter: a node paired with itself | P1 37, P6 37 |
| M25 | iter: the score the largest part | P1 351, P6 351 |
| M28 | solution: the top part the root's XOR | P1 68, P3 72, P6 68 |
| M29 | solution: the first node from 2 | P1 93, P2 35, P3 100, P5 35, P6 93 |

P1 and P6 kill sixteen, P3 fourteen, P4 four, and P2 and P5 one each.
P3, every node renamed `n - 1 - i`, hangs the tree from another root,
and nearly every edit that miscounts a subtree or an ancestor shows in
it. It alone kills M16: every case joins each node to one before it,
so a node's ancestors all have smaller numbers and the second of a
pair is never above the first; the test the edit drops is needed only
once the renaming turns the numbers round. P4, the edges written the
other way and in reverse order, fails where the order of a node's
neighbours or the direction of an edge matters: the second edge left
in, each edge walked one way, the last child's XOR alone, and inside
judged by the start alone. P2 and P5 fail only for the template's
first node from 2, which on a tree of three nodes tries no pair and
answers `i32.MAX`.

Of the thirty-one, fourteen were not kept. Seven fail alike, and none
is kept: the ★ arm's exit time one past the entry (M2), the parents
arm's every depth 0 (M12) and its climb one level past (M14), the sets
arm's child's set never merged (M17) and node never in its own set
(M18), the iter arm's span one step long (M22) and the template's exit
time the entry time (M27). Each loses the test of one node above
another, so every pair is scored as two subtrees apart. The ★ arm's
second node never above the first (M3) fails as the parents arm's M16;
its top part the whole tree's XOR (M4) as the template's top part the
root's (M28); the naive arm's score the largest part (M11) as the iter
arm's (M25); the iter arm's child's XOR never added (M26) as the ★
arm's (M1); and the template's rest less the first node's subtree
(M31) as the parents arm's (M15). The naive arm's second edge the first
again (M10) and the template's answer begun at 100 (M30) fail apart
from every kept one, and were left out to keep three to an arm and two
to the template.

M10 and M30 replace two edits that could not run. The naive arm's two
neighbouring edges never taken out left a tree of two edges with no
pair and its best at `i64.MAX`, and P5, which doubles the answer,
stopped there on an integer overflow.
The template's answer begun at a bare `100` is refused by `karac
check`: the literal keeps the default `i64`, and the message says so
and offers the `i32` that the template's answer needs; the edit is
written `100i32`.

## Verification

Every arm prints the same output as `tree.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the ★, parents, sets and template arms take
0.3 to 0.6 s, the iter arm 0.7 s, and the naive arm, which floods the
tree again for every pair of edges, 11.7 s. The differential takes 23 s
there, most of it the literal reading's labels passed along the edges
for every pair and the naive arm's floods, and 1.2 s under `karac
__mir-llvm-run`.

## Benchmarks

The bench builds 10 random trees of 1000 nodes with values up to `10^8`
once, then makes 30 passes over them with the ★ arm in all five
languages, each pass changing one value of each tree, chosen at
random, before scoring it. Every implementation prints `30 passes over
10 trees of 1000 nodes: checksum 838479156`. Each builds lists of
neighbours for every call, walks them recursively, and then scores all
`499500` pairs; C keeps the lists as growable arrays.

BENCHTAB
