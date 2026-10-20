# 813. Largest Sum of Averages

Given an integer array `nums` and an integer `k`, cut the array into at
most `k` non-empty groups of adjacent numbers, using every number. The
score of a cut is the sum of the groups' averages, which need not be an
integer. Return the largest score any cut achieves. Answers within 10^-6
of the true score are accepted.

```
nums = [9, 1, 2, 3, 9], k = 3              ->  20.0     [9], [1, 2, 3], [9]
nums = [1, 2, 3, 4, 5, 6, 7], k = 4        ->  20.5
```

**Constraints:** `1 <= nums.length <= 100`, `1 <= nums[i] <= 10^4` and
`1 <= k <= nums.length`.

## Approaches

Every arm reads group sums off the prefix sums, `prefix[i] - prefix[p]`
for the group `nums[p..i]`, and builds the best score of a prefix from
the best scores of shorter prefixes with one group fewer.

| file | mechanism |
|---|---|
| `largest_sum_of_averages.kara` ★ | one row `best[i]` for the first i numbers, starting at one group, their average. Each further group lets `best[i]` end in a last group `nums[p..i]` after `best[p]`; updating i from the right reads only entries still at one group fewer. O(k n^2) time, O(n) space |
| `largest_sum_of_averages_table.kara` | the full table `dp[g][i]` for exactly g groups over the first i numbers, and the best g up to k at the end. O(k n^2) time and space |
| `largest_sum_of_averages_memo.kara` | `best(start, groups)` for the suffix from `start` in at most `groups` groups: all of it as one group, or a first group and the best of the rest, each pair worked out once. O(k n^2) |
| `largest_sum_of_averages_iter.kara` | the rows as iterators: each next row a `map` over prefix lengths of a `fold` to the maximum over splits |
| `differential.kara` | the four arms against every way to cut the numbers, four properties |

With every number at least 1, cutting a group in two always raises the
score: the two averages add up to more than the average of the whole. So
the best cut always uses `min(k, n)` groups, and "at most k" and
"exactly k" give the same answer; the table arm still takes the best g
up to k, as the statement asks.

The answer is printed to five decimals, since the arms add the same
averages in different orders and need not agree in the last bits. Every
arm prints the same 13 lines: LeetCode's two examples; one number; three
numbers in one group and in three; four equal numbers in two groups; one
large number among 1s; the zigzag `[3, 10, 3, 10, 3]`, whose two best
cuts into two groups tie; LeetCode's largest, 100 numbers up to 10000,
in at most 1, 7, 50 and 100 groups; and 300 random rounds of 1 to 12
numbers, with a total. `largest_sum_of_averages.py` mirrors the ★ arm
and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement
itself: every set of cut places, `2^(n-1)` of them, those with at most
`k - 1` cuts scored by adding the groups' averages, the largest score
kept. Its 1,600 cases have 1 to 12 numbers and a `k` from 1 to n, and
come in four kinds of 400: numbers from 1 to 50; from 1 to 3, so that
many cuts tie; mostly 1 with a few up to 10000, so that the best cuts
set the large ones apart; and rising or falling runs. Scores are
compared to within a billionth of the larger, as the arms and the
definition add in different orders.

| | property |
|---|---|
| P1 | the statement's answer |
| P2 | no less with one more group allowed, and the plain sum of the numbers with a group for every number |
| P3 | the same answer for the numbers reversed |
| P4 | three times the answer for the numbers tripled |

