# 636. Exclusive Time of Functions

On a single-threaded CPU, a program runs `n` functions with ids 0 to
`n - 1`. Calls are tracked on a stack: a call pushes the function's id,
and the function on top of the stack is the one running. The logs are
given in timestamp order, each `"{id}:start:{t}"` or `"{id}:end:{t}"`: a
start at `t` begins at the beginning of unit `t`, and an end at `t`
finishes at the end of unit `t`. A function's exclusive time is the
number of units it ran, across all its calls, not counting the time its
callees ran. Return the exclusive times by id.

```
n = 2, ["0:start:0","1:start:2","1:end:5","0:end:6"]                          ->  [3, 4]
n = 1, ["0:start:0","0:start:2","0:end:5","0:start:6","0:end:6","0:end:7"]    ->  [8]
n = 2, ["0:start:0","0:start:2","0:end:5","1:start:6","1:end:6","0:end:7"]    ->  [7, 1]
```

**Constraints:** `n` from 1 to 100; 1 to 500 logs; timestamps from 0 to
10^9; no two starts and no two ends at the same timestamp; every start
has its end.

## Approaches

Every arm is `fn exclusive_time(n: i64, logs: Vec[String]) -> Vec[i64]`
and reads each log with `split(":")` and `i64.parse`.

| file | mechanism |
|---|---|
| `exclusive_time.kara` ★ | a stack of running ids and the time of the last event; each log hands the time since that event to whoever was running: a start at `t` gives the caller `t - prev`, an end at `t` gives the callee `t - prev + 1` and the caller resumes at `t + 1`; O(logs) |
| `exclusive_time_frames.kara` | a stack of frames of (id, start, callee time); at an end the call's whole length `t - start + 1`, less its callees' time, is its own, and the whole length goes to the caller's frame as callee time; O(logs) |
| `exclusive_time_recursive.kara` | the logs parsed into events and read as a grammar, a call being a start, any number of calls and an end; a recursive `call` returns each call's whole length so its caller can take it off; O(logs), recursing as deep as the calls nest |
| `exclusive_time_pairs.kara` | every call matched to its end and recorded with its depth; a call's own time is its length less the lengths of the calls one level deeper inside it, found by trying every pair; O(logs^2) |
| `differential.kara` | the four arms against the definition, five properties |

Every arm prints the same 11 lines: the three LeetCode examples; six
more (one call of one unit; two calls back to back; a call after a gap;
a callee filling its caller but for its first and last units; three
calls deep; timestamps up to 10^9); a total and checksum over 300 random
cases of 1 to 5 functions and 1 to 20 calls; and the longest-running of
100 functions over 250 calls with gaps of up to 3,799,999 units, all
within 10^9. `exclusive_time.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition:
every unit of time from 0 to the last timestamp goes to the function of
the innermost call whose start and end units include it, found by
scanning all the calls. Each of 1,000 cases makes valid logs for 1 to
4 functions and 1 to 12 calls, with gaps of 0 to 3 units between events,
so that many calls last one unit or start right where another ends.

| | property |
|---|---|
| P1 | the times are the definition's |
| P2 | they add up to the time the outermost calls cover |
| P3 | renaming function `i` to `i + 1` (and the last to 0) moves its time there |
| P4 | moving every timestamp later by up to 10^6 changes nothing |
| P5 | the logs run twice, the second time after the first, give every function twice its time |

It prints `1000 cases (24059 units), 4 arms, 20000 checks, 0 failures`
under `karac __mir-run` and `karac __mir-llvm-run`, and runs clean under
`karac __mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac __mir-run`.
All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: an end giving the callee up to unit `t - 1` | P1 1000, P2 1000 |
| M2 | ★: the caller resuming at `t`, not `t + 1` | P1 823, P2 823 |
| M3 | frames: a call's length taken one short | P1 1000, P2 1000 |
| M4 | frames: the caller charged only its callee's own time | P1 574, P2 574 |
| M5 | recursive: only the last nested call taken off | P1 518, P2 518 |
| M6 | recursive: a call's length taken one short | P1 1000, P2 1000 |
| M7 | pairs: every deeper call inside taken off | P1 574, P2 574 |
| M8 | pairs: a call one level deeper taken off whenever it starts later | P1 660, P2 660, P5 823 |
| E1 | ★: the last event's time starting at 5 | 0 |
| E2 | frames: the time charged to the end log's id | 0 |
| E3 | recursive: the time charged to the end event's id | 0 |
| E4 | pairs: a deeper call starting at the same time counted | 0 |

P1 kills all eight, and P2 sees each of them as well, since each gives
some unit to two functions or to none. P3 and P4 see none: every mutant
reads only the differences between timestamps and treats every id alike,
so renaming the functions or moving all the times leaves its mistakes
where they were. P5 sees only M8, whose mistake can reach across the two
runs: with the end check gone, a call of the first run takes off calls
one level deeper from the second. The four survivors cannot change an
answer: the first log is a start with nothing running, which sets the
last event's time before reading it; an end's id is always the id of the
call it ends, so charging either is the same; and no two starts share a
timestamp, so no other call starts with this one.

## Verification

Every arm prints the same output as `exclusive_time.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints its line under all three. `karac check` passes every arm, the
differential and the bench program. All at kara `ea2a2da2be` for the
debug build and `70f54e9583` for the release build that runs `check` and
`__mir-run`.

