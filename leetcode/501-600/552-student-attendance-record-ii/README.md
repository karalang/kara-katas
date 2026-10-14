# 552. Student Attendance Record II

An attendance record for a student can be represented as a string where
each character signifies whether the student was absent, late, or
present on that day. The record only contains the following three
characters: `'A'`: Absent, `'L'`: Late, `'P'`: Present. Any student is
eligible for an attendance award if they meet both of the following
criteria: the student was absent (`'A'`) for strictly fewer than 2 days
total; the student was never late (`'L'`) for 3 or more consecutive
days. Given an integer `n`, return the number of possible attendance
records of length `n` that make a student eligible for an attendance
award. The answer may be very large, so return it modulo `10^9 + 7`.

```
n = 2      ->  8
n = 1      ->  3
n = 10101  ->  183236316
```

**Constraints:** `1 <= n <= 10^5`.

## Approaches

Every arm is `fn check_record(n: i64) -> i64`. A record that can still
win is in one of six states: 0 or 1 absences, and 0, 1 or 2 lates at its
end.

| file | mechanism |
|---|---|
| `student_attendance_record_ii.kara` ★ | six counters rolled forward a day at a time, each day a fresh `Vec` of six from the last; O(n) |
| `student_attendance_record_ii_matrix.kara` | one day's step as a 6 x 6 matrix, raised to the power n by squaring; O(log n) matrix products |
| `student_attendance_record_ii_split.kara` | around the one absence: f[i] records of P and L alone with no three lates (f[i] = f[i - 1] + f[i - 2] + f[i - 3]), then f[n] plus f[i] f[n - 1 - i] for the absence on each day i; O(n) |
| `student_attendance_record_ii_table.kara` | the whole table dp[i][a][l] kept, flat in one `Vec` of 6 (n + 1); O(n) time and memory |
| `differential.kara` | the four arms against the definition, five properties |

Every arm prints the same 10 lines: the three examples, the answers for
1 to 12 days, a checksum over 300 random lengths from 1 to 2,000, and
five lengths up to 100,000 (the problem's most).
`student_attendance_record_ii.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
the statement read literally a day at a time: records counted by their
number of A's and by their last two days, a new day refused if it is a
second A or the third L in a row. It returns the count for every length
up to n, and also counts with no A allowed at all, for P3. Each arm is
held to the properties below on 1,000 random lengths, from 1 to 8, 1 to
20 or 1 to 300 in turn.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | up to 18 days, where nothing wraps, more than for a day fewer and at most three times as many |
| P3 | the records with no A, and those with one A between two such records, add up to the answer |
| P4 | the answer is reduced: from 0 to 10^9 + 6 |
| P5 | up to 8 days, every record written out and counted one by one |

It prints `1000 cases, 4 arms, 20000 checks, 0 failures` under `karac
__mir-run` and `karac __mir-llvm-run`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers, and four that do not, each run under `karac __mir-run`. All
eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: only one late in a row allowed | P1 940, P3 940, P5 421 |
| M2 | ★: a second absence allowed | P1 940, P3 940, P5 421 |
| M3 | matrix: the answer read down a column, not along the start row | P1 940, P3 940, P5 421 |
| M4 | matrix: the step multiplied in on the even bits | P1 1000, P2 525, P3 1000, P5 481 |
| M5 | split: three records of two days, not four | P1 940, P3 940, P5 421 |
| M6 | split: the days after the absence counted one too many | P1 1000, P3 1000, P5 481 |
| M7 | table: a second late taken from a run of two | P1 940, P3 940, P5 421 |
| M8 | table: an absence only after a present day | P1 940, P3 940, P5 421 |
| E1 | ★: empty states not skipped | 0 |
| E2 | matrix: the step multiplied on the left | 0 |
| E3 | split: the absence's day tried from the last | 0 |
| E4 | table: room for one more day than needed | 0 |

Six mutants fail the same 940 cases: every length from 2 days on, since
each of those mistakes already changes the count for two days, and the
60 cases of one day are the ones they get right. M4 and M6 are wrong at
one day as well. The answer is one number, so the properties are about
its size and how it splits: P2 sees only M4, whose wrong powers break
the steady growth from one length to the next, and P4 sees nothing,
since every arm reduces each sum. E2 is safe because powers of one
matrix commute, E1 because skipping an empty state adds nothing, and
E3 and E4 because the order of a sum and spare room at the end of a
table change no count.

## Verification

Every arm prints the same output as `student_attendance_record_ii.py`
under `karac __mir-run` (the v2 MIR interpreter) and `karac
__mir-llvm-run`, and runs clean under `karac __mir-llvm-asan`
(AddressSanitizer and LeakSanitizer): output identical, no error, no
leak. `karac check` passes on every arm, the differential and the bench
program.

The frozen legacy backends: the matrix, split and table arms print the
same output under `karac run --interp`, `karac run` and `karac build`,
and under `KARAC_AUTO_PAR=1 karac build`. The ★ arm, the differential
and the bench program stop at type checking under all three, on `*c`
over `iter()` of a `Vec[i64]` ("unary '*' requires 'ref T' ... found
'i64'"). Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It answers 100 lengths near
100,000 (the problem's most), length k being 100,000 - (k * 997) %
1000, once each, and folds the answers into a checksum. Every
implementation prints `100 lengths, 9915850 days: checksum
744784518`, the Kāra program under `karac __mir-run` included (56.1 s).

Rust and Go make a fresh vector of six each day as the Kāra arm does; C
uses a local array of six, which is what a fresh `Vec` of six would be
if it never touched the heap. Spot timings on a shared 4-core container,
three runs each (two for Python; `bench.sh` timings need a quiet
machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.12 to 0.13 s |
| Rust (`rustc -O`) | 0.27 to 0.33 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.23 to 0.30 s |
| Go | 0.43 to 0.46 s |
| Python | 12.98 to 13.72 s |
| Kāra (`karac build --mir`) | 0.30 to 0.35 s |

The legacy `karac build` refuses this program (see Verification). So
`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend; that edit is by hand, on top of the
`scripts/new-bench.sh` output. The `--mir` row is timed at kara
`2b8238c108`. Under `karac __mir-llvm-run` the program prints the same
line in 1.9 s, compile included; that JITs the MIR's IR without
optimization passes, so it is not a benchmark. The Kāra row is level
with Rust's; C is faster because it allocates nothing.

## Compiler findings

None new. Nothing was filed from this kata; the legacy failures above
are not filed because legacy is frozen.
