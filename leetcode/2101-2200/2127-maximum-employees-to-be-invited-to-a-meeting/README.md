# 2127. Maximum Employees to Be Invited to a Meeting

A company is organizing a meeting and has a list of `n` employees,
waiting to be invited. They have arranged for a large circular table,
capable of seating any number of employees.

The employees are numbered from `0` to `n - 1`. Each employee has a
favorite person and they will attend the meeting only if they can sit
next to their favorite person at the table. The favorite person of an
employee is not themself.

Given a 0-indexed integer array `favorite`, where `favorite[i]` denotes
the favorite person of the `i`th employee, return the maximum number of
employees that can be invited to the meeting.

```
favorite = [2, 2, 1, 2]     ->  3
favorite = [1, 2, 0]        ->  3
favorite = [3, 0, 1, 4, 1]  ->  4
```

**Constraints:** `n == favorite.length`; `2 <= n <= 10^5`; `0 <=
favorite[i] <= n - 1`; `favorite[i] != i`.

Each employee points at one favorite, so the favorites split the
employees into groups that each end in one cycle. A cycle of three or
more fills its seats on both sides of everyone in it, so it can only sit
alone, all of it and nothing else. Two employees who favor each other
have a free side each, so a pair sits with the longest chain of fans
leading into each of them, and every such pair with its chains can share
the table at once. The answer is the larger of the longest cycle and the
sum over the pairs. O(n).

## Approaches

| file | mechanism |
|---|---|
| `invitations.kara` ★ | the people no one favors peeled off first in Kahn's order over a `VecDeque`, carrying the longest chain into each person; what is left are the cycles, walked once |
| `invitations_stamps.kara` | each walk along the favorites stamps the people it passes with where it started and how far it had come, and meeting its own stamp closes a cycle; each pair's tails found by levels, breadth first, over `Vec[Vec[i64]]` lists of fans |
| `invitations_struct.kara` | a `struct Office` holding the favorites and the fans, with a recursive `tail` (`ref self`) skipping the partner, and `cycle_from`, which keeps the path in a `Vec` and finds where it repeats with `position` |
| `invitations_walk.kara` | every person walked forward on an explicit stack until someone already settled; a walk that runs into itself settles a cycle, and the stack is unwound, each person taking the cycle member its chain reaches and how far it is |
| `invitations_colors.kara` | a walk that keeps a `Map` from each person on it to their place; the tails into each pair by a depth-first search with an explicit stack of `(person, depth)` |
| `invitations_solution.kara` | LeetCode's Rust template: Kahn's order over a `VecDeque<usize>` and a `Vec<i32>` of depths, carried by `karac fix` in five rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's three examples and three
more (one pair, two pairs each with a tail, a triangle beside a pair),
each with its answer; then the employees invited and a checksum over
3000 random tables of 2 to 12; then the constraints' largest, 100000 in
one ring, a pair with a tail of 99998, and 100000 random favorites.
`invitations.py` mirrors the ★ arm and its output is byte-identical.

The struct arm finds a tail by recursion, 99998 calls deep at the
constraints' largest. That fits the main thread's stack, but the loop
over the pairs is a sum that auto-par accepts, and a pool worker's stack
is 8 MiB: under `karac __mir-llvm-asan`, whose frames are larger, the
arm dies of a stack overflow on a worker, and with `KARAC_AUTO_PAR=0` it
passes. A default build shows the same past the constraints, a pair at
the end of 1000000 people, as a bare segmentation fault in 6 runs of 8.
That is filed as karac B-2026-11-14-7; the arm keeps its recursion.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every set of employees is tried, and every way to seat that
set around the table with the first seat fixed, by backtracking; a
seating works when each one sits next to their favorite. No cycle or
pair is assumed. It checks 300 random tables of 2 to 7 employees; then
30 whose favorites are mostly mutual pairs, with the rest favoring
someone before them; then 30 of 2 to 10, a ring with a chain into it,
which runs down the numbers into the ring's last person or, every other
time, up them into person 0. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the employees numbered backwards: the same answer |
| P3 | one more employee, favoring someone already there: the answer or one more |
| P4 | a ring of three more employees, apart: the larger of the answer and 3 |
| P5 | a mutual pair more, apart: the answer, or one or two more |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 tables: checksum 322187606, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading of the same
tables by the same search. On a failure it prints the first ten and then
the count by property.

## Mutation testing

