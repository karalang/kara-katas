# 2224. Minimum Number of Operations to Convert Time

You are given two strings `current` and `correct` representing two
**24-hour times**, formatted as `"HH:MM"`, from `00:00` to `23:59`.

In one operation you can increase the time `current` by `1`, `5`, `15`
or `60` minutes, as many times as you like.

Return *the **minimum number of operations** needed to convert
`current` to `correct`*.

```
current = "02:30", correct = "04:35"  ->  3
current = "11:00", correct = "11:01"  ->  1
```

**Constraints:** `current` and `correct` are in the format `"HH:MM"`;
`current <= correct`.

Each step length divides the next (1, 5, 15, 60), so the greedy choice
is optimal: the gap in minutes is cut by as many 60s as fit, then 15s,
5s and 1s. O(1).

## Approaches

| file | mechanism |
|---|---|
| `convert.kara` ★ | each time read from its four digits (`filter` out the colon, `collect`), the gap cut by `for step in [60, 15, 5, 1]` with `/` and `%=` |
| `convert_dp.kara` | no trust in greed: the fewest steps for every gap from 0 up, each the best of one step of 1, 5, 15 or 60 after a smaller gap, as in coin change; the times read by `split(":")` and `i64.parse`; O(gap) |
| `convert_walk.kara` | the clock walked forward one operation at a time, always the largest step that does not pass the correct time, the hours and minutes kept apart and the minutes carried into the hours at 60; O(answer) |
| `convert_struct.kara` | a `struct Time` with `parse`, `minutes` and `until` (`ref self`), and an `enum Step` of the four operations with `length`, tried from the longest |
| `convert_iter.kara` | the gap by `zip`ping the two times' digits with their place values in minutes (600, 60, 10, 1) and `sum`ming the differences, the digits read by a closure bound to a `let`; then a `fold` over the steps carrying the gap left and the operations |
| `convert_solution.kara` | LeetCode's Rust template: two `String`s in, `i32` out, a nested `fn minutes` over `split(':')` and `parse::<i32>()`, and the gap cut in a `for &step in [60, 15, 5, 1].iter()` loop; carried by `karac fix`, with one literal suffixed by hand |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's two examples and four
more (no change, the whole day, one of each step, and four of the
smallest), each with its count; then a checksum of 3000 random pairs,
the earlier time first; then the total over every pair of the times
00:00, 00:29, 00:58, ... in order. `convert.py` mirrors the ★ arm and
its output is byte-identical.

`karac fix` carries the template through the Rust syntax in one round of
12 edits: the nested `fn minutes` moved out to the top level (Kāra has
no nested items), `&str` to `Str`, `':'` to `":"`,
`parts.next().unwrap().parse()` with its annotation to
`i32.parse(parts.next().unwrap())`, the `&` dropped from the arguments
and from `&step`, `ops` typed `i32`, `struct Solution;` to `struct
Solution {}`, `Solution::` to `Solution.`, and the adapter's `as i64`
removed. What it leaves is `diff / step` and `diff %= step` reported
twice as a narrowing from `i64` to `i32`: an unsuffixed literal beside
an `i32` keeps `i64`, so the steps in `[60, 15, 5, 1]` are `i64`, and
karac offers no fix (kara B-2026-11-17-143). The first step was written
`60i32` by hand, after which `karac fix` drops the `.iter()` too, a
`for` walking an array by value.

