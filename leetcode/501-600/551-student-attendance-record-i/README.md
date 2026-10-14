# 551. Student Attendance Record I

You are given a string `s` representing an attendance record for a
student where each character signifies whether the student was absent,
late, or present on that day. The record only contains the following
three characters: `'A'`: Absent, `'L'`: Late, `'P'`: Present. The
student is eligible for an attendance award if they meet both of the
following criteria: the student was absent (`'A'`) for strictly fewer
than 2 days total; the student was never late (`'L'`) for 3 or more
consecutive days. Return `true` if the student is eligible for an
attendance award, or `false` otherwise.

```
s = "PPALLP"  ->  true
s = "PPALLL"  ->  false
```

**Constraints:** `1 <= s.length <= 1000`; `s[i]` is either `'A'`, `'L'`,
or `'P'`.

## Approaches

Every arm is `fn check_record(s: Str) -> bool`.

| file | mechanism |
|---|---|
| `student_attendance_record_i.kara` ★ | one pass over `chars()` with two counters, absences and the current run of lates, returning as soon as either reaches its limit |
| `student_attendance_record_i_contains.kara` | the rule as written: absences counted with `chars().filter(...).count()`, and `contains("LLL")` |
| `student_attendance_record_i_window.kara` | the record as `bytes()`, absences counted and every window of three bytes checked for three `L` |
| `student_attendance_record_i_states.kara` | a seven-state automaton, (absences, lates in a row) and a failed state, its table built from a step function and walked once |
| `differential.kara` | the four arms against the definition, five properties |

Every arm prints the same 16 lines: both examples and nine short
records, each with its answer; then for 300 random records of 1 to
20 days (absent with chance 3, 10 or 20 in 100 and late with chance
30, 50 or 70 in 100 in turn) the number of days, how many are fine and a
checksum; and last four records of 1,000 days (the problem's most): all
present, 333 pairs of lates and one absence, three lates on the last
days, and absent on the first and last days.
`student_attendance_record_i.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
the statement read literally: the record cut into its runs of one
character, fewer than 2 days absent in all and no run of lates 3 long.
Each arm is held to the properties below on 1,000 random records of 1 to
12 days, absent with chance 5, 10 or 20 in 100 and late with chance
40, 55 or 70 in 100 in turn; 534 of them are fine.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | the record reversed gives the same answer |
| P3 | a day present added at the end gives the same answer |
| P4 | a fine record stays fine with any one day made present |
| P5 | a present day and an absence added at the end give a fine record only if it was fine with no absence, and three lates added at the end never do |

The harness builds each record from a `Vec[char]` of days with `for c in
days.iter() { s.push(c); }`. It prints `1000 cases (534 fine), 4 arms,
20000 checks, 0 failures` under `karac __mir-run` and `karac
__mir-llvm-run`, and runs clean under `karac __mir-llvm-asan`. Until
kara B-2026-10-14-2 was fixed (kara 4979cb27c2) the MIR backends refused
that line; the mutation testing below was run then, on a copy that wrote
`s.push(*c)`, the only change, and the copy printed the same line.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers, and four that do not, each run under `karac __mir-run`. All
eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the run of lates never reset | P1 178 |
| M2 | ★: a third absence needed to fail | P1 59, P5 166 |
| M3 | contains: two absences allowed | P1 59, P5 166 |
| M4 | contains: four lates in a row needed to fail | P1 123, P5 319 |
| M5 | window: two lates in a row taken as three | P1 141, P2 77 |
| M6 | window: one absence enough to fail | P1 166, P5 368 |
| M7 | states: an absence keeps the run of lates | P1 23 |
| M8 | states: a present day keeps the run of lates | P1 144, P4 8 |
| E1 | ★: three or more lates, not exactly three | 0 |
| E2 | contains: `"LL"` looked for before `"LLL"` | 0 |
| E3 | window: the index also checked against the length | 0 |
| E4 | states: the walk ends fine below 6, not at anything but 6 | 0 |

P5 is the property aimed at the two limits, and catches every mistake in
the number of absences (M2, M3, M6) and the length of a run (M4). The
mistakes about when a run of lates ends (M1, M7, M8) are seen only by
the definition, apart from a few of M8's by P4, because the properties
change the record only at its end. M5 fails P2 as well: it counts two
lates as three only from the third day on, so a pair at the very start
passes while the same pair at the end of the reversed record does not.
E1 is safe because the walk stops at the third late, so the count never
passes 3; E2 because a record with `LLL` in it has `LL` too; E3 because
the loop's index is always in range; and E4 because 6 is the largest
state.

## Verification

Every arm prints the same output as `student_attendance_record_i.py`
under `karac __mir-run` (the v2 MIR interpreter) and `karac
__mir-llvm-run`, and runs clean under `karac __mir-llvm-asan`
(AddressSanitizer and LeakSanitizer): output identical, no error, no
leak. So does the differential, as described above. `karac check` passes
on every arm, the differential and the bench program. Checked at kara
5b82548ad6.

The frozen legacy backends: `karac run --interp` prints the same output
for every arm, and stops the differential with an error at its first
`definition(s.as_str())`. `karac run` and `karac build` panic in codegen
(src/codegen/control_flow_for.rs) on the ★, contains and states arms and
the differential, and refuse the window arm ("no handler for method
'bytes'"). Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It makes 1,000 random records of
1,000 days (the problem's most), absent with chance 1 in 2,000 and late
with chance 100 in 2,000, once; 782 in 1,000 of the checks come out
fine, so most walks read the whole record. Then 300 times over, every
record is checked, and the answers go into the checksum. Every
implementation prints `1000 records, 300 rounds each: 234600 fine,
checksum 251594982`, the Kāra program under `karac __mir-run` included
(349.9 s).

Rust and Go walk the characters of a `String` as Kāra does (`chars()`
and `range`); C walks a NUL-terminated byte array. Spot timings on a
shared 4-core container, three runs each (two for Python; `bench.sh`
timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.30 to 0.32 s |
| Rust (`rustc -O`) | 0.33 to 0.34 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.37 to 0.40 s |
| Go | 0.45 to 0.50 s |
| Python | 8.24 s |
| Kāra (`karac build --mir`) | 0.97 to 1.05 s |

The legacy `karac build` refuses this program: it moves `records[(round
* 7 + g) % count]` out of the index where v2 borrows it
(`E_INDEX_MOVE_NON_COPY`). So `bench.sh` builds the Kāra program with
`karac build --mir`, the v2 compiled backend; that edit is by hand, on
top of the `scripts/new-bench.sh` output. The `--mir` row is timed at
kara `2b8238c108`. Under `karac __mir-llvm-run` the program prints the
same line in 4.8 s, compile included; that JITs the MIR's IR without
optimization passes, so it is not a benchmark. The Kāra row is about
2.6 times Rust's with overflow checks; where the time goes was not
looked into.

## Compiler findings

kara B-2026-10-14-2, filed from this kata and fixed in kara
4979cb27c2: `s.push(c)`, `s.find(c)` and `s.split(c)` with `c` a `ref
char` from `Vec[char].iter()` passed `karac check` but were refused by
the MIR pipeline's typecheck, which types the program with the Kāra
library linked, so `iter()` yields `ref char`, and the builtin String
methods wanted exactly a `char`. Met here in the differential's record
builder, which now runs as written.
