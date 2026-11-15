# 2187. Minimum Time to Complete Trips

You are given an array `time` where `time[i]` denotes the time taken by
the `ith` bus to complete **one trip**.

Each bus can make multiple trips **successively**; that is, the next
trip can start **immediately after** completing the current trip. Also,
each bus operates **independently**; that is, the trips of one bus do
not influence the trips of any other bus.

You are also given an integer `totalTrips`, which denotes the number of
trips all buses should make **in total**. Return *the **minimum time**
required for all buses to complete **at least*** `totalTrips` *trips*.

```
time = [1, 2, 3], totalTrips = 5  ->  3
time = [2],       totalTrips = 1  ->  2
```

**Constraints:** `1 <= time.length <= 10^5`; `1 <= time[i], totalTrips
<= 10^7`.

By time t a bus of trip time x has made t / x trips, and the sum only
grows with t, so the least t whose trips reach the total is found by a
binary search. The fastest bus alone reaches the total by its time
times the total, which bounds the search at 10^14. A sum over 10^5
buses of up to 10^14 trips each would pass an `i64`, so the count stops
once it reaches the total. O(n log(min * total)).

## Approaches

| file | mechanism |
|---|---|
| `trips.kara` ★ | a binary search over [1, the fastest bus alone], the trips by each time counted with a `break` once they reach the total |
| `trips_doubling.kara` | no bound worked out: the time doubled from 1 until it suffices, then halved between the last time that fell short and the first that did not; O(n log answer) |
| `trips_sorted.kara` | the buses `sort`ed fastest first, so a count stops at the first bus slower than the time, which makes none, as well as at the total; the search from the fastest bus's first trip |
| `trips_struct.kara` | a `struct Fleet` of the times and the fastest, made `of` a list, that counts its `trips_by` a time up to a cap and finds its `first_time_for` so many trips (`ref self`) |
| `trips_iter.kara` | the bound by `min`, the trips by a time each bus's `map`ped and `sum`med in a closure, and the search a `fold` over the bits of the largest time that falls short, from bit 47 down |
| `trips_solution.kara` | LeetCode's Rust template: `Vec<i32>`, `*time.iter().min().unwrap() as i64 * total`, `map(\|&x\| mid / x as i64).sum::<i64>()`, `struct Solution;`, `Solution::`; carried by `karac fix` in two rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's two examples and four more
(one bus at the constraints' largest, buses of one time, a bus too slow
to help, and a total met exactly at a time two buses share), each with
its time; then the total and a checksum over 2000 random fleets of 1 to
20 buses, with times of 1 to 10 and 1 to 100 trips, and times of 1 to
10^7 and 1 to 10^7 trips, in turn; then the constraints' largest,
10^5 buses and 10^7 trips: every time 10^7, every time 1, and times at
random. `trips.py` mirrors the ★ arm and its output is byte-identical.

The iterator arm was written with its closure's return type,
`|t: i64| -> i64 { .. }`, which is Rust's spelling; `karac check`
refuses it with a fix, and `karac fix` moves the type onto the binding,
`let trips: Fn(i64) -> i64 = |t: i64| { .. }`, in one round of 2 edits.