The frozen legacy backends refuse every file at type checking. They
still hold the old rule that an argument which is already a `mut ref`,
as `seed` is inside the harness's `wide`, drops its call-site `mut`
marker; the differential also passes an element of a `Vec[String]` by
indexing, which they refuse, and they type the items of a `Vec`'s
`iter()` by value, so `*t` is an error. Legacy is frozen, so these are
noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It makes 10 inputs of 100 functions
and 250 calls (500 logs, timestamps up to about 10^9) once, then
10,000 rounds each answer one of them, picked by the round, adding up
the times and putting each into a checksum. Every implementation prints
`10 inputs of 500 logs, 10000 rounds: total 9120469479000, checksum
23909961`, the Kāra program under `karac __mir-run` included (in 30 s).

Each implementation splits every log at its colons and parses the two
numbers each round: Rust collects `split(':')` into a `Vec` of `&str`
views, Go uses `strings.Split`, Python `str.split`, and C finds the two
colons with `strchr` and parses in place with `strtoll`. Spot timings on
a shared 4-core container, three runs each (two for Python; `bench.sh`
timings need a quiet machine), each including making the inputs:

| | time |
|---|---|
| C (`clang -O3`) | 0.20 to 0.22 s |
| Rust (`rustc -O`) | 0.32 to 0.39 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.32 to 0.34 s |
| Go | 0.48 to 0.51 s |
| Python | 2.12 to 2.15 s |
| Kāra (`karac build --mir`) | 1.03 to 1.10 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend, since the legacy `karac build` refuses the bench
program as above; that edit is by hand, on top of the
`scripts/new-bench.sh` output. A copy outside the kata that drops the
forwarded `mut` markers and the two `*`s and takes `logs` as `ref
Vec[String]` builds under legacy and takes 0.93 to 0.98 s, so the
v2 build is about a tenth slower than legacy here; the `i64.parse` copy
described below is a likely cause, which is inferred, not measured.
Under `karac __mir-llvm-run` the program prints the same line in 7.8 s,
compile included; that JITs the MIR's IR without optimization passes, so
it is not a benchmark.

The Kāra build takes about three times as long as Rust and five times as
long as C. Each round reads 500 logs, so the run splits 5 million logs
and parses 10 million numbers. Kāra's `split` returns a `Vec` of new
`String`s rather than views (B-2026-10-12-7), so each log makes three
new `String`s where Rust and C copy no text, and on the v2 compiled
backend each `i64.parse` copies its text into a fresh `String` before
parsing (B-2026-10-13-34, measured there at about 30 ns a parse, which
would be about 0.3 s here). Both rows are open. That these two account
for the gap is inferred from the rows' measurements and the shape of the
loop, not profiled.

## Compiler findings

None new. The legacy failures above are not filed because legacy is
frozen.
