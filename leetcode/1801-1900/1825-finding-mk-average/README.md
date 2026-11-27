# 1825. Finding MK Average

You are given two integers, `m` and `k`, and a stream of integers. You
are tasked to implement a data structure that calculates the MKAverage
for the stream. The MKAverage can be calculated using these steps: if
the number of the elements in the stream is less than `m` you should
consider the MKAverage to be `-1`; otherwise, copy the last `m` elements
of the stream to a separate container, remove the smallest `k` elements
and the largest `k` elements from the container, and calculate the
average value for the rest of the elements rounded down to the nearest
integer. Implement the `MKAverage` class: `MKAverage(int m, int k)`
initializes the object with an empty stream and the two integers `m` and
`k`; `void addElement(int num)` inserts a new element `num` into the
stream; `int calculateMKAverage()` calculates and returns the MKAverage
for the current stream rounded down to the nearest integer.

```
MKAverage(3, 1), addElement(3), addElement(1), calculateMKAverage(), addElement(10),
calculateMKAverage(), addElement(5), addElement(5), addElement(5), calculateMKAverage()
  ->  null, null, null, -1, null, 3, null, null, null, 5
```

**Constraints:** `3 <= m <= 10^5`, `1 <= k * 2 < m`, `1 <= num <= 10^5`,
at most `10^5` calls to `addElement` and `calculateMKAverage`.

The arms are `struct MkAverage`, with `fn new(m: i64, k: i64) ->
MkAverage`, `fn add_element(mut ref self, num: i64)` and `fn
calculate_mk_average(self) -> i64`. The harness drives one with `run(m,
k, ops)`: a number in `ops` is added, and a -1 asks for the average.

## Approaches

| file | mechanism |
|---|---|
| `finding_mk_average.kara` ★ | once the window is full, its numbers are kept in three ordered bags, a `SortedMap` of counts each, the `k` smallest, the `k` largest and the rest, with the sum of the rest. A number leaving or coming in goes to the bag its value belongs in, and the bags are then evened out at their ends. O(log m) per operation |
| `finding_mk_average_fenwick.kara` | two Fenwick trees over the values 1 to 10^5, of how many numbers of the window hold each value and of their sums; the sum of the `t` smallest is found by walking down the tree's powers of two, so the average is the sum of the `m - k` smallest less that of the `k` smallest. O(log V) per operation, V = 10^5 |
| `finding_mk_average_segment.kara` | a segment tree over the values 1 to 10^5, each node holding how many numbers of the window fall in its range and their sum; the sum of the `t` smallest is read going down from the root, taking a left child whole when the `t` smallest reach past it. O(log V) per operation |
| `finding_mk_average_sort.kara` | no structure kept but the window, a `VecDeque`: each average sorts a copy of it and sums all but its `k` smallest and `k` largest. O(1) to add, O(m log m) to average |
| `finding_mk_average_solution.kara` | a Rust solution as LeetCode's Rust users write it (the fenwick arm's two trees, with a `VecDeque<i32>` window and `usize` indices), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 5 lines: LeetCode's example; four edges, a
window of equal numbers, the oldest numbers leaving the window with the
largest among them, the largest values, and the most cut, `k` as large
as `m` allows (`[7] [46, 2, 2, 3] [100000] [5, 4]`); the constraints'
most, 10^5 calls of 99990 numbers from 1 to 10^5 and 10 averages, on a
window of 50000 numbers cutting 10000 from each end (`the most: [-1, -1,
-1, -1, -1, 49996, 49776, 49793, 49915, 49882]`) and on one of 99000
cutting 1 (`the most again: [-1, -1, -1, -1, -1, -1, -1, -1, -1,
49905]`); and 300 random runs of 1 to 60 operations on windows of 3 to
10 numbers from 1 to 20, about a third of them asking for the average
(`300 random runs: 2931 averages, checksum 622633566`).
`finding_mk_average.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac __mir-run`,
`karac run`, `karac build` and `karac __mir-llvm-run`.

