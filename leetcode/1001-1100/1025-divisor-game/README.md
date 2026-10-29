# 1025. Divisor Game

Alice and Bob take turns, Alice first, with a number `n` on a
chalkboard. On a turn the player chooses any `x` with `0 < x < n` and
`n % x == 0`, and replaces `n` with `n - x`. A player who cannot move
loses. Return `true` if and only if Alice wins with both players playing
optimally.

```
n = 2  ->  true    (Alice takes 1, and Bob has no move at 1)
n = 3  ->  false   (Alice can only take 1; Bob takes 1 from 2)
```

**Constraints:** `1 <= n <= 1000`.

## Approaches

The player to move at `m` wins exactly when some move leads to a number
where the other player loses, and 1 has no move. Four arms compute that
table of winners; the ★ arm is the closed form it comes to.

| file | mechanism |
|---|---|
| `divisor_game.kara` ★ | parity: Alice wins exactly when `n` is even. From an even number she takes 1 and hands Bob an odd one; every divisor of an odd number is odd, so whatever Bob takes hands her back an even one, and Bob is left holding 1. O(1) |
| `divisor_game_dp.kara` | a table of winners, divisors in pairs: fill `wins[m]` from 2 up, finding the moves by trial division up to the square root of `m`, each divisor `d` giving its partner `m / d` too unless that is `m` itself. O(n sqrt n) |
| `divisor_game_sieve.kara` | a sieve of divisors: list every move from every number up to `n` at once from the divisor's side, `x` a move from each of `2x, 3x, ...`, in a `Vec` of `Vec`s; then fill the table with `any` over each number's moves. O(n log n) |
| `divisor_game_memo.kara` | recursion with a memo: search the game from `n` down, trying every divisor no more than half the number, each number solved once and kept in a `Map`. O(n^2) |
| `divisor_game_iter.kara` | an iterator search: push each number's answer onto a `Vec`, found as `(1..m / 2 + 1).filter(..).any(..)` over the candidate moves. O(n^2) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 11 lines: LeetCode's two examples; the winner
for every `n` from 1 to 60; for six groups of random games (500 with `n`
up to 10, down to 10 with `n` up to 1,000), how many Alice wins and a
checksum; and the answers for 1,000 and 999. `divisor_game.py` mirrors
the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the player to move wins when some `x` with `0 < x < n` and
`n % x == 0` leaves the other player a number they lose at, searched
afresh with no table, stopping at the first winning move. It asks every
arm for every `n` from 1 to 400, each call on its own, and checks each
answer against the arm's own answers for smaller numbers. The literal
search grows too fast to go past 70.

| | property |
|---|---|
| P1 | the statement read literally, for `n` up to 70 |
| P2 | a number the arm calls a win has a move to a number it calls a loss |
| P3 | a number the arm calls a loss has no such move |
| P4 | two losses are never neighbours, since taking 1 from `n` leaves `n - 1` |
| P5 | a game played out from `n`, the player the arm says is winning always moving to a number it calls a loss and the other moving at random, is won by the player the arm predicted; the random moves come from a seed of `n`'s own, so every arm and every edit meets the same ones on the same path |
| P6 | each arm agrees with at least two of the other four |

The differential prints `n = 1 to 400 (70 searched in full): checksum
73899654, 10345 checks over 5 arms: 0 failures` under `karac __mir-run`
(9.8 s) and `karac __mir-llvm-run`, and the same under `karac
__mir-llvm-asan` with no error.

## Mutation testing

Thirty edits to the differential, each run under `karac __mir-run` and
`karac __mir-llvm-run`; fifteen are kept, three to each arm, all fifteen
are killed, each fails the same checks under both, and no two kept ones
fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the winner the wrong way round | P1 70, P2 1, P3 199, P5 197, P6 400 |
| M2 | ★: odd multiples of 9 winning | P1 4, P2 23, P5 57, P6 22 |
| M3 | ★: Bob winning from 300 up | P3 101, P4 101, P5 42, P6 51 |
| M4 | dp: numbers leaving remainder 1 taken as moves | P1 29, P2 52, P5 384, P6 194 |
| M5 | dp: the answer read one place early | P1 69, P3 200, P4 1, P5 196, P6 399 |
| M6 | dp: 2 never filled | P1 2, P3 1, P4 1, P5 399, P6 2 |
| M7 | sieve: 1 never listed | P1 3, P3 8, P4 8, P5 141, P6 4 |
| M8 | sieve: each number listed as its own move | P1 5, P2 4, P3 7, P4 4, P5 310, P6 11 |
| M9 | sieve: all for any | P1 67, P3 199, P4 1, P5 194, P6 397 |
| M10 | memo: half the number never tried | P1 4, P3 2, P4 1, P5 188, P6 4 |
| M11 | memo: a move to a winning number taken | P1 35, P3 399, P4 399, P5 184, P6 200 |
| M12 | memo: the opposite remembered | P1 16, P2 209, P5 379, P6 122 |
| M13 | iter: half the number never tried | P1 1, P3 2, P4 2, P5 1, P6 1 |
| M14 | iter: the non-divisors taken for moves | P1 40, P2 300, P3 19, P4 4, P5 386, P6 208 |
| M15 | iter: the move's size looked up, not where it leads | P1 34, P2 398, P5 398, P6 199 |

