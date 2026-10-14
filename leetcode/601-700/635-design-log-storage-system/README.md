# 635. Design Log Storage System

Each log has a unique id and a timestamp
`Year:Month:Day:Hour:Minute:Second`, every field zero-padded, as in
`2017:01:01:23:59:59`. Implement `LogSystem`: `put(id, timestamp)`
stores a log, and `retrieve(start, end, granularity)` returns the ids of
the logs whose timestamps lie from `start` to `end` inclusive, comparing
only down to `granularity`, one of `Year`, `Month`, `Day`, `Hour`,
`Minute` and `Second`. With `Day`, for example, `2017:01:01:23:59:59` to
`2017:01:02:23:59:59` means every log on January 1 or 2, 2017. The ids
may come back in any order.

```
put(1, "2017:01:01:23:59:59")
put(2, "2017:01:01:22:59:59")
put(3, "2016:01:01:00:00:00")
retrieve("2016:01:01:01:01:01", "2017:01:01:23:00:00", "Year")  ->  [3, 2, 1]
retrieve("2016:01:01:01:01:01", "2017:01:01:23:00:00", "Hour")  ->  [2, 1]
```

**Constraints:** ids from 1 to 500; years from 2000 to 2017, months 1 to
12, days 1 to 31, hours 0 to 23, minutes and seconds 0 to 59; at most
500 calls.

## Approaches

Every arm is a `struct LogSystem` with `fn put(mut ref self, id:
i64, timestamp: String)` and `fn retrieve(self, start: String, end:
String, granularity: String) -> Vec[i64]`, and each turns the
granularity name into a number with a `match` on the name.

| file | mechanism |
|---|---|
| `log_system.kara` ★ | the logs in a `Vec` of (id, timestamp); since every field is zero-padded, comparing two timestamps as text compares them as times, and cutting both to the granularity's length first compares them at that granularity; `match granularity` on the `String`; O(1) per put, O(logs) per retrieve |
| `log_system_packed.kara` | each timestamp packed into one number, two decimal digits a field after the year, so `2017:01:01:23:59:59` is 20170101235959; dividing by 100 for each field below the granularity cuts it; `match granularity` on the `String`; O(1) per put, O(logs) per retrieve |
| `log_system_numbers.kara` | each timestamp parsed at `put` into a `Vec` of its six fields, and the fields compared one at a time, as many as the granularity names; `match granularity.as_str()`; O(1) per put, O(logs) per retrieve |
| `log_system_sorted.kara` | a `SortedMap` from timestamp to the ids put at it; the bounds keep their fields down to the granularity and have the rest filled in with `0`s and `9`s, and `range_inclusive` reads out the logs between; `match granularity.as_str()`; O(log logs) per put |
| `differential.kara` | the four arms against the definition, five properties |

Every arm prints the same 10 lines: the two LeetCode examples; seven
more retrieves after two more logs are put, one at the same time as log
2 (a log's own time as both bounds at `Second`, `Minute` and `Hour`; a
range across New Year's Day at `Day` and one within December at `Month`;
a range that ends before it starts; and a one-second range across the
end of a year); and a count and checksum of the ids found by 200 random
retrieves over 300 random logs. The harness sorts each answer before
printing it, since the sorted arm returns its ids in time order and the
others in the order they were put. `log_system.py` mirrors the ★ arm and
its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition:
every timestamp turned into a count of seconds in a calendar of
12 months of 31 days, which orders times as the real calendar does, and
a log kept when its count, divided down to whole steps of the
granularity, lies between the bounds' counts divided the same way. Each
of 1,000 cases puts 1 to 20 logs with ids 1 up, at times drawn from two
values in each field so that logs and bounds often agree on some fields,
and draws two bounds in either order, three more times, and a
granularity.

| | property |
|---|---|
| P1 | the ids, sorted, are the definition's |
| P2 | the next coarser granularity keeps every id kept |
| P3 | putting the logs in reverse order gives the same ids |
| P4 | a log's own time, to the second, finds exactly the logs put at that time |
| P5 | to the second, a range split at a middle time keeps as many ids as its two halves, less those at the middle |

The kata's copy is refused like the numbers and sorted arms it holds
(see Verification). Its copy outside this directory with `.as_str()`
dropped from those two prints `1000 cases (3019 ids kept), 4 arms,
20000 checks, 0 failures` under `karac __mir-run` and `karac
__mir-llvm-run`, and runs clean under `karac __mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac __mir-run`
on the copy described under Verification. All eight that change answers
are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a log at the start left out | P1 362, P2 113, P4 1000 |
| M2 | ★: `Day` cut one character short | P1 59 |
| M3 | numbers: the year not compared | P1 603, P4 518, P5 351 |
| M4 | numbers: `Hour` compared down to the minute | P1 14 |
| M5 | packed: `Month` compared down to the day | P1 59 |
| M6 | packed: a log at the end left out | P1 354, P2 109, P4 1000 |
| M7 | sorted: the start filled in with `9`s | P1 345, P2 129 |
| M8 | sorted: the end cut from the start | P1 576 |
| E1 | ★: `Year` cut with the colon after it | 0 |
| E2 | numbers: `compare` giving -2, not -1, for before | 0 |
| E3 | packed: the number started from 1, not 0 | 0 |
| E4 | sorted: the end filled in with the latest real time, `12:31:23:59:59` | 0 |

