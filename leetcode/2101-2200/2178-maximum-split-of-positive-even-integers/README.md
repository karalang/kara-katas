# 2178. Maximum Split of Positive Even Integers

You are given an integer `finalSum`. Split it into a sum of a **maximum**
number of **unique** positive even integers.

- For example, given `finalSum = 12`, the following splits are **valid**
  (unique positive even integers summing up to `finalSum`): `(12)`,
  `(2 + 10)`, `(2 + 4 + 6)`, and `(4 + 8)`. Among them, `(2 + 4 + 6)`
  contains the maximum number of integers. Note that `finalSum` cannot
  be split into `(2 + 2 + 4 + 4)` as all the numbers should be unique.

Return *a list of integers that represent a valid split containing a
**maximum** number of integers*. If no valid split exists for
`finalSum`, return *an **empty** list*. You may return the integers in
**any** order.

```
finalSum = 12  ->  [2, 4, 6]
finalSum = 7   ->  []
finalSum = 28  ->  [2, 4, 6, 16]
```

**Constraints:** `1 <= finalSum <= 10^10`.

An odd sum has no split. Otherwise k distinct evens sum to at least 2 +
4 + ... + 2k = k(k + 1), so the most parts is the largest k with k(k +
1) at most the sum: take 2, 4, 6, ... while what is left is at least the
next one, and add what is left to the last, which keeps the parts
distinct. O(sqrt(finalSum)).

## Approaches

| file | mechanism |
|---|---|
| `split.kara` ★ | 2, 4, 6, ... pushed while what is left holds the next, and the rest added to the last |
| `split_formula.kara` | the most parts k as the largest with k(k + 1) at most the sum, by a binary search; the parts `map`ped from 1 to k and `collect`ed, the rest on the last |
| `split_rec.kara` | a recursion over what is left and the smallest part: it takes the part when the rest still holds a larger one, and is otherwise the rest alone; the parts pushed onto a list passed `mut ref` |
| `split_struct.kara` | a `struct Split` of the parts so far and what is left, made `of` a sum, that `can_take` the next even (`ref self`), `take`s it (`mut ref self`), and is `finish`ed (`own self`) with the rest on its last part |
| `split_iter.kara` | the evens `map`ped from `1..`, `scan`ned to their running totals, `take_while` the total is at most the sum, `map`ped back and `collect`ed; their `sum` gives the rest for the last |
| `split_solution.kara` | LeetCode's Rust template: `-> Vec<i64>`, `vec![]`, `Vec::new()`, `*res.last_mut().unwrap() += rest`, `struct Solution;`, `Solution::`; carried by `karac fix` in two rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 10 lines: LeetCode's three examples and four
more (2, 4, 1, and 38, which leaves 8 after 2 to 10, too little for a
12), each with its split; then the parts in all and a checksum over 2000
random sums of up to 100, 10^4 or 10^6 in turn; then the constraints'
largest, 10^10 and the even sum just under it, each with its count, its
last part and a checksum. `split.py` mirrors the ★ arm and its output is
byte-identical.

`karac fix` carries the template in two rounds of 7 and 2 edits: Rust's
spellings (`Vec<i64>` to `Vec[i64]` in both signatures, `Vec::new()` to
`Vec.new()`, `struct Solution;` to `struct Solution {}`, and
`Solution::` to `.`, among them); then `vec![]` to `Vec.new()`, and
`*res.last_mut().unwrap() += rest` to `res[res.len() - 1] += rest`.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: a table over every sum up to the number of the most distinct
positive evens that make it, each even from 2 up offered once, as in a
0/1 knapsack; the most for the number. No greedy walk and no rest put on
a last part. It checks 300 random sums of 1 to 200; then 30 that are
exactly 2 + 4 + ... + 2k; then 30 just short of the next, k(k + 1) + 2k.
All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the number of parts is the statement read literally |
| P2 | an even sum 2(k + 1) more, for k parts: exactly one part more |
| P3 | the sum 2 more: no fewer parts |
| P4 | the sum doubled: no fewer parts |
| P5 | the parts are distinct positive evens that make the sum, and there are none only for an odd sum |
| P6 | each arm agrees with at least three of the other five |

