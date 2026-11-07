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
the same way.

### Apple M5 Pro, 2026-11-07

30 runs each, 5 warmups, on the Apple M5 Pro, karac `0.8.0-dev.14781+g3dc7786b7`
(g3dc7786b7, the v2/MIR backend), measured 2026-11-07, with the Kāra binary built
`KARAC_AUTO_PAR=0`. This is the kata's first M5 measurement; Python was not run.
The last column is Kāra's mean over that row's mean.

| implementation | mean | Kāra / this |
|---|---|---|
| rust `-O` | 73.0 ms ± 0.6 | 1.73× |
| c `clang -O3` | 93.5 ms ± 0.5 | 1.35× |
| **kāra `karac build`, seq** | **126.0 ms ± 6.7** | **—** |
| rust `-O -C overflow-checks=on` (equal-safety) | 129.6 ms ± 9.2 | 0.97× |
| go `go build` | 258.6 ms ± 2.2 | 0.49× |

Kāra is 1.73× `rustc -O`, 0.97× equal-safety Rust, 1.35× C and 0.49× Go. The gap to `rustc -O` is the cost of the overflow checks Kāra keeps on by default; C's lead was not investigated. Against the legacy backend (exact counts, dd86e3955, `KARAC_AUTO_PAR=0`) Kāra executes 0.95× the instructions in 0.88× the cycles.

Compile time (cold, 10 runs) and artefact size:

| | compile | binary | peak RSS |
|---|---|---|---|
| c | 46.5 ms ± 0.8 | 32.8 KiB | 1.0 MiB |
| rust | 104.8 ms ± 2.4 | 458.1 KiB | 1.2 MiB |
| kāra | 118.1 ms ± 1.6 | 66.9 KiB | 1.2 MiB |
| go | — | 2450.9 KiB | 2.8 MiB |

`karac build` is 2.5× clang's cold compile and 1.1× rustc's. Kāra's
68,512-byte binary is 2.0× clang's and 6.8× smaller than rustc's. Raw numbers are in
[`bench/results.json`](bench/results.json). The sink matches across the Kāra,
Rust, C and Go builds (`60000 rounds on 5000 numbers: total 329429860, checksum 47720820`).

### Container x86-64 history

Spot timings on a shared 4-core container, two or three
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
