# 795. Number of Subarrays with Bounded Maximum

Given an array `nums` and two numbers `left` and `right`, count the
non-empty contiguous subarrays whose largest number is at least `left`
and at most `right`.

```
nums = [2, 1, 4, 3],    left = 2, right = 3  ->  3   ([2], [2, 1], [3])
nums = [2, 9, 2, 5, 6], left = 2, right = 8  ->  7
```

**Constraints:** 1 to 100,000 numbers from 0 to 10^9, and `0 <= left <=
right <= 10^9`.

## Approaches

| file | mechanism |
|---|---|
| `num_subarray_bounded_max.kara` ★ | one pass, keeping the last place of a number above `right` and the last place of a number in range; the subarrays ending at `i` that count start after the first and at or before the second, so add their difference; O(n) |
| `num_subarray_bounded_max_atmost.kara` | the subarrays with every number at most `right`, less those with every number below `left`, each a sum over runs of numbers within the bound, a run of `k` having `k (k + 1) / 2`; O(n) |
| `num_subarray_bounded_max_stack.kara` | each subarray given to its leftmost largest number, which has those starting after the last number before it at least as large and ending before the next one after it that is larger, both found with a stack whose numbers go down; add up the counts of the numbers in range; O(n) |
| `num_subarray_bounded_max_scan.kara` | from each start, extend the subarray keeping its maximum and count it while the maximum is in range, stopping at the first number above `right`; O(n²) at worst |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 8 lines: LeetCode's two examples; a single
number equal to both bounds; numbers all below `left`; a range taking in
every number; a range of one number, `10^9`, LeetCode's largest; a range
of one number met three times; and 300 random cases, 1 to 200 numbers
below 1 to 20 and bounds among them, with the subarrays in all and a
checksum. `num_subarray_bounded_max.py` mirrors the ★ arm and its output
is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition:
every subarray, its maximum found afresh. Its 1,600 cases have 1 to 30
numbers: a quarter below 1 to 8, a quarter up to a billion, a quarter
with a range taking in every number or none, and a quarter in runs of up
to five of one number. Outside the third kind each bound is a number of
the array moved by up to one.

| | property |
|---|---|
| P1 | the count is the definition's |
| P2 | the array backwards has the same count |
| P3 | cutting the range in two at any number gives counts that add up to the whole |
| P4 | the range from 0 to 10^9 counts every subarray, `n (n + 1) / 2` |

It prints `1600 cases (118646 subarrays), 4 arms, 25600 checks, 0
failures` under `karac __mir-run` and `karac __mir-llvm-run`, and the
same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a number equal to right taken as too big | P1 679, P3 433 |
| M2 | ★: a number equal to left not taken as in range | P1 963, P3 331, P4 993 |
| M3 | ★: every start after the last big number counted | P1 529, P2 469, P3 359 |
| M4 | at-most: the numbers equal to left taken off too | P1 963, P3 331, P4 993 |
| M5 | at-most: a run not ended by a larger number | P1 705 |
| M6 | at-most: each number counted once, not its run | P1 1233, P4 1548 |
| M7 | stack: every number's subarrays starting at the array's start | P1 1243, P2 1037, P4 1527 |
| M8 | stack: every number's subarrays going to the array's end | P1 983, P2 1036, P4 1293 |
| M9 | stack: a number equal to right left out | P1 679, P3 433 |
| M10 | scan: each scan stopping at a number equal to right | P1 679, P3 433 |
| M11 | scan: the last number checked against left, not the maximum | P1 529, P2 555, P3 359 |
| M12 | scan: every second end skipped | P1 1211, P4 1548 |

P1 kills all twelve. P3 kills seven: the five that mishandle a number
equal to a bound, of which cutting the range makes more, and the two
that count a subarray by something other than its maximum. P4 kills the
six that miscount when every number is in range, among them the two that
drop a number equal to `left`, as the range from 0 makes every 0 one. P2
kills the four that treat the two ends of a subarray unlike each other.
A run not ended by a larger number is seen by P1 alone.

## Verification

Every arm prints the same output as `num_subarray_bounded_max.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The debug build that
runs `__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` and the
release build that runs `check` and `__mir-run` are both at kara
`cfbbf3e8eb`, whose last compiler change is `b115567cf2`. The runtime
archives were built after the last runtime change, `176f59738b`.

Since kara `3c8e763161` (B-2026-10-18-31) the sanitizer lane sees leaks
itself. The leak check also copied each arm's and the differential's
lane executable as it was linked and ran it with the preloaded shim from
kata 708, which refuses the lane's hand-made stack so that LeakSanitizer
sees `main`: all five print their output and report no leak.

The frozen legacy backends accept all four arms and the differential
unchanged and print the same output under the legacy interpreter (`karac
run --interp`), the legacy JIT (`karac run`), `karac build` and an
auto-par build; for the at-most arm's two calls of `all_at_most` on one
`nums` they warn that `nums` is moved and used again, and run it right
regardless. Legacy refuses the bench program's
`num_subarray_bounded_max(arrays[r % 16], ...)` as a move out of an
index; a copy with `nums` written `ref Vec[i64]` builds and prints the
same line, and the bench timing below is of it. Legacy is frozen, so
this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. 16 arrays of
100,000 numbers up to a billion, LeetCode's longest and largest, are
made once. Each of 8,000 rounds counts the subarrays of one of them
whose maximum lies in a random range, with the ★ arm's one pass. Every
implementation prints `8000 rounds of 100000 numbers: 18980324012
subarrays, checksum 77897410`, the Kāra program under `karac __mir-run`
included (in 198 s).

The bench measures one tight loop over a long array, with two
comparisons and an unpredictable branch a number. Spot timings on a
shared 4-core container, eight runs of each compiled program, five of
them interleaved, and two of Python (`bench.sh` timings need a quiet
machine):

| | time |
|---|---|
| C (`clang -O3`) | 2.50 to 2.84 s |
| Rust (`rustc -O`) | 2.51 to 2.74 s |
| Rust (`rustc -O -C overflow-checks=on`) | 2.52 to 2.83 s |
| Go | 3.21 to 3.50 s |
| Python | 49.05 to 50.43 s |
| Kāra (`karac build --mir`) | 2.54 to 2.85 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, since the legacy `karac build` refuses it (see
Verification); that edit is by hand, on top of the
`scripts/new-bench.sh` output. Under `karac __mir-llvm-run` the program
prints the same line in 8.8 s, compile included; that JITs the MIR's IR
without optimization passes, so it is not a benchmark.

At the medians of the interleaved runs the v2 build takes 2.82 s,
against C's 2.63, Rust's 2.67 (2.65 under overflow checks) and Go's
3.31. Under valgrind's cachegrind v2 runs 12.4 billion instructions and
2.41 billion branches, against C's 11.0 billion and 1.20 billion and
Rust's 11.0 billion and 1.21 billion; all three mispredict the same 181
million branches, set by the numbers' random order. The legacy build of
the copy ran 2.62 to 2.83 s, a median of 2.75 s in the interleaved runs,
so v2 takes 1.03 times legacy. The comparison with C and Rust waits
until after M4.

## Compiler findings

Nothing new in v2.
