# 1353. Maximum Number of Events That Can Be Attended

You are given an array of `events` where `events[i] = [startDayi,
endDayi]`. Every event `i` starts at `startDayi` and ends at `endDayi`.

You can attend an event `i` at any day `d` where `startDayi <= d <=
endDayi`. You can only attend one event at any time `d`.

Return the maximum number of events you can attend.

```
events = [[1,2],[2,3],[3,4]]          ->  3
events = [[1,2],[2,3],[3,4],[1,2]]    ->  4
```

**Constraints:** `1 <= events.length <= 10^5`, `events[i].length == 2`,
`1 <= startDayi <= endDayi <= 10^5`.

Each arm is `fn max_events(events: Vec[Vec[i32]]) -> i32`.

## Approaches

| file | mechanism |
|---|---|
| `max_events.kara` ★ | a sweep over the days with a `PriorityQueue` of the open events' last days, smallest first. Each day the events starting then join the queue, the ones already over leave it, and the open event ending soonest is attended; attending the most urgent event never costs a later one. A day with nothing open jumps to the next start. O(n log n + D) over D days |
| `max_events_dsu.kara` | the events by last day, each given the first free day from its start, if that day is not past its end. A taken day points on to the next, so a lookup skips every taken day at once (path halving). O(n log n + D α(D)) |
| `max_events_sorted.kara` | every day up to the last end in a `SortedSet` of free days; the events by last day, each taking the first free day of its span, found by `range_inclusive`, and removing it. O(D log D + n log n) |
| `max_events_tree.kara` | a segment tree over the days, each node how many of its days are still free; the events by last day, each taking the first free day at or after its start, found by walking down the tree, if that day is not past its end. Its leaves are the days from 0 to the last end, rounded up to a power of two. O(D + n log D) |
| `max_events_solution.kara` | a Rust solution as LeetCode's Rust users write it (`events.sort_unstable()`, a `BinaryHeap` of `Reverse(end)`, a loop over `1..=last_day`, and the expired ends dropped by the let-chain `while let Some(&Reverse(end)) = heap.peek() && end < day`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 2 lines: LeetCode's two examples, one event,
three events of the same one day, and 10^5 events, the constraints'
most, all on day 10^5, all over the whole 10^5 days, and at random,
lasting up to 50 days (`3 4 1 1 1 100000 32811`); and 2000 random sets
of 1 to 300 events, most of them few, crowded into 10 days or spread
over 1000, lasting up to 1, 5 or 100 days (`2000 random sets: 18803
events attended in all, checksum 815000826`). `max_events.py` mirrors
the ★ arm, and its output is byte-identical. Every arm gives the same
output under `karac __mir-run`, `karac run` and `karac __mir-llvm-run`.

The Mend loop: the ★, union-find, sorted and tree arms check clean. The
Rust solution takes one round of 20 fixes by `karac fix`'s count: the
two `use` lines go, since Kāra's `PriorityQueue` is in the prelude and
pops the smallest first, so `Reverse` goes from the push too; `struct
Solution;` becomes `struct Solution {}`; `mut events: Vec<Vec<i32>>`
becomes `events: own Vec[Vec[i32]]` and a `let mut events = events;`;
`sort_unstable()` becomes `sort()`, `BinaryHeap::new()`
`PriorityQueue.new()`, and each `&&` `and`. The let-chain is the
interesting one: Kāra has no let-chains, and `karac check` says that a
`while let` cannot be joined with `and` (E0001); `karac fix` matches
`heap.peek().cloned()`, the copy that Rust's `&` pattern asked for, and
moves the rest of the condition into a guard that leaves the loop, `if
not (end < day) { break; }`. Until B-2026-11-21-71 (fixed), the
scrutinee parsed as `heap.peek() and end < day`, and the checker
reported a `bool` operand error and a pattern mismatch instead of
naming the let-chain. Every arm matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every way of giving each event one free day of its span or
none, the most events kept. 2000 sets of 1 to 6 events in four kinds,
500 each: starting on day 1 to 3 and lasting up to 2 days, crowded; each
a single day from 1 to 6; starting on day 1 to 6 and lasting up to 6
days; and every event from day 1 to 1, 2 or 3, all the same choice.
Every set is drawn before any arm answers.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the events in the opposite order: the same answer |
| P3 | every day 1000 later: the same answer |
| P4 | time run backwards, each day d made the last end + 1 - d: the same answer |
| P5 | the first event held twice: the same answer or one more |
| P6 | the ★ arm's answer |

All 60,000 checks pass on every arm: `2000 sets: checksum 968607295,
60000 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run` and `karac __mir-llvm-run`. Python, matching events to days by
Kuhn's augmenting paths, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash, and no two
fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: an event already over attended | P1 845, P6 3380 |
| M2 | ★: the open event ending last attended | P1 318, P4 322, P6 1272 |
| M3 | union-find: a lookup stopped after one hop | P1 1, P2 1, P4 1, P6 1 |
| M4 | union-find: every day left in a taken event marked | P1 405, P6 405 |
| M5 | sorted: an event's last day never offered | P1 1581, P6 1581 |
| M6 | sorted: the events taken by first day | P1 173, P2 239, P4 194, P5 59, P6 173 |
| M7 | tree: the later half searched first | P1 1533, P2 35, P3 703, P4 380, P6 1533 |
| M8 | tree: a day past the event's end taken | P1 500, P3 465, P4 116, P6 500 |
| M9 | solution: the last day never used | P1 1353, P4 165, P6 1353 |
| M10 | solution: the events never sorted | P1 930, P2 826, P4 1132, P6 930 |

P1 and P6 kill all ten, P4 seven, P2 four, P3 two and P5 one. Running
time backwards (P4) turns every event's start into an end, and catches
the edits that favour one end of the calendar: the latest end first
(M2), the later half (M7), a day past the end (M8), the last day (M9),
and the edits that take the events in the wrong order (M6, M10). The
opposite order (P2) catches the edits whose answer depends on the order
the events come in: the unsorted solution (M10) wholly, the sort by
first day (M6), which leaves events with the same start in their given
order, and the one-hop lookup (M3) and the later half (M7), whose wrong
day depends on which of two events with the same last day goes first.
Moving every day 1000
later (P3) changes only the tree, whose leaves start at day 0 and whose
size is rounded up to a power of two, so it catches only the tree's two
edits. A second copy of the first event (P5) may add at most one event,
and only the edit that orders by first day (M6) answers outside that
range. The edits
that are wrong on every calendar, an event attended after it ends (M1),
a whole event's days taken (M4) and its last day never offered (M5),
show only against the literal answer. The weakest edit, a lookup that
stops after one hop (M3), moves two pointers on and so returns a taken
day only when the free day lies three or more pointers away, which path
halving rarely leaves; that happens in 1 of the 2000 sets.

## Benchmarks

The bench builds 20 sets of 10^4 events, starting on day 1 to 10^4 and
lasting 1 to 30 days, once; then makes 600 rounds, each moving one event
of one set to a start and length drawn from the checksum so far, so no
answer carries over, and answering that set with the ★ arm's sweep,
folding each answer plus the round into the checksum. Every
implementation prints `600 rounds over 20 sets of 10^4 events: checksum
188259283`. The C sort is `qsort` with a comparison function.

BENCHTAB
