# 2528. Maximize the Minimum Powered City

You are given a **0-indexed** integer array `stations` of length `n`,
where `stations[i]` represents the number of power stations in the
`i`-th city.

Each power station can provide power to every city in a fixed **range**.
In other words, if the range is denoted by `r`, then a power station at
city `i` can provide power to all cities `j` such that `|i - j| <= r` and
`0 <= i, j <= n - 1`.

The **power** of a city is the total number of power stations it is
being provided power from.

The government has sanctioned building `k` more power stations, each of
which can be built in any city, and have the same range as the
pre-existing ones.

Given the two integers `r` and `k`, return *the **maximum possible
minimum power** of a city, if the additional power stations are built
optimally.*

**Note** that you can build the `k` power stations in multiple cities.

```
stations = [1, 2, 4, 5, 0], r = 1, k = 2  ->  5
stations = [4, 4, 4, 4], r = 0, k = 3     ->  4
```

**Constraints:** `n == stations.length`; `1 <= n <= 10^5`;
`0 <= stations[i] <= 10^5`; `0 <= r <= n - 1`; `0 <= k <= 10^9`.

Whether a least power `m` can be reached is monotone in `m`, so every
arm searches for the largest reachable one. A target is checked by a
sweep from the left: a city short of it gets the shortfall placed as far
right as still reaches it, `r` cities on, where the new stations also
help the most cities still to come. A city's power reaches `10^10`, and
the answer that plus `10^9`, so everything is an `i64`.

## Approaches

| file | mechanism |
|---|---|
| `power.kara` ★ | each city's power from prefix sums, then a binary search with the sweep; a placed station's reach ends `2r + 1` on, kept in a difference array. O(n log(k + max power)) |
| `power_window.kara` | a sliding window over the stations themselves, no power formed ahead: the window gains the city `r` on and loses the one `r + 1` back, stations placed so far counted in; a shortfall placed at the window's right end |
| `power_queue.kara` | the ★ arm's sweep with the placed stations kept in a `VecDeque` of `(last city reached, count)`, the front leaving once the sweep passes it |
| `power_rec.kara` | recursion: the binary search as a recursion on the range still open, and the sweep as a recursion over the cities carrying the running count and the stations still to place; up to `10^5` deep |
| `power_iter.kara` | iterators: the prefix sums as a `scan`, the powers `map`ped from them, the least a `min`; a target reachable when `all` cities, swept by a closure that keeps the running count, the stations used and the difference array, can be brought up to it |
| `power_solution.kara` | LeetCode's Rust template: `Vec<i32>` and two `i32` in, `i64` out; the ★ arm's method with `saturating_sub` for the window's left end and the sweep as a closure; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 12 lines: LeetCode's two examples and six
more, among them a single city with `k = 10^9`, two full cities about an
empty one with `r = 0`, and an `r` that reaches every city; then 2000
random lists of 1 to 20 cities with 0 to 5 stations, `r` up to `n - 1`
and `k` up to 20, as the sum of the answers and a checksum; then the
constraints' largest, `10^5` cities of up to `10^5` stations with
`k = 10^9` and `r` of 0, 10 and `10^4`. `power.py` mirrors the ★ arm
and its output is byte-identical, and the mirror was checked on 1500
random lists of 1 to 5 cities with 0 to 3 stations and `k` up to 4
against every way to build the `k` stations, and the two agreed on
every list.

`check` reported one error on the iter arm as first written: its
closure declared `-> bool`, which Kāra infers, and `karac fix` removed
it. The other four Kāra arms checked clean.

`check` first reports 6 errors on the template: the unit struct
`struct Solution;`, two `Vec<..>`, the closure's `-> bool`, the path
call `Solution::max_power`, and the `&x` closure pattern. `karac fix`
carries it in one call, reporting 19 edits. Besides those six, it
makes the written `usize` of `let r = r as usize` an `i64`, the two
`vec![0i64; n + 1]` `Vec.filled(n + 1, 0)`, drops the `i64` suffixes
and the casts an `i32` widens through by itself, and keeps the floor
of `i.saturating_sub(r)`, which an `i64` does not have, with `.max(0)`.

