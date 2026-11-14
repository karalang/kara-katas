# 2141. Maximum Running Time of N Computers

You have `n` computers. You are given the integer `n` and a
**0-indexed** integer array `batteries` where the `i`th battery can
**run** a computer for `batteries[i]` minutes. You are interested in
running **all** `n` computers **simultaneously** using the given
batteries.

Initially, you can insert **at most one battery** into each computer.
After that and at any integer time moment, you can remove a battery from
a computer and insert another battery **any number of times**. The
inserted battery can be a totally new battery or a battery from another
computer. You may assume that the removing and inserting processes take
no time.

Note that the batteries cannot be recharged.

Return *the **maximum** number of minutes you can run all the* `n`
*computers simultaneously.*

```
n = 2, batteries = [3,3,3]      ->  4
n = 2, batteries = [1,1,1,1]    ->  2
```

**Constraints:** `1 <= n <= batteries.length <= 10^5`;
`1 <= batteries[i] <= 10^9`.

Swaps are free, so n computers can run for T minutes exactly when the
batteries hold n T minutes counting each at most T, since no battery can
run two computers at once. That test is monotone in T, so the longest T
is found by halving. O(len log(sum / n)).

## Approaches

| file | mechanism |
|---|---|
| `running.kara` ★ | the longest T found by halving from 0 to the whole charge over n, each test a `map` of `min(mid)` and a `sum` |
| `running_greedy.kara` | sorted largest first by `sort_by`; a battery holding more than the average share of the computers left is set aside with its computer, and the rest share evenly |
| `running_heap.kara` | the same set aside off a `PriorityQueue.max_first_from`, its largest read by `peek().cloned()` and popped |
| `running_struct.kara` | a `struct Fleet` asked whether it `lasts` a number of minutes (`ref self`, returning early once the charge is enough), and its `longest` run halved between a run it lasts and one it fails |
| `running_bound.kara` | no halving and no setting aside: any k smallest batteries must carry the n - (len - k) computers the rest cannot, so each k gives an upper bound, and the least of them is the answer, a `fold` over the prefix sums |
| `running_solution.kara` | LeetCode's Rust template: the halving over minutes with `sum::<i64>()`, `\|&b\|` patterns and `(b as i64).min(mid)`; carried by `karac fix` in two rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's two examples and four more
(one computer, a computer for every battery, one battery too large to
share, and the most charge one computer can use), each with its answer;
then the total and a checksum over 2000 random fleets of 1 to 12
batteries of 1 to 10 or 1 to 10^9 in turn, for 1 computer up to one for
every battery; then the constraints' largest, 100000 batteries of up to
10^9: every one full for 100000 computers, at random for one computer,
and at random for 50000. `running.py` mirrors the ★ arm and its output
is byte-identical.

No compiler gap was met. `karac fix` carries the template in two rounds
of 13 and 1 edits: Rust's spellings (`Vec<..>` to `Vec[..]`,
`sum::<i64>()` to `sum()`, the `|&b|` and `|&v|` patterns to `|b|` and
`|v|`, `struct Solution;` to `struct Solution {}`, the adapter's `&Vec`
to `ref Vec`, `Solution::` to `.`); then the `ref` dropped from the
adapter's parameter, which borrows already. The `as i64` and `as i32`
casts stay, since the template's batteries are `i32`.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: minute by minute, every choice of n batteries with charge
left to run the n computers is tried, each losing a minute of charge,
and the longest run over all the choices is the answer, the charges
left remembered in a `Map` once sorted; no bound is assumed and no
halving is done. It checks 300 random fleets of 1 to 6 batteries of 1
to 4 minutes, for 1 computer up to one for every battery; then 30 with
one battery of up to 12; then 30 with a computer for every battery. All
360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the minutes are the statement read literally |
| P2 | the batteries in reverse order: the same minutes |
| P3 | every battery listed twice, for twice the computers: the same minutes |
| P4 | one computer: every minute of charge |
| P5 | a battery holding the whole charge added, for one more computer: the same minutes |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 fleets: checksum 310299914, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading of the same
fleets by the same search. On a failure it prints the first ten and
then the count by property.

## Mutation testing

