# 2310. Sum of Numbers With Units Digit K

Given two integers `num` and `k`, consider a set of positive integers
with the following properties:

- The units digit of each integer is `k`.
- The sum of the integers is `num`.

Return *the **minimum** possible size of such a set, or* `-1` *if no
such set exists.*

Note:

- The set can contain multiple instances of the same integer, and the
  sum of an empty set is considered `0`.
- The **units digit** of a number is the rightmost digit of the number.

```
num = 58, k = 9  ->  2      (9 + 49)
num = 37, k = 2  ->  -1
num = 0, k = 7   ->  0
```

**Constraints:** `0 <= num <= 3000`; `0 <= k <= 9`.

A set of `n` numbers ending in `k` sums to `n k` plus a multiple of 10,
and any multiple of 10 can be added to one of its numbers; for `k = 0`
each number is itself a multiple of 10 from 10 up, and `n k = 0`
leaves room for that whenever `num` is. So `n` numbers can sum to
`num` exactly when `n k <= num` and `num - n k` is a multiple of 10.
`n` and `n + 10` leave the same units digit, so only 1 to 10 need
trying, and a larger `n` only raises `n k`: the least one that fits is
the answer. O(1).

## Approaches

| file | mechanism |
|---|---|
| `units.kara` ★ | 0 for a sum of 0; otherwise `n` from 1 to 10, the first with `n * k <= num` and `(num - n * k) % 10 == 0`, and -1 after |
| `units_naive.kara` | coin change: the numbers ending in `k` up to `num` as coins, any number of each, and `fewest[s]` the fewest summing to `s`, built from 0 up, -1 where none does. O(num^2 / 10) |
| `units_bfs.kara` | breadth first over the sums from 0, a `VecDeque[i64]` of those still to grow and each step adding one number ending in `k`; the step that first reaches `num` is the size. O(num^2 / 10) |
| `units_digit.kara` | the units digit walked: `n` numbers of `k` end in `digit`, which moves on by `k` mod 10, and total `total`, which moves on by `k`; the first `n` whose digit is `num`'s while `total` fits, with no multiplication |
| `units_iter.kara` | `(1..=10).find(..)` of the same test as the ★ arm, `unwrap_or(-1)`, and 0 for a sum of 0 |
| `units_solution.kara` | LeetCode's Rust template: `i32` in and out, the counts 1 to 10 tried with `&&` between the two tests; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 10 lines: LeetCode's three examples; 10 made
of one 10; 0 with `k = 0`; the largest sum, 3000, with units digits 9
and 3, which take 10 numbers each, 2999 with 1, and 2998 with 5, which
no count of numbers ending in 5 can make; then every sum from 0 to 200
with every units digit, 2010 cases, with a checksum and the count of
impossible ones. `units.py` mirrors the ★ arm and its output is
byte-identical.

`karac fix` carries the template in one call, reporting 5 edits:
`struct Solution;` to `struct Solution {}`; `&&` to `and`;
`Solution::minimum_numbers` to `Solution.minimum_numbers` in the
harness's wrapper; then, in the second round, `1..=10` to `1i32..=10`,
since the loop's `i` is returned as the method's `i32` and a bare
range would be `i64`; and the wrapper's `as i64` on the `i32` answer
dropped, as it widens on its own.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: for each size from 0 up, every multiset of that many
positive numbers ending in `k`, as a non-increasing list, is searched
by recursion for one summing to `num`; the first size that has one is
the answer, and -1 once every size up to `num` has none. No units-digit
argument. It checks every `num` from 0 to 60 with every `k` from 0 to
9, 610 cases.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | the answer is 0 exactly when `num` is 0, and otherwise -1 or from 1 to 10 |
| P3 | `num + 10`, where the answer `n` is 1 or more: `n` again |
| P4 | `num - 10`, where the answer `n` is 1 or more and `num - 10` is above 0 and at least `n k`: `n` again |
| P5 | `num - k`, where the answer `n` is 2 or more: `n - 1` |
| P6 | each arm agrees with at least three of the other five |

P3 and P4 hold because the answer, when there is one, is the least
count with the right units digit, and adding or taking off 10 changes
neither the digit nor whether that count fits. P5 holds because one
number of `k` fewer leaves `n - 1` numbers with the right digit for
`num - k`, and no fewer could have it.

