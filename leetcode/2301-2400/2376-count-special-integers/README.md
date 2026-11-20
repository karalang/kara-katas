# 2376. Count Special Integers

We call a positive integer **special** if all of its digits are
**distinct**.

Given a **positive** integer `n`, return *the number of special integers
that belong to the interval* `[1, n]`.

```
n = 20   ->  19
n = 5    ->  5
n = 135  ->  110
```

**Constraints:** `1 <= n <= 2 * 10^9`.

A special number of `L` digits has 9 choices for its first digit and
then the unused ones, so there are `9 * 9 * 8 * ...` of them; the ones
of `n`'s own length below it fall under `n` at a first place, and every
place after that one is free among the digits left. There are 5974650
special numbers up to `2 * 10^9`, so the answer fits LeetCode's `i32`.

## Approaches

| file | mechanism |
|---|---|
| `special.kara` ★ | digit by digit: the shorter numbers counted by length, then each place of `n` adding its smaller unused digits times the arrangements of the places after it, stopping at the first repeated digit of `n`, and `n` itself counted when none repeats. O(10 L) |
| `special_memo.kara` | digit DP: the numbers written place by place with a digit not yet used, a place no higher than `n`'s while the digits so far equal `n`'s, and the count of a number that has started and fallen below `n` kept by its place and the set of digits used. O(10 * 2^10 * L) |
| `special_dfs.kara` | every special number up to `n` written out by a depth-first walk that appends each unused digit in turn and stops as soon as the number passes `n`. One step per special number |
| `special_below.kara` | the special numbers below `n + 1`, from a table of factorials, with nothing added for `n + 1` itself |
| `special_iter.kara` | iterators: the shorter numbers as a `sum` of `product`s, and `n`'s digits folded into the count, the set of digits used and whether every digit so far was new |
| `special_solution.kara` | LeetCode's Rust template: the digits from `n.to_string().into_bytes()`, a `[false; 10]` array of the digits used and `i32` products; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 4 lines: LeetCode's three examples; 1 and 10;
`2 * 10^9` and 123456789; then 2000 random `n` of 1 to 5 digits, with a
checksum and how many are special themselves. `special.py` mirrors the ★
arm and its output is byte-identical, and the mirror was checked against
a count of every `n` up to 200000 and on 3000 random `n` up to
`2 * 10^9` against the sorted list of all 8877690 special numbers.

`check` first reports 4 errors on the template, and `karac fix` carries
it in one call, reporting 10 edits: `struct Solution;` given its braces
and `Vec<u8>` its brackets; `into_bytes()` written `bytes().to_vec()`;
`!` written `not`; `Solution::` written with a dot and the wrapper's
`as i64` dropped, since an `i32` widens; and the three counts that start
from a bare literal, `res` and the two `cur`s, given their `i32`, which
the `i32` they are added to or returned as asks for. The `[false; 10]`
array, `as usize` and `(9 - i - k) as i32` stand as Kāra.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every integer from 1 to `n` taken apart by `% 10` and counted
when no digit comes twice. No arithmetic on the digits of `n`. It checks
300 random `n` of 1 to 5 digits; then 30 of 6 or 7 digits; then 30
special numbers of 4 to 6 different digits. All 360 are drawn before any
arm answers, and the literal reading answers the 319 below `10^5`.

| | property |
|---|---|
| P1 | below `10^5`, the answer is the literal reading's |
| P2 | less the answer for `n - 1`: 1 when `n`'s digits are all different, else 0 |
| P3 | from 1 to `n` |
| P4 | for `n + e`, `e` from 1 to 1000: from the answer to the answer plus `e` |
| P5 | every digit after `n`'s first repeated one made 0: the same answer |
| P6 | each arm agrees with at least three of the other five |

P2 and P4 hold because each number is counted once, when it is special.
P5 holds because every number from the zeroed `n` up to `n` begins with
the same digits up to and including the repeated one, so none of them
is special. For `n = 1`, P2 takes the answer for 0 as 0, which no arm is
asked; and the `e` of P4 is the case's number times 37, modulo 1000,
plus 1.

