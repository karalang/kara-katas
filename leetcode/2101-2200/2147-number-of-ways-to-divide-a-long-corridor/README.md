# 2147. Number of Ways to Divide a Long Corridor

Along a long library corridor, there is a line of seats and decorative
plants. You are given a **0-indexed** string `corridor` of length `n`
consisting of letters `'S'` and `'P'` where each `'S'` represents a seat
and each `'P'` represents a plant.

One room divider has **already** been installed to the left of index `0`,
and **another** to the right of index `n - 1`. Additional room dividers
can be installed. For each position between indices `i - 1` and `i`
(`1 <= i <= n - 1`), at most one divider can be installed.

Divide the corridor into non-overlapping sections, where each section
has **exactly two seats** with any number of plants. There may be
multiple ways to perform the division. Two ways are **different** if
there is a position with a room divider installed in the first way but
not in the second way.

Return *the number of ways to divide the corridor*. Since the answer may
be very large, return it **modulo** `10^9 + 7`. If there is no way,
return `0`.

```
corridor = "SSPPSPS"  ->  3
corridor = "PPSPSP"   ->  1
corridor = "S"        ->  0
```

**Constraints:** `n == corridor.length`; `1 <= n <= 10^5`;
`corridor[i]` is either `'S'` or `'P'`.

Every section holds two seats, so the seats pair off in order, the first
with the second, the third with the fourth, and so on. Between two
neighbouring pairs a divider must stand somewhere after the one pair's
second seat and before the next pair's first, which is as many places
as the gap between their indices, and each such divider is chosen
apart from the others: the answer is the product of the gaps. With no
seat, or an odd number, there is no way. O(n).

## Approaches

| file | mechanism |
|---|---|
| `corridor.kara` ★ | the seats' indices `collect`ed from `chars().enumerate()` under `filter`, then the gaps between pairs multiplied over `step_by(2)` |
| `corridor_dp.kara` | no list: the ways so far counted by how many seats the open section holds, none, one or two; a seat moves each count on, a plant may close a full section; the ways ending full are the answer |
| `corridor_count.kara` | counting as it goes over `bytes()`, `b'S'` against each byte: once an even number of seats is in, each place walked is one more place for a divider, and the next seat multiplies them in |
| `corridor_struct.kara` | a `struct Usher` that `passes` each place (`mut ref self`), remembering the last seat and the seats seen, and tells the `ways` (`ref self`) |
| `corridor_fold.kara` | one `fold` over the `enumerate`d places carrying (seats seen, last seat, ways) through tuple patterns, then a `match` on the seats seen with a guard |
| `corridor_solution.kara` | LeetCode's Rust template: the seats as `Vec<usize>` from `bytes().enumerate()` with `|&(_, b)|` and `b'S'`, `is_empty`, `||`, a `const MOD`, the gaps multiplied `as i64`; carried by `karac fix` in four rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's three examples and three
more (no seat, one pair, and three pairs with gaps of two and three),
each with its ways; then the total and a checksum over 2000 random
corridors of 1 to 20 places, a seat one place in 2, 3 or 6 in turn; then
the constraints' largest, 100000 places: every one a seat, seats and
plants in turn, and at random, a seat one place in 4 with the last place
making the seats even. `corridor.py` mirrors the ★ arm and its output is
byte-identical.

