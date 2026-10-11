# 378. Kth Smallest Element in a Sorted Matrix

Given an `n x n` matrix whose rows and columns are each sorted in
ascending order, return the `k`-th smallest entry, counting repeats
(the `k`-th entry of the sorted list of all `n²` entries).

```
matrix = [[1, 5, 9], [10, 11, 13], [12, 13, 15]], k = 8   -> 13
matrix = [[-5]], k = 1                                     -> -5
```

**Constraints:** `1 <= n <= 300`; `-10^9 <= matrix[i][j] <= 10^9`;
every row and every column is sorted ascending; `1 <= k <= n²`.

## Approaches

| file | mechanism | time |
|---|---|---|
| `kth_smallest.kara` ★ | binary search on the value: the answer is the least `x` with at least `k` entries `<= x`, and that count is one walk up the staircase from the bottom-left corner (an entry `<= x` means its whole column above it is too, so add the column's height and step right; otherwise step up) | O(n log(range)), O(1) space |
| `kth_smallest_heap.kara` | merge the rows with a min-first `PriorityQueue` of `(value, row, column)` heads, popping `k` times; only the first `min(n, k)` rows start in the queue | O(k log min(n, k)) |
| `kth_smallest_sort.kara` | copy every entry into one list, sort it, read position `k - 1` | O(n² log n) |
| `kth_smallest_pointers.kara` | the merge without a heap: one next-column pointer per row, and `k` scans of the rows for the smallest unread entry | O(k · n) |
| `differential.kara` | the four arms against a counting oracle, 1,500 random matrices, 29,232 checks, five properties | — |

The binary search only settles on a value that is in the matrix, though
it never looks one up: the count changes only at entries, so the least
`x` with enough entries is one.

Every arm prints the same 9 lines: the two LeetCode examples, six edge
cases (`k = 1`, `k = n²`, rows that overlap, all equal, repeats across
rows, entries at both bounds), and a checksum over 100 random matrices
up to 40 by 40. Each random entry is the larger of its upper and left
neighbours plus a small step, which keeps rows and columns sorted and,
in half the matrices, makes repeats common. `kth_smallest.py` mirrors
the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms. The oracle counts,
for each entry `v`, how many entries are smaller and how many are no
larger, and answers with the `v` that has fewer than `k` below it and at
least `k` at or below it. It runs 1,500 random matrices up to 12 by 12,
a third of them stepping by at most 1.

| | property |
|---|---|
| P1 | each arm gives the oracle's value |
| P2 | transposing the matrix changes nothing |
| P3 | adding 1,000 to every entry adds 1,000 to the answer |
| P4 | the answer for `k + 1` is never smaller (checked when `k < n²`) |
| P5 | negating the matrix and turning it half around keeps it sorted, and its `k`-th smallest is minus the original's `(n² - k + 1)`-th |

It prints `1500 cases, 29232 checks, 0 failures` under
`karac __mir-run`, `karac __mir-llvm-run` and `karac run --interp`.
LLJIT and `karac build` refuse it; see Compiler findings.

## Mutation testing

Eight edits to the copies inside `differential.kara`, each run under
`karac __mir-run`. All eight are killed.

| # | mutation | how |
|---|---|---|
| M1 | search: counts the entries below `x` instead of at most `x` | P1 and P5, 2651 failures |
| M2 | search: adds the row index instead of the column's height | P1, P2 and P5, 2850 failures |
| M3 | search: a midpoint with enough entries is ruled out | P1 and P5, 1377 failures |
| M4 | heap: only the first row starts in the queue | P1, P2 and P5, 3528 failures |
| M5 | heap: the next entry comes from the row below instead of the right | P1, P2, P4 and P5, 3620 failures |
| M6 | sort: reads position `k` | P1 and P5, 1932 failures |
| M7 | pointers: compares with the first entry of the best row so far | P1, P2 and P4, 2106 failures |
| M8 | oracle: needs more than `k` entries at or below the answer | P1, 4132 failures |

Two first drafts were replaced. Rounding the search's midpoint up
never ends once `hi = lo + 1`, so it is caught only by the interpreter's
step limit. Letting ties go to the last row in the pointer arm picks an
equal value, so it is still correct.

## Verification

All four arms print the same output as `kth_smallest.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run` (the
same MIR compiled to LLVM) and `karac run --interp`. LLJIT, `karac build`
and `KARAC_AUTO_PAR=1 karac build` refuse every arm at the line that
builds the random matrices.

## Benchmarks

The bench program builds 10 random 300 by 300 matrices, the problem's
largest, and asks each for 10,000 random `k`, answered by the ★ arm.
The C mirror keeps the matrix in one flat allocation. The C, Rust, Go
and Python mirrors all print `checksum 157581360`, and so does
`karac __mir-llvm-run`. `bench.sh` cannot run yet, because it builds the
Kāra side with the legacy `karac build`, which refuses the bench program
at the same line (see Compiler findings). Timings are not taken yet;
they need a quiet machine.

## Compiler findings

One, in the legacy backends, which are frozen, so it is not filed; the
MIR interpreter and mir-llvm run every arm.

- **Legacy codegen refuses a method call on a doubly indexed element**,
  the same refusal kata 375 records. `karac build` and LLJIT stop at
  `matrix[i - 1][j].max(row[j - 1])` with `chained indexed receivers
  (a[i][j].max(...)) are deferred to v1.x; bind the inner element to a
  temporary first`. The arms keep the natural form.
