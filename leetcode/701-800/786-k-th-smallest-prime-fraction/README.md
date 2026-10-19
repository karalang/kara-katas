# 786. K-th Smallest Prime Fraction

`arr` is a sorted array of 1 and prime numbers, all different. For every
pair `i < j` there is the fraction `arr[i] / arr[j]`. Return the `k`-th
smallest of these fractions as `[arr[i], arr[j]]`.

```
arr = [1, 2, 3, 5], k = 3  ->  [2, 5]
arr = [1, 7],       k = 1  ->  [1, 7]
```

**Constraints:** `arr` has 2 to 1,000 numbers, `arr[0]` is 1, the rest
are primes up to 30,000 in increasing order, and `k` is from 1 to `n
(n - 1) / 2`.

## Approaches

The numbers are 1 and different primes, so no two fractions are equal
and the `k`-th smallest is well defined. Every arm compares two
fractions exactly, `a / b < c / d` as `a d < c b`, except where the
binary search arm compares against its floating point guess.

| file | mechanism |
|---|---|
| `kth_smallest_prime_fraction.kara` ★ | the fractions over each denominator are a sorted list, so merge the lists with a smallest-first `PriorityQueue` holding the next fraction of each: take out the least `k` times, putting in the next of its list each time; O(n + k log n) |
| `kth_smallest_prime_fraction_binary.kara` | binary search on the value: for a guess `x` the fractions at most `x` are counted with two pointers, and the search ends when exactly `k` are at most `x`, the largest of them being the answer; O(n log(1/ε)) |
| `kth_smallest_prime_fraction_sorted.kara` | every pair made and sorted with `sort_by`; O(n² log n) |
| `kth_smallest_prime_fraction_select.kara` | every pair made, and quickselect finds the `k`-th without sorting the rest: Lomuto's partition around the middle pair of the range, going on in the side that holds position `k - 1`; O(n²) on average |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 13 lines: LeetCode's two examples; the first
and last of `[1, 2, 3, 5]`; one with a larger gap, and one with a prime
near 30,000; then 1 and the first 999 primes, LeetCode's largest array,
at six values of `k` from the first to the last; and 300 random arrays
of 2 to 60 numbers with a random `k`, with the sum of the answers' terms
and a checksum. `kth_smallest_prime_fraction.py` mirrors the ★ arm and
its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition:
the fraction with exactly `k - 1` fractions below it, found by counting,
for every pair, the pairs below it. Its 1,400 random arrays are 1,200 of
2 to 14 numbers, where that count is cheap, and 200 of 15 to 100. A
quarter take any primes below 30,000, a quarter primes from the first
40, a quarter a run of consecutive primes from a random place, and a
quarter the first primes; `k` is 1 in one array in five, the last in
another, and random in the rest.

| | property |
|---|---|
| P1 | the answer is the definition's (arrays up to 14 numbers) |
| P2 | the answer is two numbers of the array, the smaller first, with exactly `k - 1` fractions below them |
| P3 | the next `k` gives a larger fraction |
| P4 | the `k`-th fraction of the array without its largest number is the `(k + c)`-th of the whole array, where `c` counts the fractions over the largest number that are below it |

It prints `1400 arrays (terms sum to 17109448), 4 arms, 19484 checks, 0
failures` under `karac __mir-run` and `karac __mir-llvm-run`, and the
same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the heap giving the largest first | P1 954, P2 1151, P3 408, P4 1289 |
| M2 | ★: one fraction too many taken out | P1 1200, P2 1400, P3 36, P4 109 |
| M3 | ★: the list over arr[1] never started | P1 722, P2 842, P3 36, P4 109 |
| M4 | binary: the search stopping at the first value with k or more below | P1 738, P2 898, P3 898, P4 179 |
| M5 | binary: the first fraction kept, not the largest | P1 677, P2 832, P3 569 |
| M6 | binary: the largest denominator recorded | P1 623, P2 776, P3 820, P4 1289 |
| M7 | sorted: the fractions sorted by numerator | P1 956, P2 1151, P3 828, P4 1289 |
| M8 | sorted: k taken from 0 | P1 822, P2 982, P3 36, P4 103 |
| M9 | sorted: the fractions sorted by the product of their terms | P1 953, P2 1149, P3 690, P4 1289 |
| M10 | select: the pivot left where it was after the split | P1 651, P2 808, P3 371, P4 1047 |
| M11 | select: the first of the range left out of the split | P1 675, P2 837, P3 253, P4 1014 |
| M12 | select: the pivot read from the start of the range | P1 735, P2 900, P3 410, P4 1099 |

