# 845. Longest Mountain in Array

An array is a mountain if it has at least three elements and some `i`
with `0 < i < n - 1` has `arr[0] < ... < arr[i]` and `arr[i] > ... >
arr[n - 1]`: it climbs strictly and then falls strictly. Given an
integer array `arr`, return the length of its longest subarray that is a
mountain, or 0 if there is none.

```
arr = [2,1,4,7,3,2,5]  ->  5   ([1,4,7,3,2])
arr = [2,2,2]          ->  0
```

**Constraints:** `1 <= arr.length <= 10^4`, `0 <= arr[i] <= 10^4`. The
follow-up asks for one pass and O(1) space.

## Approaches

| file | mechanism |
|---|---|
| `longest_mountain.kara` ★ | one pass with two counters, the follow-up: walking the pairs of neighbours, `up` counts the climbing steps of the mountain in progress and `down` its falling steps; a step up after a fall, or any flat step, ends that mountain and starts afresh, and whenever both counts are positive the mountain so far has `up + down + 1` elements. O(n) time, O(1) space |
| `longest_mountain_runs.kara` | climbs and falls on each side: `rise[i]` counts the strictly rising steps that end at `i`, from the left, and `fall[i]` the strictly falling steps that start at `i`, from the right; an element with both is a peak of a mountain of `rise[i] + fall[i] + 1` elements. O(n) time and space |
| `longest_mountain_peaks.kara` | outward from each peak: from an element higher than both neighbours the mountain spreads left and right while the values keep falling away from it, and the scan then jumps to the foot of its right side, where the next peak can start at the earliest. O(n) time, O(1) space |
| `longest_mountain_signs.kara` | runs of the steps' signs: `arr.windows(2)` gives each step's sign, 1, -1 or 0; equal signs side by side are gathered into runs, and a run of ups followed at once by a run of downs is a mountain of `ups + downs + 1` elements. O(n) time and space |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 18 lines: LeetCode's two examples; eleven more
(one and two elements, a climb alone, a fall alone, the smallest
mountain, a zigzag, a plateau at the top, two mountains sharing a foot,
a mountain ended by a flat step, the values 0 and 10^4, and a row of
three mountains of 3, 5 and 6 elements); four arrays of LeetCode's most
elements, 10^4: one mountain over the whole array, a zigzag, equal
values and random values; and 500 random arrays of up to 40 values from
up to six distinct ones, with the sum of their answers and a checksum.
`longest_mountain.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: a subarray `arr[l..=r]` of at least three elements is a
mountain when some `i` strictly inside it has every step from `l` to `i`
going up and every step from `i` to `r` going down, and every subarray
and every such `i` is tried, O(n^4). Its 1,600 cases of up to 24
elements come in four kinds of 400: values from at most three distinct
ones, so many flat steps; any values up to 10^4; a walk of steps of -1,
0 or 1, so long slopes and plateaus; and mountains of random heights
side by side, sharing feet or not. In 1,162 of them there is a mountain.

| | property |
|---|---|
| P1 | the statement's answer |
| P2 | the array reversed gives the same answer |
| P3 | the same number added to every value gives the same answer |
| P4 | every value doubled gives the same answer |
| P5 | the array, two equal values higher than all of it, and the array again give the same answer: no mountain can cross the flat step between them |

It prints `1600 cases, 1162 with a mountain, 32000 checks over 4 arms: 0
failures` under `karac __mir-run` and `karac __mir-llvm-run`, and the
same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a flat step not ending the mountain | P1 269, P5 674 |
| M2 | ★: a climb after a fall not ending it | P1 1024, P5 1071 |
| M3 | ★: the peak not counted | P1 1162 |
| M4 | runs: a flat step continuing a rise | P1 510, P2 504, P5 772 |
| M5 | runs: a rise alone taken for a mountain | P1 207, P2 228, P5 378 |
| M6 | runs: the falls counted from the left | P1 658, P2 668 |
| M7 | peaks: flat steps joining the left slope | P1 304, P2 394 |
| M8 | peaks: a peak at the second element missed | P1 83, P2 132, P5 83 |
| M9 | peaks: the right slope one short | P1 195, P2 246, P5 195 |
| M10 | signs: a flat step joining the run before it | P1 497, P2 325, P5 767 |
| M11 | signs: valleys taken for mountains | P1 734, P5 656 |
| M12 | signs: the last run never ending a mountain | P1 268, P2 306, P5 268 |

P1 kills all twelve; M3 fails exactly the 1,162 cases with a mountain.
P2 sees the edits that treat the two sides of a mountain differently (M4
to M10, and M12, whose last run is at the other end once the array is
reversed); the ★ arm's three edits and M11 are symmetric. P5 sees the
edits that let a mountain run over or into a flat step (M1, M4, M5,
M10), those whose mistake depends on where the array ends (M8 at the
second element, M9 and M12 at the last), which the second copy no longer
meets, and those the wall's own slopes fool (M2, M11).

P3 and P4 kill nothing, and cannot here: every arm, and every edit, only
compares neighbouring values, and adding to or doubling every value
keeps each comparison as it was.

## Verification

Every arm prints the same output as `longest_mountain.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its lines under all three. `karac check` passes all
four arms, the differential and the bench program. The release and debug
builds are both at kara `0cf32f3e6f`, and the runtime archives are
current with them. Under `karac __mir-run` the arms take 0.2 to 0.4 s
and the differential 3.3 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all five print their output and report no leak.

