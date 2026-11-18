# 1604. Alert Using Same Key-Card Three or More Times in a One Hour Period

LeetCode company workers use key-cards to unlock office doors. Each time
a worker uses their key-card, the security system saves the worker's
name and the time when it was used. The system emits an **alert** if any
worker uses the key-card **three or more times** in a one-hour period.

You are given a list of strings `keyName` and `keyTime` where
`[keyName[i], keyTime[i]]` corresponds to a person's name and the time
when their key-card was used **in a single day**.

Access times are given in the **24-hour time format "HH:MM"**, such as
`"23:51"` and `"09:49"`.

Return a *list of unique worker names who received an alert for frequent
keycard use*. Sort the names in **ascending order alphabetically**.

Notice that `"10:00"` - `"11:00"` is considered to be within a one-hour
period, while `"22:51"` - `"23:52"` is not considered to be within a
one-hour period.

```
keyName = ["daniel","daniel","daniel","luis","luis","luis","luis"],
keyTime = ["10:00","10:40","11:00","09:00","11:00","13:00","15:00"]  ->  ["daniel"]
keyName = ["alice","alice","alice","bob","bob","bob","bob"],
keyTime = ["12:01","12:00","18:00","21:00","21:20","21:30","23:00"]  ->  ["bob"]
```

**Constraints:** `1 <= keyName.length, keyTime.length <= 10^5`;
`keyName.length == keyTime.length`; `keyTime[i]` is in the format
"HH:MM"; `[keyName[i], keyTime[i]]` is unique; `1 <= keyName[i].length
<= 10`; `keyName[i]` contains only lowercase English letters.

## Approaches

Three swipes lie within an hour exactly when, among a name's swipes in
time order, some swipe and the one two after it are at most 60 minutes
apart.

| file | mechanism |
|---|---|
| `alert.kara` ★ | each name's minutes gathered in a `SortedMap[String, Vec[i32]]` through `entry(..).or_insert(..)`, so the names come out in order; each list sorted in place through `iter_mut`, and `(2..len).any(..)` for two swipes apart. O(n log n) |
| `alert_sorted.kara` | every swipe made a `(String, i32)` pair and the whole list sorted once, so each name's swipes stand together in time order and the names in order; a swipe and the one two before it, the same name and within the hour, alert the name once (`out.last() != Some(ref name)`). O(n log n) |
| `alert_minutes.kara` | 1441 counts a name in a `Map[String, Vec[i32]]` (`Vec.filled`), summed to running counts, and a name alerted when some hour `[m, m + 60]` holds three; the names sorted at the end. O(n + names * 1440) |
| `alert_solution.kara` | LeetCode's Rust template (a `HashMap<String, Vec<i32>>` filled through `entry(..).or_insert_with(Vec::new)`, `t[..2].parse::<i32>()`, `windows(3)`, the answer sorted), carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's two examples and three
more (three swipes across midnight, which does not wrap; an hour exactly
and 58 minutes; and four swipes each 61 minutes from the one two after),
then the alerts and a checksum of the names for 3000 days of up to 8
swipes by up to 4 names within two hours, 300 of up to 2000 swipes by up
to 50 names, and 3 of up to 100000 swipes by up to 2000 names, over the
whole day. `alert.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every three swipes by one name compared, and the name alerted
when the latest and the earliest of some three are at most 60 minutes
apart. It checks 3000 days of 1 to 8 swipes by three names, within 150
minutes of a random start, every random choice drawn before any arm
answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the swipes in reverse order leave the answer |
| P3 | every swipe moved later by the same minutes, the last to 23:59, leaves the answer |
| P4 | a swipe by a new name leaves the answer |
| P5 | every swipe given twice alerts every name the swipes once did |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 949477048, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends.

Two first choices were replaced. Leaving out the minutes arm's final
sort was killed, but by different counts under the two backends: that
arm reads its names from a `Map`, whose order is the process's hash
order, so the mutant's output is not a fixed thing to compare. Starting
its running sum at minute 2 was equivalent, as nothing is ever counted
before minute 1, and the first replacement for it, the windows that
start in the last hour skipped, was equivalent too: the window from
22:59 holds every swipe after it.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: exactly an hour apart not alerted | P1 11, P6 11 |
| M2 | ★: a name's minutes not sorted | P1 627, P2 413, P6 627 |
| M3 | ★: a time's minutes read as zero | P1 425, P3 298, P6 425 |
| M4 | sorted: two swipes apart taken without asking for the same name | P1 1825, P4 2267, P5 28, P6 1825 |
| M5 | sorted: the first three swipes never ending a window | P1 228, P6 228 |
| M6 | minutes: the window's last minute left out | P1 11, P6 11 |
| M7 | minutes: four swipes asked for | P1 729, P6 729 |
| M8 | template: the window's middle swipe taken for its first | P1 628, P6 628 |
| M9 | template: only the tens of the minutes read | P1 84, P3 69, P6 84 |
| M10 | minutes: no window starting after 21:40 | P1 11, P3 768, P6 11 |

## Benchmarks

The bench makes 30 days of 100000 swipes by 20000 names, all of it first. Then: each name's minutes in an ordered map (C hash + sorted names), each list sorted. Every implementation prints `30 days of 100000 swipes by 20000 names: 48329 alerts, checksum 700171452`.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `5bb1708545` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 1.026 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.264 s |
| Rust (`rustc -O`) | 1.403 s |
| Go | 1.536 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 1.739 s |
| Kāra (`karac build`) | 1.754 s |
| Python | 5.7 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its user time is not above its real time (1.652 s and 1.814 s on one run).

## Verification

All four arms print the same output as `alert.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them, the differential and the bench. `karac check` reports nothing on
any of them, and `karac fix` has nothing left to change. Checked at kara
`5bb1708545`.

## Writing it

The minutes arm was written in Kāra and checked as written, and so was the differential but for one `"zed".to_string()` pushed onto a `Vec[String]`, whose call `karac fix` dropped. The ★ arm
wrote `t.split_once(':')`, and `karac fix` made it `":"`, as `split_once`
takes a string. It also wrote `h.parse[i32]()`, the generic method
called with its type in brackets, as Kāra writes types; `karac check`
read the brackets as an index and said `i32` is a type, not a function,
and to cast with `as i32`, which would not parse a string, so the call
was rewritten by hand as `i32.parse(h)` (B-2026-11-18-7). The sorted arm wrote
`let (name, t) = swipes[i];`, which would move a `String` out of an
index; `karac fix` made the first `swipes[i].clone()` and the second
`ref swipes[i - 2]`, and the `Some(name)` compared with `out.last()`
`Some(ref name)`. The clone is left: the name it copies is only read.
The shared harness wrote `b as i64` on a byte, and `karac fix` dropped
the cast.

The Rust template took one `karac fix` of 23 edits:
`use std::collections::HashMap` dropped, `struct Solution;` to
`struct Solution {}`, the `<..>` types to `[..]` and `HashMap` to
`Map`, `::new` to `.new`, `&key_time[i]` to `ref key_time[i]`, each
`t[..2].parse::<i32>()` to `i32.parse(t[..2])`, `windows(3).any(..)` to
`windows(3).into_iter().any(..)`, and `Solution::` to `Solution.`. It
then checks and agrees with no hand edit.
