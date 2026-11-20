# 1670. Design Front Middle Back Queue

Design a queue that supports `push` and `pop` operations in the front,
middle, and back.

Implement the `FrontMiddleBackQueue` class:

- `FrontMiddleBackQueue()` Initializes the queue.
- `void pushFront(int val)` Adds `val` to the **front** of the queue.
- `void pushMiddle(int val)` Adds `val` to the **middle** of the queue.
- `void pushBack(int val)` Adds `val` to the **back** of the queue.
- `int popFront()` Removes the **front** element of the queue and returns
  it. If the queue is empty, return `-1`.
- `int popMiddle()` Removes the **middle** element of the queue and
  returns it. If the queue is empty, return `-1`.
- `int popBack()` Removes the **back** element of the queue and returns
  it. If the queue is empty, return `-1`.

**Notice** that when there are **two** middle position choices, the
operation is performed on the **frontmost** middle position choice. For
example:

- Pushing `6` into the middle of `[1, 2, 3, 4, 5]` results in
  `[1, 2, 6, 3, 4, 5]`.
- Popping the middle from `[1, 2, 3, 4, 5, 6]` returns `3` and results in
  `[1, 2, 4, 5, 6]`.

```
["FrontMiddleBackQueue", "pushFront", "pushBack", "pushMiddle", "pushMiddle", "popFront", "popMiddle", "popMiddle", "popBack", "popFront"]
[[], [1], [2], [3], [4], [], [], [], [], []]
->  [null, null, null, null, null, 1, 3, 4, 2, -1]
```

**Constraints:** `1 <= val <= 10^9`; at most `1000` calls will be made to
`pushFront`, `pushMiddle`, `pushBack`, `popFront`, `popMiddle`, and
`popBack`.

## Approaches

| file | mechanism |
|---|---|
| `queue.kara` ★ | two `VecDeque`s, the front half and the back half, the back half as long as the front or one longer, so the middle is always at the seam: a middle push goes on the end of the front half, a middle pop takes the end of the front half when the halves are even, else the start of the back half. At most one value moves across the seam after a call. O(1) per call |
| `queue_vec.kara` | one `Vec`, front first: `insert` and `remove` at index 0, n / 2 for a middle push and (n - 1) / 2 for a middle pop. O(n) at the front and the middle |
| `queue_deque.kara` | one `VecDeque`, the same indices: O(1) at both ends, O(n) at the middle |
| `queue_solution.kara` | a Rust solution as LeetCode's Rust users write it, two `std::collections::VecDeque`s with a `while` loop to rebalance and `unwrap_or(-1)` for an empty pop, carried to Kāra by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, five properties |

The queue is a plain `struct` whose methods take `mut ref self`, the
receiver that writes. Values are `i32`, as in LeetCode's signatures.

Every arm prints the same 6 lines: LeetCode's example; seven pops from
the middle of `[1, 2, 3, 4, 5, 6]` with `7` pushed into its middle, one
pop past empty; seven pops from the back of `[1, 2, 3, 4, 5]` with `7`
pushed into its middle; then the pops on an empty queue and a checksum of
every pop's answer for 3000 random runs of 20 calls, 300 of 1000 and 3
of `10^5`, a push half the time. `queue.py` mirrors the ★ arm and its
output is byte-identical.

```
[1, 3, 4, 2, -1]
[7, 3, 4, 2, 5, 1, 6, -1]
[5, 4, 3, 7, 2, 1, -1]
3000 runs of 20 calls: 9130 pops on an empty queue, checksum 541408478
300 runs of 1000 calls: 7202 pops on an empty queue, checksum 704496612
3 runs of 100000 calls: 929 pops on an empty queue, checksum 352599277
```

## Differential

