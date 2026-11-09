# 1086. High Five

Given a list of the scores of different students, `items`, where
`items[i] = [IDi, scorei]` represents one score from a student with
`IDi`, calculate each student's top five average.

Return the answer as an array of pairs `result`, where
`result[j] = [IDj, topFiveAveragej]` represents the student with `IDj`
and their top five average. Sort `result` by `IDj` in increasing order.

A student's top five average is calculated by taking the sum of their
top five scores and dividing it by `5` using integer division.

```
items = [[1,91],[1,92],[2,93],[2,97],[1,60],[2,77],[1,65],[1,87],[1,100],[2,100],[2,76]]  ->  [[1,87],[2,88]]
items = [[1,100],[7,100],[1,100],[7,100],[1,100],[7,100],[1,100],[7,100],[1,100],[7,100]]  ->  [[1,100],[7,100]]
```

**Constraints:** `1 <= items.length <= 1000`; `items[i].length == 2`;
`1 <= IDi <= 1000`; `0 <= scorei <= 100`; for each `IDi`, there will be
at least five scores.

The arms take the items as a `Vec[Vec[i64]]` and return the pairs as a
`Vec[Vec[i64]]`.

## Approaches

| file | mechanism |
|---|---|
| `high_five.kara` ★ | the scores grouped by student in a `SortedMap[i64, Vec[i64]]` (`get_mut`, else `insert`), which walks the ids in order; each student's scores cloned, sorted high to low with `sort_by`, and `take(5).sum()` divided by 5. O(n log n) |
| `high_five_heap.kara` | a smallest-first `PriorityQueue` of five per student in a `Map` (`entry(id).or_insert_with`): each score pushed, the smallest popped when there are six; the ids collected and sorted, and each queue summed with `iter().sum()`. O(n log 5) |
| `high_five_sorted.kara` | one `sort_by` of every item, by id and then by score high to low (`cmp(..).then(..)`), and one walk that sums the first five of each run of an id. O(n log n) |
| `high_five_buckets.kara` | counted, not sorted: a `Vec[Array[i64, 101]]` of score counts for each id up to the greatest, filled in one pass; then, for each id seen, the five highest read from the counts down from 100. O(n + m · 101), m the greatest id |
| `high_five_five.kara` | the five best kept in place: a `SortedMap` of a `struct` holding an `Array[i64, 5]`, highest first, into which each score is slid where it belongs, the lowest falling off. O(5 n) |
| `high_five_solution.kara` | LeetCode's Rust template (`struct Solution;`, a `BTreeMap<i32, BinaryHeap<Reverse<i32>>>`, `entry(..).or_insert_with(BinaryHeap::new)`, `push(Reverse(..))`, `heap.into_iter().map(\|Reverse(s)\| s).sum()`, `vec![id, sum / 5]`, `Solution::`), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 5 lines: LeetCode's two examples and two more,
and the students and a checksum over 300 random lists of 1 to 40
students with ids 1 to 1000 (`6036 students, checksum 24879333`).
`high_five.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: each student once, smallest id first, the next being the
smallest id above the last one answered; and its average, the sum of its
five greatest scores, each the greatest of those left taken out in turn,
divided by 5. It checks 2000 problems: 1000 lists of 1 to 4 students
with ids 1 to 6 and 5 to 7 scores each, from 0 to 10 in half of them and
9 or 10 in the other half, so that ties are common, and 1000 of 1 to 30
students with ids 1 to 499 and 5 to 12 scores from 0 to 100. Every
random choice is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the items in another order, or written backwards, answer the same |
| P3 | a score no greater than a student's fifth best, added, changes nothing |
| P4 | every id moved to 2 id + 1 moves the answer's ids the same way |
| P5 | every score raised by d raises every average by d: half the time d takes the greatest score to 100, otherwise it is anywhere short of that |
| P6 | one student's items alone answer that student's row |

All 72,000 checks pass on every arm: `2000 problems: checksum 684392327,
72000 checks over 6 arms: 0 failures`. A Python reading of the same
problems, by sorting each student's scores, gives the same checksum.

## Mutation testing

Thirty edits to the differential, five to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. Twenty-six are caught,
each the same way under both backends but one (H3, below), and two more
stop both with an index out of bounds (the buckets arm reading no 100,
and taking at most one of each score, run below 0 when a student's five
best are not all there). Fifteen are kept, no two failing the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: four scores summed | P1 1883, P5 1245 |
| M2 | ★: a student's first score lost | P1 1715, P2 1549, P3 347, P5 660 |
| M3 | heap: the largest popped (`max_first`) | P1 1549, P3 1703 |
| M4 | heap: the ids in the map's order | P1 1511, P2 1643 |
| M5 | heap: the first five kept | P1 1464, P2 1452 |
| M6 | heap: the five thrown out at a sixth (`clear`) | P1 1895, P2 1471, P3 1499, P5 1167 |
| M7 | sorted: sorted by score alone | P1 1713, P2 1691, P3 1525, P5 1000, P6 1712 |
| M8 | sorted: every score of a run summed | P1 1709, P3 1355, P5 1166 |
| M9 | sorted: the ids high to low | P1 1713 |
| M10 | buckets: each score counted once however many take it | P1 2000, P5 1281 |
| M11 | buckets: a student seen only by a score above 0 | P1 237, P2 544, P3 308, P5 120 |
| M12 | five: the lower score dropped, not slid down | P1 1871, P2 1909, P3 1208, P5 1118 |
| M13 | five: four kept | P1 1940, P5 1236 |
| M14 | solution: 100 read as 0 (`sum / 5 % 100`) | P5 49 |
| M15 | solution: two popped at a time | P1 1524, P2 1095, P3 1557, P5 800 |

M4's P1 count is 1511 under one backend and 1534 under the other, and
moves from run to run: it walks a `Map`, whose order is random per
process.

P1 catches fourteen, P5 eleven, P2 and P3 eight each, P6 one and P4
none. P1 misses M14 because no list it is given has a student whose five
best are all 100; P5 makes one by raising the greatest score to 100, and
a first pass of this differential, before P5 did that half the time, let
M14 live. P4 moves every id while keeping their order, and every edit
here treats an id by its order alone. M4 is the one that might not, and
its counts suggest, without it being checked, that the map walks these
small tables in the order the ids arrive, which P2 changes and P4
keeps. P6 sees only M7, which breaks one
student's run with another's: a student alone has no other to mix with.
P3's low score goes in last, so it sees the edits that care where or
whether a score below the five best arrives.

Of the fifteen not kept, the two crashes are above, two are equivalent
and survive, and eleven fail exactly as a kept edit or as one another.
The equivalent two are in the five arm: an equal score slid in (`>=`)
moves the same values, and the array starting at 0 rather than -1 is
filled past by the five scores every student has. The ★ arm sorted low
to high, the sorted arm's runs sorted low to high and the solution arm
built `max_first` fail as M3; four kept in the solution arm, and its
first score in heap order skipped (the smallest, in a smallest-first
queue), as M1; the score written over the first lower in the five arm as
M12; six kept in the heap and sorted arms fail alike (P1 1677, P3 420,
P5 1130); and the ★ arm counting a lower score as its first, rounding
up, and the buckets arm leaving out the greatest id fail in ways of
their own but were not needed.

## Verification

Every arm prints the same output as `high_five.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any file. Under `karac __mir-run`, with the machine busy with a test
run, the arms take 0.5 s to 1.2 s and the differential 83 s.

