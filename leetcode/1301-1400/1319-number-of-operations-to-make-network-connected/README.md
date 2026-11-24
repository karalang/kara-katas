# 1319. Number of Operations to Make Network Connected

There are `n` computers numbered from `0` to `n - 1` connected by ethernet
cables `connections` forming a network where `connections[i] = [ai, bi]`
represents a connection between computers `ai` and `bi`. Any computer can
reach any other computer directly or indirectly through the network.

You are given an initial computer network `connections`. You can extract
certain cables between two directly connected computers, and place them
between any pair of disconnected computers to make them directly
connected.

Return the minimum number of times you need to do this in order to make
all the computers connected. If it is not possible, return `-1`.

```
n = 4, connections = [[0,1],[0,2],[1,2]]              ->  1
n = 6, connections = [[0,1],[0,2],[0,3],[1,2],[1,3]]  ->  2
n = 6, connections = [[0,1],[0,2],[0,3],[1,2]]        ->  -1
```

**Constraints:** `1 <= n <= 10^5`, `1 <= connections.length <= min(n *
(n - 1) / 2, 10^5)`, `connections[i].length == 2`, `0 <= ai, bi < n`,
`ai != bi`, there are no repeated connections, and no two computers are
connected by more than one cable.

The arms are `fn make_connected(n: i64, connections: Vec[Vec[i64]]) ->
i64`.

## Approaches

Fewer than n - 1 cables can never join n computers. With n - 1 or more,
every cable inside a group of computers beyond the ones that join it is
spare, there are enough of them, and one move joins two groups, so the
answer is the number of groups less one.

| file | mechanism |
|---|---|
| `make_connected.kara` ★ | the groups by union-find, each root's parent pointers halved on the way up and the smaller group hung under the larger. O(m α(n)) |
| `make_connected_bfs.kara` | the cables made into a list of neighbours for each computer, and the groups counted by a breadth-first walk from a `VecDeque` out of every computer not yet reached. O(n + m) |
| `make_connected_dfs.kara` | the same neighbour lists, and each group marked by a recursive depth-first walk from its first computer. O(n + m), as deep as the longest path the walk takes |
| `make_connected_label.kara` | every computer starts with its own number as its label, and every cable passes the smaller of its two ends' labels to both, pass after pass until a pass changes nothing; the groups are the computers that keep their own label. O(m · passes), slow when a label has far to go against the cables' order |
| `make_connected_solution.kara` | a Rust solution as LeetCode's Rust users write it (a `fn find(parent: &mut Vec<usize>, x: usize) -> usize` nested in the method that compresses by recursion, the cables read as `c[0] as usize`, the groups counted down from n), carried to Kāra by `karac fix` |
| `make_connected_graph.kara` | a second Rust solution as LeetCode's Rust users write it (the neighbour lists as `vec![vec![]; n]`, a `visited: Vec<bool>`, and an explicit `let mut stack = vec![i];` walk out of every computer not yet visited), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, five more properties |

