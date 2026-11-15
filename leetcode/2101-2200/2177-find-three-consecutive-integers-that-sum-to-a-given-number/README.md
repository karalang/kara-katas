# 2177. Find Three Consecutive Integers That Sum to a Given Number

Given an integer `num`, return *three consecutive integers (as a sorted
array) that **sum** to* `num`. If `num` cannot be expressed as the sum
of three consecutive integers, return *an **empty** array.*

```
num = 33  ->  [10, 11, 12]
num = 4   ->  []
```

**Constraints:** `0 <= num <= 10^15`.

Three consecutive integers x - 1, x and x + 1 sum to 3x, so a number is
such a sum exactly when 3 divides it, and then x is its third. O(1).

## Approaches

| file | mechanism |
|---|---|
| `three.kara` ★ | none unless 3 divides the number, and then the three around its third |
| `three_search.kara` | a binary search from -1 to the number for the least middle whose sum 3x is at least the number, kept if it hits it; O(log num) |
| `three_option.kara` | the middle as an `Option[i64]`, `Some` only when 3 divides the number, and a `match` that spells the three out or gives none |
| `three_struct.kara` | a `struct Run` of three by its first, made `summing_to` a number from the floor of its third by `div_euclid`, kept only if its `sum` (`ref self`) is the number; its `to_vec` gives the three |
| `three_iter.kara` | `Some` of the number's third, `filter`ed to one that times 3 is the number, `map`ped to the range around it `collect`ed, and `unwrap_or` an empty list |
| `three_solution.kara` | LeetCode's Rust template: `num: i64`, `-> Vec<i64>`, `vec![]`, `vec![x - 1, x, x + 1]`, `struct Solution;`, `Solution::`; carried by `karac fix` in two rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's two examples and four more
(0, 3, 10^15, and the largest multiple of 3 below it), each with its
three; then how many were found and a checksum over 2000 random numbers
of up to 10, 1000 or 10^15 in turn; then the same over every number from
0 to 3000. `three.py` mirrors the ★ arm and its output is
byte-identical.

The iterator arm's `.map(|x| ((x - 1)..(x + 2)).collect()).unwrap_or(Vec.new())`,
returned as a `Vec[i64]`, was at first refused with "expected '?T7',
found 'Vec[?T8]'": the `Option`'s element was still the `collect`'s open
output, and a slot that is one open variable did not take an open value
handed to it. That is ledger row B-2026-11-15-29, fixed in karac b545bd3ba1, which
fixes `unwrap_or_else(|| Vec.new())` too.

`karac fix` carries the template in two rounds of 6 and 2 edits: Rust's
spellings (`Vec<i64>` to `Vec[i64]` in both signatures, `struct
Solution;` to `struct Solution {}`, and `Solution::` to `.`); then
`vec![]` to `Vec.new()` and `vec![x - 1, x, x + 1]` to the list literal
`[x - 1, x, x + 1]`.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every first integer from -1 up to the number tried, and the
first whose run of three sums to the number kept, or none. No division.
It checks 300 random numbers of up to 10, 100 or 3000 in turn; then 30
multiples of 3; then 30 one or two past a multiple of 3. All 360 are
drawn before any arm answers.

| | property |
|---|---|
| P1 | the three are the statement read literally |
| P2 | the number 3 more: each of the three 1 more, or none again |
| P3 | the number times 4: the middle times 4, or none again |
| P4 | the number 1 more and 2 more: none, when the number has three |
| P5 | three found are consecutive and sum to the number, and none are found only when 3 does not divide it |
| P6 | each arm agrees with at least three of the other five |

P2 holds since each of the three 1 more sums to 3 more. P3 holds since
3 divides 4n exactly when it divides n, and then the middle is 4n / 3.
P4 holds since of three numbers in a row, 3 divides only one.