The kata found two gaps, fixed in kara `2f62c55005` with
`tests/kata_1086_priority_queue_iter.rs`:

- **`PriorityQueue` could not be read without draining it.** The heap
  arm sums each student's queue, and the Rust template sums it with
  `heap.into_iter()`. `PriorityQueue` had no `iter`, no `into_iter`, no
  `for`, no `Clone` and no `Display`, though collections.md says every
  collection works with `for` and is `Display` when its elements are;
  the only way to read one was `into_sorted_vec`, which pops every
  element. It now has `iter` and `into_vec`, the `Iterable` and
  `IntoIterator` impls, `Clone` and `Display`, all in the queue's own
  order, its backing vector's, as Rust's `BinaryHeap::iter` is. Kara
  B-2026-11-09-41.
- **The template's `Reverse` heap stopped `karac fix`.** `|Reverse(s)|`
  as a closure parameter got only "a parameter's pattern must be
  irrefutable", with no edit; and `BinaryHeap::new` named as a value
  (`or_insert_with(BinaryHeap::new)`) was not seen as a heap's
  constructor, so neither it nor any `Reverse` in the program got the
  smallest-first fix the called form gets. The parameter is now fixed to
  `|s|` in a program that uses `std::cmp::Reverse`, and the named
  constructor is recorded like the called one. Kara B-2026-11-09-42.

