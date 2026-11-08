# 2029. Stone Game IX

Alice and Bob take turns, Alice first, removing one stone at a time from a
row of stones with values `stones[i]`. The player who removes a stone loses
if the sum of all the stones removed so far is divisible by 3. If no stones
are left, Bob wins, even on Alice's turn. Both play optimally; return
whether Alice wins.

```
stones = [2,1]          ->  true
stones = [2]            ->  false
stones = [5,1,2,4,3]    ->  false
```

**Constraints:** `1 <= stones.length <= 10^5`; `1 <= stones[i] <= 10^4`.

Only a stone's value mod 3 matters. A stone worth 0 changes the sum by
nothing and only passes the turn, so only the parity of their count
matters. A player whose sum is 1 mod 3 cannot take a 2 and one at 2 mod 3
cannot take a 1, so after Alice's opening the 1s and 2s go in a forced
order, `a, a, b, a, b, ...`. With an even count of 0s Alice wins when she
has both a 1 and a 2; with an odd count, when one side outnumbers the other
by more than 2.

## Approaches

| file | mechanism |
|---|---|
| `stones.kara` ★ | the residues counted in an array of 3, then the rule on the parity of the 0s. O(n) |
| `stones_play.kara` | the forced order played out on the counts from each opening, every 0 spent as a pass, the player who cannot follow it stuck. O(n) |
| `stones_fold.kara` | the residues counted by `fold` into a tuple, the rule as a `match` on the parity of the 0s. O(n) |
| `stones_sorted.kara` | the residues tallied in a `SortedMap` through `entry(..).or_insert(0)`; the length of each opening's forced run counted in closed form from the tallies. O(n) |
| `stones_buckets.kara` | the stones dealt into three piles by residue and each game played by taking stones off them, a 0 taken only when the order's pile is empty. O(n) |
| `stones_solution.kara` | LeetCode's Rust template (a unit struct, `impl Solution`, `Vec<i32>`, a `[0; 3]` array, `for &s in &stones`, `as usize`, `&&`, a `&Vec` wrapper with `|&x|`), carried by `karac fix` to a clean check |
| `differential.kara` | all six arms against the statement read literally, six properties |

