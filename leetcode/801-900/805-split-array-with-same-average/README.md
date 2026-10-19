# 805. Split Array With Same Average

Given an integer array `nums`, move each number into one of two arrays
`A` and `B` so that both are nonempty and `average(A) == average(B)`.
Return whether that can be done.

```
nums = [1, 2, 3, 4, 5, 6, 7, 8]  ->  true    ([1, 4, 5, 8] and [2, 3, 6, 7], both 4.5)
nums = [3, 1]                    ->  false
```

**Constraints:** `1 <= nums.length <= 30`, `0 <= nums[i] <= 10^4`.

## Approaches

| file | mechanism |
|---|---|
| `split_array.kara` ★ | splitting off `k` numbers with the whole array's average means their sum is `k · total / n`, and one part has at most `n / 2` numbers; for each size up to `n / 2` keep a `Set` of the sums some that many numbers make, adding the numbers one at a time, and look for a size whose wanted sum is whole and in its set |
| `split_array_meet.kara` | multiply every number by `n` and take away the total, so that a part has the average exactly when it sums to 0; find the sums of the nonempty parts of each half, and look for a part of the second half summing to 0 or to the opposite of a part of the first half that is not the whole half. O(2^(n/2) · n) |
| `split_array_bits.kara` | the ★ table with each size's sums kept as the bits of a row of `u64` words, adding a number by or-ing the row below shifted up by it |
| `split_array_pick.kara` | for each size whose wanted sum is whole, search the sorted numbers for that many that make it, stopping when the sum passes the wanted one and skipping a number equal to the one just tried at the same step. Exponential at worst |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 9 lines: LeetCode's two examples; a single
number, which cannot be split; `[0, 0]` and `[4, 4, 4, 4]`, which can;
two arrays of nine numbers, one of each answer; 30 numbers, LeetCode's
most, 10000 and 9999 with 28 zeros, which cannot; and 300 random arrays
of up to 16 numbers below a cap of 4 to 400, with how many can be split
and a checksum. `split_array.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition:
try every way to cut the numbers into two nonempty parts, and compare
averages without dividing, `sum(a) · n == total · |a|`. Its 1,600 cases
have 1 to 11 numbers and come in four kinds of 400: numbers below 4, so
that splits are common; below 100; up to 10,000; and mostly zeros with a
few numbers from 5,000 to 10,000.

| | property |
|---|---|
| P1 | the definition's answer |
| P2 | the numbers in the other order give the same answer |
| P3 | every number doubled and 3 added gives the same answer, both averages moving the same way |
| P4 | the first five numbers (or all, if fewer) given twice over can be split, into the two copies; and when the average is whole, the numbers with it added can be split, into it and the rest |

It prints `1600 cases (223 can be split), 4 arms, 25600 checks, 0
failures` under `karac __mir-run` (in 35 s) and `karac __mir-llvm-run`,
and the same under `karac __mir-llvm-asan` with no error. A first
version had up to 12 numbers and gave every array twice over to P4, and
ran for 3.5 minutes under `karac __mir-run`: the ★ arm's sets of sums
grow quickly with 24 numbers up to 10,000.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the largest size never looked at | P1 106, P4 1414 |
| M2 | ★: a sum kept for a size without the number added | P1 10, P3 56 |
| M3 | ★: the wanted sum rounded down when it is not whole | P1 353, P3 132 |
| M4 | meet: the whole first half kept | P1 1227 |
| M5 | meet: a kept sum looked for, not its opposite | P1 550, P2 45 |
| M6 | meet: the last number never in a part of the second half | P1 1227 |
| M7 | bits: the carry between words shifted one too few | P1 33, P3 41, P4 615 |
| M8 | bits: the lowest word reached never written | P1 223, P4 1600 |
| M9 | bits: no numbers taken to make 1 as well as 0 | P1 32, P3 130 |
| M10 | pick: a step stopped when its numbers exactly make the sum | P1 223, P4 1600 |
| M11 | pick: a number one above the one before skipped | P1 98, P3 98, P4 345 |
| M12 | pick: half of an even count never tried | P1 79, P4 1386 |

P1 kills all twelve. P2 sees only the meet edit that looks for a kept
sum rather than its opposite, which depends on which half a number falls
in. P3 sees the edits whose mistake changes with the size of the
numbers: a size's sum kept without the number (M2), the wanted sum
rounded down (M3), the carry between words (M7), the bit for 1 (M9) and
the skipped number one above the last (M11). P4 sees the edits that lose
a split P4 knows is there: the largest size never looked at (M1, M12),
the lowest word never written (M8), an exact sum stopped (M10), and M7
and M11 again. Two are seen by P1 alone, both in the meet arm and both
answering yes to every array of two or more numbers: keeping the whole
first half (M4) lets the whole array count as a part, and leaving the
last number out of the second half's parts (M6) makes the part of that
number alone an empty part summing to 0. Every property but P1 holds for
an arm that always answers yes.

## Verification

Every arm prints the same output as `split_array.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The debug build that
runs `__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` and the
release build that runs `check` and `__mir-run` are both at kara
`60266bcc51`, which is its last compiler change. The runtime archives
were built after the last runtime change, `216d20e28a`.

