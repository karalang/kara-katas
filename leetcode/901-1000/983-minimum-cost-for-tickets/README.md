# 983. Minimum Cost For Tickets

You have planned some train traveling one year in advance. The days of
the year in which you will travel are given as an integer array `days`.
Each day is an integer from 1 to 365.

Train tickets are sold in three different ways:

- a 1-day pass is sold for `costs[0]` dollars,
- a 7-day pass is sold for `costs[1]` dollars, and
- a 30-day pass is sold for `costs[2]` dollars.

The passes allow that many days of consecutive travel. For example, if
we get a 7-day pass on day 2, then we can travel for 7 days: 2, 3, 4,
5, 6, 7, and 8.

Return the minimum number of dollars you need to travel every day in
the given list of days.

```
days = [1,4,6,7,8,20], costs = [2,7,15]                ->  11
days = [1,2,3,4,5,6,7,8,9,10,30,31], costs = [2,7,15]  ->  17
```

**Constraints:** `1 <= days.length <= 365`; `1 <= days[i] <= 365`;
`days` is strictly increasing; `costs.length == 3`;
`1 <= costs[i] <= 1000`.

## Approaches

| file | mechanism |
|---|---|
| `mincost_tickets.kara` ★ | a table over the calendar: best[d] is the least that covers every travel day up to day d; a day with no travel costs what the day before did, and a travel day is covered by a pass ending on it, bought on top of the best 1, 7 or 30 days earlier. O(last day) |
| `mincost_tickets_windows.kara` | a table over the travel days with two trailing pointers: best[i] covers the first i travel days, and the i-th is covered by a day pass on top of best[i - 1] or by a 7- or 30-day pass reaching back to the first travel day each pointer marks; the pointers only move forward. O(n) |
| `mincost_tickets_memo.kara` | forward choices, memoised: from the i-th travel day on, buy some pass on that day, then the cheapest plan from the first travel day it does not cover, found by binary search. O(n log n) |
| `mincost_tickets_dijkstra.kara` | shortest path: place i means "the first i travel days are covered", a pass bought on travel day i is an edge to the first place it does not reach, weighted by its price, and a smallest-first `PriorityQueue` finds the cheapest path from place 0 to place n. O(n log n) |
| `mincost_tickets_deque.kara` | two queues of live passes: each travel day offers a 7-day and a 30-day pass bought on it, at the cost so far plus its price; passes run out from the front of their `VecDeque`, and since the cost so far never falls the front is also the cheapest, so each day costs the least of a day pass and the two fronts. O(n) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 13 lines. The first ten are LeetCode's two
examples and eight more: one day (2); day 365 alone, with a week pass
cheaper than a day pass (4); a week pass cheapest for three days in one
week (2); a month pass cheapest of all (1); four days a week apart,
where one month pass beats four week passes (9); three days 30 apart,
each needing its own pass (15); and the whole year at LeetCode's
example prices (187) and with a month pass at 1 (13). Then totals and
checksums over random plans: 300 of up to 12 days within 40 (cost
3,583), 3,000 of up to 60 days within the year (924,118), and four of
up to LeetCode's 365 days (29,994), at prices up to 20, 100 and 1,000.
`mincost_tickets.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every plan that buys, on each travel day, nothing (if a pass
already covers it) or one of the three passes, keeping those that cover
every travel day, and the least total price among them. A pass that
starts on a day with no travel could start on the next travel day and
cover no less, so these plans include a cheapest one. It checks 3,200
plans: 3,000 of 1 to 7 days against the statement, and 200 of up to 365
days against the other properties. The days fall within 10, 40, 120 or
365 days by turns, and the prices run up to 10 or up to 1,000 by turns.

| | property |
|---|---|
| P1 | the statement's answer, on the first 3,000 plans |
| P2 | only the gaps between the days matter: every day moved by the same random amount, within the year, gives the same cost |
| P3 | the bounds: never less than the cheapest pass, never more than a day pass for every day, or the fewest week passes or month passes laid greedily from the first uncovered day |
| P4 | every price tripled triples the cost, and one price raised by a random amount never lowers it |
| P5 | the plan again, 30 or more days after its last day when the year has room, costs exactly twice as much, since no pass reaches from one copy to the other |
| P6 | each arm agrees with at least two of the other four |

It prints `3200 plans of 49222 days: cost 1330146, checksum 965620267,
95000 checks over 5 arms: 0 failures` under `karac __mir-run` (16.0 s)
and `karac __mir-llvm-run`, and the same under `karac __mir-llvm-asan`
with no error.

## Mutation testing

Twenty-six edits to the differential, each run under `karac
__mir-run` and `karac __mir-llvm-run`; fifteen are kept, three to each
arm, all fifteen are killed, and each fails the same checks under both.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the week pass one day short | P1 75, P3 93, P6 104 |
| M2 | ★: the month pass one day long | P1 45, P5 40, P6 114 |
| M3 | ★: a day pass priced as a week pass | P1 668, P3 545, P6 684 |
| M4 | windows: the week pass one day long | P1 101, P6 139 |
| M5 | windows: the month pass one day short | P1 56, P3 98, P6 135 |
| M6 | windows: the week pass priced as a month pass | P1 878, P3 805, P6 933 |
| M7 | memo: every pass covers one day more | P1 244, P5 40, P6 345 |
| M8 | memo: the dearest choice kept | P1 2993, P3 3193, P6 3193 |
| M9 | memo: one too many remembered | P1 1204, P3 1151, P4 1399, P5 1997, P6 1399 |
| M10 | dijkstra: only the last pass's price counted | P1 2038, P5 2468, P6 2236 |
| M11 | dijkstra: day and month prices swapped | P1 1759, P3 929, P6 1927 |
| M12 | dijkstra: every pass one cheaper | P1 3000, P3 1234, P4 3200, P6 3200 |
| M13 | deque: the week pass priced as a day pass | P1 1131, P3 739, P6 1207 |
| M14 | deque: the month pass never bought | P1 1635, P3 1670, P6 1809 |
| M15 | deque: the newest month pass at the front | P1 1426, P3 1460, P6 1599 |

P1 and P6 kill all fifteen, P3 eleven (all but M2, M4, M7 and M10), P5
four (M2, M7, M9, M10), P4 two (M9 and M12) and P2 none. P4 sees only
an edit that adds or takes away a fixed amount, which tripling the
prices does not triple: M9 remembers one more than it found and M12
charges one less per pass. P2 guards against an arm that leans on the
calendar's absolute days; none of these edits does, since every arm
reads the days only through their differences, or, in ★, through a
table indexed from day 1 whose early entries are all zero. A pass one
day too long (M2, M7) fails P5 only when the second copy starts exactly
30 days after the first ends, so that the longer pass bridges them.

Eleven other edits were tried and set aside. Five failed exactly the
same checks as a kept one: memo's month pass one day short, as M5;
dijkstra's pass covering one day more, as M7; dijkstra's week pass one
day short, as M1; deque's week pass one day long, as M4; and deque's
month pass one day short, as M5. Four were sound but beyond three an
arm: ★ charging a day pass on a day with no travel; ★ never buying a
month pass (deque's M14 fails the same checks, and is kept there since
★'s was not); windows' month pass leaving its first day out; dijkstra
stopping one place early. One survived and is equivalent: dijkstra
scanning for a pass's reach from place 0 rather than from its own
place, which finds the same place since the days are in order. One ran
past the harness's 200-second limit in both lanes: dijkstra settling a
place again each time it leaves the queue. It still gives the right
answers, the ten examples included, but each extra visit pushes its
passes again, and on the larger plans the queue grows faster than it
drains.

## Verification

Every arm prints the same output as `mincost_tickets.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `395f71ae05`, the runtime
archives rebuilt at `d867340a02`, whose runtime sources are the same.
Under `karac __mir-run` the arms take 0.8 s (windows) to 2.8 s
(dijkstra), the ★ arm 1.0 s, and the differential 16.0 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The legacy compiler was removed from kara at M3, so there is no legacy
lane.

