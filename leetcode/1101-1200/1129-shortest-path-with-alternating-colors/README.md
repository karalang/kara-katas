# 1129. Shortest Path with Alternating Colors

You are given an integer `n`, the number of nodes in a directed graph
where the nodes are labeled from `0` to `n - 1`. Each edge is red or
blue in this graph, and there could be self-edges and parallel edges.

You are given two arrays `redEdges` and `blueEdges` where:

- `redEdges[i] = [ai, bi]` indicates that there is a directed red edge
  from node `ai` to node `bi` in the graph, and
- `blueEdges[j] = [uj, vj]` indicates that there is a directed blue edge
  from node `uj` to node `vj` in the graph.

Return an array `answer` of length `n`, where each `answer[x]` is the
length of the shortest path from node `0` to node `x` such that the edge
colors alternate along the path, or `-1` if such a path does not exist.

```
n = 3, redEdges = [[0,1],[1,2]], blueEdges = []        ->  [0,1,-1]
n = 3, redEdges = [[0,1]], blueEdges = [[2,1]]         ->  [0,1,-1]
```

**Constraints:** `1 <= n <= 100`; `0 <= redEdges.length,
blueEdges.length <= 400`; `redEdges[i].length == blueEdges[j].length ==
2`; `0 <= ai, bi, uj, vj < n`.

The arms are `fn shortest_alternating_paths(n: i64, red_edges:
Vec[Vec[i64]], blue_edges: Vec[Vec[i64]]) -> Vec[i64]`.

## Approaches

A path's next edge depends on the colour of the last one, so each arm
reads the graph as one of states, a node and the colour that reached it.
Node 0 starts under both colours: the first edge may be either. A
shortest path meets each state at most once, so it has at most `2n - 1`
edges.

| file | mechanism |
|---|---|
| `shortest_alternating_paths.kara` ★ | a breadth-first search over (node, colour) with a `VecDeque`, an adjacency list per colour, each state's length set when it is first met. O(n + edges) |
| `shortest_alternating_paths_levels.kara` | level by level: the nodes just reached by a red edge and those just reached by a blue one, each grown along the other colour, a node's length the first level it is met at. O(n + edges) |
| `shortest_alternating_paths_relax.kara` | relaxation as Bellman-Ford does it: the shortest lengths known ending red and ending blue, every red edge lowering the red one from the blue one and every blue edge the reverse, round after round until a round changes nothing. O(n * edges) |
| `shortest_alternating_paths_steps.kara` | step by step: the set of nodes `k` edges reach ending red and the set ending blue, each made from the other's set of `k - 1`, for `k` up to `2n`. O(n * edges) |
| `shortest_alternating_paths_solution.kara` | a Rust solution as LeetCode's Rust users write it (`impl Solution`, one adjacency list of `(usize, i32)` pairs, a `VecDeque` of `(node, length, last colour)` with `-1` for none, `vec![[false; 2]; n]`, `&(next, color)` patterns), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 12 lines: the answers for LeetCode's five
examples and four more (one node, a red and a blue cycle that a long
path winds through, loops at node 0, and every edge in both colours),
then over 2000 random graphs of up to 100 nodes and up to `2n` edges of
each colour, the nodes reached, the lengths summed and a checksum
(`2000 random graphs: 27615 nodes reached, lengths total 53424, checksum
263784554`), and two of LeetCode's largest: 100 nodes with 400 edges of
each colour at random, and a chain of 100 whose edges alternate (`last
99, total 4950`). `shortest_alternating_paths.py` mirrors the ★ arm and
its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every walk from node 0 whose edges alternate in colour,
followed edge by edge up to `2n` edges, and each node's shortest. It
checks 2000 problems in five kinds of 400: up to 6 nodes and up to `n`
edges of each colour; up to 4 nodes and up to 8 edges of each, so walks
cross and loop; up to 6 nodes, up to `2n` red edges and one or two blue;
a chain of up to 7 nodes alternating in colour; and a chain of 2 to 8
nodes in one colour with a loop of the other on every node between its
ends, where node `k` is first reached at `2k - 1`. The two chains carry
up to 2 more edges of each colour. Every random choice is drawn before
any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal one |
| P2 | by a second reading, from the sets of nodes `k` edges reach ending red and ending blue: a node answered `d` is in a set of `d` and in none before, and a node answered `-1` in none up to `2n` |
| P3 | red and blue swapped give the same answer |
| P4 | each colour's edges listed last first give the same answer |
| P5 | every node but 0 relabelled `n - v` moves the answers with it |
| P6 | a new node `n` with one red edge from node 0 is answered 1, and every other answer stays |

