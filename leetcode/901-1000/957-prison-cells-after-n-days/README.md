# 957. Prison Cells After N Days

There are `8` prison cells in a row and each cell is either occupied or
vacant. Each day, whether the cell is occupied or vacant changes
according to the following rules: if a cell has two adjacent neighbors
that are both occupied or both vacant, then the cell becomes occupied;
otherwise, it becomes vacant. Note that because the prison is a row, the
first and the last cells in the row can't have two adjacent neighbors.
You are given an integer array `cells` where `cells[i] == 1` if the
`i`th cell is occupied and `cells[i] == 0` if the `i`th cell is vacant,
and you are given an integer `n`. Return the state of the prison after
`n` days.

```
cells = [0,1,0,1,1,0,0,1], n = 7             ->  [0,0,1,1,0,0,0,0]
cells = [1,0,0,1,0,0,1,0], n = 1000000000    ->  [0,0,1,1,1,1,1,0]
```

**Constraints:** `cells.length == 8`; `cells[i]` is either `0` or `1`;
`1 <= n <= 10^9`.

## Approaches

| file | mechanism |
|---|---|
| `prison_after_n_days.kara` ★ | a day per state seen: there are only 2^8 rows, so the days repeat. Step day by day, writing each row's first day in a `Map` keyed by the row read as a number; the first row seen twice closes a cycle, and the days left shrink to their remainder modulo its length. At most 2^8 steps whatever n |
| `prison_after_n_days_period.kara` | a period of 14: from day 1 the end cells are empty and the rows repeat with a period dividing 14, so after one day only (n - 1) mod 14 more are needed. O(1) |
| `prison_after_n_days_bits.kara` | the row as one byte, cell 0 the high bit: a cell is occupied the next day when its neighbours agree, the complement of `(s << 1) ^ (s >> 1)` with the end bits cleared, and each byte's first day sits in a 256-entry table |
| `prison_after_n_days_doubling.kara` | jumps by powers of two: a day tabulated as a function on the 256 rows, then the function for 2, 4, 8, ... days, each the one before applied twice, and the binary digits of n walked, taking the jump for each digit that is set. O(2^8 log n) |
| `prison_after_n_days_history.kara` | every row so far kept in a list; when the next row is already in it, at day f, day n is read off the list, directly when reached and otherwise at f plus its distance past f modulo the cycle |
| `differential.kara` | the five arms against the statement read literally, six properties |

The first drafts of three arms took `cells` as a bare parameter and
returned it or a row bound to it; `karac check` refused that, since a
bare parameter borrows, and `karac fix` made the parameter `own`. The
bits arm was first written with `!` for the complement; `karac fix`
rewrote it to `not` and then, on the next pass, which found `not` on an
integer, to `~`.

Every arm prints the same 14 lines: LeetCode's two examples and seven
more (the first example after 0 and 1 days, all vacant after a day, all
occupied after 10^9 days, an alternating row after 14 and 15 days, and a
row that is its own image after 999,999,999 days); for 300 random rows
after 0 to 99 days, the total of the final rows read as bytes and a
checksum; and all 256 rows after 10^9, 999,999,999, 999,999,986 and
2^29 days, each with its total and checksum. `prison_after_n_days.py`
mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: n days stepped one at a time, a cell with two neighbours both
occupied or both vacant occupied the next day and every other cell,
the two ends among them, vacant. It checks 3,200 random rows: 3,000
after 0 to 99 days against the statement, and 200 after up to 10^9 days
against the other properties.

| | property |
|---|---|
| P1 | the statement's answer, on the small cases |
| P2 | the rule is symmetric, so the row backwards ends backwards |
| P3 | from day 1 on the rows repeat every 14 days: n + 14 days give the same row |
| P4 | n days are a random first part of them followed by the rest |
| P5 | two neighbours agree exactly when their complements do, so the complemented row ends the same from day 1 on (and complemented on day 0) |
| P6 | each arm agrees with at least two of the other four |

It prints `3200 cases: rows adding to 203163, checksum 658879042, 95000
checks over 5 arms: 0 failures` under `karac __mir-run` (34 s)
and `karac __mir-llvm-run`, and the same under `karac __mir-llvm-asan`
with no error. Most of the interpreter's time goes to the doubling arm,
which builds up to 30 tables of 256 rows on every call.

## Mutation testing

