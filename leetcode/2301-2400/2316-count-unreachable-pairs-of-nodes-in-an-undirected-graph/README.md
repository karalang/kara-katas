# 2316. Count Unreachable Pairs of Nodes in an Undirected Graph

You are given an integer `n`. There is an **undirected** graph with `n`
nodes, numbered from `0` to `n - 1`. You are given a 2D integer array
`edges` where `edges[i] = [a_i, b_i]` denotes that there exists an
**undirected** edge connecting nodes `a_i` and `b_i`.

Return *the **number of pairs** of different nodes that are
**unreachable** from each other*.

```
n = 3, edges = [[0,1],[0,2],[1,2]]              ->  0
n = 7, edges = [[0,2],[0,5],[2,4],[1,6],[5,4]]  ->  14
```

**Constraints:** `1 <= n <= 10^5`; `0 <= edges.length <= 2 * 10^5`;
`edges[i].length == 2`; `0 <= a_i, b_i < n`; `a_i != b_i`; there are
no repeated edges.

Two nodes are unreachable from each other exactly when they lie in
different components, so the answer is the sum over pairs of
components of the products of their sizes. Taking the components in
any order, each one pairs with every node of those before it. The
count reaches `n (n - 1) / 2`, about `5 * 10^9`, so it is an `i64`.

## Approaches

| file | mechanism |
|---|---|
| `pairs.kara` ★ | union-find over a `Vec[i64]` of parents, `find` halving paths through a `mut ref`, union by size; each root, met in order, adds its size times the nodes before it |
| `pairs_naive.kara` | a breadth-first search from every node, the nodes it leaves unmarked counted, and the total halved. O(n (n + m)) |
| `pairs_bfs.kara` | adjacency lists and a `VecDeque[i64]`: a search from each node not yet seen measures its component |
| `pairs_labels.kara` | each node its own label, and sweeps over the edges giving both ends the smaller label until one changes nothing; each node then misses `n` less its component's size, halved |
| `pairs_iter.kara` | the ★ arm's union-find, then `(n^2 - within) / 2`, `within` the roots `filter`ed out and their sizes `map`ped to squares and `sum`med |
| `pairs_solution.kara` | LeetCode's Rust template: a recursive `find` nested in the method over a `&mut Vec<usize>`, union without sizes, the sizes counted from each node's root, each paired with the nodes still to come; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's two examples; one node;
five nodes and no edges; two triangles; a path of 2000 nodes; 2000
nodes and 1000 random edges; then 300 random graphs of 1 to 30 nodes
with up to as many edges as nodes, with a checksum and the pairs in
all. `pairs.py` mirrors the ★ arm and its output is byte-identical. No
case reaches `10^5` nodes, which the naive arm's search from every
node could not finish; the bench does.