P1 and P2 each kill all twelve. M2 and M3 change the ★ arm, which also
gives the large arrays' answers that the terms sum is taken from, and
those runs count fewer checks: an answer that is not two numbers skips
P3 and P4. The first M4 counted one fraction too few for each numerator,
and the binary search arm then never met exactly `k` and ran without
end; it was replaced by this one, which stops at the first guess with
`k` or more fractions at most it. M5 keeps the first fraction counted
instead of the largest, which makes the answer the largest fraction with
numerator 1 that is at most the `k`-th; P4 misses it in all 1,400
arrays.

## Verification

Every arm prints the same output as `kth_smallest_prime_fraction.py`
under `karac __mir-run` (the v2 MIR interpreter) and `karac
__mir-llvm-run`, and under `karac __mir-llvm-asan` (AddressSanitizer)
with no error; the differential prints its line under all three. `karac
check` passes all four arms, the differential and the bench program. The
debug build that runs `__mir-llvm-run`, `__mir-llvm-asan` and `build
--mir` and the release build that runs `check` and `__mir-run` are both
at kara `cfbbf3e8eb`, whose last compiler change is `b115567cf2`. The
runtime archives were built after the last runtime change, `176f59738b`.

Since kara `3c8e763161` (B-2026-10-18-31) the sanitizer lane sees leaks
itself. The leak check also copied each arm's and the differential's
lane executable as it was linked and ran it with the preloaded shim from
kata 708, which refuses the lane's hand-made stack so that LeakSanitizer
sees `main`: all five print their output and report no leak.

The frozen legacy backends refuse all four arms, the differential and
the bench program at the type check. In the harness's `for p in
picked.iter()` they take the items for `i64` rather than references, so
`arr.push(*p)` is an error, and they refuse the bench's
`kth_smallest_prime_fraction(arrays[r % 64], k)` as a move out of an
index. Copies of the four arms with that `*` removed print the same
output under the legacy interpreter (`karac run --interp`), the legacy
JIT (`karac run`), `karac build` and an auto-par build, each build with
a warning that a borrowed `arr` is used after a move, since legacy
predates borrowed parameters; the legacy interpreter takes 52 minutes
over the ★ arm. A copy of the bench with its parameter written `ref
Vec[i64]` builds, and the bench timing below is of it. Legacy is frozen,
so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. 64 arrays of
1,000 numbers, LeetCode's most, are made once: 1 and 999 different
primes below 30,000 picked at random. Each of 64 rounds asks the next
array for a random `k`-th smallest fraction, so on average about a
quarter of a million fractions are taken out of the heap for each. Every
implementation prints `64 rounds of 1000-number arrays: terms sum to
1660242, checksum 707887771`, the Kāra program under `karac __mir-run`
included (in 547 s).

The bench measures a binary heap of four-field records compared by cross
multiplication. Rust's heap is `BinaryHeap<Reverse<Fraction>>`, C's a
hand-written binary heap, Go's `container/heap`, whose interface boxes
each record it pushes, and Python's `heapq` over a class with `__lt__`.
Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and two of Python (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 1.32 to 1.52 s |
| Rust (`rustc -O`) | 0.94 to 1.22 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.98 to 1.15 s |
| Go | 3.45 to 3.87 s |
| Python | 20.31 to 21.33 s |
| Kāra (`karac build --mir`) | 2.09 to 2.83 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, since the legacy `karac build` refuses it (see
Verification); that edit is by hand, on top of the
`scripts/new-bench.sh` output. Under `karac __mir-llvm-run` the program
prints the same line in 7.4 s, compile included; that JITs the MIR's IR
without optimization passes, so it is not a benchmark.

At the medians of the interleaved runs the v2 build takes 2.13 s,
against C's 1.42, Rust's 1.01 (1.07 under overflow checks) and Go's
3.61. Under valgrind's cachegrind v2 runs 14.5 billion instructions and
2.30 billion branches, against C's 5.53 billion and 0.64 billion and
Rust's 5.02 billion and 0.34 billion. Rust's `BinaryHeap` takes out the
least by moving the hole all the way down and then sifting the last
record up, which needs about half the comparisons of C's sift-down, so C
runs more branches than Rust and mispredicts 87 million of them to
Rust's 31 million. Where v2's extra instructions lie is not profiled.
The legacy build of the copy ran 2.32 to 2.54 s, a median of 2.40 s in
the interleaved runs, so v2 takes 0.89 times legacy. The comparison with
C and Rust waits until after M4.

## Compiler findings

Nothing new.
