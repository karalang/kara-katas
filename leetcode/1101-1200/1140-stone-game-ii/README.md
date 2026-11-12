# 1140. Stone Game II

Alice and Bob continue their games with piles of stones. There are a
number of piles arranged in a row, and each pile has a positive integer
number of stones `piles[i]`. The objective of the game is to end with the
most stones.

Alice and Bob take turns, with Alice starting first. Initially, `M = 1`.

On each player's turn, that player can take all the stones in the first
`X` remaining piles, where `1 <= X <= 2M`. Then, we set `M = max(M, X)`.

The game continues until all the stones have been taken.

Assuming Alice and Bob play optimally, return the maximum number of
stones Alice can get.

```
piles = [2,7,9,4,4]        ->  10
piles = [1,2,3,4,5,100]    ->  104
```

**Constraints:** `1 <= piles.length <= 100`; `1 <= piles[i] <= 10^4`.

The arms are `fn stone_game_ii(piles: Vec[i64]) -> i64`.

## Approaches

| file | mechanism |
|---|---|
| `stone_game_ii.kara` ★ | a table of the most the player to move can take from pile `i` on with `M = m`, filled from the last pile back in nested `Vec.filled` rows: all that is left when `2m` piles reach the end, otherwise what is left less the least the other player can be held to, over every first move of 1 to `2m` piles. O(n^3) |
| `stone_game_ii_memo.kara` | the same recursion top down, each position remembered once found in a table passed down as `mut ref`. O(n^3) |
| `stone_game_ii_minimax.kara` | the game as two players: Alice takes the move that gives her the most, Bob the one that leaves her the least, each position keyed by the pile, `M` and whose turn it is in a `Map[(i64, i64, bool), i64]`. O(n^3) |
| `stone_game_ii_lead.kara` | the lead: how many stones more than the other the player to move can end with, each move worth the piles it takes, from prefix sums, less the other's lead after it; Alice's stones are half of the total and her lead. O(n^3) |
| `stone_game_ii_solution.kara` | a Rust solution as LeetCode's Rust users write it (`impl Solution`, `piles: Vec<i32>`, a `vec![0; n + 1]` suffix sum and a `vec![vec![0; n + 1]; n + 1]` table, `std::cmp::max`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five properties |

Every arm prints the same 11 lines: LeetCode's two examples; one pile;
two; a big pile third and fifth, beyond Alice's first move (2 and 3);
seven equal piles (16). Then over 2000 random rows of 1 to 30 piles, of
1 to 10000 stones or, every third row, 1 to 10, the answers summed and a
checksum (`2000 random rows: answers total 51099126, checksum
312447166`), and three of the largest rows the constraints allow, 100
piles: all 10000 (500000), 1 to 100 rising (2526), and 1 to 10000 at
random (238772). `stone_game_ii.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every way the game can go, the player to move taking 1 to 2M
piles and each player taking the most stones they can, with no table;
the stones Alice ends with. It checks 2000 rows of 1 to 12 piles in four
kinds of 500: 1 to 10000 stones; 1 to 3, so moves tie; 1 to 5 with one
pile of 1000 to 2000; and every pile the same. Every random choice, the
pile P5 raises and by how much among them, is drawn before any arm
answers.

| | property |
|---|---|
| P1 | the answer is the literal one |
| P2 | every pile three times as big gives three times the answer |
| P3 | the answer is at least the first two piles (or the only one) and at most every stone |
| P4 | the answer and the answer for the piles after the first sum to at least every stone: Alice may take one pile and leave Bob that game |
| P5 | a pile raised by 1 to 50 stones raises the answer by no less than 0 and no more than that |
| P6 | past two piles, the answer leaves Bob at least the smaller of the second and third pile |

All 57,415 checks pass on every arm: `2000 rows: checksum 193451456,
57415 checks over 5 arms: 0 failures`. A Python reading of the same
rows, by the same search, with the six properties asserted against the
★ arm's mirror, gives the same line.

## Mutation testing

Thirty edits to the differential, six to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run` with `KARAC_HASH_SEED=1`,
each failing the same way under both. Twenty-seven are caught; three are
equivalent. The ★ arm taking all that is left only when `2M` piles pass
the end (`>` for `>=`) changes nothing: at exactly the end its loop
tries every move, and the one that takes the rest is worth all of it.
The memo arm finding a position worth 0 again (`> 0` for `>= 0`) only
recomputes it: a position with a pile left is worth at least one stone.
The memo arm remembering a position as worth at most one stone less than
all that is left changes no value it remembers: a position remembered
is one where the other player moves again, and takes a pile. Fifteen are
kept, no two failing the same checks; two of them stop the run.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a first move of 2M piles never tried | P1 1549, P3 295 |
| M2 | ★: M never grows | P1 840 |
| M3 | ★: each pile one stone short | P1 2000, P2 2000, P3 765, P4 1246 |
| M4 | memo: M grows by each move | P1 1117, P4 750 |
| M5 | memo: each pile past the first costs a stone | P1 1520, P2 1642, P3 248 |
| M6 | memo: a first move of one pile never tried | P1 818, P4 824 |
| M7 | minimax: Bob plays for Alice | stops: integer overflow |
| M8 | minimax: every position remembered as Alice's | P1 626, P4 479 |
| M9 | minimax: the turn never passes | P1 1660, P6 1660 |
| M10 | lead: Bob's share returned | P1 1772, P3 686, P4 1823 |
| M11 | lead: the first pile of a move not counted | P1 1580, P2 900, P3 509, P4 1092, P6 10 |
| M12 | lead: M = n never filled | P1 177, P2 101, P3 177 |
| M13 | solution: all that is left taken when M piles reach the end | stops: index out of bounds |
| M14 | solution: piles counted at most 100 | P1 847, P2 1198, P3 705, P4 911 |
| M15 | solution: Alice never below half | P1 245, P2 136 |

