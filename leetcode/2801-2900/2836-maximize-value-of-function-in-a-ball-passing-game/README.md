# 2836. Maximize Value of Function in a Ball Passing Game

You are given an integer array `receiver` of length `n` and an integer
`k`. `n` players are playing a ball-passing game.

You choose the starting player, `i`. The game proceeds as follows:
player `i` passes the ball to player `receiver[i]`, who then passes it
to `receiver[receiver[i]]`, and so on, for `k` passes in total. The
game's score is the sum of the indices of the players who touched the
ball, including repetitions, i.e. `i + receiver[i] +
receiver[receiver[i]] + ... + receiver^(k)[i]`.

Return the **maximum** possible score.

**Notes:** `receiver` may contain duplicates, and `receiver[i]` may be
equal to `i`.

```
receiver = [2,0,1], k = 4        ->  6
receiver = [1,1,1,2,3], k = 3    ->  10
```

**Constraints:** `1 <= receiver.length == n <= 10^5`; `0 <= receiver[i]
<= n - 1`; `1 <= k <= 10^10`.

## Approaches

| file | mechanism |
|---|---|
| `ball.kara` ★ | binary lifting: jump[j][i], where the ball is 2^j passes after player i holds it, and gain[j][i], the ids on the way, each level built from the one below by `map(..).collect()`; k's bits then walk any start in 34 steps |
| `ball_pairs.kara` | doubling over one `Vec[(i64, i64)]` of (where to, what gained) per block of passes, squared level by level while k's bits, low to high, are folded into every start's pair at once; no table is kept |
| `ball_cycle.kara` | each start walked until a player comes round again: the step each player was first reached at gives the cycle's start and length, so the rest of the k passes are whole laps of its sum and a part lap; O(n) a start, for the harness's sizes |
| `ball_tree.kara` | the graph's shape, O(n) in all: cycles found by a three-state walk into a struct of prefix sums over each cycle written twice, read by a method; trees hanging into them walked depth first up the reversed edges with a stack, prefix sums kept along the path to the cycle |
| `ball_solution.kara` | a Rust solution as LeetCode's Rust users write it: `vec![vec![(0usize, 0i64); n]; 35]` for the lifted jumps and sums, destructured with `let (mid, s1) = f[j - 1][i]`, `k` walked by its bits, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 5 lines: LeetCode's two examples; one
player; 10^5 players, LeetCode's most, each keeping the ball, with k =
10^10, LeetCode's most; then 3000 random games of 1 to 8 players with
k up to 20, and 100 of up to 2000 players with k up to 10^10, as
checksums. `ball.py` mirrors the ★ arm and its output is
byte-identical.

```
6 10
0
999990000099999
3000 small games: checksum 763755569
100 large games: checksum 994263367
```

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: from every start, the ball passed k times one pass at
a time, the ids added, and the most. It draws 2000 random games of 1
to 8 players with k up to 20, then 50 of up to 1500 players with k up
to 10^10, all before any arm answers; the literal reading is asked only
of the first 2000.

| | property |
|---|---|
| P1 | k up to 20, the answer is the literal reading's |
| P2 | k one larger: no smaller |
| P3 | every player keeping the ball: (n - 1)(k + 1) |
| P4 | a player n added who passes to player 0: no smaller, and at least n |
| P5 | from n - 1 to (n - 1)(k + 1) |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2050 cases: checksum 488808332, 61500 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases gives the same checksum. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: one level short of k's top bit | P3 2, P6 2 |
| M2 | ★: the start's own id left out | P1 1660, P3 1772, P4 508, P5 130, P6 1710 |
| M3 | pairs: the block squared before the bit is folded in | P1 1575, P3 1772, P5 1023, P6 1625 |
| M4 | pairs: the gain of a block not doubled | P1 1487, P2 426, P3 1673, P6 1537 |
| M5 | cycle: the lap measured one long | P1 1203, P3 1579, P6 1253 |
| M6 | cycle: the part lap left out | P1 285, P6 311 |
| M7 | tree: the cycle entered one place on | P1 476, P6 502 |
| M8 | tree: a tree player's passes all taken down the path | killed under both: runtime error: index out of bounds |
| M9 | solution: the start's id left out | P1 1660, P3 1772, P4 508, P5 130, P6 1710 |
| M10 | solution: the lifted sum takes only its first half | P1 1487, P2 426, P3 1673, P6 1537 |

## Benchmarks

The bench draws 10 games of 10^5 players with k up to 10^10,
LeetCode's most, all of them first, then answers each 3 times by the ★
arm in all five languages; each answer builds its 34 levels afresh.
Every implementation prints `10 games of 100000, 3 rounds: checksum
365545195`.

BENCHTAB

## Verification

All five arms print the same output as `ball.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The four own arms checked clean as first written.

LeetCode's Rust template took 13 `karac fix` edits in one run, the
wrapper included: `struct Solution {}` added for the `impl`; `Vec<..>`
became `Vec[..]`; `vec![vec![(0usize, 0i64); n]; 35]` became
`Vec.filled(35, Vec.filled(n, (0, 0)))`, both suffixes gone, `usize`
being `i64` in Kāra and `i64` the default; `receiver[i] as usize`
became `as i64` and `let mut sum = i as i64` lost its cast;
`Solution::` took `.`, and `|&v|` lost its `&`. The destructuring
`let (mid, s1) = f[j - 1][i]` of an element read out of the table was
accepted as written.
