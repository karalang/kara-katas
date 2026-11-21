# 2457. Minimum Addition to Make Integer Beautiful

You are given two positive integers `n` and `target`.

An integer is considered **beautiful** if the sum of its digits is less
than or equal to `target`.

Return *the minimum **non-negative** integer* `x` *such that* `n + x`
*is beautiful*. The input will be generated such that it is always
possible to make `n` beautiful.

```
n = 16, target = 6   ->  4
n = 467, target = 6  ->  33
n = 1, target = 1    ->  0
```

**Constraints:** `1 <= n <= 10^12`; `1 <= target <= 150`; the input
will be generated such that it is always possible to make `n`
beautiful.

Adding to `n` can lower its digit sum only by a carry, and the cheapest
carry clears the lowest nonzero digit: rounding `n` up to a multiple of
10 sets its last digit to 0 and adds one to the digit above. So the
answer makes `n + x` some rounding of `n` up to a multiple of `10^k`,
and the least `k` whose rounding fits gives it. At most 13 roundings
are tried, each with a digit sum of at most 13 digits.

## Approaches

| file | mechanism |
|---|---|
| `beautiful.kara` ★ | rounding up: while the digit sum is too large, `n + x` rounded up to the next multiple of a power of ten one place higher, by `(m + p - 1) / p * p`. O(log^2 n) |
| `beautiful_digits.kara` | a digit vector: `n`'s digits lowest first, and while their sum by `iter().sum()` is too large, the lowest nonzero digit cleared and one carried into the digit above, through nines, by a `loop` with `break`; the digits read back by `rev`. O(log^2 n) |
| `beautiful_recursive.kara` | recursion on the last digit: a number that fits needs nothing, one that does not must end in 0, so its last digit is taken up to 10 and the rest is the same question for the number above, scaled by ten; the digit sum recursive too. O(log^2 n) |
| `beautiful_power.kara` | every candidate: `n` rounded up to a multiple of `10^k` for each `k` from 0 to 13, and the least addition whose digit sum, read off `to_string().bytes()`, fits. O(log^2 n) |
| `beautiful_iter.kara` | iterators: the powers of ten by `successors`, `n` rounded up to each by `map`, and the first rounding that fits taken by `find`; the digit sum by `successors` dividing by ten, `map` and `sum`. O(log^2 n) |
| `beautiful_solution.kara` | LeetCode's Rust template: a nested `fn digit_sum(mut x: i64) -> i32` summing `(x % 10) as i32`, and a loop raising `p` by ten and setting `x = (n / p + 1) * p - n` while the digit sum of `n + x` is above the `i32` target; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 10 lines: LeetCode's three examples; `10^12`,
the constraints' most, already fitting; `10^12 - 1` down to a target of
1, a carry through twelve nines; 19 to 1; 190 to 1, its zero ending
kept; `10^12 - 1` against its own digit sum, 108; then 2000 random
values up to `10^12` against targets from 1 to 150, as a checksum and
the total; and 3000 random values up to `10^4` against targets from 1
to 20, as a checksum. `beautiful.py` mirrors the ★ arm and its output
is byte-identical, and the mirror was checked on 20000 random values up
to 3000 against every `x` tried from 0.

`check` first reports 3 errors on the template, and `karac fix` carries
it in one call, reporting 8 edits: the parameter `mut x: i64` written
`x: i64` with `let mut x = x;` opening the body, since a parameter's
mode is written in its type; the nested `fn digit_sum` hoisted above
the `impl`, since Kāra has no nested items and it captures nothing;
`struct Solution;` given its braces; and, once the template parses,
the suffixes of `0i64` and `1i64` dropped, since the literals take
`i64` from their use, and `let mut s = 0` declared `s: i32`, its
literal otherwise keeping the default `i64` against the `i32` it adds.
`(x % 10) as i32`, `x /= 10` and the comparison with the `i32` target
stand as Kāra. The target fits an `i32`, as LeetCode's signature has it;
the other arms take `i64`.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: `x` tried from 0 upward, one at a time, until the digits of
`n + x`, read off its decimal text, add up to at most `target`. No
rounding is done. It checks 300 random cases with `n` up to 999 and
targets from 1 to 15; then 30 with `n` up to `10^5` and targets from 1
to 30; then 30 with `n` just below a power of ten, up to `10^5`, and
targets from 1 to 5, so a carry runs through nines. All 360 are drawn
before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | `n` raised by some `k` up to the answer: the answer less `k` |
| P3 | `n` times ten: the answer times ten |
| P4 | the target raised by one: an answer no larger |
| P5 | the digits of `n` plus the answer add up to at most the target |
| P6 | each arm agrees with at least three of the other five |

