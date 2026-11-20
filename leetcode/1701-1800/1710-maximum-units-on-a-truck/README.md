# 1710. Maximum Units on a Truck

You are assigned to put some amount of boxes onto **one truck**. You are
given a 2D array `boxTypes`, where `boxTypes[i] = [numberOfBoxesi,
numberOfUnitsPerBoxi]`:

- `numberOfBoxesi` is the number of boxes of type `i`.
- `numberOfUnitsPerBoxi` is the number of units in each box of the type
  `i`.

You are also given an integer `truckSize`, which is the **maximum**
number of **boxes** that can be put on the truck. You can choose any
boxes to put on the truck as long as the number of boxes does not exceed
`truckSize`.

Return *the **maximum** total number of **units** that can be put on the
truck.*

```
boxTypes = [[1,3],[2,2],[3,1]], truckSize = 4              ->  8
boxTypes = [[5,10],[2,5],[4,7],[3,9]], truckSize = 10      ->  91
```

**Constraints:** `1 <= boxTypes.length <= 1000`;
`1 <= numberOfBoxesi, numberOfUnitsPerBoxi <= 1000`;
`1 <= truckSize <= 10^6`.

## Approaches

| file | mechanism |
|---|---|
| `units.kara` ★ | every box takes the same room, so one of more units is never worse: the types sorted by units, most first (`sort_by_key` on the negated units), and boxes taken from the front until the truck is full. O(n log n) |
| `units_counting.kara` | a box holds 1 to 1000 units, so the boxes of each count are added up in an array of 1001 and the truck filled walking it from 1000 down. No sort: O(n + 1000) |
| `units_heap.kara` | the types in a `PriorityQueue.max_first()` as (units, boxes), the truck taking from the top until it is full or the queue is empty. O(n log n) |
| `units_solution.kara` | a Rust solution as LeetCode's Rust users write it, `mut box_types` sorted in place by `sort_unstable_by(\|a, b\| b[1].cmp(&a[1]))`, consumed by `for bt in box_types`, and `remaining.min(bt[0])`, carried to Kāra by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 8 lines: LeetCode's two examples, a truck
bigger than every box, one box, and two types of the same units; then
the answers summed and a checksum for 3000 random problems of up to 6
box types, 300 of up to 1000 with trucks up to `10^6`, and 10 of up to
1000 with trucks up to 1000. `units.py` mirrors the ★ arm and its output
is byte-identical.

```
8
91
26
1
34
3000 problems of up to 6 box types: answers sum to 71895, checksum 291724005
300 problems of up to 1000 box types: answers sum to 30478933286, checksum 744557626
10 problems of up to 1000 box types: answers sum to 5716454, checksum 643112178
```

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every choice of how many boxes of each type to put on, from
none to all of them, that the truck holds; the most units among them.
It checks 3000 random problems of 1 to 5 box types, each 1 to 4 boxes of
1 to 6 units, and a truck of 1 to 16 boxes. Every case is drawn before
any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | a truck one box larger carries at least as many units, and at most the most units of any box more |
| P3 | every box's units doubled doubles the answer |
| P4 | the box types listed in reverse give the same answer |
| P5 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 621622603, 60000 checks
over 4 arms: 0 failures` under every lane in Verification, and a Python
reading of the statement, every set of single boxes that fits from
`itertools.combinations`, gives the same checksum. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. M1 and M9 sort the fewest units first
in two arms and fail the very same checks; a truck one larger still
takes one more box, of whatever units, so neither fails P2.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the fewest units first | P1 1128, P5 1128 |
| M2 | ★: each type takes one box less than the room left | P1 1396, P5 1396 |
| M3 | ★: sorted by the number of boxes, not their units | P1 802, P4 501, P5 802 |
| M4 | counting: a later type of the same units replaces an earlier | P1 938, P4 769, P5 938 |
| M5 | counting: boxes of one unit left off | P1 789, P3 789, P5 789 |
| M6 | counting: every box of a count taken, the room ignored | P1 960, P2 139, P5 960 |
| M7 | heap: queued by the number of boxes | P1 1662, P2 24, P3 2443, P5 1662 |
| M8 | heap: the last box of room never filled | P1 563, P2 288, P5 563 |
| M9 | solution: sorted the fewest units first | P1 1128, P5 1128 |
| M10 | solution: stops at the type that fills the room left | P1 784, P2 156, P4 323, P5 784 |

## Benchmarks

The bench draws 1000 random problems of 1000 box types, LeetCode's
most, each 1 to 1000 boxes of 1 to 1000 units and a truck of up to
`10^6` boxes, all of them first, then answers each 10 times by the ★ arm
in all five languages; each answer sorts a copy of its box types. Every
implementation prints `1000 problems of 1000 box types, 10 rounds:
answers sum to 2102738929280, checksum 53618223`. The C mirror holds a
box type as a struct of two `int`s and sorts with `qsort`. The C build
also runs clean under gcc's AddressSanitizer and
UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `9b0b5eb92c` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.620 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.673 s |
| Rust (`rustc -O`) | 0.683 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.764 s |
| Kāra (`karac build`) | 0.815 s |
| Go | 4.014 s |
| Python | 3.6 s |

The sequential Kāra build takes 1.12x Rust's time and 1.14x that of Rust
with overflow checks on, the equal-safety comparison (BENCHMARKS.md). C
is the fastest here at 0.620 s.

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here:
its user time is not above its real time (0.711 s and 0.749 s on one
run).

## Verification

All four arms print the same output as `units.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `9b0b5eb92c`.

## Writing it

The ★, counting and heap arms each started their total `let mut total =
0` and added `i32` products to it, as Rust infers. In Kāra a literal
keeps its default, `i64`, when only an operator meets it, so returning
`total` as the `i32` answer narrowed; `karac check` said so and to
declare it `total: i32`, and `karac fix` did. The counting arm's walk
`(1..=1000).rev()` multiplied its count into the same total, and the
fix wrote its first bound `1i32` too.

LeetCode's Rust template took one `karac fix` of 10 edits:
`struct Solution {}` added, `Vec<Vec<i32>>` written `Vec[Vec[i32]]`,
`mut box_types` written `box_types: own
Vec[Vec[i32]]` with `let mut box_types = box_types;` at the body's start
(the `own` carried on to the wrapper), `sort_unstable_by` written
`sort_by`, `&a[1]` written `a[1]`, and `total: i32`. `for bt in
box_types` and `remaining.min(bt[0])` carried over as written.

The differential's `arm` first cast the `i32` answer `as i64`; the
`lossless_cast` lint saw that it widens by itself, and `karac fix`
dropped it. `arm_name` indexes a list of string literals for a `Str`, as
#1662's differential does (B-2026-11-19-131).
