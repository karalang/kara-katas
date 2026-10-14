# 598. Range Addition II

You are given an `m x n` matrix `M` initialized with all `0`'s and an
array of operations `ops`, where `ops[i] = [ai, bi]` means `M[x][y]`
should be incremented by one for all `0 <= x < ai` and `0 <= y < bi`.
Count and return the number of maximum integers in the matrix after
performing all the operations.

```
m = 3, n = 3, ops = [[2,2],[3,3]]                                       ->  4
m = 3, n = 3, ops = [[2,2],[3,3],[3,3],[3,3],[2,2],[3,3],[3,3],[3,3],
                     [2,2],[3,3],[3,3],[3,3]]                           ->  4
m = 3, n = 3, ops = []                                                  ->  9
```

**Constraints:** `1 <= m, n <= 4 * 10^4`; `0 <= ops.length <=
10^4`; `ops[i].length == 2`; `1 <= ai <= m`; `1 <= bi <= n`.

## Approaches

Every arm is `fn max_count(m: i64, n: i64, ops: Vec[Vec[i64]]) ->
i64`, the operations borrowed. Every operation covers the cell
(0, 0), so it holds the maximum, and the cells that tie with it are the
ones every operation covers.

| file | mechanism |
|---|---|
| `max_count.kara` ★ | one loop keeping the smallest a and the smallest b, starting from m and n; the answer is their product; O(k) for k operations |
| `max_count_iter.kara` | the same two minimums by iterator, `ops.iter().map(|op| op[0]).min()`, with `unwrap_or(m)` for no operations; O(k) |
| `max_count_sorted.kara` | the a's and the b's collected and sorted, the first of each the smallest; O(k log k) |
| `max_count_histogram.kara` | how many operations reach past each row, from a histogram of the a's summed from the bottom up; the rows all k reach, times the columns all k reach, likewise; O(m + n + k) |
| `differential.kara` | the four arms against the definition, five properties |

Every arm prints the same 10 lines: the three examples above, five cases
at the edges (one cell; one operation over the whole matrix; a single
row; the two smallest sides coming from different operations; the
largest matrix with no operations, 1,600,000,000 cells),
10,000 operations, the problem's most, on the largest matrix, and a
total and checksum over 300 random cases. `max_count.py` mirrors the ★
arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
which is the problem's matrix: every operation applied to it cell by
cell, then the cells equal to its largest value counted. Each of
1,000 random cases has sides from 1 to 8 and 0 to 6 operations; in
173 of them every cell ties at the top.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | the operations in the opposite order give the same answer |
| P3 | the matrix and every operation turned on its side, m with n and a with b, give the same answer |
| P4 | one more operation over the whole matrix changes nothing |
| P5 | one more operation on the corner cell alone leaves that cell alone at the top: the answer is 1 |

It prints `1000 cases (173 with every cell at the top), 4 arms,
20000 checks, 0 failures` under `karac __mir-run` and `karac
__mir-llvm-run`, and runs clean under `karac __mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac __mir-run`.
All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the rows bounded by the operations' column counts | P1 428, P3 462, P4 55 |
| M2 | ★: the columns start from m | P1 193, P3 259, P4 55 |
| M3 | iter: the largest row count, not the smallest | P1 608, P3 632, P4 351, P5 734 |
| M4 | iter: no operations give 0 columns | P1 147, P4 147 |
| M5 | sorted: the largest column count | P1 580, P3 632, P4 329, P5 707 |
| M6 | sorted: no operations give 0 | P1 147, P4 147 |
| M7 | histogram: the rows any operation reaches | P1 839, P4 668, P5 827 |
| M8 | histogram: each side ending a row early | P1 853, P4 147, P5 1000 |
| E1 | ★: the smaller row count by `if` | 0 |
| E2 | iter: the row count by `fold` from m | 0 |
| E3 | sorted: the empty test on the column counts | 0 |
| E4 | histogram: at least every operation, not exactly | 0 |

P2 kills nothing: no arm here depends on the order of the operations,
and the property is there for one that would. M4 and M6 are wrong
exactly on the 147 cases with no operations, and P4, which adds an
operation and so takes the case out of that branch, sees the same
147 cases. M1 and M2 mix up the two sides, which turning the matrix on
its side shows more often than the definition does. The corner operation
of P5 makes the smallest side 1, so it shows every mutant that does not
take the smallest: M3, M5 and M7, and M8 on every case, since a side of
1 then ends before the first row. E1 and E2 compute the same minimum
another way, every a being at most m; E3 is safe because the two lists
have the same length; and E4 because no more operations can reach a row
than there are.

## Verification

Every arm prints the same output as `max_count.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. `karac check`
passes every arm, the differential and the bench program. All at kara
`286748264f`.

The frozen legacy backends agree too: every arm prints the same output
under `karac run --interp`, `karac run` and `karac build`, and under
`KARAC_AUTO_PAR=1 karac build`, and the differential prints its line
under `karac run --interp` and `karac build`, though `karac build` warns
that it moves `ops` and uses it again, where v2 borrows it. Only the
bench program is refused, by `karac build` at type checking: it passes
`lists[..]` to the borrowing parameter, which legacy reads as a move out
of an index (E_INDEX_MOVE_NON_COPY). Legacy is frozen, so this is noted,
not filed.

## Benchmarks

The bench program uses the ★ arm. It makes 100 lists of
10,000 operations, the problem's most, on matrices of up to 40,000 by
40,000, once, each operation within an eighth of the matrix's sides, and
then 300 times over solves every list. Every implementation prints
`100 lists, 300 rounds: total 9486902255100, checksum 752415071`, the
Kāra program under `karac __mir-run` included (136 s).

Each implementation keeps every operation as its own pair, as LeetCode
gives them: a `Vec` of `Vec`s in Rust and Kāra, a slice of slices in Go,
an `int64_t **` of `malloc`'d pairs in C (LeetCode's C signature), a
list of lists in Python; so every operation read is a step through a
pointer. Spot timings on a shared 4-core container, three runs each (two
for Python; `bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.56 to 0.60 s |
| Rust (`rustc -O`) | 0.78 to 0.81 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.76 to 0.79 s |
| Go | 0.70 to 0.71 s |
| Python | 54.8 to 57.1 s |
| Kāra (`karac build --mir`) | 0.78 to 0.87 s |

So `bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend; that edit is by hand, on top of the
`scripts/new-bench.sh` output. A copy outside this directory that passes
`lists[..].clone()` instead, which legacy builds, runs in 9.50 to
11.18 s under the legacy `karac build` and 11.16 to 11.42 s under `karac
build --mir`, three runs each. That copy spends most of its time cloning
10,000 two-value `Vec`s a call, so it measures the clone more than the
walk; the two ranges overlap, v2's at the top of legacy's. Under `karac
__mir-llvm-run` the program prints the same line in 2.94 s, compile
included; that JITs the MIR's IR without optimization passes, so it is
not a benchmark.

The Kāra row is level with Rust's. C's is about 1.4 times faster than
both. Its list of operations is an array of 8-byte pointers, where
Rust's and Kāra's is an array of 24-byte `Vec` headers, three times the
memory to walk for the same pairs; that this is the difference is a
reading of the layouts, not measured.

## Compiler findings

None. The legacy failures above are not filed because legacy is frozen.
