# 724. Find Pivot Index

Given an array of integers `nums`, return its pivot index: the index
where the sum of all the numbers strictly to its left equals the sum of
all the numbers strictly to its right. At the left edge the left sum is
0, and likewise at the right edge. Return the leftmost pivot index, or
-1 if there is none.

```
nums = [1, 7, 3, 6, 5, 6]  ->  3    (1 + 7 + 3 = 5 + 6)
nums = [1, 2, 3]           ->  -1
nums = [2, 1, -1]          ->  0    (0 = 1 + -1)
```

**Constraints:** 1 <= `nums.length` <= 10^4; -1000 <= `nums[i]` <= 1000.

## Approaches

The numbers right of an index add up to the total less the left sum less
the number itself, so once the total is known one running sum answers
for every index.

| file | mechanism |
|---|---|
| `find_pivot_index.kara` ★ | the total once, then a walk from the left keeping the sum of the numbers passed, stopping at the first index whose left sum equals the total less the left sum less the number; O(n) time, O(1) space |
| `find_pivot_index_prefix.kara` | a table of prefix sums, prefix[i] the sum of the first i numbers, so the left of index i is prefix[i] and the right prefix[n] - prefix[i + 1]; O(n) time and space |
| `find_pivot_index_sides.kara` | both sides of each index added up afresh; O(n^2) time, O(1) space |
| `find_pivot_index_fromright.kara` | the mirror of the ★ arm, walking from the end and keeping the sum right of the index; every pivot is seen on the way and the last one seen is the leftmost; O(n) |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 14 lines: the three LeetCode examples; a
single 0 and a single 5, each its own pivot; three 0s, every index of
which is a pivot; [1, -1], which has none; four more short arrays with
negative numbers or a 0; 10,000 random numbers, the problem's most,
which have none; 9,999 numbers built to balance at index
4,999; 10,000 0s, whose pivot is 0; and 300 random arrays of up to
12 numbers with how many have a pivot and a checksum.
`find_pivot_index.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
which adds up both sides of every index afresh, as the sides arm does,
but collects every pivot and takes the smallest. 3,000 random arrays are
checked, each of 1 to 14 numbers from -t to t with t from 0 to 4, so
several pivots and none are both common; 1,045 have none.

| | property |
|---|---|
| P1 | the index is the definition's |
| P2 | the numbers reversed give the mirror of the last pivot, n - 1 less it, or -1 with none |
| P3 | every number times -3 gives the same index |
| P4 | one number put at both ends, chosen so that neither end balances, gives the index one place on, or -1 with none |

It prints `3000 arrays (1045 with no pivot), 4 arms, 48000 checks,
0 failures` under `karac __mir-run` and `karac __mir-llvm-run`, and the
same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed. Three more edits, E1 to
E3, change nothing that can be seen, and the differential rightly
reports no failure for them.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the number at the index counted on the right | P1 1558, P2 1557, P4 177 |
| M2 | ★: the left sum only the last number | P1 879, P2 883, P4 1300 |
| M3 | ★: the total only the last number | P1 1226, P2 1246, P4 3000 |
| M4 | prefix: the number at the index counted on the right | P1 1558, P2 1557, P4 177 |
| M5 | prefix: each prefix only its last number | P1 1640, P2 1631, P4 3000 |
| M6 | prefix: index 0 never tried | P1 1058, P2 1055, P4 1058 |
| M7 | sides: the number at the index counted on the right | P1 1558, P2 1557, P4 177 |
| M8 | sides: the last index never tried | P1 353, P2 358, P4 353 |
| M9 | sides: a smaller left side taken as balanced | P1 1427, P2 1449, P3 1942, P4 2218 |
| M10 | fromright: the first pivot found kept, the largest | P1 956, P2 956 |
| M11 | fromright: the right sum subtracted | P1 704, P2 723, P4 1879 |
| M12 | fromright: index 0 never tried | P1 1058, P2 1055, P4 1058 |
| E1 | ★: the test as 2 * left + nums[i] == total | 0 |
| E2 | prefix: the test as prefix[i] + prefix[i + 1] == prefix[n] | 0 |
| E3 | fromright: the two sides compared the other way round | 0 |

P1 and P2 both kill all twelve, P4 all but M10, and P3 only
M9. M1, M4 and M7 are one mistake in three arms, the number at the index
counted on the right as well, and fail exactly the same arrays; M6 and
M12 both never try index 0, and fail the same arrays too. M10 returns
the rightmost pivot: P2 sees it because the reversed numbers' answer is
the mirror of the last pivot, but P4 cannot, since the padded array's
rightmost pivot is also one place on. P3 sees only M9, whose <= turns
into >= when every number changes sign; every other edit still tests an
equation between sums of the numbers, which multiplying them all by
-3 leaves true or false as it was. E1 writes the ★ test as 2 * left +
nums[i] == total, E2 the prefix test as prefix[i] + prefix[i + 1] ==
prefix[n], and E3 the fromright test with its two sides swapped.

## Verification

Every arm prints the same output as `find_pivot_index.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The debug build that
runs `__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` and the
release build that runs `check` and `__mir-run` are both at kara
`a4b0967495`, whose last compiler change is `d2fb23c673`. The runtime
archives were built after the last runtime change, `3c8e763161`.

