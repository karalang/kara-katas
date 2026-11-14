# 2149. Rearrange Array Elements by Sign

You are given a **0-indexed** integer array `nums` of **even** length
consisting of an **equal** number of positive and negative integers.

You should return the array of `nums` such that the array follows the
given conditions:

1. Every **consecutive pair** of integers have **opposite signs**.
2. For all integers with the same sign, the **order** in which they were
   present in `nums` is **preserved**.
3. The rearranged array begins with a positive integer.

Return *the modified array after rearranging the elements to satisfy the
aforementioned conditions*.

```
nums = [3,1,-2,-5,2,-4]  ->  [3,-2,1,-5,2,-4]
nums = [-1,1]            ->  [1,-1]
```

**Constraints:** `2 <= nums.length <= 2 * 10^5`; `nums.length` is
even; `1 <= |nums[i]| <= 10^5`; `nums` consists of an equal number of
positive and negative integers.

The answer begins with a positive and the signs alternate, so the
positives sit at the even places and the negatives at the odd ones, each
in the order the list has them: the k-th positive, counting from 0, goes
to place 2k and the k-th negative to place 2k + 1. O(n).

## Approaches

| file | mechanism |
|---|---|
| `signs.kara` ★ | one walk with two cursors, one per sign, each stepping by two through a `Vec.filled` answer |
| `signs_split.kara` | the list split by sign with `partition`, then woven back by `zip` and `flat_map`, a positive then a negative |
| `signs_queues.kara` | a `VecDeque` per sign filled by `push_back`, then emptied from the front in turn under `while let` on a pair of `pop_front`s |
| `signs_struct.kara` | a `struct Seater` holding the row and each sign's next place, that `seat`s each number (`mut ref self`) and hands over the row when `seated` (`own self`) |
| `signs_iter.kara` | two `filter` iterators over the list held side by side and drawn from in turn with `next`, so neither half is ever stored |
| `signs_solution.kara` | LeetCode's Rust template: `vec![0; n]`, a tuple of `usize` cursors bound `(mut i, mut j)`, `for &x in &nums`; carried by `karac fix` in three rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 11 lines: LeetCode's two examples and four
more (the negatives first, one pair already in place, every positive
then every negative, and the constraints' extremes), each with its
answer; then a total and a checksum over 2000 random lists of 1 to 10
positives and as many negatives, of 1 to 3 or 1 to 100000 in turn, in a
random order; then the constraints' largest, 200000 numbers: every
positive then every negative, the signs already in turn, and at random,
each with its first two places, its last two and a checksum.
`signs.py` mirrors the ★ arm and its output is byte-identical.

No compiler gap was met. `karac fix` carries the template in three
rounds of 18, 1 and 2 edits: Rust's spellings (`Vec<..>` to `Vec[..]`,
`let (mut i, mut j)` to `let mut (i, j)`, `for &x in &nums` to `for x in
ref nums`, the `|&x|` patterns to bare ones, `struct Solution;` to
`struct Solution {}`, the adapter's `&Vec` to `ref Vec`, `Solution::` to
`.`); then the `0` of `vec![0; n]` written `0i32`, so that the answer is
a `Vec[i32]`; then `vec![0i32; n]` to `Vec.filled(n, 0i32)`, and the
`ref` dropped from the adapter's parameter, which borrows already. The
template's `usize` cursors stay, as Kāra indexes by them too.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: each number's place is found by counting the numbers of its
sign before it, k of them putting a positive at 2k and a negative at
2k + 1; no cursor is kept. It checks 300 random lists of 1 to 5
positives and as many negatives, of 1 to 3 or 1 to 100 in turn, in a
random order; then 30 with every positive first; then 30 with the signs
in turn, a negative first. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | every number negated: each pair of the answer negated and swapped |
| P3 | the answer's even places: the positives, in the list's order |
| P4 | the answer's odd places: the negatives, in the list's order |
| P5 | the answer fed back in: the same answer, and it is a list the statement allows |
| P6 | each arm agrees with at least three of the other five |

P5 asks first that the answer be as long as the list, half of it
positive, so that a wrong answer is never fed back to an arm whose
cursors it would run past the end; it fails rather than crashes.