Thirty-one edits to the differential, each run under
`karac __mir-llvm-run`; fifteen are kept, three to each arm, and all
fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the cycle taken one day longer | P1 2100, P3 2556, P4 1770, P5 99, P6 2280 |
| M2 | ★: a cell occupied when its neighbours differ | P1 2551, P6 2721 |
| M3 | ★: a zero remainder not stopped at | P1 187, P3 25, P4 409, P5 221, P6 201 |
| M4 | period: a period of 7 | P1 1287, P4 1296, P6 1377 |
| M5 | period: no first day taken | P1 2911, P4 2845, P5 230, P6 3110 |
| M6 | period: n mod 14 days after the first, not (n - 1) mod 14 | P1 2910, P4 2844, P6 3109 |
| M7 | bits: the end cells kept in the step | P1 609, P3 362, P4 1315, P5 666, P6 627 |
| M8 | bits: the low bit read as cell 0 | P1 2602, P4 2785, P6 2785 |
| M9 | bits: the step without the complement | P1 2224, P3 335, P4 1123, P5 1385, P6 2372 |
| M10 | doubling: a jump taken for each clear digit of n | P1 2866, P3 1246, P4 2783, P5 163, P6 3062 |
| M11 | doubling: each level the one before, not applied twice | P1 2662, P3 1991, P4 2185, P6 2851 |
| M12 | doubling: the right neighbour read one place left, at the cell itself | P1 2910, P2 2893, P3 3168, P6 3107 |
| M13 | history: the remainder counted from day 0, not from f | P1 1851, P3 287, P4 554, P5 1385, P6 1998 |
| M14 | history: the end cells copied, not cleared | P1 2185, P5 3168, P6 2333 |
| M15 | history: a reached day read one day early | P1 385, P3 385, P4 1506, P5 41, P6 385 |

P1 and P6 kill all fifteen, P4 twelve (all but M2, M12 and M14), P3 nine
(M1, M3, M7, M9 to M13, M15), P5 nine (M1, M3, M5, M7, M9, M10, M13 to
M15) and P2 one (M12).

Sixteen other edits were tried and set aside. Two failed exactly the
same checks as a kept one: bits taking the cycle one day longer, as M1,
and history occupying a cell when its neighbours differ, as M2. Six were
sound but beyond three an arm: period stepping day 0 and stopping the
middle one cell short, bits shifting by two, and doubling applying each
level three times, placing the cell bit one off and skipping the highest
digit of n. Two crashed with an index out of bounds: ★ stepping the end
cells, which reads past the row, and history taking the cycle one day
longer, which reads past the list. One ran out of time: bits not
reducing the days left by the cycle, which steps up to 10^9 times.

Five were equivalent. ★ keeping the seen days after the cycle closes:
the next lookup finds a row exactly one cycle back, and a remainder
already below the cycle is unchanged by it. ★ looking rows up without
their first cell: only the starting row can have it occupied, and it is
looked up before anything is stored. ★ counting each day twice: the
cycle comes out twice as long, and the remainder modulo twice the cycle
is still right modulo the cycle. Period using a period of 28, a multiple
of 14. And history searching for the repeat from day 1: when the day 0
row comes round again, the search goes on one day to find day 1
repeated, and n is at least 1 by then.

## Verification

Every arm prints the same output as `prison_after_n_days.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `46c2e7477d`, the runtime
archives rebuilt at the same commit. Under `karac __mir-run` period and bits
take 0.2 s, history 0.3 s, ★ 0.7 s and doubling 4.4 s, and the
differential 34 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The legacy compiler was removed from kara at M3, so there is no legacy
lane.

## Benchmarks

The bench program makes all 256 rows of 8 cells once. In each of 2,000
rounds it runs the ★ arm on every row, after 10^9 - r days in round r,
and folds each final row, read as a number, into a checksum. Every
implementation prints `2000 rounds over all 256 rows: rows adding to
32256000, checksum 884347326`. Each call gets its own copy of the row
(`clone` in Kāra and Rust, a fresh slice in Go, `list` in Python) and
keeps the first days in the language's hash map (`Map`, `HashMap`,
`map`, `dict`), and Kāra, Rust, Go and Python allocate a new row for
every day stepped. C keeps the rows in arrays on the stack and the
first days in an open-addressing table of 64 slots, also on the stack,
so it allocates nothing.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.052 to 0.090 s | 0.058 s |
| Rust (`rustc -O`) | 0.69 to 0.96 s | 0.75 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.76 to 0.95 s | 0.81 s |
| Go | 1.35 to 1.64 s | 1.51 s |
| Python | 11.4 s | |
| Kāra (`karac build --mir`) | 0.84 to 1.04 s | 0.94 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Python's run is about 196 times
C's.

v2 takes 1.16 times Rust's median time under overflow checks and 16
times C's; the gap to C is the allocation per day and the hash map,
which C has neither of. Under valgrind's cachegrind v2 runs 10.92
billion instructions and 1.83 billion branches with 103.4 million
mispredicted, Rust with overflow checks 9.58 billion, 1.50 billion and
65.0 million, and C 0.62 billion, 24.8 million and 2.59 million.
