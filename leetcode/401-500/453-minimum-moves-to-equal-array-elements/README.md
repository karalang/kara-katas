# 453. Minimum Moves to Equal Array Elements

Given an integer array `nums` of size `n`, return the minimum number of
moves required to make all array elements equal. In one move, you can
increment `n - 1` elements of the array by `1`.

```
nums = [1,2,3]  ->  3   ([1,2,3] => [2,3,3] => [3,4,3] => [4,4,4])
nums = [1,1,1]  ->  0
```

**Constraints:** `1 <= nums.length <= 10^5`;
`-10^9 <= nums[i] <= 10^9`; the answer fits in a 32-bit integer.

## Approaches

Every arm is `fn min_moves(nums: Vec[i64]) -> i64`. Raising every
element but one by 1 leaves the differences between them as they were,
except that the one left out falls 1 behind, so a move is the same as
taking 1 from a single element. The answer is the number of single
decrements that bring everything down to the minimum.

| file | mechanism |
|---|---|
| `min_moves.kara` ★ | one pass for the sum and the minimum: `sum - n * min`. O(n) |
| `min_moves_sorted.kara` | sort a copy, then add up each element's distance to the first. O(n log n) |
| `min_moves_steps.kara` | sort a copy and walk the gaps between neighbours from the bottom: the gap below `sorted[i]` is crossed by the `n - i` elements from `i` up. O(n log n) |
| `min_moves_levels.kara` | count each value in a `SortedMap`, then repeatedly bring the top level down to the next one, at its count times the drop, merging the two. O(n log n) |
| `differential.kara` | the four arms on 1,500 random cases, five properties |

Every arm prints the same 9 lines: the two LeetCode examples, one
element, two elements, the two extremes, a minimum below two equal
maxima, one outlier, a mixed array, and for 300 random arrays of 1 to
200 numbers (spread over 1, 10, 1,000 or every value from -10^9 to
10^9) the total moves and a checksum. The arms use `i64`, so answers
past 32 bits, which the random arrays reach, print as they are.
`min_moves.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and runs them on
1,500 random cases.

| | property |
|---|---|
| P1 | on 1 to 4 numbers within 0 to 3, the count is a breadth-first search's over the moves themselves (a state is each number's difference to the smallest; leaving out a largest number never widens the spread, so a shortest path stays within it) |
| P2 | on 1 to 40 numbers over a mixed spread, adding one constant to every number keeps the count |
| P3 | multiplying every number by 1 to 5 multiplies the count by the same factor |
| P4 | listing the numbers in another order keeps the count |
| P5 | one more number `v`, at or above the smallest `m`, anywhere in the array, adds `v - m` |

It prints `1500 cases, 4 arms, 30000 checks, 0 failures` under
`karac __mir-run`, and a count for each property when anything fails.

## Mutation testing

Eight edits to `differential.kara`, two to each arm, each run under
`karac __mir-run`. All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | sum: the minimum starts at 0 | P1 761, P2 575, P5 20 |
| M2 | sum: the maximum is taken for the minimum | P1 1000, P5 1348 |
| M3 | sorted: every number is raised to the largest | P1 531, P5 1327 |
| M4 | sorted: the copy is reversed, not sorted | P1 557, P4 982, P5 1018 |
| M5 | steps: a gap costs the numbers below it | P1 531, P5 1327 |
| M6 | steps: the lowest gap is skipped | P1 750, P5 877 |
| M7 | levels: a drop costs 1, not the level's count | P1 589, P5 750 |
| M8 | levels: only one number joins the level below | P1 107, P5 687 |

P1 and P5 see all eight. P3 sees none: every mutant still computes a
sum of differences, which scales with the numbers. P2 sees only M1,
whose starting minimum of 0 does not move with the numbers. M3 and M5
fail the same checks: both count the moves that raise every number to
the largest, which is the answer for "add 1 to one element per move",
not this problem.

## Verification

All four arms print the same output as `min_moves.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and `karac check` passes on every file. The differential prints
`30000 checks, 0 failures` on both. The four arms and the differential
also run clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak.

