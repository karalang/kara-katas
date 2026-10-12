# 396. Rotate Function

Given an integer array `nums` of length `n`, let `arr_k` be `nums`
rotated `k` places clockwise (to the right), and define the rotation
function `F(k) = 0 * arr_k[0] + 1 * arr_k[1] + ... + (n - 1) * arr_k[n - 1]`.
Return the largest of `F(0), F(1), ..., F(n - 1)`.

```
nums = [4, 3, 2, 6]  -> 26
  F(0) = 0*4 + 1*3 + 2*2 + 3*6 = 25
  F(1) = 0*6 + 1*4 + 2*3 + 3*2 = 16
  F(2) = 0*2 + 1*6 + 2*4 + 3*3 = 23
  F(3) = 0*3 + 1*2 + 2*6 + 3*4 = 26
nums = [100]         -> 0
```

**Constraints:** `1 <= n <= 10^5`; `-100 <= nums[i] <= 100`. The answer
fits in a 32-bit integer.

## Approaches

| file | mechanism | time | space |
|---|---|---|---|
| `rotate_function.kara` ★ | one rotation from the last: rotating once more adds the sum of all values, except the value that wraps from the last place to the first, which drops from `n - 1` copies to none, so `F(k) = F(k - 1) + sum - n * nums[n - k]` | O(n) | O(1) |
| `rotate_function_brute.kara` | every `F(k)` in full, reading `arr_k[i]` as `nums[(i - k) mod n]` | O(n^2) | O(1) |
| `rotate_function_windows.kara` | every rotation is a window of `n` values in `nums + nums`; prefix sums of the values and of index times value give each window's `F` in constant time | O(n) | O(n) |
| `rotate_function_deque.kara` | the current rotation held in a `VecDeque`; each step moves the back value to the front and updates `F` with it | O(n) | O(n) |
| `differential.kara` | the four arms on 3,000 random arrays, five properties | — | — |

Every arm prints the same 10 lines: the two LeetCode examples, seven edge
cases (one negative value, two values both ways round, all negative, all
zero, all equal, an alternating array whose best rotation is not the
first), and for 3,000
random arrays (1 to 50 values from -100 to 100) the sum of the answers
and a checksum. `rotate_function.py` mirrors the ★ arm and its output is
byte-identical.

The deque arm is O(n) given a constant-time `push_front`. Under
`karac __mir-run` `VecDeque.push_front` is O(n) today (kara
`B-2026-10-12-10`), so there the arm is quadratic.

## Differential

`differential.kara` holds copies of the four arms. For each of 3,000
random arrays of 1 to 50 values from -100 to 100:

| | property |
|---|---|
| P1 | `n` copies of one value `c` give `c * n(n - 1) / 2`, whatever the rotation |
| P2 | one nonzero value `v` among zeros gives `v * (n - 1)` if `v` > 0 (it can be rotated to the last place) and 0 otherwise (to the first) |
| P3 | rotating the array changes no answer |
| P4 | adding `c` to every value adds `c * n(n - 1) / 2` to every `F(k)`, so to the answer |
| P5 | doubling every value doubles the answer |

It prints `3000 arrays, 60000 checks, 0 failures` under
`karac __mir-run`, and a count for each property when anything fails.

## Mutation testing

Eight edits to `differential.kara`, each run under `karac __mir-run`.
All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | step: the wrapping value is taken from the wrong end | P2 2833, P3 2769 |
| M2 | step: the last rotation is never tried | P2 201, P3 336 |
| M3 | step: the wrapping value is subtracted `n - 1` times | P1 1453, P2 1363, P3 2752, P4 2780 |
| M4 | brute: the weights count from 1 | P1 2979, P2 2979, P4 2979 |
| M5 | brute: the best starts at 0 instead of `F(0)` | P1 1468, P4 1487 |
| M6 | windows: the weight is the window's position, not the array's | P1 1453, P2 2723, P3 2761, P4 2697 |
| M7 | windows: the weighted prefix counts from 1 | P1 2979, P2 2979, P4 2979 |
| M8 | deque: `F` is updated with the next value to move, not the one that just moved | P2 2921, P3 2750 |

The first M4 had the brute-force arm rotate left instead of right, and
no property caught it. It cannot change an answer: the left rotations
are the right rotations in another order, and the arm takes the largest
over all of them, so that mutant is equivalent. M4 and M7 are one
mistake in two arms and fail the same checks. No mutation fails P5:
every mutant is still linear in the values, so doubling them doubles its
answer too. P5 stays because it would catch a nonlinear mistake, such as
an overflowing or clamped sum.

## Verification

All four arms print the same output as `rotate_function.py` on every
backend: `karac __mir-run` (the v2 MIR interpreter),
`karac __mir-llvm-run`, `karac run --interp`, LLJIT, `karac build` and
`KARAC_AUTO_PAR=1 karac build`. `karac check` passes on every file. The
differential prints `60000 checks, 0 failures` on all six.

## Benchmarks

The bench program uses the ★ arm, with the parameter taken as a
`Slice[i64]` so that windows of one pool are read without copying; the
body is the same. It builds a pool of 1,000,000 values from -100 to 100
once, then makes 2,000 calls, each on a window of 100,000 values (the
problem's limit) at a random place, and folds the answers into a sum and
a checksum. Every implementation prints `2000 windows: total
2454697670428, checksum 66131566`; a 4-call cut of the Kāra program
under `karac __mir-run` prints the same as the C program cut the same
way. Spot timings on a shared 4-core container (`bench.sh` timings need
a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.32 s |
| Rust (`rustc -O`) | 0.35 s |
| Go | 0.37 s |
| Kāra (legacy `karac build`) | 0.39 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.42 s |
| Python | 36 s |

The Kāra program also prints the same line under `karac __mir-llvm-run`
in 2.9 s, compile included. That JITs the MIR's IR without optimization
passes, so it is not a benchmark. The `karac build` time is the frozen
legacy backend.

## Compiler findings

No new findings. Every arm and the differential agree on every backend.
The one gap the kata touches is already known: the MIR interpreter's
O(n) `VecDeque.push_front` (kara `B-2026-10-12-10`).
