# 2791. Count Paths That Can Form a Palindrome in a Tree

You are given a **tree** (i.e. a connected, undirected graph that has no
cycles) **rooted** at node `0` consisting of `n` nodes numbered from `0`
to `n - 1`. The tree is represented by a **0-indexed** array `parent` of
size `n`, where `parent[i]` is the parent of node `i`. Since node `0` is
the root, `parent[0] == -1`.

You are also given a string `s` of length `n`, where `s[i]` is the
character assigned to the edge between `i` and `parent[i]`. `s[0]` can
be ignored.

Return *the number of pairs of nodes* `(u, v)` *such that* `u < v` *and
the characters assigned to edges on the path from* `u` *to* `v` *can be
**rearranged** to form a **palindrome***.

A string is a **palindrome** when it reads the same backwards as
forwards.

```
parent = [-1, 0, 0, 1, 1, 2], s = "acaabc"  ->  8
parent = [-1, 0, 0, 0, 0], s = "aaaaa"      ->  10
```

**Constraints:** `n == parent.length == s.length`, `1 <= n <= 10^5`,
`0 <= parent[i] <= n - 1` for all `i >= 1`, `parent[0] == -1`, `parent`
represents a valid tree, and `s` consists of only lowercase English
letters.

## Approaches

A node's mask holds the parity of each letter on the way from the root.
The edges above the meeting point of u and v appear on both their ways
and cancel, so the path's letters have the parities of `mask[u] ^
mask[v]`, and they make a palindrome when at most one bit of it is set.
The pairs are those whose masks are equal or one bit apart.

| file | mechanism |
|---|---|
| `paths.kara` ★ | the masks by walking the children from the root with a stack, then counted in a `Map` as they come, each node pairing with the earlier ones whose mask is the same or one of the 26 one bit away. O(26 n) |
| `paths_memo.kara` | the masks by memo up the parents, no children lists: from each node, climbing to the nearest one already known and coming back down, each mask an `Option[i64]`; then the ★ arm's pairing. O(26 n) |
| `paths_sorted.kara` | by sorting, no `Map`: the masks found breadth first with a `VecDeque`, sorted, and each one's partners counted by two `partition_point`s; each pair counted from both ends and halved, and a mask with itself taken out. O(26 n log n) |
| `paths_groups.kara` | by groups: the masks found by recursion from the root, the nodes of each mask counted in a `Map`, and the pairs summed over the groups, c(c - 1) / 2 within a group and c times the other's count for each group one bit above. O(26 n) |
| `paths_solution.kara` | a Rust solution as LeetCode's Rust users write it, a `HashMap<i32, i64>` filled from an explicit stack of `(node, mask)` pairs, each node adding the count of its own mask and the 26 one bit away, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 6 lines: LeetCode's two examples; a path of
`10^5` nodes, LeetCode's most, all a, every pair counted and the deepest
recursion from the root; `10^5` nodes on one root, the letters going
round the alphabet; 3000 random trees of 1 to 12 nodes with letters from
a to c; and 20 of `10^5` nodes with letters from a to z, the last two
with the sum of the counts and a checksum. `paths.py` mirrors the ★ arm
and its output is byte-identical.

```
8
10
4999950000
192353847
3000 small trees: paths sum to 43550, checksum 868117490
20 trees of 10^5: paths sum to 8302678, checksum 349684374
```

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every pair u < v, the path between them found by climbing the
deeper node and then both until they meet, the letters on its edges
gathered, and the pair taken when at most one letter is there an odd
number of times; no masks. It draws 2000 random trees of 1 to 10 nodes
with letters from a to c, then 50 of up to 2000 nodes, the letters from
a to c or from a to z, all before any arm answers; the literal reading
is asked only of the first 2000.

| | property |
|---|---|
| P1 | up to 10 nodes, the count is the literal reading's |
| P2 | every letter moved one on round the alphabet: the same count |
| P3 | the root's letter, on no edge, changed: the same count |
| P4 | every node but the root numbered from the other end, so that parents come after their children: the same count |
| P5 | from n - 1, each edge's two ends, to n(n - 1) / 2, and n(n - 1) / 2 when every letter is a |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2050 cases: checksum 803481387, 61500 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases, each path the nodes above u or v but not
both, gives the same checksum. On a failure it prints the first ten and
then the count by property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the same mask never paired | P1 1343, P5 1669, P6 1393 |
| M2 | ★: a child's mask not its parent's | P1 1096, P6 1146 |
| M3 | memo: a node's mask flipped by its parent's letter | P1 1357, P3 933, P6 1407 |
| M4 | memo: only 25 letters one bit away | P2 25, P6 25 |
| M5 | sorted: a mask paired with itself | P1 1806, P5 1856, P6 1856 |
| M6 | sorted: each pair counted from both ends, not halved | P1 1806, P5 1856, P6 1856 |
| M7 | groups: the pairs within a group counted as c(c + 1) / 2 | P1 2000, P5 2050, P6 2050 |
| M8 | groups: each group paired with those one bit below as well | P1 1806, P5 1856, P6 1856 |
| M9 | solution: each mask seen counted twice | P1 1806, P5 1856, P6 1856 |
| M10 | solution: a child's letter taken from its parent | P1 1357, P3 933, P6 1407 |

## Benchmarks

The bench draws 20 random trees of `10^5` nodes, LeetCode's most, with
letters from a to z, all of them first, then answers each 5 times by
the ★ arm in all five languages; the C version counts the masks in an
open-addressing table of its own, C having no map. Every implementation
prints `20 trees of 10^5, 5 rounds: paths sum to 41950275, checksum
761055851`.

BENCHTAB

## Verification

All five arms print the same output as `paths.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

Each own arm first read its letters as `s.bytes().iter().map(|b| b -
97).collect()` into a `Vec[i64]`; `karac check` refused it, `collect`
not widening a `u8`, and `karac fix` wrote the widening into the map,
`(b - 97) as i64`. The sorted arm first named its queue `Deque`, and
`karac fix` made it `VecDeque`. The harness first made a letter by
`('a' as i64 + i % 26) as char`, which `karac check` refused, not every
integer being a `char`; it now indexes the alphabet. The differential's
literal reading was first written with `let (mut a, mut b)` and
`collect::[Set[char]]()`, both refused and both rewritten by `karac
fix`, to `let mut (a, b)` and `Set[char].from_iter(..)`; it now collects
into a `Set[char]` named by the `let`.

LeetCode's Rust template took 34 `karac fix` edits, the wrapper
included: `use std::collections::HashMap` became `struct Solution {}`;
the `Vec<..>`s became `Vec[..]` and `HashMap<i32, i64>` became
`Map[i32, i64]`; `s.as_bytes()` became `s.bytes()`; `vec![vec![]; n]`
became `Vec.filled(n, Vec.new())` and `vec![(0usize, 0i32)]` the list
`[(0, 0i32)]`; the `as usize` indices and `usize` element types became
`i64`; `if let Some(&c) = cnt.get(&m)` became `if let Some(c) =
cnt.get(m).cloned()`; `for &v in &g[u]` became `for v in ref g[u]`; the
wrapper's `&str` became `Str` and its `|&p|` dropped the `&`; and
`Solution::` became `Solution.`.
