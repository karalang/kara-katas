# 539. Minimum Time Difference

Given a list of 24-hour clock time points in `"HH:MM"` format, return
the minimum minutes difference between any two time-points in the list.

```
timePoints = ["23:59","00:00"]          ->  1
timePoints = ["00:00","23:59","00:00"]  ->  0
```

**Constraints:** `2 <= timePoints.length <= 2 * 10^4`; `timePoints[i]`
is in the format `"HH:MM"`.

## Approaches

Every arm is `fn find_min_difference(time_points: Vec[String]) -> i64`.
The clock is a circle of 1,440 minutes, so two times are apart by the
shorter way round, and with the times in order the closest pair is two
neighbours or the last and the first across midnight.

| file | mechanism | time |
|---|---|---|
| `find_min_difference.kara` ★ | each time parsed to minutes (`i64.parse` of the two slices), sorted, neighbours compared | n log n |
| `find_min_difference_buckets.kara` | a mark for each of the 1,440 minutes, read off the bytes; more than 1,440 times, or a mark already set, is a repeat and the answer 0 | n + 1440 |
| `find_min_difference_strings.kara` | the times sorted as written, since `"HH:MM"` sorts as text in the order of the clock; only neighbours are parsed | n log n |
| `find_min_difference_ordered.kara` | a `SortedSet` of the minutes, cut at the `find(":")`; an insert that finds its minute there is a repeat | n log n |
| `differential.kara` | the four arms against the definition, five properties | |

Every arm prints the same 11 lines: both examples, half a day, a
repeat, a closest pair across midnight and one inside the day, times
six hours apart; then for 300 random lists of 2 to 60 times, from the
whole day or from its first two hours in turn, how many have a repeat
and a checksum over the answers; and last every third minute of the
day, every minute, and 20,000 random times (the problem's most), each
in a random order. `find_min_difference.py` mirrors the ★ arm and its
output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition:
over every pair of times, the shorter way round the clock. Each arm is
held to the properties below on 1,000 random lists, in turn: 2 to
50 times from the whole day; 2 to 50 from a window of 30 minutes that
starts in the last hour of the day, so that about half of the windows
cross midnight; and 2 to 5 from the whole day.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | the list backwards gives the same answer |
| P3 | every time moved on by the same number of minutes, round the clock, gives the same answer |
| P4 | the list with one of its times again gives 0 |
| P5 | the answer is from 0 to 720, and times the number of times at most a day |

It prints `1000 cases, 4 arms, 20000 checks, 0 failures` under `karac
__mir-run`.

## Mutation testing

Twelve edits to `differential.kara`, two to each arm that change its
answers, and four that do not, each run under `karac __mir-run`. All
eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the gap across midnight never taken | P1 38, P3 68, P5 23 |
| M2 | ★: an hour taken as 100 minutes | P1 773, P3 697, P4 597, P5 597 |
| M3 | buckets: the circle never closed, last to first | P1 38, P3 68, P5 23 |
| M4 | buckets: the hour's second digit dropped | P1 519, P3 275 |
| M5 | strings: every time measured from the first, not the one before | P1 643, P3 508, P4 716, P5 136 |
| M6 | strings: the times never sorted | P1 932, P2 968, P3 572, P4 971, P5 932 |
| M7 | ordered: a repeat not noticed | P1 390, P4 1000, P5 1 |
| M8 | ordered: the walk started from midnight, not the first time | P1 182, P3 222, P5 61 |
| E1 | ★: each gap taken as an absolute value | 0 |
| E2 | buckets: the shortcut for many times moved from 1,440 to 2,000 | 0 |
| E3 | strings: the minutes read to the end of the time, not to byte 5 | 0 |
| E4 | ordered: the best started at half a day, not a whole one | 0 |

M1 and M3 are one mistake in two arms and fail in the same cases: the
closest pair has to be the one across midnight, which the first draft of
the differential (lists from the whole day, or from 30 minutes anywhere
in it) gave in 5 cases of 1,000. The window that now starts in the last
hour of the day, and the short lists, raise that to 38. M7 fails P4 in
every case, as it should, and P1 only where the list already had a
repeat. P2 sees only M6, the one edit that makes the answer depend on
the order of the list. E2 is equivalent because the marks find a repeat
on their own; the shortcut only saves the walk. E4 is equivalent because
the shorter way round is never more than half a day.

## Verification

Every arm prints the same output as `find_min_difference.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and runs clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints `20000 checks, 0 failures` on the first two and runs clean under
the third. `karac check` passes on every arm, the differential and the
bench program.

The frozen legacy backends do less. `karac run --interp` gives the right
output for the ★ and buckets arms. It refuses the strings arm, the
differential and the bench program at type checking, on taking a `Str`
or a `Vec[String]` out of a `Vec` by index (E_INDEX_MOVE_NON_COPY), and
the ordered arm on the `*` of `set.min().unwrap()`, which legacy types
by value. `karac run` and `karac build` fail on the ★ arm at its
`t[0..2]` ("no handler for expression kind Range") and on the buckets
arm with an LLVM module that does not verify (the harness's `show`
called with a mismatched argument). Legacy is frozen, so this is noted,
not filed.

## Benchmarks

The bench program uses the ★ arm. It builds 300 lists of 20 to
1,440 distinct times once, the first places of a shuffle of the whole
day; then the answer for each list is found 100 times, every call
parsing and sorting the list afresh. Every implementation prints
`300 lists, 210949 times, 100 times each: total 30500, checksum
191494886`, the Kāra program under `karac __mir-run` included (in
162 s).

The mirrors parse each part the way their language reads a number from
a string: Rust with `parse::<i64>()`, Go with `strconv.ParseInt`,
Python with `int`, and C with a loop over the digits, since `strtoll`
cannot stop at a length. C sorts with `qsort`, Go with `slices.Sort`,
Rust with `sort` (stable, as Kāra's `sort` is). Spot timings on a
shared 4-core container, three runs each (two for Python; `bench.sh`
timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 1.82 to 1.89 s |
| Rust (`rustc -O`) | 0.50 to 0.53 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.49 to 0.56 s |
| Go | 1.84 to 1.98 s |
| Python | 10.6 s |
| Kāra (`karac build --mir`) | 1.92 to 1.99 s |

The legacy `karac build` refuses this program (see Verification). So
`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend; that edit is by hand, on top of the
`scripts/new-bench.sh` output. The `--mir` row is timed at kara
`2649217dc8`. Under `karac __mir-llvm-run` the program prints the same
line in 23.5 s, compile included; that JITs the MIR's IR without
optimization passes, so it is not a benchmark.

The Kāra row is level with C and Go and nearly four times Rust's. Almost
all of the gap is `i64.parse`, which allocates on every call (kara
B-2026-10-13-34, below).

## Compiler findings

kara B-2026-10-13-34 (open), filed from this kata: `i64.parse` on the
v2 compiled backend copies the text into a fresh heap `String`, trims it
and parses an `i128` on every call, some 30 ns for two digits. With the
two parses spelt as byte arithmetic the bench program runs in 0.47 s
instead of 1.90 s; without the sort, 1.75 s. The row also notes that
every backend trims whitespace before parsing, which the spec's
`ParseError` does not seem to allow; that question sits with kara
B-2026-10-12-6 (open, filed from kata 388), under which `parse` still
returns an `Option` where the spec gives a `Result`. Every arm calls
`.unwrap()`, which reads the same on either.