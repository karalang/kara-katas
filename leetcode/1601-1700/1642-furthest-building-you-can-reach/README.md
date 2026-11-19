# 1642. Furthest Building You Can Reach

You are given an integer array `heights` representing the heights of
buildings, some `bricks`, and some `ladders`.

You start your journey from building `0` and move to the next building by
possibly using bricks or ladders.

While moving from building `i` to building `i+1` (**0-indexed**),

- If the current building's height is **greater than or equal** to the
  next building's height, you do **not** need a ladder or bricks.
- If the current building's height is **less than** the next building's
  height, you can either use **one ladder** or
  `(h[i+1] - h[i])` **bricks**.

*Return the furthest building index (0-indexed) you can reach if you use
the given ladders and bricks optimally.*

```
heights = [4,2,7,6,9,14,12], bricks = 5, ladders = 1                 ->  4
heights = [4,12,2,7,3,18,20,3,19], bricks = 10, ladders = 2          ->  7
heights = [14,3,19,3], bricks = 17, ladders = 0                      ->  3
```

**Constraints:** `1 <= heights.length <= 10^5`;
`1 <= heights[i] <= 10^6`; `0 <= bricks <= 10^9`;
`0 <= ladders <= heights.length`.

## Approaches

| file | mechanism |
|---|---|
| `furthest.kara` ★ | ladders are best spent on the largest climbs: the climbs so far that ladders cover in a `PriorityQueue` (smallest first), and once there are more of them than ladders the smallest is paid for in bricks. The first building the bricks cannot pay for is the end. O(n log l) for l ladders |
| `furthest_bricks.kara` | the mirror image: every climb paid in bricks and kept in a largest-first heap, a `PriorityQueue` of `Reverse` climbs; when the bricks run short, the largest paid climb gets a ladder instead. O(n log n) |
| `furthest_search.kara` | a binary search on the answer: building k can be reached when its climbs, sorted, fit ladders on the largest and bricks on the rest, which only gets harder as k grows. O(n log^2 n) |
| `furthest_solution.kara` | LeetCode's Rust template: a `BinaryHeap` of `Reverse(climb)` with `bricks` a `mut` parameter. Carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's three examples, one
building (0), a row all downhill with nothing to climb with (3), and one
climb with nothing to pay (0); then the indices summed and a checksum
for 3000 random rows of up to 8 buildings up to 5 high, 300 of up to 1000
up to `10^6`, and 5 of up to `10^5` up to `10^6`. `furthest.py` mirrors
the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: building k can be reached when some choice of which climbs on
the way take a ladder, no more than there are ladders, leaves the rest
within the bricks; every choice is tried as a bit mask, and the answer is
the furthest such k. It checks 3000 random rows of 1 to 8 buildings with
0 to 12 bricks and 0 to 2 ladders, every other row with heights 1 to 4,
so climbs are small and often equal, the rest 1 to 20. Every row is drawn
before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | five more bricks never take you less far |
| P3 | one more ladder never takes you less far |
| P4 | every building 100 higher gives the same answer |
| P5 | the answer is a building of the row, and short of the last one only where the next step is a climb |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 779448934, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. Two first tries survived and are
equivalent, and were replaced: the ★ arm and the template pushing level
and downhill steps into the heap as climbs of 0. A 0 there is always
popped first and costs no bricks. The bricks arm refunding the newest
climb rather than the largest when it takes a ladder (M4) is the
subtlest kill: 4 rows of the 3000 show it.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a ladder held back | P1 581, P6 581 |
| M2 | ★: the building the bricks cannot pay for counted as reached | P1 596, P5 337, P6 596 |
| M3 | ★: each overflow paid with the newest climb, not the smallest | P1 116, P6 116 |
| M4 | bricks: a ladder refunds the newest climb, not the largest | P1 4, P2 2, P6 4 |
| M5 | bricks: ladders never run out | P1 596, P6 596 |
| M6 | search: the lower bound steps back past a good guess | hangs on both backends |
| M7 | search: one ladder too many | P1 596, P6 596 |
| M8 | search: the climbs left unsorted | P1 128, P6 128 |
| M9 | template: one ladder too many | P1 596, P6 596 |
| M10 | template: each climb weighed at half | P1 394, P6 394 |

## Benchmarks

The bench draws 50 random rows of 100000 buildings up to `10^4` high,
LeetCode's longest, each with up to `10^9` bricks and up to 5000
ladders, all of them first, then walks each by the ★ arm in all five
languages, each with its own min-heap: Kāra's `PriorityQueue`, Rust's
`BinaryHeap` of `Reverse`, Go's `container/heap`, Python's `heapq`, and a
binary heap written out in C. Heights up to `10^4` rather than `10^6`
let the bricks last most of the row. Every implementation prints `50
rows of 100000 buildings: indices sum to 4340757, checksum 975070592`.
The C build also runs clean under gcc's AddressSanitizer and
UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `ee08f070a` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.114 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.120 s |
| Kāra (`karac build`) | 0.121 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.124 s |
| Rust (`rustc -O`) | 0.130 s |
| Go | 0.377 s |
| Python | 2.2 s |

The sequential Kāra build is level with Rust and level with Rust with
overflow checks on, the equal-safety comparison (BENCHMARKS.md). C is
the fastest here at 0.114 s.

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes
nothing here: its user time is not above its real time (0.108 s and
0.117 s on one run).

## Verification

All four arms print the same output as `furthest.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `336218278`.

## Writing it

The ★ arm checked clean as first written. The bricks and search arms
first declared their pairs Rust's way, `let (mut bricks, mut ladders) =
..`, and `karac fix` moved the `mut` before the pattern. The bricks arm
also wrote `Reverse(climb)` and `let Reverse(largest) = ..` as Rust's
tuple struct, and the fix wrote Kāra's `Reverse { value: climb }` with
`import std.cmp.Reverse;`. The search arm compared an `i64` sum with
`bricks as i64`, and the `lossless_cast` lint dropped the cast.

LeetCode's Rust template takes one `karac fix` of 16 edits, among them
the `mut bricks: i32` parameter to a plain one with
`let mut bricks = bricks;` first in the body, `BinaryHeap` of `Reverse`
to a plain `PriorityQueue` (Kāra's pops smallest first already) with
`.0` dropped from the pop, `ladders as usize` to `ladders`, and both `use`
lines dropped. The arm then checks and agrees with no hand edit.