`differential.kara` holds copies of the four arms, each queue type
renamed and given a `run_<arm>` that replays a run of calls on a new
queue and then empties what is left one of three ways, and the statement
read literally on a `Vec`: a push into the middle lands at the frontmost
middle of the queue it makes, index n / 2 of n + 1, and a pop from the
middle takes the frontmost middle of the queue it finds, index
(n - 1) / 2. It checks 3000 random runs of 1 to 30 calls, a push half the
time. Every case is drawn before any arm answers.

| | property |
|---|---|
| P1 | every pop's answer is the statement read literally |
| P2 | what is left, popped from the front, is the literal queue in order |
| P3 | what is left, popped from the back, is the literal queue reversed |
| P4 | what is left, popped from the middle, is the literal middle order |
| P5 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 574127638, 60000 checks
over 4 arms: 0 failures` under every lane in Verification, and a Python
reading of the statement gives the same checksum. On a failure it prints
the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two to four to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. A first M2 pushed a middle value onto
the start of the back half rather than the end of the front half; that
is the same place in the queue, the seam, and no property can tell them
apart, so it was replaced.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the front half also handed a value when the halves are even | P1 719, P2 988, P3 988, P4 988, P5 988 |
| M2 | ★: a middle push put at the very front | P1 1196, P2 1481, P3 1481, P4 1481, P5 1481 |
| M3 | ★: a middle pop from the wrong half | P1 2155, P2 2155, P3 2155, P4 2759, P5 2155 |
| M4 | ★: no rebalance after a front pop | P1 136, P2 206, P3 206, P4 214, P5 206 |
| M5 | vec: a middle push at (n + 1) / 2 | P1 1422, P2 1718, P3 1718, P4 1718, P5 1718 |
| M6 | vec: a middle pop at n / 2, the backmost middle | P1 1345, P2 1345, P3 1345, P4 2175, P5 1345 |
| M7 | deque: a front push at the back | P1 1803, P2 2000, P3 2000, P4 2000, P5 2000 |
| M8 | deque: a front pop from the back | P1 1677, P2 2233, P3 1677, P4 1677, P5 2233 |
| M9 | solution: the back half let grow two longer | P1 403, P2 570, P3 570, P4 570, P5 570 |
| M10 | solution: a middle pop from the front half's start | P1 623, P2 623, P3 623, P4 1109, P5 623 |

## Benchmarks

The bench draws one run of `10^6` calls, a push three times in five,
values up to `10^9`, and replays it 60 times, each on a new queue, by the
★ arm in all five languages: `VecDeque` in Kāra and Rust,
`collections.deque` in Python, and in C and Go, which have no deque, a
growable ring buffer written for the bench. Every implementation prints
`1000000 calls, 60 rounds: 360 pops on an empty queue, 11992800 values
left, checksum 397814324`. The C build also runs clean under gcc's
AddressSanitizer and UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `9b0b5eb92c` on LLVM 22:

| | median |
|---|---|
| Rust (`rustc -O -C overflow-checks=on`) | 0.592 s |
| Rust (`rustc -O`) | 0.602 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.616 s |
| Kāra (`karac build`) | 0.623 s |
| C (`clang -O3`) | 0.771 s |
| Go | 0.946 s |
| Python | 18 s |

The sequential Kāra build is level with Rust and level with Rust with
overflow checks on, the equal-safety comparison (BENCHMARKS.md).

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here:
its user time is not above its real time (0.641 s and 0.647 s on one
run).

## Verification

All four arms print the same output as `queue.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `9b0b5eb92c`.

## Writing it

The ★, vec and deque arms checked clean as first written.

The Rust solution took one `karac fix` of 16 edits: the
`use std::collections::VecDeque;` line deleted (`VecDeque` is in Kāra's
prelude), `VecDeque<i32>` written `VecDeque[i32]`, `Self { .. }` written
with the type's name, `VecDeque::new` written `VecDeque.new`, every
`&mut self` written `mut ref self`, and `!` written `not`.

`arm_name` in the differential indexes a list of string literals for a
`Str`, as #1662's does (B-2026-11-19-131).