The deque arm was first written with `*s + 7 > d` and `.min(*w)`, after
`while let Some((s, _)) = weeks.front()` and
`let (_, w) = weeks.front().unwrap()`. `karac check` refused only the
`*w`, saying a copied `i64` takes no `*`, and accepted the `*s`; the MIR
front ends accepted both. Over a borrowed scrutinee a `Copy` part binds
by copy, so neither `*` belongs, and the arm writes neither; the
disagreement is kara's `B-2026-10-24-36`.

## Benchmarks

The bench runs the ★ arm in all five languages. The program makes 1,000
random plans once, each of up to 365 days within the year at prices up
to 1,000, LeetCode's largest. In each of 300 rounds it runs the arm on
every plan, each round starting from a different one, and folds every
cost into a checksum. Every implementation prints `300 rounds over 1000
plans of up to 365 days: cost 1469862600, checksum 310984814`. Each call
allocates a table of up to 366 costs and a flag for every day of the
year, and fills the table day by day.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python, with karac at `395f71ae05`:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.460 to 0.525 s | 0.500 s |
| Rust (`rustc -O`) | 0.524 to 0.604 s | 0.573 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.546 to 0.624 s | 0.559 s |
| Go | 0.760 to 0.826 s | 0.809 s |
| Python | 15.5 s | |
| Kāra (`karac build --mir`) | 0.587 to 0.684 s | 0.645 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Python's run is about 24 times
Kāra's.

v2 took 1.15 times Rust's median time under overflow checks and 1.29
times C's. Under valgrind's cachegrind v2 ran 5,057 million
instructions and 2,203 million branches with 35.9 million mispredicted,
Rust with overflow checks 3,775 million, 1,514 million and 36.0 million,
and C 2,983 million, 1,195 million and 36.6 million. All three
mispredict about 36 million times, one for every three of the at most 110
million days the rounds walk, which fits the branch on whether a day
has travel, taken at random in most plans (inferred). v2 runs
34% more instructions than Rust and 46% more branches; it checks every
index and every addition, as Rust with overflow checks does, so where
the extra branches come from is not traced here.
