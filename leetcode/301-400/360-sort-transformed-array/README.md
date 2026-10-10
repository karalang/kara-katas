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

Not measured yet. The bench programs in `bench/` and their C, Rust, Go and
Python mirrors are written and agree on the printed checksum, but the timings
still have to be taken on a quiet machine. This section will carry the table
when they are.

## Compiler findings

None. All three arms and the differential ran on every backend at the first
try.