`karac fix` carries the template in one call, reporting 34 edits.
`check` first reports twelve errors and offers 17 edits for them:
`struct Solution;` to `struct Solution {}`; the ten brackets of the
two `Vec<Vec<i32>>` and the two `Vec<usize>`; `&mut Vec` to `mut ref
Vec`, `&edges` to `ref edges`, and the three `&` dropped from the
`&mut parent` arguments; and `Solution::` to `Solution.` in the
wrapper. The other seventeen follow from those: the nested `fn find`,
which captures nothing, moved above `impl Solution`; its `usize`s and
the parents' to `i64`, the type of an index; `find(parent, ..)` within
it to `find(mut parent, ..)`; `n as usize` to `n as i64`, and the `as
usize` on each edge's ends and the `as i64` on `n` dropped; `vec![0i64;
n]` to `Vec.filled(n, 0)` and the answer's `0i64` to `0`; and the wrapper's `vec![a as i32, b as i32]` to an array
literal. `parent[x] = find(mut parent, parent[x])`, the parents read
for the argument and written through the call, stands as Kāra.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: a table of which node reaches which, each node itself and
each edge both ways, closed by letting every node in turn join what
reaches it to what it reaches, and every pair the table leaves apart
counted. No union-find and no search. It checks 300 random graphs of 1
to 12 nodes with up to as many edges as nodes; then 30 with no edges;
then 30 of 40 nodes and up to 60 edges. All 360 are drawn before any
arm answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | the answer is at most the pairs of nodes less the edges, since every edge joins a pair |
| P3 | every node `i` renamed `n - 1 - i`: the same answer |
| P4 | the edges listed in reverse, each with its ends swapped: the same answer |
| P5 | one node more with no edges: `n` more |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 cases: checksum 992677691, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that
builds the same cases and searches from every node. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M2 | ★: each union growing a set by one | P1 74, P4 67, P5 91, P6 74 |
| M3 | ★: each set before counted as one node | P1 157, P3 179, P4 114, P5 243, P6 157 |
| M4 | ★: the second end's own node joined, not its root | P1 123, P2 106, P4 126, P5 132, P6 123 |
| M8 | naive: the start not counted as reached | P1 321, P2 198, P5 178, P6 321 |
| M9 | naive: each edge one way | P1 192, P2 119, P6 192 |
| M10 | naive: the start not marked seen | P1 243, P2 50, P5 18, P6 243 |
| M13 | bfs: each component paired with itself | P1 346, P2 192, P5 321, P6 346 |
| M15 | bfs: each edge one way | P1 197, P2 146, P3 207, P4 212, P6 197 |
| M16 | bfs: only the component before counted | P1 222, P3 92, P5 271, P6 222 |
| M17 | labels: a single sweep | P1 123, P2 41, P3 129, P4 149, P6 123 |
| M18 | labels: node 0 left out of the sizes | P1 178, P2 46, P3 102, P6 178 |
| M21 | labels: an edge relabeled only when its first end changes | P1 197, P2 145, P3 205, P4 212, P6 197 |
| M22 | iter: each pair counted from both ends | P1 271, P2 239, P5 360, P6 271 |
| M24 | iter: the non-roots summed | P1 321, P2 311, P4 92, P5 202, P6 321 |
| M26 | iter: each union growing a set by one | P1 91, P2 6, P4 84, P6 91 |
| M30 | solution: each node counted under its parent, not its root | P1 138, P2 48, P4 136, P6 138 |
| M31 | solution: the rest begun one short | P1 360, P2 133, P5 360, P6 360 |

P1 and P6 kill all seventeen, P2 fourteen, P5 ten, P4 nine and P3 six.
P2 fails for more pairs apart than the pairs no edge joins, which most
overcounts reach. P5, a node more on its own, fails where a component's
size or its pairing is miscounted, since the new node pairs with all
`n`; it misses the edits that only lose an edge or a union, whose new
node still pairs rightly. P4, the edges reversed and turned, fails where
the order of the unions or the direction of an edge matters: a set
grown by one, a root not found, an edge one way in the search, a sweep
cut short. P3, the nodes renamed, fails where node 0 or the order in
which components are met is special: a set counted as one node, the
component before alone, node 0 left out, a sweep that leans on which
end is smaller.

Of the thirty-one, fourteen were not kept. The naive (M7) and labels
(M19) arms' pairs counted from both ends fail as the iter arm's (M22);
the labels arm's nodes counted under themselves (M20), the iter arm's
sizes not squared (M23) and larger set put under the smaller (M25), and
the template's no set joined (M27) and nodes counted under themselves
(M29) all fail alike, every one as though there were no edges, and none
is kept. The ★ arm's no set joined (M1), every node's size counted (M5)
and first edge left out (M6), the naive arm's no search from node 0
(M11), the breadth-first arm's components one node larger (M12) and
unseen nodes skipped (M14), and the template's rest taken before the
size leaves it (M28) fail apart from every kept one, and were left out
to keep three to an arm. M18 replaces the labels arm's first end alone
relabeled, which never stopped sweeping, and M30 the template's node 0
never following its parent, whose `find` recursed without end and
crashed.

## Verification

Every arm prints the same output as `pairs.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` every arm but the naive one takes 0.2 to 0.3
s, and the naive arm, a search from each of the 2000 nodes of the two
large cases, 6.0 s. The differential takes 1.1 s there and 0.5 s under
`karac __mir-llvm-run`.

## Benchmarks

The bench builds 10 graphs of `10^5` nodes once, graph `g` joining each
node `i` after the first, `g + 2` times in `g + 3`, to a random node
before it, so that no edge repeats and the components are trees, then
makes 50 passes, pass `p` taking graph `(a + p) % 10` at step `a`, with
the ★ arm in all five languages. Every implementation prints `50
passes over 10 graphs of 10^5 nodes: checksum 497959684`. Each
allocates the parents and the sizes, 64-bit integers, afresh for every
call and walks the edges once.

BENCHTAB
