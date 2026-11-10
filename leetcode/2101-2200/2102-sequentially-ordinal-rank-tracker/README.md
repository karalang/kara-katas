# 2102. Sequentially Ordinal Rank Tracker

A scenic location is represented by its `name` and attractiveness
`score`, where `name` is a unique string among all locations and `score`
is an integer. Locations can be ranked from the best to the worst. The
higher the score, the better the location. If the scores of two
locations are equal, then the location with the lexicographically
smaller name is better.

You are building a system that tracks the ranking of locations with the
system initially starting with no locations. It supports:

- adding scenic locations, one at a time;
- querying the `i`th best location of all locations already added,
  where `i` is the number of times the system has been queried
  (including the current query).

Implement the `SORTracker` class: `SORTracker()` initializes the
tracker; `void add(string name, int score)` adds a scenic location;
`string get()` queries and returns the `i`th best location.

```
add("bradford", 2), add("branford", 3), get()  ->  "branford"
add("alps", 2), get()                          ->  "alps"
add("orland", 2), get()                        ->  "bradford"
add("orlando", 3), get()                       ->  "bradford"
add("alpine", 2), get()                        ->  "bradford"
get()                                          ->  "orland"
```

**Constraints:** `name` consists of lowercase English letters and is
unique among all locations; `1 <= name.length <= 10`; `1 <= score <=
10^5`; at any time, the number of calls to `get` does not exceed the
number of calls to `add`; at most `4 * 10^4` calls in total.

The `i`th `get` asks for the `i`th best place among those added so far,
so a better place added later pushes the answer down: in the example,
the third `get` returns `bradford`, and so do the next two, because
`orlando` and `alpine` each land above it. The places handed out so far
are always the best ones, and each `get` hands out the best of the rest.

## Approaches

| file | mechanism |
|---|---|
| `rank_tracker.kara` ★ | a `struct Place` with hand-written `PartialEq`, `Eq`, `PartialOrd` and `Ord` (greater is better: the higher score, then the smaller name), and two `PriorityQueue`s: the places handed out in a smallest-first one, its worst on top, and the rest in a `max_first` one, its best on top. An `add` goes through the first and its worst moves to the second; a `get` moves the second's best across. O(log n) a call |
| `rank_tracker_tuples.kara` | the same two heaps over `(-score, name)` tuples, whose natural order puts the better place first, so no `Ord` is written: the handed-out places in a `max_first` queue, the rest smallest first |
| `rank_tracker_sorted.kara` | one `Vec` of `(-score, name)` kept in order: an `add` finds its slot with `partition_point` and `insert`s, and the `i`th `get` reads index `i - 1`. O(n) an add, O(1) a get |
| `rank_tracker_fenwick.kara` | a sparse Fenwick tree in a `Map` counting places by rank `100001 - score`, each rank's names sorted in a `Vec`; the `i`th `get` walks the tree down by powers of two to the rank holding the `i`th place and reads the name left over. O(log^2 n) a call plus the bucket's insert |
| `rank_tracker_sets.kara` | two `SortedSet[(i64, String)]`: an `add` inserts into the handed-out set and moves its worst out with `pop_last`; a `get` moves the other set's best in with `pop_first` |
| `rank_tracker_solution.kara` | LeetCode's Rust template, two `BinaryHeap`s of `(Reverse(score), name)` and `(score, Reverse(name))`, as `karac fix` leaves it; it does not check (Verification) and is not in the differential |
| `differential.kara` | the five Kāra arms against the statement read literally, six properties |

Every arm drives its tracker through one function, `answers(ops)`, an
`op` being a name and a score, or an empty name for a `get`. Every Kāra
arm prints the same 6 lines: LeetCode's example and three more (three
places tied on score, so names alone decide; a better place added after
each `get`; one place only), each with its answers; then how many gets
3000 random runs of 1 to 30 calls make (names of 1 to 3 letters from a
to d with scores of 1 to 3, so that ties are common, or names of 1 to 10
letters with scores up to 10^5) and a checksum of the names returned;
then the constraints' largest, 4 * 10^4 calls, 20000 adds of scores
that rise and fall in waves each followed by a `get`. `rank_tracker.py`
mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five Kāra arms and the
statement read literally: at the `i`th `get`, every place added so far
sorted, best first, and the one at index `i - 1` taken. It checks 300
random runs of 1 to 20 calls with names of 1 to 3 letters from a to d
and scores of 1 to 3; then 20 runs where every score is the same; then
20 runs with names of 1 to 10 letters and scores up to 10^5; a `get`
only when there are more adds than gets so far. All 340 are drawn before
any arm answers.

| | property |
|---|---|
| P1 | the answers are the statement read literally |
| P2 | at the `i`th `get`, exactly `i - 1` of the places added so far are better than the one returned, counted without sorting |
| P3 | every score replaced by its rank among the run's scores: the same answers |
| P4 | the adds first and the gets after them: the best places, best first, as many as there were gets |
| P5 | a place worse than all others (`zzzzzzzzzz`, score 1) added first: the same answers |
| P6 | each arm agrees with at least two of the other four |

