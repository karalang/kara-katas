# 2188. Minimum Time to Finish the Race

You are given a **0-indexed** 2D integer array `tires` where `tires[i] =
[fi, ri]` indicates that the `ith` tire can finish its `xth` successive
lap in `fi * ri^(x-1)` seconds.

- For example, if `fi = 3` and `ri = 2`, then the tire would finish its
  `1st` lap in `3` seconds, its `2nd` lap in `3 * 2 = 6` seconds, its
  `3rd` lap in `3 * 2^2 = 12` seconds, etc.

You are also given an integer `changeTime` and an integer `numLaps`.

The race consists of `numLaps` laps and you may start the race with
**any** tire. You have an **unlimited** supply of each tire and after
every lap, you may **change** to any given tire (including the current
tire type) if you wait `changeTime` seconds.

Return *the **minimum** time to finish the race.*

```
tires = [[2, 3], [3, 4]],          changeTime = 5, numLaps = 4  ->  21
tires = [[1, 10], [2, 2], [3, 4]], changeTime = 6, numLaps = 5  ->  25
```

**Constraints:** `1 <= tires.length <= 10^5`; `tires[i].length == 2`;
`1 <= fi, changeTime <= 10^5`; `2 <= ri <= 10^5`; `1 <= numLaps <=
1000`.

A race is runs on one tire with a change between each two. A lap that
costs more than a change and a fresh first lap, f + changeTime, is
never worth running, and with r at least 2 a lap's time at least
doubles, so no run is worth more than about 18 laps. So the least time
for each length of run on one tire is found first, over every tire, and
then the least time for n laps is, over the length k of the last run,
the least for n - k laps, a change, and that run. O(tires * 18 + laps *
18).

## Approaches

