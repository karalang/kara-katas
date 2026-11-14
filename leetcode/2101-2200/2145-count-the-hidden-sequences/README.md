# 2145. Count the Hidden Sequences

You are given a **0-indexed** array of `n` integers `differences`, which
describes the **differences** between each pair of **consecutive**
integers of a **hidden** sequence of length `(n + 1)`. More formally,
call the hidden sequence `hidden`, then we have that
`differences[i] = hidden[i + 1] - hidden[i]`.

You are further given two integers `lower` and `upper` that describe the
**inclusive** range of values `[lower, upper]` that the hidden sequence
can contain.

- For example, given `differences = [1, -3, 4]`, `lower = 1`,
  `upper = 6`, the hidden sequence is a sequence of length `4` whose
  elements are in between `1` and `6` (**inclusive**).
  - `[3, 4, 1, 5]` and `[4, 5, 2, 6]` are possible hidden sequences.
  - `[5, 6, 3, 7]` is not possible since it contains an element greater
    than `6`.
  - `[1, 2, 3, 4]` is not possible since the differences are not
    correct.

Return *the number of **possible** hidden sequences there are.* If there
are no possible sequences, return `0`.

```
differences = [1,-3,4], lower = 1, upper = 6          ->  2
differences = [3,-4,5,1,-2], lower = -4, upper = 5    ->  4
differences = [4,-7,2], lower = 3, upper = 6          ->  0
```

**Constraints:** `n == differences.length`; `1 <= n <= 10^5`;
`-10^5 <= differences[i] <= 10^5`; `-10^5 <= lower <= upper <= 10^5`.

A hidden sequence is fixed by its first value, and every later value is
the first plus a prefix sum of the differences; so it fits when the
first value lifts the lowest prefix to at least `lower` and keeps the
highest at most `upper`. The starts that fit number the room left,
`upper - lower` less the span from the lowest prefix to the highest, and
one more, or none. O(n).

## Approaches

| file | mechanism |
|---|---|
| `hidden.kara` ★ | the prefix sums walked once, keeping the lowest and the highest, 0 among them for the first value itself |
| `hidden_narrow.kara` | the range of first values, `lower` to `upper` at first, cut down by each prefix p to `lower - p` and `upper - p`, returning 0 as soon as it is empty |
| `hidden_scan.kara` | the prefix sums made by `scan`, Kāra's form that threads an owned state and returns `Some((state, item))`, `chain`ed after the first value's 0 and `collect`ed; their `max` and `min` give the span |
| `hidden_struct.kara` | a `struct Walk` that `step`s along the differences (`mut ref self`), keeping where it is and the lowest and highest it has been, and is asked how many starts it `fits` (`ref self`) |
| `hidden_fold.kara` | one `fold` carrying the triple (where the walk is, its lowest, its highest), its closure taking a tuple pattern, and the triple taken apart by a `let` pattern |
| `hidden_solution.kara` | LeetCode's Rust template: the running sum and its lowest and highest bound by one `let (mut cur, mut mn, mut mx)` of `0i64`s, `for &d in &differences`, and `as i64` casts; carried by `karac fix` in two rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's three examples and three
more (a walk that stays put in a range of one value, the widest single
step, and a step too wide for its range), each with its count; then the
total and a checksum over 2000 random walks of 1 to 12 steps of up to 5
or 10000 either way in turn, within bounds up to ten steps either side
of 0; then the constraints' largest, 100000 differences between -100000
and 100000: every one 1, swinging the widest each way in turn, and at
random by up to 10. `hidden.py` mirrors the ★ arm and its output is
byte-identical.

