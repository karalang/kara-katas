# 760. Find Anagram Mappings

`nums2` is an anagram of `nums1`: the same values, duplicates included,
in another order. Return a mapping `mapping`, where `mapping[i] = j`
means that `nums1[i]` appears in `nums2` at index `j`, using each index
of `nums2` once. LeetCode accepts any such mapping; every arm here
returns the one that maps the k-th occurrence of a value in `nums1` to
its k-th occurrence in `nums2`, so that the arms can be compared
exactly.

```
[12, 28, 46, 32, 50]  [50, 12, 32, 46, 28]  ->  [1, 4, 3, 2, 0]
[84, 46]              [84, 46]              ->  [0, 1]
```

**Constraints:** 1 <= `nums1.length` == `nums2.length` <= 100; 0 <=
`nums1[i]`, `nums2[i]` <= 10^5.

## Approaches

| file | mechanism |
|---|---|
| `anagram_mappings.kara` ★ | a `Map` from each value to its positions in `nums2`, in order, and a second `Map` counting how many of them are used; each value of `nums1` takes its next position; O(n) |
| `anagram_mappings_sorted.kara` | sort the `(value, index)` pairs of both lists; the k-th pair of one then matches the k-th of the other, ties broken by index; O(n log n) |
| `anagram_mappings_scan.kara` | for each value of `nums1`, scan `nums2` from the start for the first equal value not yet taken; O(n^2) |
| `anagram_mappings_queues.kara` | a `Map` from each value to a `VecDeque` of its positions; `nums1.iter().map(...)` pops each value's front position and `collect` gathers them |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 8 lines: the two LeetCode examples; one value;
three equal values; two values alternating; 0 and 10^5 with a repeat; a
reversed list; then 500 random pairs of up to 100 values, half of them
from at most 10 distinct values, with the number of values mapped to
their own index and a checksum. `anagram_mappings.py` mirrors the ★ arm
and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
which counts the earlier occurrences k of `nums1[i]` and finds the k-th
occurrence in `nums2` by scanning. 3,000 random pairs of up to 30 values
are checked, mostly from a range of at most 12 values so that repeats
are common, and a quarter of the time from up to 10^5.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | it is a mapping: one index of `nums2` for each value, each index once, with equal values at both ends |
| P3 | swapping the lists gives the inverse mapping |
| P4 | renaming the values one to one, x to 7x + 3, changes nothing |

It prints `3000 pairs (27393 repeated values), 4 arms, 48000 checks,
0 failures` under `karac __mir-run` and `karac __mir-llvm-run`, and the
same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed. Three more edits, E1 to
E3, change nothing that can be seen, and the differential rightly
reports no failure for them.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the count of used positions never advanced | P1 2159, P2 2159, P3 2159 |
| M2 | ★: each value's positions kept newest first | P1 2159 |
| M3 | ★: each value's first position listed twice | P1 2159, P2 2159, P3 2159 |
| M4 | sorting: nums2's positions left unsorted | P1 2278, P2 2278, P3 2314 |
| M5 | sorting: the pairs read the wrong way round | P1 2124, P2 2124, P3 2124 |
| M6 | sorting: nums1's positions sorted largest first | P1 2896, P2 2334, P3 2334 |
| M7 | scanning: a position never marked taken | P1 2159, P2 2159, P3 2159 |
| M8 | scanning: the scan stopped at a taken match | P1 2857, P2 2857, P3 2857 |
| M9 | scanning: nums2 scanned from the end | P1 2159 |
| M10 | queues: positions queued at the front | P1 2159 |
| M11 | queues: values queued instead of positions | P1 2963, P2 2963, P3 2965, P4 3000 |
| M12 | queues: positions taken from the back | P1 2159 |
| E1 | sorting: both sorts given the natural comparison | 0 |
| E2 | scanning: the two tests of the scan swapped | 0 |
| E3 | queues: an empty queue answered with -1 | 0 |