On the frozen legacy backends the ★, sorted and steps arms match under
`karac run --interp`. LLJIT and `karac build` stop in the legacy code
generator on the harness's index into an array literal ("Index operator
applied to non-array type"). The levels arm and the differential do not
type-check on legacy: its `SortedMap.floor` hands out the key by value,
so `*top` is rejected. Legacy `karac build` also rejects the bench
program (see Benchmarks). Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It builds 10 random arrays of
1,000,000 numbers from -10^9 to 10^9 once, then runs 20 rounds; each
round sets one number in every array to a new random value and counts
the moves for every array, so no count can be carried over from the
round before. Every implementation prints `20 rounds on 10 arrays of
1000000: 187279637438174816 moves, checksum 465561932`, the Kāra
program under `karac __mir-run` included (in 70 s).

The legacy `karac build` rejects the bench program (it moves `all[a]`
out of the index, where v2 borrows it), so `bench.sh` builds the Kāra
program with `karac build --mir`, the v2 compiled backend. That edit is
by hand, on top of the `scripts/new-bench.sh` output.

The mirrors keep the ★ arm's structure: one pass for the sum and the
minimum.

### Apple M5 Pro, 2026-11-07

30 runs each, 5 warmups, on the Apple M5 Pro, karac `0.8.1-dev.14833+gfa3eab9b4`
(gfa3eab9b4, the v2/MIR backend), measured 2026-11-07, with the Kāra binary built
`KARAC_AUTO_PAR=0`. This is the kata's first M5 measurement; Python was not run.
The last column is Kāra's mean over that row's mean.

| implementation | mean | Kāra / this |
|---|---|---|
| c `clang -O3` | 51.4 ms ± 0.4 | 2.26× |
| rust `-O` | 51.8 ms ± 0.3 | 2.24× |
| rust `-O -C overflow-checks=on` (equal-safety) | 115.5 ms ± 1.0 | 1.00× |
| **kāra `karac build`, seq** | **116.0 ms ± 0.5** | **—** |
| go `go build` | 159.0 ms ± 1.2 | 0.73× |

Kāra is 2.24× `rustc -O`, 1.00× equal-safety Rust, 2.26× C and 0.73× Go. The gap to `rustc -O` and C is the cost of the overflow checks Kāra keeps on by default (1.00× equal-safety Rust).

Compile time (cold, 10 runs) and artefact size:

| | compile | binary | peak RSS |
|---|---|---|---|
| c | 48.1 ms ± 0.9 | 32.9 KiB | 77.6 MiB |
| rust | 92.7 ms ± 2.5 | 455.9 KiB | 79.9 MiB |
| kāra | 118.0 ms ± 3.2 | 66.9 KiB | 77.6 MiB |
| go | — | 2450.4 KiB | 137.2 MiB |

`karac build` is 2.5× clang's cold compile and 1.3× rustc's. Kāra's
68,504-byte binary is 2.0× clang's and 6.8× smaller than rustc's. Raw numbers are in
[`bench/results.json`](bench/results.json). The sink matches across the Kāra,
Rust, C and Go builds (`20 rounds on 10 arrays of 1000000: 187279637438174816 moves, checksum 465561932`).

### Container x86-64 history

Spot timings on a shared 4-core container, three runs each
(two for Python; `bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.32 to 0.41 s |
| Rust (`rustc -O`) | 0.29 to 0.42 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.23 to 0.38 s |
| Go | 0.70 to 0.77 s |
| Python | 12.0 to 12.6 s |
| Kāra (`karac build --mir`) | 0.31 to 0.36 s |

The runs overlap too much to rank C, Rust and Kāra; part of each is
building the arrays, 20 million calls to the random number generator.

## Compiler findings

- **B-2026-10-12-28** (MIR front end, fixed in kara `b47c3c85e5`): a
  `SortedMap.floor` entry taken out with `.expect(...)`, as in
  `let (top, _) = levels.floor(i64.MAX).expect("a top level");` then
  `let top = *top;`, lost its `ref`s on the MIR backends, and `*top`
  was rejected with "found 'i64'". The levels arm used a let-else form
  until the fix and is back to `.expect(...)`.
