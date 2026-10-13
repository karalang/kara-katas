# 488. Zuma Game

You are playing a variation of the game Zuma. There is a single row of
coloured balls on a board, where each ball can be red `R`, yellow `Y`,
blue `B`, green `G` or white `W`. You also have several coloured balls
in your hand.

Your goal is to clear all of the balls from the board. On each turn:

- pick any ball from your hand and insert it between two balls in the
  row or at either end of the row;
- if there is a group of three or more consecutive balls of the same
  colour, remove the group; if this removal makes more such groups,
  keep removing them until there are none left;
- if there are no balls left on the board, you win;
- repeat until you win or have no balls left in your hand.

Given the strings `board` and `hand`, return the minimum number of
balls you have to insert to clear the board, or `-1` if the balls in
your hand cannot clear it.

```
board = "WRRBBW",   hand = "RB"     ->  -1
board = "WWRRBBWW", hand = "WRBRW"  ->  2
board = "G",        hand = "GGGGG"  ->  2
```

**Constraints:** `1 <= board.length <= 16`; `1 <= hand.length <= 5`;
both are made of `R`, `Y`, `B`, `G` and `W`; the board starts with no
group of three or more of the same colour.

## Approaches

Every arm is `fn find_min_step(board: String, hand: String) -> i64`, and
borrows both strings. Every arm tries only the insertions that can help:
a ball at the start of a run of its own colour, or a ball splitting two
equal neighbours of another colour, which is what makes `RRWWRRBBRR`
with `WB` clearable (`W` between the last two `R`s, then `B` beside the
`BB`). After an insertion, only the run around the new ball can reach
three, so removing every run of three or more until none is left is the
same as removing the chain the rules describe.

| file | mechanism |
|---|---|
| `zuma_game.kara` ★ | breadth first over (board, sorted hand) states, a `Set[String]` of those seen; the first empty board is reached with the fewest balls. Removal rescans the whole row until nothing goes |
| `zuma_game_memo.kara` | depth first with a `Map[String, i64]` of the fewest balls from each state. Removal starts at the new ball and widens: when a run goes, the balls either side meet, and go too if they make three |
| `zuma_game_deepening.kara` | iterative deepening: can the board be cleared within 1 ball, 2, 3, ...? A plain depth-first search with nothing remembered, so the first yes is the fewest. Removal is one pass with a stack of (colour, count) |
| `zuma_game_counts.kara` | the hand as five counts, one per colour, borrowed `mut ref` down the search and put back after each try; depth first with a `Map` of states and the ★ arm's removal |
| `differential.kara` | the four arms on 1,000 random cases, five properties |

Every arm prints the same 10 lines: the three LeetCode examples,
`RRWWRRBBRR` with `WB` (2, by splitting), `RBYYBBRRB` with `YRBGB`, two
boards of 16 balls with hands of 5, two boards that cannot be cleared,
and for 300 random cases (a board of 1 to 10 balls with no three alike
in a row and a hand of 1 to 5, from the first 2 to 5 colours) how many
are cleared, with how many balls, and a checksum. `zuma_game.py`
mirrors the ★ arm and its output is byte-identical. The nine fixed
answers also agree with a Python search that tries every ball at every
position, with no pruning.

## Differential

`differential.kara` holds copies of the four arms and runs them on
1,000 random cases: a board of 1 to 7 balls with no three alike in a
row and a hand of 1 to 3, from the first 2 to 5 colours, except one case
in ten, which is a board of 10 balls in runs of one or two and a hand of
3, from 2 colours.

