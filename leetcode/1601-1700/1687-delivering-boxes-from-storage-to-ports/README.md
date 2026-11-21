# 1687. Delivering Boxes from Storage to Ports

You have the task of delivering some boxes from storage to their ports
using only one ship. However, this ship has a **limit** on the **number
of boxes** and the **total weight** that it can carry.

You are given an array `boxes`, where `boxes[i] = [portsi, weighti]`, and
three integers `portsCount`, `maxBoxes`, and `maxWeight`.

- `portsi` is the port where you need to deliver the `i`th box and
  `weightsi` is the weight of the `i`th box.
- `portsCount` is the number of ports.
- `maxBoxes` and `maxWeight` are the respective box and weight limits of
  the ship.

The boxes need to be delivered **in the order they are given**. The ship
will follow these steps:

- The ship will take some number of boxes from the `boxes` queue, not
  violating the `maxBoxes` and `maxWeight` constraints.
- For each loaded box **in order**, the ship will make a **trip** to the
  port the box needs to be delivered to and deliver it. If the ship is
  already at the correct port, no **trip** is needed, and the box can
  immediately be delivered.
- The ship then makes a return **trip** to storage to take more boxes
  from the queue.

The ship must end at storage after all the boxes have been delivered.

Return *the **minimum** number of **trips** the ship needs to make to
deliver all boxes to their respective ports.*

```
boxes = [[1,1],[2,1],[1,1]], portsCount = 2, maxBoxes = 3, maxWeight = 3                     ->  4
boxes = [[1,2],[3,3],[3,1],[3,1],[2,4]], portsCount = 3, maxBoxes = 3, maxWeight = 6         ->  6
boxes = [[1,4],[1,2],[2,1],[2,1],[3,2],[3,4]], portsCount = 3, maxBoxes = 6, maxWeight = 7   ->  6
```

**Constraints:** `1 <= boxes.length <= 10^5`; `1 <= portsCount, maxBoxes,
maxWeight <= 10^5`; `1 <= portsi <= portsCount`; `1 <= weightsi <=
maxWeight`.

## Approaches

| file | mechanism |
|---|---|
| `boxes.kara` ★ | `trips[i]`, the fewest trips for the first i boxes, is the least `trips[j] - changes[j]` over the starts j of the last trip the caps allow, plus `changes[i - 1] + 2`, where `changes[k]` counts the port changes up to box k. The allowed starts slide forward, so a `VecDeque` keeps them with that cost rising: a new start drops the ones behind it that cost no less, and the front drops the ones the caps no longer allow. O(n) |
| `boxes_window.kara` | the same table, every start of the last trip tried from i - 1 back while the caps hold, the load and the changes counted on the way. O(n * maxBoxes) |
| `boxes_heap.kara` | the same recurrence, the starts in a min-first `PriorityQueue` of `(trips[j] - changes[j], j)`: a start the caps no longer allow never comes back, so one found on top is popped for good. O(n log n) |
| `boxes_solution.kara` | a Rust solution as LeetCode's Rust users write it, `std::collections::VecDeque` of `usize` starts, `vec![0i64; n + 1]` prefix weights, a `bool as i32` port change and `while let Some(&j) = q.front()`, carried to Kāra by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 8 lines: LeetCode's three examples, one box,
and four boxes for one port in one trip; then the trips summed and a
checksum for 3000 random problems of up to 10 boxes, 3 ports and caps up
to 5, 300 of up to 1000 boxes, 10 ports and caps up to 50, and 10 of up
to `10^5` boxes with ports and caps up to `10^5`. `boxes.py` mirrors the
★ arm and its output is byte-identical.