P2 holds since an even sum s with k parts has k(k + 1) <= s < (k + 1)(k
+ 2), and adding 2(k + 1) moves both bounds up by exactly one step. P3
and P4 hold since the most parts is the largest k with k(k + 1) at most
the sum, which does not fall as the sum grows, and an even sum stays
even.

The differential prints `360 sums: checksum 100972656, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading of the same
sums. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Twenty-nine edits to the differential, three to six to each arm, each
run under `karac __mir-llvm-run` and `karac __mir-run`. Seventeen are
kept, three to each Kāra arm and two to the Rust-template arm. Each kept
one is killed, fails the same way under both backends and not by a
crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the rest left off the last | P5 159, P6 159 |
| M4 | ★: the rest put on the first | P5 104, P6 153 |
| M5 | ★: the parts stepping by 4 | P1 189, P2 90, P6 190 |
| M7 | formula: the search capped at 10 | P1 69, P2 87, P6 69 |
| M8 | formula: k one less | P1 195, P2 50, P6 195 |
| M9 | formula: the rest counted from k squared | P5 203, P6 203 |
| M11 | rec: a part taken while the rest holds it alone | P1 55, P5 55, P6 55 |
| M12 | rec: a part taken while the rest holds two more | P1 42, P2 2, P6 42 |
| M13 | rec: the next smallest 4 more | P1 180, P2 101, P6 184 |
| M18 | struct: taking leaves what was left | P1 188, P2 134, P5 203, P6 203 |
| M20 | struct: an odd sum split | P1 149, P5 149, P6 149 |
| M29 | struct: at most 12 parts | P1 21, P2 45, P6 21 |
| M21 | iter: the evens from 0 | P1 180, P5 203, P6 203 |
| M23 | iter: the running total of the counts | P1 201, P2 203, P5 201, P6 201 |
| M25 | iter: the rest on the second last | P5 10, P6 153 |
| M26 | solution: the adapter's sum 2 less | P1 42, P2 2, P5 201, P6 201 |
| M27 | solution: an odd sum told by 4 | P1 81, P3 81, P5 81, P6 81 |

P6 kills all seventeen, P1 thirteen, P5 eleven, P2 nine, P3 one and P4
none. P1 counts the parts only, so it misses the four edits that get the
count right but the parts wrong: the rest left off (M1), on the first
(M4) or on the second last (M25), and counted from k squared (M9); P5
sees each of them, since the parts no longer make the sum or are no
longer distinct. P5 in turn misses an edit that gives a valid split
with too few parts (M5, M7, M8, M12, M13, M29). P2 steps the sum to the
next count, and sees an edit whose count is off by a number that changes
from one k to the next: steps of 4 (M5), the cap (M7, M29), k one less
at its edge (M8), the loose and tight tests (M12, M13), and the sum
shifted (M26). P3 adds 2, and sees only the odd sum told by 4 (M27),
which answers an even sum 2 more than a multiple of 4 with none. P4 sees
no kept edit: each one's count still does not fall when the sum doubles.

Of the twenty-nine, twelve were not kept. One is equivalent: the formula
arm's parts as the odd numbers plus 1 (M10), which are the evens. Five
crash, each by indexing the last of no parts: the ★ arm's part taken
while the rest is more than it and its evens from 4 (M2, M3), the struct
arm's next even one place on and its take while more is left (M16,
M17), and the template's pushes from 2 to the rest (M28). Five fail as
a kept one does: the formula arm's search keeping k(k + 1) under the sum
(M6), as M12; the rec arm's last part halved (M14), as M9; the struct
arm's rest on the first part (M19), as M4; the iter arm's total let
past the sum (M22), as M11; and its rest left off (M24), as M1. One was
left out to keep three to an arm: the rec arm's odd sum split too (M15).

## Verification

Every arm prints the same output as `split.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the ★ and template arms take 0.4 s, the struct
arm 0.8 s, the formula and rec arms 1.1 s and 1.2 s, and the iter arm 4.0
s, which runs a chain of four adapters for each of the 2 x 10^5 parts of
the two largest sums. The differential takes 0.7 s.

## Benchmarks

The bench solves 400 random sums of up to 10^10, so that no solve
repeats one before, and folds every part into a checksum, with the ★ arm
in all five languages: about 3.4 x 10^4 parts a solve, each pushed onto
a growing list. Every implementation prints `400 solves: 13452484
parts, checksum 628074714`.

BENCHTAB
