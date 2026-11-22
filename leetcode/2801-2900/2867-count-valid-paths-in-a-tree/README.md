# 2867. Count Valid Paths in a Tree

There is an undirected tree with `n` nodes labeled from `1` to `n`. You
are given the integer `n` and a 2D integer array `edges` of length
`n - 1`, where `edges[i] = [ui, vi]` indicates that there is an edge
between nodes `ui` and `vi` in the tree.

Return *the **number of valid paths** in the tree*.

A path `(a, b)` is **valid** if there exists **exactly one** prime
number among the node labels in the path from `a` to `b`.

**Note** that:

- The path `(a, b)` is a sequence of **distinct** nodes starting with
  node `a` and ending with node `b` such that every two adjacent nodes
  in the sequence share an edge in the tree.
- Path `(a, b)` and path `(b, a)` are considered the **same** and
  counted only once.

```
n = 5, edges = [[1,2],[1,3],[2,4],[2,5]]        ->  4
n = 6, edges = [[1,2],[1,3],[2,4],[3,5],[3,6]]  ->  6
```

**Constraints:** `1 <= n <= 10^5`; `edges.length == n - 1`;
`edges[i].length == 2`; `1 <= ui, vi <= n`; the input is generated
such that `edges` represent a valid tree.

## Approaches

| file | mechanism |
|---|---|
| `paths.kara` ★ | with the primes taken out, the other nodes fall into components, joined by a disjoint-set union over the edges between two non-primes; a valid path has its one prime p and the rest in at most two of the components around p, so for each p its neighbours' component sizes are walked, each adding its size (paths ending at p) and its size times the sizes before it (paths through p) |
| `paths_flood.kara` | the components labelled by breadth-first flood fill with a queue; for each prime, with S the sum of its neighbours' component sizes and Q the sum of their squares, S paths end at it and (S^2 - Q) / 2 pass through it |
| `paths_dp.kara` | one pass of dynamic programming over the tree rooted at 1, children before parents in reverse breadth-first order: for each node, the paths from it down with no prime and with one; each child's halves are paired with the halves gathered so far, one side's prime with the other's none, before they are gathered in |
| `paths_sorted.kara` | the components' sizes by a disjoint-set union by size, then every edge from a prime to a non-prime as a pair (prime, size), the pairs sorted, and each prime's run walked as the ★ arm walks its neighbours |
| `paths_solution.kara` | a Rust solution as LeetCode's Rust users write it: a sieve, a `vec![vec![]; n + 1]` adjacency list, and for each prime a stack-based search from each non-prime neighbour not yet sized, the size written on every node of its component, then `ans += size[v] * sum + size[v]`, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 4 lines: LeetCode's two examples; 10^5
nodes, LeetCode's most, as a path and as a star around node 2; then
3000 random trees of 1 to 10 nodes, and 30 of 10^4 to 10^5, every other
one deep, each node's parent among the five before it, as a total of
paths and a checksum. `paths.py` mirrors the ★ arm and its output is
byte-identical.

```
4 6
989728 4086848436
3000 small trees: 17390 paths, checksum 796885421
30 large trees: 1326967278 paths, checksum 345925422
```

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: every pair a < b, the path between them found by
walking up from b to the root of a breadth-first search from a, its
primes counted by trial division, and the pair kept when there is one.
It draws 2000 random trees of 1 to 12 nodes, then 50 of up to 3000,
every other one deep, each edge written either way round and the list
shuffled, all before any arm answers; the literal reading is asked only
of the first 2000.

| | property |
|---|---|
| P1 | up to 12 nodes, the answer is the literal reading's |
| P2 | every edge written the other way round and the list reversed: the same answer |
| P3 | from the number of edges joining a prime to a non-prime to n(n - 1) / 2 |
| P4 | labels 1 and 4 swapped, two non-primes: the same answer |
| P5 | labels 2 and 3 swapped, two primes: the same answer |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2050 cases, 3125929 paths: checksum 827128368,
61500 checks over 5 arms: 0 failures` under every lane in Verification,
and a Python reading of the same cases gives the same checksum. On a
failure it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the sieve stopped before n, so n is never struck off | P1 886, P3 135, P4 134, P6 928 |
| M2 | ★: paths ending at the prime not counted | P1 1840, P3 1444, P6 1890 |
| M3 | flood: a component's size one short | P1 1840, P3 1344, P6 1890 |
| M4 | flood: the pairs through a prime counted twice | P1 1118, P6 1168 |
| M5 | dp: a prime node's halves gathered as a non-prime's | P1 1444, P6 1494 |
| M6 | dp: the pairing done after the gathering | P1 1329, P3 4, P4 959, P6 1379 |
| M7 | sorted: a non-prime pair's union skipped when the first is larger | P1 726, P2 1060, P4 401, P6 775 |
| M8 | sorted: each run's sizes before not reset | P1 1429, P3 428, P6 1478 |
| M9 | solution: a component's size not written on its nodes | P1 234, P3 20, P6 283 |
| M10 | solution: 1 taken as a prime | P1 1840, P3 1275, P4 1298, P6 1890 |

## Benchmarks

The bench draws 10 trees of 10^5 nodes, LeetCode's most, every other one
deep, all of them first, then answers each 10 times by the ★ arm in all
five languages. C keeps each node's prime-side neighbours in one array
indexed by offsets, counted first, where the others push onto a list per
node; every implementation allocates its arrays on each call. Every
implementation prints `10 trees of 100000, 10 rounds: 11321535960
paths, checksum 794783311`.

BENCHTAB

## Verification

All five arms print the same output as `paths.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

`paths_sorted.kara`, as first written, swapped its two roots through
Rust's `let (mut a, mut b) = (..)`, and `karac check` reported E0001 at
each `mut`: in Kāra `mut` goes before the whole pattern. `karac fix`
wrote `let mut (a, b) = (..)`. The other three arms checked clean.

LeetCode's Rust template took 32 `karac fix` edits in one run, the
wrapper included: `struct Solution {}` added for the `impl`; `Vec<..>`
became `Vec[..]`, and every `usize`, in `n as usize` and the edge's
`e[0] as usize`, became `i64`; `vec![x; n + 1]` became `Vec.filled(n +
1, x)`, `vec![vec![]; n + 1]` with `Vec.new()` inside, and `vec![v]` a
plain `[v]`; `for &v in &g[p]` became `for v in ref g[p]` and `for e in
&edges` `for e in ref edges`; `!` and `&&` became `not` and `and`;
`0i64` lost its suffix and `comp.len() as i64` its cast; `|&x|` lost its
`&`, and `Solution::` took `.`. `for i in 2..=n`, `while let Some(u) =
stack.pop()` and `size[v] = -1` were accepted as written.