Every arm prints the same 10 lines: the answers for LeetCode's three
examples and five more; then how often Alice wins and a checksum of the
answers for 3000 games of 1 to 20 stones up to 30, the 0s and 1s at odds
of their own, and for 8 games of 100000 stones up to 10000.
`stones.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: a search over every stone each player could take, by the set of
stones taken (a bitmask) and their sum, never by residues. It checks 1500
games of 1 to 8 stones up to 30. Every random choice of a game is drawn
before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | with a stone worth 3 appended, the answer is still the statement read literally |
| P3 | with a stone worth 1 appended, the answer is still the statement read literally |
| P4 | every stone worth 1 mod 3 raised by 1 and every one worth 2 mod 3 lowered by 1, swapping the two residues, leaves the answer |
| P5 | two stones worth 3 appended leave the answer |
| P6 | each arm agrees with at least three of the other five |

P2 and P3 judge each arm's answer to a neighbouring game the way P1 judges
the original: one more 0 flips the parity that decides which rule applies,
and one more 1 moves the counts across the rule's thresholds. P4 holds
because the game is the same with the names of the residues 1 and 2
swapped; P5 because two passes give the turn back.

The differential prints `1500 games: checksum 641080700, 54000 checks over
6 arms: 0 failures` under every lane in Verification. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Thirty edits to the differential, five to each of its arms, each run under
`karac __mir-run` and `karac __mir-llvm-run`. Seventeen are kept, three to
each of the five Kāra arms and two to the Rust arm. All thirty are killed,
each fails the same way under both backends, none by a crash, and no two
kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the 0s' parity read the wrong way round | P1 760, P2 760, P3 1076, P6 760 |
| M2 | ★: an even count of 0s won with a 1 or a 2 | P1 322, P2 299, P3 226, P6 322 |
| M3 | ★: each residue counted at most once | P1 354, P2 397, P3 480, P5 87, P6 354 |
| M4 | play: the opening stone never taken | P1 281, P2 263, P3 357, P6 281 |
| M5 | play: the total never moved on | P1 292, P2 289, P3 429, P6 292 |
| M6 | play: a game with no stones left won | P1 328, P2 312, P3 233, P6 328 |
| M7 | fold: the 1s counted as 2s | P1 610, P2 596, P3 886, P6 610 |
| M8 | fold: an even count of 0s won with a 1 alone | P1 170, P2 151, P3 226, P4 322, P6 170 |
| M9 | fold: a gap of 2 enough for the 2s | P1 69, P2 69, P3 24, P4 138, P6 69 |
| M10 | sorted: a run of the opening residue one move longer | P1 576, P2 548, P3 808, P6 576 |
| M11 | sorted: a run of the other residue one move shorter | P1 200, P2 199, P3 283, P6 200 |
| M12 | sorted: an opening with no stone of it tried | P1 244, P2 413, P3 163, P5 134, P6 244 |
| M13 | buckets: the total raised by 1 whatever was taken | P1 29, P2 11, P3 43, P4 24, P5 29, P6 29 |
| M14 | buckets: the stuck player always Bob | P1 358, P2 402, P3 522, P6 358 |
| M15 | buckets: the 2s left out of the stones left | P1 154, P2 142, P3 102, P4 298, P6 154 |
| M16 | Rust: the 0s' count taken mod 3 | P1 448, P2 510, P3 562, P5 530, P6 448 |
| M17 | Rust: every residue turned one up | P1 652, P2 766, P3 891, P4 652, P5 350, P6 652 |

P1, P2, P3 and P6 kill all seventeen, P4 and P5 five each. P2 and P3 ask
the arm about a neighbouring game and judge it by the literal search, so
they see every edit P1 sees, at counts of their own: one more 0 moves a
game to the other rule, one more 1 moves the counts across its thresholds.
P4 swaps the residues 1 and 2, so it sees the edits that treat them
unevenly: an even count of 0s won with a 1 alone (M8), a gap enough for the
2s at 2 (M9), the total always raised by 1 (M13), the 2s left out of the
stones left (M15), and every residue turned one up (M17). P5 adds two 0s,
which only an arm reading more of the 0s' count than its parity notices:
each residue counted at most once (M3), an opening with no stone of it
tried, whose run length goes negative and lets the 0s decide (M12), the
total raised by 1 (M13), the count taken mod 3 (M16), and the residues
turned up, which makes the 2s into 0s (M17).

The other thirteen fail as a kept one does, or with counts of their own.
Alice's turns read the wrong way round fail as M1 in the play and buckets
arms (the stuck player on an even move, Alice to move after her opening),
and the sorted arm's game with no stones left won as M6. The play arm's
0s never spent, the fold arm's 0s never counted and the Rust arm's every
stone counted twice fail alike: each leaves the count of 0s even. Only
more 1s than 2s counted as a gap (★, fold) fail alike, as do only the
opening 1 tried (sorted, buckets). The ★ arm's gap of 2 enough, and the
Rust arm's gap of 3 needed and its two 2s needed, fail with counts of their
own. Two drafts were replaced: the play arm wanting the other residue next
reaches a total of 0 and indexes a fourth count, which stops the program
("index out of bounds"); and the sorted arm comparing its runs one apart
changes the moves only where `b = a - 1`, where both readings use every
stone and Bob wins either way.

## Verification

Every arm prints the same output as `stones.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every arm
and the differential. `karac check --output=json` reports nothing on any
of them. Under `karac __mir-run` the arms take 1.9 s to 3.0 s, most of it
the eight games of 100000 stones, and the differential 4.4 s.

The five arms were written in Kāra and checked clean but one: the buckets
arm first took its piles as `piles: Vec[Vec[i64]]` and wrote `let mut
piles = piles;`, Rust's way to change an owned argument. A bare parameter
borrows in Kāra, so each `pop` on it was refused, with the reason and a
machine fix to `piles: own Vec[Vec[i64]]`, which `karac fix` applied.

The Rust arm was written as LeetCode's Rust template and reaches a clean
check through `karac fix` alone, in two rounds (11 and 1 edits). The first
carries the unit struct, `Vec<..>` twice, the `&` in `for &s in &stones`
and in `|&x|`, `&&`, the `&Vec` parameter and the `::` path; the second
drops the wrapper's `ref`. `cnt[(s % 3) as usize]` keeps its `usize`,
which indexes an array as well. The `[0; 3]` array's `0` takes the default
`i64` where Rust's is `i32`, but nothing here mixes it with an `i32`, so
nothing needs a fix.

## Benchmarks

The bench builds 20 games of 100000 stones once in all five languages,
game `a` with odds `a % 5` in 10 of a 0 and `3 a % 11` in 10 of a 1 among
the rest, then runs 100 rounds, each adding 1 to one stone of each game
before the ★ arm answers it: 2000 calls, each a pass over 100000 stones.
Every implementation prints `2000 calls: Alice wins 1938, checksum
737195199`.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with kara `64bba595f2` on LLVM 22:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 0.351 to 0.439 s | 0.373 s |
| C (`clang -O3`) | 0.359 to 0.397 s | 0.377 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.349 to 0.463 s | 0.380 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.356 to 0.444 s | 0.392 s |
| Rust (`rustc -O`) | 0.350 to 0.449 s | 0.394 s |
| Go | 0.413 to 0.558 s | 0.446 s |
| Python | 12.8 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`, the
sequential lane. A plain `karac build` parallelizes nothing here: its user
time (0.354 s) is not above its real time (0.373 s).

The sequential Kāra program is 0.97x Rust under overflow checks and 1.01x
C.