# 2876. Count Visited Nodes in a Directed Graph

There is a **directed** graph consisting of `n` nodes numbered from `0`
to `n - 1` and `n` directed edges.

You are given a **0-indexed** array `edges` where `edges[i]` indicates
that there is an edge from node `i` to node `edges[i]`.

Consider the following process on the graph:

- You start from a node `x` and keep visiting other nodes through edges
  until you reach a node that you have already visited before on this
  **same** process.

Return *an array* `answer` *where* `answer[i]` *is the number of
**different** nodes that you will visit if you perform the process
starting from node* `i`.

```
edges = [1,2,0,0]    ->  [3,3,3,4]
edges = [1,2,3,4,0]  ->  [5,5,5,5,5]
```

**Constraints:** `n == edges.length`; `2 <= n <= 10^5`;
`0 <= edges[i] <= n - 1`; `edges[i] != i`.

## Approaches

| file | mechanism |
|---|---|
| `visited.kara` ★ | every node has one edge out, so each part of the graph is a cycle with trees hanging into it. Nodes with nothing coming in are peeled off, Kahn's way, until only the cycles are left; a node on a cycle visits its cycle's length, and a peeled node, taken in the reverse of the peeling order, one more than the node its edge leads to |
| `visited_walk.kara` | from each node not yet answered, the edges followed with the walk's nodes kept in order and each one's place in it, until the walk meets itself, a new cycle, or a node already answered; then the walk answered from its far end back |
| `visited_memo.kara` | recursive: a node's count is one more than its edge's, memoised, except on a cycle. The recursion keeps the depth it reached each node at; meeting a node still open closes a cycle of the difference, and every node back up to it takes that length. A path of 10^5 nodes recurses 10^5 deep |
| `visited_reverse.kara` | the cycles found first, by walking from each node with every node coloured new, on this walk, or done; then a breadth-first search over the edges reversed, out from every cycle at once |
| `visited_solution.kara` | a Rust solution as LeetCode's Rust users write it: in-degrees peeled with a `VecDeque`, each cycle measured and filled, then the peeled nodes filled from a `Vec<usize>` order walked backwards, `as usize` at every index, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 4 lines: LeetCode's two examples; 10^5 nodes,
LeetCode's most, as one cycle, and as a path into a cycle of two at its
end, the totals and the path's first and last counts; then 3000 random
graphs of 2 to 8 nodes, and 100 of 1000 to 10^5, every other one with
each edge a step of 1 to 5 forward, as a total of the counts and a
checksum over them. `visited.py` mirrors the ★ arm and its output is
byte-identical.

```
[3, 3, 3, 4] [5, 5, 5, 5, 5]
10000000000 5000050001 100000 2
3000 small graphs: visits total 51660, checksum 354227880
100 large graphs: visits total 56410502280, checksum 300381287
```

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: from every node the edges followed, the nodes met kept,
until one comes round again, and the count of them taken. It draws 2000
random graphs of 2 to 10 nodes, then 50 of up to 3000, every other one
with each edge a step of 1 to 5 forward, all before any arm answers;
the literal reading is asked only of the first 2000.

| | property |
|---|---|
| P1 | up to 10 nodes, the answer is the literal reading's |
| P2 | every label v made n - 1 - v: the answers in reverse |
| P3 | a new node with its edge into node 0: the same answers, and one more than node 0's for it |
| P4 | each count from 2 to n, and its edge's count or one more |
| P5 | the counts that equal their edge's are the cycles': as many nodes hold such a count L as a multiple of L |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2050 cases, visits total 31431643: checksum
423067292, 61500 checks over 5 arms: 0 failures` under every lane in
Verification, and a Python reading of the same cases gives the same
checksum. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Not run yet. On the karac release this batch was checked with
(`684b860a5`), the mutation runner stopped on a compiler crash before
any verdict; the table comes with a run on a newer build.

## Benchmarks

The bench draws 20 graphs of 10^5 nodes, LeetCode's most, every other
one with each edge a step of 1 to 5 forward and the rest anywhere, all
first, then answers each 20 times by the ★ arm in all five languages;
each allocates its work arrays per call. Every implementation prints
`20 graphs of 100000, 20 rounds: visits total 674491220600, checksum
623958885`.

BENCHTAB

## Verification

All five arms print the same output as `visited.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The four own arms checked clean as first written, the recursion's two
`mut ref Vec[i64]` parameters among them. The harness as first written
summed a `Vec` with `sum::[i64]()` inside an f-string, Rust's turbofish
in Kāra's brackets; `karac check` names it as a turbofish Kāra does not
have, and `karac fix` takes it out, the sum's type coming from the
`Vec[i64]` it is over.

LeetCode's Rust template took 34 `karac fix` edits over two runs, the
wrapper and the harness's two turbofish included: `use
std::collections::VecDeque;` went and `struct Solution {}` came for the
`impl`, `VecDeque::new()` becoming `VecDeque.new()`; `Vec<..>` became
`Vec[..]`, the order's `Vec<usize>` a `Vec[i64]`; `vec![0; n]` became
`Vec.filled(n, 0)` twice; `for &e in &edges` became `for e in ref
edges`, and `for &u` and the wrapper's two `|&x|` lost their `&`; `&&`
became `and`; and of the six `as usize` casts, the four used straight
as an index or assigned to an `i64` went, while the two that type a
fresh `let` became `as i64`.