All 60,000 checks pass on every arm: `2000 problems: checksum
655558073, 60000 checks over 5 arms: 0 failures`. A Python reading of
the same problems, a breadth-first search over (node, colour) with a
dictionary of lengths, gives the same checksum.

The first draft drew four kinds of 500, without the chain of loops. Its
shortest answers were short: an edit that took a length of `n` or more
for unreached (M7) failed on 10 problems of 2000. The fifth kind raises
that to 261.

## Mutation testing

Thirty edits to the differential, six to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run` with `KARAC_HASH_SEED=1`,
each failing the same way under both. All thirty are caught. Fifteen
are kept, no two failing the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: node 0 started under red alone | P1 726, P2 726, P3 1272, P6 2000 |
| M2 | ★: a node reached only by a blue edge left unreached | P1 669, P2 669, P3 1093 |
| M3 | ★: the queue taken as a stack | P1 66, P2 66, P3 103, P4 11 |
| M4 | levels: a red edge taken after a red one | P1 997, P2 997, P3 1272 |
| M5 | levels: every length one too long | P1 1368, P2 1368, P6 2000 |
| M6 | levels: node 1 never reached by a blue edge | P1 666, P2 666, P3 1095, P5 750 |
| M7 | relax: a length of `n` or more taken for unreached | P1 261, P2 261, P6 147 |
| M8 | relax: one round alone | P1 662, P2 662, P3 448 |
| M9 | relax: node 1 never reached by a red edge | P1 716, P2 716, P3 1095, P5 805, P6 286 |
| M10 | steps: a node met only ending red | P1 844, P2 844, P3 1272 |
| M11 | steps: a blue edge marking where it starts | P1 879, P2 879, P3 1259 |
| M12 | steps: the last node never given a length | P1 1181, P2 1181, P5 1013, P6 2000 |
| M13 | solution: the colours never checked to alternate | P1 472, P2 472 |
| M14 | solution: a node's last length kept | P1 632, P2 632 |
| M15 | solution: the queue taken as a stack | P1 162, P2 162, P3 58, P4 166 |

P1 and P2 catch all fifteen, P3 ten, P6 five, P5 three and P4 two. P2
fails on exactly the problems P1 does: the first length whose set holds
a node pins its answer as tightly as the literal walk. P3 sees the edits
that treat the two colours apart (a start under one, a length ending in
one, a red edge after a red one, node 1 kept from one), and the order
edits too, since swapping the colours changes the order a search meets
its states. P6 sees the edits that get node 0's start or a length wrong
across the board, and the two that single out the last node or a long
length, since the new node is last and `n` grows. P5 sees only the edits
that single out a node by its label. P4 sees only the two searches that
take the queue as a stack, whose answer depends on the order edges are
met. One round of relaxation (M8) finds a red edge and a blue edge after
it whatever order the lists are in, so P4 cannot see it, but swapping
the colours finds the other paths of two.

M13 and M14 fail on P1 and P2 alone: an arm that ignores the colours, or
keeps a node's last length, answers the swapped, reversed, relabelled
and grown graphs consistently wrong. Only the two readings of the answer
see them.

Of the fifteen not kept, nine fail exactly as a kept one: node 0
started under one colour in the levels, relax, steps and solution arms
as M1; the longer of two lengths kept in the ★ arm, and a node's last
level in the levels arm, as M14; a node's length ending red alone in the
relax arm as M10; paths of `n` edges or more never made in the steps arm
as M7; and the last colour never updated in the solution arm as M13. A
red edge after a red one in the relax and steps arms fail alike; each
edge taken in the colour of the one before in the ★ arm, the two
frontiers swapped in the levels arm and the two sets swapped in the
steps arm fail alike too, on P1 and P2 alone; and node 0's own length
never set in the steps arm fails all 2000 problems on P1 and P2. Those
six were not needed.

## Verification

Every arm prints the same output as `shortest_alternating_paths.py`
under `karac __mir-run` (the v2 MIR interpreter), `karac
__mir-llvm-run`, and `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer) with no error. `karac run` and a `karac build` binary
print the same output for every arm and the differential. `karac check
--output=json` reports nothing on any file, and `karac fix` has nothing
to apply.