P1 catches all thirteen edits that let the run finish. P3 and P4 catch
seven each. P3 sees an answer below what Alice's first move alone
gives: no move of two piles (M1), stones lost (M3, M5, M11, M14), Bob's
share returned (M10), and a lead table with its widest column empty
(M12). P4 sees an answer too small to cover the total with the answer
for the piles after the first: no move of one pile (M6), which is the
move P4's bound stands on, positions undervalued (M3, M4, M8, M11, M14),
and Bob's share (M10). P2 catches six, the edits whose answers do not
scale with the stones: a stone taken off per pile or per move (M3, M5),
piles capped (M14), and the lead arm's and M15's halving, whose rounding
changes when the total's parity does (M11, M12, M15). P6 catches the two
edits that leave Bob too little: the turn never passing (M9), which gives
Alice every stone, and, on ten rows, the lead arm's first pile not
counted (M11). Only P1 sees M
never growing (M2): the answers are those of a game played with M fixed
at 1, which keeps every bound and relation the properties check. P5
catches none of the thirty: every edit still answers with each pile's
stones counted once or not at all, and capped at most, so raising one
pile never lowers the answer or raises it by more than the stones added.
Of the two that stop the run, Bob playing for Alice starts his best at
`i64.MAX` and never brings it down, so Alice's stones added to it
overflow; and the solution arm taking the rest only when `M` piles reach
the end tries moves past the end of its table.

Of the twelve caught and not kept, six fail exactly as a kept one: a
first move of 2M piles never tried in the solution arm as M1; M the
smaller of the two in the solution arm as M2; the lead arm adding the
other's lead as M9; a move to the last pile never made in the minimax
arm stops on an integer overflow as M7 does; and the ★ arm started with M = 2 and the memo arm taking
the rest when M piles reach the end stop on an index out of bounds as
M13 does. The other six (M one more after every move in the ★ arm,
piles counted at most 5000 and Bob's least starting at 0 in the minimax
arm, at most M piles a move and a lead never below 0 in the lead arm,
and the first pile's row never filled in the solution arm) each fail in
a way of their own and were not needed.

## Verification

Every arm prints the same output as `stone_game_ii.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
every arm and the differential. `karac check --output=json` reports
nothing on any file, and `karac fix` has nothing to apply.

The ★, memo, minimax and lead arms were written as Kāra and checked
clean as written. `karac fix` carried the solution arm in five rounds:
`Vec<i32>` to `Vec[i32]`, `std::cmp::max` to `max` and `Solution::` to
`Solution.`; then `struct Solution {}` declared; then the suffix's
`vec!` to `Vec.filled`, `0i32` on the table's literal, and the `as i64`
that widens the call's `i32` for nothing dropped; then `0i32` on the
suffix's literal and the table's inner `vec!` to `Vec.filled`; then its
outer `vec!`.

The kata found no gaps.

## Benchmarks

The bench builds 20 rows of 100 piles of 1 to 10000 stones once,
LeetCode's longest. Each of 100 rounds draws one pile of every row again
and answers the row with the ★ arm: 2000 calls, each filling a 101 by
101 table, 83,300 moves tried. Every implementation prints `100
rounds over 20 rows of 100 piles: answers total 473828343, checksum
549690955`. Each makes the table row by row in every call: nested
`Vec.filled` in Kāra, `vec![vec![0; n + 1]; n + 1]` in Rust, `calloc`
in C, `make` in Go and list repetition in Python.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `828dd324e1`
on LLVM 22. karac builds for the x86-64-v3 baseline, so the C and
overflow-checked Rust programs are also built at `-march=x86-64-v3`:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.121 to 0.249 s | 0.151 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.105 to 0.269 s | 0.153 s |
| Rust (`rustc -O`) | 0.147 to 0.292 s | 0.189 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.156 to 0.343 s | 0.207 s |
| Kāra (`karac build`) | 0.184 to 0.346 s | 0.213 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.184 to 0.304 s | 0.234 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.192 to 0.327 s | 0.240 s |
| Go | 0.322 to 0.418 s | 0.349 s |
| Python | 17.2 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. The runs are short and their spreads wide, 0.13 to 0.16 s for
most rows. Rust under overflow checks takes about 0.86x to 0.98x Kāra's
median time, and Kāra checks every addition and subtraction the same
way; Rust without the checks takes about 0.79x and C about 0.63x. This
README has not measured where the rest of C's lead comes from. Go takes
about 1.45x Kāra's time and Python about 72x.
