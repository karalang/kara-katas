# 2446. Determine if Two Events Have Conflict

You are given two arrays of strings that represent two inclusive events
that happened **on the same day**, `event1` and `event2`, where:

- `event1 = [startTime1, endTime1]` and
- `event2 = [startTime2, endTime2]`.

Event times are valid 24 hours format in the form of `HH:MM`.

A **conflict** happens when two events have some non-empty intersection
(i.e., some moment is common to both events).

Return `true` *if there is a conflict between two events. Otherwise,
return* `false`.

```
event1 = ["01:15","02:00"], event2 = ["02:00","03:00"]  ->  true
event1 = ["01:00","02:00"], event2 = ["01:20","03:00"]  ->  true
event1 = ["10:00","11:00"], event2 = ["14:00","15:00"]  ->  false
```

**Constraints:** `event1.length == event2.length == 2`;
`event1[i].length == event2[i].length == 5`;
`startTime1 <= endTime1`; `startTime2 <= endTime2`; all the event times
follow the `HH:MM` format.

Two closed intervals meet exactly when each starts no later than the
other ends, which is the later start being no later than the earlier
end. A time written `HH:MM` with leading zeros has a fixed width and its
digits run from the largest place down, so the strings sort as text in
the order the times sort, and the four strings can be compared directly.

## Approaches

| file | mechanism |
|---|---|
| `conflict.kara` ★ | the four strings compared as text: each event starts no later than the other ends, joined by `and`. O(1) |
| `conflict_minutes.kara` | each time read as minutes since midnight, the hour and the minute parsed by `i64.parse` from the two sides of `split(":")`, and the later start compared with the earlier end by `max` and `min`. O(1) |
| `conflict_naive.kara` | the statement read directly: every minute of the day written as `HH:MM` by an f-string, marked in a `Vec[bool]` of 1440 when it lies within the first event, and a conflict when some marked minute lies within the second too. O(1440) |
| `conflict_sorted.kara` | the two events as `(start, end)` pairs of byte vectors from `bytes()`, sorted as tuples: they conflict when the second starts no later than the first ends. O(1) |
| `conflict_iter.kara` | iterators: the latest start by `max` and the earliest end by `min`, each a `map` over an array of the two events that clones the string. O(1) |
| `conflict_solution.kara` | LeetCode's Rust template: `Vec<String>` compared with `<=` and joined by `&&`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 10 lines: LeetCode's three examples; the same
event twice; two events touching at one end; the whole day against one
minute; two one-minute events, apart and together; then 3000 random
pairs of events and 3000 pairs of events of at most 30 minutes, each as
the count that conflict and a checksum of where they fall.
`conflict.py` mirrors the ★ arm and its output is byte-identical, and
the mirror was checked on 200000 random pairs against every minute of
the day tested in both events.

`check` first reports 4 errors on the template, and `karac fix` carries
it in one call, reporting 6 edits: each of the four angle brackets of
the two `Vec<String>` made square, `&&` written `and`, and `struct
Solution;` given its braces. `String`'s `<=` stands as Kāra, comparing
the text as Rust's does, and so do the indexing and the `bool` return.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: each time turned into minutes from its four digit bytes, and
every minute of the day tested for lying within both events; one that
does is a conflict. No string is compared and no start or end is
chosen. It checks 300 random pairs of events; then 30 pairs of events
of up to 30 minutes; then 20 pairs that touch, the second starting
where the first ends or one minute after; then 10 events ending at
23:59 against the one minute 23:59 itself. All 360 are drawn before
any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | the events swapped: the same answer |
| P3 | both events moved by one number of minutes, kept within the day: the same answer |
| P4 | the first event widened to the whole day: true |
| P5 | the second event the one minute after the first ends, when there is one: false |
| P6 | each arm agrees with at least three of the other five |

P2 holds because a common moment is common whichever event is named
first. P3 holds because moving both events moves their common moments
with them. P4 holds because the whole day holds every moment of the
second event, and P5 because a minute past the first event's end lies
outside it.

