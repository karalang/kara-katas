# 911. Online Election

You are given two integer arrays `persons` and `times`. In an election,
the `i`th vote was cast for `persons[i]` at time `times[i]`.

For each query at a time `t`, find the person that was leading the
election at time `t`. Votes cast at time `t` will count towards our
query. In the case of a tie, the most recent vote (among tied
candidates) wins.

Implement the `TopVotedCandidate` class:

- `TopVotedCandidate(int[] persons, int[] times)` Initializes the object
  with the `persons` and `times` arrays.
- `int q(int t)` Returns the number of the person that was leading the
  election at time `t` according to the mentioned rules.

```
persons = [0,1,1,0,0,1,0], times = [0,5,10,15,20,25,30]
q(3) -> 0, q(12) -> 1, q(25) -> 1, q(15) -> 0, q(24) -> 0, q(8) -> 1
```

At time 3 the votes are [0] and 0 leads; at 12 they are [0,1,1] and 1
leads; at 25, [0,1,1,0,0,1], a tie that 1 wins as the most recent vote.

**Constraints:** `1 <= persons.length <= 5000`,
`times.length == persons.length`, `0 <= persons[i] < persons.length`,
`0 <= times[i] <= 10^9`, `times` is sorted in strictly increasing order,
`times[0] <= t <= 10^9`, and at most `10^4` calls are made to `q`.

## Approaches

| file | mechanism |
|---|---|
| `top_voted_candidate.kara` ★ | the leader after every vote: the votes counted in order, a candidate whose count reaches the leader's taking the lead (a tie goes to the most recent vote), the leader stored after each vote; a query binary-searches the times for the last vote at or before t. O(n) to build, O(log n) a query |
| `top_voted_candidate_changes.kara` | only the changes of leader kept: a (time, leader) pair recorded when the lead changes hands, and a query binary-searches the changes, which can be far fewer than the votes. O(log c) a query for c changes |
| `top_voted_candidate_map.kara` | a `SortedMap` from each vote's time to the leader after it; a query takes the last entry of the map's range from the first time to t. O(n log n) to build, O(log n) a query |
| `top_voted_candidate_lazy.kara` | the votes counted only as far as the queries need: a query finds its vote by binary search and counts up to it if no earlier query has, so the counting is O(n) in all |
| `top_voted_candidate_gallop.kara` | galloping back from the latest vote: the leaders stored as the ★ arm does, with the leader the last candidate to reach the most votes; a query steps back 1, 2, 4, ... votes until one is at or before t, then searches only that last step. O(log d) a query landing d votes from the end |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's example and four more (a
single vote asked at its own time and at 10^9; two votes asked at, and
after, each; a tie that changes hands as each candidate catches up; and
a last vote at 10^9 asked about on both sides of it); for 300 random
elections of up to 500 votes among 2, 10 or every person, with gaps up
to 3, 1,000 or 10^6 between votes and 30 queries each, a checksum of the
answers; and two of LeetCode's largest, 5,000 votes up to time 10^9
with 10,000 queries, among 5,000 people and among 3.
`top_voted_candidate.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: for each query, the votes cast at or before t counted afresh,
and of the people with the most, the one whose latest such vote is the
most recent. It checks 3,200 random elections: 3,000 of up to 8 votes
among up to 3 people, with gaps up to 3 and 6 queries each, against the
statement, and 200 of up to 300 votes among 2, 10 or every person, with
gaps up to 3, 1,000 or 10^6 and 20 queries each, against the other
properties; 44,293 votes and 22,000 queries in all. A check covers every
query of an election.

| | property |
|---|---|
| P1 | the statement's leader at every query, on the small elections |
| P2 | the same answers with each query moved back to the last vote at or before it |
| P3 | the same answers with every time and query moved later by the same random amount |
| P4 | the answers renamed with the people: person `p` renamed `(p + r) % n` |
| P5 | the same answers with one more vote, for the final leader, after every query, and that leader the answer at the new vote |
| P6 | each arm agrees with at least two of the other four |

P2 to P6 are checked on every election. It prints `3200 elections, 44293
votes, 22000 queries, 95000 checks over 5 arms: 0 failures` under
`karac __mir-run` and `karac __mir-llvm-run`, and the same under
`karac __mir-llvm-asan` with no error.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-llvm-run`. All fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a tie kept by the earlier leader | P1 998, P6 1162 |
| M2 | ★: a vote cast at t itself not counted | P1 861, P2 892, P6 894 |
| M3 | ★: the last vote never found | P1 388, P5 393, P6 393 |
| M4 | changes: a candidate one vote behind taking the lead | P1 473, P6 575 |
| M5 | changes: person 0's votes counted twice | P1 783, P4 913, P5 256, P6 896 |
| M6 | changes: the old leader recorded at a change | P1 1461, P4 1920, P5 1669, P6 1659 |
| M7 | map: the voter filed, not the leader | P1 658, P6 792 |
| M8 | map: a vote at t itself left out | P1 2169, P2 1981, P4 1383, P6 2207 |
| M9 | map: the first vote left out of every range | P1 2287, P4 1912, P6 2386 |
| M10 | lazy: the leaders recounted for every query, the counts kept | P1 735, P5 471, P6 909 |
| M11 | lazy: a vote one tick after t counted | P1 861, P2 672, P6 897 |
| M12 | lazy: the votes counted from the last | P1 1192, P5 1184, P6 1388 |
| M13 | gallop: a vote that changes nothing giving the lead back to the first leader | P1 138, P6 240 |
| M14 | gallop: the first vote never reached | P1 264, P5 550, P6 270 |
| M15 | gallop: the search stepping one past a vote at or before t | P1 423, P5 662, P6 565 |

