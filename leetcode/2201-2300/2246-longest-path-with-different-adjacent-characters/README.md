# 2246. Longest Path With Different Adjacent Characters

You are given a **tree** (i.e. a connected, undirected graph that has no
cycles) **rooted** at node `0` consisting of `n` nodes numbered from `0`
to `n - 1`. The tree is represented by a **0-indexed** array `parent` of
size `n`, where `parent[i]` is the parent of node `i`. Since node `0` is
the root, `parent[0] == -1`.

You are also given a string `s` of length `n`, where `s[i]` is the
character assigned to node `i`.

Return *the length of the **longest path** in the tree such that no pair
of **adjacent** nodes on the path have the same character assigned to
them.*

```
parent = [-1,0,0,1,1,2], s = "abacbe"  ->  3
parent = [-1,0,0,0],     s = "aabc"    ->  3
```

**Constraints:** `n == parent.length == s.length`; `1 <= n <= 10^5`;
`0 <= parent[i] <= n - 1` for all `i >= 1`; `parent[0] == -1`; `parent`
represents a valid tree; `s` consists of only lowercase English
letters.

A path's length counts its nodes. Every path bends at its highest node,
so it is that node with the two longest chains going down from it,
each through a child of another letter, and each chain changing letter
at every step. Every node's longest such chain comes from its
children's, so one pass with every child before its parent finds them
all. O(n).

## Approaches

| file | mechanism |
|---|---|
| `path.kara` ★ | child lists; the nodes in breadth-first order from the root, taken back to front; each node's longest chain `down[v]` and its two longest through children of another letter |
| `path_recursive.kara` | a recursive depth-first search: `chain` returns the longest chain down from a node and records the path that bends there in `best` (`mut ref i64`); the path of 10^5 nodes recurses 10^5 deep |
| `path_peel.kara` | no child lists: each node counts the children it waits for, the leaves are ready first, and a ready node hands its chain to its parent through a `VecDeque`; the parent keeps its two longest in two arrays |
| `path_struct.kara` | a `struct Tree` (`Tree.build`, `post_order` from an explicit stack) and a `#[derive(Copy, Clone)] struct TopTwo` whose `offer` (`mut ref self`) keeps the two longest chains, with `path` and `chain` (`ref self`) |
| `path_iter.kara` | iterator chains: the child lists by `fold`, the tree's levels by `successors` (each level the `flat_map` of the one above), deepest first; each node's two longest chains by `filter`, `map` and a `fold` keeping the top two, a level answered whole before its chains are written back |
| `path_solution.kara` | LeetCode's Rust template: `Vec<i32>` and `String` in, `i32` out, `s.as_bytes()`, `vec![vec![]; n]`, and a recursive `Self::dfs` over `&Vec<Vec<usize>>` and `&[u8]` with `ans: &mut i32`, counting edges; carried by `karac fix` in one round |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's two examples and four
more (one node, a path of one letter, a path of two letters in turn,
and a star of five letters), each with its answer; then the longest
over 2000 random trees of 1 to 30 nodes and 1 to 4 letters, with a
checksum of the answers; then the constraints' largest, 10^5 nodes
numbered at random with 26 letters; then a path of 10^5 nodes with two
letters in turn, whose answer is all of it. `path.py` mirrors the ★ arm
and its output is byte-identical.

