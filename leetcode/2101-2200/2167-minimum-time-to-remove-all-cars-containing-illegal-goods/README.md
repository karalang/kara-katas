# 2167. Minimum Time to Remove All Cars Containing Illegal Goods

You are given a **0-indexed** binary string `s` which represents a
sequence of train cars. `s[i] = '0'` denotes that the `i`th car does
**not** contain illegal goods and `s[i] = '1'` denotes that the `i`th
car does contain illegal goods.

As the train conductor, you would like to get rid of all the cars
containing illegal goods. You can do any of the following three
operations **any** number of times:

1. Remove a train car from the **left** end (i.e., remove `s[0]`) which
   takes 1 unit of time.
2. Remove a train car from the **right** end (i.e., remove
   `s[s.length - 1]`) which takes 1 unit of time.
3. Remove a train car from **anywhere** in the sequence which takes 2
   units of time.

Return *the **minimum** time to remove all the cars containing illegal
goods*.

Note that an empty sequence of cars is considered to have no cars
containing illegal goods.

```
s = "1100101"  ->  5
s = "0010"     ->  2
```

**Constraints:** `1 <= s.length <= 2 * 10^5`; `s[i]` is either `'0'`
or `'1'`.

The train is cut once: the cars before the cut are cleared from the
front or from the middle, and the cars after it are taken from the
back. Clearing the first k cars takes either every one of them, k, or 2
for each car with goods, whichever is less at each car, so one pass
from the front gives every cut. O(n).

## Approaches

| file | mechanism |
|---|---|
| `removal.kara` ★ | one pass over `chars().enumerate()`: the least time that clears the cars so far, `min(that + 2, i + 1)` at a car with goods, and the cars after it taken from the back |
| `removal_split.kara` | two tables over `bytes()`, the least time that clears the first k cars built forwards and the cars from k on built backwards, and the least sum at a cut |
| `removal_prefix.kara` | prefix sums of the goods: taking a cars from the front and the cars from e on leaves `a + (n - e) + 2 * (P[e] - P[a])`, and the least `a - 2 * P[a]` up to each e is kept as the walk goes |
| `removal_struct.kara` | a `struct Clearing` of the least time to clear each run of cars from one end, made `from` a list (`own` it) and asked the time `of` its first k cars; the train cleared from the front and, reversed, from the back, and cut by `map` and `min` where the two add up least |
| `removal_iter.kara` | the ★ arm's walk as one `fold` over `bytes().iter().enumerate()`, its state a tuple of the time that clears the cars so far and the best answer |
| `removal_solution.kara` | LeetCode's Rust template: `s.as_bytes()`, `for (i, &b) in bytes.iter().enumerate()`, `std::cmp::min`, `i as i32`; carried by `karac fix` in two rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's two examples and five
more (one car without goods and one with, every car with goods, goods
only in the middle, and goods at both ends), each with its time; then
the total and a checksum over 2000 random trains of 1 to 20 cars, a car
with goods 1 in 2, 1 in 4 or 1 in 8 in turn; then the constraints'
largest, 200000 cars at random, every one with goods, and goods in
every other car. `removal.py` mirrors the ★ arm and its output is
byte-identical.

The iterator arm was carried by `karac fix` in one edit: the `.iter()`
between `bytes()`, a `Slice[u8]`, and `enumerate`.

`karac fix` carries the template in two rounds of 5 and 3 edits: Rust's
spellings (the `for` pattern's `(i, &b)` to `(i, b)`, `std::cmp::min` to
`min`, `struct Solution;` to `struct Solution {}`, `&str` to `Str`,
`Solution::` to `.`); then `as_bytes()` to `bytes()`, `let mut left = 0`
to `let mut left: i32 = 0`, which Rust types from the `i32` it is
compared with and Kāra keeps at the default `i64` (design.md §8
Literals), and the adapter's widening `as i64` dropped.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every count of cars taken from the front and from the back
that leaves a train between them, each car with goods left there taken
from the middle for 2, and the least time; no running minimum. It
checks 300 random trains of 1 to 12 cars, a car with goods 1 in 2, 1 in
4 or 1 in 8 in turn; then 30 with goods in 7 cars in 8; then 30 with
goods only between two runs of cars without. All 360 are drawn before
any arm answers.

| | property |
|---|---|
| P1 | the time is the statement read literally |
| P2 | the train reversed: the same time |
| P3 | the time at least the cars with goods, and at most every car and at most 2 for each car with goods |
| P4 | the goods taken out of one car: the time no more, and at most 2 less |
| P5 | the last car taken off a train of two or more: the time no more, and at most 1 less |
| P6 | each arm agrees with at least three of the other five |

