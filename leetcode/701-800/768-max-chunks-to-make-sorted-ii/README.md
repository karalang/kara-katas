# 768. Max Chunks To Make Sorted II

Split `arr` into consecutive chunks, sort each chunk on its own, and put
them back in order. Return the most chunks a split can have and still
leave the whole array sorted. Values may repeat.

```
[5, 4, 3, 2, 1]  ->  1
[2, 1, 3, 4, 4]  ->  4
```

**Constraints:** `arr` has from 1 to 2000 values, each from 0 to 10^8.

## Approaches

A chunk may end after a place exactly when nothing before the cut is
greater than anything after it. The arms find those cuts in four ways.

| file | mechanism |
|---|---|
| `max_chunks_to_sorted.kara` ★ | a stack of each chunk's largest value; a smaller value merges every chunk whose largest is greater than it into one; the stack's height is the answer; O(n) |
| `max_chunks_to_sorted_bounds.kara` | the smallest value of every suffix worked out first, then one pass keeping the largest so far, cutting wherever it is at most the next suffix's smallest |
| `max_chunks_to_sorted_counted.kara` | a sorted copy, and a `Map` of how many more of each value the array has had than the copy; a cut wherever no count is off zero |
| `max_chunks_to_sorted_ranked.kara` | the places sorted by value, ties by place, so that the array becomes a permutation of its ranks; a cut wherever the ranks so far reach no further than the place, as in LeetCode 769 |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 9 lines: the two LeetCode examples; a single
value; an array already sorted, and one of equal values; two arrays
whose repeats cross a cut; values up to 10^8; then 300 random arrays of
up to 60 values that mostly rise, with their chunks' total and a
checksum. `max_chunks_to_sorted.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
which tries every way of cutting the array and keeps the most pieces
that, each sorted on its own, make the sorted array. The 1,800 random
arrays mostly rise, by a random step with noise of a random size; the
first 1,500, of up to 10 values, are checked against the definition, and
the last 300, of up to 2,000, against the other properties.

| | property |
|---|---|
| P1 | the answer is the definition's (the 1,500 short arrays) |
| P2 | a rising change of every value, 3x + 7, changes nothing |
| P3 | one more value at the end, at least every other value, adds exactly one chunk |
| P4 | the array reversed and negated has the same answer |

It prints `1800 arrays (90469 chunks), 4 arms, 27600 checks, 0 failures`
under `karac __mir-run` and `karac __mir-llvm-run`, and the same under
`karac __mir-llvm-asan` with no error; the total is the ★ arm's.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a merged chunk keeps the new value as its largest | P1 567, P4 826 |
| M2 | ★: chunks whose largest equals the new value merged too | P1 229, P4 439 |
| M3 | ★: at most one chunk merged | P1 554, P4 826 |
| M4 | bounds: a cut refused where the two sides meet at one value | P1 653, P3 598 |
| M5 | bounds: the next place counted on the left of the cut | P1 536, P3 728, P4 538 |
| M6 | bounds: each suffix's minimum taken as its first value | P1 554, P4 826 |
| M7 | counted: a cut allowed with two values uneven | P1 981 |
| M8 | counted: the copy never sorted | P1 981 |
| M9 | counted: every nonzero count counted again | P1 375, P3 621, P4 525 |
| M10 | ranked: equal values ranked last place first | P1 653, P3 598 |
| M11 | ranked: no running maximum of the ranks | P1 828 |
| M12 | ranked: places sorted largest value first | P1 1147, P3 1716 |

P1 kills all twelve, and P2 none: every arm only compares values, and 3x
+ 7 keeps every comparison. P4 sees the ★ arm's three edits, M5 and
M6, and M9; P3 sees the edits that go wrong when the last value equals
the largest before it, M4, M10 and M12, and M5 and M9 again. M7, M8 and
M11 are seen by P1 alone: M8 answers the array's length whatever it
holds, and M7 and M11 cut in places that one more largest value and a
reversal carry along. Two first choices were replaced. Allowing a cut
with one value uneven changes nothing, rightly: the excesses always sum
to zero, so one value cannot be off alone, and the edit kept allows two.
Ranking ties by negated place stopped the program at a negative index;
the edit kept now ranks ties last place first.

## Verification

Every arm prints the same output as `max_chunks_to_sorted.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The debug build that
runs `__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` and the
release build that runs `check` and `__mir-run` are both at kara
`4f079681eb`, whose last compiler change is `ecb1a0322e`. The runtime
archives were built after the last runtime change, `176f59738b`.

Since kara `3c8e763161` (B-2026-10-18-31) the sanitizer lane sees leaks
itself. The leak check also copied each arm's and the differential's
lane executable as it was linked and ran it with the preloaded shim from
kata 708, which refuses the lane's hand-made stack so that LeakSanitizer
sees `main`: all five print their output and report no leak.

The frozen legacy backends accept all four arms, the differential and,
through a copy, the bench. Each arm prints the same output under the
legacy interpreter, `karac run`, `karac build` and an auto-par build,
and the differential prints its line under the legacy interpreter and
`karac build`, each with a warning that a borrowed `arr` is used after a
move, since legacy predates borrowed parameters. Legacy refuses the
bench at `max_chunks_to_sorted(pool[round % 64])`, as a move out of an
index; its timing below is of a copy whose parameter is `ref Vec[i64]`.
Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. Sixty-four
random arrays of 2,000 values, the most LeetCode allows, are built once,
each rising by 50 a place with noise of a random size, so that chunks
form and merge; each of 40,000 rounds counts the next one's chunks.
Every implementation prints `40000 arrays of 2000 values:
15379375 chunks in all, checksum 129417505`, the Kāra program under
`karac __mir-run` included (in 152 s). C keeps the stack in one array
allocated for each call; the others grow a vector or list.

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and two of Python (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.55 to 0.66 s |
| Rust (`rustc -O`) | 0.51 to 0.64 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.52 to 0.58 s |
| Go | 0.63 to 0.70 s |
| Python | 7.7 to 7.8 s |
| Kāra (`karac build --mir`) | 0.54 to 0.67 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend, the one this kata measures now that legacy is
frozen. That edit is by hand, on top of the `scripts/new-bench.sh`
output. Under `karac __mir-llvm-run` the program prints the same line in
2.8 s, compile included; that JITs the MIR's IR without optimization
passes, so it is not a benchmark.

So at the medians of the interleaved runs the v2 build takes 0.61 s,
against C's 0.59, Rust's 0.57 (0.56 under overflow checks) and Go's
0.68. Under valgrind's cachegrind v2 runs 2.6 billion instructions, Rust
1.9 billion and C 1.3 billion; all three mispredict 7 to 9 percent of
their branches, on whether each value merges chunks, and that rather
than the instruction count sets the time, which is why C is no faster.
The legacy build of the copy ran 0.52 to 0.59 s, a median of 0.52 s in
the interleaved runs, so v2 takes 1.2 times as long as legacy, inside
M2's limit of twice legacy; new katas' benches are outside M2's frozen
set in any case. The comparison with C and Rust waits until after M4.

## Compiler findings

B-2026-10-19-7 (filed). The ★ arm first read `Some(top) if x < top => {
let largest = top; ... maxima.pop(); ... maxima.push(largest); }`, and
the counted arm `let before =
excess.get(value).unwrap_or(0); excess.insert(value, before + change);
if before == 0 { ... }`. Both bindings are references into the
collection, so each is read after the collection changes, and every MIR
surface refuses the program as a borrow conflict; but `karac check`
passes both. The arms now copy the value out, with `*top` and
`excess.get(value) ?? 0`, which is the code the spec intends, not a
workaround.
