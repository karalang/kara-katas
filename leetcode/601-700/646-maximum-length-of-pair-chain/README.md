# 646. Maximum Length of Pair Chain

Given `n` pairs `[left, right]` with `left < right`, a pair `[c, d]` can
follow `[a, b]` when `b < c`. Return the length of the longest chain of
pairs, each following the one before; the pairs may be taken in any
order, and not every pair need be used.

```
pairs = [[1,2],[2,3],[3,4]]  ->  2    [1,2] then [3,4]
pairs = [[1,2],[7,8],[4,5]]  ->  3    [1,2] then [4,5] then [7,8]
```

**Constraints:** `n` from 1 to 1,000; every value from -1,000 to 1,000.

## Approaches

Every arm is `fn find_longest_chain(pairs: Vec[Vec[i64]]) -> i64`. Each
sorts a clone of the pairs and leaves its argument as it was.

| file | mechanism |
|---|---|
| `pair_chain.kara` ★ | the pairs by right end; every pair kept that starts after the last one kept ended, since the pair that ends first can always begin a longest chain; O(n log n) |
| `pair_chain_dp.kara` | the pairs by left end; the longest chain ending at each pair is one more than the longest ending at an earlier pair that ends before it starts; O(n^2) |
| `pair_chain_tails.kara` | the pairs by left end, keeping the smallest right end of any chain of each length; a binary search finds the longest chain a pair can extend, as in the longest increasing subsequence; O(n log n) |
| `pair_chain_swap.kara` | the pairs by left end and one chain: a pair that starts after the chain ends extends it, and one that ends sooner than the chain's last pair replaces it; O(n log n) |
| `differential.kara` | the four arms against the definition, five properties |

Every arm prints the same 12 lines: the two LeetCode examples; seven
more (one pair; the same pair three times; a long pair that starts first
but blocks two short ones; a long pair that ends last; negative values
out of order; five pairs that only touch; and the extremes of the
values), each with its answer; the total and a checksum of the answers
to 300 random cases of 1 to 30 pairs; and two cases of the problem's
largest size, 1,000 pairs, long and short. `pair_chain.py` mirrors the ★
arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition:
every set of the pairs tried, a set being a chain when, taken by left
end, each pair ends before the next one starts. Each of 1,000 cases has
1 to 10 pairs, each starting from -15 to 14 and covering 1 to 8 more
values, so pairs often overlap, touch and repeat.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | the answer is at least 1 and at most the number of pairs |
| P3 | the pairs in reverse give the same answer |
| P4 | every pair `[a, b]` turned into `[-b, -a]` gives the same answer |
| P5 | a pair starting after every other one ends adds exactly one |

It prints `1000 cases (5685 pairs), 4 arms, 20000 checks, 0 failures`
under `karac __mir-run` and `karac __mir-llvm-run`, and runs clean under
`karac __mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac __mir-run`.
All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the pairs taken by left end | P1 117, P3 68, P4 158 |
| M2 | ★: a pair that only touches the last one kept | P1 270 |
| M3 | dp: the starts compared, not an end with a start | P1 766, P4 415 |
| M4 | dp: the pair just before never tried | P1 425, P3 24, P4 82, P5 428 |
| M5 | tails: an end equal to the start counted as below it | P1 270 |
| M6 | tails: the larger end kept | P1 488 |
| M7 | swap: never trading down | P1 117, P3 68, P4 158 |
| M8 | swap: the pairs taken latest start first | P1 856, P5 1000 |
| E1 | ★: the end started at 5, not 0 | 0 |
| E2 | dp: every pair tried as the one before, not only earlier ones | 0 |
| E3 | tails: the middle spelled `lo + (hi - lo) / 2` | 0 |
| E4 | swap: the pairs taken by right end | 0 |

P1 kills all eight. M1 and M7 fail in exactly the same cases because
they are the same algorithm: the ★ arm taken by left end and the swap
arm without its trade-down both keep the first pair by start that fits.
P3 and P4 see them because which of two pairs with the same left end
comes first, and which pair starts first at all, change when the pairs
are reversed or mirrored. M2 and M5 also agree, both letting a pair
follow one it only touches; only P1 sees them, since touching is the
same in reverse and in the mirror and the pair P5 appends starts two
values clear. M6 is seen only by P1 for the same reason: the answer it
gets wrong does not depend on the order or the direction of the pairs.
P5 sees M4, which never lets the appended pair follow the pair just
before it by left end, and M8, which takes the appended pair first and
so answers 1. P2 sees nothing: every arm counts the first pair it looks
at and at most one per pair. The four survivors cannot change an answer:
the ★ arm never reads `end` before it keeps a pair; a pair later by left
end ends after this one starts, so it can never come before it; the two
middles are equal whenever `lo` and `hi` are not negative; and taken by
right end, no pair ends sooner than the last one kept, so the swap arm
never trades down and is the ★ arm.

## Verification

Every arm prints the same output as `pair_chain.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints its line under all three. `karac check` passes all four arms, the
differential and the bench program. All at kara `8d40e1a762`, debug and
release builds, with runtime archives newer than the last `runtime/src`
change.

The frozen legacy backends refuse every arm and the differential at type
checking: the harness hands `seed`, already a `mut ref` parameter, on
with the `mut` marker design.md asks for, which legacy rejects. Legacy
is frozen, so these are noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It makes 20 inputs of 10,000 pairs
once, each pair starting from 0 to 29,999 and covering 1 to a longest
from 10 to 1,000 more values, the longest picked for each input; then
200 rounds each answer one input, picked by the round, adding up the
answers and putting each into a checksum. Every implementation prints
`20 inputs, 200 rounds: total 132460, checksum 880944844`, the Kāra
program under `karac __mir-run` included (in 16 s).

Each implementation copies the pairs, sorts the copy by right end and
walks it. Kāra and Rust clone a `Vec` of 10,000 two-element `Vec`s, so
each round allocates 10,001 vectors; Go copies the outer slice and
Python builds a sorted list, both sharing the inner lists; C copies a
flat array of pairs and sorts it with `qsort`. Spot timings on a shared
4-core container, three runs each (two for Python; `bench.sh` timings
need a quiet machine), each including making the inputs:

| | time |
|---|---|
| C (`clang -O3`) | 0.33 to 0.35 s |
| Rust (`rustc -O`) | 0.19 to 0.21 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.19 to 0.21 s |
| Go | 0.47 to 0.51 s |
| Python | 0.59 to 0.60 s |
| Kāra (`karac build --mir`) | 0.37 to 0.38 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend, since the legacy `karac build` refuses the bench
program: its parameters are still owned rather than borrowed, so handing
`all[(r * 7) % inputs]` to `find_longest_chain` moves an element out of
a `Vec`. That edit is by hand, on top of the `scripts/new-bench.sh`
output. A copy outside the kata whose parameter is `ref Vec[Vec[i64]]`
builds under legacy and takes 0.49 to 0.51 s. Under `karac
__mir-llvm-run` the program prints the same line in 1.9 s, compile
included; that JITs the MIR's IR without optimization passes, so it is
not a benchmark.

So the v2 build is ahead of legacy and Go and a little behind C, whose
`qsort` calls its comparison through a pointer. Rust takes about half
the time with the same clone and the same allocations. The comparison
with C and Rust waits until after M4.

## Compiler findings

None new. All four arms, the differential and the bench program pass
`karac check` and run the same on both v2 backends. The legacy refusals
above are not filed because legacy is frozen.
