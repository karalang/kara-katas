# 1845. Seat Reservation Manager

Design a system that manages the reservation state of `n` seats that are
numbered from `1` to `n`. Implement the `SeatManager` class:
`SeatManager(int n)` initializes a `SeatManager` object that will manage
`n` seats numbered from `1` to `n`, all of them initially available;
`int reserve()` fetches the smallest-numbered unreserved seat, reserves
it, and returns its number; `void unreserve(int seatNumber)` unreserves
the seat with the given `seatNumber`.

```
SeatManager(5), reserve, reserve, unreserve(2), reserve, reserve, reserve, reserve, unreserve(5)
  ->  1, 2, 2, 3, 4, 5
```

**Constraints:** `1 <= n <= 10^5`, `1 <= seatNumber <= n`; each call to
`reserve` has at least one unreserved seat, each call to `unreserve`
names a reserved seat, and at most `10^5` calls are made in all.

The arms are `struct SeatManager` with `fn new(n: i64) -> SeatManager`,
`fn reserve(mut ref self) -> i64` and `fn unreserve(mut ref self,
seat_number: i64)`.

## Approaches

| file | mechanism |
|---|---|
| `seat_manager.kara` ★ | every unreserved seat in a `PriorityQueue`, which pops the smallest first, so a reservation pops the lowest free seat and a seat given back is pushed again. O(n log n) to build, O(log n) a call |
| `seat_manager_lazy.kara` | the seats never reserved are the run from `next` on, kept as a number alone, and only the seats given back go in a `PriorityQueue`; a reservation takes the queue's least when it has one, as every seat in it is below `next`, and `next` otherwise. O(log k) a call, `k` the seats given back |
| `seat_manager_set.kara` | the unreserved seats in a `SortedSet`, the lowest its `min`, removed on a reservation and put back on a return. O(n log n) to build, O(log n) a call |
| `seat_manager_tree.kara` | a segment tree over the seats counting the free ones in each range: a reservation walks down from the root to the first leaf with a free seat, always the left child when it has one, and marks it taken; a return marks it free again. O(n) to build, O(log n) a call |
| `seat_manager_solution.kara` | a Rust solution as LeetCode's Rust users write it (a `BinaryHeap<Reverse<i32>>` collected from `1..=n`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 4 lines: LeetCode's example; three edges, one
seat taken and given back twice over, every seat taken, and the lowest
given back first and then a higher one (`[1, 1, 1] [1, 2, 3, 4] [1, 2,
3, 1, 3]`); the constraints' most, 10^5 seats and 10^5 calls drawn at
random, and 10^5 reservations, each folded to one number (`the most:
204778183 743978544`); and 300 random runs of 1 to 60 calls on 1 to 12
seats, each return a held seat drawn at random (`300 random runs: 5227
reservations, checksum 83839602`). `seat_manager.py` mirrors the ★ arm,
and its output is byte-identical. Every arm gives the same output under
`karac __mir-run`, `karac run`, `karac build` and `karac
__mir-llvm-run`.