Since kara `3c8e763161` (B-2026-10-18-31) the sanitizer lane sees leaks
itself. The leak check also copied each arm's and the differential's
lane executable as it was linked and ran it with the preloaded shim from
kata 708, which refuses the lane's hand-made stack so that LeakSanitizer
sees `main`: all five print their output and report no leak.

The frozen legacy compiler prints the same output for all four arms and
the differential, unchanged, under its interpreter (`karac run
--interp`), its JIT (`karac run`), `karac build` and an auto-par build,
with a warning in the pick arm and the differential that `sorted` is
used after a move. Legacy refuses the bench program at
`split_array_same_average(arrays[r % 16])`, a move out of an index,
legacy taking a bare parameter as owned rather than borrowed; a copy
with a `ref` parameter and the array bound by `ref` first builds and
prints the same line, and the bench timing below is of it. Legacy is
frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. 16 arrays of 30
numbers, LeetCode's longest, are made once, the numbers below 300; in
every other array the last number is set so that the total is 1 more
than a multiple of 30, which makes the answer false. Each of 400 rounds
answers for the next array, building every size's set of sums whatever
the answer. Every implementation prints `400 rounds of 30 numbers: 175
can be split, checksum 312902833`, the Kāra program under `karac
__mir-run` included (in 313 s). Rust uses a `HashSet<i64>` and Go a
`map[int64]struct{}`; C has no set, so its program keeps each size's
sums in an open-addressing table of its own that doubles when half full.

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and two of Python (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 1.61 to 1.84 s |
| Rust (`rustc -O`) | 1.45 to 1.68 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.46 to 1.66 s |
| Go | 2.51 to 2.82 s |
| Python | 4.63 s both times |
| Kāra (`karac build --mir`) | 2.09 to 2.51 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, since the legacy `karac build` refuses it (see
Verification); that edit is by hand, on top of the
`scripts/new-bench.sh` output. Under `karac __mir-llvm-run` the program
prints the same line in 21.9 s, compile included; that JITs the MIR's IR
without optimization passes, so it is not a benchmark.

At the medians of the interleaved runs the v2 build takes 2.26 s,
against C's 1.79, Rust's 1.52 (1.53 under overflow checks) and Go's
2.65. Under valgrind's cachegrind v2 runs 23.0 billion instructions and
2.87 billion branches, against Rust's 15.0 billion and 750 million and
C's 6.47 billion and 1.36 billion. The legacy build of the copy ran 3.76
to 4.13 s, a median of 3.97 s in the interleaved runs, with 26.6 billion
instructions and 3.02 billion branches, so v2 takes 0.57 times legacy.
The C table here is a plain hand-written one, and mispredicts 150
million branches to Rust's 23 million and v2's 33 million, so its time
says more about that table than about C. The comparison with C and Rust
waits until after M4.

## Compiler findings

Nothing new in v2.
