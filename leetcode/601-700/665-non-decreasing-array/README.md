# 665. Non-decreasing Array

Given an array `nums`, return whether changing at most one element can
make it non-decreasing, each element at most the next.

```
nums = [4,2,3]  ->  true    (the 4 becomes 1)
nums = [4,2,1]  ->  false
```

**Constraints:** 1 to 10,000 numbers from -100,000 to 100,000.

## Approaches

Every arm is `fn check_possibility(nums: Vec[i64]) -> bool`. The
parameter borrows the array, so the ★ arm, which changes the elements as
it goes, works on a copy; the others only read.

| file | mechanism |
|---|---|
| `non_decreasing_array.kara` ★ | each drop fixed as it comes, the left one lowered when the one before it allows, the right one raised otherwise; refused at a second fix; O(n), on a copy |
| `non_decreasing_array_drops.kara` | the drops counted: none is fine, two are not, and one is fixable when either of its two elements fits between its neighbours; O(n) |
| `non_decreasing_array_remove.kara` | a changed element can take its neighbour's value, so the array must be in order without it; at the first drop, each of its two elements left out in turn; O(n) |
| `non_decreasing_array_longest.kara` | the longest non-decreasing subsequence, by patience sorting and binary search, must leave out at most one element; O(n log n) |
| `differential.kara` | the four arms against a definition that tries every element set to every value in the array, five properties |

Every arm prints the same 15 lines: the two LeetCode examples; one
number; eight short arrays with one drop to be fixed by lowering the
left element, by raising the right one, or either, or with drops no one
change fixes; four arrays of the problem's longest, 10,000 numbers:
rising, rising with one number changed, with two changed far apart, and
falling all the way; and how many of 1,000 random arrays of 1 to
8 numbers from 0 to 3 can be sorted, with a checksum.
`non_decreasing_array.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
which leaves the array as it is or sets any one element to any value
already in it, a neighbour's included, and looks for an order;
O(n^3). Each of 2,000 random arrays has 1 to 8 numbers from 0 up to 2 to
9, small enough that equal neighbours and drops are common: 1,000 of
them can be sorted.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | the array reversed and negated gives the same answer |
| P3 | so does every number doubled plus 7 |
| P4 | a sorted array with one element set at random can always be sorted |
| P5 | an array that can be sorted still can with its first or its last element gone |

It prints `2000 arrays (8997 numbers, 1000 can be sorted), 4 arms,
40000 checks, 0 failures` under `karac __mir-run` and `karac
__mir-llvm-run`, and runs clean under `karac __mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac __mir-run`.
All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the left one always lowered | P1 92 |
| M2 | ★: the right one always raised | P1 109, P2 232, P4 468 |
| M3 | drops: the right one never raised | P1 41, P2 71, P4 167 |
| M4 | drops: the left one lowered only above a strictly smaller one | P1 16, P2 34, P4 49 |
| M5 | remove: only the later of the two left out | P1 109, P2 232, P4 468 |
| M6 | remove: equal neighbours taken as a drop | P1 210, P4 755 |
| M7 | longest: a strictly rising subsequence | P1 252, P4 939 |
| M8 | longest: two elements allowed to change | P1 443 |
| E1 | ★: the left one never actually lowered | 0 |
| E2 | drops: a second drop recognised by `drop >= 1` | 0 |
| E3 | remove: the last drop used rather than the first | 0 |
| E4 | longest: a new tail added when the search ends at or past the end | 0 |

P1 kills all eight. P2, reversal with negation, sees the four that
favour one side of a drop, M2, M3, M4 and M5, since it swaps the sides:
lowering the left element becomes raising the right one. P4, a sorted
array with one element spoiled, sees every mutant that refuses some
fixable array, M2 to M7; it misses M1, whose failures need a shape a
spoiled sorted array rarely has, and M8, which accepts too many rather
than too few. P3 and P5 see none: no arm cares about the numbers' scale,
only their order, and none of these mutants accepts an array while
refusing one of its shortened copies. They stay as checks on the arms
themselves. The four survivors cannot change an answer: a lowered left
element is read again only at a second drop, which refuses first; `drop`
is never 0, as the first index it can take is 1; the last drop is the
first when there is only one, and with two, leaving out either element
of the last cannot fix the first; and the search never ends past the
end.

## Verification

Every arm prints the same output as `non_decreasing_array.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and runs clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints its line under all three. `karac check` passes all four arms, the
differential and the bench program. All with the compiler at kara
`8d40e1a762` for the debug build and `72739d54d6` for the release build
that runs `check` and `__mir-run`, with runtime archives newer than the
last `runtime/src` change.

The frozen legacy backends refuse every arm and the differential at type
checking: the harness's `rising` hands `seed`, already a `mut ref`
parameter, on with the `mut` marker design.md asks for, and the longest
arm and the differential read through `*` a number that `iter()` hands
them, which legacy types as a plain `i64`. Legacy rejects both. Legacy
is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It makes 16 arrays of the problem's
longest, 10,000 numbers, once: each rises by 0 to 20 at a step from
-100,000, then has 0, 1 or 2 numbers set at random. Then each of
40,000 rounds checks one, picked by the round, and puts the answer into
a checksum. Every implementation prints `16 arrays of
10000, 40000 rounds: 27500 can be sorted, checksum 163032454`, the Kāra
program under `karac __mir-run` included (in 81 s).

Each implementation is the same single pass on a fresh copy of the
array, stopping at a second fix: Kāra's and Rust's copy a `Vec`, Go's a
slice, Python's a list, and C's `malloc`s and `memcpy`s one. Spot
timings on a shared 4-core container, three runs each (two for Python;
`bench.sh` timings need a quiet machine), each including making the
arrays:

| | time |
|---|---|
| C (`clang -O3`) | 0.32 to 0.34 s |
| Rust (`rustc -O`) | 0.36 to 0.41 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.33 to 0.41 s |
| Go | 1.10 to 1.20 s |
| Python | 13 s |
| Kāra (`karac build --mir`) | 0.28 to 0.36 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend, since the legacy `karac build` refuses the bench
program at type checking: `main` hands `arrays[r % 16]` to
`check_possibility` without copying it, which design.md allows, since a
parameter borrows, and which legacy rejects as a move out of an index.
That edit is by hand, on top of the `scripts/new-bench.sh` output. A
copy outside the kata that clones the array builds under legacy and
takes 0.44 to 0.47 s, a second copy of each array included. Under `karac
__mir-llvm-run` the program prints the same line in 2.2 s, compile
included; that JITs the MIR's IR without optimization passes, so it is
not a benchmark.

So the v2 build is level with Rust and C, all of them spending the time
copying each array and walking it once. The legacy copy makes a second
copy of each array, so its time is not a like-for-like comparison. Go is
behind; it has not been profiled. The comparison with C and Rust waits
until after M4.

## Compiler findings

None new. All four arms, the differential and the bench program pass
`karac check` and run the same on both v2 backends. The legacy refusal
above is not filed because legacy is frozen.