The iter arm's closure was first written `|time: String| -> Vec[i64] {
... collect() }`, Rust's return type on a closure. `karac fix` moves
that type onto the binding, since the `collect` needs it, but wrote the
parameter owned, `Fn(String) -> Vec[i64]`, where a closure's bare
parameter borrows: the next round made both callers take their times
owned and cloned them. karac now writes `Fn(ref String) -> Vec[i64]`
(kara B-2026-11-17-141), which is what the arm holds. Written first
with no type on the parameter, `|time| { time.chars()... }`, the closure
got only an internal "not lowered yet" error naming no cause (kara
B-2026-11-17-144).

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: a breadth-first search over the minutes of the day from the
current time, each of the four operations tried from every minute
reached and none past the correct time, until the correct time is
reached; no division and no greed. It checks 300 random pairs, the
earlier first; then 30 with the two times equal; then 30 a whole number
of hours apart, give or take a minute. All 360 are drawn before any arm
answers.

| | property |
|---|---|
| P1 | the answer is the fewest operations, read literally |
| P2 | both times moved by the same minutes within the day: the same answer |
| P3 | at least the gap in whole hours rounded up, at most the gap, and 0 exactly when the times are equal |
| P4 | through a time between them: no more than the two legs together |
| P5 | the correct time an hour later, where the day allows: one more |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 cases: checksum 624196588, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that tries
every number of hour, quarter and five steps that fits in the gap and
fills the rest with single minutes. On a failure it prints the first
ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, five to each Kāra arm and six to
the Rust-template arm, each run under `karac __mir-llvm-run`, and the
kept ones under `karac __mir-run` too. Seventeen are kept, three to each
Kāra arm and two to the Rust-template arm. Each kept one is killed,
fails the same way under both backends and not by a crash, and no two
kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the quarter step missed | P1 217, P6 217 |
| M2 | ★: the minutes' tens read as ones | P1 214, P2 163, P3 7, P4 11, P6 214 |
| M5 | ★: an hour of fifty minutes | P1 266, P5 173, P6 266 |
| M7 | dp: the table one gap short | P1 330, P3 330, P5 331, P6 330 |
| M8 | dp: a long step counted twice | P1 327, P5 331, P6 327 |
| M9 | dp: the hours read by a hundred | P1 311, P2 106, P5 331, P6 311 |
| M11 | walk: the carry losing a minute | P1 282, P2 104, P3 11, P4 3, P5 290, P6 282 |
| M12 | walk: a quarter taken where only a five fits | P1 125, P4 14, P6 125 |
| M13 | walk: the correct time's minute tens dropped | P1 242, P2 219, P3 16, P4 49, P5 35, P6 242 |
| M16 | struct: a quarter of sixteen minutes | P1 213, P4 8, P6 213 |
| M17 | struct: the gap taken backwards | P1 330, P3 330, P4 237, P5 331, P6 330 |
| M20 | struct: the minutes read from the hours | P1 285, P2 106, P3 11, P5 331, P6 285 |
| M21 | iter: a place value of a hundred | P1 282, P2 176, P3 42, P4 32, P5 331, P6 282 |
| M22 | iter: the fold keeping the whole gap | P1 327, P3 327, P4 237, P5 331, P6 327 |
| M24 | iter: the fold seeded with one operation | P1 360, P3 33, P6 360 |
| M27 | solution: the minutes and hours swapped | P1 298, P2 106, P3 187, P4 153, P5 44, P6 298 |
| M30 | solution: the remainder counted for the quotient | P1 321, P3 66, P5 331, P6 321 |

P1 and P6 kill all seventeen, P5 twelve, P3 eleven, P4 nine and P2
seven. P5, exactly one more operation an hour later, holds for the true
count whatever the gap, so it catches the edits whose count does not
grow by one with a whole hour: the hour step changed (M5), a step
weighed wrong (M8, M30), or a time misread. P2 moves both times
together, so it catches only the edits that read a time's digits wrong
(M2, M9, M11, M13, M20, M21, M27), where the error depends on the time
and not on the gap.

Of the thirty-one, fourteen were not kept, and none survives, crashes or
differs between the backends. Nine fail as a kept one does: the ★ arm's
gap never cut (M3) as the iter arm's fold keeping it (M22); the ★ arm's
times the wrong way round, the iter arm's digits subtracted the wrong
way and the template's times handed in swapped (M4, M23, M29) as the
struct arm's gap backwards (M17); the dp arm's minute step free and the
iter arm's correct time zipped with itself (M10, M25) as the table one
short (M7); the struct arm's gap cut by the count and the template's
steps smallest first (M18, M26) as the long step counted twice (M8);
and the template's count from one (M28) as the fold seeded with one
(M24). Five fail their own way and are left out for the count of three
(two for the template): the dp arm's five step left out (M6), the walk
arm's two operations a step and its hour taken only past an hour (M14,
M15), the struct arm's hour step skipped (M19), and the template's gap
a minute long (M31).

## Verification

Every arm prints the same output as `convert.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the template, struct, walk, ★ and iter arms
take 0.2 s to 0.4 s, the dp arm 2.2 s, and the differential 1.7 s.

## Benchmarks

The bench builds the 1440 times of the day as `"HH:MM"` once, then
answers 2 * 10^6 random pairs of them, the earlier first, with the ★
arm in all five languages. Every implementation reads a time's four
digits into a growable list as the ★ arm does, except C, which fills a
four-element array. Every implementation prints `2000000 pairs:
checksum 289196929`.

BENCHTAB
