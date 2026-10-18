# 718. Maximum Length of Repeated Subarray

Given two integer arrays `nums1` and `nums2`, return the maximum length
of a subarray that appears in both arrays.

```
nums1 = [1, 2, 3, 2, 1], nums2 = [3, 2, 1, 4, 7]  ->  3   ([3, 2, 1])
nums1 = [0, 0, 0, 0, 0], nums2 = [0, 0, 0, 0, 0]  ->  5
```

**Constraints:** 1 <= `nums1.length`, `nums2.length` <= 1000; 0 <=
`nums1[i]`, `nums2[i]` <= 100.

## Approaches

A common subarray lines up a run of nums1 with a run of nums2 at one
offset, so the question is the longest run of matches along any diagonal
of the grid of pairs.

| file | mechanism |
|---|---|
| `maximum_length_of_repeated_subarray.kara` ★ | one row of run lengths: the run ending at each pair of places is one more than the run ending one place back on both when the numbers match, else 0, and walking each row downwards reads the previous row before overwriting it; O(m * n) time, O(n) space |
| `maximum_length_of_repeated_subarray_table.kara` | the same recurrence kept whole, from the other end: the run starting at each pair; O(m * n) space |
| `maximum_length_of_repeated_subarray_diagonal.kara` | each of the m + n - 1 offsets in turn, walking its overlap and counting the current run of matches; O(1) space |
| `maximum_length_of_repeated_subarray_hash.kara` | a binary search on the length, since a common subarray of some length has common subarrays of every shorter one; a length is tested by putting the rolling hashes of nums1's windows in a map and rolling along nums2, comparing the numbers whenever a hash is found, so a collision never counts; O((m + n) log min(m, n)) expected |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 14 lines: the two LeetCode examples; one equal
and one different number; arrays with nothing in common; two halves
swapped; a run shifted by one place; alternating 1s and 2s against
alternating 2s and 1s; 1,000 random numbers, the problem's most, against
themselves and against their reverse; two random arrays of 1,000 numbers
up to 100, and of 1,000 0s and 1s; a run of 300 planted at different
places in two random arrays; and 300 random pairs of up to 30 numbers
with a checksum. `maximum_length_of_repeated_subarray.py` mirrors the ★
arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
which tries every start in nums1, every start in nums2 and every length
that fits both, comparing the numbers one by one. 3,000 random pairs are
checked, each array 1 to 12 numbers from 1 to 4 values, so long runs are
common.

| | property |
|---|---|
| P1 | the length is the definition's |
| P2 | the arrays swapped give the same length |
| P3 | both arrays reversed give the same length |
| P4 | nums2 with a copy of nums1 put in at a random place gives the whole length of nums1 |

