# 2172. Maximum AND Sum of Array

You are given an integer array `nums` of length `n` and an integer
`numSlots` such that `2 * numSlots >= n`. There are `numSlots` slots
numbered from `1` to `numSlots`.

You have to place all `n` integers into the slots such that each slot
contains at **most** two numbers. The **AND sum** of a given placement
is the sum of the **bitwise** `AND` of every number with its respective
slot number.

- For example, the **AND sum** of placing the numbers `[1, 3]` into slot
  `1` and `[4, 6]` into slot `2` is equal to `(1 AND 1) + (3 AND 1) + (4
  AND 2) + (6 AND 2) = 1 + 1 + 0 + 2 = 4`.

Return *the maximum possible **AND sum** of* `nums` *given* `numSlots`
*slots.*

```
nums = [1, 2, 3, 4, 5, 6],  numSlots = 3  ->  9
nums = [1, 3, 10, 4, 7, 1], numSlots = 9  ->  24
```

**Constraints:** `1 <= numSlots <= 9`; `1 <= n <= 2 * numSlots`; `1 <=
nums[i] <= 15`.

A slot holds none, one or two numbers, so how full the slots are is a
number in base 3, one digit a slot, and the numbers placed so far are
its digits' sum: the next number goes into any slot not yet full. The
best sum of each fill is pushed forward to the fills one number more.
O(3^slots * slots).

## Approaches

| file | mechanism |
|---|---|
| `and_sum.kara` ★ | the fill in base 3 over a `Vec.filled(3^slots, -1)`, its numbers placed its digits' sum, each fill's best pushed forward to every slot with room |
| `and_sum_pairs.kara` | each slot split into two places, a fill a bit mask over twice the slots, its `count_ones` the numbers placed; each mask's best pulled from the masks with one place fewer |
| `and_sum_memo.kara` | top down: the best for the numbers still to place, by recursion over the slot the next one takes, each fill's answer kept in a memo passed `mut ref` |
| `and_sum_struct.kara` | a `struct Ternary` of the powers of 3, made `of` the slots, that reads a fill's `digit`, says whether a slot `has_room`, counts what is `placed`, and knows its `size`; the fills pushed forward in order |
| `and_sum_iter.kara` | pulled by iterators: a fill's digits by `map`, the numbers placed by `sum`, its best from the slots it holds a number in, `filter`ed, `map`ped and their `max`; the answer the `max` over the fills that hold every number |
| `and_sum_solution.kara` | LeetCode's Rust template: two places a slot, `vec![0i32; 1 << m]`, `1usize << m`, `count_ones() as usize`, `(j / 2 + 1) as i32`; carried by `karac fix` in three rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's two examples and four more
(one number in one slot, two numbers sharing one slot, eighteen 15s in
nine slots, and the numbers 1 to 9 in nine slots), each with its sum;
then the total and a checksum over 2000 random cases of 1 to 6 slots,
each holding 1 to twice the slots numbers of 1 to 15; then the
constraints' largest, nine slots and eighteen numbers at random, three
times. `and_sum.py` mirrors the ★ arm and its output is byte-identical.

`karac fix` carries the template in three rounds of 8, 6 and 1 edits:
Rust's spellings (`Vec<..>` to `Vec[..]`, `struct Solution;` to
`struct Solution {}`, the adapter's `&Vec<i64>` to `ref Vec[i64]`, its
closure's `&x` to `x`, and `Solution::` to `.`, among them); then the
`usize`s: `(num_slots * 2) as usize` to `as i64`, `vec![0i32; 1 << m]`
to `Vec.filled(1 << m, 0i32)`, `1usize << m` to `1 << m`, the `as usize`
on `count_ones()` dropped, since a count is `i64` already, `let mut ans
= 0` to `let mut ans: i32 = 0` for the `i32` sums it holds, and the
adapter's widening `as i64` dropped; then the adapter's `ref` dropped,
since a parameter borrows already.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every way to give each number a slot with room left, tried
by recursion, and the most any gives. No fill in base 3 and no masks.
It checks 300 random cases of 1 to 4 slots and 1 to twice the slots
numbers, at most 7, of 1 to 15, 1 to 3 or 8 to 15 in turn; then 30 with
every slot full; then 30 of powers of two. All 360 are drawn before any
arm answers.

| | property |
|---|---|
| P1 | the sum is the statement read literally |
| P2 | the numbers reversed: the same sum |
| P3 | one slot more: the sum no less |
| P4 | every number 16 more: the same sum |
| P5 | the sum at least the best one number gives alone, and at most what each number gives in its own best slot, added up |
| P6 | each arm agrees with at least three of the other five |

