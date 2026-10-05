# 349. Intersection of Two Arrays

Given two integer arrays, return every value that appears in both, each value
once. LeetCode accepts the answer in any order; every arm here returns it in
ascending order, so the output is one exact string.

```
nums1 = [1, 2, 2, 1],  nums2 = [2, 2]           ->  [2]
nums1 = [4, 9, 5],     nums2 = [9, 4, 9, 8, 4]  ->  [4, 9]
```

**Constraints:** `1 <= nums1.length, nums2.length <= 1000` and
`0 <= nums1[i], nums2[i] <= 1000`.

## Approaches

| file | mechanism | cost |
|---|---|---|
| `intersection.kara` ★ | a `Set` of the first array; walk the second and keep each value the set still holds, removing it as it is kept so a repeat is not kept twice; sort the answer | `O(n + m)` expected, plus the sort of the answer |
| `intersection_sorted_set.kara` | both arrays into a `SortedSet`, then the library's `intersection`, which iterates in ascending order | `O((n + m) log(n + m))` |
| `intersection_two_pointers.kara` | sort copies of both and merge them, keeping a match unless it repeats the last value kept | `O(n log n + m log m)`, no hashing |
| `intersection_binary_search.kara` | sort both, then binary-search the second for each distinct value of the first | `O((n + m) log m)` |
| `intersection_bitmap.kara` | the values are bounded by 1,000, so two tables of 1,001 flags replace the set; sweep them in order | `O(n + m + 1001)` |
| `differential.kara` | the five arms and a linear-scan oracle on 2,880 array pairs, five properties | — |
| `bench/intersection.kara` | the ★ arm on 20,000 pairs of 1,000-value windows of a fixed pool, the problem's largest arrays | — |

None of the arms walks a `Set` in its own iteration order, so the hash
order, which differs from run to run, never reaches the output.

Every arm prints the same 6 lines: the two examples, two disjoint arrays, a
single value repeated, the bounds `0` and `1,000`, and 200 pairs of 1,000
values each at the problem's bounds, reported as the number of values found
and their sum. `intersection.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` compares the five arms on every pair of lengths `0..24`
by `0..24`, with values drawn from `0..=hi` for `hi` in 0, 3, 12 and 1,000,
and once more from `{0, 250, 500, 750, 1000}` so that both ends of the value
range turn up often: 2,880 pairs, from arrays of one repeated value to arrays
that barely overlap.
The oracle asks every value from 0 to 1,000 whether a linear scan finds it in
both arrays.

| | property |
|---|---|
| P1 | all five arms equal the oracle exactly |
| P2 | the intersection of `a` and `b` equals the intersection of `b` and `a` |
| P3 | the answer is strictly ascending, and every value in it is in both arrays |
| P4 | the intersection of `a` with itself is `a`'s distinct values, ascending |
| P5 | the intersection with an empty array is empty |

It prints `failures 0` and all properties hold on every surface, with
`2880 cases: 6265 values in all, checksum 563961149`. An independent Python
replay of the input generator, using Python's own set intersection, gives the
same line.

## Mutation testing

Eleven edits to the copies inside `differential.kara`, each run under
`karac run --interp`. All eleven are killed.

| # | mutation | how |
|---|---|---|
| M1 | set: test membership with `contains` instead of `remove`, so a repeat is kept twice | P1 to P4, 20,237 failures |
| M2 | set: reverse the answer instead of sorting it | P1 to P4, 6,555 failures |
| M3 | sorted set: `union` instead of `intersection` | P1, 1,870 failures |
| M4 | two pointers: keep every match, repeats included | P1, 1,504 failures |
| M5 | two pointers: when the first side is smaller, advance the second | P1, 1,195 failures |
| M6 | binary search: drop the final equality check | P1, 1,256 failures |
| M7 | binary search: `hi = mid - 1` | P1, 1,189 failures |
| M8 | binary search: do not skip repeats in the first array | P1, 1,773 failures |
| M9 | bitmap: keep a value either array marks | P1, 1,870 failures |
| M10 | bitmap: sweep stops at 999 | P1, 362 failures |
| M11 | oracle: ask only the first array | P1 and P2, 2,904 failures |

M10 survived the first version of the differential, whose arrays of at most
23 values in `0..=1000` almost never both held 1,000. The
`{0, 250, 500, 750, 1000}` inputs were added for it.

## Verification

