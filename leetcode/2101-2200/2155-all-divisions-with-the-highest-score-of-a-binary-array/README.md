# 2155. All Divisions With the Highest Score of a Binary Array

You are given a **0-indexed** binary array `nums` of length `n`. `nums`
can be divided at index `i` (where `0 <= i <= n`) into two arrays
(possibly empty) `numsleft` and `numsright`:

- `numsleft` has all the elements of `nums` between index `0` and
  `i - 1` (inclusive), while `numsright` has all the elements of nums
  between index `i` and `n - 1` (inclusive).
- If `i == 0`, `numsleft` is **empty**, while `numsright` has all the
  elements of `nums`.
- If `i == n`, `numsleft` has all the elements of nums, while
  `numsright` is **empty**.

The **division score** of an index `i` is the **sum** of the number of
`0`'s in `numsleft` and the number of `1`'s in `numsright`.

Return ***all distinct indices** that have the **highest** possible
**division score***. You may return the answer in **any order**.

```
nums = [0,0,1,0]  ->  [2,4]
nums = [0,0,0]    ->  [3]
nums = [1,1]      ->  [0]
```

**Constraints:** `n == nums.length`; `1 <= n <= 10^5`; `nums[i]` is
either `0` or `1`.

Moving the division one place to the right past a 0 adds one to the
score, and past a 1 takes one away, so one walk carries every score from
the first. O(n).

## Approaches

| file | mechanism |
|---|---|
| `divisions.kara` ★ | the 1s counted by `filter`; one walk by `enumerate` moves the division along, keeping the divisions that tie the best so far and starting over by `clear` when one beats it |
| `divisions_prefix.kara` | every score at once: the 0s before each division by `scan` from the left and the 1s after it by `scan` over `rev`, `extend`ed onto a 0 and `reverse`d; the best by `max`, the divisions that reach it by `enumerate` and `filter` |
| `divisions_relative.kara` | relative to the first division: a running balance, +1 for a 0 and -1 for a 1, and the divisions where it is highest; the 1s never counted |
| `divisions_struct.kara` | a `struct Divider` that `pass`es one place on (`mut ref self`) and tells its `score` (`ref self`), and a `struct Podium` `offer`ed each division in turn |
| `divisions_fold.kara` | one `fold` carrying (score, top, places) as a tuple, with a `match` on `next.cmp(top)` choosing to start the places over, add one, or leave them |
| `divisions_solution.kara` | LeetCode's Rust template: the 1s summed as an `i32`, `vec![0]`, `for (i, &x) in nums.iter().enumerate()`, the places pushed as `i as i32 + 1`; carried by `karac fix` in three rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 11 lines: LeetCode's three examples and four
more (a lone 0, a lone 1, a 1 then a 0, and 0 and 1 in turn), each with
its divisions in ascending order, since any order is allowed; then the
total and a checksum over 2000 random lists of 1 to 16 bits, a 1 one
time in 2, 3 or 4 in turn; then the constraints' largest, 100000 bits
of 0 and 1 in turn, all 0, and at random. `divisions.py` mirrors the ★
arm and its output is byte-identical.

No compiler gap was met. `karac fix` carries the template in three
rounds of 14, 2 and 1 edits: Rust's spellings (`<..>` to `[..]`, the `&`
dropped from the patterns `&x`, `&i` and `&x` of the loop and the
adapter's two closures, `struct Solution;` to `struct Solution {}`, the
adapter's `&Vec` to `ref Vec`, `Solution::` to `.`); then `zeros` given
the `i32` that Rust infers from `zeros + ones`, and `vec![0]` to `[0]`;
then the `ref` dropped from the adapter's parameter, which borrows
already. The prefix arm was written with Rust's `scan`, whose closure
writes through `*seen` and returns `Some(*seen)`, and `karac fix` turned
each into Kāra's, which takes the state and returns it with the item,
`Some((seen, seen))`.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every division's score counted afresh, the 0s left of it one
by one and the 1s from it on one by one, and the divisions that reach
the highest listed; no running count. Any order is allowed, so each
arm's divisions are sorted before they are compared. It checks 300
random lists of 1 to 12 bits, a 1 one time in 2, 3 or 4 in turn; then
30 all one bit; then 30 of 0 and 1 in turn. All 360 are drawn before
any arm answers.

| | property |
|---|---|
| P1 | the divisions are the statement read literally |
| P2 | the bits reversed and flipped: each division `i` becomes `n - i` |
| P3 | a 0 put in front: each division moves on by one |
| P4 | a 1 put at the end: the same divisions |
| P5 | every bit doubled: each division `i` becomes `2i`, and `2i + 1` joins them when `i + 1` is a division too |
| P6 | each arm agrees with at least three of the other five |

