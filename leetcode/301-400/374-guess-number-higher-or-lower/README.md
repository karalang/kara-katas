# 374. Guess Number Higher or Lower

The judge picks a number from 1 to `n`. Each call `guess(num)` returns -1
when the pick is lower than `num`, 1 when it is higher, and 0 when `num`
is the pick. Return the pick.

```
n = 10, pick = 6   -> 6
n = 1, pick = 1    -> 1
n = 2, pick = 1    -> 1
```

**Constraints:** `1 <= n <= 2^31 - 1`; `1 <= pick <= n`.

## Approaches

The judge is a `Game` struct holding the pick and a guess counter, and
`guess` is a `mut ref self` method on it. Every arm takes the game as a
`mut ref Game` parameter, so a caller writes `guess_number(n, mut game)`.

| file | mechanism | guesses |
|---|---|---|
| `guess_number.kara` ★ | binary search: guess the middle of `[lo, hi]` and drop the half the answer rules out; the middle is written `lo + (hi - lo) / 2`, which cannot overflow even in 32 bits | at most the bit length of `n`, 31 |
| `guess_number_ternary.kara` | ternary search: guess the one-third and two-thirds points and keep the part the two answers leave | at most two per base-3 digit of `n`, about 1.26 times binary search |
| `guess_number_bits.kara` | build the pick from its top bit down: guess what is known so far plus the next bit, and keep the bit when the pick is at least that; a candidate above `n` is skipped without a guess | at most the bit length of `n` |
| `guess_number_gallop.kara` | guess 1, 2, 4, 8, ..., capped at `n`, until the pick is not above the guess, then binary search between the last two guesses | at most twice the bit length of the pick |
| `differential.kara` | the four arms against the pick, 100,000 checks, five properties | — |

The bit arm can return without ever hearing a 0: once every bit is
decided, the pick is known.

Every arm prints the same 10 lines: the three LeetCode examples, six edge
cases (the top of two, 1 and `2^31 - 1` with `n = 2^31 - 1`, `2^30`, the
middle of three, a pick of `2^16 - 1`), and a checksum over 1,000 random
games with `n` up to `2^31 - 1`. `guess_number.py` mirrors the ★ arm and
its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and a judge that also
tracks the range its answers still leave possible. It plays 5,000 random
games: a third with `n` up to 20, a third up to `2^20`, a third up to
`2^31 - 1`; one pick in eight is 1 and one in eight is `n`.

| | property |
|---|---|
| P1 | each arm returns the pick |
| P2 | each arm stays within its guess bound in the table above |
| P3 | every guess is in `[1, n]` |
| P4 | no guess is a number that earlier answers ruled out, so none repeats |
| P5 | the answer does not change when `n` grows to `2^31 - 1` |

It prints `5000 cases, 100000 checks, 0 failures` under
`karac __mir-run`, `karac run --interp`, LLJIT, `karac build` and
`KARAC_AUTO_PAR=1 karac build`.

## Mutation testing

Eight edits to the copies inside `differential.kara`, each run under
`karac __mir-run`. Seven are killed; M1 survives because it is still a
correct search.

| # | mutation | how |
|---|---|---|
| M1 | binary: after a guess that is too high, `hi` becomes `mid`, not `mid - 1` | survives |
| M2 | binary: the loop stops while one number is left | P1 and P5, 5118 failures |
| M3 | ternary: above the second probe, the probe stays in the range | P2 and P4, 1358 failures |
| M4 | ternary: between the probes, the upper end is not lowered | P2 and P4, 2022 failures |
| M5 | bits: starts at bit 29 | P1, 251 failures |
| M6 | bits: guesses candidates above `n` | P2, P3 and P4, 12648 failures |
| M7 | gallop: forgets the last probe that was too low | P2 and P4, 4560 failures |
| M8 | gallop: the probe is not capped at `n` | P3 and P4, 3030 failures |

M1 leaves a ruled-out number at the top of the range, but the next middle
is always below it, and `lo` cannot reach it because the pick is lower,
so it is never guessed and the answer is still right. It does cost extra
guesses: counted exhaustively in Python over every game with `n` below
600, it takes more guesses than the ★ arm in 65,472 of the 179,700 games,
but never more than the bit length of `n`, so P2 cannot see it.

## Verification

All four arms print the same output as `guess_number.py` under
`karac run --interp`, `karac __mir-run` (the v2 MIR interpreter), LLJIT,
`karac build` and `KARAC_AUTO_PAR=1 karac build`.

## Benchmarks

The bench program plays 2,000,000 random games with `n` up to
`2^31 - 1`, answered by the ★ arm against a judge that counts guesses.
The Kāra build and the C, Rust, Go and Python mirrors all print
`57224931 guesses, checksum 829113003`. Timings are not taken yet; they
need a quiet machine.

## Compiler findings

None.