P2 holds since a placement does not care in what order its numbers
came. P3 holds since every placement in the slots is one in the slots
and one more. P4 holds since 16 is above every slot number, so the bit
it adds is never in an AND. P5 holds since one number put in its best
slot and the rest anywhere is a placement, and no number gives more
than in its best slot.

The differential prints `360 cases: checksum 740113623, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading of the same
cases. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Thirty-four edits to the differential, five to nine to each arm, each
run under `karac __mir-llvm-run` and `karac __mir-run`. Seventeen are
kept, three to each Kāra arm and two to the Rust-template arm. Each kept
one is killed, fails the same way under both backends and not by a
crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M2 | ★: slots numbered from 0 | P1 240, P5 115, P6 240 |
| M3 | ★: the answer the last full fill's best | P1 78, P3 81, P5 26, P6 78 |
| M5 | ★: the numbers placed counted by the digits not 0 | P1 219, P2 53, P5 216, P6 219 |
| M6 | pairs: a place's slot its own index | P1 254, P5 238, P6 254 |
| M8 | pairs: a full mask with its first place empty skipped | P1 53, P5 30, P6 53 |
| M10 | pairs: the answer from the mask of every place only | P1 240, P3 80, P5 240, P6 240 |
| M12 | memo: the memo keyed by the numbers placed | P1 90, P2 72, P5 53, P6 90 |
| M13 | memo: the next number's AND left out | P1 320, P5 320, P6 320 |
| M14 | memo: a slot full at one | P1 171, P2 103, P5 21, P6 171 |
| M20 | struct: the numbers placed counted over all slots but the last | P1 278, P3 27, P5 268, P6 278 |
| M30 | struct: a fill's best overwritten, not raised | P1 114, P2 119, P5 7, P6 114 |
| M32 | struct: the answer the first full fill's | P1 133, P5 49, P6 133 |
| M23 | iter: the least of the ways into a fill | P1 156, P5 39, P6 156 |
| M33 | iter: the AND an OR | P1 352, P4 360, P5 352, P6 352 |
| M34 | iter: the answer from the fills of one number fewer | P1 249, P2 179, P5 103, P6 249 |
| M28 | solution: the adapter's slots one fewer, but room for every number | P1 94, P5 45, P6 94 |
| M29 | solution: the adapter's numbers capped at 7 | P1 171, P4 123, P5 150, P6 171 |

P1, P5 and P6 kill all seventeen, P2 five, P3 three and P4 two. P5
bounds the sum by the best a number gives alone and by every number in
its own best slot, and each kept edit leaves those bounds somewhere. P2
reverses the numbers, and sees an edit whose answer hangs on which
number comes when: the digits counted wrong (M5), the memo keyed by the
count (M12), a slot full at one (M14), the best overwritten by the
latest way in (M30), and the fills short a number (M34). P3 adds a slot,
and sees an edit that reads the answer from one fill: the last (M3), the
mask of every place (M10), or the fills that miss the last slot (M20).
P4 adds 16 to every number, and sees only an edit that reads the high
bits: the OR (M33) and the cap at 7 (M29).

Of the thirty-four, seventeen were not kept. Six are equivalent. Three
place the numbers in another order, which a placement does not see: the
pairs arm taking the first number for the last (M7), the memo arm
taking the one after (M15), and the iter arm placing the first number
last (M25). The memo never read (M11) is the same recursion, slower.
And the iter arm's and the template's answer taken over the fills of
fewer numbers too (M24, M27) adds sums that are never more, since a
number gives at least 0 wherever it goes. Five crash: four of the
struct arm's (room while a digit is under 3, the digit without its
modulo, the size twice the last power, and the next fill a slot up)
index past the fills, and the iter arm's slots holding two only (M22)
unwraps an empty `max`. One fails as a kept one does: the iter arm's
slot given its place, as M2. Five were left out to keep three to an
arm: the ★ arm's slot that holds one number (M1) and its best kept when
first reached (M4), the pairs arm's one place a slot (M9), the struct
arm's slot k worth 2k + 1 (M31), and the template's slot one more
(M26).

## Verification

Every arm prints the same output as `and_sum.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the ★, memo and struct arms take 1.1 s to 2.4
s, and the pairs, iter and template arms 9.4 s, 11 s and 13 s: the two
mask arms walk 2^18 masks of eighteen places for each case of nine
slots, and the iter arm builds a chain of adapters for every fill. The
differential takes 2.5 s.

## Benchmarks

The bench builds one row of 100000 numbers from 1 to 15 once; then
solves 200 windows of 18 numbers in 9 slots, the constraints' largest,
each at a random start, so that no solve repeats one before, with the ★
arm in all five languages. C works over a pointer and a length, the
others over a slice. Every implementation prints `200 solves: checksum
394785803`.

BENCHTAB
