# 949. Largest Time for Given Digits

Given an array `arr` of 4 digits, find the latest 24-hour time that can
be made using each digit **exactly once**.

24-hour times are formatted as `"HH:MM"`, where `HH` is between `00` and
`23`, and `MM` is between `00` and `59`. The earliest 24-hour time is
`00:00`, and the latest is `23:59`.

Return *the latest 24-hour time in* `"HH:MM"` *format*. If no valid time
can be made, return an empty string.

```
arr = [1,2,3,4]  ->  "23:41"
arr = [5,5,5,5]  ->  ""
```

**Constraints:** `arr.length == 4`; `0 <= arr[i] <= 9`.

## Approaches

| file | mechanism |
|---|---|
| `largest_time_from_digits.kara` ★ | every arrangement: the places of the first three digits chosen in three loops and the fourth the one left, `6 - i - j - k`; the first two read as the hours and the last two as the minutes, and the latest that is a time kept, in minutes. O(1): 24 arrangements |
| `largest_time_from_digits_countdown.kara` | every time, latest first: the day walked backwards from 23:59 to 00:00, and the first time made of the same four digits as those given returned. Two sets of four digits are the same when they hold each digit as many times, so each set is kept as one number adding `5^d` for each digit `d`, its counts, of at most 4, the digits of a number in base 5. O(1): at most 1,440 times |
| `largest_time_from_digits_lexi.kara` | the digits sorted and stepped through their arrangements in dictionary order by the next-permutation step: the last place whose digit is below the next swapped with the last digit larger than it, and what follows reversed. Read as `HH:MM`, dictionary order is time order, so the last arrangement that is a time is the latest. O(1): at most 24 arrangements |
| `largest_time_from_digits_greedy.kara` | `HH:MM` filled from the left, each place taking the largest unused digit it allows (at most 2 for the tens of hours, 3 for the hours after a 2 and 9 otherwise, 5 for the tens of minutes, 9 for the last), backing up to the next smaller digit when the places after it cannot be filled. A later time is larger in its first differing place, so the first time filled is the latest. O(1): at most 24 arrangements tried |
| `largest_time_from_digits_strings.kara` | every arrangement written out as a string `HH:MM`, by swapping each digit in turn into each place; the strings that are times kept, the hours below `"24"` and the tens of minutes below `"6"`, compared as strings; sorted, and the last taken. Strings of digits of one length sort as their numbers do. O(1): 24 strings |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 10 lines: LeetCode's two examples and six more
(four zeros, `[0,0,1,0]`, `[2,0,6,6]`, whose two 6s can only be the last
digits of the hours and of the minutes, `[1,9,6,0]`, `[9,5,3,2]` giving 23:59, and
`[2,4,5,9]` with no time); then the answer for every one of the 10,000
arrays of four digits, folded into how many make a time (5,935), the
minutes they add to and a checksum, and how many different times come
out (389) and the most common, 05:43, from 24 arrays.
`largest_time_from_digits.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every way of giving each of the four places of `HH:MM` one of
the digits, all 256 tried and those using a digit twice dropped, read as
a time when `HH` is 00 to 23 and `MM` is 00 to 59, and the latest. It
checks 3,200 random arrays: 3,000 of digits from 0 to between 1 and 9,
so that repeats and small digits are common, against the statement, and
200 of digits from 0 to 9, against the other properties; 2,701 of them
make a time.

| | property |
|---|---|
| P1 | the statement's latest time, on the first 3,000 arrays |
| P2 | `""` or `HH:MM`, hours below 24 and minutes below 60, made of the digits given, each once |
| P3 | the digits shuffled give the same answer |
| P4 | one digit lowered by one never turns a time into `""` |
| P5 | one digit raised by one never turns `""` into a time, and the digits read in the order given, when they are a time, are no later than the answer |
| P6 | each arm agrees with at least two of the other four |

It prints `3200 arrays, 2701 times, minutes adding to 2727665, checksum
154866211, 95000 checks over 5 arms: 0 failures` under `karac __mir-run`
(9 s) and `karac __mir-llvm-run`, and the same under
`karac __mir-llvm-asan` with no error.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-llvm-run`. All fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: minute 60 allowed | P1 36, P2 39, P6 39 |
| M2 | ★: the third digit used twice | P1 1606, P2 1712, P5 22, P6 1712 |
| M3 | ★: the last time found kept | P1 1732, P3 1866, P5 617, P6 1800 |
| M4 | countdown: 00:00 never tried | P1 25, P4 31, P5 25, P6 25 |
| M5 | countdown: the tens of minutes counted twice | P1 2580, P2 1667, P4 215, P5 688, P6 2701 |
| M6 | countdown: every other minute tried | P1 1810, P4 214, P5 622, P6 1878 |
| M7 | lexi: the digits never sorted | P1 940, P3 755, P4 2, P5 3, P6 1018 |
| M8 | lexi: the tail reversed one short | P1 245, P5 19, P6 289 |
| M9 | lexi: any hour below 30 | P1 695, P2 763, P6 763 |
| M10 | greedy: at most 1 for the tens of hours | P1 1235, P5 351, P6 1278 |
| M11 | greedy: a digit lost after a dead end | P1 36, P4 7, P5 10, P6 45 |
| M12 | greedy: 0 never tried | P1 1662, P4 309, P5 1318, P6 1742 |
| M13 | strings: the times never sorted | P1 1774, P3 1844, P5 720, P6 1844 |
| M14 | strings: each swap never undone | P1 764, P3 1091, P6 811 |
| M15 | strings: the earliest time taken | P1 2351, P5 1243, P6 2451 |

