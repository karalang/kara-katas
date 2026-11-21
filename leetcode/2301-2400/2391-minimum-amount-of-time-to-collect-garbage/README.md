# 2391. Minimum Amount of Time to Collect Garbage

You are given a **0-indexed** array of strings `garbage` where
`garbage[i]` represents the assortment of garbage at the `i`th house.
`garbage[i]` consists only of the characters `'M'`, `'P'` and `'G'`
representing one unit of metal, paper and glass garbage respectively.
Picking up **one** unit of any type of garbage takes `1` minute.

You are also given a **0-indexed** integer array `travel` where
`travel[i]` is the number of minutes needed to go from house `i` to
house `i + 1`.

There are three garbage trucks in the city, each responsible for
picking up one type of garbage. Each garbage truck starts at house `0`
and must visit each house **in order**; however, they do **not** need
to visit every house.

Only **one** garbage truck may be used at any given moment. While one
truck is driving or picking up garbage, the other two trucks **cannot**
do anything.

Return *the **minimum** number of minutes needed to pick up all the
garbage.*

```
garbage = ["G","P","GP","GG"], travel = [2,4,3]  ->  21
garbage = ["MMM","PGM","GP"], travel = [3,10]    ->  37
```

**Constraints:** `2 <= garbage.length <= 10^5`; `garbage[i]` consists
of only the letters `'M'`, `'P'`, and `'G'`; `1 <= garbage[i].length <=
10`; `travel.length == garbage.length - 1`; `1 <= travel[i] <= 100`.

Since only one truck works at a time, the minutes add up: every unit is
one minute whichever truck takes it, and each truck drives exactly to
the last house holding its kind.

## Approaches

| file | mechanism |
|---|---|
| `garbage.kara` ★ | the units counted once, each kind's last house noted, and each truck's drive the travel's prefix sum up to it. O(total length) |
| `garbage_trucks.kara` | the three trucks driven one at a time, each carrying the travel it has not paid for until a house holds its kind. O(3 * total length) |
| `garbage_back.kara` | from the end of the street: the kinds seen so far are the trucks that must cross each road into the house, so each road is paid once per kind. O(total length) |
| `garbage_map.kara` | a `Map[char, i64]` from each kind to its last house, and the prefix sums from a `Vec.filled`; the `Map` is only summed, so its order never shows |
| `garbage_iter.kara` | iterators: the units by `map` and `sum`, each kind's last house by `rposition` with `contains`, its drive by `take` and `sum` |
| `garbage_solution.kara` | LeetCode's Rust template: `enumerate`, a `[0usize; 3]` of last houses, a `match` on byte literals, prefix sums in a `vec![0; n]`, and the drives summed with a turbofish; carried by `karac fix` and one hand edit (below) |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 6 lines: LeetCode's two examples; one house of
all three kinds; glass only at the first house with metal further on;
`10^5` houses of up to 10 units with travel up to 100, and the same
street's travel with glass at every house and metal and paper only at
the first; then 3000 random streets of 1 to 30 houses, with a checksum
and the longest time. `garbage.py` mirrors the ★ arm and its output is
byte-identical, and the mirror was checked on 20000 random streets of
up to 8 houses against every stopping house for every truck.

`check` first reports 5 errors on the template, and `karac fix` carries
it in one call, reporting 11 edits: `struct Solution;` given its braces;
the two `Vec<..>` their brackets; `[0usize; 3]` written `[0; 3]`; `let
mut ans = 0;` given the `i32` it is returned as; the `&` of `|&j|`
dropped; `vec![0; n]` written `Vec.filled(n, 0i32)`; and the turbofish
of `sum::<i32>()` dropped. The `0i32` is for the tail `ans +
last.iter().map(|j| pre[j]).sum()`, an `i32`. At first that narrowing
was left with no fix: the same narrowing at `pre[k]` or at
`pre.iter().sum()` was traced to `pre`'s literal, but not `pre` read
inside a `map` closure over another collection (B-2026-11-21-43, fixed),
and the template was carried again after the fix. The match on `b'M'`,
the `as` casts, `enumerate` and the prefix sums stand as Kāra.

