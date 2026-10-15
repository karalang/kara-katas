# 658. Find K Closest Elements

Given a sorted array `arr`, a count `k` and a target `x`, return the `k`
numbers in `arr` closest to `x`, in ascending order. Of two numbers
equally close, the smaller is closer.

```
arr = [1,2,3,4,5],   k = 4, x = 3   ->  [1,2,3,4]
arr = [1,1,2,3,4,5], k = 4, x = -1  ->  [1,1,2,3]
```

**Constraints:** 1 <= `k` <= `arr.length` <= 10,000; `arr` sorted
ascending; `arr[i]` and `x` from -10,000 to 10,000.

## Approaches

Every arm is `fn find_closest_elements(arr: Vec[i64], k: i64, x: i64) ->
Vec[i64]`. In a sorted array the `k` closest numbers always sit side by
side, so three arms look for a window; the fourth sorts by distance and
does not rely on it.

| file | mechanism |
|---|---|
| `find_k_closest_elements.kara` ★ | a binary search over where the window starts: it moves right exactly when the number just past its end is closer than the number at its start; O(log(n - k) + k) |
| `find_k_closest_elements_shrink.kara` | the whole array, dropping the farther end, the larger on a tie, until `k` are left; O(n) |
| `find_k_closest_elements_sorted.kara` | `(distance, number)` pairs sorted, the first `k` kept and sorted back; O(n log n) |
| `find_k_closest_elements_expand.kara` | a binary search for `x`, then an empty window there grown `k` times towards the closer side; O(log n + k) |
| `differential.kara` | the four arms against the definition, five properties |

Every arm prints the same 11 lines: the two LeetCode examples; five more
(one number; all of them; `x` past the right end; a tie between the two
sides, the smaller winning; and repeated numbers), each with its answer;
a total and a checksum of 300 random arrays of 1 to 50 numbers from
-20 to 20; and three queries on the problem's largest array,
10,000 numbers from -10,000 to 10,000: 100 numbers around 17, all
10,000, and 3 from far off the left, each with a checksum.
`find_k_closest_elements.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition:
`k` times, take the closest number not yet taken, the smaller on a tie,
then sort what was taken. Each of 1,000 random sorted arrays has 1 to
30 numbers from -10 to 10, so that ties and repeats are common, with `k`
from 1 to the length and `x` from -15 to 15.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | `k` numbers, side by side in the array |
| P3 | and no number left out is closer than one kept |
| P4 | adding the same number to every element and to `x` adds it to the answer |
| P5 | the answer lies inside the answer for `k + 1` |

It prints `1000 arrays (15583 numbers), 4 arms, 20000 checks,
0 failures` under `karac __mir-run` and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac __mir-run`.
All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a tie moving the window right | P1 88, P3 88 |
| M2 | ★: the two ends' distances compared without their signs | P1 19, P3 19, P5 13 |
| M3 | shrink: a tie dropping the smaller end | P1 88, P3 88 |
| M4 | shrink: the smaller end's distance taken with its sign | P1 523, P3 523 |
| M5 | sorted: the distances taken with their signs | P1 523, P3 523 |
| M6 | sorted: the kept numbers left in order of distance | P1 566, P2 566, P3 566 |
| M7 | expand: a tie taking the right side | P1 88, P3 88 |
| M8 | expand: the last number taken only once the left side runs out | P1 147, P3 147 |
| E1 | ★: the search running while the ends differ | 0 |
| E2 | shrink: the window's size compared one lower | 0 |
| E3 | sorted: the distance taken from the other side | 0 |
| E4 | expand: the search landing after the numbers equal to x | 0 |

P1 and P3 kill all eight, and only M6, which leaves the kept numbers in
order of distance, is seen by P2. Every other mutant still returns a
window, just the wrong one: M1, M3 and M7 break a tie towards the larger
number, and M4, M5 and M8 misjudge which side is closer. P4 sees none,
since every arm, right or wrong, only ever subtracts `x`. P5 sees only
M2, the well-known slip of comparing the two ends' distances without
their signs: with a number repeated left of `x`, the window's start and
the number just past its end can be that same number, equally far, and
the search then moves left where it should move right. The four
survivors cannot change an answer: the search's ends never cross; `high
- low >= k` is the same test as `high - low + 1 > k`; a distance is the
same from either side; and starting the window after the numbers equal
to `x` only means taking them from the left, at distance 0, first.

## Verification

Every arm prints the same output as `find_k_closest_elements.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and runs clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints its line under all three. `karac check` passes all four arms, the
differential and the bench program. All with the compiler at kara
`8d40e1a762` for the debug build and `abbdbaf131` for the release build
that runs `check` and `__mir-run`, with runtime archives newer than the
last `runtime/src` change.

The frozen legacy backends print the same output for every arm and the
differential, under the interpreter, the JIT and `karac build`, with and
without `KARAC_AUTO_PAR=1`. Legacy's `karac build` warns that `arr` is
moved into `find_closest_elements` and used again, since legacy still
takes parameters owned; the output is not affected. Legacy is frozen, so
the warning is noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It makes one sorted array of
1,000,000 numbers from -1,000,000 to 1,000,000 once; then
1,000,000 queries each take `k` from 1 to 64 in turn and a random `x`,
and put the answer's two ends and its length into a checksum. Every
implementation prints `1000000 numbers, 1000000 queries: checksum
298219344`, the Kāra program under `karac __mir-run` included (in 28 s).

Each implementation is the same search, with each answer copied into a
new array, freed by hand in C. Spot timings on a shared 4-core
container, three runs each (two for Python; `bench.sh` timings need a
quiet machine), each including making and sorting the array:

| | time |
|---|---|
| C (`clang -O3`) | 0.48 to 0.56 s |
| Rust (`rustc -O`) | 0.37 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.37 to 0.43 s |
| Go | 0.71 to 0.78 s |
| Python | 10.6 to 10.9 s |
| Kāra (`karac build --mir`) | 0.42 to 0.45 s |
| Kāra, legacy (`karac build`) | 0.50 to 0.55 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend; the frozen legacy `karac build` builds it too, and
its row is above. Under `karac __mir-llvm-run` the program prints the
same line in 2.8 s, compile included; that JITs the MIR's IR without
optimization passes, so it is not a benchmark.

So the v2 build is a little faster than legacy and about a fifth slower
than Rust. C trails Rust here, likely in `qsort` sorting the array. The
comparison with C and Rust waits until after M4.

## Compiler findings

None new. All four arms, the differential and the bench program pass
`karac check` and run the same on both v2 backends. The legacy warning
above is not filed because legacy is frozen.