P2 holds because no number from `n` to `n + x` is beautiful but the
last, so from any of them the nearest is still `n + x`. P3 holds
because a trailing 0 adds nothing to a digit sum, and the rounding of
`10 n` up to a multiple of `10^(k + 1)` is ten times the rounding of `n`
up to `10^k`, while its rounding to 10 is `10 n` itself. P4 holds
because whatever fits a target fits one larger, and P5 is the
definition.

The differential prints `360 cases: checksum 784322827, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and tries every `x`. On a failure it prints the first
ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M2 | ★: rounded down | P1 279, P2 279, P4 51, P5 279, P6 279 |
| M5 | ★: one too many | P1 360, P2 73, P3 360, P5 72, P6 360 |
| M6 | ★: each 9 counted as 0 | P1 99, P2 64, P5 99, P6 99 |
| M7 | digits: an 8 carried through | P1 7, P2 2, P6 7 |
| M8 | digits: the digits read back reversed | P1 352, P2 352, P3 360, P4 56, P5 324, P6 352 |
| M9 | digits: the top digit dropped on reading back | P1 360, P2 360, P4 27, P5 360, P6 360 |
| M12 | recursive: every other digit summed | P1 154, P2 18, P3 99, P5 154, P6 154 |
| M13 | recursive: a zero ending not scaled | P1 17, P2 29, P3 279, P5 17, P6 17 |
| M14 | recursive: one short of ten | P1 279, P2 19, P5 279, P6 279 |
| M17 | power: three places only | P1 79, P2 79, P3 172, P4 17, P5 79, P6 79 |
| M19 | power: the greatest addition | P1 360, P3 360, P6 360 |
| M20 | power: the leading digit left out | P1 182, P5 182, P6 182 |
| M22 | iter: n itself never tried | P1 61, P3 61, P6 61 |
| M24 | iter: the leading digit dropped | P1 181, P3 1, P5 181, P6 181 |
| M26 | iter: two places at a time | P1 136, P2 10, P3 207, P6 136 |
| M29 | solution: each digit halved | P1 208, P5 208, P6 208 |
| M31 | solution: n one higher | P1 288, P3 291, P5 288, P6 288 |

P1 and P6 kill all seventeen, P5 thirteen, P2 eleven, P3 ten and P4
four.

Fourteen are not kept. Three fail exactly as a kept one: the ★ arm's
two places at a time (M4) as the iter arm's (M26); the power arm's `n`
itself never tried (M21) as the iter arm's (M22); and the iter arm's
rounded down (M25) as the ★ arm's (M2). Nine fail apart from every kept
one and were left out because those arms keep their share already: the
★, iter and template arms' one over the target allowed (M3, M23, M30),
which fail alike; the digits arm's leading digit never read and each 9
read as 0 (M10, M11); the recursive arm's no carry and last 1 taken as
0 (M15, M16); the power arm's multiple rounded up again (M18), which
there skips `n` itself whenever it ends in 0; and the template's two
places at a time (M28), which differs from M4 and M26 by two of the
`10 n` checks.

One ends in an integer overflow, not a wrong answer, under both
backends: the template's two steps up (M27) sets `n + x` to `(n / p + 2)
* p`, which can leave the digit sum too large at every `p`, so the loop
runs on until `p *= 10` overflows.

One survives, and is equivalent: the ★ arm's multiple rounded up again
(M1), `(m + p) / p * p`. It differs only when `m` is already a multiple
of the new `p`, and then it adds `p`, one to the digit at that place.
That digit sum is larger than `m`'s, which did not fit, unless the
digit was 9 and the carry gives the rounding to `10 p` itself; either
way the next rounding, to `10 p`, lands where the ★ arm's does, so the
loop stops at the same multiple.

## Verification

Every arm prints the same output as `beautiful.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` every arm takes 0.2 to 0.4 s, but for the power
arm, which reads every candidate's digits off its text, at 1.3 s; the
differential takes 2.2 s there, whose literal reading tries every `x`,
0.8 s under `karac __mir-llvm-asan` and 0.35 s under `karac run`.

## Benchmarks

The bench builds `10^5` pairs once from its own generator, each a value
up to `10^12`, the constraints' largest, and a base target. It then
makes 36 passes; pass `p` moves every target to `1 + (t + p) % 150`, so
no answer carries over, then answers every pair, folding the answer
plus the pass into the checksum. The bench uses the ★ arm, rounding up
one place at a time, in all five languages. Every implementation prints
`36 passes over 10^5 pairs: checksum 815539925`.

BENCHTAB