```
4
6
6
2
2
3000 problems of up to 10 boxes, 3 ports, caps up to 5: 29306 trips, checksum 776064145
300 problems of up to 1000 boxes, 10 ports, caps up to 50: 243653 trips, checksum 432102514
10 problems of up to 100000 boxes, 100000 ports, caps up to 100000: 686990 trips, checksum 967475495
```

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every way to cut the boxes, in order, into trips, from all
`2^(n-1)`, the ones that keep both caps played out (the ship sails to a
box's port unless it is there already, and back to storage at the end),
and the fewest trips win. It checks 3000 random problems of 1 to 10
boxes, 1 to 4 ports and caps of 1 to 6, each with a place to split the
boxes at. Every case is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the ports renumbered, p to portsCount + 1 - p, give the same answer |
| P3 | both caps raised by one never give more trips |
| P4 | the boxes split in two never take fewer trips, summed, than the whole |
| P5 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 551382922, 60000 checks
over 4 arms: 0 failures` under every lane in Verification, and a Python
reading of the statement, a search over where each trip ends with each
trip played out, gives the same checksum. On a failure it prints the
first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. P2 fails for no mutant: renumbering
keeps which boxes share a port, and no edit looks at more. M3 and M8 both
lose the weight cap, one by a prefix weight that holds only the last box,
and fail the same checks.

Three first drafts were replaced. A first M1 let a trip hold one box
fewer (`>=` for `>` on the box cap); with `maxBoxes` = 1 the deque runs
empty and `unwrap()` meets `None`, on both backends, before any property
is checked. A first M4 (`>=` for `>` on the weight cap) left a box no
trip at all and added 2 to `i32.MAX`, an overflow Kāra stops. A first
M10 dropped a start from the back only when its trips alone were no
fewer; that drops only starts the right rule drops too, and it passed
every check.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: every box counted a change of port | P1 897, P5 897 |
| M2 | ★: a trip counted 1, not 2 | P1 3000, P5 3000 |
| M3 | ★: the prefix weight holds only the last box | P1 2059, P5 2059 |
| M4 | window: the weight cap counts boxes | P1 1666, P5 1666 |
| M5 | window: the changes counted against the trip's last box | P1 69, P5 69 |
| M6 | window: a trip holds one box too many | P1 318, P5 318 |
| M7 | heap: a start's cost without its changes | P1 1817, P4 1264, P5 1817 |
| M8 | heap: the weight cap ignored | P1 2059, P5 2059 |
| M9 | solution: a trip's cost without its start's changes | P1 1817, P3 63, P4 1263, P5 1817 |
| M10 | solution: the newest start read, not the cheapest | P1 1321, P5 1321 |

## Benchmarks

The bench draws 50 problems of `10^5` boxes, LeetCode's largest, each
with up to 100 ports, a cap of up to 1000 boxes and 1000 to `10^5` in
weight, and boxes of 1 to 1000, all of them first, then answers each 20
times by the ★ arm in all five languages: `VecDeque` in Kāra and Rust,
`collections.deque` in Python, and in C and Go, which have no deque, an
array with a head and a tail, since each start goes in once. Every
implementation prints `50 problems of 100000 boxes, 20 rounds: 100021160
trips, checksum 161561252`. The C build also runs clean under gcc's
AddressSanitizer and UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `21cdf88b69` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.939 s |
| Go | 1.166 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 1.584 s |
| Kāra (`karac build`) | 1.596 s |
| Rust (`rustc -O`) | 1.886 s |
| Rust (`rustc -O -C overflow-checks=on`) | 2.025 s |
| Python | 56 s |

The sequential Kāra build is 16% faster than Rust and 22% faster than
Rust with overflow checks on, the equal-safety comparison
(BENCHMARKS.md). C is the fastest here at 0.939 s.

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here:
its user time is not above its real time (1.429 s and 1.524 s on one
run).

## Verification

All four arms print the same output as `boxes.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `21cdf88b69`.

## Writing it

The heap arm checked clean as first written. The ★ arm filled its
`changes` and `trips` tables with a bare `0`, which keeps the literal's
`i64`, and returned `trips[n]` as the `i32` the signature names; the
refusal (E0200) named the fill literal, and `karac fix` wrote `0i32` in
both. Its `while let Some(back) = starts.back()` pops the deque inside
the loop, and Kāra takes that as written: the start read out is an
`i64`, copied, not a borrow of the deque. The window arm took the same
`0i32`, and its `let mut changes = 0` became `changes: i32`.

LeetCode's Rust solution took one `karac fix` of 23 edits: the
`use std::collections::VecDeque;` line deleted (`VecDeque` is in Kāra's
prelude), `struct Solution {}` added, `Vec<Vec<i32>>` and
`VecDeque<usize>` written `Vec[Vec[i32]]` and `VecDeque[i64]`,
`VecDeque::new` written `VecDeque.new`, each `vec![0i32; n]` written
`Vec.filled(n, 0i32)` and `vec![0i64; n + 1]` `Vec.filled(n + 1, 0)`,
the widening `as i64` and `as usize` casts dropped,
`while let Some(&j) = q.front()` written
`while let Some(j) = q.front().cloned()`, `||` written `or`, and the
harness's `boxes.clone()` passed as `boxes` (`redundant_clone`). The
`bool as i32` port change and `*q.front().unwrap()` carried over as
written.

`arm_name` in the differential indexes a list of string literals for a
`Str`, as #1662's does (B-2026-11-19-131).
