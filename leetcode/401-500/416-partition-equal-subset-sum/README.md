# 416. Partition Equal Subset Sum

Given an array `nums` of positive integers, return whether it can be
split into two subsets whose sums are equal.

```
nums = [1,5,11,5]  -> true    ([1,5,5] and [11])
nums = [1,2,3,5]   -> false
```

**Constraints:** `1 <= nums.length <= 200`; `1 <= nums[i] <= 100`.

## Approaches

| file | mechanism | time | space |
|---|---|---|---|
| `can_partition.kara` ★ | sums up to half: the total must be even and some subset must reach half of it. A table says which sums some subset of the numbers so far reaches; each number `x` marks `s` where `s - x` was marked, walking `s` downward so that `x` is used once | O(n · total) | O(total) |
| `can_partition_bits.kara` | the same table as bits, 64 to a `u64` word: a number `x` ORs in the whole set shifted up by `x` bits, word by word from the top, carrying bits across words | O(n · total / 64) | O(total / 64) |
| `can_partition_memo.kara` | top-down search: whether the numbers from `i` on hold a subset summing to what is left, taking `nums[i]` if it fits or not, with a table keyed by (`i`, what is left) | O(n · total) | O(n · total) |
| `can_partition_sums.kara` | a `Set` of every sum some subset reaches, from `{0}`; each number adds itself to every sum in the set, kept up to half | O(n · total) | O(total) |
| `differential.kara` | the four arms on 2,000 random arrays, five properties, one of them a brute force over every subset | — | — |

Every arm prints the same 12 lines: the two LeetCode examples, eight
edge cases (one number, two equal, two unequal, an even total with no
split, an odd total, four 100s with 99 and 1, twenty-five 1s with 100,
two hundred numbers alternating 100 and 99), and for 2,000 random
arrays of 1 to 40 numbers from 1 to a random limit of up to 100, how
many can be split and a checksum. `can_partition.py` mirrors the ★ arm
and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms. Each of 2,000
random cases makes an array of 1 to 12 numbers from 1 to a random limit
of up to 100, small enough to try every subset:

| | property |
|---|---|
| P1 | the answer is whether some subset sums to half the total, trying all `2^n` subsets |
| P2 | the array reversed, or rotated by a random amount, gives the same answer |
| P3 | doubling every number changes nothing, and adding two equal numbers never turns a split into none |
| P4 | the numbers joined with more numbers of the same total, cut at random, and shuffled, always split |
| P5 | an odd total never splits, and neither does an array with one number larger than all the others together |

It prints `2000 cases, 4 arms, 40000 checks, 0 failures` under
`karac __mir-run`, and a count for each property when anything fails.
A first draft of P3 said adding two equal numbers changes nothing; that
is false (`[1, 3]` cannot split, `[1, 3, 1, 1]` can) and every arm
failed it the same way, so the property was corrected, not the arms.

## Mutation testing

Eight edits to `differential.kara`, each run under `karac __mir-run`.
All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | half: an odd total is not refused | P1 625, P3 625, P5 1260 |
| M2 | half: no subset starts at a number on its own | P1 488, P4 2000 |
| M3 | bits: no bits carry over from the word below | P1 286, P3 113, P4 1307 |
| M4 | bits: the lowest word to shift into is skipped | P1 488, P4 2000 |
| M5 | memo: a number may not take all that is left | P1 488, P4 2000 |
| M6 | memo: the memo is keyed by what is left alone | P1 5, P2 8, P4 3 |
| M7 | sums: a sum reaching exactly half is not kept | P1 488, P4 2000 |
| M8 | sums: each number adds only itself, not itself to every sum | P1 470, P3 18, P4 1793 |

M2, M4, M5 and M7 each make their arm answer `false` on every array,
so they fail the same checks: the 488 random arrays that do split and
every joined array. M1 answers `true` wherever half the total rounded
down is reachable. M3 matters only once half the total passes 63, when
the table spans two words. M6 lets two searches that reach the same
amount left at different numbers share an answer; that is wrong only on
16 of the 40,000 checks, the weakest kill here, and P1, P2 and P4 each
see some of it. No arm or mutant fails P5 except M1: refusing an odd
total, and finding no subset past a number larger than the rest, are
both what a correct table does without trying.

## Verification

All four arms print the same output as `can_partition.py` on every
backend: `karac __mir-run` (the v2 MIR interpreter),
`karac __mir-llvm-run`, `karac run --interp`, LLJIT, `karac build` and
`KARAC_AUTO_PAR=1 karac build`. `karac check` passes on every file.
The differential prints `40000 checks, 0 failures` on all six. The
frozen legacy `karac build` warns that the bench program reuses `nums`
after passing it to `can_partition`, since it predates bare parameters
borrowing; the program still builds and runs. Not filed.

## Benchmarks

The bench program uses the ★ arm on 200 numbers (the problem's limit)
from 1 to 100, with the total made even. Each of 2,000 rounds moves one
unit from one random number to another, keeping every number within 1
to 100, and decides the split again, so no compiler can hoist the work
out of the loop; it counts the arrays that split and folds the answers
into a checksum. Every array in the run splits. Every implementation
prints `2000 rounds on 200 numbers: 2000 can be split, checksum
503223156`; a 5-round cut of the Kāra program under `karac __mir-run`
prints the same as the C program cut the same way. Spot timings on a
shared 4-core container, three runs each (`bench.sh` timings need a
quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.94 to 1.09 s |
| Go | 1.78 to 2.07 s |
| Rust (`rustc -O`) | 2.22 to 2.35 s |
| Rust (`rustc -O -C overflow-checks=on`) | 2.40 to 2.50 s |
| Kāra (legacy `karac build`) | 2.46 to 2.51 s |
| Python (a 100-round cut, 4.0 s, times 20) | about 80 s |

The inner loop reads `reach[s - x]` and writes `reach[s]`; C does no
bounds checks there and the others do, which is likely most of the gap
to C; that is inferred, not profiled. The Kāra program also prints the
same line under `karac __mir-llvm-run` in 6.9 s, compile included;
that JITs the MIR's IR without optimization passes, so it is not a
benchmark. The `karac build` time is the frozen legacy backend.

## Compiler findings

No new findings.