No compiler gap was met. `karac fix` carries the template in two rounds
of 16 and 7 edits: Rust's spellings (`Vec<..>` to `Vec[..]`, `let (mut
cur, mut mn, mut mx)` to `let mut (cur, mn, mx)`, `for &d in
&differences` to `for d in ref differences`, the `&x` pattern to `x`,
`struct Solution;` to `struct Solution {}`, the adapter's `&Vec` to
`ref Vec`, `Solution::` to `.`); then the three `0i64` suffixes and the
`as i64` casts dropped, since an `i32` widens to the `i64` sum on its
own, and the `ref` dropped from the adapter's parameter, which borrows
already. The sum stays an `i64`: a walk of 100000 steps of 100000 each,
which reaches 10^10, counts 0 sequences rather than overflowing.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every first value from `lower` to `upper` is tried, the
sequence it starts walked out by the differences, and it counts when
every value stays between the bounds; no prefix sum is kept apart and no
span is measured. It checks 300 random walks of 1 to 8 steps of up to 3
either way, within bounds up to 15 either side of 0; then 30 whose every
step is 0; then 30 whose bounds are one value. All 360 are drawn before
any arm answers.

| | property |
|---|---|
| P1 | the count is the statement read literally |
| P2 | the walk taken backwards, its differences reversed and turned round: the same count |
| P3 | every difference turned round: the same count |
| P4 | the bounds set to the lowest and highest the walk reaches from 0: one |
| P5 | the walk followed by its own way back: the same count |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 walks: checksum 874464050, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal counts was checked against a Python reading of the same
walks by the same trial of every first value. On a failure it prints
the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, five to six to each arm, each run
under `karac __mir-llvm-run` and `karac __mir-run`. Seventeen are kept,
three to each Kāra arm and two to the Rust-template arm. Each kept one
is killed, fails the same way under both backends and not by a crash,
and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the lowest started above the first value | P1 68, P2 123, P3 128, P4 83, P5 68, P6 68 |
| M2 | ★: no room for the last start | P1 261, P4 360, P6 261 |
| M5 | ★: the span read as the highest alone | P1 189, P2 278, P3 292, P4 210, P6 189 |
| M7 | narrow: the top narrowed by the step, not the sum | P1 143, P2 175, P3 195, P4 191, P5 81, P6 143 |
| M8 | narrow: an empty range let through | P1 81, P6 81 |
| M10 | narrow: the bounds swapped in the narrowing | P1 258, P4 322, P6 258 |
| M11 | scan: the first value's 0 left out | P1 128, P2 137, P4 156, P5 128, P6 128 |
| M13 | scan: the sum yielded before the step | P1 124, P2 137, P4 162, P5 124, P6 124 |
| M14 | scan: the highest read as the last prefix | P1 192, P2 274, P3 295, P4 209, P5 274, P6 192 |
| M18 | struct: the highest set by the step | P1 101, P2 194, P3 189, P4 121, P5 71, P6 101 |
| M19 | struct: a full room counted as none | P1 21, P4 360, P6 21 |
| M20 | struct: the walk started at the bottom | P1 60, P2 129, P3 128, P4 73, P5 60, P6 60 |
| M21 | fold: the lowest taken before the step | P1 55, P2 123, P3 124, P4 75, P5 55, P6 55 |
| M22 | fold: the highest never carried | P1 86, P3 143, P4 112, P5 132, P6 86 |
| M24 | fold: the span added to the room | P1 200, P2 284, P3 307, P4 210, P6 200 |
| M26 | solution: the template's lowest from the highest | P1 163, P2 197, P3 232, P4 190, P5 231, P6 163 |
| M30 | solution: the template's steps all taken upward | P1 147, P4 220, P5 178, P6 147 |

P1 and P6 kill all seventeen, P4 sixteen, P2 and P5 eleven each, and P3
ten. P4 sets the bounds to the very span the walk covers from 0, where
exactly one first value fits; it sees every edit but the narrowing that
lets an empty range through (M8), which only goes wrong when no start
fits. P2 and P3 take the walk backwards or upside down, which keeps its
span; they see an edit that measures the span from one end of the walk
or from one side of it: a lowest or highest misread or never carried
(M1, M5, M14, M18, M20, M21, M26, and for P3 alone M22), a span added
rather than taken away (M24), and the top narrowed by the step (M7),
and P2 sees the
first value's 0 left out and the sum yielded a step late (M11, M13),
which change with the walk's direction but not with its sign. P5 walks
out and back, which keeps the span and ends where it began; it sees an
edit that lets the end of the walk count apart from its middle (M1,
M7, M11, M13, M14, M18, M20, M21, M22, M26) and the template's steps
all taken upward (M30), which the way back doubles.

Of the thirty-one, fourteen were not kept. One does not compile:
yielding the step itself from `scan` gives items that are references,
not the `i64`s the `Vec` collects, and the typechecker says so. One is
equivalent: the struct's step taken away rather than added, which walks
the mirror image, of the same span. Ten fail as a kept one does: a
negative count let through by the ★ arm and by the template, as M8; the
★ arm's highest kept as the last, as M14; the narrowing from below
dropped, the scan's lowest read as the first prefix and the struct's
lowest never moved, as M5; the narrow range one short, as M2; the
fold's room test turned, as M19; the adapter's bounds swapped, as M10;
and the adapter dropping the first difference, as M11. Two are killed
with checks of their own but were left out because their arms keep
their share: the fold's walk started at 1 (P1 180, P2 179, P3 166, P4
223, P5 58, P6 180) and the template's room one too many (P1 279, P4
360, P6 279).

## Verification

Every arm prints the same output as `hidden.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.6 s to 1.6 s and the
differential 0.5 s.

## Benchmarks

The bench builds 20 walks of 100000 differences of up to 10 either way
once; then counts every walk 200 times between -100000 and 100000, one
difference redrawn before each count so that no count repeats one
before, with the ★ arm in all five languages. Every implementation
prints `4000 solves: 786836986 sequences in all, checksum 715281587`.

BENCHTAB