The changed runs stay within the constraints. The differential prints
`340 runs: checksum 363245561, 10200 checks over 5 arms: 0 failures`
under every lane in Verification; the checksum of the literal answers
was checked against a Python reading of the same runs. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Thirty-six edits to the differential, six to nine to each arm; the
last seven were added after the first twenty-nine, for the arms whose
signatures those crowded. Each was run under `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, four to each of the ★ and sorted
arms and three to each of the others. Each kept one is killed, fails the
same way under both backends and not by a crash, and no two kept ones
fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: names ranked the way scores are | P1 234, P2 234, P4 260, P5 147, P6 234 |
| M2 | ★: scores ranked by their last digit | P1 14, P2 14, P3 14, P4 17, P5 4, P6 14 |
| M3 | ★: the served heap largest first | P1 250, P2 250, P6 250 |
| M4 | ★: the new place sent straight to the waiting | P1 210, P2 210, P6 210 |
| M5 | tuples: the key put back negated | P1 200, P2 200, P5 180, P6 200 |
| M6 | tuples: scores halved | P1 119, P2 119, P3 21, P4 177, P6 119 |
| M7 | tuples: scores capped at 50000 | P1 7, P2 7, P3 7, P4 14, P6 7 |
| M8 | sorted: the slot found among the worse | P1 277, P2 277, P4 302, P5 308, P6 277 |
| M9 | sorted: the new place put at the end | P1 257, P2 257, P4 283, P5 308, P6 257 |
| M10 | sorted: the first get read twice | P1 270, P2 270, P4 270, P6 270 |
| M11 | sorted: each get one place too far, stopping at the last | P1 255, P2 255, P4 302, P5 228, P6 255 |
| M12 | fenwick: the rank the score itself | P1 250, P2 250, P4 279, P5 275, P6 250 |
| M13 | fenwick: a bucket's names unsorted | P1 186, P2 186, P4 222, P5 147, P6 186 |
| M14 | fenwick: ranks of ten scores shared | P1 202, P2 202, P3 16, P4 230, P6 202 |
| M15 | sets: the worst waiting served | P1 255, P2 255, P4 302, P5 308, P6 255 |
| M16 | sets: a score of 1 ranked first | P1 207, P2 207, P3 36, P4 232, P5 275, P6 207 |
| M17 | sets: a score of 2 ranked as 3 | P1 119, P2 119, P3 16, P4 177, P6 119 |

P1, P2 and P6 kill all seventeen, P4 fourteen, P5 ten and P3 six. P4
misses the edits that only go wrong once a place has been handed out or
moved twice (M3, M4, M5): with every add first, each place passes
through the heaps once before any `get`. P3 sees only the edits that
look at a score's size rather than its order (M2, M6, M7, M14, M16,
M17), since ranking keeps every order and changes every size. P5 misses
the edits whose damage stays above the worst place, and sees the
reversed or misplaced orders that can bring the worst place forward.

Of the thirty-six, nineteen were not kept. Fourteen fail as a kept one:
a lower score ranked better (★) and the score not negated (tuples,
sorted, sets) as M12; the tuples arm's served queue smallest first and
the sets arm's best served moved back as M3; the ★ arm's served place
not kept, the tuples arm's new place sent straight to the waiting and
the sets arm's served place not kept as M4; the sorted arm's scores by
their last digit as M2; the sorted arm's gets read from the end as M8;
the sets arm's scores halved as M6; the fenwick arm's names in reverse
as M1; the sets arm's scores under 10 ranked together as M14. Four
crash and are not kept, all in the fenwick arm: the walk starting from
2^10, the tree climbed one by one, a count equal to what is left
stepped over, and the walk's last step skipped, each reading a rank
that holds no names. One survives: the fenwick arm's scores over 99000
ranked together, since none of the 20 wide runs draws two such scores
(a score above 99000 is 1 in 100). It names a blind spot of the wide
runs rather than an equivalent edit.

## Verification

Every Kāra arm prints the same output as `rank_tracker.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
Kāra arm and the differential. `karac check --output=json` reports
nothing on any of them.

Under `karac __mir-run` the arms take 1.6 s to 3.7 s, and the
differential 1.6 s (timed while other work shared the machine).

The harness met a gap. It lists its example runs as `let examples:
Vec[Vec[(String, i64)]] = [a.collect(), b.collect(), ..].to_vec();`. A
bare `collect()` names no type of its own, and the `let` names it
through `to_vec`, whose receiver the checker then refines; the
refinement reached the elements' types but not the `collect` calls'
own type argument, and `karac check` stopped at "the method call
`.collect` with no resolved callee is not lowered yet". It now reaches
the calls too. Fixed in kara COLLECTSHA, test
`tests/kata_2102_to_vec_of_collects.rs`.

The Rust template does not carry. `karac fix` takes it in three rounds
of 22, 1 and 4 edits (Rust's spellings, `&mut self` to `mut ref self`,
the two `use` lines deleted, `BinaryHeap` to `PriorityQueue` with
`max_first()`, which keeps Rust's largest-first order), and then stops
at seven uses of `Reverse`. Kāra has no `Reverse`; the fix that drops it
covers a heap whose whole item is reversed, which becomes a
smallest-first queue. Here only one part of a tuple is reversed, a
score in one heap and a name in the other, and no edit of the tuple
keeps that order: a score could be negated, but a `String` cannot. The
Kāra spellings are a hand-written `Ord`, as the ★ arm has, or a
negated score with the name left alone, as the tuples arm has. Filed as
REVROW. The arm stays as the fix left it.

## Benchmarks

The bench runs 20 runs of 4 * 10^4 calls, the constraints' largest,
each 20000 adds of unique names of 1 to 10 letters with scores up to
10^5 and 20000 gets, with the ★ arm in all five languages: two heaps of
places ordered by score and then name (`PriorityQueue` of a `Place` with
its own `Ord`, `BinaryHeap` with `Reverse`, index heaps in C,
`container/heap` in Go, `heapq` in Python). Every implementation prints
`20 runs: 400000 gets, checksum 630654706`.

BENCHTAB
