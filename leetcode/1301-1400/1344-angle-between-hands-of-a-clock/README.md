# 1344. Angle Between Hands of a Clock

Given two numbers, `hour` and `minutes`, return the smaller angle (in
degrees) formed between the hour and the minute hand. Answers within
10^-5 of the actual value will be accepted as correct.

```
hour = 12, minutes = 30  ->  165
hour = 3, minutes = 30   ->  75
hour = 3, minutes = 15   ->  7.5
```

**Constraints:** `1 <= hour <= 12`, `0 <= minutes <= 59`.

The arms are `fn angle_clock(hour: i32, minutes: i32) -> f64`.

## Approaches

| file | mechanism |
|---|---|
| `angle_clock.kara` ★ | the minute hand is 6 degrees a minute from 12, the hour hand 30 degrees an hour plus half a degree a minute; the gap between them, or 360 less it if that is smaller, by the float method `gap.min(360.0 - gap)`. O(1) |
| `angle_clock_halves.kara` | every place is a whole number of half degrees, so the hands are placed in integers (the hour hand 60 an hour and 1 a minute, the minute hand 12 a minute), the smaller gap found exactly, and only then halved. O(1) |
| `angle_clock_gaining.kara` | at 12 the hands meet, and each minute after it the minute hand gains 5.5 degrees on the hour hand, so the angle is 5.5 times the minutes since 12 around a circle of 360, or 360 less that. O(1) |
| `angle_clock_walk.kara` | both hands set at 12 and moved a minute at a time, in half degrees round a face of 720, then the gap the shorter way round. O(minutes since 12) |
| `angle_clock_solution.kara` | a Rust solution as LeetCode's Rust users write it (the hands as `f64` from `hour as f64 % 12.0 * 30.0 + minutes as f64 / 2.0` and `minutes as f64 * 6.0`, the answer `diff.min(360.0 - diff)`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties, at every one of the 720 times |

Every arm prints the same 2 lines: LeetCode's three examples, noon, six
o'clock, and 1:05, where the hands nearly meet (`165.0 75.0 7.5 0.0
180.0 2.5`); and every one of the 720 times, each angle a whole number
of half degrees, so twice it folds into the checksum exactly (`720
times: angles total 64800.0, largest 180.0, checksum 359323530`).
`angle_clock.py` mirrors the ★ arm, and its output is byte-identical.
Every arm gives the same output under `karac __mir-run`, `karac run` and
`karac __mir-llvm-run`.

The Mend loop: the first draft of the ★ arm returned `min(gap, 360.0 -
gap)`, and the harness kept `largest = max(largest, a)`, both on `f64`.
`karac check` refuses the free `min` and `max` there (E0200), as the
design says, since `f64` has no total order; but its advice, to wrap the
values in `F64` or drop an `Ord` bound the program never wrote, does not
fit the call, and following it gives a second error. The documented
float method, `gap.min(360.0 - gap)`, is not named, and `karac fix` has
no fix. That is ledger row B-2026-11-24-48; the arms use the method. The
same call over float literals alone, `min(1.5, 2.5)`, passes `karac
check` and then stops the interpreter with "call of unknown function
min" (B-2026-11-25-36). A fourth arm read the face as 60 minute marks,
the hour hand `minutes as f64 / 12.0` marks past its hour; a twelfth is
not exact in binary, and at 1:05 it printed `2.5000000000000018` where
Python prints `2.5`. That was the program's mistake, caught by the
oracle, and the walk arm, in whole half degrees, took its place. The
Rust solution takes one round of 2 fixes by `karac fix`'s count, from 2
errors: `struct Solution;` to `struct Solution {}` and `Solution::` to
`Solution.`. Its output matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: each hand's place in half degrees clockwise from 12, the
angle between them each way round by `rem_euclid(720)`, and the smaller
of the two in degrees. It runs at every one of the 720 times, from 1:00
to 12:59, the whole input space.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the face in a mirror, the time as far before 12 as this is after it: the same angle |
| P3 | six hours on, the hour hand turned half round: 180 less the angle |
| P4 | from 0 to 180, a whole number of half degrees |
| P5 | a minute on: the angle changes by at most 5.5 degrees |
| P6 | the ★ arm's answer |

All 21,600 checks pass on every arm: `720 times: checksum 359323530,
21600 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run` and `karac __mir-llvm-run`. Python, in whole half degrees, gives
the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash, and no two
fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the hour hand not moved by the minutes | P1 708, P2 708, P5 720, P6 2832 |
| M2 | ★: the larger angle returned | P1 719, P3 720, P4 719, P6 2876 |
| M3 | halves: the minute hand counted in degrees among half degrees | P1 702, P2 700, P5 10, P6 702 |
| M4 | halves: the gap taken without its sign | P1 354, P2 708, P3 550, P4 354, P5 11, P6 354 |
| M5 | gaining: the minute hand's 6 degrees a minute taken for the gain | P1 719, P3 696, P5 720, P6 719 |
| M6 | gaining: the angle never folded past 180 | P1 359, P2 718, P3 718, P4 359, P5 11, P6 359 |
| M7 | walk: the hour hand walked at twice its pace | P1 718, P2 360, P3 710, P4 180, P5 5, P6 718 |
| M8 | walk: the gap folded past 90 degrees | P1 179, P2 358, P3 358, P4 179, P5 11, P6 179 |
| M9 | solution: the hour hand a twelfth of a degree a minute | P1 708, P2 708, P3 274, P4 600, P5 698, P6 708 |
| M10 | solution: the minute hand 5 degrees a minute | P1 690, P2 704, P5 10, P6 690 |

P1 and P6 kill all ten, P5 nine, P2 eight, P3 seven and P4 six. A
minute on (P5) catches every edit but the larger angle (M2): a hand at
the wrong speed lets the angle jump, and so does folding at the wrong
place, at the few minutes where the fold is crossed. The mirror (P2)
catches every edit that is not symmetric about the 12-6 line, all but
the larger angle (M2) and a gain of 6 a minute (M5), each of which turns
a time and its mirror into the same wrong angle. Six hours on (P3) holds
whenever the hour hand still moves exactly half round in six hours, so
it misses the edits that only change the minute hand or the minutes'
pull on the hour hand (M1, M3, M10). The range (P4) catches the edits
that fold wrong or not at all (M2, M4, M6, M8), the doubled hour hand
(M7), which can leave the gap over 180, and the twelfth of a degree
(M9), which is not a half degree. M8 is the weakest: folding past 90
instead of 180 changes only the angles between 90 and 180, 179 of the
720 times.

## Benchmarks

The bench answers 3 * 10^7 times with the ★ arm, each the i-th time plus
the checksum so far, taken round a 12-hour face, so no answer can be
computed ahead, and folds twice each angle, a whole number, into the
checksum. C and Go take the smaller value with `fmin` and `math.Min`.
Every implementation prints `3 * 10^7 times: checksum 923927587`.

BENCHTAB