P4 holds since a way to clear the train without those goods clears the
train with them once that car is taken from the middle too, for 2. P5
holds since a way to clear the shorter train clears the longer one with
one more car from the back, or the same one taken to its end, for 1.

The differential prints `360 trains: checksum 778389050, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading of the same
trains. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Thirty edits to the differential, four to six to each arm, each run
under `karac __mir-llvm-run` and `karac __mir-run`. Seventeen are kept,
three to each Kāra arm and two to the Rust-template arm. Each kept one
is killed, fails the same way under both backends and not by a crash,
and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a car with goods always taken from the middle | P1 96, P2 131, P6 96 |
| M3 | ★: one car too many from the back | P1 336, P3 172, P6 336 |
| M4 | ★: the cars without goods paid for | P1 333, P3 284, P4 200, P6 333 |
| M5 | split: the back taking one car more | P1 102, P2 120, P5 43, P6 102 |
| M8 | split: a car without goods clearing the front | P1 224, P2 129, P3 224, P5 54, P6 224 |
| M29 | split: a car without goods clearing the back | P1 236, P2 129, P3 236, P4 35, P6 236 |
| M11 | prefix: the empty front never taken | P1 204, P2 134, P3 154, P6 204 |
| M12 | prefix: the best one under the whole train | P1 24, P3 24, P6 24 |
| M28 | prefix: every car counted as goods | P1 336, P3 255, P6 336 |
| M13 | struct: the back cleared unreversed | P1 118, P2 181, P3 73, P4 35, P5 50, P6 118 |
| M14 | struct: the back asked of the same cut | P1 279, P3 279, P6 279 |
| M15 | struct: a run taken whole for one more | P1 188, P3 42, P5 40, P6 188 |
| M17 | iter: the back never counted | P1 292, P2 111, P3 221, P6 292 |
| M19 | iter: a car with goods from the middle for 1 | P1 188, P6 188 |
| M26 | iter: each car behind paid for 2 | P1 102, P2 131, P5 63, P6 102 |
| M20 | solution: two cars too many from the back | P1 360, P3 172, P6 360 |
| M22 | solution: the front one car short | P1 156, P2 134, P3 60, P6 156 |

P1 and P6 kill all seventeen, P3 thirteen, P2 nine, P5 five and P4
three. P3 bounds the time by the goods and the cars; it sees an edit
that charges too much or too little at either end, and misses those
whose wrong time still falls between (M1, M5, M19, M26). P2 reverses
the train, which a right time ignores; it sees an edit that treats the
front and the back differently, and misses those whose error is the
same for a train and its reverse, such as one car too many from the
back at every cut (M3, M4, M12, M14, M15, M19, M20, M28). P5 takes off the last car and sees an edit
whose time jumps by more than one car's worth (M5, M8, M13, M15, M26),
and P4 takes the goods out of one car and sees the edits that charge a
car without goods (M4) or make the train's two ends disagree (M13,
M29).

Of the thirty, thirteen were not kept. Five are equivalent. The split
arm's cut after the last car is never below the cut before it, since
taking the last car from the back costs at most what clearing it from
the front does. The prefix arm's least front taken after the best only
loses, at the last car, the cut that takes every car from the front,
which costs n, as the best starts. The ★ arm's best started past every
train loses only the train taken whole from the back, which the cut
after the first car never exceeds. The iterator arm's cap on the time
that clears the front at a car without goods never binds, since that
time is at most the cars so far. And the template's adapter reversing
the train gives the same time, as P2 says. Eight fail as a kept one
does: the ★ arm's front one car short, as M22; the split arm's back read
from the front, as M13; the prefix arm's goods counted once in the
front, as M1; the struct arm's car without goods paid for, as M28; the
iterator's fold started one under the train and the template's answer
started there, as M12; the prefix arm's one car too many from the back,
as M3; and the split arm's car with goods from the middle for 1, as
M19.

## Verification

Every arm prints the same output as `removal.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 1.2 s to 1.6 s, but for the struct
arm, 2.8 s, which builds a list of times from each end and a reversed
copy of the train; the differential takes 0.4 s.

## Benchmarks

The bench builds one train of 400000 cars once, a car with goods 1 in
3; then solves 100 windows of 200000 cars, each at a random start, so
that no solve repeats one before, with the ★ arm in all five languages:
C over a pointer and a length, the others over a slice of the text.
Every implementation prints `100 solves: checksum 287276259`.

BENCHTAB