P1 and P6 kill all fifteen; P5 kills seven, P4 four, P2 three and P3
none. Every arm, mutated or not, compares times only with each other
and with t, so moving them all later by the same amount can never
change an answer. P2 sees only the mutants that misplace the edge at a
vote's own time (M2 and M8 leave out a vote cast at t, M11 counts one
cast a tick later), since those answer differently at the vote's time
and just after it. P4 sees the mutants that treat some person or some
answer specially: M5 doubles person 0's votes, M6's first change records
person 0 as the old leader, and M8 and M9 answer `-1`, a number the
renaming moves, when a query's range comes out empty.

Two mutants were replaced. The first M4 dated each change one tick late,
and the differential stopped with an index out of bounds: a query at
the first vote's own time then finds no change at or before it. The
first M13 never recorded the most votes, so every vote took the lead;
that made the gallop arm answer the most recent voter, the same function
as M7, and both gave the same failures.
## Verification

Every arm prints the same output as `top_voted_candidate.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build and the runtime archives are both at
kara `5502146bed`. Under `karac __mir-run` the arms take 0.4 to 1.0 s
each (the sorted map the longest) and the differential 5.4 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

Every frozen legacy lane refuses every arm and the differential. The
harness's `*t` on an element of `.iter()` is rejected, because legacy's
iterator gives the value itself, and the map arm's
`range_inclusive(...).next_back()` is rejected because legacy's
`SortedMap.range` returns a `Vec`. The legacy build of the bench
program runs and prints the same line as the others. Legacy is frozen,
so none of this is filed.

## Benchmarks

The bench program uses the ★ arm on one election of 1,000,000 votes
among 1,000 people, with gaps of 1 to 1,000 between votes, built once.
Each query asks for the leader at a random time from the first vote to
the last gap and folds the answer into a checksum; 2,000,000 queries.
Every implementation prints `1000000 votes, 2000000 queries: checksum
166438777`.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.52 to 0.60 s | 0.54 s |
| Rust (`rustc -O`) | 0.48 to 0.55 s | 0.52 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.47 to 0.55 s | 0.52 s |
| Go | 0.57 to 0.64 s | 0.59 s |
| Python | 10.3 s | |
| Kāra (`karac build --mir`) | 0.53 to 0.63 s | 0.58 s |
| Kāra (legacy `karac build`) | 0.53 to 0.61 s | 0.56 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does.

The compiled programs are within 15% of each other. v2 takes 1.10 times
Rust's median time under overflow checks and 1.07 times C's. Under
valgrind's cachegrind v2 runs 0.86 billion instructions and 228 million
branches, legacy about the same, Rust with overflow checks 0.68 billion
and 180 million, and C 0.58 billion and 86 million; all four mispredict
about 22 million branches, about 11 for each query, which fits a binary
search over random times guessing wrong on half of its 20 steps. That
the times stay this close despite the instruction counts suggests the
searches are waiting on memory, the times and leaders being 8 MB each,
but cache misses were not measured.