The differential prints `360 cases: checksum 930265376, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and tests every minute. On a failure it prints the first
ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M3 | ★: only the second start inside the first | P1 93, P2 229, P6 93 |
| M4 | ★: only the second end inside the first | P1 117, P2 219, P6 117 |
| M5 | ★: the first end before the second | P1 102, P2 219, P4 350, P6 102 |
| M7 | minutes: an hour of 10 minutes | P1 47, P3 38, P4 28, P5 3, P6 47 |
| M8 | minutes: the minutes ignored | P1 17, P3 5, P5 347, P6 17 |
| M9 | minutes: a touch not a conflict | P1 22, P4 13, P6 22 |
| M12 | naive: the first end never busy | P1 22, P2 12, P4 10, P6 22 |
| M14 | naive: 23:59 never busy | P1 10, P3 10, P4 10, P6 10 |
| M15 | naive: a free minute taken | P1 202, P2 123, P4 360, P5 350, P6 202 |
| M18 | sorted: a touch not a conflict | P1 22, P4 10, P6 22 |
| M19 | sorted: the ends compared | P1 106, P4 1, P6 106 |
| M20 | sorted: the second event read backwards | P1 117, P2 217, P6 117 |
| M22 | iter: the earlier start | P1 131, P5 350, P6 131 |
| M25 | iter: the start from the ends | P1 219, P4 350, P6 219 |
| M26 | iter: a start at the first end enough | P2 1 |
| M27 | solution: only the first test | P1 74, P2 131, P5 350, P6 74 |
| M29 | solution: the second start before the first start | P1 136, P2 229, P4 359, P6 136 |


P1 and P6 kill sixteen, P4 ten, P2 nine, P5 five and P3 three. The
iter arm's start at the first end enough (M26) is caught by P2 alone,
in one case.

Fourteen are not kept. Five fail exactly as a kept one: the ★ arm's
either test enough, the minutes arm's earlier start, the sorted arm's
first start against the second end and the iter arm's later end (M2,
M10, M21, M23) as the iter arm's earlier start (M22), each answering
`true` for every pair, since each compares a start with an end that
cannot come before it; and the iter arm's touch not a conflict (M24) as
the minutes arm's (M9). Four more fail alike, apart from every kept
one, and none is kept because those arms keep their share already: the
minutes arm's only the first end, the naive arm's second end never
checked, the sorted arm's never sorted and the template's only the
second test (M11, M13, M17, M28), each reading a conflict as the second
event starting by the time the first ends, which misses a second event
that ends before the first begins. Five fail apart from every kept one
and were left out for the same reason: the ★ arm's start at the other
end not a conflict and second start strictly inside (M1, M6), the naive
arm's each minute marked one late (M16), and the template's answer
negated and same start not a conflict (M30, M31).

The first run had one survivor, the naive arm's 23:59 never busy
(M14), which is not equivalent: two events that share only the day's
last minute conflict, and the 360 cases held no such pair. Ten events
ending at 23:59 against the minute 23:59 itself were added, and all 31
were run again; M14 is now killed and kept.

## Verification

Every arm prints the same output as `conflict.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.3 to 0.9 s, but for the naive
arm, which formats 2880 times for each of its 6008 pairs: it takes
46.6 s there, 14.5 s under `karac __mir-llvm-asan` and 2.3 s under
`karac run`. The differential takes 24.9 s under `karac __mir-run`,
9.9 s under `karac __mir-llvm-asan` and 1.9 s under `karac run`.

## Benchmarks

The bench builds `10^5` events once from its own generator, each two
random times written `HH:MM`, the earlier first. It then makes 300
passes, pass `p` pairing event `i` with event `(7 i + p + 1) mod 10^5`,
so every pass asks new pairs, and folds each answer plus the pass into
the checksum. The bench uses the ★ arm, the four strings compared as
text, in all five languages. Every implementation prints `300 passes
over 10^5 events: checksum 211080453`. Each event is a list of two
heap strings in every language, and in C an array of two `malloc`ed
strings compared by `strcmp`.

BENCHTAB
