# 384. Shuffle an Array

Given an integer array `nums`, design a way to shuffle it so that every
order of its elements is equally likely.

- `Solution(nums)` keeps the array;
- `reset()` returns the array as it was given;
- `shuffle()` returns a random shuffle of it.

```
Solution([1, 2, 3])
shuffle() -> any order of [1, 2, 3], e.g. [3, 1, 2], each with probability 1/6
reset()   -> [1, 2, 3]
shuffle() -> another random order, e.g. [1, 3, 2]
```

**Constraints:** `1 <= nums.len() <= 50`; `-10^6 <= nums[i] <= 10^6`;
the values are unique; at most `10^4` calls to `reset` and `shuffle`.

## Approaches

Every arm keeps `original: Vec[i64]` and draws its random numbers from
the same seeded LCG, as `below(n)`, a number from 0 to n - 1.

| file | mechanism | per shuffle | extra space |
|---|---|---|---|
| `shuffle.kara` ★ | Fisher-Yates: walk a copy from the last position down to the second, swapping each with a position chosen from it and the ones before it | O(n) | O(n) for the copy |
| `shuffle_sort.kara` | give each element a random key from 0 to 2^31 - 2 and sort by the keys | O(n log n) | O(n) |
| `shuffle_draw.kara` | draw from a hat: take a uniformly chosen element out of a copy until it is empty | O(n^2) | O(n) |
| `shuffle_inside_out.kara` | inside-out Fisher-Yates: element i goes to a random position j from 0 to i, and what was at j moves to the end | O(n) | O(n) |
| `differential.kara` | the four arms with random numbers the test controls, 300 random arrays, five properties | — | — |

The sorting arm leaves tied keys in their original order. Ties are
rare enough with keys this wide not to show in any test here, but they
make it very slightly unfair, which is why Fisher-Yates is the ★ arm.

The arms spend their random numbers differently, so they return
different shuffles. Every arm therefore prints the same 11 lines of
properties rather than the shuffles: the LeetCode example (a shuffle,
`reset`, another shuffle), one element, no elements, repeated values
kept through 1,000 shuffles, chi-square tests over all orders of 3, 4
and 5 elements (60,000, 48,000 and 60,000 shuffles), where element 0 of
50 lands over 20,000 shuffles, and `reset` after all of them. The test
bound is `dof + 6 * sqrt(2 * dof) + 12`, far in the tail for its
degrees of freedom. `shuffle.py` mirrors the ★ arm, shuffles the same
way, and prints the same lines.

`Solution.new` takes `nums: own Vec[i64]`, since it keeps the array: a
bare parameter borrows, and `karac check` says so and names the fix.

## Differential

`differential.kara` holds copies of the four arms as functions that
take their random numbers from an `Rng` the test controls. It can be
the seeded LCG, play back a script of choices, always give the largest
number allowed, or always give 0, and it records the bound of every
call. The test builds 300 random arrays of up to 12 values from -3 to
3, so that values repeat.

| | property |
|---|---|
| P1 | every arm returns a permutation of its input, with the LCG |
| P2 | always choosing the largest number allowed gives the input (Fisher-Yates, sorting, inside-out) or the input reversed (drawing) |
| P3 | always choosing 0 gives the input rotated left by one (Fisher-Yates), the input (sorting, drawing) or rotated right by one (inside-out) |
| P4 | for 1 to 6 values, every sequence of choices an arm can make gives a different order, and there are exactly n! of them |
| P5 | with the LCG from three seeds, 12,000 shuffles of 4 values pass the chi-square test over the 24 orders |

P4 is the exact form of "every order is equally likely". It walks every
sequence of choices like an odometer, using the bounds the arm asked
for, so it also catches an arm that asks for the wrong bounds. The
sorting arm's keys are too many to walk, so it is fed every order of
the keys 0 to n - 1 instead.

It prints `300 arrays, 7104 checks, 0 failures` under
`karac __mir-run`.

## Mutation testing

Eight edits to `differential.kara`, each run under `karac __mir-run`.
All eight are killed.

| # | mutation | how |
|---|---|---|
| M1 | Fisher-Yates: never leaves an element in place (Sattolo's algorithm, `below(i)`) | P2, P4 and P5, 261 failures |
| M2 | Fisher-Yates: stops before position 1 | P3, P4 and P5, 234 failures |
| M3 | Fisher-Yates: swaps with any position, the classic biased shuffle | P2, P4 and P5, 239 failures |
| M4 | sort: keys from 0 to 1 | P5, 3 failures |
| M5 | sort: sorts by value, not by key | P2, P3, P4 and P5, 476 failures |
| M6 | draw: draws from the front half only | P2, P4 and P5, 261 failures |
| M7 | inside-out: the displaced element is lost | P1, P3, P4 and P5, 488 failures |
| M8 | inside-out: the new element is not put at j | P1, P3, P4 and P5, 497 failures |

M1 and M3 are the two well-known wrong shuffles: Sattolo's algorithm
gives only the (n - 1)! orders that are a single cycle, and swapping
with any position gives n^n equally likely outcomes, which n! does not
divide. P4 counts the outcomes, so it catches both exactly; P5 catches
them statistically. M4 is caught only by P5, because with ties nearly
every time the stable sort leaves most elements where they were, and
the scripted keys of P4 bypass the key width.

## Verification

All four arms print the same output as `shuffle.py` under every backend:
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run` (the
same MIR compiled to LLVM), `karac run --interp`, LLJIT, `karac build`
and `KARAC_AUTO_PAR=1 karac build`. `differential.kara` prints
`300 arrays, 7104 checks, 0 failures` under all six. `karac check`
passes on every file.

The differential's calls that hand an `Rng` binding to a `mut ref Rng`
parameter were first written without the `mut` call-site marker;
`karac fix` added all six.

## Benchmarks

The bench program uses the ★ arm. It builds 1,000 values once, then
calls `shuffle` 250,000 times; each shuffle is folded into a checksum
through a position-weighted sum of all its values, so no work can be
skipped. Every implementation prints
`250000 shuffles of 1000 values, checksum 926725461`. Spot timings on a
shared 4-core container (`bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.76 s |
| Rust (`rustc -O`) | 0.80 s |
| Kāra, legacy `karac build` | 0.82 s |
| Go | 2.6 s |
| Kāra, `karac __mir-llvm-run` (includes compiling with a debug `karac`) | 4.9 s |
| Python | 84 s |

`karac __mir-llvm-run` JITs the IR without LLVM's optimization
passes, through a debug-built runner, so its times show that the new
backend runs the program, not how fast it will be.

## Compiler findings

None. Every arm, the differential and the bench program work on every
backend.
