# 2251. Number of Flowers in Full Bloom

You are given a **0-indexed** 2D integer array `flowers`, where
`flowers[i] = [start_i, end_i]` means the `i`th flower will be in **full
bloom** from `start_i` to `end_i` (**inclusive**). You are also given a
**0-indexed** integer array `people` of size `n`, where `people[i]` is
the time that the `i`th person will arrive to see the flowers.

Return *an integer array* `answer` *of size* `n`*, where* `answer[i]`
*is the **number** of flowers that are in full bloom when the* `i`*th
person arrives.*

```
flowers = [[1,6],[3,7],[9,12],[4,13]], people = [2,3,7,11]  ->  [1,2,2,2]
flowers = [[1,10],[3,3]], people = [3,3,2]                  ->  [2,2,1]
```

**Constraints:** `1 <= flowers.length <= 5 * 10^4`;
`flowers[i].length == 2`; `1 <= start_i <= end_i <= 10^9`;
`1 <= people.length <= 5 * 10^4`; `1 <= people[i] <= 10^9`.

A flower is in bloom at `t` exactly when its start is at most `t` and
its end is not before `t`. No flower ends before it starts, so every
flower over before `t` has also begun, and the count at `t` is the
starts of at most `t` less the ends before `t`: two searches in the
sorted starts and the sorted ends. O((f + p) log f).

## Approaches

| file | mechanism |
|---|---|
| `flowers.kara` ★ | the starts and the ends collected and sorted once; each person `starts.partition_point(\|s\| s <= t) - ends.partition_point(\|e\| e < t)` |
| `flowers_sweep.kara` | offline, no search: the people's indices sorted by `sort_by_key(\|i\| people[i])`, and two pointers that only move forward over the sorted starts and ends; their difference written back to the person's own place |
| `flowers_diff.kara` | a difference map: a `SortedMap[i64, i64]` of +1 on each first day and -1 on the day after each last, through `*change.entry(d).or_insert(0) += ..`; walked in key order into the days the count changes and the count from each, and a person's count the one from the last such day not after theirs, by `partition_point` |
| `flowers_struct.kara` | a `struct Garden` of the sorted starts and ends, built by `Garden.plant`, whose `in_bloom` (`ref self`) is the starts of at most `t` less the ends of at most `t - 1`, each counted by `at_most`, a binary search written out by hand |
| `flowers_iter.kara` | iterator chains over one sorted list of events: starts as `(day, 0, 0)`, people as `(day, 1, index)` by `enumerate`, ends as `(day, 2, 0)`, joined by `chain`, so on one day the starts come before the people and the ends after them; a `scan` threads the number open and yields each person's index and count, `filter_map` keeps those, and the pairs sorted by index give the answers |
| `flowers_solution.kara` | LeetCode's Rust template: `Vec<Vec<i32>>` and `Vec<i32>` in, `Vec<i32>` out; the flowers sorted, the people's indices by `sort_unstable_by_key`, and a `BinaryHeap` of `Reverse(end)` pushed as flowers begin and popped while the earliest end is before `t`; each person answered by `heap.len()`; carried by `karac fix` in one round |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's two examples and four
more (people on a flower's first and last day and either side of it,
one flower over every day, one flower three times, and flowers of one
day each), each with its counts; then the total over 2000 cases of 1 to
8 flowers and 1 to 8 people with days 1 to 10, with a checksum of the
counts; then the constraints' largest, 5 * 10^4 flowers and 5 * 10^4
people with days up to 10^9. `flowers.py` mirrors the ★ arm and its
output is byte-identical.

`karac fix` carries the template in one round of 41 edits. Besides
`Vec<..>` to `Vec[..]`, `vec![0; n]` to `Vec.filled`, `usize` to `i64`,
`&&` to `and`, `sort_unstable` and `sort_unstable_by_key` to `sort` and
`sort_by_key`, the `&` patterns dropped from the closures, `struct
Solution;` to `struct Solution {}` and `Solution::` to `Solution.`, it
turns the max-first `BinaryHeap` of `Reverse(end)` into Kāra's
`PriorityQueue.new()`, which pops the smallest first: `Reverse(..)` is
dropped from the push, `while let Some(&Reverse(e)) = heap.peek()`
becomes `while let Some(e) = heap.peek().cloned()`, and the two `use`
lines go with it. It also marks `flowers` `own`, since the template
moves it into a `let mut`.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: for every person every flower tried, counted when `start <= t
<= end`; no sorting or searching. It checks 300 random cases of 1 to 8
flowers and 1 to 8 people with days 1 to 10; then 30 with days up to
5 * 10^8, so that moved they stay in bounds; then 30 whose people stand
on a flower's first or last day or the day either side of it. All 360
are drawn before any arm answers.