| | property |
|---|---|
| P1 | the answer is the fewest balls when every ball is tried at every position, with no pruning, and the chain removed one run at a time (a fifth removal, written apart from the arms') |
| P2 | the board reversed gives the same answer |
| P3 | the colours renamed (R to Y to B to G to W to R) give the same answer |
| P4 | one more ball in hand never makes the answer worse |
| P5 | the hand in another order gives the same answer, and it is -1 or from 1 to the hand's size |

The one case in ten is there for the splitting rule. A search in Python
over every board of up to 8 balls from 3 colours, with every hand of up
to 3, found none where splitting a pair pays; the first are at 9 balls
(`RRYRRYYRR` with `YYY`, 3). And on random boards of runs of one or two
from 2 colours, with hands of 3, it paid for 0 in 400 at 8 balls, 1 in
400 at 9 and 9 in 400 at 10. On the first draft of the differential
(1,500 boards of up to 7 balls) a mutant that never splits survived. It
prints `1000 cases, 4 arms, 20000 checks, 0 failures` under `karac
__mir-run`, in 31 s, and a count for each property when anything fails.
It is cut to 1,000 cases to stay under the corpus runner's 60 s limit.

## Mutation testing

Eight edits to `differential.kara`, two to each arm, each run under
`karac __mir-run`. All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a ball never splits two equal neighbours | P1 2 |
| M2 | ★: only a run of exactly three is removed | P1 28 |
| M3 | memo: the chain stops after the first run | P1 99 |
| M4 | memo: two balls meeting are enough to go | P1 87 |
| M5 | deepening: a run of exactly three stays on the stack | P1 107 |
| M6 | deepening: the budgets start at 2 | P1 47 |
| M7 | counts: a ball tried is not given back | the run stops: stack overflow |
| M8 | counts: a colour held only once is never played | P1 133 |

Only P1, which knows the answer, sees any of them: every mutant here is
a wrong rule applied the same way to a board and its mirror image,
under any names for the colours, so P2, P3 and P5 cannot tell, and none
of them happens to break P4. M1 fails on exactly two cases, both
`YYRRYYRRYY` with `RRR`, which starts with an `R` between the first two
`Y`s (or the last two).
Under M7 the count of the colour tried falls below zero, the `== 0`
test never stops it again, and the search recurses until the stack runs
out. One first draft survived and was replaced: "the state's key leaves
out the count of the last colour", which can merge two states only when
the same board is reached with different numbers of `W` left, and that
never happened on these cases.

## Verification

All four arms print the same output as `zuma_game.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and `karac check` passes on every file, the bench program included. The
differential prints `20000 checks, 0 failures` on both. The four arms
and the differential also run clean under `karac __mir-llvm-asan`
(AddressSanitizer and LeakSanitizer): output identical, no error, no
leak.

The frozen legacy backends agree on every arm: `karac run --interp`,
LLJIT, legacy `karac build` and a `KARAC_AUTO_PAR=1` build print the
same output, and the differential prints `0 failures` under the legacy
interpreter and legacy `karac build`. Legacy `karac build` warns on the
★ arm and the differential that `after` is "moved here, used again
here": it passes `after` to `key` before pushing it, which legacy reads
as a move and v2 as a borrow. Its output is right all the same. The
bench program does not build on legacy (see Benchmarks). Legacy is
frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It builds 60 cases at the problem's
limits once, a board of 16 balls with no three alike in a row and a
hand of 5, from the first 2 to 4 colours, then solves each once. Every
implementation prints `60 cases of 16 balls and a hand of 5: 19 cleared
with 56 balls, checksum 930155176`, the Kāra program under
`karac __mir-run` included (in 58 s). Most cases cannot be cleared, so
most of the time goes on searching every state a hand of 5 can reach.

Every mirror keeps the same levels of (board, sorted hand) states and a
hash set of state strings: Rust `HashSet<String>`, Go a
`map[string]struct{}`, Python a `set`, and in C an open-addressing
table written out by hand, since C has none (with an FNV-1a hash, where
the others use their language's default hasher). Spot timings on a
shared 4-core container, three runs each (two for Python; `bench.sh`
timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.26 to 0.31 s |
| Rust (`rustc -O`) | 0.46 to 0.55 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.42 to 0.58 s |
| Go | 0.55 to 0.63 s |
| Python | 6.1 to 6.2 s |
| Kāra (`karac build --mir`) | 0.68 to 0.71 s |

The legacy `karac build` refuses this program: "cannot move out of an
index expression", on `find_min_step(boards[k], hands[k])`, which v2
reads as two borrows. So `bench.sh` builds the Kāra program with
`karac build --mir`, the v2 compiled backend. That edit is by hand, on
top of the `scripts/new-bench.sh` output. The `--mir` row is timed at
kara `aebbc5cf99`. Under `karac __mir-llvm-run` the program prints the
same line in 5.5 s, compile included; that JITs the MIR's IR without
optimization passes, so it is not a benchmark.

## Compiler findings

None. Every arm, the differential and the bench program ran first time
on the v2 backends.
