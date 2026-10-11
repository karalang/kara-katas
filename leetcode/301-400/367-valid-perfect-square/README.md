# 367. Valid Perfect Square

Given a positive integer `num`, return `true` if it is the square of an
integer and `false` otherwise, without a library square root.

```
num = 16   -> true    (4 * 4)
num = 14   -> false
```

**Constraints:** `1 <= num <= 2^31 - 1`.

## Approaches

| file | mechanism | time |
|---|---|---|
| `perfect_square.kara` ★ | binary search for the root in `[1, num]`; `num` is below 2^31, so `mid * mid` fits an `i64` | O(log num) |
| `perfect_square_newton.kara` | Newton's method on integers, `x = (x + num / x) / 2` from `x = num` down to the floor of the root, then square it back | O(log num) |
| `perfect_square_odd.kara` | subtract 1, 3, 5, … in turn, since their running sums are the squares; a square lands exactly on zero | O(sqrt num) |
| `perfect_square_bits.kara` | the schoolbook square root in base 2, one root bit per power of four, with no multiplication; a square leaves nothing over | O(log num) |
| `differential.kara` | the four arms against an oracle that builds each number around a known root, 41,190 checks, five properties | — |

Every arm prints the same 12 lines: the two LeetCode examples, nine edge
cases (1, 2, a square and its two neighbours, a million, 46340², which is
the largest square in range, the number after it, and 2^31 - 1), and a count and checksum
over 1,000 random numbers below a million, half of them squares.
`perfect_square.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms. The oracle never takes a
square root: it draws a root `r` and an offset `0 <= d <= 2r` and builds
`num = r² + d`, which lies from `r²` up to just below `(r + 1)²`, so `num` is
a square exactly when `d` is 0. Half the cases have `d = 0`. The roots come
from three ranges, up to 30, up to 2,000 and up to 46,340, so that small
numbers, mid-sized ones and ones near the 2^31 bound all turn up. One step of
the test's generator gives only 15 good bits, so each draw joins two steps;
without that no root passes 32,768 and no number reaches 2^30.

| | property |
|---|---|
| P1 | each arm gives the oracle's answer |
| P2 | multiplying `num` by 4 or by 9, where that stays in range, changes no answer |
| P3 | `r²` is a square, and `r² + 1` and (for `r >= 2`) `r² - 1` are not |
| P4 | the product of two squares, where it stays in range, is a square |
| P5 | for `num <= 300`, the arm finds exactly `r` squares in `1..=num` |

The odd-number arm is O(sqrt num), so it runs only on numbers below a
million to keep the test inside the corpus time limit; the other three see
every number. The main program's edge cases cover the odd arm up to 2^31 - 1.

It prints `2000 cases, 41190 checks, 0 failures` under `karac __mir-run`
(about 8 seconds), `karac run --interp`, LLJIT, `karac build` and
`KARAC_AUTO_PAR=1 karac build`.

## Mutation testing

Nine edits to the copies inside `differential.kara`, each run under
`karac __mir-run`. All nine are killed.

| # | mutation | how |
|---|---|---|
| M1 | binary: `hi = mid - 2`, which can step over the root | P1 to P5, 1697 failures |
| M2 | binary: searches `[1, num / 2]`, which misses the root of 1 | P1, P3 and P5, 387 failures |
| M3 | binary: `while lo < hi`, so the last candidate is never tried | P1 to P5, 2131 failures |
| M4 | newton: one step instead of a loop | P1 to P5, 4223 failures |
| M5 | odd: subtracts 1, 2, 3, …, the triangular numbers | P1 to P5, 2305 failures |
| M6 | odd: stops while 1 is left, so 1 is not a square | P1, P3 and P5, 387 failures |
| M7 | bits: starts at 4^14 instead of 4^15, too low for numbers from 2^30 | P1 to P4, 392 failures |
| M8 | bits: keeps the root unshifted when it gains a bit | P1 to P5, 3427 failures |
| M9 | oracle: lets `d` reach `2r + 1`, which is `(r + 1)²` | P1, P2 and P5, 284 failures |

M7 survived the first version of the test, whose draws never passed 32,768:
no number reached 2^30, where the missing power of four starts to matter.
Joining two generator steps per draw is what kills it.

## Verification

All four arms print the same output as `perfect_square.py` under
`karac run --interp`, `karac __mir-run` (the v2 MIR interpreter), LLJIT,
`karac build` and `KARAC_AUTO_PAR=1 karac build`.

## Benchmarks

The bench program tests three million random numbers below 2^31 with the ★
arm: the even-numbered ones are squares of roots up to 46,340 and the odd
ones are anywhere in range. The Kāra build and the C, Rust, Go and Python
mirrors all print `1500038 squares, checksum 430926364`. Timings are not
taken yet; they need a quiet machine.

## Compiler findings

None.