It prints `1600 cases, 25600 checks over 4 arms: 0 failures` under
`karac __mir-run` and `karac __mir-llvm-run`, and the same under `karac
__mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the groups before the last never cover just one number | P1 654, P2 1440, P3 625, P4 654 |
| M2 | ★: one group fewer than k | P1 1146, P2 1440, P3 1146, P4 1146 |
| M3 | ★: the last group's length counted one too many | P1 1146, P2 1440, P3 1146, P4 1146 |
| M4 | table: the first g - 1 groups never as short as they can be | P1 654, P2 1440, P3 625, P4 654 |
| M5 | table: one group's average over one number too many | P1 1600, P2 1600, P3 1600, P4 1600 |
| M6 | table: the groups before read one prefix short | P1 1051, P2 1440, P3 1051, P4 1051 |
| M7 | memo: the last two groups taken as one | P1 1146, P2 1440, P3 1146, P4 1146 |
| M8 | memo: a first group never one number long | P1 967, P2 1440, P3 959, P4 967 |
| M9 | memo: answers kept by start alone | P1 387, P3 392, P4 387 |
| M10 | iter: the groups before the last never cover just one number | P1 654, P2 1440, P3 625, P4 654 |
| M11 | iter: the first row's averages over all n | P1 1146, P2 1440, P3 1146, P4 1146 |
| M12 | iter: one group more than k | P1 1180, P3 1180, P4 1180 |

P1 kills all twelve. Many counts repeat because the best cut always uses
`min(k, n)` groups: an edit that loses a group, or makes any group after
the first worse, is wrong on exactly the 1,146 cases with `k >= 2` (M2,
M3, M7, M11), and P2 fails on the 1,440 cases with two numbers or more,
where a group for every number is no longer the plain sum. M12, one
group too many, is wrong on the 1,180 cases with `k < n`, and P2 cannot
see it, since the answer still rises with k and still reaches the sum.
M9 keeps a single answer per suffix whatever the groups left; the first
answer worked out for each suffix comes down the path that cuts one
number at a time, so with a group for every number it is still the sum,
and P2 cannot see that one either.

An edit that starts the iterator arm's `fold` at 0 in place of the row
before leaves every answer right and is not counted: with every number
at least 1 the best split into more groups always beats the row before.

## Verification

Every arm prints the same output as `largest_sum_of_averages.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The debug build that
runs `__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` is at kara
`d0ad6409f5`, whose last compiler change is `c120cafada`; the release
build that runs `check` and `__mir-run` is at `f6f2efb14`, one parser
change behind it. The runtime archives were built after the last runtime
change, `45d6c491fc`.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all five print their output and report no leak.

The frozen legacy interpreter (`karac run --interp`), the legacy JIT
(`karac run`), `karac build` and an auto-par build print the same output
for all four arms. Legacy refuses the differential, as it types the item
of `nums.iter()` as an `i64` rather than a reference and so refuses its
`*`, and the bench program, reading `largest_sum_of_averages(arrays[a],
..)` as moving a `Vec` out of an index (`E_INDEX_MOVE_NON_COPY`). Legacy
is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. 64 arrays of 100
numbers from 1 to 10000 are made once. Each of 6,000 rounds writes a new
number into one place of the next array and finds its largest sum of
averages in at most k groups, k going round from 1 to 100, so a round
does up to 99 passes of about 5,000 divisions. Every implementation
prints `6000 rounds of 100 numbers: total 1753753579.13717, checksum
836784651`, the Kāra program under `karac __mir-run` included, in 833 s.

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and two of Python (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 3.03 to 3.26 s |
| Rust (`rustc -O`) | 3.01 to 3.57 s |
| Rust (`rustc -O -C overflow-checks=on`) | 3.39 to 3.90 s |
| Go | 3.16 to 3.53 s |
| Python | 98.71 to 99.10 s |
| Kāra (`karac build --mir`) | 3.24 to 3.51 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend; that edit is by hand, on top of the
`scripts/new-bench.sh` output. Under `karac __mir-llvm-run` the program
prints the same line in 10.7 s, compile included; that JITs the MIR's IR
without optimization passes, so it is not a benchmark.

At the medians of the interleaved runs the v2 build takes 3.28 s,
against C's 3.21, Rust's 3.25 (3.79 under overflow checks) and Go's
3.29: all four are level, as every one waits on the same floating-point
divisions, one per candidate, and the divider sets the pace. Under
valgrind's cachegrind v2 runs 30.0 billion instructions, Rust 25.5
billion and C 21.1 billion; v2 runs 8.9 billion branches against C's 3.0
billion, most likely its overflow checks (not traced), and they run
alongside the divisions at little cost in time. Built for `x86-64-v3`,
the target `karac build` uses, C (`clang -O3 -march=x86-64-v3`) takes
2.98 to 3.19 s and Rust with overflow checks (`-C target-cpu=x86-64-v3`)
3.09 to 3.25 s, against v2's 3.03 to 3.24 s in the same five interleaved
runs. Legacy refuses the bench program (see Verification), so there is
no legacy timing to set v2 against. The comparison with C and Rust waits
until after M4.

## Compiler findings

Nothing new in v2: every arm, the differential and the bench passed
`karac check` and every v2 lane as first written.
