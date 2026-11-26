# 1791. Find Center of Star Graph

There is an undirected star graph of `n` nodes labelled `1` to `n`: one
center node joined to every other node by exactly `n - 1` edges. Given
`edges`, where `edges[i] = [u, v]` is an edge between `u` and `v`,
return the center of the star.

```
edges = [[1,2],[2,3],[4,2]]        ->  2
edges = [[1,2],[5,1],[1,3],[1,4]]  ->  1
```

**Constraints:** `3 <= n <= 10^5`, `edges.length == n - 1`, `1 <= u, v
<= n`, `u != v`, and the edges form a valid star.

The arms are `fn find_center(edges: Vec[Vec[i32]]) -> i32`.

## Approaches

| file | mechanism |
|---|---|
| `find_center.kara` ★ | the center is on every edge and a leaf on only one, so the center is the node the first two edges share. O(1) |
| `find_center_degree.kara` | every node's degree counted over all the edges; the center is the one on all `n - 1` of them. O(n) |
| `find_center_repeat.kara` | the endpoints walked edge by edge into a `Set`, whose `insert` says whether the node is new; a leaf is on one edge, so the first node seen twice is the center. O(1), at most three endpoints |
| `find_center_sum.kara` | arithmetic: the endpoints summed hold the center `n - 1` times and every other node once, so their sum less `1 + 2 + ... + n` is the center `n - 2` times. O(n) |
| `find_center_solution.kara` | a Rust solution as LeetCode's Rust users write it (the first two edges compared with `\|\|`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 4 lines: LeetCode's two examples (`2 1`); four
edges, three nodes with the center first, second and last in the first
edge, and four nodes with the center the largest label (`1 2 3 4`); the
constraints' most, 100000 nodes around 1, around 100000 and around one
at random, the edges shuffled and each written from either end (`the
most: 1 100000 12010`); and 3000 random stars of 3 to 40 nodes (`3000
random stars: checksum 875673000`). `find_center.py` mirrors the ★ arm,
and its output is byte-identical. Every arm gives the same output under
`karac __mir-run`, `karac run`, `karac build` and `karac
__mir-llvm-run`.

The Mend loop: the ★, degree, repeat and sum arms and the harness check
clean as first written. The Rust solution takes one round of 9 fixes by
`karac fix`'s count, and its diff is: `struct Solution;` to `struct
Solution {}`, `Vec<Vec<i32>>` to `Vec[Vec[i32]]` in both signatures,
`||` to `or`, and `Solution::` to `Solution.`. Every arm's output
matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the node joined to every other node, each node tried against
every edge, while there are at most 60 nodes. LeetCode's examples, the
four edges, 5000 nodes around 1, around 5000 and around one at random,
and 1991 random stars of 3 to 60 nodes. Each arm meets six properties on
each case:

| property | what it checks |
|---|---|
| P1 | the statement read literally, while there are at most 60 nodes |
| P2 | the edges in reverse order give the same answer |
| P3 | each edge written from its other end gives the same answer |
| P4 | the labels reversed, `v` to `n + 1 - v`, reverse the answer |
| P5 | one more leaf, `n + 1`, joined to the ★ arm's center gives the same answer |
| P6 | the ★ arm's answer |

The differential checks clean as first written. All 59,985 checks pass
on every arm: `2000 cases: checksum 236171337, 59985 checks over 5 arms:
0 failures`, under `karac __mir-run`, `karac run`, `karac build` and
`karac __mir-llvm-run`. Python, running the ★ arm's mirror over the same
cases, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: only the second edge's first end compared | P1 490, P2 883, P3 1000, P5 752, P6 1960 |
| M2 | ★: the two ends of the first edge the wrong way round | P1 1997, P2 2000, P5 3038, P6 8000 |
| M3 | degree: any node on an edge taken as the center | P1 1870, P4 2000, P5 2000, P6 1872 |
| M4 | degree: only each edge's first end counted | P1 1982, P3 29, P4 1985, P6 1985 |
| M5 | repeat: the first node seen once returned | P1 1007, P2 1483, P3 2000, P6 1010 |
| M6 | repeat: the first edge skipped | P1 31, P4 31, P5 31, P6 31 |
| M7 | sum: the surplus divided by n - 1 | P1 1997, P4 2000, P5 128, P6 2000 |
| M8 | sum: only each edge's first end summed | P1 1997, P3 1612, P4 2000, P5 978, P6 2000 |
| M9 | solution: only the second edge's second end compared | P1 500, P2 858, P3 1000, P6 500 |
| M10 | solution: the two ends of the first edge the wrong way round | P1 1997, P2 2000, P6 2000 |

## Benchmarks

The bench builds 2000 random stars of 100 nodes once, the edges shuffled
and each written from either end, and makes 20000000 calls of the ★ arm,
each star drawn from the checksum so far. Each call reads at most four
numbers. It checks clean as first written. Every implementation prints
`20000000 calls over 2000 stars: checksum 938043979`.

BENCHTAB

Measured by hand, best of three on a machine shared with a test run,
Kāra takes 0.92 s against Rust's 0.91 s (0.92 s with overflow checks
on), C's 0.45 s and Go's 0.97 s; Python takes 4.7 s.
