# 2220. Minimum Bit Flips to Convert Number

A **bit flip** of a number `x` is choosing a bit in the binary
representation of `x` and **flipping** it from either `0` to `1` or `1`
to `0`.

- For example, for `x = 7`, the binary representation is `111` and we
  may choose any bit (including any leading zeros not shown) and flip
  it. We can flip the first bit from the right to get `110`, flip the
  second bit from the right to get `101`, flip the fifth bit from the
  right (a leading zero) to get `10111`, etc.

Given two integers `start` and `goal`, return *the **minimum** number of
**bit flips** to convert* `start` *to* `goal`.

```
start = 10, goal = 7  ->  3
start = 3, goal = 4   ->  3
```

**Constraints:** `0 <= start, goal <= 10^9`.

A bit has to be flipped exactly where `start` and `goal` differ, which
is where `start ^ goal` has a 1, and flipping it once is enough; so the
answer is the 1 bits of `start ^ goal`, counted by clearing the lowest
with `x & (x - 1)` until none is left. O(number of flips).

## Approaches

| file | mechanism |
|---|---|
| `flips.kara` ★ | `start ^ goal`, its lowest 1 cleared by `x & (x - 1)` until it is 0, the clears counted |
| `flips_shift.kara` | both numbers read a bit at a time from the bottom with `% 2` and halved, a flip counted where the bits differ, until both are 0 |
| `flips_text.kara` | both written in binary with `f"{x:b}"` into `Vec[char]`s, the shorter padded on the left by `insert(0, '0')`, the places whose characters differ counted |
| `flips_struct.kara` | a `struct Register` holding a number, `bit` (`ref self`) reading one bit, `flip` (`mut ref self`) toggling one, and `toward` (`mut ref self`) flipping it into the goal bit by bit and counting; an `assert` that the register then holds the goal |
| `flips_iter.kara` | the places 0 to 30 by a range, `filter`ed to those where the two numbers' bits differ, and `count`ed |
| `flips_solution.kara` | LeetCode's Rust template: two `i32`s in, `i32` out, `(start ^ goal).count_ones() as i32`; carried by `karac fix` in one round |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's two examples and four more
(the same number, 0 to 10^9, 10^9 to one less, and 29 ones to 0), each
with its answer; then a checksum of 3000 random pairs up to 10^9, every
third goal the start with one to three bits flipped; then 10^5 random
pairs up to 10^9, their flips summed. A number up to 10^9 is drawn from
two draws, since one stops at 32767. `flips.py` mirrors the ★ arm and
its output is byte-identical.

`karac fix` carries the template in one round of 3 edits: `struct
Solution;` to `struct Solution {}`, `Solution::` to `Solution.`, and the
adapter's `as i64` on the `i32` result dropped, since an `i32` widens to
`i64` on its own. `count_ones` is Kāra's too, so the body is unchanged.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: a breadth-first search from `start` over the numbers below
2^11, one move flipping any one bit, until `goal` is reached; no xor
counting. It checks 300 random pairs below 2^10; then 30 of a number and
itself; then 30 of a number and its ten low bits all flipped. All 360
are drawn before any arm answers.

| | property |
|---|---|
| P1 | the flips are the statement read literally |
| P2 | they are from 0 to 30, and 0 exactly when start is goal |
| P3 | start and goal swapped: the same flips |
| P4 | both xored with one random mask below 2^30: the same flips |
| P5 | one random bit of goal, from 0 to 29, flipped: one flip more or one fewer |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 cases: checksum 786109183, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading over the
padded binary strings. On a failure it prints the first ten and then the
count by property.

## Mutation testing