Since kara `3c8e763161` (B-2026-10-18-31) the sanitizer lane sees leaks
itself. The leak check also copied each arm's and the differential's
lane executable as it was linked and ran it with the preloaded shim from
kata 708, which refuses the lane's hand-made stack so that LeakSanitizer
sees `main`: all five print their output and report no leak.

The frozen legacy backends refuse the ★ and fromright arms, the
differential and the bench program at type checking, at `*x` over the
numbers' `iter()`, since legacy gives those by value where v2 gives
references. They accept the prefix and sides arms, which print the same
output under the legacy `karac build`, sequential and with
`KARAC_AUTO_PAR=1`, and under its JIT; the legacy interpreter did not
finish the sides arm, quadratic over 10,000 numbers, within the check's
60 s limit. Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. It makes
50 arrays of 9,999 numbers from -1000 to 1000 once, each built to
balance at index 4,999 if nowhere earlier, and in each of 1,000 rounds
changes the sign of one number in every array before finding every
array's pivot index, summing the indexes with -1 for none. Every
implementation prints `1000 rounds of 50 arrays of 9999 numbers: sum
11230526`, the Kāra program under `karac __mir-run` included (in
10.2 minutes).

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and two of Python (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.34 to 0.41 s |
| Rust (`rustc -O`) | 0.43 to 0.51 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.67 to 0.83 s |
| Go | 0.48 to 0.59 s |
| Python | 32.3 to 33.6 s |
| Kāra (`karac build --mir`) | 0.65 to 0.73 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend; the legacy `karac build` refuses it (above). That
edit is by hand, on top of the `scripts/new-bench.sh` output. Under
`karac __mir-llvm-run` the program prints the same line in 6.2 s,
compile included; that JITs the MIR's IR without optimization passes, so
it is not a benchmark.

So the v2 build is about 1.8 times C and 1.4 times Rust at the medians
of the interleaved runs (0.67 s against 0.38 and 0.49), a fifth behind
Go (0.55) and level with Rust under overflow checks (0.70). Under
valgrind's cachegrind it runs 8.9 billion instructions against Rust's
6.3 and C's 4.0, and 3.4 billion branches against 1.1 and 0.7, with
almost none mispredicted in any of the three, so the extra branches are
well predicted, most likely checks that never fire. Kāra checks every
addition and subtraction for overflow, four for each number here, which
likely accounts for most of them, since Rust with the same checks is
level with it; that was not traced. The comparison with C and Rust waits
until after M4.

## Compiler findings

None new.
