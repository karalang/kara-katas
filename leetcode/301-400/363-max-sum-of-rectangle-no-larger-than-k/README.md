# 363. Max Sum of Rectangle No Larger Than K

Given an `m x n` integer matrix and an integer `k`, return the largest sum
of a rectangle in the matrix whose sum is no larger than `k`. Some rectangle
is guaranteed to have a sum no larger than `k`.

```
matrix = [[1, 0, 1], [0, -2, 3]], k = 2   -> 2   ([[0, 1], [-2, 3]])
matrix = [[2, 2, -1]], k = 3              -> 3
```

**Constraints:** `1 <= m, n <= 100`; `-100 <= matrix[i][j] <= 100`;
`-10^5 <= k <= 10^5`.
**Follow-up:** what if the number of rows is much larger than the number of
columns?

## Approaches

Every arm but the brute-force one fixes the rectangle's top and bottom rows
and adds the columns between them into one array, so a rectangle is a run
of that array and its sum is `prefix[j] - prefix[i]` for `i < j`. The arms
differ in how they find the best such difference at most `k`.

| file | mechanism | time |
|---|---|---|
| `max_sum.kara` ★ | walk `j` left to right with the earlier prefixes in a `SortedSet`; the least prefix at or above `prefix[j] - k`, the first element of `seen.range(prefix[j] - k, i64.MAX)`, gives the best run ending at `j` | O(m² n log n) |
| `max_sum_merge.kara` | merge sort the prefixes; before two sorted halves merge, one pointer walk finds, for each left prefix, the largest right prefix at most `k` above it | O(m² n log n) |
| `max_sum_sorted.kara` | the ★ arm with a `Vec` kept in order, a hand-written lower bound, and `insert` | O(m² n²) worst case, a memmove per insert |
| `max_sum_brute.kara` | a table of 2D prefix sums and every one of the O(m² n²) rectangles | O(m² n²) |
| `differential.kara` | the merge and sorted arms against the brute-force arm, 13,734 checks, five properties | — |

The ★ arm is written against the library spec, which gives `SortedSet` a
`range(from, to)` iterator. It does not pass `karac check` yet: see Compiler
findings. The follow-up's answer is to put the smaller dimension inside the
row-pair loop; every arm here iterates row pairs as written, since the tests
are square or small.

Every arm prints the same 12 lines: the two LeetCode examples, nine edge
cases (a single cell equal to `k` and below it, only a negative run fitting,
negative `k`, `k` above the total, a best fit that is not the largest sum,
one column, values at the bounds, a 60-column row), and a checksum over 300
random matrices up to 12 x 12. `max_sum.py` mirrors the ★ arm, with `bisect`
for the set, and its output is byte-identical to every Kāra arm's.

## Differential

`differential.kara` holds copies of the merge, sorted and brute-force arms.
The brute-force arm is the oracle. The test draws 1,500 random matrices up
to 6 x 6, half with cells in `[-3, 3]`, so that equal sums and sums exactly
`k` are common, and half in `[-100, 100]`. `k` is never below the least
cell, so some rectangle always fits.

| | property |
|---|---|
| P1 | each arm gives the oracle's answer |
| P2 | no answer exceeds `k` |
| P3 | transposing the matrix changes no answer |
| P4 | reversing every row changes no answer |
| P5 | with `k` set to one below the answer, the answer drops |

It prints `1500 cases, 13734 checks, 0 failures` under `karac __mir-run`,
`karac run --interp` and `karac build`.

## Mutation testing

Nine edits to the copies inside `differential.kara`, each run under
`karac __mir-run`. All nine are killed.

| # | mutation | how |
|---|---|---|
| M1 | merge: the pointer stops before a sum equal to `k` | P1, 926 failures |
| M2 | merge: reads `p[j]` instead of `p[j - 1]` | P1 to P5, 4835 failures |
| M3 | merge: never writes the merged halves back | P1 to P5, 3187 failures |
| M4 | merge: drops the last prefix | P1, P3 and P4, 1976 failures |
| M5 | merge: column sums not reset for a new top row | P1 and P3, 1231 failures |
| M6 | sorted: the search finds the first prefix above the bound | P1, 926 failures |
| M7 | sorted: no empty prefix, so runs from column 0 are missed | P1, P3 and P4, 1938 failures |
| M8 | sorted: column sums not reset for a new top row | P1 and P3, 1231 failures |
| M9 | oracle: skips one-row rectangles | P1, 1534 failures |

## Verification

The merge, sorted and brute-force arms print the same output as
`max_sum.py` under `karac run --interp`, `karac __mir-run` (the v2 MIR
interpreter), LLJIT, `karac build` and `KARAC_AUTO_PAR=1 karac build`. The
★ arm does not pass `karac check` yet.

## Benchmarks

The bench program solves 20 random 100 x 100 matrices, the problem's
largest, with `k` drawn from `[-10000, 10000]`. It uses the merge-sort arm,
because the ★ arm does not compile yet and C has no ordered set to mirror
it with. The Kāra build and the C, Rust, Go and Python mirrors all print
`checksum 384035913`. Timings are not taken yet; they need a quiet machine.

## Compiler findings

- **`SortedSet.range` returns a `Vec`, not the spec's iterator.**
  `docs/library/collections.md` gives `range(from, to) -> impl Iterator[Item
  = ref T]`. Since kara `2d33c06c0c` the method exists, but it returns a
  `Vec` of clones, so the ★ arm's `seen.range(prefix - k, i64.MAX).next()` is
  refused: `no method 'next' on type 'Vec'`. The stdlib thread has the
  iterator typing scheduled after its slice work. Before `2d33c06c0c`,
  `karac check` refused the method itself.
- **`range` bounds: the spec and the compiler disagreed.** The spec says
  `range` covers `[from, to)`, and every backend implemented
  `SortedMap.range` as `[from, to]`. The spec stands (kara `a697568335`):
  `range` is now half-open in the MIR interpreter, `range_inclusive` is the
  closed form, and kata 327 moved to it. The ★ arm's upper bound is
  `i64.MAX`, which no prefix reaches, so it gives the same answer either way.
