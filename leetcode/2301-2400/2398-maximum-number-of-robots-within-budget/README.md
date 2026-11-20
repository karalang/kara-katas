# 2398. Maximum Number of Robots Within Budget

You have `n` robots. You are given two **0-indexed** integer arrays,
`chargeTimes` and `runningCosts`, both of length `n`. The `i`th robot
costs `chargeTimes[i]` units to charge and costs `runningCosts[i]`
units to run. You are also given an integer `budget`.

The **total cost** of running `k` chosen robots is equal to `max(chargeTimes)
+ k * sum(runningCosts)`, where `max(chargeTimes)` is the largest
charge cost among the `k` robots and `sum(runningCosts)` is the sum of
running costs among the `k` robots.

Return *the **maximum** number of **consecutive** robots you can run
such that the total cost **does not** exceed* `budget`.

```
chargeTimes = [3,6,1,3,4], runningCosts = [2,1,3,4,5], budget = 25  ->  3
chargeTimes = [11,12,19], runningCosts = [10,8,7], budget = 19       ->  0
```

**Constraints:** `chargeTimes.length == runningCosts.length == n`; `1
<= n <= 5 * 10^4`; `1 <= chargeTimes[i], runningCosts[i] <= 10^5`; `1
<= budget <= 10^15`.

A run's cost only grows when the run grows, so the longest run that
fits can be found with a window whose left end only moves forward.

## Approaches

| file | mechanism |
|---|---|
| `robots.kara` ★ | a sliding window, its largest charge time the front of a monotonic `VecDeque` of indexes. O(n) |
| `robots_binary.kara` | binary search on the count, each count checked by sliding a window of exactly that size, with a monotonic deque and prefix sums. O(n log n) |
| `robots_sparse.kara` | two pointers over a sparse table, each window's largest charge time from two overlapping runs of `2^j` robots. O(n log n) |
| `robots_heap.kara` | two pointers with a `PriorityQueue.max_first()` of (charge time, index), the tops that have left the window popped and thrown away. O(n log n) |
| `robots_iter.kara` | iterators: a binary search on the count, each count checked by `any` over its windows; prefix sums by `scan`, and a sparse table whose levels are built by `map` and `collect` |
| `robots_solution.kara` | LeetCode's Rust template: the sliding window with a `VecDeque<usize>`, its state a tuple `(0usize, 0i64, 0usize)`, the front read as `*q.front().unwrap()`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 5 lines: LeetCode's two examples; a budget
that just fits one robot, one short of it, and one for every robot;
then `5 * 10^4` robots with charge times and running costs up to
`10^5`, for each budget from `10^5` to `10^15`; then 3000 random fleets
of 1 to 30 robots, with a checksum and the total. `robots.py` mirrors
the ★ arm and its output is byte-identical, and the mirror was checked
on 20000 random fleets of up to 9 robots against every run.

`robots_iter.kara` was first written with a closure declaring `-> i64`
and `[0].iter().chain(..)` of an array's references with a `scan`'s
values; `karac fix` removed the return type and put `.cloned()` before
`chain`, in one call of 2 edits.

`check` first reports 11 errors on the template, and `karac fix`
carries it in one call, reporting 24 edits: `struct Solution;` given
its braces; `use std::collections::VecDeque;` deleted; `Vec<..>` and
`VecDeque<..>` their brackets; `VecDeque::new` written with a dot; the
`mut` of each name in `let (mut l, mut sum, mut ans)` moved before the
pattern, `let mut (l, sum, ans)`; `Some(&b) = q.back()` written `Some(b)
= q.back().cloned()`; `&&` written `and`; and `usize` made `i64`, after
which `0usize`, `0i64` and every widening `as i64` were needless and
removed. `*q.front().unwrap()`, `while let` and `ans as i32` stand as
Kāra.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every run of consecutive robots, its largest charge time and
its running costs summed afresh, and the longest whose cost is within
the budget kept. No window carried between runs. It checks 300 random
fleets of 1 to 12 robots, which the literal reading answers; then 30 of
up to 500 robots with costs up to `10^5`; then 30 of up to 500 robots
with costs up to 3. Each budget is drawn to cut somewhere inside the
fleet, and all 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | up to 12 robots, the answer is the literal reading's |
| P2 | some run of the answer's length fits the budget, and no run one longer does |
| P3 | the robots in reverse order: the same answer |
| P4 | the budget doubled: the answer or more |
| P5 | every charge time, running cost and the budget doubled: the same answer |
| P6 | each arm agrees with at least three of the other five |

