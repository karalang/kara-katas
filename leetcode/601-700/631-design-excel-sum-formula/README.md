# 631. Design Excel Sum Formula

Design a sheet with `height` rows numbered from 1 and columns lettered
from `A` to `width`, every cell 0 at first. `set(row, column, val)`
writes a number to a cell. `get(row, column)` reads a cell. `sum(row,
column, numbers)` makes a cell the sum of the cells that `numbers`
names, each a single cell such as `F7` or a range of cells such as
`B3:F7`, and returns its value. A cell named twice counts twice. The
formula stays until the cell is set or given another formula, so its
value follows every change to the cells it reads. No formula reads
itself, directly or not.

```
Excel(3, C)
set(1, A, 2)
sum(3, C, [A1, A1:B2])  ->  4
set(2, B, 2)
get(3, C)               ->  6
```

**Constraints:** `height` from 1 to 26 and `width` from `A` to `Z`;
`val` from -100 to 100; 1 to 5 names in each `sum`; at most 100 calls.

## Approaches

Every arm is a `struct Excel` with `fn new(height: i64, width: char)`,
`fn set(mut ref self, row: i64, column: char, val: i64)`, `fn get(self,
row: i64, column: char) -> i64` and `fn sum(mut ref self, row:
i64, column: char, numbers: Vec[String]) -> i64`, the cells kept in one
flat `Vec` row by row.

| file | mechanism |
|---|---|
| `excel.kara` ★ | each formula a `Map` from each cell it reads to how many times its ranges cover it; a read of a formula cell adds up those cells, each read the same way; `set` and `sum` O(cells named), `get` O(the cells a formula reaches) |
| `excel_push.kara` | every value stored, and each cell's readers kept with their counts; a write pushes its change, times the count, to each reader and on through theirs; `get` O(1), a write O(the formulas that depend on it) |
| `excel_text.kara` | each formula the list of names it was given, parsed again on every read; `set` and `sum` only store, and `get` does all the work |
| `excel_rebuild.kara` | each formula a list of the cells it reads, and after every write a depth-first walk orders the formulas after the cells they read and recomputes them all; `get` O(1), a write O(cells + reads) |
| `differential.kara` | the four arms against the definition, five properties |

Every arm prints the same 8 lines: the LeetCode example's two results;
six more, from calls that give a formula that reads a formula, change a
cell two formulas read, set a cell that held a formula so that it no
longer follows its cells, and give a formula that names one cell three
times through overlapping ranges; and a checksum over 400 random calls
on a 26 by Z sheet, sets of -1,000 to 1,000, sums of one to three ranges
of up to 2 by 2 cells in the rows above, and gets, with the sheet's
final total. `excel.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition:
replaying the calls so far, a cell's value is decided by the last `set`
or `sum` written to it, or is 0 if none was, and a `sum` adds up the
cells it covers as they stand after those same calls. Each of
1,000 cases is 8 to 30 random calls on a 4 by D sheet: sets of -9 to
9, sums of one to three ranges of up to 2 by 2 cells in the rows above,
so that no formula reads itself, and gets. Each arm returns every `sum`
and `get` result and then every cell's final value.

| | property |
|---|---|
| P1 | every result and final value is the definition's |
| P2 | ranges written out as their single cells change nothing |
| P3 | every set value doubled doubles every result |
| P4 | a `get` right after a `set` or `sum` reads back what was written or returned |
| P5 | every `set` done twice changes nothing |

It prints `1000 cases (19046 calls), 4 arms, 20000 checks, 0 failures`
under `karac __mir-run` and `karac __mir-llvm-run`, and runs clean under
`karac __mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac __mir-run`.
All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a cell named twice in one formula counted once | P1 401 |
| M2 | ★: the last row of every range left out | P1 795, P2 363 |
| M3 | push: a replaced formula still told of changes to the cells it read | P1 281 |
| M4 | push: a change passed on without the count of the reader in between | P1 62 |
| M5 | text: every range cut to its first row | P1 419, P2 419 |
| M6 | text: a `set` on a formula cell leaving the formula | P1 488, P4 523 |
| M7 | rebuild: the formulas recomputed readers first | P1 177, P5 87 |
| M8 | rebuild: a new formula not recomputed | P1 794 |
| E1 | ★: the count written one plus the old | 0 |
| E2 | push: a change of zero spread like any other | 0 |
| E3 | text: the last end found at half the count of ends | 0 |
| E4 | rebuild: the cells visited last first | 0 |

P1 kills all eight. P2 sees M2 and M5, which cut a range short; written
out as single cells, the same names are no longer cut, so the two runs
disagree. P4 sees only M6: a `set` on a formula cell leaves the formula
in place, so the `get` right after it reads the formula's sum and not
the value set. P5 sees only M7: with readers recomputed first, a formula
that reads another formula is a step behind, and a `set` done twice
recomputes a second time and catches part of that up. M1, M3, M4 and
M8 fail P1 alone, and P3 sees none of the eight, since every mutant is
still linear in the values set. The four survivors cannot change an
answer: a count of one plus the old is the old plus one; spreading a
change of zero adds zero everywhere; with one end or two, half the count
of ends is the index of the last; and any order of visiting the cells
gives an order in which each formula comes after the cells it reads.

## Verification

Every arm prints the same output as `excel.py` under `karac __mir-run`
(the v2 MIR interpreter) and `karac __mir-llvm-run`, and runs clean
under `karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer):
output identical, no error, no leak. The differential prints its line
under all three. `karac check` passes every arm, the differential and
the bench program. All at kara `ea2a2da2be` for the debug build and
`9575b48af3` for the release build that runs `check` and `__mir-run`.