The differential prints `610 cases: checksum 232765849, 21960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that runs
the same search, memoized. On a failure it prints the first ten and
then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M4 | ★: the units digit tested for 1, not 0 | P1 418, P6 418 |
| M5 | ★: a sum of exactly `n k` refused | P1 56, P4 54, P6 56 |
| M6 | ★: the count tried from 2 | P1 60, P5 56, P6 60 |
| M8 | naive: the coins 5 apart, not 10 | P1 193, P4 1, P6 193 |
| M9 | naive: the most coins kept, not the fewest | P1 138, P2 98, P3 142, P4 5, P5 5, P6 138 |
| M10 | naive: the largest coin left out | P1 106, P2 17, P3 14, P4 24, P5 55, P6 106 |
| M12 | bfs: each sum given the steps of the one before it | P1 277, P2 277, P6 277 |
| M13 | bfs: every number 10 larger | P1 170, P4 32, P6 170 |
| M14 | bfs: a sum 10 on queued again, its steps rewritten | P1 5, P3 6, P4 5, P5 5, P6 5 |
| M18 | digit: the digit not wrapped at 10 | P1 133, P6 133 |
| M19 | digit: the total never moved on | P1 101, P5 22, P6 101 |
| M21 | digit: five steps, not ten | P1 57, P6 57 |
| M22 | iter: a sum of 0 impossible | P1 10, P2 10, P6 10 |
| M23 | iter: the counts tried from 0 | P1 60, P2 60, P6 60 |
| M24 | iter: the last count that fits, not the first | P1 70, P3 26, P5 13, P6 70 |
| M27 | solution: a sum of 0 taking one number | P1 10, P2 10, P3 9, P6 10 |
| M30 | solution: the count doubled | P1 277, P2 57, P5 277, P6 277 |

P1 and P6 kill all seventeen, P2 and P5 seven each, P4 six and P3
five. Most edits here change only which count is found, so the
literal reading is what catches them, and the properties catch the
ones whose answer moves with `num`: P4, `num - 10`, fails where an
edit refuses a sum on the edge of fitting (a sum of exactly `n k`
refused, coins 5 apart, numbers 10 too large) and in three that go
wrong more widely; P5, `num - k`, where an
edit's count is not the least (the count tried from 2, the last count
that fits, the count doubled); P3, `num + 10`, where an edit answers 1
for the sum 0 and the right count for 10, or where a coin or a count
leaves the answer depending on the size of `num`. P2 fails for answers
outside -1 and 1 to 10, or 0 off the sum 0.

Of the thirty-one, fourteen were not kept. Two are equivalent and
killed by nothing: the breadth-first arm taking sums from the back of
its queue (M15), which on these sums still sets each one's steps first
along the shortest way; and the template trying eleven counts (M29),
since a count with the right digit always turns up by 10. The ★ arm's
sum of 0 taking one number (M1) fails as the template's (M27), and the
template's numbers allowed past the sum (M28) as the ★ arm's (M3); the
digit arm's comparison before the digit moves (M20) as the ★ arm's nine
counts (M2); the digit arm's walk stopped one count early (M17) as the
★ arm's sum of exactly `n k` refused (M5); the template's missing
answer 0 (M31) as the iter arm's (M26). The ★ arm's numbers allowed
past the sum (M3) and nine counts (M2), the naive arm's coin of 0
(M7) and empty sum unreachable (M11), the breadth-first arm's target
never reached (M16) and the iter arm's units digit of `num - k` (M25)
and missing answer 0 (M26) fail apart from every kept one, and were
left out to keep three to an arm.

## Verification

Every arm prints the same output as `units.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the ★, digit, iter and template arms take 0.2
to 0.3 s, the breadth-first arm 0.5 s, and the naive arm, which fills
a coin-change table for each of the 2010 sums, 1.9 s. The differential
takes 0.8 s there and 0.4 s under `karac __mir-llvm-run`.

## Benchmarks

The bench makes 300 passes over every sum from 0 to 3000 with every
units digit, 30010 calls a pass, with the ★ arm in all five languages,
pass `p` folding each answer plus `1 + p` into the checksum so that no
answer is negative under `%`. Every implementation prints `300 passes
over 3001 sums and 10 digits: checksum 594670457`. Each works in 64-bit
integers, and none holds any data: the work is the loop of at most ten
multiplications and remainders a call.

BENCHTAB
