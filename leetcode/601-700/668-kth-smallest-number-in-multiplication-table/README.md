# 668. Kth Smallest Number in Multiplication Table

The `m` by `n` multiplication table holds `i * j` in row `i` and column
`j`, counting from 1. Given `m`, `n` and `k`, return the `k`-th smallest
number in it, counting repeats.

```
m = 3, n = 3, k = 5  ->  3   (1,2,2,3,3,4,6,6,9)
m = 2, n = 3, k = 6  ->  6   (1,2,2,3,4,6)
```

**Constraints:** 1 <= `m`, `n` <= 30,000; 1 <= `k` <= `m * n`.

## Approaches

Every arm is `fn find_kth_number(m: i64, n: i64, k: i64) -> i64`. The
table can hold 900 million numbers, so none is written out: every arm
searches on the value, asking how many entries are at most `x`, and they
differ in how they count and how they narrow the search.

| file | mechanism |
|---|---|
| `kth_smallest_number_in_multiplication_table.kara` ★ | binary search on `x` from 1 to m * n; row `i` holds `min(x / i, n)` entries at most `x`; O(m log(m n)) |
| `kth_smallest_number_in_multiplication_table_staircase.kara` | the same search, counting along the staircase's edge from the bottom-left corner, a column's height at each step right; O((m + n) log(m n)) |
| `kth_smallest_number_in_multiplication_table_blocks.kara` | the same search, counting the rows in runs that share `x / i`, the full rows at once; O(sqrt(m n) log(m n)) |
| `kth_smallest_number_in_multiplication_table_entries.kara` | the top of the range dropped to the largest entry at most `x`, so it is always a table entry; O(m log(m n)) |
| `differential.kara` | the four arms against a definition that writes out and sorts the table, five properties |

Every arm prints the same 18 lines: the two LeetCode examples; eight
small cases (one cell; the first and the last entry of a 4 by 5 table;
one row; one column; a tall table and a wide one; and the middle of a
12 by 12 table); six on the problem's largest tables (the first, middle
and last entry of 30,000 by 30,000 and one between, and 30,000 by 17 and
17 by 30,000); every `k` of a 6 by 7 table in order; and a checksum of
1,000 random tables of 1 to 40 by 1 to 40, each with a random `k`.
`kth_smallest_number_in_multiplication_table.py` mirrors the ★ arm and
its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
which writes out every entry of the table, sorts them, and takes the
`k`-th. Each of 2,000 random tables is 1 to 12 by 1 to 12, with a random
`k`.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | the table with `m` and `n` swapped gives the same answer |
| P3 | the answer is an entry of the table |
| P4 | the answer for `k` is at most the answer for `k + 1` |
| P5 | the table with one more row gives an answer at most this one |

It prints `2000 tables (84332 cells), 4 arms, 40000 checks, 0 failures`
under `karac __mir-run` and `karac __mir-llvm-run`, and runs clean under
`karac __mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac __mir-run`.
All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: each row counted without the cap at n | P1 1038, P2 1111, P3 129 |
| M2 | ★: the count required to pass k | P1 1226, P5 38 |
| M3 | staircase: one short for each column passed | P1 1889, P2 1236, P5 191 |
| M4 | staircase: the walk starting a row up | P1 1018, P2 1032 |
| M5 | blocks: each run one row short | P1 1703, P2 1443, P5 17 |
| M6 | blocks: a run let past the last row | P1 604, P2 805, P3 96, P5 1 |
| M7 | entries: the top dropped below the largest entry | P1 943, P3 317, P5 261 |
| M8 | entries: the largest entry taken as its column | P1 1048, P2 971, P3 171, P5 61 |
| E1 | ★: the search starting one above m * n | 0 |
| E2 | staircase: the test as j <= x / i | 0 |
| E3 | blocks: a run's end kept at least its start | 0 |
| E4 | entries: the top dropped to at most mid | 0 |

P1 kills all eight. P2, the table turned on its side, sees the six that
miscount rows and columns differently, and misses M2 and M7, which count
correctly and err only in where the search stops, the same whichever way
the table lies. P3 sees the four whose answer can land off the table:
M1 counts multiples of a row past its last column, M6 counts rows past
the last, and M7 and M8 drop the top of the range below an entry. The
others still stop where a count, right or wrong, rises, which only
happens at an entry. P4 sees none: each mutant's answers still rise with
`k`, wrong as they are; it stays as a check on the arms themselves.
P5, a row added, sees six, all but M1 and M4. The four survivors cannot
change an answer: the search's top need only be at least the answer; `j
<= x / i` and `i * j <= x` are the same test on positive whole numbers;
`x / q` is never below `i`; and the largest entry at most `mid` is never
above it.

## Verification

Every arm prints the same output as
`kth_smallest_number_in_multiplication_table.py` under `karac __mir-run`
(the v2 MIR interpreter) and `karac __mir-llvm-run`, and runs clean
under `karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer):
output identical, no error, no leak. The differential prints its line
under all three. `karac check` passes all four arms, the differential
and the bench program. All with the compiler at kara `8d40e1a762` for
the debug build and `72739d54d6` for the release build that runs `check`
and `__mir-run`, with runtime archives newer than the last `runtime/src`
change.

The frozen legacy backends print the same output for every arm under the
interpreter, the JIT and `karac build`, with and without
`KARAC_AUTO_PAR=1`, and run the differential to the same line under all
three. The legacy interpreter is slow on the entries arm, 72 s against
15 s for the ★ arm, past this check's 60 s limit; given longer, it
prints the same output.

## Benchmarks

The bench program uses the ★ arm. Each of 200 rounds asks for one number
from a table of 20,001 to 30,000 by 20,001 to 30,000, near the problem's
largest, with the table and `k` picked by the round, and puts the answer
into a checksum. Every implementation prints `200 rounds: checksum
713671438`, the Kāra program under `karac __mir-run` included (in 43 s).

Each implementation is the same search with the same row count, each
division capped at `n`. Spot timings on a shared 4-core container, three
runs each (two for Python; `bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.32 s |
| Rust (`rustc -O`) | 0.32 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.32 to 0.33 s |
| Go | 0.53 to 0.54 s |
| Python | 16 to 18 s |
| Kāra (`karac build --mir`) | 0.32 to 0.35 s |
| Kāra, legacy (`karac build`) | 0.32 to 0.33 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend; the frozen legacy `karac build` builds it too, and
its row is above. Under `karac __mir-llvm-run` the program prints the
same line in 1.3 s, compile included; that JITs the MIR's IR without
optimization passes, so it is not a benchmark.

So the v2 build is level with legacy, Rust and C, all of them spending
the time on one division for each row and each step of the search. Go is
behind; it has not been profiled. The comparison with C and Rust waits
until after M4.

## Compiler findings

None new. All four arms, the differential and the bench program pass
`karac check` and run the same on both v2 backends.