The differential prints `360 cases: checksum 130387159, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and counts every integer. On a failure it prints the
first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: each shorter length counted as 9 | P1 201, P4 41, P6 242 |
| M2 | ★: n itself never counted | P1 230, P2 88, P3 3, P6 246 |
| M3 | ★: the first place allowed a 0 | P1 319, P2 3, P3 144, P4 66, P6 360 |
| M8 | memo: the number 0 counted | P1 319, P2 3, P3 66, P6 360 |
| M9 | memo: a leading zero taking the digit 0 | P1 201, P4 8, P6 242 |
| M10 | memo: tight kept past a smaller digit | P1 235, P2 259, P4 140, P5 51, P6 274 |
| M12 | dfs: n itself left out | P1 164, P2 85, P6 180 |
| M13 | dfs: the walk started from 0 too | P1 319, P2 191, P3 208, P4 171, P6 360 |
| M14 | dfs: the digit 9 allowed twice | P1 202, P2 9, P5 4, P6 243 |
| M18 | below: the shorter numbers from ten digits | P1 202, P2 1, P4 10, P6 243 |
| M19 | below: a repeat never stopping the count | P1 44, P2 54, P4 7, P5 60, P6 63 |
| M20 | below: no digit ever marked seen | P1 205, P2 134, P4 4, P5 70, P6 246 |
| M22 | iter: the shorter lengths through n's own | P1 319, P2 3, P3 344, P4 154, P6 360 |
| M23 | iter: the used digits counted below too | P1 183, P2 82, P4 7, P6 217 |
| M24 | iter: every digit taken as new | P1 89, P2 132, P4 6, P5 66, P6 114 |
| M28 | solution: each shorter length started at 10 | P1 253, P4 4, P6 294 |
| M29 | solution: no digit ever marked used | P1 214, P2 136, P4 4, P5 70, P6 255 |

P1 and P6 kill all seventeen, P2 fourteen, P4 thirteen, P5 six and P3
five. P5, the digits after the first repeat zeroed, fails the edits that
let the count run on past a repeated digit of `n`: a repeat never
stopping the count (M19), no digit ever marked seen or used (M20, M29),
every digit taken as new (M24) and the digit 9 allowed twice (M14), and
with them tight kept past a smaller digit (M10). P3, from 1 to `n`,
fails the edits that count 0 or more numbers than there are: the first
place allowed a 0 (M3), the number 0 counted (M8), the walk started
from 0 (M13), the shorter lengths run through `n`'s own (M22), and `n`
itself never counted (M2), which answers 0 for `n = 1`.

Of the thirty-one, fourteen were not kept. `n` itself never counted in
the below arm and the template (M17, M27) fails as in the ★ arm (M2);
the first place allowed a 0 in the iter arm and the template (M26,
M31) as in the ★ arm (M3); the used digits counted below too and a
repeat never stopping the count in the ★ arm (M5, M6) as the iter arm's
used digits counted below and every digit taken as new (M23, M24); and
the places after arranged from ten digits in the ★ and iter arms (M4,
M25) fail alike. The memo keyed without the place (M11), the dfs arm's
one-digit numbers not counted and only the last digit passed down
(M15, M16), the below arm's places after one too many (M21) and the
template's places after one short (M30) fail apart from every kept one,
and were left out to keep three to an arm and two to the template, as
were M4 and M25. The memo arm's tight count kept in the memo (M7)
survives and changes nothing: the number that still follows `n` is the
last one tried at its place, so its count is stored after every lookup
that could read it.

## Verification

Every arm prints the same output as `special.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.3 to 0.7 s, the memo 3.7 s, but
the dfs arm 16 s: it takes one step for each special number up to `n`,
5974650 for `2 * 10^9` and 2392084 for 123456789. The differential
takes 12 s there and 0.58 s under `karac __mir-llvm-run`.

## Benchmarks

The bench builds `10^5` values once from the harness's generator, each
of up to 1 to 10 digits, drawn from 30 random bits and so below `2^30`,
then makes
100 passes, pass `p` folding each answer plus `p` into the checksum,
with the ★ arm in all five languages. Every implementation prints `100
passes over 10^5 values: checksum 785598791`. Every implementation
writes out `n`'s digits and its flags of the digits used afresh in each
call: C into a stack buffer by `snprintf` and two `malloc`ed arrays, the
others into a string and two vectors.

BENCHTAB
