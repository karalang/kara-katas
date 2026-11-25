# 1375. Number of Times Binary String Is Prefix-Aligned

You have a 1-indexed binary string of length `n` where all the bits are
`0` initially. We will flip all the bits of this binary string (i.e.
change them from `0` to `1`) one by one. You are given a 1-indexed
integer array `flips` where `flips[i]` indicates that the bit at index
`flips[i]` will be flipped in the `i`th step.

A binary string is prefix-aligned if, after the `i`th step, all the
bits in the inclusive range `[1, i]` are ones and all the other bits
are zeros.

Return the number of times the binary string is prefix-aligned during
the flipping process.

```
flips = [3,2,4,1,5]  ->  2
flips = [4,1,2,3]    ->  1
```

**Constraints:** `n == flips.length`, `1 <= n <= 5 * 10^4`, and
`flips` is a permutation of the integers from 1 to `n`.

Each arm is `fn num_times_all_blue(flips: Vec[i32]) -> i32`.

## Approaches

| file | mechanism |
|---|---|
| `num_times_all_blue.kara` ★ | after step `i`, `i` bits are on, and they are bits 1 to `i` exactly when the largest bit flipped so far is `i`; one pass keeping that largest. O(n) |
| `num_times_all_blue_sum.kara` | the flips are distinct, so after step `i` their sum is at least 1 + 2 + .. + `i`, and equal to it exactly when they are bits 1 to `i`; one pass keeping the sum. O(n) |
| `num_times_all_blue_fenwick.kara` | the bits that are on kept in a Fenwick tree; after step `i` the string is aligned when bits 1 to `i` hold `i` ones, read as a prefix count. O(n log n) |
| `num_times_all_blue_lowest.kara` | the bits kept as a `Vec[bool]`, and the lowest bit still off moved up past every bit that is on after each step; the string is aligned when that lowest is the next step's. O(n) in all |
| `num_times_all_blue_solution.kara` | a Rust solution as LeetCode's Rust users write it (`let mut mx = 0;`, `for (i, &f) in flips.iter().enumerate()`, `mx = mx.max(f);`, `if mx == i as i32 + 1`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 2 lines: LeetCode's two examples, and 5 * 10^4
bits flipped in order and in reverse (`2 1 50000 1`); and 2000 random
orders of 1 to 300 bits, a quarter shuffled whole and the rest shuffled
within runs of 2 to 8, so that many steps are aligned, folded into a
checksum (`2000 random orders: aligned 87675 times, checksum
778948431`). `num_times_all_blue.py` mirrors the ★ arm, and its output
is byte-identical. Every arm gives the same output under `karac
__mir-run`, `karac run` and `karac __mir-llvm-run`.

The Mend loop: the four Kāra arms check clean as first written. The Rust
solution takes one round of 7 fixes by `karac fix`'s count, from 5 parse
errors: `struct Solution;` to `struct Solution {}`, `Vec<i32>` to
`Vec[i32]`, the `&` dropped from the pattern `(i, &f)`, and `Solution::`
to `Solution.`. With the `&` gone, `f` is a `ref i32`, and `mx` an
`i64`, since its literal kept the default; `mx.max(f)` was refused until
B-2026-11-21-66, found on this arm, let a `ref` to a narrower integer
widen at a numeric method's argument. Every arm matches on the first
run.

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: the string kept as `n` bits, and after every step each
bit read, bits 1 to `i` on and every other bit off. It checks the two
examples, 1500 random orders of 1 to 12 bits and 500 of 1 to 120,
shuffled as above, each with a second order of 1 to 12 bits for P4 and
a step at which to trade two flips for P5.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | at least 1, since every bit is on after the last step, and at most `n` |
| P3 | one more bit, flipped last, once more aligned |
| P4 | a second order of higher bits flipped after this one, the two counts added |
| P5 | two neighbouring flips traded, a count at most 1 away |
| P6 | the ★ arm's count |

All 60,060 checks pass on every arm: `2002 cases: checksum 452803588,
60060 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run` and `karac __mir-llvm-run`. Python, reading every bit after every
step the same way, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash, and no two
fail the same checks. Six first edits were replaced. Three never let a
step count, and so failed the same checks: the ★ arm's largest compared
with the step before, the sum started at 1, and the Fenwick count taken
over bits 1 to `i - 1`. The sum arm's last step never checked failed as
the Fenwick tree with bit `n` never stored did. The ★ arm's count
stopped at the first step not aligned failed as the lowest arm's lowest
moved up one place at most a step did, but for P6. And the solution's
flips read from the last crashed both lanes, `call of unknown function
i64.max`: once the iterator is adapted (`.rev()`, `.skip(1)`,
`.filter(..)`), `mx.max(f)` passed `karac check` and was not lowered,
which B-2026-11-25-23 fixed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the count set to 1, not raised by 1 | P1 1297, P3 2002, P4 2002, P6 5188 |
| M2 | ★: the latest flip kept, not the largest | P1 1425, P2 384, P5 349, P6 5700 |
| M3 | sum: the last step never checked | P1 2002, P2 705, P4 2002, P6 2002 |
| M4 | sum: the latest flip also required to be the step's own bit | P1 1746, P2 726, P5 318, P6 1746 |
| M5 | fenwick: each flip stored at its own place only | P1 1872, P2 1426, P3 2002, P4 651, P6 1872 |
| M6 | fenwick: the prefix read one place at a time | P1 1627, P2 813, P3 2002, P4 1233, P6 1627 |
| M7 | lowest: moved up one place at most a step | P1 1746, P2 1426, P3 1746, P4 569, P5 196, P6 1746 |
| M8 | lowest: each flip marks the bit below it | P1 1800, P2 1261, P3 2002, P4 763, P6 1800 |
| M9 | solution: every step once bit `n` is on counted | P1 1129, P3 1129, P4 1129, P6 1129 |
| M10 | solution: the first step never counted | P1 576, P2 130, P4 651, P6 576 |

P1 and P6 kill all ten, P2 and P4 eight each, P3 six and P5 three. The
bound (P2) misses the two edits whose counts stay within 1 and `n`
whatever the order: the count held at 1 (M1), and every step counted
once bit `n` is on (M9). One more bit flipped last (P3) catches the
edits that miss the step it adds, or count it more than once: the count
set to 1 (M1), the Fenwick tree read or stored wrong (M5, M6), the
lowest bit behind (M7, M8) and the steps after bit `n` (M9). Joining two
orders (P4) catches all but the two edits that look at the latest flip
(M2, M4), whose miscounts add up across the join as the true counts do.
Trading two neighbours (P5) catches the edits that look at the latest
flip rather than the largest (M2, M4) and the lowest that lags (M7):
their counts change by more than the one step a trade can align or
unalign.

## Benchmarks

The bench builds 20 orders of 5 * 10^4 bits, the constraints' most, 1
to `n` shuffled within runs of 2 to 8, once; then makes 1000 rounds,
each trading two neighbouring flips of one order, both drawn from the
checksum so far, and counting that order's aligned steps with the ★
arm. Every implementation prints `1000 rounds over 20 orders of 50000
bits: checksum 702202148`. The work is one pass over 5 * 10^4 flips a
round, the same in every language; the Rust function takes `&[i32]`,
as the Kāra one borrows its `Vec`.

BENCHTAB