That last edit reached kara main while this kata was written
(B-2026-11-21-70, found by kata 1314; this kata found it again). In the
template `i` is a `usize` from `0..n` and `r` a `usize`, so Rust's
`saturating_sub` stops at 0. In Kāra `i` comes from a length, an `i64`,
and the fix that made `r` an `i64` left the call as it was; an `i64`'s
`saturating_sub` stops only at `i64.MIN`, so the fixed program, which
`check` accepted, read `prefix[-1]` and failed at run time with an index
out of bounds. A `saturating_sub` or `checked_sub` on an `i64` index
whose argument is a written `usize` now gets the floor the fix already
gave a `usize` receiver.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every way to build the `k` new stations, one city at a time
with repeats allowed, is tried, and the answer is the best least power
any of them gives, each city's power summed over the cities within `r`
of it. It checks 360 random lists of 1 to 6 cities with 0 to 4 stations
each, `r` from 0 to `n - 1` and `k` from 0 to 4. All are drawn before
any arm answers, and in 286 of them the new stations raise the least
power.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer lies between the least power with no new station and that plus `k` |
| P3 | `k` one more: the answer the same or one more |
| P4 | the cities reversed: the same answer |
| P5 | every city's stations and `k` doubled: at least twice the answer |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 cases, 286 raised above the least:
checksum 813638215, 12960 checks over 6 arms: 0 failures` under every
lane in Verification; the checksum of the literal answers was checked
against a Python reading that builds the same cases and tries every
placement. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M4 | ★: the window one city short on the right | P1 278, P2 143, P4 164, P6 278 |
| M5 | ★: the search capped below k | P1 255, P6 255 |
| M6 | ★: a shortfall met by one station | P1 46, P3 5, P6 46 |
| M8 | window: a shortfall placed at the city itself | P1 41, P6 41 |
| M9 | window: the window begun one city short | P1 232, P4 112, P6 232 |
| M10 | window: the least taken as the first window | P1 54, P2 48, P4 95, P6 54 |
| M12 | queue: a station leaving a city early | P1 19, P6 19 |
| M14 | queue: each station counted twice | P1 279, P6 279 |
| M16 | queue: half a station leaving | P1 44, P4 11, P5 24, P6 44 |
| M17 | rec: the sweep stopped a city early | P1 36, P4 15, P6 36 |
| M19 | rec: running out allowed | P1 27, P3 10, P4 9, P5 27, P6 27 |
| M20 | rec: the search taking the lower half on success | P1 291, P3 24, P5 10, P6 291 |
| M23 | iter: the reach ending a city late | P1 36, P6 36 |
| M24 | iter: k plus 1 allowed | P1 22, P5 22, P6 22 |
| M26 | iter: the search capped at k | P1 231, P6 231 |
| M27 | solution: the window reaching r + 1 on the right | P1 107, P2 77, P4 155, P6 107 |
| M31 | solution: a shortfall of one more | P1 261, P3 7, P4 19, P5 12, P6 261 |

P1 and P6 kill all seventeen, P4 eight, P5 five, P3 four, and P2
three.

Two of the first thirty-one edits survived, both to the queue arm, and
were replaced. One station leaving per city at most is equivalent: each
city places at most one entry, and the entries' last cities rise one by
one, so no two leave together. The search begun at 0 is equivalent too:
the least power is always reachable, so the lower half of the search
only costs steps. They became the queue arm's each station counted
twice and half a station leaving (M14, M16).

Fourteen are not kept, and none survives. Three fail exactly as a kept
one: the ★ arm's `k + 1` allowed (M3) as the iter arm's (M24); the
queue arm's station reaching one city less (M13) as its station leaving
a city early (M12); and the template's `k` read as half (M29) as the
queue arm's each station counted twice (M14), each spending stations at
twice the rate. The other eleven fail in five ways of their own, in
arms that already hold their kept edits: the reach ending `2r` on in
the ★, rec and template arms (M1, M18, M30); the ★ arm's reach never
ending and the window arm's placed stations never leaving (M2, M7); the
window arm's `k` allowed but not reached (M11); the queue arm's
shortfall not added in, the rec arm's not carried on and the iter arm's
running count not carried (M15, M21, M25); and the iter arm's prefix
sums one place off and the template's window's left end one city in (M22,
M28), each reading the window from a city too far right.

## Verification

Every arm prints the same output as `power.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 4.8 to 28.1 s and the differential 0.6 s; under `karac __mir-llvm-asan` the arms take 1.6 to 4.6 s and the differential 0.8 s; and under `karac run` the differential takes 0.7 s.

## Benchmarks

The bench builds `10^5` random cities of 0 to `10^5` stations once from
its own generator, then makes 20 passes. Each pass asks for the answer
with `r = check % 100` and `k = 10^9 - check % 1000`, and folds it plus
the pass into the checksum. The bench uses the ★ arm in all five
languages. Every implementation prints `20 passes over 100000 cities:
checksum 971065409`.

BENCHTAB
