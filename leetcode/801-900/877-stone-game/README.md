# 877. Stone Game

Alice and Bob play a game with piles of stones. There are an even number
of piles arranged in a row, and each pile has a positive integer number
of stones `piles[i]`. The objective of the game is to end with the most
stones. The total number of stones across all the piles is odd, so there
are no ties. Alice and Bob take turns, with Alice starting first. Each
turn, a player takes the entire pile of stones either from the beginning
or from the end of the row. This continues until there are no more
piles left, at which point the person with the most stones wins.
Assuming Alice and Bob play optimally, return `true` if Alice wins the
game, or `false` if Bob wins.

```
piles = [5,3,4,5]  ->  true
piles = [3,7,2,3]  ->  true
```

**Constraints:** `2 <= piles.length <= 500`, `piles.length` is even,
`1 <= piles[i] <= 500`, and `sum(piles[i])` is odd.

## Approaches

| file | mechanism |
|---|---|
| `stone_game.kara` ★ | the best margin of every run of piles: whoever moves on the piles i..j takes pile i or pile j and leaves the other player to move on the rest, so the mover's best margin is `max(piles[i] - margin[i + 1][j], piles[j] - margin[i][j - 1])`, filled in for runs of growing length. Alice wins when her margin over the whole row is above 0. O(n^2) time and space |
| `stone_game_memo.kara` | the same margin by memoized recursion: `best(i, j)` takes the better end, and a `Map` keyed by the run keeps each answer. O(n^2) |
| `stone_game_rolling.kara` | the margins in one row: a run's margin needs only the margins one pile shorter, so one `Vec` holds a whole length's margins and each pass overwrites it in place. O(n^2) time, O(n) space |
| `stone_game_totals.kara` | the best total rather than the margin: the mover ends with the run's total less what the other player gets on the rest, `best[i][j] = sum(i..j) - min(best[i + 1][j], best[i][j - 1])`, with prefix sums; Alice wins with more than half of all the stones. O(n^2) |
| `stone_game_parity.kara` | the first player's strategy: with an even number of piles Alice can take every pile at an even index, or every pile at an odd index, whichever she chooses, since each end she takes leaves Bob two ends of the other kind. The total is odd, so one kind holds more stones, and taking it wins: under LeetCode's constraints the answer is always true. The arm sums the two kinds and returns whether they differ. O(n), and correct only for an even number of piles with an odd total |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 10 lines: LeetCode's two examples and seven
more (two piles each way round; a large pile second from the left,
`[1, 100, 2, 1]`; the largest pile at the left end and at the right
end; six piles where the largest one is not at an end; and 500 piles,
LeetCode's longest row, of 499 and 500 stones); and the answers for 100
games, one of every even length from 2 to 40 and the rest of random even
lengths up to 500, with up to 500 or up to 3 stones a pile, with a
checksum. Every answer is true, as the parity argument says.
`stone_game.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every line of play followed out to the end, each player on
every turn taking the end that leaves them the most stones when the game
is over, and Alice winning with more stones than Bob. Under LeetCode's
constraints the answer is always true, which would leave most mistakes
unseen, so the four arms that play the game are also checked away from
the constraints, on any number of piles and any total, where Alice can
lose or tie; the parity arm is checked only within them. It plays 2,200
games: 1,000 within the constraints (2 to 12 piles, up to 500 or up to 3
stones a pile), 1,000 of 1 to 12 piles with any total, of which Alice
wins 782, and 200 of 13 to 60 piles, too many to play out.

| | property |
|---|---|
| P1 | the statement's answer, within the constraints, all five arms |
| P2 | the statement's answer away from the constraints, the four arms that play the game |
| P3 | the row reversed gives the same answer |
| P4 | every pile multiplied by the same number, 2 to 4, gives the same answer |
| P5 | a row of equal piles: Alice wins with an odd number of them and ties with an even number |
| P6 | on 13 to 60 piles, each of the four agrees with at least two of the other three |

P3 and P4 are checked on both sets of games, P5 on the second and P6
on the third. It prints `2200 games, Alice wins 782 of the 1000 away
from the constraints, 31800 checks over 5 arms: 0 failures` under
`karac __mir-run` and `karac __mir-llvm-run`, and the same under `karac
__mir-llvm-asan` with no error.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-llvm-run`. All fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a tie counted as a win | P2 67, P5 500, P6 11 |
| M2 | ★: the other player's margin added | P2 218, P5 500, P6 86 |
| M3 | ★: the worse end taken | P1 1000, P2 586, P6 181 |
| M4 | memo: a run keyed by i + j | P1 91, P2 153, P3 249, P6 90 |
| M5 | memo: a last pile worth nothing | P2 202, P5 1000, P6 9 |
| M6 | memo: the right end taken as the left pile | P1 589, P2 428, P3 834, P6 136 |
| M7 | rolling: the shorter runs swapped | P1 1000, P2 586, P6 181 |
| M8 | rolling: the runs of two skipped | P1 64, P2 177, P3 197, P5 916, P6 30 |
| M9 | rolling: the answer read from the last place | P2 218, P5 500, P6 86 |
| M10 | totals: the other player's best taken as the larger | P1 1000, P2 586, P6 181 |
| M11 | totals: a run counted one pile short | P1 949, P2 657, P3 234, P6 183 |
| M12 | totals: a single pile worth nothing | P2 285, P5 1000, P6 16 |
| M13 | parity: only the even piles winning | P1 547, P3 1000 |
| M14 | parity: only the last even pile counted | P1 19, P3 42 |
| M15 | parity: each odd pile counted one too many | P3 2, P4 38 |

P1 kills nine of the fifteen. Within the constraints Alice always
wins, so a mistake shows there only if it turns an answer to false, and
M1, M2, M5, M9 and M12 keep Alice ahead on every valid row; the games
away from the constraints catch them, in P2 and P5, where ties and
losses happen. M3, M7 and M10 are one fault in three arms, the player
taking the end that is worse for them, and fail the same games. A
mutant of the parity arm is killed only when it makes the two sums
equal, which an odd total never allows for any split of the piles into
two kinds: the first M14 tried, every third pile counted as even, was
equivalent for that reason and was replaced. M15 adds one stone for each
odd pile, which ties the sums on none of the rows P1 sees and on a few
of the reversed and scaled ones.

## Verification

Every arm prints the same output as `stone_game.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `89d76e3ff2` and the runtime
archives at `e903d5b111`, with no runtime change between them. Under
`karac __mir-run` the arms take under 1 to 23 s each (the memo arm, with
a `Map` lookup for every run, the slowest) and the differential 6 s;
the random games were cut from 300 to 100 to keep the memo arm there.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The frozen legacy backends (its interpreter and JIT, and `karac build
--legacy` with and without auto-par) print the same output for the ★,
memo, rolling and parity arms. They refuse the totals arm and the
differential at a `*` on a `for` element, saying the value is not a
reference, where v2 yields a reference, and the bench program at
`rows[k % 20]` passed to a function, saying it moves a `Vec` out of an
index, where v2 lends it. Legacy is frozen, so this is noted, not
filed.

## Benchmarks

The bench program uses the ★ arm, in all five languages: 20 rows of 500
piles, LeetCode's largest, with up to 500 or up to 3 stones a pile and an
odd total, built once; then 1,000 games, each building its own 500 by
500 table of margins, as LeetCode's function does, so the run fills some
1.25 x 10^8 cells. The table is a `Vec` of `Vec`s in Kāra and Rust, a
slice of slices in Go, a list of lists in Python and an array of
`malloc`'d rows in C. Every implementation prints `1000 games of 500
piles: Alice wins 1000, checksum 28444096`.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.80 to 0.90 s | 0.85 s |
| Rust (`rustc -O`) | 0.74 to 0.90 s | 0.82 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.71 to 0.90 s | 0.80 s |
| Go | 1.59 to 1.90 s | 1.72 s |
| Python | 28.8 s | |
| Kāra (`karac build --mir`) | 0.45 to 0.53 s | 0.46 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 876's does. Legacy refuses the bench program
(above), so it has no lane here.

v2 is the fastest here, at 0.58 times Rust's median time under overflow
checks and 0.54 times C's. It is not the instruction count: under
valgrind's cachegrind C runs 3.95 billion instructions, Rust with
overflow checks 9.34 billion and v2 8.00 billion, so v2 runs twice C's
instructions in half C's time, and its loop carries bounds and overflow
checks that C's does not. Nor is it the instruction set: built for
x86-64-v3, as `karac build` targets, C and Rust with overflow checks
take 0.80 and 0.74 s in five spot runs. Cachegrind's simulated cache
counts as many first-level write misses in C as in v2 (47 million each).
Each cell reads a cell of the next row, which the table's layout puts
thousands of bytes away, so the time most likely depends on how the rows
sit in memory, but what makes v2's loop faster was not traced; this
container has no hardware counters. The comparison with C and Rust waits
until after M4.