Every file went through `karac fix`, which changed nothing outside the
Rust arm. The Rust arm reaches a clean check in four rounds and gives the
text the arm holds: the syntax (`struct Solution {}`, `<>` to `[]`, `::`
to `.`, the `&` dropped from `|&x|`, `Solution.`), the `use std::cmp`
line gone and `|Reverse(s)|` to `|s|`; then the `use std::collections`
line gone; then `BTreeMap` to `SortedMap`, `BinaryHeap[Reverse[i32]]` to
`PriorityQueue[i32]`, `BinaryHeap.new` to `PriorityQueue.new` and
`push(Reverse(..))` to `push(..)`; then `vec![id, sum / 5]` to
`[id, sum / 5]`. The `.map(|s| s)` left behind stays as written.

## Benchmarks

The bench builds 200 random lists of 1000 items once, LeetCode's
largest: list t has 50 + t % 150 students with ids from 1 to 1000, five
scores each and the rest of the 1000 given to students at random, every
score 0 to 100, the items shuffled. Each of 50 rounds answers every list
with the ★ arm, in an order that changes with the round, folding every
id and average into a checksum. Every implementation prints `50 rounds
over 200 lists of 1000 items: 1120000 students, checksum 871461591`.

Each mirror keeps the ★ arm's steps in its own language's way: Rust
groups in a `BTreeMap` over LeetCode's `Vec<Vec<i64>>`; Go and Python in
a hash map whose ids are sorted at the end, as neither has an ordered
map; C in an array of groups kept sorted by id and found by binary
search, each sorted with `qsort`. Every mirror allocates the groups and
the sorted copy afresh for each list, as the Kāra arm does.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `2f62c55005`
on LLVM 22. karac builds for the x86-64-v3 baseline, so the C and
overflow-checked Rust programs are also built at `-march=x86-64-v3`:

| | time | median |
|---|---|---|
| Rust (`rustc -O`) | 0.889 to 1.083 s | 0.922 s |
| C (`clang -O3`) | 0.876 to 1.113 s | 0.931 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.919 to 1.042 s | 0.936 s |
| Kāra (`karac build`) | 0.926 to 1.100 s | 0.980 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.891 to 1.251 s | 0.986 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.933 to 1.168 s | 1.013 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.957 to 1.169 s | 1.045 s |
| Go | 0.989 to 1.250 s | 1.079 s |
| Python | 1.93 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time (0.96 s) is its real time, and the 3% between the two Kāra
rows is within their spread.

The work is 10 million items grouped, about 1.1 million small vectors
cloned and sorted, and as many answers allocated. Every compiled
language is within 17% of every other: Kāra is 3% behind Rust with
overflow checks at the same ISA, 10% behind plain `rustc -O` and 6%
ahead of Go. C's `qsort` calls its comparator through a pointer for
every comparison, which is likely why C is level with the rest rather
than ahead. Python takes 1.9x Kāra, probably this close because its
dictionary and `sorted` run in C.
