# 2332. The Latest Time to Catch a Bus

You are given a **0-indexed** integer array `buses` of length `n`, where
`buses[i]` represents the departure time of the `i`th bus. You are also
given a **0-indexed** integer array `passengers` of length `m`, where
`passengers[j]` represents the arrival time of the `j`th passenger. All
bus departure times are unique. All passenger arrival times are unique.

You are given an integer `capacity`, which represents the **maximum**
number of passengers that can get on each bus.

When a passenger arrives, they will wait in line for the next available
bus. You can get on a bus that departs at `x` minutes if you arrive at
`y` minutes where `y <= x`, and the bus is not full. Passengers with
the **earliest** arrival times get on the bus first.

More formally when a bus arrives, either:

- If `capacity` or fewer passengers are waiting for a bus, they will
  **all** get on the bus, or
- The `capacity` passengers with the **earliest** arrival times will
  get on the bus.

Return *the latest time you may arrive at the bus station to catch a
bus*. You **cannot** arrive at the same time as another passenger.

**Note:** The arrays `buses` and `passengers` are not necessarily
sorted.

```
buses = [10,20], passengers = [2,17,18,19], capacity = 2                ->  16
buses = [20,30,10], passengers = [19,13,26,4,25,11,21], capacity = 2    ->  20
```

**Constraints:** `n == buses.length`; `m == passengers.length`;
`1 <= n, m, capacity <= 10^5`; `2 <= buses[i], passengers[i] <= 10^9`;
each `buses[i]` is unique; each `passengers[i]` is unique.

With both lists sorted the buses fill from the earliest passengers, and
only the last bus matters. If it leaves with room, arriving at its
departure boards it; if it leaves full, one must stand in its last
passenger's place, arriving just before them. Either way the time tried
may belong to a passenger, so step back one unit at a time past the run
of passengers who boarded just before. Since the times are at least 2,
the step never passes 1. O((n + m) log(n + m)) for the sorts.

## Approaches

| file | mechanism |
|---|---|
| `bus.kara` ★ | both lists sorted, the buses filled in order with one pointer into the passengers; the last bus's departure or its last passenger's time, then a step back past the passengers boarded just before, read off the sorted list |
| `bus_naive.kara` | every candidate tried: the latest workable time is a departure or one before some passenger, so each of those no passenger holds is tried from the largest down, the whole boarding run again with oneself in the queue. O((n + m)^2 log(n + m)) |
| `bus_set.kara` | a `Set[i64]` of the passengers' times: the buses fill as in the ★ arm, and the time tried steps down while the `Set` holds it |
| `bus_search.kara` | a binary search on the time: arriving earlier never costs a seat, so the times that board run from 1 up to some largest one, found by halving between 1 and the last departure, each tried by counting who stands ahead; then stepped down past the passengers with `binary_search` |
| `bus_iter.kara` | iterators: the sorted buses `fold`ed into how far the passengers have boarded and how many took the last bus, each bus's share what `skip`, `take_while` and `take` let on; then `(1..=start).rev().find` the first time no passenger holds |
| `bus_solution.kara` | LeetCode's Rust template: `mut` vectors of `i32` sorted with `sort_unstable`, a `usize` pointer, and the step back through an `i32` index; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 7 lines: LeetCode's two examples; one bus and
a passenger at its departure; more passengers before the first bus than
it holds; passengers at every time up to a bus; 1000 buses and 2000
passengers up to `10^9`; then 2000 random cases of 1 to 8 buses and 1
to 12 passengers at times up to 40, capacity 1 to 3, with a checksum and
the answers in all. `bus.py` mirrors the ★ arm and its output is
byte-identical.

`karac fix` carries the template in one call, reporting 27 edits.
`check` first reports 17 errors and offers 16 edits for them:
`struct Solution;` to `struct Solution {}`; the brackets of the six
`Vec<..>`; the three `&&` to `and`; the `&` of `for &b in &buses` and of
the two closures' `|&t|` dropped and `&buses` to `ref buses`; and
`Solution::` to `Solution.` in the harness's wrapper. The other eleven
follow from those. The two parameters written `mut buses`, which the
method sorts, become `own Vec[i32]` with a `let mut buses = buses;` in
the body, since a bare parameter borrows and cannot be sorted in place;
`sort_unstable` becomes `sort`; and the wrapper's `as i64` on the `i32`
answer is dropped, since it widens on its own. The `k as usize` index
and the `j as i32 - 1` stand as Kāra.

The search arm's bounds are written `let mut (low, high) = (1, ...)`,
and its step back asks `passengers.binary_search(latest).is_some()`.
Kāra's `binary_search` gives an `Option`; Rust's `is_ok()` there is
accepted as a deprecated spelling, which `karac check` warns about and
`karac fix` rewrites to `is_some()`, one edit.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: for every arrival time from 1 to the last departure that no
passenger holds, the stop is run minute by minute, everyone arriving
joining the back of one queue, oneself among them, and each bus at its
minute taking up to `capacity` from the front; the answer is the latest
time that boards. Nothing is sorted ahead and nothing is stepped back.
It checks 300 random cases of 1 to 6 buses and 1 to 10 passengers at
times up to 30, capacity 1 to 3; then 30 crowded ones, 15 to 25
passengers and 1 to 3 buses up to 40, capacity 1 or 2; then 30 of up to
200 buses and 300 passengers up to `10^9`, capacity 1 to 5. All 360 are
drawn before any arm answers.

