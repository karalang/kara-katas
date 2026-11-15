# 2162. Minimum Cost to Set Cooking Time

A generic microwave supports cooking times for:

- at least `1` second.
- at most `99` minutes and `99` seconds.

To set the cooking time, you push **at most four digits**. The microwave
normalizes what you push as four digits by **prepending zeroes**. It
interprets the **first** two digits as the minutes and the **last** two
digits as the seconds. It then **adds** them up as the cooking time. For
example,

- You push `9` `5` `4` (three digits). It is normalized as `0954` and
  interpreted as `9` minutes and `54` seconds.
- You push `0` `0` `0` `8` (four digits). It is interpreted as `0`
  minutes and `8` seconds.
- You push `8` `0` `9` `0`. It is interpreted as `80` minutes and `90`
  seconds.
- You push `8` `1` `3` `0`. It is interpreted as `81` minutes and `30`
  seconds.

You are given integers `startAt`, `moveCost`, `pushCost`, and
`targetSeconds`. **Initially**, your finger is on the digit `startAt`.
Moving the finger above **any specific digit** costs `moveCost` units of
fatigue. Pushing the digit below the finger **once** costs `pushCost`
units of fatigue.

There can be multiple ways to set the microwave to cook for
`targetSeconds` seconds but you are interested in the way with the
minimum cost.

Return *the **minimum cost** to set* `targetSeconds` *seconds of cooking
time*.

Remember that one minute consists of `60` seconds.

```
startAt = 1, moveCost = 2, pushCost = 1, targetSeconds = 600  ->  6
startAt = 0, moveCost = 1, pushCost = 2, targetSeconds = 76   ->  6
```

**Constraints:** `0 <= startAt <= 9`; `1 <= moveCost, pushCost <= 10^5`;
`1 <= targetSeconds <= 6039`.

A time is written at most two ways: as its minutes and seconds, and with
one minute fewer and 60 seconds more, each when both sides fit in two
digits. Leading zeros cost pushes and never save a move, so each way is
pushed without them, and the cheaper way is the answer. O(1).

## Approaches

| file | mechanism |
|---|---|
| `cooking.kara` ★ | each way that fits written as the number `minutes * 100 + seconds`, whose text has no leading zeros; its `chars` walked from the start digit, a move for each change of digit and a push for each digit |
| `cooking_minutes.kara` | every count of minutes from 0 to 99 tried, the seconds what is left, kept when 0 to 99; the four digits by `/ 10` and `% 10`, the leading zeros skipped until a digit other than 0 starts the number |
| `cooking_pad.kara` | each way printed as the microwave reads it, `f"{m:02}{s:02}"`, the zeros in front taken off one at a time by a `while let` on `strip_prefix`; the moves the places where a digit differs from the one before |
| `cooking_struct.kara` | a `struct Finger` that keeps where it rests and what it has spent: `push` moves it if it must and pushes (`mut ref self`), and `type_number` pushes a number's digits highest first by recursing on `n / 10` |
| `cooking_iter.kara` | the minutes by `filter_map` to the ways that fit, each way's digits from its text with the start digit put in front by `once` and `chain`, the moves counted by `windows(2)`, the least by `min` |
| `cooking_solution.kara` | LeetCode's Rust template: a closure `cost` over `[m / 10, m % 10, s / 10, s % 10]` that skips the leading zeros and returns `i32::MAX` for a way that does not fit, `|..| -> i32`, `for &d in &digits[i..]`; carried by `karac fix` in two rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's two examples and four more
(one second, the longest time, 100 minutes that only 99:60 can write,
and a time whose shorter way costs more), each with its cost; then the
total and a checksum over 2000 random settings, the costs up to 10,
1000 or 10^5 in turn; then every time the constraints allow from every
start digit, once moving dear and once pushing dear. `cooking.py`
mirrors the ★ arm and its output is byte-identical.

The pad arm was first written with Rust's `trim_start_matches('0')`;
Kāra has no such method, and `karac check` names `strip_prefix` and the
loop for stripping every one (B-2026-11-01-9), which the arm now
writes. The iterator arm was carried by `karac fix` in two rounds of 2
and 1 edits: the `.into_iter()` that `windows(2)` needs before `filter`,
and the `as i64` dropped from a `len()`, and then from the `count()`,
which are `i64` already.

`karac fix` carries the template in two rounds of 9 and 2 edits: Rust's
spellings (the closure's `-> i32` dropped, `||` and `&&` to `or` and
`and`, `i32::MAX` to `i32.MAX`, `for &d in &digits[i..]` to `for d in
digits[i..]`, `struct Solution;` to `struct Solution {}`, `Solution::`
to `.`); then the adapter's `as i64` dropped, since an `i32` widens on
return, and `let mut total = 0` to `let mut total: i32 = 0`. Rust types
`total` from the closure's `-> i32`; once that is dropped, its literal
keeps the default `i64` (design.md §8 Literals) and meets the `return
i32.MAX`. That was refused as a bare "closure returns conflicting types:
'i64' vs 'i32'" with no fix, where the same body in a `fn` names the
binding and annotates it; the closure now does the same (kara 761ab5b3e0).

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every push of one to four digits, each normalized to four
digits by zeros in front, read as minutes and seconds, and kept when it
cooks for the time; each kept push walked from the start digit, and the
least cost taken. There is no rule about the two ways of writing a
time. It checks 300 random settings, the costs up to 10, 1000 or 10^5
in turn; then 30 of the longest times, 5940 to 6039 seconds; then 30 of
the shortest, one in each three seconds from 1 to 90. All 360 are drawn
before any arm answers.