The differential prints `360 numbers: checksum 94269377, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading of the same
numbers. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Thirty-four edits to the differential, five to eight to each arm, each
run under `karac __mir-llvm-run` and `karac __mir-run`. Seventeen are
kept, three to each Kāra arm and two to the Rust-template arm. Each kept
one is killed, fails the same way under both backends and not by a
crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M3 | ★: a remainder of 1 taken too | P1 129, P3 129, P4 245, P5 129, P6 129 |
| M4 | ★: the number's half taken for its third | P1 101, P2 56, P3 56, P5 101, P6 101 |
| M5 | ★: 0 found none | P1 6, P2 6, P5 6, P6 6 |
| M8 | search: the low end raised past an equal middle | P1 110, P2 6, P5 110, P6 110 |
| M9 | search: a hit within 1 taken | P1 115, P3 115, P4 231, P5 115, P6 115 |
| M34 | search: the search capped at 2000 | P3 29 |
| M11 | option: the middle `Some` for an even number too | P1 123, P2 244, P3 244, P4 239, P5 123, P6 123 |
| M14 | option: `None` for the multiples of 9 | P1 39, P2 73, P5 39, P6 39 |
| M29 | option: `None` above 1000 | P1 39, P3 12, P5 39, P6 39 |
| M17 | struct: a run's sum 3 times its first | P1 116, P5 116, P6 116 |
| M18 | struct: every run kept, since its sum is never above the number | P1 244, P3 244, P4 360, P5 244, P6 244 |
| M30 | struct: a run's sum 1 more past a first of 1000 | P3 83 |
| M23 | iter: the third kept only when even | P1 56, P2 116, P3 56, P5 56, P6 56 |
| M32 | iter: a third under 500 only | P1 29, P3 22, P5 29, P6 29 |
| M33 | iter: none spelled as a lone 0 | P1 244, P2 244, P3 244, P4 360, P5 244, P6 244 |
| M26 | solution: the adapter's number 3 less | P1 116, P3 116, P5 116, P6 116 |
| M28 | solution: none for a multiple of 6 | P1 60, P2 116, P3 56, P5 60, P6 60 |

P1, P5 and P6 kill fifteen, P3 twelve, P2 eight and P4 five. The two
that only P3 sees (M30, M34) go wrong only past a middle of 1000 or
2000, which the differential's numbers, at most 3000, reach only once
P3 multiplies them by 4. P3 also sees an edit whose middle is wrong by
an amount that does not grow fourfold: a shift of the three by one
(M26), a third that is not one (M4), one let through within 1 (M3,
M9) or always (M18), and those that drop a middle by its size or its residue (M11,
M23, M28, M29, M32). P2 adds 3, and sees an edit that treats neighbouring
multiples of 3 apart: by parity (M11, M23, M28), by 9 (M14), at 0 (M5,
M8), the half (M4), and the lone 0 (M33). P4 asks the next two numbers,
and sees an edit that finds three where 3 does not divide: a remainder
of 1 (M3), within 1 (M9), always (M18), an even number (M11), and the
lone 0 (M33).

Of the thirty-four, seventeen were not kept. Three are equivalent: the
search arm's low end from 0 (M6) and its high end at half the number
(M7), since the middle of a number from 0 up is between them, and the
option arm's third rounded up (M12), which is the third whenever 3
divides the number. Fourteen fail as a kept one does. Five shift or
misspell the three wherever they are found, as M26: the ★ arm's middle
one less and its three from the third up (M1, M2), the iter arm's range
one short and from the third (M21, M24), and the template's middle one
more (M27). Five give a wrong three that P3 does not scale, as M17: the
search arm's last one more (M10), the option arm's middle twice and the
three reversed (M13, M15), and the struct arm's first one more and last
one more (M16, M19). The struct arm's first from a quarter (M20) fails
as M8; the iter arm's filter never applied (M22) as M18; its near third
let through (M25) as M3; and the struct arm's even first only (M31) as
M28.

## Verification

Every arm prints the same output as `three.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.1 s to 0.2 s, and the
differential 0.2 s.

## Benchmarks

The bench builds one row of 10^6 numbers up to 10^15 once; then makes
two passes, asking each number and then its successor for its three, 2 x
10^6 solves, each of which builds a list for the numbers that have
three, with the ★ arm in all five languages. Every implementation prints
`2000000 solves: 666709 found, checksum 799960228`.

BENCHTAB