P2 checks each answer against every run of its length and the next,
worked out in the harness. P3 holds because the runs reversed are the
same runs, P4 because a run that fits a budget fits a larger one, and
P5 because doubling every cost doubles every run's total.

The differential prints `360 cases: checksum 67247577, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and costs every run. On a failure it prints the first
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
| M1 | ★: the deque kept rising | P1 15, P2 16, P3 1, P6 16 |
| M3 | ★: the window counted one short | P1 103, P2 123, P6 123 |
| M5 | ★: the best one short | P1 272, P2 331, P6 331 |
| M8 | binary: a failed count lowering the bound by two | P1 73, P2 88, P6 88 |
| M10 | binary: the running costs not multiplied | P1 190, P2 248, P6 248 |
| M11 | binary: never every robot | P1 40, P2 41, P6 41 |
| M12 | sparse: each level its left half only | P1 8, P2 8, P3 7, P6 8 |
| M13 | sparse: the window's largest from its left run | P1 1, P2 1, P3 1, P6 1 |
| M16 | sparse: the last window kept | P1 79, P2 132, P3 141, P6 132 |
| M18 | heap: the running cost queued for the charge time | P1 28, P2 29, P6 29 |
| M20 | heap: the robots added to the running costs | P1 176, P2 234, P5 45, P6 234 |
| M21 | heap: the charge times summed for the running costs | P1 131, P2 186, P3 143, P6 186 |
| M22 | iter: a cost over the budget taken as fitting | P1 300, P2 359, P4 80, P6 359 |
| M23 | iter: each window's largest from single robots | P1 1, P2 2, P6 2 |
| M24 | iter: each window's first cost left out | P1 127, P2 147, P3 37, P6 147 |
| M29 | solution: the budget one larger | P1 11, P2 11, P5 11, P6 11 |
| M31 | solution: each robot queued at the front | P1 7, P2 8, P3 6, P6 8 |

P1, P2 and P6 kill all seventeen, P3 seven, P5 two and P4 one. P2 pins
the answer exactly, a run of its length that fits and none one longer,
so it fails every wrong answer. P3, the robots reversed, fails seven of
them (M1, M12, M13, M16, M21, M24, M31). P5, every cost and the budget
doubled, fails the two edits that do not scale with them: the robots
added to the running costs rather than multiplying them (M20), and the
budget one larger (M29). P4, the budget doubled, fails only the edit
that turns the comparison around (M22), so that a larger budget fits
fewer windows.

Of the thirty-one, fourteen were not kept. A robot's running cost never
taken off in the ★, sparse and template arms (M2, M15, M27) fails
alike, and apart from every kept one; so does a cost equal to the
budget refused in the ★, binary and iter arms (M6, M9, M26), and the
binary arm's window one robot wider with the heap arm's robot one
behind the window kept (M7, M17). The sparse arm's running costs not
multiplied (M14) fails as the binary arm's (M10); the heap arm's
smallest charge time on top and the template's deque popped while
larger (M19, M28) as the ★ arm's deque kept rising (M1); and the
template's answer one short (M30) as the ★ arm's best one short (M5).
The iter arm's last window never tried (M25) fails apart from every
kept one and was left out to keep three to an arm. The ★ arm's charge
time kept after it leaves (M4) indexed past the deque and stopped with
a runtime error under both backends; a crash is not kept. The iter
arm's M22 was first the scan yielding each cost alone, which does not
type-check: `karac` reports the scan's items a `ref i64` where the
chain needs `i64`, and names `.cloned()`. It never ran, so it was
replaced by the cost over the budget taken as fitting (M22).

## Verification

Every arm prints the same output as `robots.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 3.2 to 9.2 s, except the binary
arm at 34.6 s and the iter arm at 81.5 s. The differential takes 9.8 s there and 0.65 s
under `karac __mir-llvm-run`.

## Benchmarks

The bench builds 20 fleets of `5 * 10^4` robots with charge times and
running costs up to `10^5` once from the harness's generator, then
makes 2 passes, answering every fleet for each budget from `10^5` to
`10^15` and folding each answer plus the pass into the checksum, with
the ★ arm in all five languages. Every implementation prints `2 passes
over 20 fleets of 5 * 10^4 robots, 11 budgets: checksum 999766360`.
Kāra and Rust keep the deque in a `VecDeque`, Python in a `deque`, Go
in a slice cut from the front, and C in one array of indexes allocated
for each call.

BENCHTAB