The frozen legacy backends refuse every file at type checking. They take
a bare parameter by value, so passing `ends[0]`, a `String` in a `Vec`,
to `position` is "cannot move out of an index expression"; and they type
the items of a `Vec`'s `iter()` by value, so the harness's `*name` and
the differential's `*r` are errors. Legacy is frozen, so these are
noted, not filed.

## Benchmarks

The bench program uses the rebuild arm, the one written the same way in
all five languages; the ★ arm's `Map` has no counterpart in C. It makes
2,000 random calls once, the same mix as the arms' random block on a
26 by Z sheet, then 60 rounds replay them on a fresh sheet, putting
every result into a checksum and adding up the final sheet. Every
implementation prints `2000 operations, 60 rounds (37980 sums): checksum
61566955, sheet total 58592400`, the Kāra program under `karac
__mir-run` included (in 342 s).

Each implementation keeps the formulas as lists of cell indexes and, on
every `set` and `sum`, allocates a fresh `seen` array and `order` list
for the walk, as the Kāra program does. Kāra, Rust, Go and Python split
each range name into a new list of its ends; C reads the name in place
with `strchr`. Spot timings on a shared 4-core container, three runs
each (two for Python; `bench.sh` timings need a quiet machine), each
including making the calls:

| | time |
|---|---|
| C (`clang -O3`) | 0.41 to 0.46 s |
| Rust (`rustc -O`) | 0.50 to 0.55 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.47 to 0.58 s |
| Go | 0.92 to 0.93 s |
| Python | 12.3 to 12.9 s |
| Kāra (`karac build --mir`) | 0.72 to 0.75 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend, since the legacy `karac build` refuses it as above;
that edit is by hand, on top of the `scripts/new-bench.sh` output. A
copy outside the kata that clones the two ends, drops the `*` on
`iter()` items and the forwarded `mut` markers, and takes `visit`'s
`formulas` as `ref` builds under legacy and takes 5.6 to 5.9 s, so the
v2 build is about 8 times faster than legacy here. Why legacy is that
slow is not profiled. Under `karac __mir-llvm-run` the program prints
the same line in 3.8 s, compile included; that JITs the MIR's IR without
optimization passes, so it is not a benchmark.

The Kāra build is about 1.4 times the Rust build and 1.7 times the C
build, and ahead of Go. That gap is not profiled.

## Compiler findings

None filed. Two legacy findings are noted here and not filed, because
legacy is frozen.

`karac check` on the differential prints a note that `Excel_star.value`
and `Excel_text.value` form a mutual recursion group. They do not: each
`value` calls only itself, and the two share nothing but the name. The
front-end effect checker groups methods of different types by their bare
name. Here both do index a `Vec`, so the effect it infers, `panics`, is
still right. In a 25-line copy outside the kata with two such types,
where only one method indexes, it also gives the other method `panics`;
`karac __mir-effects`, the v2 effect pass, gives that method no effects.

A copy of the bench outside the kata that leaves `visit`'s `formulas` a
bare parameter builds under legacy `karac build`, then stops with `vec
index out of bounds` in `recompute`. Taking it as `ref
Vec[Option[Vec[i64]]]` prints the right line.