`karac fix` carries the template in one round of 33 edits: `Vec<..>` to
`Vec[..]`, `s.as_bytes()` to `s.bytes()` and `&[u8]` to `Slice[u8]`,
`vec![vec![]; n]` to `Vec.filled(n, Vec.new())`, `usize` to `i64` and
the `as usize` casts removed, `&Vec<Vec<usize>>` to `Vec[Vec[i64]]` (a
parameter borrows), `ans: &mut i32` to `ans: mut ref i32` with `&mut
ans` to `mut ans` at the calls, `for &v in &g[u]` to `for v in ref
g[u]`, `let mut ans = 0` and `let mut max_len = 0` typed `i32`,
`Self::dfs` to `Solution.dfs`, `struct Solution;` to `struct Solution
{}`, the `&` pattern dropped from the adapter's closure, and its `as
i64` removed as lossless.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every pair of nodes joined by the one path between them,
found by climbing from both to their first shared ancestor, kept when no
two neighbours on it share a letter, and the most nodes taken; no
chains. It checks 300 random trees of 1 to 10 nodes and 1 to 4 letters;
then 30 paths of up to 12 nodes and two letters, numbered at random;
then 30 trees lettered by depth, a, b, c in turn, so that every edge
changes letter and the answer is the longest path of all. All 360 are
drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the longest such path, read literally |
| P2 | the nodes other than the root renumbered in reverse: the same answer |
| P3 | the tree rooted at another node, renumbered so that it is 0: the same answer |
| P4 | a new leaf with a letter no node has: the same answer or one more |
| P5 | every letter made the same: 1; and the answer is 1 to n |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 cases: checksum 609125413, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that finds
the path between every two nodes by breadth-first search over the
undirected edges. On a failure it prints the first ten and then the
count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under `karac __mir-llvm-run`, and the kept
ones under `karac __mir-run` too. Seventeen are kept, three to each
Kāra arm and two to the Rust-template arm. Each kept one is killed,
fails the same way under both backends and not by a crash, and no two
kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M4 | ★: the order taken front to back | P1 139, P3 33, P6 139 |
| M5 | ★: a child of another letter counted only when numbered above its parent | P1 116, P2 122, P3 84, P6 116 |
| M6 | ★: no second chain | P1 81, P2 64, P3 71, P4 16, P6 81 |
| M7 | recursive: children of the same letter counted | P1 223, P5 324, P6 223 |
| M8 | recursive: only one chain counted at a bend | P1 114, P3 90, P6 114 |
| M10 | recursive: the search begun at the last node | P1 210, P2 111, P3 55, P4 63, P6 210 |
| M12 | peel: a node with one child ready at once | P1 82, P2 86, P3 55, P4 12, P5 13, P6 82 |
| M15 | peel: the root's path not counted | P1 166, P3 114, P6 166 |
| M16 | peel: the first chain not moved to second | P1 52, P2 2, P3 41, P4 17, P6 52 |
| M17 | struct: `offer` keeping the shorter first | P1 176, P6 176 |
| M18 | struct: the path one node short | P1 229, P6 229 |
| M19 | struct: the chain handed up from the second | P1 130, P3 58, P6 130 |
| M23 | iter: only children of the same letter | P1 284, P5 324, P6 284 |
| M24 | iter: the fold losing the first chain | P1 23, P2 53, P3 23, P4 5, P6 23 |
| M26 | iter: a level of one node ending the walk | P1 63, P3 122, P4 8, P6 63 |
| M27 | solution: the answer in edges | P1 360, P5 360, P6 360 |
| M30 | solution: the longest chain raised before the answer | P1 183, P3 90, P4 203, P5 59, P6 183 |

P1 and P6 kill all seventeen, P3 twelve, P4 seven, P2 six and P5 five.
P3 hangs the tree from another node, so an arm that leans on the root
or on the order it walks in answers differently; P2 renumbers the
nodes, and catches the edits that read the numbers themselves (M5, M10,
M12) or lose a chain only for some orders of the children (M6, M16,
M24). P4's fresh letter grows the answer by at most one, and catches the
edits that let two chains overlap or miscount the new leaf. P5's single
letter catches the edits that ignore or invert the letters, and the
answer counted in edges (M27).

Of the thirty-one, fourteen were not kept, and none crashes or differs
between the backends. Thirteen fail as a kept one does: the ★, peel and
struct arms' children of the same letter counted (M1, M13, M21) as the
recursive arm's (M7); the ★ arm's first chain not moved to second (M2)
as the iter arm's fold losing it (M24); the path one node short or the
chain handed up without its node in the ★, recursive, peel, iter and
template arms (M3, M9, M14, M25, M29) as the struct arm's (M18); the
recursive arm's shorter chain kept first (M11) as the struct arm's
(M17); the struct arm's post order not reversed and the iter arm's
levels shallowest first (M20, M22) as the ★ arm's order front to back
(M4); and the template's children of the same letter only (M28) as the
iter arm's (M23). One fails its own way and is left out for the count
of two: the template's node 1 never linked (M31). One first try was
replaced: the ★ arm's chains begun at 0 survived, and is equivalent,
since every node's chain is written before its parent reads it.

## Verification

Every arm prints the same output as `path.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the peel arm takes 1.2 s, the ★ and struct arms
1.5 s, the recursive arm 1.6 s, the template 1.9 s, the iter arm 4.4 s,
and the differential 0.8 s.

## Benchmarks

The bench answers 40 random trees of 10^5 nodes with the ★ arm in all
five languages, each node's parent drawn from those numbered before it
and its letter from 26. C keeps the child lists in one array by
offsets (CSR); the others keep a list per node. Every implementation
prints `40 trees of 100000 nodes: checksum 932329026`.

BENCHTAB