| file | mechanism |
|---|---|
| `race.kara` ★ | the least time for each length of run, over every tire while a lap still pays, in a list that grows as runs do; then the laps bottom up, the last run paying no change |
| `race_memo.kara` | top down: the least time for n laps the least, over the last run, of the time for n - k laps, a change, and the run; each answer kept in a `Vec[i64]` memo passed `mut ref`, and no laps a change taken back |
| `race_pareto.kara` | the tires `sort`ed as pairs and thinned: a tire kept only when its ratio is below every kept tire's, since one no faster on its first lap and no slower to tire never wins; then the runs and the laps over the few left |
| `race_struct.kara` | a `struct Stint` of the least time for each length of run, made `of` the tires, a change time and the laps; it is `extend`ed by a tire (`mut ref self`) and says its `longest` run and the time to `finish` (`ref self`) |
| `race_iter.kara` | each tire's laps a `successors` sequence, `take_while` they pay, summed by `scan`, `collect`ed; each length's least by `filter_map` over `get` and `min`; the laps a `fold` that grows the list of least times, each a `min` over the runs |
| `race_solution.kara` | LeetCode's Rust template: `Vec<Vec<i32>>`, `vec![i64::MAX; 20]` and `vec![i64::MAX; n + 1]`, `for t in &tires`, `0i64`, `as usize`, `struct Solution;`, `Solution::`; carried by `karac fix` in two rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's two examples and four more
(one lap, a change too dear to make, a change cheaper than any second
lap, and the constraints' largest numbers on one tire over 1000 laps),
each with its time; then the total and a checksum over 2000 random
races of 1 to 10 tires: small numbers and 1 to 20 laps, and numbers up
to the constraints' and 1 to 1000 laps, in turn; then the constraints'
largest, 10^5 tires and 1000 laps: every tire [1, 2] with a change of
1, and tires at random with a change of 10^5 and of 1. `race.py`
mirrors the ★ arm and its output is byte-identical.

The iterator arm found a compiler bug, now fixed (B-2026-11-15-30):
`successors(Some(f), |lap| Some(lap * r))` inside the `map` over the
tires typed `lap` as the tires' `ref Vec[i64]`, "type 'ref Vec[i64]'
does not implement trait Mul". A generic free function called inside a
method call's closure read its own type parameter `T` as the method's
receiver's `T`. The same call with its seed taken straight from a
`v.iter()`, `Some(x)` with `x: ref i64`, is refused with E0509 and no
fix, where `Some(*x)` is the mend; kara B-2026-11-15-34 asks for the
diagnostic to name the seed and offer it. The arm binds `let f = t[0];`
first. Its `scan` was written as Rust's, writing the state through
`*sum`; `karac check` refuses that with a fix, and `karac fix` rewrites
it to Kāra's `|sum, lap| { let sum = sum + lap; Some((sum, sum)) }`, the
state passed by value.

`karac fix` carries the template in two rounds of 16 and 5 edits:
Rust's spellings (`Vec<..>` to `Vec[..]`, `i64::MAX` to `i64.MAX`, `for t
in &tires` to `for t in ref tires`, the `&x` pattern, `struct
Solution;` to `struct Solution {}`, and `Solution::` to `.`, among
them); then the `usize`s and the macros: `num_laps as usize` to `as
i64`, each `vec![v; n]` to `Vec.filled(n, v)`, the `i64` suffix of `0i64`
dropped, and the adapter's widening `as i64`.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every race tried, lap by lap, each lap either run on the
tire already on, at f * r^(x - 1), or on a fresh tire of any kind after
a change, and the least total kept. No runs worked out first and no
table over the laps. It checks 300 random races of 1 to 3 tires with f
of 1 to 5 and r of 2 to 4, a change of 1 to 10 and 1 to 6 laps; then 30
of one tire; then 30 with a change of 20 to 40. All 360 are drawn
before any arm answers.

| | property |
|---|---|
| P1 | the time is the statement read literally |
| P2 | the tires reversed: the same time |
| P3 | a tire added one second slower on its first lap than the first one there: the same time |
| P4 | a change one second dearer: a time no less, and at most the laps less one more |
| P5 | the time at least the laps times the least f, and at most a fresh tire of the least f every lap |
| P6 | each arm agrees with at least three of the other five |

P2 holds since the tires are a set to choose from. P3 holds since the
new tire is slower than an old one on every lap. P4 holds since every
race costs at least as much with the dearer change, and the best race
before, with at most laps - 1 changes, costs at most that much more.
P5 holds since no lap is faster than the least f, and a fresh tire of
the least f every lap is one race.

The differential prints `360 races: checksum 947616673, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading of the same
races. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Thirty edits to the differential, five to each Kāra arm, seven to the
pareto arm and three to the template, each run under `karac
__mir-llvm-run` and `karac __mir-run`. Seventeen are kept, three to
each Kāra arm and two to the Rust-template arm. Each kept one is
killed, fails the same way under both backends and not by a crash, and
no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M2 | ★: the last run paying a change too | P1 145, P6 145 |
| M3 | ★: a later tire's run kept even when slower | P1 90, P2 148, P3 260, P4 9, P5 58, P6 90 |
| M4 | ★: each lap's time grown by r + 1 | P1 189, P6 189 |
| M6 | memo: no laps costing nothing | P1 360, P4 149, P5 271, P6 360 |
| M7 | memo: the longest run never tried | P1 297, P4 25, P5 145, P6 297 |
| M9 | memo: the first tire only | P1 121, P2 201, P5 99, P6 121 |
| M12 | pareto: a tire kept on a larger ratio | P1 6, P6 6 |
| M15 | pareto: runs of two laps never tried | P1 165, P4 4, P6 165 |
| M30 | pareto: the tires sorted by ratio | P1 107, P2 66, P5 87, P6 107 |
| M16 | struct: the longest run one short | P1 152, P4 10, P6 152 |
| M19 | struct: every run's first lap counted twice | P1 360, P4 9, P5 206, P6 360 |
| M20 | struct: a change free | P1 213, P4 174, P5 102, P6 213 |
| M22 | iter: each length's slowest run, not its least | P1 153, P3 221, P4 22, P5 105, P6 153 |
| M23 | iter: the run index one off | P1 92, P4 26, P5 32, P6 92 |
| M24 | iter: the scan's laps, not their sum | P1 213, P4 15, P6 213 |
| M26 | solution: the adapter's laps one more | P1 360, P4 98, P5 251, P6 360 |
| M27 | solution: the change counted twice | P1 360, P4 191, P5 326, P6 360 |

P1 and P6 kill all seventeen, P4 twelve, P5 eleven, P2 three and P3
two. P5's bounds are wide, and it misses an edit that only makes a race
dearer or misses a cheaper one: the last run paying a change (M2), r +
1 (M4), a larger ratio kept (M12), no runs of two (M15), the longest
one short (M16), and the scan's laps (M24). P4 misses an edit whose
answer is still the time of some race, which moves with the change as
a race's does: M2, M4, the first tire only (M9), M12, and the tires
sorted by ratio (M30). P2 reverses the tires, and sees the edits that
depend on their order: a later tire's run kept (M3), the first tire
only (M9), and the sort by ratio alone (M30), which keeps the tires of
one ratio in the order given. P3 adds a tire slower than another, and
sees only the edits that let it win: a later tire's run kept (M3) and
each length's slowest (M22).

Of the thirty, thirteen were not kept. Two are equivalent: the pareto
arm's tire kept on an equal ratio (M11), which is never better and
never worse than the one kept before it; and the iter arm's lap run
only while cheaper than a change and a first lap (M21), since a lap of
exactly that costs what changing for it does. Three crash: the ★ arm's
lap run only while no dearer than a change (M1), which with a change
below f leaves no run of one lap to read; the struct arm's runs cut one
short of the laps (M18), which with one lap leaves none; and the
template's run of one lap never tried (M28), whose `i64.MAX` for one
lap then overflows. Six fail as a kept one does: the ★ arm's runs of
one lap, as M4; the memo arm's later run replacing, as M3; the pareto
arm's first tire only, as M12; and the pareto arm's change left on at
the end, the struct arm's no laps with no change to take back, and the
iter arm's laps from 0, each a change more on every race, as M6. Two
were left out to keep three to an arm: the memo arm's memo kept one too
few (M8) and the pareto arm's first lap one slower (M29).

## Verification

Every arm prints the same output as `race.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the ★, struct, memo and pareto arms take 1.4 s
to 2.2 s, the template 3.8 s and the iter arm 10 s. The differential
takes 0.7 s.

## Benchmarks

The bench builds 10^5 tires once, with f of 1 to 100 and r of 2 to 5,
so that runs reach a dozen laps; then solves 5000 windows of 100 tires,
each at a random start and with a change of 1 to 10^5, over 1000 laps,
with the ★ arm in all five languages. C works over a pointer to the
window's pairs, Rust and Go over a slice of the row; Kāra and Python
copy each window into a list of lists of their own. Every
implementation prints `5000 solves: checksum 325679308`.

BENCHTAB