The frozen legacy backends run all four arms right: `karac run
--interp`, `karac run`, `karac build` and a `KARAC_AUTO_PAR=1` build all
print the same output, and `karac run --interp` and `karac build` print
the differential's `0 failures`. Legacy refuses the bench program as
moving an array out of an index, which v2's borrowing parameters do not
do. Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. It draws 64
arrays once, each of LeetCode's most elements, 10^4, with values from 0
to 10^4: array `g` is random values when `g % 3` is 0, a walk of steps
of -1, 0 or 1 when it is 1, and mountains of random heights up to 40
side by side when it is 2. Each of 20,000 rounds asks the next array.
Every implementation prints `20000 rounds of 64 arrays: lengths sum to
694051, checksum 216723101`, the Kāra program under `karac __mir-run`
included, in 122 s.

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and three of Python (`bench.sh`
timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.88 to 1.10 s |
| Rust (`rustc -O`) | 0.97 to 1.17 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.06 to 1.22 s |
| Go | 1.07 to 1.16 s |
| Python | 25.9 to 26.8 s |
| Kāra (`karac build --mir`) | 0.94 to 1.06 s |

The legacy backend refuses the program (Verification), so there is no
legacy time. `bench.sh` builds the Kāra program with `karac build
--mir`, the v2 compiled backend; that edit is by hand, on top of the
`scripts/new-bench.sh` output.

At the medians of the interleaved runs v2 takes 1.00 s, against Rust's
1.06 (1.14 under overflow checks), C's 0.99 and Go's 1.10: 0.88 times
Rust's time under overflow checks, 1.01 times C's and 0.91 times Go's.
Under valgrind's cachegrind v2 runs the fewest instructions, 4.98
billion against C's 5.57 billion and Rust's 5.91 billion, but the most
branches, 1.27 billion against 401 million and 605 million, and it
mispredicts 85 million of them against C's 52 million and Rust's 68
million; why the three still take about the same time was not traced.
Built for `x86-64-v3`, the target `karac build` uses, C takes 0.61 to
0.63 s, well ahead, and Rust with overflow checks 1.05 to 1.09 s,
against v2's 0.94 to 0.98 s in the same five interleaved runs; most
likely clang turns the comparisons into branch-free code with the wider
target's instructions, which would remove C's mispredicts (not traced).
Python takes 26.6 s, about 27 times C's time. The comparison with C and
Rust waits until after M4.