The differential prints `360 lists: checksum 37860864, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading of the same
lists, split by sign and zipped. On a failure it prints the first ten
and then the count by property.

## Mutation testing

Thirty-five edits to the differential, five to eight to each arm, each
run under `karac __mir-llvm-run` and `karac __mir-run`. Fourteen are
kept: three to the ★ and queue arms and two to each other. Each kept one
is killed, fails the same way under both backends and not by a crash,
and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M2 | ★: a positive moving one place | P1 286, P2 286, P3 286, P4 237, P5 286, P6 286 |
| M4 | ★: the signs swapped | P1 360, P3 360, P4 360, P6 360 |
| M32 | ★: the list walked from its back | P1 276, P3 243, P4 248, P5 276, P6 276 |
| M8 | split: the first negative dropped | P1 360, P2 360, P3 360, P4 360, P5 360, P6 360 |
| M9 | split: each positive woven twice | P1 360, P2 360, P4 360, P5 360, P6 360 |
| M12 | queues: the positives queued at the front | P1 243, P2 276, P3 243, P5 243, P6 243 |
| M14 | queues: every negative queued twice | P1 269, P2 282, P4 269, P5 182, P6 269 |
| M15 | queues: a one queued as a negative | P1 127, P2 161, P3 127, P4 127, P5 127, P6 127 |
| M18 | struct: a negative seated one place back | P1 360, P2 360, P3 239, P4 360, P5 360, P6 360 |
| M19 | struct: the negatives' place never moved | P1 286, P2 286, P4 286, P5 286, P6 286 |
| M24 | iter: the negatives drawn from the back | P1 248, P2 276, P4 248, P5 248, P6 248 |
| M25 | iter: every positive one up | P1 360, P2 360, P3 360, P5 360, P6 360 |
| M28 | solution: the adapter's answer reversed | P1 360, P3 360, P4 360, P5 276, P6 360 |
| M29 | solution: the adapter doubling every number | P1 360, P3 360, P4 360, P5 360, P6 360 |

P1 and P6 kill all fourteen, P5 thirteen, P4 twelve, P2 and P3 ten
each. The answer is a whole list, and nearly any wrong edit spoils it
for nearly every list drawn, so the counts are mostly 360 and the edits
are told apart by which properties they pass. P3 and P4 look at one
sign at a time, so an edit that spoils only the negatives passes P3
(M9, M14, M19, M24) and one that spoils only the positives passes P4
(M12, M25). P2 negates every number, which
turns the signs round: an edit that treats the two signs alike passes
it (M4, M28, M29, M32), and one that treats one sign apart fails it.
P5 feeds the answer back in, which the right answer survives unchanged;
it sees every kept edit but the swapped signs (M4), whose answer, a
negative first, the same edit leaves as it is when fed back.

Of the thirty-five, twenty-one were not kept. Two are equivalent: a
positive found by `x >= 0` in the ★ arm and a negative by `x <= 0` in
the iterator arm, since no number is 0. One fails by a crash: the
template reading a one as a negative, which runs a cursor past the end.
Eighteen fail as a kept one does. Six put each pair negative first, as
M4: the split taking the negatives first and weaving each pair negative
first, the queues pushing each pair negative first, the struct's two
places started swapped, the iterators pushed negative first, and the
template's cursors swapped. Five spoil only the negatives' values, as
M9: the ★ arm writing a negative negated or one up, and the iterators
doubling or negating every negative. Two run the positives' cursor one
place a step, as M2: the struct's and the template's. Two make a list
too short or too long in every check, as M8: the struct's row two places
long and the iterators one pair short. The ★ arm's negatives started at
0, as M18; the split from the list's back, as M32; the queue's negatives
taken from the back, as M24; and the ★ arm's answer one place long, as
M25.

## Verification

Every arm prints the same output as `signs.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 1.2 s to 5.8 s and the
differential 0.6 s.

## Benchmarks

The bench builds 4 lists of 100000 positives and as many negatives, of
1 to 100000, once in a random order; then rearranges every list 25
times, two of its numbers swapped before each so that no answer repeats
one before, and reads three places of each answer, with the ★ arm in all
five languages. Every implementation prints `100 answers: checksum
912083352`.

BENCHTAB