The Mend loop: every arm checks clean as first written. The Rust
solution takes 15 fixes by `karac fix`'s count, and its diff is: `use
std::cmp::Reverse` to `import std.cmp.Reverse`, and the `BinaryHeap`
import taken off; `BinaryHeap<Reverse<i32>>` to
`PriorityQueue[Reverse[i32]]`; `.map(Reverse)` to `.map(|x| Reverse {
value: x })`, `Reverse(seat_number)` to `Reverse { value: seat_number }`
and `.0` to `.value`; `&mut self` to `mut ref self`; `SeatManager::new`
to `SeatManager.new` at the harness's 2 calls; and one of the harness's
two `as i64` on a reservation taken off. That program checks clean and
is wrong: it prints `[5, 4, 3, 2, 2, 1]` for LeetCode's example. Rust's
`BinaryHeap` pops the largest first, so a heap of `Reverse` seats pops
the smallest seat, and Kāra's `PriorityQueue` pops the smallest first,
so the same heap of `Reverse` seats pops the largest. `karac fix` writes
a collected `BinaryHeap` as `PriorityQueue.max_first_from(..)`, which
keeps Rust's order, when it is collected into a `let` (B-2026-11-15-80,
B-2026-11-15-86), and it misses one collected into a struct literal's
field, B-2026-11-27-3. The solution here is the fixed program with that
one call written by hand, `PriorityQueue.max_first_from((1..=n).map(|x|
Reverse { value: x }).collect())`. The solution takes and gives `i32`s,
so its harness passes `n as i32` and each seat `as i32`. Every arm's
output matches on the first run.

## Differential

`differential.kara` holds copies of the five arms, each behind one
`trait Seats` so one driver runs them all, and the statement read
literally: every seat marked reserved or not, a reservation the
smallest-numbered seat not reserved, and a return its seat marked
unreserved. It runs 2000 random runs of 1 to 40 calls on 1 to 12 seats,
drawn as LeetCode allows them on the literal reading: a reservation
while a seat is free, when none is held or by a draw, and otherwise a
held seat drawn at random given back. Each arm meets six properties on
each case:

| property | what it checks |
|---|---|
| P1 | the statement read literally |
| P2 | each seat from 1 to `n`, none handed out while it is held |
| P3 | five seats more change nothing, as the lowest free seat is never past the seats held |
| P4 | a seat reserved, given back and reserved again is the same seat |
| P5 | each reservation at most one past the seats held before it |
| P6 | the ★ arm's answer |

It checks clean as first written. All 60,000 checks pass on every arm:
`2000 cases: checksum 746470343, 60000 checks over 5 arms: 0 failures`,
under `karac __mir-run`, `karac run`, `karac build` and `karac
__mir-llvm-run`. Python, over the same cases, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash. The set arm's
first edit was first to reserve the highest free seat; it stopped on an
`unwrap` of `None`, a crash, and it now leaves a reserved seat in the
free set. The solution's second edit builds its heap with
`PriorityQueue.from(..)` in place of `PriorityQueue.max_first_from(..)`,
so the queue pops the largest seat first, as the program `karac fix`
writes does.

| | edit | failures by property |
|---|---|---|
| M1 | ★: the seats numbered from 2 | P1 2000, P2 1108, P4 412, P5 2000, P6 8000 |
| M2 | ★: a seat given back as the one after it | P1 1823, P2 1775, P4 412, P5 1693, P6 7292 |
| M3 | lazy: a seat never reserved handed out as the one after it | P1 2000, P2 1108, P4 412, P5 2000, P6 2000 |
| M4 | lazy: a seat given back recorded as the next never reserved | P1 1823, P2 1764, P4 412, P5 1823, P6 1823 |
| M5 | set: a reserved seat left in the free set | P1 1709, P2 1709, P6 1709 |
| M6 | set: a reserved seat left in the set, the one after it removed | P1 1709, P2 1709, P6 1709 |
| M7 | tree: the walk down taking the right child first, the highest free seat | P1 1820, P2 1040, P3 2000, P4 1113, P5 1820, P6 1820 |
| M8 | tree: each seat handed out as the one before it | P1 2000, P2 2000, P6 2000 |
| M9 | solution: a seat given back as the one after it | P1 1823, P2 1775, P4 412, P5 1693, P6 1823 |
| M10 | solution: the queue of `Reverse` seats built smallest first, as `karac fix` builds it, so the highest seat pops | P1 1820, P2 1170, P3 2000, P4 1078, P5 1820, P6 1820 |

## Benchmarks

The bench builds one list of 10^6 draws once and makes 50 runs of the ★
arm, each of 10^5 calls on 50000 to 99999 seats, the run's size and its
place in the draws taken from the checksum so far. A draw reserves a
seat two times in three, while one is free, and otherwise gives back a
held seat it picks, and every seat reserved goes into the checksum. C,
which has no priority queue, writes the heap out. It checks clean as
first written. Every implementation prints `50 runs: checksum
412106871`.

BENCHTAB

Measured by hand, best of three on a machine shared with a test run,
Kāra takes 0.26 s against Rust's 0.26 s (0.26 s with overflow checks
on), C's 0.28 s and Go's 0.74 s; Python takes 2.7 s.
