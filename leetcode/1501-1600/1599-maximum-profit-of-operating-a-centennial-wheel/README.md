# 1599. Maximum Profit of Operating a Centennial Wheel

You are the operator of a Centennial Wheel that has four gondolas, and
each gondola has room for up to four people. You have the ability to
rotate the gondolas counterclockwise, which costs you `runningCost`
dollars.

You are given an array `customers` of length `n` where `customers[i]` is
the number of new customers arriving just before the `i`th rotation
(0-indexed). This means you must rotate the wheel `i` times before the
`customers[i]` customers arrive. You cannot make customers wait if there
is room in the gondola. Each customer pays `boardingCost` dollars when
they board on the gondola closest to the ground and will exit once that
gondola reaches the ground again.

You can stop the wheel at any time, including before serving all
customers. If you decide to stop serving customers, all subsequent
rotations are free in order to get all the customers down safely. Note
that if there are currently more than four customers waiting at the
wheel, only four will board the gondola, and the rest will wait for the
next rotation.

Return the minimum number of rotations you need to perform to maximize
your profit. If there is no scenario where the profit is positive,
return `-1`.

```
customers = [8,3],        boardingCost = 5, runningCost = 6   ->  3
customers = [10,9,6],     boardingCost = 6, runningCost = 4   ->  7
customers = [3,4,0,5,1],  boardingCost = 1, runningCost = 92  ->  -1
```

**Constraints:** `n == customers.length`; `1 <= n <= 10^5`;
`0 <= customers[i] <= 50`; `1 <= boardingCost, runningCost <= 100`.

## Approaches

| file | mechanism |
|---|---|
| `wheel.kara` ★ | the wheel run rotation by rotation: the next group joins the queue, up to four board, the profit moves by their fares less the running cost, and the first rotation at a new highest profit is kept. O(n + total / 4) |
| `wheel_tail.kara` | the tail in closed form: rotations while groups arrive run as the ★ arm runs them; after that every rotation but the last boards four, so each changes the profit by the same amount and only the last of them can be a new best, and the last rotation is weighed on its own. O(n) |
| `wheel_profits.kara` | every profit, then the best: the profit after each rotation collected by `scan` over the rotation numbers with (queue, profit) as its state, and the first index of the largest found by `enumerate` and `fold`. O(n + total / 4) |
| `wheel_solution.kara` | LeetCode's Rust template (an index over the arrivals, a `loop` that breaks when no one is left, a tuple `let (mut wait, mut profit, ..)`), carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 10 lines: LeetCode's three examples and four
more (no one comes; four come and pay exactly the running cost; fifty a
rotation at a high fare; a late group that never pays its way), then the
count never in profit and a checksum for 3000 random days of up to 6
arrivals, 300 of up to 100 and 3 of up to 100000, groups of 0 to 50 and
costs from 1 to 100. `wheel.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: for each number of rotations `k` the wheel could be stopped
after, the day run from the start for exactly `k` rotations, its profit
the fares less `k` running costs; the fewest rotations of the highest
profit, or `-1` when none makes one. It checks 3000 days of 1 to 5
arrivals of 0 to 10 customers, costs from 1 to 12, every random choice
drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | both costs doubled leave the answer |
| P3 | a last arrival of no one leaves the answer |
| P4 | a higher boarding cost never turns a profit into `-1` |
| P5 | a running cost of four boardings or more answers `-1` |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 162380095, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends.

The tail arm was first written wrong and the differential caught it: it
took the profit after the full rotations as the best without comparing,
and added their cost only when they paid.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a tie with the best profit taken as a new best | P1 162, P5 620, P6 162 |
| M2 | ★: three board a rotation, not four | P1 1927, P6 1927 |
| M3 | ★: the wheel stops when the arrivals do | P1 1859, P3 1859, P6 1859 |
| M4 | tail: a tie at the last rotation taken as a new best | P1 91, P3 26, P6 91 |
| M5 | tail: the full rotations' profit left out | P1 684, P3 684, P6 684 |
| M6 | tail: a full rotation costs nothing to run | P1 78, P3 51, P5 1389, P6 78 |
| M7 | profits: the last index of the largest profit | P1 108, P6 108 |
| M8 | profits: a best of zero taken as a profit | P1 54, P5 620, P6 54 |
| M9 | template: the loop stops when the arrivals do | P1 1859, P3 1859, P6 1859 |
| M10 | template: the rotation counted one short | P1 2539, P6 2539 |

## Benchmarks

The bench runs the ★ arm on 300 days of 100000 arrivals, all drawn
first, in all five languages. Every implementation prints `300 days of
100000 arrivals: checksum 120410238`. The C mirror runs the wheel
rotation by rotation in `int64_t`.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `5dc4418bbd` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.171 s |
| Rust (`rustc -O`) | 0.181 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.187 s |
| Kāra (`karac build`) | 0.188 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.191 s |
| Go | 0.336 s |
| Python | 10.4 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here:
its user time is below its real time (0.135 s and 0.188 s on one run).

## Verification

All four arms print the same output as `wheel.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them, the differential and the bench. `karac check` reports nothing on
any of them, and `karac fix` has nothing left to change. Checked at kara
`5dc4418bbd`.

## Writing it

The ★ and tail arms were written in Kāra and checked as written, but for
one line of the shared harness: it wrote `*boarding` and `*running` for
the numbers of a tuple met in `for (..) in examples.iter()`, and `karac
fix` dropped the `*`s, as an `i32` is copied. The profits arm wrote its
`scan` as Rust's, writing the state through `*state`; `karac fix` made
it Kāra's, binding `let state = ..` and returning `Some((state, item))`.

The Rust template took one `karac fix`, of 12 edits: `struct Solution;`
to `struct Solution {}`, `Vec<i32>` to `Vec[i32]`,
`let (mut wait, mut profit, mut best, mut ans)` to
`let mut (wait, profit, best, ans)`, `&&` to `and`, and `Solution::` to
`Solution.`. It then checks and agrees with no hand edit.
