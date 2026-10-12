# 413. Arithmetic Slices

An array is arithmetic if it has at least three numbers and every two
neighbours differ by the same amount. Given an array `nums`, return the
number of its contiguous subarrays (slices) that are arithmetic.

```
nums = [1,2,3,4]  -> 3   ([1,2,3], [2,3,4], [1,2,3,4])
nums = [1]        -> 0
```

**Constraints:** `1 <= nums.length <= 5000`; `-1000 <= nums[i] <= 1000`.

## Approaches

| file | mechanism | time | space |
|---|---|---|---|
| `arithmetic_slices.kara` ★ | slices ending here: when the difference into `i` equals the one before, every slice ending at `i - 1` grows by one and a new slice of three starts, so the count ending at `i` is one more than at `i - 1`; otherwise it is 0. Sum the counts | O(n) | O(1) |
| `arithmetic_slices_runs.kara` | maximal runs of one difference: a run of `k` numbers holds `(k - 1)(k - 2) / 2` slices, and neighbouring runs share their boundary number | O(n) | O(1) |
| `arithmetic_slices_extend.kara` | from every start, fix the first difference and walk right while it holds, counting a slice at each step past the second number | O(n^2) at worst | O(1) |
| `arithmetic_slices_recursive.kara` | the ★ arm's recurrence top down: `ending(i)` calls `ending(i - 1)`, with a table so that each end is computed once | O(n) | O(n) |
| `differential.kara` | the four arms on 3,000 random arrays, five properties, one of them a brute force over every (start, end) pair | — | — |

Every arm prints the same 11 lines: the two LeetCode examples, eight
edge cases (two numbers, three, five equal, a falling run, two runs
with a break, a geometric array, runs that share a boundary, numbers at
the limits), and for 2,000 random arrays of 1 to 60 numbers built from
runs of 1 to 8 steps of one difference from -3 to 3, the total of the
counts and a checksum. `arithmetic_slices.py` mirrors the ★ arm and its
output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms. Each of 3,000 random
cases builds an array of 1 to 40 numbers from runs of one difference,
as the harness does:

| | property |
|---|---|
| P1 | one arithmetic array of `n` numbers holds `(n - 1)(n - 2) / 2` |
| P2 | the count is that of a check of every (start, end) pair at least two apart, testing every difference between them |
| P3 | adding a constant to every number, or negating every number, changes nothing |
| P4 | the array reversed gives the same count |
| P5 | the squares `0, 1, 4, 9, ...` hold none, and neither do differences `1, 2, 1, 2, ...` |

It prints `3000 cases, 4 arms, 60000 checks, 0 failures` under
`karac __mir-run`, and a count for each property when anything fails.

## Mutation testing

Eight edits to `differential.kara`, each run under `karac __mir-run`.
All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ending: each end counts once, not once per slice | P1 2762, P2 2728 |
| M2 | ending: a break does not reset the count | P2 2404 |
| M3 | runs: neighbouring runs do not share their boundary | P2 2413, P4 2228 |
| M4 | runs: a run counts only its slices of length 3 | P1 2762, P2 2728 |
| M5 | extend: slices of length 3 are missed | P1 2836, P2 2825, P4 137, P5 2762 |
| M6 | extend: the last possible start is skipped | P1 2836, P2 2306, P4 711 |
| M7 | recursive: each step adds 2 | P1 2836, P2 2826 |
| M8 | recursive: each difference is compared with the first | P2 2453, P4 2337, P5 2762 |

M1 and M4 fail exactly the same checks: both count only the slices of
length 3, one per end and one per run position. P1 cannot see M2, since
a single run never breaks, and only P2 does. No mutant fails P3: every
arm reads only differences, which a shift or a negation keeps equal or
equal in pairs. P5 sees the mutants that stop comparing neighbouring
differences (M5, M8).

## Verification

All four arms print the same output as `arithmetic_slices.py` on every
backend: `karac __mir-run` (the v2 MIR interpreter),
`karac __mir-llvm-run`, `karac run --interp`, LLJIT, `karac build` and
`KARAC_AUTO_PAR=1 karac build`. `karac check` passes on every file.
The differential prints `60000 checks, 0 failures` on all six.

## Benchmarks

The bench program uses the ★ arm on one array of 5,000 numbers (the
problem's limit) built from runs of 1 to 30 steps of one difference
from -3 to 3, kept within -1,000 to 1,000. Each of 60,000 rounds
changes one number by -1, 0 or 1 and counts again, so no compiler can
hoist the count out of the loop; it folds the counts into a total and a
checksum. Every implementation prints `60000 rounds on 5000 numbers:
total 329429860, checksum 47720820`; a 100-round cut of the Kāra
program under `karac __mir-run` prints the same as the C program cut
the same way. Spot timings on a shared 4-core container, two or three
runs each (`bench.sh` timings need a quiet machine):

| | time |
|---|---|
| Rust (`rustc -O`) | 0.17 to 0.18 s |
| C (`clang -O3`) | 0.17 to 0.23 s |
| Go | 0.30 to 0.38 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.35 to 0.39 s |
| Kāra (legacy `karac build`) | 0.35 to 0.44 s |
| Python | 30 s |

The Kāra program also prints the same line under `karac __mir-llvm-run`
in 3.3 s, compile included; that JITs the MIR's IR without optimization
passes, so it is not a benchmark. The `karac build` time is the frozen
legacy backend.

## Compiler findings

No new findings.