The Mend loop: the fenwick, segment and sort arms and the harness check
clean as first written. The harness's constraints' most was first
written on a window its numbers never filled, so every average came out
-1, and with its numbers drawn only up to 32767; the window is now 50000
numbers, and each number is made of two draws. The ★ arm was first
written with LeetCode's name, `MKAverage`; check warned that the name
breaks Kāra's case rule for acronyms, and `karac fix` wrote `MkAverage`,
5 fixes. The Rust solution takes 38 fixes by `karac fix`'s count, and
its diff is: `use std::collections::VecDeque` taken off; `MKAverage` to
`MkAverage`; the `usize` fields, const and parameters to `i64`, so `m as
usize`, `num as usize`, `old as usize`, `x as i64`, `t as i64`, `pos as
i64` and the divisor's `as i64` are all taken off; `Vec<i64>` and
`VecDeque<i32>` to `Vec[i64]` and `VecDeque[i32]`; `VecDeque::new()` to
`VecDeque.new()` and `vec![0; N + 1]` to `Vec.filled(N + 1, 0)`; `&mut
self` to `mut ref self` and `&self` to `self`; `&&` to `and`;
`MKAverage::new` to `MkAverage.new` in the harness; and the harness's
`as i64` on the average taken off. `i.wrapping_neg()`, `1 << 17` and
`self.q.pop_front().unwrap()` are Kāra as they stand, and the `i32`
numbers of the window widen to the `i64` index without a cast. The
solution takes `i32`s, so its harness passes `m as i32`, `k as i32` and
`op as i32`. Every arm's output matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every number kept as it comes; asked, the average is -1 while
fewer than `m` have come, and otherwise the last `m` are copied and
sorted, the `k` smallest and the `k` largest taken off, and the rest
averaged, rounded down. The five arms are driven through one `trait
Window`, which each arm's `MkAverage` implements, and one generic
`drive[W: Window]`. It runs 2000 random runs of 1 to 40 operations on
windows of 3 to 10 numbers from 1 to 20, about a third of them asking
for the average. Each arm meets six properties on each case:

| property | what it checks |
|---|---|
| P1 | the statement read literally |
| P2 | -1 exactly while fewer than `m` numbers have come, and otherwise between the least and the largest of the last `m` |
| P3 | every number raised by 1000 raises every average by 1000 |
| P4 | every number `x` made `100001 - x` swaps the `k` smallest with the `k` largest, so an average and its mirror sum to 100001, or one less where the average was rounded down |
| P5 | every average asked for twice in a row is given twice |
| P6 | the ★ arm's answer |

It checks clean as first written. All 60,000 checks pass on every arm:
`2000 cases: checksum 318935914, 60000 checks over 5 arms: 0 failures`,
under `karac __mir-run`, `karac run`, `karac build` and `karac
__mir-llvm-run`. Python, over the same cases, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: the average taken over m - k numbers | P1 1395, P2 485, P3 1395, P4 1395, P6 5580 |
| M2 | ★: the largest bag let hold k + 1 | P1 822, P2 368, P3 822, P4 1108, P6 3288 |
| M3 | fenwick: each node's sum kept of its index | P1 1343, P2 766, P3 911, P4 1389, P6 1343 |
| M4 | fenwick: the value the walk stops below counted one less | P1 453, P2 3, P4 30, P6 453 |
| M5 | segment: the value the walk stops at counted one more | P1 302, P2 5, P4 241, P6 302 |
| M6 | segment: a number leaving the window left in the sums | P1 1158, P2 1029, P3 1159, P4 1220, P6 1158 |
| M7 | sort: one of the k largest kept | P1 1395, P2 783, P3 1395, P4 1395, P6 1395 |
| M8 | sort: the window let hold m + 1 numbers | P1 1097, P4 1222, P6 1097 |
| M9 | solution: the value the walk stops below counted one less | P1 453, P2 3, P4 30, P6 453 |
| M10 | solution: the k largest kept | P1 1395, P2 1024, P3 1395, P4 1395, P6 1395 |

## Benchmarks

The ★ arm's ordered bags have no counterpart in C, Go or Python's
standard library, so the bench runs the fenwick arm, which every
language writes the same way. It builds one list of 10^5 numbers from 1
to 10^5 once and makes 20 calls, each a fresh `MkAverage` on a window of
1000 to 49999 numbers cutting 1 to half of them, the window and its cut
drawn from the checksum so far; each call adds the 10^5 numbers and asks
for the average after every hundredth. It checks clean as first written.
Every implementation prints `20 calls: checksum 689359792`.

BENCHTAB

Measured by hand, best of three on a machine shared with a test run,
Kāra is ahead of Rust here at 0.15 s against Rust's 0.16 s (0.17 s with
overflow checks on), C's 0.16 s and Go's 0.22 s; Python takes 7.4 s.
