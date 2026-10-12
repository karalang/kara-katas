# 398. Random Pick Index

Given an integer array `nums` that may hold repeated values, pick an
index of a given `target` at random; every index that holds `target`
must be equally likely.

- `Solution(nums)` keeps the array;
- `pick(target)` returns a random index `i` with `nums[i] == target`.

```
Solution([1, 2, 3, 3, 3])
pick(3) -> 2, 3 or 4, each with probability 1/3
pick(1) -> 0
```

**Constraints:** `1 <= nums.len() <= 2 * 10^4`; `-2^31 <= nums[i] <=
2^31 - 1`; `target` is in `nums`; at most `10^4` calls to `pick`.

## Approaches

Every arm keeps its random numbers in a seeded LCG and draws them as
`below(n)`, a number from 0 to n - 1.

| file | mechanism | build | per pick | extra space |
|---|---|---|---|---|
| `random_pick_index.kara` ★ | reservoir sampling: the i-th index holding the target replaces the kept index with probability 1/i, so after one walk each of the c such indices was kept with probability 1/c | O(1) | O(n) | O(1) |
| `random_pick_index_positions.kara` | a `Map` from each value to the indices that hold it; a pick draws one from the target's list | O(n) | O(1) expected | O(n) |
| `random_pick_index_sorted.kara` | the (value, index) pairs sorted once; two binary searches find the target's run, and a pick draws one pair from it | O(n log n) | O(log n) | O(n) |
| `random_pick_index_count.kara` | count the indices holding the target, draw `k` below the count, then walk to the k-th | O(1) | O(n) | O(1) |
| `differential.kara` | the four arms behind one enum on 300 random arrays, five properties | — | — | — |

The arms spend their random numbers differently (one per index holding
the target for the reservoir, one per pick for the others), so they draw
different indices. Every arm therefore prints the same 7 lines of
properties rather than the draws, as in kata 382: a chi-square test of
30,000 picks from the LeetCode example, the example's `pick(1)` and a
one-value array that always give 0, ten equal values, an array with two
repeated negative and positive values, an array of 1,000 values of four
kinds, and how many of 200 random arrays of 1 to 60 values pass the
test. The test (`fair`) checks that every pick holds the target and
that the chi-square statistic of how often each such index came up is
below `dof + 6 * sqrt(2 * dof) + 12`, far in the tail for its degrees of
freedom. `random_pick_index.py` mirrors the ★ arm, draws the same
indices, and prints the same lines.

## Differential

`differential.kara` holds copies of the four arms behind one enum. It
builds 300 random arrays of 1 to 12 values from -3 to 3, so that values
repeat, with a target taken from each, and gives each array to all four
arms.

| | property |
|---|---|
| P1 | every pick is an index that holds the target |
| P2 | a value held at one index only always gives that index |
| P3 | every index holding the target comes up within 60 picks per such index |
| P4 | over 100 picks per such index, the chi-square statistic is below the bound above |
| P5 | changing every other value to another value that is not the target leaves the picks as they were: every arm spends its random numbers on the target's indices only |

It prints `300 arrays, 6000 checks, 0 failures` under `karac __mir-run`,
and a count for each property when anything fails.

## Mutation testing

Eight edits to `differential.kara`, each run under `karac __mir-run`.
All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | reservoir: keeps the i-th index with probability 1/(i+1) | P1 300, P2 300, P4 300 |
| M2 | reservoir: never replaces an index once kept | P3 147, P4 147 |
| M3 | positions: draws only from the first half of the list | P3 147, P4 147 |
| M4 | positions: index 0 is stored as 1 | P1 95, P2 50, P3 114, P4 114 |
| M5 | sorted: the search finds the first value greater, not at least | P1 300, P2 300, P3 300, P4 300, P5 116 |
| M6 | sorted: the last pair of the run is drawn twice as often | P4 147 |
| M7 | count: the walk stops one index early | P3 147, P4 147 |
| M8 | count: the walk skips two indices at a time | P1 147, P3 147, P4 147 |

147 of the 300 targets are held at more than one index; the mutations
that only bias the choice fail exactly those. M6 is caught by P4 alone:
it still reaches every index, only not equally often. M1 can keep
nothing, and its pick is then -1.

## Verification

All four arms print the same output as `random_pick_index.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and `karac check` passes on every file. The reservoir, positions and
sorted arms also match under `karac run --interp`, LLJIT, `karac build`
and `KARAC_AUTO_PAR=1 karac build`. The differential prints `6000
checks, 0 failures` under `karac __mir-run` and `karac __mir-llvm-run`.

The count arm and the differential walk with `for v in ....iter()` and
read `*v`. The frozen legacy typechecker types those items as `i64` and
refuses the `*`, as in katas 382 to 389, so the legacy backends do not
run those two files. Not filed.

## Benchmarks

The bench program uses the ★ arm on one array of 20,000 values (the
problem's limit) from 0 to 9, from an LCG, and makes 10,000 picks (the
problem's limit), each for a target from 0 to 9, folding the picked
indices into a sum and a checksum: 200,000,000 values read and about
20,000,000 random numbers drawn. Every implementation prints `10000
picks: total 100290617, checksum 424807019`; a 100-pick cut of the Kāra
program under `karac __mir-run` prints the same as the C program cut the
same way. Spot timings on a shared 4-core container (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| Rust (`rustc -O`) | 0.35 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.36 s |
| C (`clang -O3`) | 0.36 s |
| Kāra (legacy `karac build`) | 0.37 s |
| Go | 0.49 s |
| Python | 10 s |

The Kāra program also prints the same line under `karac __mir-llvm-run`
in 1.2 s, compile included. That JITs the MIR's IR without optimization
passes, so it is not a benchmark. The `karac build` time is the frozen
legacy backend.

## Compiler findings

- **A parameter mode written before the parameter's name gets a
  message that points nowhere** (kara `B-2026-10-12-12`). The first
  draft wrote `fn new(own nums: Vec[i64])`, by analogy with the
  receiver's `own self`; the spec writes a parameter's mode in its type,
  `nums: own Vec[i64]`. `karac check` says `'own' is a reserved keyword
  and cannot be used as an identifier`, and `karac fix` offers nothing.
  `ref v: T` and `mut v: T` get the same message.
