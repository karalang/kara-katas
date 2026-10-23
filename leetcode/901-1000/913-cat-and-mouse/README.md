# 913. Cat and Mouse

A game on an undirected graph is played by two players, Mouse and Cat,
who alternate turns. The graph is given as `graph[a]`, a list of all
nodes `b` such that `ab` is an edge.

The mouse starts at node 1 and goes first, the cat starts at node 2 and
goes second, and there is a hole at node 0. During each player's turn
they must travel along one edge of the graph that meets where they are.
The cat is not allowed to travel to the hole.

The game can end in three ways:

- if ever the cat occupies the same node as the mouse, the cat wins;
- if ever the mouse reaches the hole, the mouse wins;
- if ever a position is repeated (the players are in the same positions
  as on a previous turn, and it is the same player's turn to move), the
  game is a draw.

Given `graph`, and assuming both players play optimally, return `1` if
the mouse wins, `2` if the cat wins, or `0` if the game is a draw.

```
graph = [[2,5],[3],[0,4,5],[1,4,5],[2,3],[0,2,3]]  ->  0
graph = [[1,3],[0],[3],[0,2]]                      ->  1
```

**Constraints:** `3 <= graph.length <= 50`,
`1 <= graph[i].length < graph.length`, `0 <= graph[i][j] < graph.length`,
`graph[i][j] != i`, `graph[i]` is unique, and the mouse and the cat can
always move.

## Approaches

A position is the mouse's node, the cat's node and whose move it is:
`n * n * 2` positions, at most 5,000.

| file | mechanism |
|---|---|
| `cat_mouse_game.kara` ★ | retrograde analysis with a queue: the game's ends settled first (the mouse in the hole, the cat on the mouse), then each settled position examined for the positions one move before it. The player to move there wins if one move reaches its own win; it loses once a count of its moves not yet known to lose reaches zero. What is never settled is a draw. O(n^3) |
| `cat_mouse_game_rounds.kara` | every unsettled position swept, settled by the same two rules from its moves, sweep after sweep until one settles nothing. O(n^4) at worst |
| `cat_mouse_game_attractors.kara` | each player's winning region grown on its own, with a stack: the mouse's from the hole, the cat's from the cat on the mouse, each a position where the region's owner has one move into it or the other player only moves into it. A start in neither is a draw. O(n^3) for each |
| `cat_mouse_game_recursive.kara` | the ★ arm's retrograde analysis, but a position settled passes the news to the positions before it at once, by recursion, rather than through a queue |
| `cat_mouse_game_bitsets.kara` | for each cat position four sets of mouse positions (won by each player, with each to move), each an `i64`, swept until none grows; the cat's move is an OR over its neighbours' sets for a win and an AND for a loss |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's two examples and three
more (the cat forcing the mouse onto it on three nodes, a triangle where
the mouse steps into the hole, a cat win on five nodes); for 300 random
graphs of 3 to 50 nodes at four densities, the count of each outcome
(110 draws, 132 mouse wins, 58 cat wins) and a checksum; and three
graphs of 50 nodes, sparse, middling and with every edge away from the
hole. `cat_mouse_game.py` mirrors the ★ arm and its output is
byte-identical.

The random graphs take each edge with a chance in 1,000 (a quarter of it
for edges at the hole, or the mouse wins too often), then mend the graph
so that every node has a neighbour and every node but the hole has one
other than the hole: the statement's "the mouse and the cat can always
move".

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the game played out move by move from the start, each player
taking its best outcome over its moves (the mouse its win, then a draw;
the cat its win, then a draw), with the positions earlier in this game
kept so that returning to one is the draw the statement names. That is a
search over every line of play, exponential in the graph, so it runs
only on graphs of up to 6 nodes: in a Python prototype the worst of
3,000 graphs of up to 7 nodes took 2.9 million calls, against 1,843 for
up to 6.

It checks 3,200 random graphs: 3,000 of 3 to 6 nodes at any density
against the statement, and 200 of 7 to 12 nodes at the harness's four
densities against the other properties, 15,375 nodes in all. The ★ arm
finds 142 draws, 1,369 mouse wins and 1,689 cat wins among them; only 78
of the 3,000 small graphs are draws, since a cat on so few nodes rarely
has room to guard without being dodged. The harness's 300 graphs, of up
to 50 nodes, are 37% draws.

| | property |
|---|---|
| P1 | the outcome of the game played out as the statement says, on the small graphs |
| P2 | the same outcome with the nodes other than 0, 1 and 2 renamed at random and every list of neighbours reversed |
| P3 | the same outcome with a separate component of two nodes joined to each other added |
| P4 | an edge to the hole added, from a node not yet next to it: no worse for the mouse |
| P5 | an edge to the hole removed, when the hole keeps another: no better for the mouse |
| P6 | each arm agrees with at least two of the other four |

P4 and P5 hold because only the mouse can use an edge at the hole. P2 to
P6 are checked on every graph. It prints `3200 graphs, 15375 nodes, 142
draws, 1369 mouse wins, 1689 cat wins, 95000 checks over 5 arms: 0
failures` under `karac __mir-run` and `karac __mir-llvm-run`, and the
same under `karac __mir-llvm-asan` with no error.

The large graphs stop at 12 nodes to keep the differential near half a
minute under `karac __mir-run`: at 7 to 48 nodes it took 3 min 44 s
there (2 s compiled), and the harness already covers graphs of up to 50.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-llvm-run`. All fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a mouse win taken back to where the mouse moved as if it were a loss | P1 1732, P6 1837 |
| M2 | ★: the cat counted as able to move into the hole | P1 18, P4 111, P5 6, P6 18 |
| M3 | ★: the start read with the cat to move | P1 1085, P6 1118 |
| M4 | rounds: the cat winning where one move is not a loss | P1 260, P6 367 |
| M5 | rounds: the mouse at node 1 never settled | P1 2922, P6 3058 |
| M6 | rounds: the game's ends not marked with the cat to move | P1 2592, P6 2707 |
| M7 | attractors: the players' roles swapped in growing | P1 1321, P6 1408 |
| M8 | attractors: the cat on the mouse not a finished game | P1 1616, P6 1673 |
| M9 | attractors: the cat's region grown for the mouse | P1 28, P6 39 |
| M10 | recursive: the cat's wins never spread | P1 1629, P6 1689 |
| M11 | recursive: two of the mouse's moves struck off for each loss | P1 1225, P2 6, P4 42, P5 9, P6 1285 |
| M12 | recursive: the cat's move taken back to the mouse's turn | P1 1289, P6 1366 |
| M13 | bitsets: the cat on the mouse let into the mouse's set | P1 187, P2 3, P6 198 |
| M14 | bitsets: the hole alone not a winning move | P1 1293, P6 1369 |
| M15 | bitsets: the last node never settled for the mouse to move | P1 414, P2 238, P3 440, P6 440 |

P1 and P6 kill all fifteen; P2 three, P4 and P5 two each, P3 one. Most
mutants compute a wrong game that is still a game: it does not depend
on the nodes' names or on a part of the graph neither player can reach,
so P2 and P3 cannot see it, and it still rewards the mouse for an edge
at the hole, so P4 and P5 cannot either. P3 sees M15 because the two
new nodes come last, so the node M15 skips is no longer one the game
uses, and P2 sees it because renaming changes which node comes last. Why P2 also sees M11
and M13, and P4 and P5 see M11, was not traced; P4 and P5 see M2
because its cat counts a move into the hole, so an edge at the hole
changes the cat's count as well as the mouse's moves.

One mutant was replaced. The first M6 let the rounds arm's cat count a
move into the hole; it is the same mistake as M2 in the ★ arm, and it
failed exactly the same checks (P1 18, P4 111, P5 6, P6 18), so it told
nothing new.

## Verification

Every arm prints the same output as `cat_mouse_game.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build and the runtime archives are both at
kara `5502146bed`. Under `karac __mir-run` the arms take 3.2 to 25 s
each (the rounds arm the longest) and the differential 37 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

Writing the harness found
[B-2026-10-23-11](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl):
`for per in vec![30, 100, 1000] { let mut seed2 = per; ... random_graph(mut seed2, 50, per) ... }`
is refused by `karac check`, `karac run` and `karac build` ("`seed2` is
a `ref` to an element of the collection the `for` iterates"), though
core-semantics.md says a `let mut` of a reference to a `Copy` value
copies it; `karac __mir-run` runs it. The harness draws those three
graphs from its one generator instead, which is as natural, so the kata
does not depend on the fix.

The frozen legacy interpreter, JIT and builds refuse every arm, the
differential and the bench program at the first `*d` on an element of
`graph[c].iter()`: "unary '*' requires 'ref T', 'mut ref T', or a raw
pointer ..., found 'i64'; a 'i64' is copied, so drop the `*`". That is
legacy's older rule for iterating a `Vec[i64]`; under v2 the element is
a reference and the `*` is required. Legacy is frozen, so none of this
is filed.

## Benchmarks

The bench program uses the ★ arm on 4,000 random graphs of 50 nodes,
the four densities in turn, each graph built and then solved. Every
implementation prints `4000 graphs of 50 nodes: 1802 draws, 2025 mouse
wins, 173 cat wins, checksum 818740075`.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.69 to 0.80 s | 0.72 s |
| Rust (`rustc -O`) | 0.86 to 1.00 s | 0.90 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.87 to 1.07 s | 0.97 s |
| Go | 1.08 to 1.19 s | 1.15 s |
| Python | 22.1 s | |
| Kāra (`karac build --mir`) | 0.89 to 0.99 s | 0.96 s |

Legacy cannot build the bench program (above), so it has no row.
`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does.

v2 takes 0.99 times Rust's median time under overflow checks and 1.33
times C's. Under valgrind's cachegrind v2 runs 4.87 billion instructions
and 1.64 billion branches, against 4.87 billion and 1.51 billion for
Rust with overflow checks and 2.75 billion and 0.80 billion for C; all
three mispredict 54 to 58 million branches. The C program keeps each
node's neighbours in an array sized for the whole graph and its queue in
one allocation, while the Kāra and Rust programs grow theirs by pushing;
whether that accounts for C's fewer instructions was not profiled.