No compiler gap was met. `karac fix` carries the template in four rounds
of 7, 2, 1 and 2 edits: Rust's spellings (`Vec<usize>` to `Vec[usize]`,
the `|&(_, b)|` pattern to a bare one, `||` to `or`, `struct Solution;`
to `struct Solution {}`, the adapter's `&String` to `ref String`,
`Solution::` to `.`); then the `.iter()` that Kāra's byte slice needs
after `bytes()`, and the adapter's `as i64` dropped, since an `i32`
widens on return; then `Vec[usize]` to `Vec[i64]`, since Kāra's indices
are `i64`; then the gap product's `as i64` dropped, the gap being an
`i64` already, and the `ref` dropped from the adapter's parameter, which
borrows already.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every set of places between neighbours is tried as the
dividers, and a set counts when every section it makes holds exactly two
seats; no pairing and no gap is assumed. It checks 300 random corridors
of 1 to 12 places, a seat one place in 2, 3 or 6 in turn; then 30 of
seats only; then 30 at random whose last place makes the seats even.
All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the ways are the statement read literally |
| P2 | the corridor reversed: the same ways |
| P3 | the plants at both ends taken away: the same ways |
| P4 | `SSP` put in front: the ways times the plants it now leads and two, or one way when the corridor has no seat |
| P5 | a plant put just after the first seat of every pair: the same ways |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 corridors: checksum 258998214, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal ways was checked against a Python reading of the same
corridors by the same trial of every set of dividers. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Twenty-nine edits to the differential, four to five to each arm, each
run under `karac __mir-llvm-run` and `karac __mir-run`. Nineteen are
kept, three to each arm and a fourth to the states arm. Each kept one is
killed, fails the same way under both backends and not by a crash, and
no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: an odd count let through | P1 151, P2 48, P6 151 |
| M4 | ★: the gap taken inside a pair | P1 35, P2 38, P4 135, P5 64, P6 35 |
| M5 | ★: every gap between seats taken | P1 28, P2 38, P4 72, P5 64, P6 28 |
| M7 | states: a plant never dividing | P1 32, P4 135, P6 32 |
| M8 | states: a full section kept open by a seat | P1 140, P4 286, P5 60, P6 140 |
| M9 | states: the answer one seat short | P1 286, P2 48, P4 74, P6 286 |
| M10 | states: a plant clearing the full section | P1 83, P2 58, P3 65, P4 144, P6 83 |
| M11 | count: the places counted from 0 at a seat | P1 64, P4 94, P6 64 |
| M13 | count: the gap multiplied at a pair's second seat | P1 28, P2 38, P4 114, P5 64, P6 28 |
| M15 | count: the places not reset at a seat | P1 64, P2 43, P3 20, P4 135, P5 64, P6 64 |
| M16 | struct: the plants not skipped | P1 170, P3 116, P4 311, P5 180, P6 170 |
| M19 | struct: the ways started at none | P1 135, P4 74, P6 135 |
| M20 | struct: the gap multiplied at an odd count | P1 81, P4 135, P5 135, P6 81 |
| M22 | fold: the last seat not moved at a pair's first seat | P1 64, P2 43, P3 20, P4 133, P5 64, P6 64 |
| M24 | fold: no seats counted as the ways | P1 74, P6 74 |
| M25 | fold: the gap doubled | P1 64, P4 135, P6 64 |
| M26 | solution: the template stepping by three | P1 5, P2 9, P4 26, P5 27, P6 5 |
| M28 | solution: the adapter dropping the first place | P1 117, P2 95, P3 94, P4 284, P5 26, P6 117 |
| M29 | solution: the template's seats read as plants | P1 172, P3 124, P4 263, P5 194, P6 172 |

P1 and P6 kill all nineteen, P4 seventeen, P5 eleven, P2 ten and P3
six. The answer is a product the literal reading checks place by
place, so every wrong edit shows against it; the other properties say
which part of the reading an edit breaks. P4 puts a pair and a plant in
front, which makes the corridor's first gap the plants it now leads
and two: it sees nearly every edit to a gap (M4, M5, M11, M13, M15, M25)
or to how a gap is closed (M7, M8, M10, M20), and the empty corridor's
one way (M9, M19), since `SSP` alone has one. P5 widens every pair from
inside, which no gap sees: it sees an edit that reads a gap within a
pair (M4, M5, M13) or counts places it should not (M8, M15, M16, M20,
M22). P2 reverses the corridor, which sees an edit that
treats the two ends of the corridor, or the two seats of a pair,
differently (M1, M4, M5, M9, M10, M13, M15, M22, M26, M28). P3 takes away the plants
at both ends, which sees an edit that counts places before the first
seat or after the last (M10, M15, M16, M22, M28, M29).

Of the twenty-nine, ten were not kept, and each fails as a kept one
does: an odd count let through by the count and fold arms, as M1; no
seats counted as one way by the ★ arm and by the template, as M24; the
★ arm's gap one place short and the states arm's seat never closing a
pair, as M11; the count arm's gap multiplied at every seat, as M5; the
struct's gap read from the start and its last seat never moved, as M15;
and the fold's last seat kept at a plant's place, as M7.

## Verification

Every arm prints the same output as `corridor.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.4 s to 1.1 s and the
differential 0.8 s.

## Benchmarks

The bench builds 4 corridors of 100000 places once, a seat one place in
3, the last place making the seats even; then counts the ways through
every corridor 25 times, two neighbouring places swapped before each
count so that no count repeats the one before, with the ★ arm in all
five languages. Each swap builds the corridor anew from slices of the old one; the
Kāra bench copies the old one out of its list by `clone()`, as `karac
fix` proposed for the move out of an index, and the C mirror copies
with `memcpy`. Every implementation prints `100 counts: 830059330 ways in
all, checksum 842492897`.

BENCHTAB
