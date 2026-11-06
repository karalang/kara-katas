# 360. Sort Transformed Array

Given a sorted array of integers `nums` and integers `a`, `b`, `c`, apply
`f(x) = a x^2 + b x + c` to every element and return the results in
ascending order. The follow-up asks for `O(n)`.

```
nums = [-4,-2,2,4], a = 1,  b = 3, c = 5  ->  [3,9,15,33]
nums = [-4,-2,2,4], a = -1, b = 3, c = 5  ->  [-23,-5,1,7]
```

**Constraints:** `1 <= nums.length <= 200`; `-100 <= nums[i], a, b, c <= 100`;
`nums` is sorted in ascending order.

## Approaches

| file | mechanism | cost |
|---|---|---|
| `sort_transformed.kara` ★ | two pointers from the ends: for `a >= 0` the larger end value is the largest remaining one, so fill the output from the back; for `a < 0` take the smaller end and fill from the front | `O(n)` |
| `sort_transformed_sort.kara` | `map` `f` over the input, `collect`, and sort | `O(n log n)` |
| `sort_transformed_merge.kara` | negate when `a < 0` so the parabola opens upward, find the vertex as the end of the falling run, then merge the falling run (read backwards) with the rising one | `O(n)` |
| `differential.kara` | the three arms against an insertion-sort oracle, 45,000 checks, five properties | — |

Every arm prints the same 13 lines: both LeetCode examples, ten edge cases
(empty, one element, rising and falling lines, a constant, the vertex inside,
left of and right of the input, duplicates, large values), and a checksum
over 2,000 random inputs. `sort_transformed.py` mirrors the ★ arm and its
output is byte-identical.

The case `a = 0` needs no special handling in either `O(n)` arm. In the ★
arm, a line's extremes are still at the two ends, so either branch is
correct. In the merge arm, a line is a parabola with one of its two runs
empty.

## Differential

`differential.kara` holds copies of the three arms, plus an oracle that
evaluates the polynomial itself (in Horner form, not through the arms' `f`)
and inserts each result into place. The test draws 3,000 random sorted
inputs of 0 to 12 values in `-6..=6`, so duplicates and a vertex inside the
input are common, with coefficients in `-3..=3`.

| | property |
|---|---|
| P1 | every arm returns the oracle's list |
| P2 | every arm's list is sorted |
| P3 | every arm's list has the input's length |
| P4 | negating `a`, `b` and `c` reverses and negates the list |
| P5 | adding `d` to `c` adds `d` to every value |

It prints `3000 cases, 45000 checks, 0 failures` under `karac run --interp`,
the MIR interpreter, LLJIT, and both builds.

## Mutation testing

Ten edits to the copies inside `differential.kara`, each run under the MIR
interpreter. Eight are killed. The other two are equivalent: they change the
code but not any result.

| # | mutation | how |
|---|---|---|
| M1 | two pointers: `a = 0` takes the `a < 0` branch | equivalent: a line's extremes are at the ends, so both branches are correct |
| M2 | two pointers: `a > 0` takes the smaller end | P1, P2 and P4, 4880 failures |
| M3 | two pointers: stops one value early | P1, P2, P4 and P5, 5870 failures |
| M4 | sort: no sort | P1, P2 and P4, 6544 failures |
| M5 | merge: flips for `a > 0` instead of `a < 0` | P1 and P2, 3400 failures |
| M6 | merge: the falling run stops at an equal pair | P1, P2 and P4, 2155 failures |
| M7 | merge: the flipped list is not reversed | P1, P2 and P4, 4246 failures |
| M8 | merge: ties take the rising run first | equivalent: tied values are equal |
| M9 | oracle: inserts without shifting | P1, 6177 failures |
| M10 | `f` drops the linear term | P1, 7065 failures |

M10 survived in the first draft, whose oracle called the arms' own `f`, so a
wrong `f` was wrong everywhere at once. The oracle now evaluates the
polynomial itself. A first draft of the merge arm also flipped a falling line
(`a = 0`, `b < 0`) as a separate case; mutating that clause away changed
nothing, so the clause is gone.

## Verification

All three arms and the differential are byte-identical under `karac run`
(LLJIT), `karac run --interp`, `karac __mir-run` (the v2 MIR interpreter),
`karac build`, and `KARAC_AUTO_PAR=1 karac build`, and the three arms match
`sort_transformed.py` byte for byte. The bench program prints
`checksum 79143329` under both builds, as do its C, Rust, Go and Python
mirrors.

## Benchmarks

The bench program runs 200 sorted arrays of 50,000 values, with random
coefficients, through the two-pointer pass. The Kāra build and its C, Rust,
Go and Python mirrors agree on the printed checksum.

### Apple M5 Pro, 2026-11-06

30 runs each, 5 warmups, on the Apple M5 Pro, karac `0.8.0-dev.14606+g162ee7a0e`
(g162ee7a0e, the v2/MIR backend), measured 2026-11-06, with the Kāra binary built
`KARAC_AUTO_PAR=0`. This is the kata's first measurement; Python was not run.
The last column is Kāra's mean over that row's mean.

| implementation | mean | Kāra / this |
|---|---|---|
| rust `-O` | 65.8 ms ± 0.9 | 1.12× |
| c `clang -O3` | 72.5 ms ± 0.5 | 1.01× |
| **kāra `karac build`, seq** | **73.4 ms ± 0.8** | **—** |
| rust `-O -C overflow-checks=on` (equal-safety) | 74.4 ms ± 0.6 | 0.99× |
| go `go build` | 94.5 ms ± 0.6 | 0.78× |

Kāra is 1.12× `rustc -O`, 0.99× equal-safety Rust, 1.01× C and 0.78× Go:
level with equal-safety Rust and C, behind `rustc -O`. The gaps were not investigated on this host.

Compile time (cold, 10 runs) and artefact size:

| | compile | binary | peak RSS |
|---|---|---|---|
| c | 48.3 ms ± 0.6 | 32.7 KiB | 1.8 MiB |
| rust | 91.3 ms ± 2.5 | 455.4 KiB | 1.9 MiB |
| kāra | 122.5 ms ± 2.7 | 67.0 KiB | 1.9 MiB |
| go | — | 2450.4 KiB | 8.0 MiB |

`karac build` is 2.5× clang's cold compile and 1.3× rustc's. Kāra's
68,560-byte binary is 2.0× clang's and 6.8× smaller than rustc's. Raw numbers are in
[`bench/results.json`](bench/results.json). The sink matches across the Kāra,
Rust, C and Go builds (`checksum 79143329`).

## Compiler findings

None. All three arms and the differential ran on every backend at the first
try.