P1 kills all twelve. M2, M9, M10 and M12 give the k-th occurrence of a
value the k-th from the end, which is still a valid mapping that
LeetCode would accept, so only P1 sees them: P2 checks only that the
mapping is one, and swapping the lists reverses the order back, so
P3 finds the inverse it expects. Every other edit hands some index out
twice or pairs unequal values, which P2 and P3 see. P4 sees only
M11, which hands out values instead of positions, so that renaming the
values changes the answer. E1 gives both sorts the comparison they
already use; E2 swaps the scan's two tests, which have no side effects
and cannot fail out of bounds, since an untaken equal value always
remains ahead; E3 answers an empty queue with -1, but no queue is ever
asked for more positions than it holds.

## Verification

Every arm prints the same output as `anagram_mappings.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The debug build that
runs `__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` and the
release build that runs `check` and `__mir-run` are both at kara
`a62eacd307`, whose last compiler change is `7d736aae75`. This paragraph
said the runtime archives were built after the last runtime change,
`b09cd37112`; in fact they predated a later one, `176f59738b`, which
changed only the order in which the runtime's merge sort makes its
merges, so it could not change any result here. Every arm and the
differential were checked again at kara `8a2af7d554`, whose last
compiler change is `60d9973e03`, with the archives rebuilt after
`176f59738b`: each prints the same under `karac __mir-llvm-run` and
`karac __mir-llvm-asan` with no error, and the bench program built by
`karac build --mir` prints the same line. The timings below are from the
earlier build.

Since kara `3c8e763161` (B-2026-10-18-31) the sanitizer lane sees leaks
itself. The leak check also copied each arm's and the differential's
lane executable as it was linked and ran it with the preloaded shim from
kata 708, which refuses the lane's hand-made stack so that LeakSanitizer
sees `main`: all five print their output and report no leak.

The frozen legacy backends accept only the sorting arm, which prints the
same output under the legacy interpreter, `karac run`, `karac build` and
an auto-par build. They refuse the ★ and queues arms, the differential
and the bench at `Map.get_mut`, which legacy lacks, and at a `*` over an
element of `iter()` (`used.get(*x)`), which legacy gives by value where
v2 gives references; the scanning arm at that `*` alone. The legacy
timings below are of a copy of the bench that writes
`positions[nums2[j]].push(j)` and `x` for `*x`, which prints the same
line. Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages, on
100,000 random pairs of 100 values, the most LeetCode allows, each value
below 50 so that every value repeats, adding up the values mapped to
their own index and a checksum. Every implementation prints
`100000 pairs of 100 values: 157740 mapped to their own index, checksum
842515663`, the Kāra program under `karac __mir-run` included (in 72 s).
C keeps its own open-addressing table from value to positions; Rust uses
two `HashMap`s and Go two maps, as the Kāra program does.

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and two of Python (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.52 to 0.57 s |
| Rust (`rustc -O`) | 1.06 to 1.27 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.13 to 1.23 s |
| Go | 1.48 to 1.68 s |
| Python | 6.6 to 7.2 s |
| Kāra (`karac build --mir`) | 1.73 to 2.02 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend, the one this kata measures now that legacy is
frozen. That edit is by hand, on top of the `scripts/new-bench.sh`
output. Under `karac __mir-llvm-run` the program prints the same line in
14.6 s, compile included; that JITs the MIR's IR without optimization
passes, so it is not a benchmark.

So at the medians of the interleaved runs the v2 build takes 1.80 s,
against C's 0.55, Rust's 1.14 (1.14 under overflow checks) and Go's
1.60. Under valgrind's cachegrind v2 runs 17.4 billion instructions,
Rust 10.9 billion and C 4.7 billion; C finds each value once in each
pass, in one table that keeps the count of used positions beside the
positions, where the Kāra program makes five map operations for each
value across two general-purpose maps (`contains_key`, then `get_mut` or
`insert`; then `get`, `get` and `insert`) and Rust four; that the
lookups account for the gap is inferred, not profiled. The legacy build
of the copy ran 1.58 to 2.04 s, a median of 1.74 s in the interleaved
runs, so v2 is level with legacy, inside M2's limit of twice legacy; new
katas' benches are outside M2's frozen set in any case. The comparison
with C and Rust waits until after M4.

## Compiler findings

None new.
