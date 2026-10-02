# 327. Count of Range Sum

Given an integer array `nums` and two integers `lower` and `upper`, return the
number of range sums `S(i, j) = nums[i] + ... + nums[j]`, `i <= j`, that lie in
`[lower, upper]`.

```
nums = [-2, 5, -1], lower = -2, upper = 2  ->  3     ([0,0], [2,2], [0,2])
nums = [0],         lower = 0,  upper = 0  ->  1
```

## Approaches

With prefix sums `p[0] = 0` and `p[k] = nums[0] + ... + nums[k-1]`, the range
sum `S(i, j)` is `p[j+1] - p[i]`, so the answer counts the pairs `a < b` with
`lower <= p[b] - p[a] <= upper`. Every arm below counts those pairs.

| file | mechanism | cost |
|---|---|---|
| `count_range_sum.kara` ★ | merge sort the prefix sums; before each merge, count the cross pairs with two pointers over the right half | `O(n log n)` time, `O(n)` space |
| `count_range_sum_bit.kara` | walk the prefix sums in order; a Fenwick tree over their ranks counts the earlier ones in `[p - upper, p - lower]` | `O(n log n)` time, `O(n)` space |
| `count_range_sum_sorted.kara` | walk the prefix sums in order; a `SortedMap` of those seen answers the same question with one `range` call | `O(n log n)` to `O(n^2)` time, `O(n)` space |
| `count_range_sum_brute.kara` | every start, every end | `O(n^2)` time, `O(1)` space |
| `differential.kara` | the four arms on 607 inputs, seven properties | — |
| `bench/count_range_sum.kara` | 20 re-counts of a 100,000-value array by the ★ arm | — |

Every arm prints the same 28 lines: the two examples, eight edge cases, two
cases at the 32-bit limits (whose sums need 64 bits), four small random
arrays, and twelve counts over random arrays of 500, 2,000 and 3,000 values
with intervals `[-w, w]` for `w` in 0, 10, 100 and 1000. The four arms' output
is byte-identical, and `count_range_sum.py` mirrors both the ★ arm and, with
`--brute`, the brute-force arm.

## Why the merge-sort window only moves right

When two sorted halves are about to be merged, a pair with `a` in the left half
and `b` in the right half is counted when `p[a] + lower <= p[b] <= p[a] +
upper`. For each `p[a]`, the right-half values in that interval form a window
`[start, end)`. The left half is sorted, so as `a` advances, `p[a]` does not
decrease and neither does either end of the window. Both pointers therefore
cross the right half once per merge, which keeps the count at `O(n)` per level.

The same order is why the merge must finish before the caller counts: the
caller's two pointers read halves that the recursive calls have already
sorted in place, through `tmp`.

The `SortedMap` arm reads more naturally and is the slowest on a wide interval.
`range` hands back every key in the interval, so when the interval covers most
of the prefix sums seen so far, each step costs time in proportion to their
number. It is here for the ordered-map surface, not for speed.

## Differential

`differential.kara` runs the four arms on seven hand-picked arrays (the empty
array, single values, all zeros, and values at both 32-bit limits) and 600
pseudo-random arrays of 0 to 29 values within `±1` to `±6`, each with an
interval of width 0 to 8 near zero.

| | property |
|---|---|
| P1 | all four counts agree |
| P2 | `0 <= count <= n(n+1)/2` |
| P3 | widening the interval by one on each side never lowers the count |
| P4 | an interval covering every range sum counts all `n(n+1)/2` of them |
| P5 | splitting the interval at its midpoint splits the count |
| P6 | negating every value and the interval keeps the count |
| P7 | reversing `nums` keeps the count |

`rounds 607, range sums counted 25020, failures 0`, and all properties hold, on
every surface.

## Mutation testing

Twelve edits to the copies inside `differential.kara`, each built and run.

| # | mutation | outcome | how |
|---|---|---|---|
| M1 | merge: the `start` loop skips `p[b] == p[a] + lower` too (`<=` for `<`) | **killed** | P1, P6, from `[0]` with `[0, 0]` |
| M2 | merge: the `end` loop stops before `p[b] == p[a] + upper` (`<` for `<=`) | **killed** | P1, P6, from `[0]` with `[0, 0]` |
| M3 | merge: restart both pointers at `mid` for every `a` | silent (equivalent) | — |
| M4 | merge: take from the right half on ties (`<` for `<=`) | silent (equivalent) | — |
| M5 | merge: skip the copy back from `tmp` | **killed** | P1, P3, P6, from the first example |
| M6 | merge: stop recursing at two elements instead of one | **killed** | P1, P3, P4, P6 |
| M7 | Fenwick: the lower rank at `v - upper` instead of `v - upper - 1` | **killed** | P1, P5 |
| M8 | Fenwick: no `dedup` of the sorted prefix sums | silent (equivalent) | — |
| M9 | Fenwick: add `p[b]` before counting | **killed** | P1, P5, from the empty array |
| M10 | `SortedMap`: record `p[b]` before querying | **killed** | P1, P7 |
| M11 | `SortedMap`: no entry for the empty prefix `p[0] = 0` | **killed** | P1, P7 |
| M12 | `SortedMap`: `range(p - lower, p - upper)`, the bounds swapped | **killed** | P1, P7, from the first example |

The three survivors are equivalent. M3 gives the same counts in `O(n^2)` time:
restarting the window gives up the speed of the monotone pointers but not
their correctness. M4 only changes which of two equal values is copied first,
and the values are indistinguishable. M8 leaves duplicate keys in the rank
table; `rank_at_most` returns the position after the last copy of a value,
so every value of a run maps to the same rank and the tree counts the same
values.