`karac fmt` writes the template's `b'M' =>` and `b'P' =>` patterns as
`77u8 =>` and `80u8 =>` (B-2026-11-21-48), so the template and the differential
keep the byte literals as written.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: each truck may stop at any house past which none of its kind
is left, and its time is every unit of its kind plus the travel to that
house, the least of those kept. No prefix sums and no last-house
shortcut. It checks 300 random streets of 1 to 12 houses, which the
literal reading answers; then 30 of up to 2000 houses; then 30 where
one kind is all there is. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | up to 12 houses, the answer is the literal reading's |
| P2 | the answer is at least the units, and at most the units and the whole street three times |
| P3 | each house's units written in reverse: the same answer |
| P4 | every road twice as long: the travel part of the answer doubled |
| P5 | the kinds renamed, M to P, P to G and G to M: the same answer |
| P6 | each arm agrees with at least three of the other five |

P3 holds because the order within a house changes neither its units nor
which kinds it holds, P4 because the units do not depend on the roads,
and P5 because the three trucks are alike.

The differential prints `360 cases: checksum 969219406, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and tries every stopping house. On a failure it prints
the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M3 | ★: every road a minute shorter | P1 273, P4 333, P6 333 |
| M4 | ★: only two trucks | P1 169, P5 222, P6 202 |
| M5 | ★: metal taken for paper | P1 109, P5 109, P6 120 |
| M7 | trucks: the travel paid again | P1 239, P2 250, P6 299 |
| M8 | trucks: one unit a house | P1 233, P2 13, P4 285, P6 285 |
| M10 | trucks: no glass truck | P1 188, P2 56, P4 221, P5 293, P6 221 |
| M13 | back: metal seen as paper | P1 105, P5 102, P6 115 |
| M14 | back: one truck on every road | P1 171, P6 189 |
| M16 | back: one truck too many | P1 273, P2 77, P6 333 |
| M17 | map: every last house the first | P1 273, P6 333 |
| M19 | map: each prefix one road | P1 244, P6 304 |
| M21 | map: each drive there and back | P1 273, P2 185, P6 333 |
| M22 | iter: each kind's first house | P1 267, P6 327 |
| M24 | iter: a house counted only when it starts with the kind | P1 119, P3 119, P6 135 |
| M26 | iter: a missing kind driving the street | P1 192, P6 243 |
| M27 | solution: one unit a house | P1 245, P2 18, P4 297, P6 297 |
| M28 | solution: every road a minute longer | P1 273, P2 31, P4 333, P6 333 |

P1 and P6 kill all seventeen, P2 seven, P4 five, P5 four and P3 one.
P5, the kinds renamed, fails the edits that treat one kind unlike the
others: two trucks only (M4), no glass truck (M10), and metal taken for
paper (M5, M13). P4, the roads doubled, fails the edits whose error is
not a multiple of the travel: a road a minute shorter or longer (M3,
M28) and a unit miscounted (M8, M10, M27). P3, each house's units
reversed, fails only the edit that reads a house by its first unit
(M24); every other arm counts a house's units in any order. P2, the
bounds, fails the edits that pay a road too often or count units
wrong, and passes those that drive too short or too far within them.

Of the thirty-one, fourteen were not kept. A unit not counted in the
★, back and map arms and the iter arm's units left out (M1, M12, M18,
M25) all fail alike, and apart from every kept one. The back arm's
first road never paid, the map arm's first road left out and the
template's last road never summed (M15, M20, M31) fail as the map arm's
every last house the first (M17); the template's paper counted as metal
(M29) as the back arm's metal seen as paper (M13); the template's only
the longest drive (M30) as the back arm's one truck on every road
(M14); and the ★ arm's each drive one house further and the iter arm's
one road past the last house (M6, M23) alike. The ★ arm's each kind's
first house kept (M2) and the trucks arm's lone unit skipped and only
the last road owed (M9, M11) each fail apart from every kept one, and
were left out to keep three to an arm. The iter arm's first edit there,
no glass truck, failed as the ★ arm's two trucks (M4) did and was
replaced by the house counted by its first unit (M24).

## Verification

Every arm prints the same output as `garbage.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 3.0 to 5.1 s, most of it the
`10^5`-house street. The differential takes 11.4 s there and 0.54 s
under `karac __mir-llvm-run`.

## Benchmarks

The bench builds 50 streets of 2000 houses of up to 10 units, with
travel up to 100, once from the harness's generator, then makes 500
passes, answering every street and folding each answer plus the pass
into the checksum, with the ★ arm in all five languages. Every
implementation prints `500 passes over 50 streets of 2000 houses:
checksum 130984228`. Every implementation allocates the prefix sums
afresh in each call.

BENCHTAB