Thirty-four edits to the differential, five to eight to each arm, each
run under `karac __mir-llvm-run` and `karac __mir-run`. Seventeen are
kept, three to each Kāra arm and two to the Rust-template arm. Each kept
one is killed, fails the same way under both backends and not by a
crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the halving's top one short | P1 272, P4 360, P5 130, P6 272 |
| M4 | ★: a strict test | P1 295, P4 360, P6 295 |
| M5 | ★: a battery counted at most one minute less | P1 237, P4 57, P5 104, P6 237 |
| M6 | greedy: the batteries sorted smallest first | P1 88, P5 214, P6 88 |
| M8 | greedy: the computer kept with its battery set aside | P1 136, P5 99, P6 136 |
| M9 | greedy: the charge kept with its battery set aside | P1 136, P3 48, P5 191, P6 136 |
| M12 | heap: the test against the computers less one | P1 57, P3 39, P5 74, P6 57 |
| M15 | heap: the test turned | P1 238, P4 308, P5 296, P6 238 |
| M30 | heap: the answer over every computer | P1 136, P5 122, P6 136 |
| M19 | struct: the computers counted one fewer | P1 86, P3 21, P5 186, P6 86 |
| M33 | struct: the fleet built for one more computer | P1 353, P3 139, P4 360, P6 353 |
| M34 | struct: the test asking a minute more | P1 360, P4 360, P5 117, P6 360 |
| M21 | bound: the batteries unsorted | P1 58, P2 60, P3 2, P6 58 |
| M23 | bound: the computers counted from the wrong end | P1 215, P3 260, P5 130, P6 215 |
| M24 | bound: the largest bound kept | P1 165, P3 194, P5 158, P6 165 |
| M27 | solution: the adapter dropping the first battery | P1 333, P2 117, P3 107, P4 360, P6 333 |
| M28 | solution: the template's n taken as one | P1 226, P3 360, P5 360, P6 226 |

P1 and P6 kill all seventeen, P5 thirteen, P3 nine, P4 seven and P2
two. P5 adds a battery as large as the whole charge, which can never be
shared and must be set aside with the computer added for it; it sees
nearly every edit to how a large battery is set aside or counted (M6,
M8, M9, M12, M15, M30), to the halving's top or its test (M1, M5, M19,
M34), and to the bounds (M23, M24), and the template's n taken as one
(M28). P3 lists the fleet twice for twice the computers, which keeps
every share; it sees an edit that ties the answer to the number of
computers rather than the share of each (M9, M12, M19, M33, M23, M28),
the bound arm's order (M21) and largest bound (M24), and the adapter's
lost battery (M27), which the doubling halves. P4 asks for one
computer, which runs on the whole charge; it sees an edit that loses
the top of the range (M1, M4, M5, M34), a test that runs the wrong way
(M15), a computer too many (M33), and the lost battery (M27). P2
reverses the batteries, which every right answer ignores; it sees the
bound arm left unsorted (M21) and the adapter's lost first battery
(M27), the only two edits that read the batteries in their order.

Of the thirty-four, seventeen were not kept. Four are equivalent: the ★
arm's midpoint written as the lower half plus the odd one, which is the
same number; the greedy's stop dropped, since once a battery shares,
every smaller one does too; the bound arm's prefix index capped at the
length, which it never passes; and the template's midpoint taken from
below and moved up when it meets the bottom, which picks the same
minutes in the end. Three fail by a crash: the greedy setting aside a
battery equal to the share, which can leave no computer and divides by
zero, and two that never finish, the heap's largest never popped and
the struct's failing end moved past the midpoint. Eight fail as a kept
one does: each battery counted whole by the ★ arm and by the struct,
and the heap smallest first, as M6; the heap's computer kept, as M8;
the heap's charge kept, as M9; the struct's failing end at the total
share, as M1; the struct's check made at the end only, as M4; and the
struct's battery counted one minute less, as M5. Two are killed with
checks of their own but were left out because their arms keep their
share: the heap's test given a computer's slack (P1 64, P5 4, P6 64)
and the struct's lasting end started at half the share (P5 29), which
only the battery added by P5 lifts past the answer.

## Verification

Every arm prints the same output as `running.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.7 s to 10.3 s and the
differential 0.6 s.

## Benchmarks

The bench builds 10 fleets of 100000 batteries once, charges of 1 to
10^9, for 10000 up to 100000 computers; then solves every fleet 20
times, one battery redrawn before each solve so that no solve repeats
one before, with the ★ arm in all five languages. Every implementation
prints `200 solves: 246525627886 minutes in all, checksum 415742643`.

BENCHTAB
