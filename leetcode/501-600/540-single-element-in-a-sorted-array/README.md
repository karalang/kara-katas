# 540. Single Element in a Sorted Array

You are given a sorted array consisting of only integers where every
element appears exactly twice, except for one element which appears
exactly once. Return the single element that appears only once. Your
solution must run in `O(log n)` time and `O(1)` space.

```
nums = [1,1,2,3,3,4,4,8,8]  ->  2
nums = [3,3,7,7,10,11,11]   ->  10
```

**Constraints:** `1 <= nums.length <= 10^5`; `0 <= nums[i] <= 10^5`.

## Approaches

Every arm is `fn single_non_duplicate(nums: Vec[i64]) -> i64`. Before
the single element each pair starts at an even index, and from it on at
an odd one, which is what the binary searches test.

| file | mechanism | time |
|---|---|---|
| `single_non_duplicate.kara` ★ | binary search over the even indices: a whole pair at `mid` sends the search right, a broken one left | log n |
| `single_non_duplicate_partner.kara` | binary search comparing `mid` with its partner `mid ^ 1`, the next index for an even `mid` and the one before for an odd one | log n |
| `single_non_duplicate_halves.kara` | binary search that finds which neighbour pairs with `mid` and goes to the side with an odd number of elements left | log n |
| `single_non_duplicate_xor.kara` | every element XORed, the pairs cancelling; O(n), so outside the problem's bound, but the simplest correct answer | n |
| `differential.kara` | the four arms against the definition, five properties | |

Every arm prints the same 12 lines: both examples, one element, the
single element first, last and in the middle, both ends of the range;
then for 300 random arrays of 0 to 30 pairs and a single element, with
values up to 99, a checksum over the answers; and last four arrays of
99,999 elements (the longest odd length the problem allows), values up
to 100,000, with the single element at the start, a quarter of the
way, the middle and the end. `single_non_duplicate.py` mirrors the ★
arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition:
the value written once, found by counting each one. Each arm is held to
the properties below on 1,000 random arrays of 0 to 40 pairs and one
single element at a random place, the values rising by 1 to 3 at a
time, or every other time by 1 to 2,000.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | every value moved up by the same amount moves the answer by it |
| P3 | the array mirrored, each value `v` as `200000 - v` and in reverse, gives 200,000 less the answer |
| P4 | one more pair below the smallest value and one above the largest leave the answer as it was |
| P5 | the answer is in the array, first written at an even place |

It prints `1000 cases, 4 arms, 20000 checks, 0 failures` under `karac
__mir-run`.

## Mutation testing

Twelve edits to `differential.kara`, two to each arm that change its
answers, and four that do not, each run under `karac __mir-run`. All
eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a whole pair at `mid` sends the search left too | P1 914, P3 977, P4 1000 |
| M2 | ★: the search stopped with three elements left | P1 417, P3 645, P4 449 |
| M3 | partner: every `mid` compared with the next element | P1 977, P3 598, P4 955, P5 416 |
| M4 | partner: the test turned round | P1 977, P3 38, P4 1000, P5 519 |
| M5 | xor: the elements added, not XORed | P1 977, P2 975, P3 977, P4 1000, P5 977 |
| M6 | xor: the fold started at 1 | P1 1000, P2 480, P3 1000, P5 931 |
| M7 | halves: the right part started one place too soon | P1 378, P3 555, P4 435, P5 149 |
| M8 | halves: an unpaired `mid` answered with its left neighbour | P1 256, P3 256, P4 359 |
| E1 | ★: the middle taken as `low + (high - low) / 2` | 0 |
| E2 | partner: the middle taken as `(low + high) / 2` | 0 |
| E3 | xor: each step written `x ^ acc` | 0 |
| E4 | halves: the answer read at `high`, which `low` has met | 0 |

P2 misses every binary-search mutant: they go wrong on where the single
element sits, not on what the values are, so moving every value leaves
the wrong answer wrong by the same amount. The 23 cases that every
other mutant passes are the arrays of one element, which no search
enters. M6's answers are the right ones with the lowest bit flipped,
which P2 sees in about half the cases, by the parity of the shift and
the answer, and P4 never sees, since the extra pairs do not change it.

Three first drafts were replaced. "★: mid itself ruled out when its
pair is broken" (`high = mid - 1`) turned out equivalent: when the
single element is at `mid`, everything left of it is whole pairs, so
the search walks right over them and stops with `low` at `mid` again.
Two others ran an index off the end of the array, which is a kill but
says less; M4 and M7 replaced them.

## Verification

Every arm prints the same output as `single_non_duplicate.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and runs clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints `20000 checks, 0 failures` on the first two and runs clean under
the third. `karac check` passes on every arm, the differential and the
bench program.

The frozen legacy backends: `karac run --interp` gives the right output
for all four arms. `karac run` and `karac build` fail on every arm with
an LLVM module that does not verify (the harness's `show` called with a
mismatched argument). The differential stops at type checking on a `*`
over a `Vec`'s `iter()` items, which legacy types by value. Legacy is
frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It builds 100 arrays of 0 to
49,999 pairs and a single element at a random place, values rising by
1 or 2, once (4,549,566 elements in all); then the answer for each array
is found 200,000 times. Every implementation prints `100 arrays,
4549566 elements, 200000 times each: total 346799000000, checksum
380136620`, the Kāra program under `karac __mir-run` included (in
143 s). Spot timings on a shared 4-core container, three runs each (two
for Python; `bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.67 to 0.69 s |
| Rust (`rustc -O`) | 0.63 to 0.66 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.70 to 0.74 s |
| Go | 0.69 to 0.72 s |
| Python | 36.4 to 36.9 s |
| Kāra (`karac build --mir`) | 0.99 to 1.00 s |

The legacy `karac build` refuses this program: it moves each array out
of the `Vec` of arrays where v2 borrows it (E_INDEX_MOVE_NON_COPY). So
`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend; that edit is by hand, on top of the
`scripts/new-bench.sh` output. The `--mir` row is timed at kara
`2649217dc8`. Under `karac __mir-llvm-run` the program prints the same
line in 5.2 s, compile included; that JITs the MIR's IR without
optimization passes, so it is not a benchmark.

The Kāra row is about 1.4 times C's. Its search loop, read off the
optimized IR, is the ★ arm as written: an overflow-checked `low + high`,
the division, two bounds checks and the two loads, with the moves of
`low` and `high` turned into selects. No cause beyond those checks was
found, so nothing is filed.

## Compiler findings

None filed. Every arm, the differential and the bench program run right
on the v2 backends, and `karac check` passes on all of them as written.