P1 and P6 kill all fifteen, P5 twelve, P4 six, and P2 and P3 four each.

P2 kills only M1, M2, M5 and M9, the four whose answers can be something
other than a time of the digits given: a minute of 60, a digit used
twice, a set of digits that is not the one given, and hours up to 29.
The other eleven always answer `""` or a real time of the digits, just
not always the latest.

P3 kills only M3, M7, M13 and M14, the four whose answer depends on the
order the digits come in. Every other arm works on the digits as a set,
whatever it gets wrong, so shuffling them changes nothing.

P4 and the first half of P5 ask only whether some time can be made. M1,
M9 and M10 change which times count, but each to a set that lowering a
digit never leaves, as the real one is (an hour or a minute only gets
smaller), so those two checks hold for them; M10's hours below 20 are
caught by the second half of P5, the digits in the order given making a
later time than the answer. P4 kills the six that answered `""` when
there was a time: M4 without 00:00, M5 with its digits miscounted, M6
with half the day skipped, M7 with the arrangements before the digits'
own order never reached, M11 with a digit lost and M12 without 0. M3,
M13, M14 and M15 look at every arrangement and differ only in which
time they keep, so they can never do that; that M2 and M8 did not on
these arrays was seen, not proved.

Ten other edits were tried and set aside. Five failed exactly the same
checks as each other, in two groups, so none of them was kept: ★, greedy
and strings each allowing hour 24, and greedy and strings allowing the
minutes 60 to 69. ★'s own edit to the minutes, M1, lets in 60 alone,
which is why it fails so few checks.
Three were sound but beyond three an arm: countdown never trying 23:59,
which only P6 caught, once; and lexi never stepping the last pair and
never stepping the first place. One crashed: ★ letting the third place
repeat the second, with an index out of bounds. One was equivalent:
countdown keeping its counts in base 4. Base 4 holds counts up to 3 exactly,
so a sum can be shared only through a digit held 4 times: four equal
digits `d`, whose sum `4^(d+1)` is the numeral of the one digit `d + 1`
held once. Every other set of four digits has each count below 4 and so
its own numeral, with digits adding to 4, never 1; no two sets share a
sum.

## Verification

Every arm prints the same output as `largest_time_from_digits.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build and the runtime archives are at kara
`086f304909`. Under `karac __mir-run` the arms take 0.4 to 5.2 s each
and the differential 9 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The legacy compiler was removed from kara at M3, so there is no legacy
lane.

## Benchmarks

The bench program builds the 10,000 arrays of four digits once; in each
of 500 rounds it runs the ★ arm on every one, each round starting from a
different one, and folds each answer's bytes into a checksum. Every
implementation prints `500 rounds over all 10000 arrays of four digits:
2967500 times, checksum 490035648`. Each call builds its answer as a new
string, as the ★ arm does: C with `malloc` and `snprintf`, Rust with
`format!`, Go with `fmt.Sprintf`, Python with an f-string, and Kāra with
an f-string.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.56 to 0.65 s | 0.57 s |
| Rust (`rustc -O`) | 0.46 to 0.52 s | 0.49 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.65 to 0.75 s | 0.70 s |
| Go | 0.84 to 0.99 s | 0.93 s |
| Python | 27.2 s | |
| Kāra (`karac build --mir`) | 0.59 to 0.67 s | 0.64 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Python's run is about 48 times
C's.

v2 takes 0.91 times Rust's median time under overflow checks and 1.13
times C's. Under valgrind's cachegrind v2 runs 7.80 billion
instructions and 2.21 billion branches with 197 million mispredicted,
Rust with overflow checks 9.99 billion, 2.24 billion and 137 million,
and C 6.80 billion, 1.05 billion and 24 million. C has half the
branches and an eighth of the mispredictions of the other two; that
clang turned the arrangement tests into selects is inferred from the
counts, not read from its code.
