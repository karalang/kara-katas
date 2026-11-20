# 2354. Number of Excellent Pairs

You are given a **0-indexed** positive integer array `nums` and a
positive integer `k`.

A pair of numbers `(num1, num2)` is called **excellent** if the
following conditions are satisfied:

- **Both** the numbers `num1` and `num2` exist in the array `nums`.
- The sum of the number of set bits in `num1 OR num2` and `num1 AND
  num2` is greater than or equal to `k`, where `OR` is the bitwise
  **OR** operation and `AND` is the bitwise **AND** operation.

Return *the number of **distinct** excellent pairs*.

Two pairs `(a, b)` and `(c, d)` are considered distinct if either
`a != c` or `b != d`. For example, `(1, 2)` and `(2, 1)` are distinct.

**Note** that a pair `(num1, num2)` such that `num1 == num2` can also be
excellent if you have at least **one** occurrence of `num1` in the
array.

```
nums = [1,2,3,1], k = 3   ->  5
nums = [5,1,1], k = 10    ->  0
```

**Constraints:** `1 <= nums.length <= 10^5`; `1 <= nums[i] <= 10^9`;
`1 <= k <= 60`.

A bit set in both `a` and `b` is counted once in `a OR b` and once in
`a AND b`, and a bit set in one of them once in `a OR b` only, so the
sum is the set bits of `a` plus those of `b`. Only each distinct
value's count of set bits matters, and `10^9 < 2^30` holds at most 30.

## Approaches

| file | mechanism |
|---|---|
| `excellent.kara` ★ | the distinct values in a `Set`, tallied by `count_ones`, then every two tallies whose bits reach `k` multiplied. O(n + 31^2) |
| `excellent_pointers.kara` | two pointers: the values sorted and `dedup`ed, their bit counts sorted, and for each count from the smallest a pointer from the top walked down while the pair still reaches `k`. O(n log n) |
| `excellent_search.kara` | binary search: the distinct values' bit counts sorted, and for each one the first count that reaches `k` with it found by halving. O(n log n) |
| `excellent_naive.kara` | every pair: the distinct values, and for each ordered pair the bits of `a \| b` and of `a & b` counted as the statement says. O(d^2) for `d` distinct values |
| `excellent_iter.kara` | iterators: the bit counts tallied by `fold` into an array, and the pairs of tallies multiplied and summed by `flat_map`, `filter` and `sum` |
| `excellent_solution.kara` | LeetCode's Rust template: a `HashSet<i32>` built by `into_iter().collect()`, tallies by `count_ones() as usize`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 7 lines: LeetCode's two examples; 7 alone,
with `k` at its bits doubled and one past; `10^5` copies of `2^30 - 1`
with `k = 60`; `10^5` values over 2000 distinct, with `k` from 1 to 57
in steps of 7; then 2000 random arrays of 1 to 30 values from 1 to
`2^b`, `b` from 1 to 30, with `k` from 1 to `2 b + 1`, with a checksum,
the pairs summed and how many arrays have none. `excellent.py` mirrors
the ★ arm and its output is byte-identical, and the mirror was checked
against every pair counted with `bin(a | b)` and `bin(a & b)` on 3000
random arrays.

`count_ones` on an `i64` returns the count as an `i64`, which indexes
the tally directly.

`karac fix` carries the template in one call, reporting 11 edits.
`check` first reports 5 errors, each with its edit: the `HashSet`
import deleted, `struct Solution;` given braces, the angle brackets of
`Vec<i32>` and `HashSet<i32>` made square, and the `::` call written
with `.`. The rest follow: `HashSet` made the prelude's `Set`, `nums`
taken `own` since `into_iter` consumes it, and the `i64` suffixes of
`0i64` dropped, since Kāra infers the tallies' type from the `i64` they
are added into. `count_ones() as usize` and `(a + b) as i32` stand as
Kāra.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every ordered pair of distinct values, the bits of `a OR b`
and of `a AND b` counted one place at a time, and the pair counted when
the two counts reach `k`. No bit counts added. It checks 300 random
arrays of 1 to 30 values from 1 to `2^b`, `b` from 1 to 30, with `k`
from 1 to `2 b + 1`; then 30 of up to 300 values from 1 to 64; then 30
of up to 300 values of 25 to 30 bits set, with `k` from 40 to 60. All
360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | up to 60 values, the answer is the literal reading's |
| P2 | from 0 to `d^2` for `d` distinct values, and the answer less the values whose bits doubled reach `k` is even |
| P3 | `k` lowered by one: no fewer pairs |
| P4 | the values given twice over: the same answer |
| P5 | the low 30 bits of every value reversed: the same answer |
| P6 | each arm agrees with at least three of the other five |