`karac fix` carries the template in two rounds of 11 and 1 edits:
Rust's spellings (`Vec<..>` to `Vec[..]`, the `&x` patterns to `x`,
`.sum::<i64>()`'s turbofish, `struct Solution;` to `struct Solution
{}`, and `Solution::` to `.`, among them); then the `as i64` on the
fastest time dropped, as the `i32` widens to the `i64` it is multiplied
by.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the clock run on one unit at a time, each bus finishing a
trip at every multiple of its time, until the trips finished reach the
total. No division and no search. It checks 300 random fleets of 1 to 5
buses with times of 1 to 6 and 1 to 20 trips; then 30 of one bus; then
30 whose buses share one time. All 360 are drawn before any arm
answers.

| | property |
|---|---|
| P1 | the time is the statement read literally |
| P2 | the buses reversed: the same time |
| P3 | every bus's time doubled: the time doubled |
| P4 | one trip more: a time no earlier, and at most the fastest bus's time later |
| P5 | the trips finished by the time, every bus counted, reach the total, and one unit before it do not |
| P6 | each arm agrees with at least three of the other five |

P2 holds since the buses run apart. P3 holds since by time 2t a bus of
time 2x has made what a bus of time x made by t, and by an odd time
2t + 1 no more. P4 holds since the trips grow with the time, and the
fastest bus finishes one more within its own time. P5 holds since the
time asked for is the first at which the trips reach the total.

The differential prints `360 fleets: checksum 730934214, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading of the same
fleets. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Thirty-four edits to the differential, seven to the ★, doubling and
struct arms, five to the sorted and iter arms and three to the
template, each run under `karac __mir-llvm-run` and `karac __mir-run`.
Seventeen are kept, three to each Kāra arm and two to the Rust-template
arm. Each kept one is killed, fails the same way under both backends
and not by a crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the search from 2 | P1 10, P3 10, P5 10, P6 10 |
| M2 | ★: the bound one short | P1 109, P3 115, P5 109, P6 109 |
| M3 | ★: a time that only matches the total | P1 151, P2 72, P3 31, P4 129, P5 151, P6 151 |
| M6 | doubling: the answer the last time that fell short | P1 360, P3 360, P5 360, P6 360 |
| M8 | doubling: the halving stopped one early | P1 96, P3 96, P4 54, P5 96, P6 96 |
| M9 | doubling: each bus a trip more | P1 350, P3 66, P5 350, P6 350 |
| M11 | sorted: never sorted | P1 41, P2 48, P4 2, P5 41, P6 41 |
| M12 | sorted: a bus as slow as the time stopping the count | P1 38, P3 38, P5 38, P6 38 |
| M13 | sorted: the search from the fastest bus's second trip | P1 39, P5 39, P6 39 |
| M17 | struct: the count capped one short | P1 240, P3 20, P5 240, P6 240 |
| M20 | struct: each bus at most one trip | P1 219, P4 12, P5 219, P6 219 |
| M34 | struct: each bus a unit slower | P1 245, P3 223, P4 43, P5 245, P6 245 |
| M22 | iter: a time that reaches the total kept as short | P1 129, P5 129, P6 129 |
| M23 | iter: the bits from 4 down | P1 37, P3 95, P5 37, P6 37 |
| M25 | iter: a bus's trips rounded up | P1 309, P3 360, P5 309, P6 309 |
| M26 | solution: the adapter's total one more | P1 233, P5 233, P6 233 |
| M28 | solution: the adapter's times halved, rounded up | P1 314, P3 237, P5 314, P6 314 |

P1, P5 and P6 kill all seventeen, P3 twelve, P4 five and P2 two. P3
doubles the times, and misses an edit that answers another question
exactly, whose answer doubles too: a total one more (M26), one trip
more than the total kept short (M22), at most one trip a bus (M20), and
the search from the second trip (M13), besides the unsorted count
(M11). P4 asks for one trip more, and sees an edit whose times jump by
more than the fastest bus between one total and the next, or fall: a
time only matching the total (M3), the halving one early (M8), the
unsorted count (M11), one trip a bus (M20), and each bus slower (M34).
P2 reverses the buses, and sees only the edits that read them in order:
the ★ arm's count that stops at the total, asked to match it exactly
(M3), and the sorted arm's count that stops at the first slow bus, with
the buses never sorted (M11).

Of the thirty-four, seventeen were not kept. Five are equivalent: the
★ arm's count checked before each bus is added (M4), which stops in
the same place or one bus later, past the total either way; its
slowest bus as the bound (M5), the struct arm's first bus as the bound
(M16), and the iter arm's slowest (M21), as any bus alone reaches the
total by its time times the total; and the doubling arm's time tripled
(M7), since the halving after finds the least time all the same. M21
holds on the differential's small fleets only: on the harness's 10^5
buses of time 1, a time of 10^14 is 10^19 trips, past an `i64`. One
crashes: the doubling arm's first bus left out (M10), which never has
enough with one bus, and doubles past an `i64`. One never ends: the
struct arm's midpoint rounded up (M19), which at two times next to each
other asks the upper one again. Five fail as a kept one does: the
struct arm's count one more below the cap, as M17; the iter arm's
answer the time that fell short, as M6; the ★ arm's trips rounded up,
as M25; the doubling arm's enough only past the total, as M26; and the
struct arm's overshoot returned as it is, as M3. Five were left out to
keep three to an arm: the ★ arm's trips by one unit before (M30), the
doubling arm's short end moved past the doubled time (M32), the sorted
arm's buses slowest first (M14) and a time that falls short taken
(M15), and the template's bound the total alone (M27).

## Verification

Every arm prints the same output as `trips.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the struct, ★, sorted and doubling arms take
1.4 s to 2.7 s, and the iter and template arms 8.7 s and 9.2 s, which
sum every bus at every step, with no stop at the total. The
differential takes 0.4 s.

## Benchmarks

The bench builds one row of 10^6 trip times of 1 to 10^7 once; then
solves 200 windows of 10^5 buses, the constraints' longest, each at a
random start and with 1 to 10^7 trips, so that no solve repeats one
before, with the ★ arm in all five languages. C works over a pointer
and a length, Rust and Go over a slice of the row; Kāra and Python copy
each window into a list of its own. Every implementation prints `200
solves: checksum 330895053`.

BENCHTAB