Thirty-seven edits to the differential, five to eight to each arm, each
run under `karac __mir-llvm-run` and `karac __mir-run`. Seventeen are
kept, three to each Kāra arm and two to the Rust-template arm. Each kept
one is killed, fails the same way under both backends and not by a
crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M5 | ★: one side's tail counted | P1 143, P2 144, P6 143 |
| M6 | ★: the cycles and pairs added | P1 5, P4 227, P6 5 |
| M32 | ★: the queue started from everyone | P1 314, P2 101, P3 166, P5 349, P6 314 |
| M7 | stamps: a cycle one too long | P1 192, P4 118, P6 192 |
| M8 | stamps: a walk ending on another's stamp counted as a cycle | P1 2, P2 2, P6 2 |
| M11 | stamps: each pair counted from both ends | P1 232, P3 113, P5 232, P6 232 |
| M13 | struct: a fan's own fans not followed | P1 73, P6 73 |
| M14 | struct: the path's last person taken as the cycle's start | P1 132, P4 190, P6 132 |
| M16 | struct: a pair's tails taken as the longer only | P1 37, P6 37 |
| M17 | walk: a pair counted once | P1 232, P5 232, P6 232 |
| M18 | walk: the distance never grown | P1 163, P6 163 |
| M21 | walk: every cycle taken as a pair | P1 108, P4 360, P6 108 |
| M23 | colors: the cycle measured from the walk's start | P1 29, P2 67, P6 29 |
| M26 | colors: only one side's tail | P1 91, P2 143, P6 91 |
| M35 | colors: the deepest taken as the last reached | P1 15, P2 24, P6 15 |
| M33 | solution: a ring of three taken as a pair | P1 59, P2 50, P4 312, P6 59 |
| M34 | solution: the adapter handing over each favorite's favorite | P1 254, P6 254 |

P1 and P6 kill all seventeen, P2 seven, P4 five, P5 three and P3 two.
P2 numbers the employees backwards, so it sees the edits whose answer
depends on the order people are reached in: which side of a pair is
counted (M5, M26), which walk runs first (M8, M23), which fan a
depth-first search pops last (M35), which member of a ring of three is
taken for the pair (M33). P4 adds a ring of three apart, which only an
edit that miscounts a cycle notices: a cycle too long or measured from
the wrong place (M7, M14), a cycle added to the pairs (M6) or taken as
one (M21, M33). P5 adds a pair apart, which must add exactly two: it
sees a pair counted once or twice (M11, M17) and the queue that starts
everyone off and counts each pair's people as their own tails (M32).
P3, one more employee, sees only those last two, M11 and M32.

Two edits survived the first draw of the differential: the stamps arm
closing a cycle on another walk's stamp (M8) and the struct arm
counting the whole path of a walk that runs into a known cycle (M15).
Both overcount only when a walk longer than any cycle runs into the
first person of a cycle stamped before it, which the arms' own 3000
tables catch and the differential's chains, all running down the
numbers into the ring's last person, never were. The third family now
runs its chain up the numbers into person 0 every other time, with up
to 10 employees, and both are killed by P1, P2 and P6 in two tables.

Of the thirty-seven, twenty were not kept. One is equivalent: the colors
arm walking on through people already done, which reaches the same
cycles at the cost of quadratic work. Five cannot be kept: the stamps
arm following the partner into a tail and the struct arm never skipping
it loop forever, by time and by stack; the walk arm leaving the cycle's
last member off and the adapter dropping the last favorite index out of
bounds; and the colors arm following the partner fails differently
under the two backends. None survives. Six fail as a kept one does: the
★ arm's chain and the Rust arm's depth never grown as M18, the stamps
arm's tail one too deep and the colors arm's as M17, the struct arm's
walk into a known cycle as M8, and the walk arm's chain reaching its
own favorite as M13. Eight are killed with checks of their own but were
left out because their arms keep their share: the ★ arm summing the
chains (P1 51) or keeping only the largest pair (P1 28); a pair taken
as a cycle in the ★ and Rust arms and a pair's two seats counted as
one in the colors arm (P1 168); the Rust arm's depth starting at 0 and
its answer the larger of the two only (P1 227); and the colors arm's
cycle one short (P1 132, P4 142).

## Verification

Every arm prints the same output as `invitations.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and every
arm but the struct arm under `karac __mir-llvm-asan` (AddressSanitizer
and LeakSanitizer) with no error; the struct arm's stack overflow there
is the one above. `karac run` and a `karac build` binary print the same
output for every arm and the differential. `karac check --output=json`
reports nothing on any of them, and `karac fix --dry-run` has nothing to
apply.

Under `karac __mir-run` the arms take 0.9 s to 2.0 s, most of it the
three tables of 100000, and the differential 6.9 s, nearly all of it the
literal search over the tables of up to 10.

`karac fix` carries the template in five rounds of 14, 9, 5, 1 and 1
edits: Rust's spellings (the `use` dropped, `<..>` to `[..]`, `for &f in
&favorite` to `for f in ref favorite`, `|&i|` to `|i|`, `struct
Solution;` to `struct Solution {}`, the adapter's `&Vec` to `ref Vec`,
`Solution::` to `Solution.`); then `vec![x; n]` to `Vec.filled(n, x)`,
`usize` to `i64`, `max_cycle` annotated `i32`, and the adapter's `as
i64` dropped, since an `i32` widens on return; then the `as i64` on
each index dropped, since an `i32` indexes, and `two_cycles` and `len`
annotated `i32`; then the depths' `1` written `1i32`; then the `ref`
dropped from the adapter's parameter, which borrows already. The `let v
= favorite[u] as i64;` stays: with no type written, the cast is what
makes `v` an `i64` for the queue of `i64`.

## Benchmarks

The bench builds 20 tables of 100000 employees once, the first quarter
in mutual pairs and the rest favoring someone at random, then solves
every table 10 times, one random favorite in the rest changed before
each solve so that no solve repeats one before, with the ★ arm in all
five languages. Every implementation prints `200 solves: 13110765
invited, checksum 758302946`.

BENCHTAB