| | property |
|---|---|
| P1 | each count is the flowers in bloom on the person's day, read literally |
| P2 | the flowers and the people both reversed: the counts reversed |
| P3 | a flower from day 1 to day 10^9 added: every count one more |
| P4 | every day moved 7 later: the same counts |
| P5 | every flower of more than one day split in two at its middle: the same counts |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 cases: checksum 838356727, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading through the
complement: all the flowers, less those not yet begun, less those
already over. On a failure it prints the first ten and then the count
by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed and fails the same way
under both backends and not by a crash. The thirty-one fall into
fifteen ways of failing, all fifteen among the kept ones; no two kept
ones in the same arm fail the same checks, and two pairs across arms do
(M2 and M29, M4 and M26).

| # | mutation | failures by property |
|---|---|---|
| M2 | ★: a person on a flower's last day not counted | P1 221, P5 210, P6 221 |
| M3 | ★: the ends not sorted | P1 206, P2 207, P3 67, P5 216, P6 206 |
| M4 | ★: the subtraction the other way round | P1 338, P3 360, P6 338 |
| M7 | sweep: the people not sorted | P1 218, P2 224, P6 218 |
| M10 | sweep: the ends left out | P1 284, P5 313, P6 284 |
| M11 | sweep: the ends taken from the starts | P1 316, P3 350, P5 202, P6 316 |
| M13 | diff: the -1 two days after the last | P1 207, P5 202, P6 207 |
| M15 | diff: the count from the next day of change | P1 338, P3 144, P5 174, P6 338 |
| M16 | diff: each day's change taken as the count | P1 308, P3 335, P5 150, P6 308 |
| M17 | struct: the search counting below `x` | P1 278, P3 114, P6 278 |
| M19 | struct: the ends not sorted | P1 207, P2 206, P3 67, P5 221, P6 207 |
| M20 | struct: the starts given the ends | P1 321, P3 360, P5 210, P6 321 |
| M23 | iter: each start a day late | P1 236, P3 114, P5 202, P6 236 |
| M24 | iter: the pairs not sorted by index | P1 218, P2 237, P6 218 |
| M26 | iter: the state never moved on | P1 338, P3 360, P6 338 |
| M27 | solution: the flowers not sorted | P1 209, P2 194, P3 289, P5 152, P6 209 |
| M29 | solution: a flower ending on `t` popped | P1 221, P5 210, P6 221 |

P1 and P6 kill all seventeen, P5 twelve, P3 eleven, P2 five, and P4
none. P5 splits each flower at its middle, which makes a new first and
last day inside it, so it catches every edit that is wrong at a
flower's edge. P3's flower over every day begins first and ends last,
so it catches the edits that miscount a flower by where its start or
end falls among the others, and misses those whose error it leaves as
it was: an edge day missed, the people's order lost, the ends dropped. P2 reverses both lists, and catches only the edits that leave
something unsorted. No edit here depends on where the days lie, so
moving them all (P4) kills none; it stays as a property of the
problem, for an edit that would.

Of the thirty-one, fourteen were not kept, and none survives, crashes
or differs between the backends. Each fails as a kept one does: a
person on a flower's first day not counted in the ★, sweep, struct and
template arms (M1, M8, M21, M28) as the iter arm's late start (M23); on
a flower's last day in the sweep, diff, struct and iter arms (M9, M12,
M18, M22) as the ★ arm's (M2); the ★ arm's starts taken from the ends
(M5) as the struct arm's (M20); the ★ arm's ends searched in the starts
and the template's start pushed for its end (M6, M31) as the sweep's
ends taken from the starts (M11); the template's people not sorted
(M30) as the sweep's (M7); the iter arm's end adding one (M25) as the
sweep's ends left out (M10); and the diff arm's search of the days
before `t` (M14) as the struct arm's search below `x` (M17).

## Verification

Every arm prints the same output as `flowers.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the sweep arm takes 0.7 s, the struct arm 0.9
s, the ★ arm 1.7 s, the iter arm 1.7 s, the template 2.1 s, the diff
arm 6.7 s, and the differential 1.0 s. The diff arm's time is the
`SortedMap` of up to 10^5 days built entry by entry.

## Benchmarks

The bench answers 20 cases of 5 * 10^4 flowers and 5 * 10^4 people with
the ★ arm in all five languages, days from 1 to 10^9. Every
implementation prints `20 cases of 5 * 10^4 flowers and people:
checksum 774958920`.

BENCHTAB