| | property |
|---|---|
| P1 | the cost is the statement read literally |
| P2 | both costs three times as much: the cost three times as much |
| P3 | a push one dearer: the cost 1 to 4 more |
| P4 | a move one dearer: the cost 0 to 4 more |
| P5 | the finger starting on the next digit: the cost changed by at most one move |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 settings: checksum 998106943, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading of the same
settings by the same pushes. On a failure it prints the first ten and
then the count by property.

The third group was first 30 random times under 100 seconds, but the
generator's numbers modulo 99 drew none under 26, so the template's
zeros in the seconds (M21) went unseen; it now takes one time in each
three seconds. P2 first compared the tripled cost with three times the
answer, which overflows when an arm answers `i64.MAX` for a time it
cannot write (M1, M15); it now divides the tripled cost by three.

## Mutation testing

Twenty-five edits to the differential, three to five to each arm, each
run under `karac __mir-llvm-run` and `karac __mir-run`. Seventeen are
kept, three to each Kāra arm and two to the Rust-template arm. Each kept
one is killed, fails the same way under both backends and not by a
crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the second way never tried | P1 71, P2 18, P3 18, P6 71 |
| M2 | ★: a move paid for every digit | P1 171, P6 171 |
| M3 | ★: 100 seconds allowed | P1 7, P6 7 |
| M5 | minutes: the minutes only to 98 | P1 32, P2 26, P3 26, P6 32 |
| M6 | minutes: every zero skipped | P1 108, P6 108 |
| M7 | minutes: the leading zeros pushed | P1 55, P6 55 |
| M9 | pad: the seconds not padded | P1 52, P6 52 |
| M10 | pad: one zero taken off at most | P1 31, P6 31 |
| M11 | pad: a move priced as a push | P1 349, P3 328, P5 42, P6 349 |
| M13 | struct: a number's hundreds never typed | P1 357, P6 357 |
| M14 | struct: the finger never moved | P1 181, P5 27, P6 181 |
| M25 | struct: 10 typed as its last digit | P1 2, P6 2 |
| M18 | iter: the start digit pushed too | P1 360, P3 305, P6 360 |
| M19 | iter: the dearest way taken | P1 98, P6 98 |
| M20 | iter: the finger starting on 0 | P1 46, P6 46 |
| M21 | solution: zeros in the seconds pushed | P1 3, P6 3 |
| M24 | solution: the adapter's push priced as a move | P1 349, P3 360, P4 328, P6 349 |

P1 and P6 kill all seventeen, P3 five, P2 and P5 two each, and P4 one.
The cost is a sum of moves and pushes, so every wrong edit shows against
the literal reading; the other properties see only edits that get the
shape of that sum wrong. P3 makes a push dearer, which a right cost
meets with one to four more, as many as the cheapest way's digits; it
sees an edit that prices pushes wrongly (M11, M18, M24) or that, by
losing a way, leaves no cost for a time it can no longer write, `i64.MAX`
or the minutes arm's -1 (M1, M5), which no dearer push changes. P2 sees those two as well. P5 moves
the start digit, which a right cost meets with at most one move more or
less; it sees a finger that never moves (M14) and moves priced as
pushes (M11). P4 makes a move dearer and sees only M24, whose pushes are
priced as moves. Most edits are wrong only for some times (the shortest,
the longest, or those with a 0 in them), and only P1 and P6 look at the
answer itself.

Of the twenty-five, eight were not kept. One is equivalent: the pad arm
trying the second way with no minute to spare, which prints a minus
sign and is longer than the first way and starts with a move, so it is
never the cheaper. Three fail as a kept one does: the ★ arm's finger
never moved, as M14; the struct arm's second way never typed, as M1;
and the iterator arm never writing 0 seconds, as M21. Four were left out
to keep three to each arm and two to the template: the minutes arm
keeping the first way and the struct arm keeping the last, which fail
alike (P1 45, P6 45); and the template's second way 59 seconds more (P1
43) and its seconds never checked (P1 9).

## Verification

Every arm prints the same output as `cooking.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.8 s to 1.8 s, but for the
iterator arm, 13.9 s, which walks 100 counts of minutes by
`filter_map` and builds a list for each way on every solve, through the
interpreter's slow iterator chains (B-2026-11-14-62); the differential takes 0.9 s.

## Benchmarks

The bench solves every time the constraints allow from every start
digit, 1811700 solves in 30 passes, each pass pricing moves and pushes
differently so that no pass repeats one before, with the ★ arm in all
five languages, each writing a way's text and walking it: C by
`snprintf`. Every implementation prints `1811700 solves: 71762538 in
all, checksum 159851316`.

BENCHTAB