It prints `3000 pairs (longest 12), 4 arms, 48000 checks, 0 failures`
under `karac __mir-run` and `karac __mir-llvm-run`, and the same under
`karac __mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed. Three more edits, E1 to
E3, change nothing that can be seen, and the differential rightly
reports no failure for them.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a mismatch leaving the old run in place | P1 791, P2 871 |
| M2 | ★: a run extended from the cell above, not the diagonal | P1 1629, P2 2140, P4 1897 |
| M3 | ★: nums2's first number never compared | P1 1014, P2 1657, P3 504, P4 403 |
| M4 | table: a run extended from the wrong neighbour | P1 1629, P2 2140, P4 1897 |
| M5 | table: nums2's last number never compared | P1 1022, P2 1652, P3 504, P4 358 |
| M6 | table: nums1's last number never compared | P1 988, P2 1652, P3 499, P4 3000 |
| M7 | diagonal: nums1 never slid past nums2's start | P1 587, P2 1192, P3 787 |
| M8 | diagonal: a mismatch not ending the run | P1 637 |
| M9 | diagonal: nums2's last number never compared | P1 1022, P2 1652, P3 504, P4 358 |
| M10 | hash: a window's numbers hashed without the 1 the removal takes off | P1 1454, P3 1210, P4 1665 |
| M11 | hash: a failed length ruling out the one below it too | P1 491 |
| M12 | hash: the rolling hash allowed to go negative | P1 27, P3 24, P4 830 |
| E1 | hash: the search started from the longer array's length | 0 |
| E2 | ★: a tie with the best run recorded again | 0 |
| E3 | diagonal: a shift of 0 started at -0 | 0 |

P1 kills all twelve, and is the only property that sees M8 and
M11. M8 lets a run carry on past a mismatch, which counts the matches
along a diagonal, and M11 rules out one length too many after a failed
test; both answer the same with the arrays swapped or reversed, and both
still find a full copy of nums1. P2 also misses M10 and M12, P3 misses
M1, M2 and M4, and P4 misses M1 and M7. M12 lets the hash go negative,
so two equal windows can hash differently depending on what came before
them: that is rare among random pairs, 27 failures in P1, and common in
P4, 830, where the copy of nums1 sits after different numbers than
nums1's own start. E1 starts the binary search from the longer array's
length, and a length that does not fit the shorter array fails at once,
so it is only slower; E2 records a tie with the best run again;
E3 starts a shift of 0 at -0.

## Verification

Every arm prints the same output as
`maximum_length_of_repeated_subarray.py` under `karac __mir-run` (the
v2 MIR interpreter) and `karac __mir-llvm-run`, and under `karac
__mir-llvm-asan` (AddressSanitizer) with no error; the differential
prints its line under all three. `karac check` passes all four arms, the
differential and the bench program. The debug build that runs
`__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` and the release
build that runs `check` and `__mir-run` are both at kara `a73d3c10ad`,
whose last compiler change is `3c8e763161`. The runtime archives were
built after that change.

Since kara `3c8e763161` (B-2026-10-18-31) the sanitizer lane sees leaks
itself. The leak check also copied each arm's and the differential's
lane executable as it was linked and ran it with the preloaded shim from
kata 708, which refuses the lane's hand-made stack so that LeakSanitizer
sees `main`: all five print their output and report no leak.

The frozen legacy backends refuse all four arms and the differential at
type checking: at `next_random(mut seed)` in the harness's
`random_nums`, whose argument is already a `mut ref`, where legacy wants
the marker dropped and design.md § Call-site `mut` markers now requires
it (kara B-2026-10-14-25), and in the hash arm also at `*a` over a
candidate list's `iter()`, since legacy gives those by value where
v2 gives references. Legacy refuses the bench program at
`find_length(arrays[k], ...)`, which it reads as moving a vector out of
the vector of arrays (E_INDEX_MOVE_NON_COPY); v2 borrows bare
parameters. Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. It makes
60 random arrays of 1,000 numbers from 0 to 9 once, and in each of
40 rounds pairs each of the first 20 with a different partner, summing
the lengths, 8 * 10^8 cells in all. Every implementation prints
`40 rounds of 20 pairs of 1000 numbers: sum 4558`, the Kāra program
under `karac __mir-run` included (in 3.6 minutes).

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and two of Python (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.44 to 0.53 s |
| Rust (`rustc -O`) | 0.38 to 0.42 s, one run at 0.54 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.50 to 0.61 s |
| Go | 1.26 to 1.52 s |
| Python | 36.6 to 39.3 s |
| Kāra (`karac build --mir`) | 1.26 to 1.53 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend; the legacy `karac build` refuses it (above). That
edit is by hand, on top of the `scripts/new-bench.sh` output. Under
`karac __mir-llvm-run` the program prints the same line in 5.4 s,
compile included; that JITs the MIR's IR without optimization passes, so
it is not a benchmark.

So the v2 build is about three times slower than C and three and a half
times slower than Rust at the medians of the interleaved runs (1.41 s
against 0.49 and 0.40), and level with Go. Under valgrind's cachegrind
it runs 16.3 billion instructions against C's 4.3 and Rust's 5.1, and
4.24 billion branches against 1.21 for both. All three mispredict the
same 88.6 million times, the match test on random numbers, so the extra
branches are all well predicted and the gap is about the size of the
instruction gap; where the extra instructions come from was not traced.
Overflow checks alone make Rust about half again as slow here (0.60 s
against 0.40). The comparison with C and Rust waits until after M4.

## Compiler findings

None new.