Thirty-three edits to the differential, six to the ★ arm, seven to the
struct arm, and five to each of the other arms, each run under `karac
__mir-llvm-run` and `karac __mir-run`; three of the struct arm's first
five crashed on its own `assert`, so two more were written. Seventeen
are kept, three to each Kāra arm and two to the Rust-template arm. Each
kept one is killed, fails the same way under both backends and not by a
crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M2 | ★: `start \| goal` for `start ^ goal` | P1 313, P2 30, P4 360, P5 54, P6 313 |
| M4 | ★: the difference halved, not its lowest 1 cleared | P1 299, P5 343, P6 299 |
| M6 | ★: bit 20 of the difference ignored | P5 14 |
| M7 | shift: the walk stopping when either number is 0 | P1 219, P2 5, P4 219, P5 222, P6 219 |
| M9 | shift: goal divided by 4 each step | P1 301, P2 30, P3 279, P4 360, P5 179, P6 301 |
| M10 | shift: the bits compared by `% 3` | P1 284, P4 229, P5 306, P6 284 |
| M12 | text: the shorter padded on the right | P1 87, P3 158, P4 87, P5 179, P6 87 |
| M14 | text: the top place never compared | P1 219, P2 1, P4 219, P5 108, P6 219 |
| M15 | text: the goal padded with 1s | P1 83, P3 181, P4 83, P5 68, P6 83 |
| M18 | struct: a flip at an odd place counted twice | P1 322, P5 179, P6 322 |
| M20 | struct: the flips rounded up to even | P1 137, P5 360, P6 137 |
| M32 | struct: a flip above place 24 not counted | P5 70 |
| M24 | iter: the goal's bit read one place higher | P1 312, P2 30, P3 274, P4 360, P5 19, P6 312 |
| M25 | iter: place 0 never compared | P1 181, P5 19, P6 181 |
| M26 | iter: two bits compared at each place | P1 299, P5 306, P6 299 |
| M27 | solution: the 0 bits of `start ^ goal` counted | P1 360, P2 32, P6 360 |
| M30 | solution: the 1 bits of `start` alone | P1 307, P2 31, P3 268, P4 360, P5 360, P6 307 |

P5 kills sixteen, P1 and P6 fifteen, P4 nine, P2 seven and P3 five. P1
and P6 miss the two edits above bit 19, the ★ arm's bit 20 ignored and
the struct arm's flips above place 24 uncounted (M6, M32): the literal
search runs below 2^11, so every pair differs only in the low ten bits,
and P4's mask, xored into both numbers, leaves their difference where
it was. Only P5 reaches the high bits, flipping one of the goal's bits
from 0 to 29. P3 swaps start and goal, and kills only the edits that
read the two unlike (M9, M12, M15, M24, M30).

Of the thirty-three, sixteen were not kept. One survives and is
equivalent: the iter arm's places 0 to 29, not 30 (M22), since a number
up to 10^9 has no bit 30, and neither does any the differential draws.
Four crash under both backends, as they should: the text arm's goal
never padded runs off its end (M13), and three of the struct arm's
edits leave the register short of the goal, which its `assert` reports
(M17, M19, M21). The other eleven are killed, and none differs between
the backends. Three fail as a kept one does: the shift arm's walk
stopping at 1 (M11) as the text arm's top place never compared (M14),
and the template's difference shifted down by one and the struct arm's
flip at place 0 counted twice (M31, M33) as the iter arm's place 0
never compared (M25). Seven fail alike in groups none of which is kept:
`start & goal` for `start ^ goal` in the ★ arm and the template (M1,
M28); the ★ arm's flips from 1 and the template's one more, with the
iter arm's equal places counted failing the same checks as many times
(M3, M29, M23);
and the shift and text arms' equal bits counted (M8, M16). One fails its
own way and is left out for the count of three: the ★ arm's two lowest
1s cleared at each step (M5).

## Verification

Every arm prints the same output as `flips.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the template takes 0.4 s, the ★, shift, struct
and iter arms 0.5 s to 1.5 s, the text arm 4.1 s, and the differential
0.9 s.

## Benchmarks

The bench draws 10^5 pairs up to 10^9 once, then 50 times punches one
goal, drawing it again, and answers every pair with the ★ arm in all
five languages, summing the flips. Every implementation prints `10^5
pairs, 50 punches: checksum 66166822`.

BENCHTAB