All five arms plus the differential are byte-identical under `karac run`
(LLJIT), `karac run --interp`, `karac build` with `KARAC_AUTO_PAR=0`, and the
default auto-parallelising `karac build` (`scripts/surface-sweep.py`, 6
programs, 0 divergences), and the five arms match `intersection.py` byte for
byte. Built with `KARAC_AUTO_PAR=0`, all six are valgrind-clean: `0 errors`
and `0 bytes in use at exit`.

## Benchmarks

`bench/intersection.kara` and its four mirrors time the ★ arm as written. A
pool of 1,000,000 pseudo-random values in `0..=1000` is built once. Each of
20,000 pairs takes two windows of 1,000 values from it at pseudo-random
offsets, the problem's largest arrays, copies them out, and intersects them.
Every answer's length and sum are folded into the sink, so no pair can be
skipped. The Rust mirror uses `std::collections::HashSet`, the Go mirror a
built-in `map`, and the C mirror a hand-written open-addressing table.

> **Host:** only the x86-64 Linux cloud container lane exists so far, in
> [`bench/results.container-x86.json`](bench/results.container-x86.json). The
> canonical Apple M5 Pro lane (`bench/results.json`) is not measured yet, and
> `bench-lib.sh` refuses to write it from Linux. Absolute milliseconds are NOT
> comparable between hosts. Only the **within-file cross-language ratios** are.

30 runs each, 5 warmups, on a 4-core x86-64 Linux container, karac
`0.1.0-dev.10498+gd140f6afb` (kara main at `5ba1d7de6` plus the fixes for
B-2026-10-05-91 and B-2026-10-05-96, both since pushed), measured
2026-10-05, with the timed lane built with `KARAC_AUTO_PAR=0`. Python is its
own lane at 3 runs.

| implementation | mean | vs fastest |
|---|---|---|
| rust `-C target-cpu=x86-64-v3` + overflow-checks (matched) | 1159 ms ± 34 | 1.00× |
| c `-march=x86-64-v3` (matched-ISA) | 1198 ms ± 35 | 1.03× |
| rust `-O -C overflow-checks=on` (equal-safety) | 1212 ms ± 27 | 1.05× |
| rust `-O` | 1213 ms ± 19 | 1.05× |
| c `clang -O3` | 1248 ms ± 25 | 1.08× |
| **kāra `karac build`** | **1634 ms ± 36** | **1.41×** |
| go `go build` | 2226 ms ± 98 | 1.92× |
| python 3 | 2918 ms ± 96 | 2.52× |

**Kāra is 1.35× behind equal-safety Rust and 1.31× behind C; Go is 1.8×
behind those two.** The C and Rust builds are within a few percent of each
other. Where Kāra's extra third goes was not investigated: the pair loop does
three things, the copies, the set walk and the sort of the answer, and none
of them was timed alone. Python is unusually close because its `set` of small
integers is implemented in C.

Compile time (cold, 10 runs) and artefact size:

| | compile | binary | peak RSS |
|---|---|---|---|
| c | 114.0 ms ± 4.9 | 16.0 KiB | 8.9 MiB |
| rust | 240.7 ms ± 5.9 | 3891.8 KiB | 9.8 MiB |
| kāra | 311.7 ms ± 11.6 | 354.0 KiB | 10.1 MiB |
| go | — | 2214.8 KiB | 19.1 MiB |
| python | — | — | 38.1 MiB |

Peak memory is mostly the 8 MB pool. `karac build` is 2.7× clang's cold
compile and 1.3× rustc's. Its binary is 22× clang's and 11× smaller than
rustc's. Raw numbers are in `bench/results.container-x86.json`. Methodology
and caveats are in [`BENCHMARKS.md`](../../../BENCHMARKS.md).

## Compiler findings

Writing this kata turned up one gap in the compiler, fixed in the kara repo.

- **B-2026-10-05-95 (codegen): a `for` loop over a `SortedSet` that has no
  name failed to build.** The SortedSet arm loops straight over the result,
  `for v in sa.intersection(sb) { .. }`. `karac run --interp` ran it, while
  `karac run` and `karac build` stopped with "for-loop over this iterable is
  not lowered". The same loop over two `Set`s compiled, and so did binding the
  result to a `let` first. A probe found the same gap for a function that
  returns a `SortedSet` or a `SortedMap`, with or without `.iter()`. The
  compiler now lowers all of these. The arm keeps the natural form.

The author already knows the language, so none of this counts toward the
machine-fix rate.
