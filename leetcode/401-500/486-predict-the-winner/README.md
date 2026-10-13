# 486. Predict the Winner

You are given an integer array `nums`. Two players are playing a game
with this array: player 1 and player 2.

Player 1 and player 2 take turns, with player 1 starting first. Both
players start the game with a score of 0. At each turn, the player
takes one of the numbers from either end of the array (i.e. `nums[0]`
or `nums[nums.length - 1]`), which reduces the size of the array by 1.
The player adds the chosen number to their score. The game ends when
there are no more elements in the array.

Return `true` if player 1 can win the game. If the scores of both
players are equal, then player 1 is still the winner, and you should
also return `true`. You may assume that both players are playing
optimally.

```
nums = [1,5,2]      ->  false
nums = [1,5,233,7]  ->  true
```

**Constraints:** `1 <= nums.length <= 20`; `0 <= nums[i] <= 10^7`.

## Approaches

Every arm is `fn predict_the_winner(nums: Vec[i64]) -> bool`, and
borrows the array.

| file | mechanism |
|---|---|
| `predict_the_winner.kara` ★ | the lead, the most the player to move can finish ahead by on `nums[i..=j]`, is the end taken minus the other player's lead on what is left; filled from the right in one row, overwritten in place. O(n²) time, O(n) space |
| `predict_the_winner_memo.kara` | the same lead, recursively, each interval worked out once and kept in a `Vec[Option[i64]]` at `i × n + j` |
| `predict_the_winner_score.kara` | the most the player to move can collect: everything in the interval less the most the other player then collects, intervals shortest first, prefix sums for the totals; player 1 wins with at least half the whole |
| `predict_the_winner_minimax.kara` | every game played out with nothing remembered, player 1's total maximized on player 1's moves and minimized on player 2's. O(2^n), which `n <= 20` allows |
| `differential.kara` | the four arms on 1,500 random arrays, five properties |

Every arm prints the same 10 lines: the two LeetCode examples, a lone 7
and a lone 0, `[1, 2, 1]` (a tie, so a win), two arrays of five, 20
numbers (the problem's most) with `10^7` at both ends, 19 numbers from
1 to 9, and for 300 random arrays (1 to 12 numbers from 0 to 20, or
from 0 to `10^7` in one array in five) the number player 1 wins and a
checksum. `predict_the_winner.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and runs them on
1,500 random arrays of 1 to 10 numbers from 0 to 20, or from 0 to
`10^6` in one array in five.

| | property |
|---|---|
| P1 | the answer is whether player 1 collects at least as much as player 2 when the game is played out with both totals kept, each player taking the end that leaves them the most |
| P2 | an array of even length is a win for player 1 |
| P3 | the array reversed gives the same answer |
| P4 | every number times `k` (1 to 5) gives the same answer |
| P5 | a number at least the sum of all the others, added at either end, makes a win for player 1 |

P1's game is a third formulation: each player maximizes their own
total, where the arms count a lead or minimize the other's total. P2
holds because player 1 can take every number at an even index, or every
one at an odd index, whichever sum is larger. P5 holds because player 1
can take the big number first. It prints `1500 cases, 4 arms, 32916
checks, 0 failures` under `karac __mir-run`, in 4.8 s, and a count for
each property when anything fails.

## Mutation testing

Eight edits to `differential.kara`, two to each arm, each run under
`karac __mir-run`. All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a tie goes to player 2 | P1 42, P2 14, P5 70 |
| M2 | ★: taking the right end subtracts the wrong lead | P1 274, P2 170, P3 389 |
| M3 | memo: an interval is remembered at `i + j` | P1 123, P2 28, P3 121 |
| M4 | memo: a lone number is a lead of 0 | P1 76 |
| M5 | score: the mover leaves the larger of the two | P1 892, P2 716, P5 1470 |
| M6 | score: the whole is counted without its last number | P1 90, P3 57 |
| M7 | minimax: player 2 takes the end that leaves player 1 the most | P1 176 |
| M8 | minimax: taking the left end does not pass the turn | P1 176 |

M7 and M8 make the minimax arm answer `true` for every array: under M7
player 2 plays for player 1, and under M8 player 1 may take every
number from the left. Both fail exactly the 176 random arrays player 1
loses, which only P1 can see, since every other property expects a win
or the same answer twice. M4 never counts the last number taken; the
properties other than P1 hold for it all the same. M1 fails only on
ties, which reversing and scaling keep, so P3 and P4 are blind to it,
and M6 leaves out a number that reversing moves, so P3 sees it where
P2 and P5 do not.

## Verification

All four arms print the same output as `predict_the_winner.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and `karac check` passes on every file, the bench program included. The
differential prints `32916 checks, 0 failures` on both. The four arms
and the differential also run clean under `karac __mir-llvm-asan`
(AddressSanitizer and LeakSanitizer): output identical, no error, no
leak.

On the frozen legacy backends, the ★ and memo arms print the same
output under `karac run --interp`, LLJIT, legacy `karac build` and a
`KARAC_AUTO_PAR=1` build. The minimax arm does too under the three
compiled ones, but `karac run --interp` had not finished it after 300 s
(the MIR interpreter takes 5.8 s; the 20-number case is about two
million calls). LLJIT and legacy `karac build` refuse the score arm and
the differential, which holds a copy of it: "chained indexed receivers
(`a[i][j].min(...)`) are deferred to v1.x; bind the inner element to a
temporary first", on `best[i + 1][j].min(best[i][j - 1])`. The legacy
interpreter runs both, and prints `0 failures` on the differential.
Legacy `karac build` also warns that `nums` is "moved here, used again
here" wherever a function lends the array twice in one expression.
Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It builds 200 arrays of 1,000 or
1,001 numbers from 0 to `10^7` once, then solves each once. That is far
past the problem's 20: the ★ arm is O(n²), so a 20-number solve is too
short to time, and timing the same call many times invites a compiler
to hoist it out of the loop. Every implementation prints `200 arrays of
1000 or 1001 numbers: player 1 wins 101, checksum 230119920`, the Kāra
program under `karac __mir-run` included (in 62 s). The 100 even-length
arrays are all wins (see P2); of the 100 odd-length ones, player 1 wins
one.

Every mirror copies the array into one row of leads and overwrites it
in place, as the Kāra arm does. Spot timings on a shared 4-core
container, three runs each (two for Python; `bench.sh` timings need a
quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.10 s |
| Rust (`rustc -O`) | 0.10 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.26 to 0.27 s |
| Go | 0.28 to 0.29 s |
| Python | 14.7 to 15.3 s |
| Kāra (`karac build`) | 0.29 to 0.30 s |
| Kāra (`karac build --mir`) | 0.26 to 0.30 s |

Both Kāra builds check the subtraction in the inner loop for overflow,
as Rust does with `overflow-checks=on`, and land beside that row rather
than beside plain `rustc -O` (inferred, not profiled). The legacy
`karac build` builds and runs this program correctly, so `bench.sh` is
the `scripts/new-bench.sh` output unchanged and times that build. The
`--mir` row is the v2 compiled backend, timed for comparison. Both Kāra
rows are timed at kara `b0b1557b39`. Under `karac __mir-llvm-run` the
program prints the same line in 1.2 s, compile included; that JITs the
MIR's IR without optimization passes, so it is not a benchmark.

## Compiler findings

None. Every arm, the differential and the bench program ran first time
on the v2 backends.