P3 holds since the 0 in front adds one to every score but the new
division 0's, which is the old division 0's and one short of the new
division 1. P4 holds the same way from the other end. P5 holds since a
division between the two copies of a bit scores the old scores on
either side of it added, so it reaches twice the highest only when both
do.

The differential prints `360 lists: checksum 440809426, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading of the same
lists by the same counting. On a failure it prints the first ten and
then the count by property.

## Mutation testing

Twenty-nine edits to the differential, four to seven to each arm, each
run under `karac __mir-llvm-run` and `karac __mir-run`. Seventeen are
kept, three to each Kāra arm and two to the Rust-template arm. Each kept
one is killed, fails the same way under both backends and not by a
crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: only the last of tied divisions kept | P1 101, P2 101, P6 101 |
| M2 | ★: division 0 never listed | P1 79, P2 249, P3 79, P6 79 |
| M3 | ★: a division listed one place early | P1 313, P2 360, P3 79, P5 313, P6 313 |
| M5 | prefix: the 1s counted on the left | P1 360, P3 360, P4 360, P6 360 |
| M6 | prefix: the 1s after never reversed | P1 231, P2 360, P3 77, P4 360, P6 231 |
| M8 | prefix: the last division never scored | P1 183, P2 249, P4 183, P5 129, P6 183 |
| M9 | relative: a 1 passed costing nothing | P1 231, P2 360, P4 360, P6 231 |
| M10 | relative: the high mark starting below the first division | P1 79, P2 249, P3 79, P5 47, P6 79 |
| M25 | relative: the high mark never raised | P1 152, P2 171, P3 133, P4 227, P5 54, P6 152 |
| M13 | struct: the divider never moving on | P1 313, P2 360, P3 360, P6 313 |
| M14 | struct: each score offered before its bit is passed | P1 249, P2 249, P3 96, P4 183, P5 129, P6 249 |
| M15 | struct: a 1 passed counted as a 0 | P1 360, P3 267, P4 157, P6 360 |
| M17 | fold: a new best keeping the old places | P1 281, P2 347, P3 360, P6 281 |
| M18 | fold: a lower score lowering the top | P1 152, P2 244, P6 152 |
| M27 | fold: a tie listed one place early | P1 101, P2 101, P5 101, P6 101 |
| M22 | solution: the list starting at division 1 | P1 79, P2 249, P3 79, P5 79, P6 79 |
| M23 | solution: the adapter's bits reversed | P1 213, P3 220, P4 311, P6 213 |

P1 and P6 kill all seventeen, P2 fourteen (all but M5, M15 and M23),
P3 twelve, P4 eight and P5 seven. A wrong division shows at once
against the literal reading and the other arms, so what the other
properties add is the shape of each failure. P3 sees an edit that
treats division 0 apart (M2, M10, M22), since the 0 in front makes a
new division 0 that is never the best. P4 sees one that treats the last
bit or the last division apart (M8, M9). P5 sees one that gets the ties
wrong, since doubling every bit puts a tie between every two
neighbouring best divisions: M27 lists a tie one place early and fails
P1, P2 and P6 just as M1, which keeps only the last of a tie, does, and
P5 alone tells them apart.

Of the twenty-nine, twelve were not kept. Two are equivalent: the ★ and
fold arms' first score taken as the count of 0s rather than of 1s
(M4, M19), which moves every score by the same amount and so picks the
same divisions. Six fail as a kept one does: the prefix arm's lowest
score taken, as M15; the relative arm's tie starting the list over and
the fold arm's tie starting the places over, as M1; the relative arm's
last bit never passed, as M8; the struct's podium never cleared, as
M17; and the fold arm's 1 passed costing nothing, as M9. Four fail in
ways of their own but were left out to keep three to each Kāra arm and
two to the template: the template's new best listed one place early
(M21) and its best starting one above division 0 (M24), the fold arm's
first division scored one above its count (M28), which fails as M24
does, and the relative arm's fall below the high mark starting the list
over (M26).

## Verification

Every arm prints the same output as `divisions.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.6 s to 2.8 s and the
differential 0.7 s.

## Benchmarks

The bench builds 4 lists of 100000 random bits once; then solves every
list 50 times, one bit at a random place flipped before each solve so
that no solve repeats one before, with the ★ arm in all five languages.
Every implementation prints `200 solves: 350 divisions in all, checksum
668585728`.

BENCHTAB