P2's evenness holds because a pair of two different values is
excellent both ways round, so only the pairs of a value with itself can
be odd in number. P5 holds because reversing the low 30 bits is one to
one on the values and keeps every value's count of set bits.

The differential prints `360 cases: checksum 687459368, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and counts with `bin`. On a failure it prints the first
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
| M1 | ★: bits that only reach k left out | P1 125, P2 49, P6 152 |
| M2 | ★: repeated values counted | P1 67, P2 91, P4 259, P6 107 |
| M3 | ★: two tallies added, not multiplied | P1 302, P2 303, P6 349 |
| M8 | pointers: one pair fewer for each count | P1 313, P2 239, P6 360 |
| M9 | pointers: the pointer moved only while the pair is exactly k | P1 165, P2 99, P3 21, P6 190 |
| M10 | pointers: the bit counts left unsorted | P1 97, P2 64, P5 111, P6 120 |
| M12 | search: each count taken after its lowest bit is dropped | P1 129, P2 91, P5 153, P6 157 |
| M13 | search: the last count never found | P1 144, P2 76, P6 163 |
| M14 | search: the search started at the second count | P1 169, P2 105, P6 197 |
| M17 | naive: only the bits of a OR b | P1 166, P2 107, P6 207 |
| M18 | naive: a XOR b for a AND b | P1 214, P2 107, P6 259 |
| M19 | naive: no value paired with itself | P1 218, P2 134, P6 259 |
| M22 | iter: only pairs whose bits are exactly k | P1 204, P2 133, P3 82, P6 241 |
| M23 | iter: each count tallied at most once | P1 188, P2 108, P6 225 |
| M24 | iter: the first tally squared | P1 301, P2 334, P6 347 |
| M27 | solution: only the low 16 bits counted | P1 61, P2 39, P5 200, P6 85 |
| M28 | solution: only the first tally added | P1 306, P2 291, P6 353 |

P1, P2 and P6 kill all seventeen, P5 three, P3 two and P4 one. P2's
evenness catches nearly every miscount, since almost any slip in a
count of pairs breaks the symmetry between `(a, b)` and `(b, a)`. P5,
the bits reversed, fails only the edits that read a value's bits by
place rather than by count: a count taken after the lowest bit is
dropped, the low 16 bits only, and the pointers arm's counts left
unsorted, whose walk then depends on the order the values sort in. P3,
`k` lowered by one, fails only the two edits that count pairs reaching
exactly `k`, the only ones whose answer is not monotone in `k`. P4,
the values given twice over, fails only repeated values counted, the
one edit that sees duplicates.

Of the thirty-one, fourteen were not kept, and four first written were
replaced. Bits that only reach `k` left out was first written in the
pointers, search, iter and template arms as in the ★ arm (M1), and all
five failed alike; the four copies were rewritten as the pairs exactly
`k` (M9, M22) and value-reading edits (M12, M27), since nothing else
killed P3 or P5. Repeated values kept or counted in the pointers,
search and naive arms (M7, M16, M21) fail as in the ★ arm (M2); the
pointer started below the top (M11) as the last count never found
(M13); the first count never paired (M15) as the search started at the
second count (M14); and only the second count below the first in the
template (M30) as no value paired with itself (M19). Each pair of
counts taken once fails alike in the ★ and iter arms (M4, M25). That
pair, the ★ arm's value tallied one bit short (M5) and no first value
with more than 15 bits (M6), one bit short of `k` enough (M20), pairs
of counts counted (M26), bit counts halved (M29) and every tally
started at 1 (M31) fail apart from every kept one; they were left out
to keep three to an arm and two to the template.

## Verification

Every arm prints the same output as `excellent.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the pointers and search arms take 0.8 and
1.6 s, the ★ arm 2.2 s and the iter arm 5.7 s, both building a `Set` of
`10^5` values for each of the line's nine calls, the template 4.6 s,
whose set holds `i32`s taken by `into_iter`, and the naive arm 22 s,
its `2000^2` pairs nine times over. The differential takes 8.3 s there
and 0.58 s under `karac __mir-llvm-run`.

## Benchmarks

The bench builds 10 arrays of `10^5` values once, array `a` holding
values from 1 to `10^9` with up to `10^(4 + a / 2)` distinct, then makes
20 passes, pass `p` asking each array for `k = 1 + (7 p + a) mod 60` and
folding each answer plus `p` into the checksum, with the ★ arm in all
five languages. Every implementation prints `20 passes over 10 arrays
of 10^5 values: checksum 39013704`. Each call builds its own set of the
distinct values; C has no set, so it finds them in a table of `2^18`
slots by open addressing, cleared for each call.

BENCHTAB
