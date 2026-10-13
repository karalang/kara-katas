# 526. Beautiful Arrangement

Suppose you have `n` integers labeled `1` through `n`. A permutation
`perm` of those `n` integers (1-indexed) is a beautiful arrangement if
for every `i` (`1 <= i <= n`) either `perm[i]` is divisible by `i`, or
`i` is divisible by `perm[i]`.

Given an integer `n`, return the number of the beautiful arrangements
that you can construct.

```
n = 2  ->  2   ([1,2] and [2,1])
n = 1  ->  1
```

**Constraints:** `1 <= n <= 15`.

## Approaches

Every arm is `fn count_arrangement(n: i64) -> i64`.

| file | mechanism |
|---|---|
| `count_arrangement.kara` ★ | backtracking: fill positions 1 to n in turn, trying every unused number that fits |
| `count_arrangement_backwards.kara` | the same search filling positions n down to 1, where the high positions, with the fewest numbers that fit, cut dead branches near the root |
| `count_arrangement_masks.kara` | counting over sets: `ways[mask]` is the number of ways to fill the first positions with exactly the numbers in `mask` |
| `count_arrangement_swaps.kara` | permutations built in place by swapping each remaining number into the next position, kept only if it fits there |
| `differential.kara` | the four arms against a brute force over every permutation, four properties |

Every arm prints the same 16 lines: the count for every `n` the
problem allows, 1 to 15, and their total, `45539`. The counts are
OEIS A320843 (1, 2, 3, 8, 10, 36, 41, 132, 250, 700, 750, 4010, 4237,
10680, 24679). `count_arrangement.py` mirrors the ★ arm and its output
is byte-identical.

## Differential

The problem has fifteen inputs, so `differential.kara` checks all of
them rather than random ones. It holds copies of the four arms and a
brute force that walks every permutation of `1..=n` in lexicographic
order and checks each in full. Each arm is held to these properties
for every `n` from 1 to 15:

| | property |
|---|---|
| P1 | the count is the brute force's, for `n` up to 9 (9! = 362,880 permutations) |
| P2 | the four arms agree |
| P3 | the count is at least `n` (the identity, and 1 swapped with each other number, are all beautiful, since position 1 takes any number and any number takes 1) and at most `n!` |
| P4 | the count is at least the count for `n - 1`, since `n` can always be put last |

It prints `n from 1 to 15, 4 arms, 216 checks, 0 failures` under
`karac __mir-run`.

## Mutation testing

Twelve edits to `differential.kara`, two to each arm that change its
answers, and four that do not, each run under `karac __mir-run`. All
eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: only numbers the position divides | P1 8, P2 56, P3 14 |
| M2 | ★: a number never freed after its branch | P1 8, P2 56, P3 14 |
| M3 | backwards: the number n never tried | P1 9, P2 60, P3 15 |
| M4 | backwards: `and` for `or` in the test | P1 8, P2 56, P3 14 |
| M5 | masks: the number 1 left out of the count of positions filled | P1 3, P2 32, P4 3 |
| M6 | masks: a mask's count overwritten, not added | P1 8, P2 56, P3 14 |
| M7 | swaps: the number already at a position never kept there | P1 9, P2 60, P3 15 |
| M8 | swaps: the swap never undone | P1 6, P2 48, P4 1 |
| E1 | ★: the end tested as `pos == n + 1` | 0 |
| E2 | backwards: stop at position 1, which any number fits | 0 |
| E3 | masks: masks with no ways not skipped | 0 |
| E4 | swaps: the test's two halves the other way round | 0 |

When one arm is wrong at some `n`, all four fail P2 there, so P2
counts four failures for every `n` the mutant gets wrong. M1, M2, M4
and M6 are wrong for every `n` from 2 to 15 and fall below `n` (P3) on
all of them; M4, for one, allows only the identity, and M2 leaves
each number used after its first branch. M3 and M7
are also wrong at `n = 1`, where they find no arrangement at all. M5
miscounts the positions filled only for masks holding 1, and is wrong
at 8 values of `n`. M8 leaves the remaining numbers in a different
order after each branch; it still visits only permutations, but misses
and repeats some, at 12 values of `n`. E2 is equivalent because
position 1 takes any number: the last number left always fits there.

## Verification

Every arm prints the same output as `count_arrangement.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and runs clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints `216 checks, 0 failures` on the first two and runs clean under
the third. `karac check` passes on every arm, the differential and the
bench program.

The frozen legacy backends agree too: `karac run --interp`, LLJIT,
legacy `karac build` and a `KARAC_AUTO_PAR=1` build print the same
output for every arm, and the differential prints `216 checks, 0
failures` under `karac run --interp` and legacy `karac build`.

## Benchmarks

The bench program uses the ★ arm. It counts every `n` from 1 to 15 in
each of 20 rounds, with a fresh `used` array for each count. Every
implementation prints `n from 1 to 15, 20 rounds: total 910780,
checksum 116453033`, the Kāra program under `karac __mir-run` included
(in 73.5 s). Spot timings on a shared 4-core container, three runs each
(two for Python; `bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.96 to 0.97 s |
| Rust (`rustc -O`) | 1.25 to 1.43 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.28 to 1.41 s |
| Go | 0.95 to 0.97 s |
| Python | 12.5 to 13.0 s |
| Kāra (legacy `karac build`) | 1.13 to 1.19 s |
| Kāra (`karac build --mir`) | 1.50 to 1.54 s |

`bench.sh` is the `scripts/new-bench.sh` output as it stands: the
legacy `karac build` still compiles this program and runs it right, so
that is what it times. The `--mir` row is the v2 compiled backend,
built by hand at kara `df61cbfff6`; it is about 30% slower here than
the legacy build. Under `karac __mir-llvm-run` the
program prints the same line in 3.1 s, compile included; that JITs the
MIR's IR without optimization passes, so it is not a benchmark.

## Compiler findings

None filed. Every arm, the differential and the bench program run
right on the v2 backends, and `karac check` passes on all of them as
written.