The kata found two gaps: one fixed, one open. The ★, levels, relax and
steps arms were written as Kāra, the solution arm as Rust writes it.

`karac fix` carried the solution arm in five rounds: the `use` line
dropped, `Vec<..>` to `[..]`, `&` to `ref`, `::` to `.`, `&&` and `!` to
`and` and `not`, and the `&(next, color)` pattern to `(next, color)`;
then the closure's return type moved to its binding; then `struct
Solution {}` declared; then `vec![[false; 2]; n]` to `Vec.filled`, `vec![]`
to `Vec.new()`, a `vec![..]` list to `[..]` and `vec![-1; n]`'s element
suffixed `i32`; then `usize` to `i64` throughout, the other `vec![..;
n]` to `Vec.filled` and the `as usize` on `color` dropped. One refusal
was left, and it has no machine fix. Rust types the `0` and `1` pushed
into the adjacency list as `i32`, from `color != last` with `last:
i32`. In Kāra a comparison beside an `i32` keeps a literal's default, so
`color` is an `i64` and `q.push_back((next, d + 1, color))` into the
queue's `i32` slot is refused: `implicit coercion from 'i64' to 'i32'
would narrow or change sign ... Write an explicit 'as i32'`. The
refusal is right, but `karac fix` offers nothing, where for a let-bound
literal it declares the binding's type. The arm keeps the `as i32` the
message asks for, written by hand (B-2026-11-12-2).

Cutting that down found a false refusal on the way: a number inside a
tuple pushed into a tuple slot kept its default. `let x = 0; q.push((x,
1))` into a `Vec[(i32, i32)]` was refused as narrowing `x`, though an
argument fixes a literal and `q.push(x)` alone typed it `i32`; so was
the kata's own push without the comparison before it. Each open number
in a pushed tuple now takes its slot's type (B-2026-11-12-1).

## Benchmarks

The bench builds 32 random graphs once, LeetCode's largest: 100 nodes,
400 red edges and 400 blue. Each of 1000 rounds moves the end of one
edge in every graph, red in even rounds and blue in odd ones, and
answers the graph with the ★ arm: 32,000 searches, each building its
adjacency lists afresh. Every implementation prints `1000 rounds over 32
graphs of 100 nodes and 400 edges of each colour: lengths total 9090999,
checksum 392587612`. Each keeps the edges as LeetCode hands them, a list
of two-number lists (`Vec[Vec[i64]]`, `Vec<Vec<i64>>`, `[][]int64`,
Python lists, and C's `int64_t **` with each edge allocated by itself),
and the adjacency as a growable list per node and colour; Kāra and Rust
queue the states in a `VecDeque`, Python in a `deque`, Go in a slice and
C in an array of `2n`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `2d47b8e713`
on LLVM 22. karac builds for the x86-64-v3 baseline, so the C and
overflow-checked Rust programs are also built at `-march=x86-64-v3`:

| | time | median |
|---|---|---|
| C (`clang -O3 -march=x86-64-v3`) | 0.465 to 0.603 s | 0.588 s |
| C (`clang -O3`) | 0.463 to 0.661 s | 0.595 s |
| Kāra (`karac build`) | 0.528 to 0.678 s | 0.643 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.522 to 0.676 s | 0.668 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.583 to 0.796 s | 0.686 s |
| Rust (`rustc -O`) | 0.561 to 0.734 s | 0.711 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.606 to 0.800 s | 0.726 s |
| Go | 1.190 to 1.266 s | 1.221 s |
| Python | 3.7 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Kāra takes about 1.12x C's time and about 0.92x Rust's under
overflow checks: all three allocate a list per node and colour in every
search and walk the same edges. Go takes about 1.8x Kāra's time, and its
user time (1.54 s) is above its real time, so some of its work runs on
other cores beside the search; its collector would be the likely one,
but this was not traced.
Python takes about 5.5x Kāra's time.