| | property |
|---|---|
| P1 | times up to 40: the answer is the literal reading's |
| P2 | the answer is from 1 to the last departure, and no passenger's time |
| P3 | the buses and the passengers each in reverse order: the same answer |
| P4 | every time 7 later: the answer 7 later |
| P5 | capacity for every passenger and one more: the latest time up to the last departure that no passenger holds |
| P6 | each arm agrees with at least three of the other five |

P5 holds because with room for everyone and oneself the last bus can
never be full, so any free time up to its departure boards.

The differential prints `360 cases: checksum 271725401, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and runs the same minute-by-minute queue. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the passengers never sorted | P1 174, P2 69, P3 199, P5 74, P6 199 |
| M5 | ★: a full bus taken as having room | P1 165, P2 52, P6 182 |
| M6 | ★: the first bus taken as the last | P1 127, P2 21, P5 288, P6 140 |
| M7 | naive: only the departures tried | P1 176, P2 92, P4 92, P5 74, P6 193 |
| M8 | naive: a passenger at the departure left behind | P1 154, P2 13, P4 13, P5 279, P6 167 |
| M9 | naive: oneself never first onto a bus | P1 206, P2 155, P4 155, P5 145, P6 223 |
| M14 | set: the first passenger left out of the set | P1 37, P2 38, P3 66, P5 16, P6 38 |
| M15 | set: the passengers never sorted | P1 137, P3 175, P6 162 |
| M16 | set: two steps back at a time | P1 159, P2 9, P5 61, P6 176 |
| M17 | search: a full bus taken as having room | P1 117, P6 134 |
| M19 | search: the search capped at the first departure | P1 229, P5 288, P6 257 |
| M21 | search: a full bus one seat short | P1 75, P4 20, P6 89 |
| M22 | iter: a bus taking one too many | P1 103, P6 118 |
| M23 | iter: a passenger at the departure left behind | P1 21, P6 21 |
| M24 | iter: a full bus taken as having room | P1 160, P6 177 |
| M27 | solution: the count aboard never reset | P1 195, P6 224 |
| M28 | solution: a passenger at the departure left behind | P1 48, P2 27, P5 81, P6 48 |

P1 and P6 kill all seventeen, P2 and P5 nine each, P4 four and P3
three. P2 fails for an answer past the last departure, below 1 or on a
passenger's time, which an edit reaches when it steps back wrongly or
finds no time and answers -1. P5, room for everyone, fails where an
edit misreads a bus with room or the last bus: the first bus taken as
the last, the search capped at the first departure, a passenger's time
left in. P4, every time 7 later, fails only in the naive arm and the
search, where an edit's answer is tied to the fixed floor of 1 or the
-1 of no time found rather than to the departures and passengers, which
move. P3, the lists reversed, fails only where order survives into the
answer: the passengers never sorted, and the first passenger left out
of the set. The edits to how many a bus takes or when it is full leave
P2 to P5 standing, since their wrong answer is still a free time in
range that moves with the times, and only the literal reading and the
other arms catch them.

Of the thirty-one, fourteen were not kept. The ★ arm's count aboard
never reset (M2) fails as the template's (M27), and its passenger at
the departure left behind (M3) as the template's (M28); the template's
full bus taken as having room (M29) and first bus taken as the last
(M31) fail as the ★ arm's (M5, M6). One step
back at most fails alike in the ★ (M4), set (M13) and template (M30)
arms, and none is kept; the search arm's (M20) fails apart from them
and was left out to keep three to an arm. The set arm's bus with room
taken one before its departure (M12) fails as the iter arm's start
itself never tried (M25), and neither is kept. The search arm's oneself standing ahead of a
passenger who comes at the same moment (M18) is killed by nothing: the
times it seats differently are passengers' own, and the step back past
them lands on the same free time. The iter arm's each bus taking from
the first passenger (M26) read past the end of the passengers and
crashed; it was replaced by the earliest free time, not the latest,
which fails apart from every kept one, as do the naive arm's passenger's
time allowed (M10) and earliest time that boards (M11), and all three
were left out to keep three to an arm.

## Verification

Every arm prints the same output as `bus.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` every arm takes 0.3 to 0.5 s; the naive arm's
quadratic retries stay small on cases of at most 20 times. The
differential takes 1.7 s there and 0.6 s under `karac __mir-llvm-run`.

## Benchmarks

The bench builds 10 cases of `5 * 10^4` buses and `10^5` passengers
once, every time distinct, drawn from a scramble that never repeats,
then makes 5 passes, case `k` in pass `p` with capacity
`1 + (k + p) % 5`, each call sorting its own copies, with the ★ arm in
all five languages. Every implementation prints `5 passes over 10 cases
of 5*10^4 buses and 10^5 passengers: checksum 959193617`. Each keeps
the times as 64-bit integers and sorts them with its standard library's
sort: Kāra's and Rust's stable merge sorts, C's `qsort`, Go's
`slices.Sort` and Python's `list.sort`.

BENCHTAB
