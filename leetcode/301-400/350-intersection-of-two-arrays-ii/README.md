# 350. Intersection of Two Arrays II

Given two integer arrays, return the values both hold, each as many times as
it appears in **both**: a value one array holds twice and the other three
times is in the answer twice. LeetCode accepts the answer in any order;
every arm here returns it in ascending order, so the output is one exact
string.

```
nums1 = [1, 2, 2, 1],  nums2 = [2, 2]           ->  [2, 2]
nums1 = [4, 9, 5],     nums2 = [9, 4, 9, 8, 4]  ->  [4, 9]
```

**Constraints:** `1 <= nums1.length, nums2.length <= 1000` and
`0 <= nums1[i], nums2[i] <= 1000`.

This is [#349](../349-intersection-of-two-arrays/) with multiplicity: #349
keeps each common value once, this one keeps it as often as the rarer side
holds it.

## Approaches

| file | mechanism | cost |
|---|---|---|
| `intersect.kara` ★ | count the first array in a `Map`; walk the second and keep each value whose count is still positive, spending one count each time; sort the answer | `O(n + m)` expected, plus the sort of the answer |
| `intersect_sorted_map.kara` | count both arrays in `SortedMap`s, walk the first map's keys in ascending order, and emit each value `min(count in a, count in b)` times | `O((n + m) log(n + m))` |
| `intersect_two_pointers.kara` | sort copies of both and merge them, keeping every match; LeetCode's follow-up "what if both arrays are already sorted?" | `O(n log n + m log m)`, `O(n + m)` if sorted |
| `intersect_counting.kara` | the values are bounded by 1,000, so two tables of 1,001 counts replace the map; sweep them in order | `O(n + m + 1001)` |
| `differential.kara` | the four arms and a counting oracle on 2,880 array pairs, six properties | — |
| `bench/intersect.kara` | the ★ arm on 20,000 pairs of 1,000-value windows of a fixed pool, the problem's largest arrays | — |

None of the arms walks a `Map` in its own iteration order, so the hash
order, which differs from run to run, never reaches the output.

Every arm prints the same 7 lines: the two examples, two disjoint arrays, a
value one side repeats, two sides that repeat different values a different
number of times, the bounds `0` and `1,000` with repeats, and 200 pairs of
1,000 values each at the problem's bounds, reported as the number of values
found and their sum. `intersect.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` compares the four arms on every pair of lengths `0..24`
by `0..24`, with values drawn from `0..=hi` for `hi` in 0, 3, 12 and 1,000,
and once more from `{0, 250, 500, 750, 1000}` so that both ends of the value
range turn up often: 2,880 pairs, from arrays of one repeated value to arrays
that barely overlap. The oracle counts every value from 0 to 1,000 in both
arrays by a linear scan and keeps it the smaller number of times.

| | property |
|---|---|
| P1 | all four arms equal the oracle exactly |
| P2 | the intersection of `a` and `b` equals the intersection of `b` and `a` |
| P3 | the answer is ascending, and no value in it occurs more often than in `a` or in `b` |
| P4 | the intersection of `a` with itself is `a`, sorted |
| P5 | the intersection with an empty array is empty |
| P6 | the intersection of `a` with `a` followed by `b` is `a`, sorted |

It prints `failures 0` and all properties hold on every surface, with
`2880 cases: 14447 values in all, checksum 513245796`. An independent Python
replay of the input generator, using `collections.Counter`'s own `&`, gives
the same line.

## Mutation testing

Eleven edits to the copies inside `differential.kara`, each run under
`karac run`. All eleven are killed.

| # | mutation | how |
|---|---|---|
| M1 | map: keep a value whose count is `>= 0`, so values the first array lacks are kept | P1 to P3, P5, P6, 27,166 failures |
| M2 | map: never spend a count, so every repeat in the second array is kept | P1 to P3, P6, 16,969 failures |
| M3 | map: reverse the answer instead of sorting it | P1 to P4, P6, 10,026 failures |
| M4 | map: count the first array as a set (`= 1` instead of `+= 1`) | P1, P2, P4, P6, 7,022 failures |
| M5 | sorted map: emit the larger count instead of the smaller | P1, 1,939 failures |
| M6 | sorted map: count the second array twice | P1, 1,279 failures |
| M7 | two pointers: advance the first side on a tie | P1, 2,132 failures |
| M8 | two pointers: keep a match without advancing the second side | P1, 1,279 failures |
| M9 | counting: take the larger count | P1, 2,851 failures |
| M10 | counting: sweep stops at 999 | P1, 362 failures |
| M11 | oracle: take the larger count | P1 and P2, 5,702 failures |

## Verification

All four arms plus the differential are byte-identical under `karac run`
(LLJIT), `karac run --interp`, `karac build` with `KARAC_AUTO_PAR=0`, and the
default auto-parallelising `karac build` (`scripts/surface-sweep.py`, 5
programs, 0 divergences), and the four arms match `intersect.py` byte for
byte. Built with `KARAC_AUTO_PAR=0`, all five are valgrind-clean: `0 errors`
and `0 bytes in use at exit`.

## Benchmarks

`bench/intersect.kara` and its four mirrors time the ★ arm as written. A
pool of 1,000,000 pseudo-random values in `0..=1000` is built once. Each of
20,000 pairs takes two windows of 1,000 values from it at pseudo-random
offsets, the problem's largest arrays, copies them out, and intersects them
with multiplicity. Every answer's length and sum are folded into the sink,
so no pair can be skipped; all five print `sink 320619822`. The Rust mirror
uses `std::collections::HashMap`, the Go mirror a built-in `map`, and the C
mirror a hand-written open-addressing count table.

> **Host:** only the x86-64 Linux cloud container lane exists so far, in
> [`bench/results.container-x86.json`](bench/results.container-x86.json). The
> canonical Apple M5 Pro lane (`bench/results.json`) is not measured yet, and
> `bench-lib.sh` refuses to write it from Linux. Absolute milliseconds are NOT
> comparable between hosts. Only the **within-file cross-language ratios** are.

30 runs each, 5 warmups, on a 4-core x86-64 Linux container, karac
`0.1.0-dev.10502+ga703616a1` (a local build of the B-2026-10-05-108 fix
commit, since pushed to kara main as `e1f8650e9`), measured 2026-10-05, with
the timed lane built with `KARAC_AUTO_PAR=0`. Python is its own lane at 3
runs.

| implementation | mean | vs fastest |
|---|---|---|
| c `clang -O3` | 1239 ms ± 38 | 1.00× |
| c `-march=x86-64-v3` (matched-ISA) | 1259 ms ± 17 | 1.02× |
| rust `-O` | 1329 ms ± 47 | 1.07× |
| rust `-C target-cpu=x86-64-v3` + overflow-checks (matched) | 1337 ms ± 43 | 1.08× |
| rust `-O -C overflow-checks=on` (equal-safety) | 1365 ms ± 29 | 1.10× |
| **kāra `karac build`** | **1612 ms ± 33** | **1.30×** |
| go `go build` | 2321 ms ± 66 | 1.87× |
| python 3 | 4069 ms ± 142 | 3.28× |

**Kāra is 1.18× behind equal-safety Rust and 1.30× behind C; Go is 1.7×
behind equal-safety Rust.** Where Kāra's extra time goes was not
investigated: the pair loop does three things, the copies, the map walk and
the sort of the answer, and none of them was timed alone. The gap is
narrower than on [#349](../349-intersection-of-two-arrays/)'s `Set` bench
(1.35× behind equal-safety Rust there), but the two runs were on different
containers and different compiler builds, so that comparison is a hint, not
a measurement.

Compile time (cold, 10 runs) and artefact size:

| | compile | binary | peak RSS |
|---|---|---|---|
| c | 125.3 ms ± 5.0 | 15.9 KiB | 8.9 MiB |
| rust | 271.2 ms ± 15.8 | 3892.6 KiB | 9.8 MiB |
| kāra | 353.1 ms ± 16.8 | 354.0 KiB | 10.0 MiB |
| go | — | 2207.9 KiB | 19.2 MiB |
| python | — | — | 38.1 MiB |

Peak memory is mostly the 8 MB pool. `karac build` is 2.8× clang's cold
compile and 1.3× rustc's. Its binary is 22× clang's and 11× smaller than
rustc's. Raw numbers are in `bench/results.container-x86.json`. Methodology
and caveats are in [`BENCHMARKS.md`](../../../BENCHMARKS.md).

## Compiler findings

Probing the other ways to write this kata turned up one gap, fixed in the
kara repo, and one older defect, filed there.

- **B-2026-10-05-108 (codegen): a `flat_map` over a `Map` or `SortedMap`, or
  one whose closure returns a mapped range, failed to build.** The natural
  iterator form of the SortedMap arm,
  `ca.iter().flat_map(|(v, n)| (0..n.min(cb.get_or(v, 0))).map(|_| v)).collect()`,
  ran under `karac run --interp` but stopped `karac build` and the JIT at
  "no handler for method 'collect'". The same `flat_map` in a `for` loop
  stopped at "not yet lowered". The compiler now lowers both, including a
  closure that builds a fresh `String` per element. The kata keeps its loop
  form, which is the clearer of the two.
- **B-2026-10-05-109 (codegen, open): looping over a `Vec.filled(n, s)`
  temporary of `String`s double-frees.** `for s in Vec.filled(2, base.clone())
  { r.push(s); }` aborts with "double free detected" under `karac build` and
  `karac run`. Binding the Vec to a `let` first does not. The kata does not
  use this shape; it turned up while testing the fix above.

The author already knows the language, so none of this counts toward the
machine-fix rate.