P5 and P6 kill all fifteen, P1 fourteen, P3 eleven, P4 ten and P2 seven.
P1 misses only M3, which goes wrong from 300 up, past the literal
search. P5 is the widest because a game passes through many numbers, and
a wrong answer at any of them leaves the predicted winner either without
a move to a loss or beaten by a random reply. P2 can fail only at a number
the arm calls a win and P3 only at one it calls a loss: of the two, M2,
M4, M12 and M15 fail only P2, eight others only P3, and M1, M8 and M14 both. M13 is wrong at 2 alone: without its largest
candidate move, 2 has no move at all and is called a loss, while from 4
up taking 1 is still in range; P3 and P4 then fail at 2 and at 3, the
first two neighbours both called losses.

Fifteen other edits were tried and set aside. Three change no answer,
because the only move any answer turns on is taking 1 from an even
number: that wins, and every move from an odd number is odd and leads to
an even number. Dp never trying a divisor equal to the square root
removes a move other than 1; the sieve listing `x` only for its even
multiples still lists 1 for every even number, and leaves odd numbers
with no moves, which lose as before; and memo trying only odd moves
still tries 1, and an odd number has no other kind. The other twelve
were killed too, beyond three per arm. Dp, memo and iter never trying 1
fail exactly as M7; dp taking the whole number as a move and ★ calling
every number but 1 a win, as M15; iter with `all` for `any`, as M9; the
sieve never listing its largest move, as M13; and the sieve and iter
calling 1 a win fail alike. Three fail on their own: ★ calling only
multiples of 4 wins, ★ calling 1 a win, and memo taking the whole number
as a move, which also calls 1 a win, since it leaves 0.

## Verification

Every arm prints the same output as `divisor_game.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and under
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error; the differential prints its line under all three. `karac check
--output=json` reports no diagnostic for the five arms, the differential
and the bench program, so `karac fix` had nothing to do. `karac run` and
a `karac build` binary print the same output for every arm and the
differential. The release build is kara `56c60bdf7c`, with runtime
archives rebuilt at `ce706dd131`, the last commit before it to change
the runtime. Under `karac __mir-run` the arms take
0.2 s (★) to 2.5 s (iter). No compiler gap turned up.

The legacy compiler was removed from kara at M3, so there is no legacy
lane.

## Benchmarks

The closed form is one modulo, so timing it would measure the loop
around it. The bench runs the sieve arm instead, the table a reader
writes before spotting the pattern, in all five languages: 100 random
`n` from 500 to 1,000, drawn once, each answered 100 times, every call
building its own lists of divisors and table of winners. The lists are
a `Vec` of `Vec`s in Kāra and Rust, a slice of slices grown with
`append` in Go, a list of lists in Python, and in C an array of
growable arrays doubled with `realloc`, freed after each call. Every
implementation prints `100 games of n from 500 to 1000, 100 rounds:
Alice wins 5400, checksum 496470446`.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with karac as above:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.637 to 0.805 s | 0.697 s |
| Rust (`rustc -O`) | 0.746 to 0.846 s | 0.770 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.727 to 0.977 s | 0.792 s |
| Go | 0.992 to 1.095 s | 1.054 s |
| Python | 5.3 s | |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.448 to 0.626 s | 0.483 s |
| Kāra (`karac build`) | 0.451 to 0.578 s | 0.463 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here
(its user time stays below its real time) and runs as fast as the
sequential one.

v2 took 0.61 times Rust's median time under overflow checks and 0.69
times C's, the fastest of the five. Every call allocates, grows and
frees about a thousand small lists; we did not measure how much of each
language's time that takes, or why Kāra comes out ahead.