P1 kills all eight. P2 sees M1, M6 and M7, the three that get a bound
wrong, because the same mistake at a coarser granularity reaches more
logs: a log kept at the finer granularity can share the start's coarser
prefix, and M1 then drops it. P3 sees none, since none of the mutants
depends on the order the logs were put. P4 sees M1 and M6, which find
nothing when the start and the end are one time, and M3, which also
finds a log from the other year at the same month, day and time. P5 sees
only M3, under which a range from one time to a later one can run
backwards once the year is ignored; M1 and M6 pass it, as a range open
at one end splits exactly into two halves open at that end. M2, M4 and
M5 change only the `Day`, `Hour` and `Month` granularities, and M8 only
ranges whose bounds differ, so P1 alone sees those four. The four
survivors cannot change an answer: the colon after the year is the same
in every timestamp; the callers test only the sign of the comparison;
starting from 1 adds 10^14 to every number, and since every divisor
divides 10^14, every cut number moves up by the same amount; and no
field of a valid timestamp is above 12, 31, 23, 59 and 59, so that end
still lies at or above every timestamp sharing its prefix.

## Verification

The ★ and packed arms print the same output as `log_system.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and run clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. `karac check`
passes both and the bench program. The numbers arm, the sorted arm and
the differential are refused by every `karac` command, `check` included,
at the literal patterns of their `match granularity.as_str()`, with
"expected 'StringSlice', found 'String'" (B-2026-10-14-43, filed from
here). So each was also run as a copy outside this directory with
`.as_str()` dropped, matching the `String` itself as the other two arms
do. The two arm copies print the mirror's output under `__mir-run` and
`__mir-llvm-run` and run clean under `__mir-llvm-asan`, the differential
copy prints its line under all three, and `check` passes all three. All
at kara `ea2a2da2be` for the debug build and `cfcdff46d8` for the
release build that runs `check` and `__mir-run`.

The frozen legacy backends refuse every file at type checking. They type
the items of a `Vec`'s `iter()` by value, so `*id` is an error; they
still hold the old rule that an argument which is already a `mut ref`,
as `seed` is inside `random_time`, drops its call-site `mut` marker;
they refuse passing an element of a `Vec[Vec[i64]]` by indexing, as the
numbers arm passes `self.times[i]`; and they share
B-2026-10-14-43. Legacy is frozen, so these are noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It puts 20,000 logs at random times
from 2000 to 2017 once, then makes 2,000 retrieves between two random
times at a random granularity, counting the ids returned and putting
each into a checksum in the order it comes back. Every implementation
prints `20000 logs, 2000 retrieves: 7207360 ids, checksum
270210966`, the Kāra program under `karac __mir-run` included (in
101 s).

Each implementation keeps the logs in a growable array of (id,
timestamp) and compares the cut timestamps as bytes: C with `memcmp` on
fixed 20-byte buffers, Rust and Go with string slices, Python with
string slices. Spot timings on a shared 4-core container, three runs
each (two for Python; `bench.sh` timings need a quiet machine), each
including putting the logs:

| | time |
|---|---|
| C (`clang -O3`) | 0.47 to 0.50 s |
| Rust (`rustc -O`) | 0.54 to 0.55 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.49 to 0.50 s |
| Go | 0.62 to 0.65 s |
| Python | 3.76 to 4.07 s |
| Kāra (`karac build --mir`) | 1.53 to 1.57 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend, since the legacy `karac build` refuses the bench
program as above; that edit is by hand, on top of the
`scripts/new-bench.sh` output. A copy outside the kata without the two
`*`s and the forwarded `mut` markers builds under legacy, but the binary
stops at once with `free(): double free detected`, so there is no legacy
time to compare with. Legacy is frozen, so that is noted, not filed.
Under `karac __mir-llvm-run` the program prints the same line in 6.0 s,
compile included; that JITs the MIR's IR without optimization passes, so
it is not a benchmark.

The Kāra build takes about three times as long as C and Rust. In the
built binary, each log the retrieve loop visits costs three calls into
the runtime: `karac_mir_str_view` for the cut, which checks that it
falls on a char boundary, and `karac_mir_str_test` twice for the two
comparisons, a general string test that is passed the comparison as a
number and dispatches on it. The C build also makes two calls per log,
to `memcmp`, so the gap is likely the work inside those runtime calls
rather than their number. That is inferred from the disassembly, not
profiled. It is not filed: the comparison with Rust and C waits until
after M4, and legacy cannot run this program.

## Compiler findings

kara B-2026-10-14-43 (open), filed from here: a string literal pattern
does not take the `Str` type of its scrutinee, so `match s.as_str() {
"Year" => ... }` and a match on a `Str` parameter are refused, while the
same match on a `String` works. The numbers and sorted arms and the
differential keep the `as_str()` spelling, which Rust code uses; once
the row is fixed they should run unchanged, and are to be rechecked
then.

The legacy failures above are not filed because legacy is frozen.