M1 and M2 fail the same number of rounds, 845, because P6 turns one into the
other: negating the values and the interval swaps the roles of `lower` and
`upper`.

## Verification

All four arms plus the differential are byte-identical under `karac run`
(LLJIT), `karac run --interp`, `karac build` with `KARAC_AUTO_PAR=0`, and the
default auto-parallelising `karac build`. All five programs are
valgrind-clean at `-O0`, the `SortedMap` arm only with kara's fix for
B-2026-10-02-47 (below). The four arms' output is byte-identical to
`count_range_sum.py` and `count_range_sum.py --brute`.

`scripts/surface-sweep.py --filter 327- --timeout 400` reports `5 programs ·
5 clean · 0 DIVERGENCES`.

The benchmark kernel's sink matches all four language twins and Python
(`sink 167387094`).

## Benchmarks

`bench/count_range_sum.kara` and its four mirrors time the ★ arm as written.
100,000 values in `[-1000, 1000]` are built once. Each of 20 punches replaces
one value at a random position, draws a fresh interval `[-w, w]` with `w` in
`[0, 999]`, and counts the range sums of the whole array again: a fresh
prefix-sum array, sorted by the merge sort that does the counting. Each count
is folded into a rolling hash, which is the sink.

> **Host:** only the x86-64 Linux cloud container lane exists so far, in
> [`bench/results.container-x86.json`](bench/results.container-x86.json). The
> canonical Apple M5 Pro lane (`bench/results.json`) is not measured yet, and
> `bench-lib.sh` refuses to write it from Linux. Absolute milliseconds are NOT
> comparable between hosts. Only the **within-file cross-language ratios** are.

30 runs each, 5 warmups, on a 4-core x86-64 Linux container, karac
`0.1.0-dev.10196+gfcd99fa94` with B-2026-10-02-47's fix applied, measured
2026-10-02. Python is its own lane at 3 runs.

| implementation | mean | vs fastest |
|---|---|---|
| c `clang -O3` | 272.8 ms ± 10.7 | 1.00× |
| c `-march=x86-64-v3` (matched-ISA) | 274.1 ms ± 7.1 | 1.00× |
| rust `-O` | 323.1 ms ± 5.0 | 1.18× |
| rust `-O -C overflow-checks=on` (equal-safety) | 354.5 ms ± 11.8 | 1.30× |
| **kāra `karac build`** | **357.8 ms ± 12.2** | **1.31×** |
| rust `-C target-cpu=x86-64-v3` + overflow-checks (matched) | 370.2 ms ± 46.9 | 1.36× |
| go `go build` | 425.4 ms ± 18.6 | 1.56× |
| python 3 | 6195 ms ± 326 | 22.7× |

**Kāra ties Rust with overflow checks, and both trail C by 30%.** Kāra and
equal-safety Rust are 3 ms apart with standard deviations of 12 ms. Plain
`rustc -O`, which wraps on overflow instead of checking, is 10% faster than
either, which suggests (not measured separately) that the overflow checks
in the merge's inner loops cost about that much. The matched-ISA Rust row had outliers (± 47 ms) and should
not be read as slower. Go is 56% behind C.

Compile time (cold, 10 runs) and artefact size:

| | compile | binary | peak RSS |
|---|---|---|---|
| c | 117.4 ms ± 4.6 | 15.8 KiB | 3.6 MiB |
| rust | 163.1 ms ± 5.9 | 3865.7 KiB | 4.3 MiB |
| kāra | 1823 ms ± 29 | 400.5 KiB | 6.0 MiB |
| go | — | 2179.1 KiB | 14.4 MiB |
| python | — | — | 15.9 MiB |

`karac build` is 15.5× clang's cold compile and 11× rustc's. That is
B-2026-10-02-48 below: the kernel holds the same self-recursive
`count_and_sort` as the ★ arm. Kāra's binary is 25× clang's and 9.7× smaller
than rustc's. Raw numbers are in `bench/results.container-x86.json`.
Methodology and caveats are in [`BENCHMARKS.md`](../../../BENCHMARKS.md).

## Compiler findings

**No wrong answers.** All five programs were byte-identical on every surface
from the first run. Two gaps, one fixed:

- **B-2026-10-02-47 (leak, medium, fixed in kara `17a385c45`): an empty
  `SortedMap.range` result leaked its buffer.** The lowering mallocs a scratch
  buffer sized for every candidate and hands it out with `cap == count`. When
  nothing matched, `cap` was 0, which every Vec drop reads as a static buffer
  that must not be freed, so the `SortedMap` arm lost 16 bytes for every
  prefix sum whose window held no earlier one. `Column.sorted()`,
  `Column.argsort()`, `Stats.sort` and `Stats.argsort` built their results the
  same way and leaked the same way on an empty result. An empty result now
  frees the buffer and is the canonical empty Vec.
- **B-2026-10-02-48 (perf, low, open): `karac build` of the ★ arm takes 2.2 s,
  against 0.3 to 0.6 s for the other three.** None of it is LLVM: a profile
  puts 92% of the instructions in the ownership predicates that ask what a
  call does with each argument, re-walking `count_and_sort`'s body from
  inside its own two self-calls. Their cycle guards stop the recursion, but
  nothing remembers a finished answer, so the same questions are asked
  again and again.

`karac check` flagged a missing `mut` marker on a `mut ref` argument in the
Fenwick arm (E0218), and `karac fix` applied it. That says little about the
diagnostics: the author already knows the language, which is why authoring
like this never counts toward the machine-fix rate.