Every arm prints the same 2 lines: LeetCode's three examples, two
computers and their one cable, a chain of `10^5` computers, the
constraints' most, and `10^5` computers with `10^5` cables at random (`1 2
-1 0 0 16153`); then 300 random networks of 2 to 2000 computers with 1 to
3000 different cables (`300 random networks: moves total 7527, checksum
848226154`). `make_connected.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac __mir-run`,
`karac run` and `karac __mir-llvm-run`, the chain taking the depth-first
arm `10^5` calls deep.

The Mend loop: the four Kāra arms checked clean as first written. The
first Rust arm takes one round of 24 fixes by `karac fix`'s count, from 13
errors: `struct Solution;` to `struct Solution {}`, `Vec<..>` to
`Vec[..]`, the nested `fn find` moved out of the method to the top level,
`&mut Vec<usize>` to `mut ref Vec[usize]`, `for c in &connections` to
`for c in ref connections`, the calls' `&mut parent` to `mut parent`,
`|&x|` to `|x|`, `::` to `.`, and the wrapper's `as i64` dropped as a
widening; its `usize` stays. The second takes one round of 26 fixes from
9 errors: the same rewrites, with `let n = n as usize` to `let n = n as
i64`, every `as usize` on an index dropped, `vec![vec![]; n]` to
`Vec.filled(n, Vec.new())`, `vec![false; n]` to `Vec.filled(n, false)`,
`vec![i]` to `[i]`, `for &v in &graph[u]` to `for v in ref graph[u]`, and
`!` to `not`. Of its two `push(.. as usize)`, the first becomes `as i64`,
which fixes the lists' element type, and the second loses its cast. Both
outputs match on the first run. No gap was met.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: a move takes out one cable and puts it between two computers no
cable joins, and a breadth-first search over the sets of cables, one bit
for each pair of computers, finds the fewest moves to cables that join
every computer, or -1 when none will. 2000 networks of 2 to 6 computers,
every cable a different pair written either way round, in four kinds, 500
each: 1 cable up to every pair; exactly n - 1 cables; n - 1 cables up to
every pair; and 1 to n - 1 cables. Every network and renumbering is drawn
before any arm answers.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the computers renumbered: the same answer |
| P3 | the cables listed last first, each written end to start: the same answer |
| P4 | one more computer with a cable to computer 0: the same answer |
| P5 | the network beside a copy of itself: -1 with fewer than n cables, which the copy cannot spare, else twice the groups less one |
| P6 | the ★ arm's answer |

All 72,000 checks pass on every arm: `2000 networks: checksum 578807307,
72000 checks over 6 arms: 0 failures`, under `karac __mir-run` and
`karac __mir-llvm-run`. Python gives the same checksum.

## Mutation testing

Fourteen edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`. Two are left out, both on the
first Rust arm, whose group count is a `usize`: starting it at n - 1 and
a `find` that climbs one step only each take it below 0, and the program
stops on an integer overflow, the same under both backends. The twelve
kept, two to each arm, are each killed, fail the same way under both
backends and not by a crash, and no two fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: never -1, however few the cables | P1 393, P5 1470, P6 1965 |
| M2 | ★: the larger root made its own parent in place of the smaller's | P1 717, P6 3585 |
| M3 | bfs: each cable kept in one direction only | P1 1044, P2 842, P3 1210, P4 1607, P6 1044 |
| M4 | bfs: n - 1 cables thought too few | P1 1077, P6 1077 |
| M5 | dfs: the walk going on only from a computer's first neighbour | P1 1074, P2 586, P3 735, P4 1568, P6 1074 |
| M6 | dfs: computer 0 never starting a group | P1 39, P2 58, P4 39, P5 2, P6 39 |
| M7 | label: one pass only | P1 254, P2 311, P3 373, P6 254 |
| M8 | label: only the computers labelled 0 counted as groups | P1 1599, P2 72, P4 1607, P5 530, P6 1599 |
| M9 | solution: -1 only below n - 2 cables | P1 205, P5 1077, P6 205 |
| M10 | solution: the first cable never read | P1 950, P3 116, P5 21, P6 950 |
| M11 | graph: a computer's neighbours walked only when it starts a group | P1 800, P2 330, P6 800 |
| M12 | graph: the groups counted, not less one | P1 1607, P5 530, P6 1607 |

P1 and P6 kill all twelve, P2 and P5 six each, P3 and P4 four each.
Renumbering the computers (P2) catches the edits whose walk or labels
depend on which computer has which number: the one-way lists (M3), the
first neighbour only (M5), computer 0 left out (M6), the labels passed
along once (M7) or read as 0 (M8), and the walk that stops at its start
(M11). Listing the cables the other way round (P3) catches the edits that
depend on the cables' order or direction (M3, M5, M7) and the first cable
skipped, which is now another cable (M10). One more computer on computer
0 (P4) changes 0's neighbours and the count of computers, and catches
M3, M5, M6 and M8. The network beside its copy (P5) doubles the groups
and the cables, and so catches the edits
that get the -1 wrong (M1, M9) or the count of groups (M6, M8, M10, M12).
M2, which never merges two groups and so miscounts only when a cable
closes a loop, and M4, whose wrong -1 at exactly n - 1 cables stays right beside a
copy, show only against the statement and the ★ arm.

## Benchmarks

The bench builds 4 networks of `10^5` computers, the constraints' most,
once from its own generator: `10^5` cables at random; a chain listed in a
shuffled order; `10^4` rings of 10 computers, `10^5` cables in all; and
99999 cables at random. It then makes 25 passes, each moving one cable of
every network to a pair chosen by the checksum so far, so no answer
carries over, answering it with the ★ arm and folding the answer plus the
pass into the checksum. A move can repeat a cable already there, which
every arm takes as one more spare. Each call takes fresh parent and size
lists in every language, two `malloc`s in C. Every implementation prints
`25 passes over 4 networks of 10^5: checksum 491186204`.

BENCHTAB
