# 698. Partition to K Equal Sum Subsets

Given an integer array `nums` and an integer `k`, return `true` if it is
possible to divide this array into `k` non-empty subsets whose sums are
all equal.

```
nums = [4, 3, 2, 3, 5, 2, 1], k = 4  ->  true   (5, 1+4, 2+3, 2+3)
nums = [1, 2, 3, 4], k = 3           ->  false
```

**Constraints:** 1 <= `k` <= `nums.length` <= 16; 1 <= `nums[i]` <=
10^4; each value appears 1 to 4 times.

## Approaches

Every arm is `fn can_partition_k_subsets(nums: Vec[i64], k: i64) ->
bool`. Each subset must sum to total / k, so every arm first refuses a
total that k does not divide.

| file | mechanism |
|---|---|
| `can_partition_k_subsets.kara` ★ | the values largest first, each tried in each of k buckets with room for it; buckets holding the same sum are alike, so a value goes into only the first of them; O(k^n) in the worst case |
| `can_partition_k_subsets_fill.kara` | one subset filled before the next: a new subset starts with the first unused value, the rest are taken in increasing place, and a value equal to one just taken back is skipped; nothing remembered; O(k 2^n) in the worst case |
| `can_partition_k_subsets_memo.kara` | the same search with the used values as a bitmask; their sum says how full the open subset is, so each set that fails is marked and never searched again; O(n 2^n) |
| `can_partition_k_subsets_dp.kara` | every set of values bottom up: `fill[mask]` is how much the open subset holds once those values are placed, or -1; each unused value that fits reaches one more set; O(n 2^n) time and O(2^n) space |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 6 lines: the two LeetCode examples; one
subset, sixteen 7s into sixteen, a total k does not divide, and a value
larger than its share; four problems whose total and values allow a
split, two of which have none; sixteen values near 10,000 in eight
pairs, with 9,997 among them (no partner, so no split) and with
9,998 instead; and 300 random problems, each k random splits of one
target mixed together, about half of them with an amount then moved from
one value to another, with a checksum. `can_partition_k_subsets.py`
mirrors the ★ arm and its output is byte-identical. The harness goes
past the last constraint in places, sixteen 7s and thirteen 9,999s among
them; no arm depends on it.

## Differential

`differential.kara` holds copies of the four arms and the definition.
The definition is written apart from all four arms: list every subset
whose sum is total / k, then look for k of them that do not overlap and
cover every value, trying for the lowest value not yet covered only the
subsets that hold it. 3,000 random problems are checked, k from 1 to
4: half are k random splits of one target, perhaps with one unit moved
between two values, and half are 1 to 10 random values from 1 to up to
12. 1,854 of them can be split, and in 2,222 k divides the total.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | the values in reverse order, the same answer |
| P3 | every value doubled, the same answer |
| P4 | when k divides the total: one more value equal to the share, and one more subset, the same answer |

It prints `3000 problems (1854 can be split), 4 arms, 44888 checks,
0 failures` under `karac __mir-run` and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed. Two more edits to the
bottom-up arm, E1 and E2, change nothing that can be seen, and the
differential rightly reports no failure for them.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a bucket skipped when one before it holds as much or more | P1 1096, P4 758 |
| M2 | ★: a value never taken back out of its bucket | P1 24 |
| M3 | ★: a value equal to the share refused | P1 671, P4 1183 |
| M4 | fill: after a failed value, every smaller value skipped too | P1 24 |
| M5 | fill: a value already used taken again | P1 42 |
| M6 | fill: a value that would fill the subset exactly refused | P1 827 |
| M7 | memo: room measured from the total used, not the open subset | P1 1096, P4 758 |
| M8 | memo: a value that would fill the subset exactly refused | P1 1854 |
| M9 | memo: done as soon as one subset is full | P1 245, P4 123 |
| M10 | dp: the open subset never closed | P1 1854 |
| M11 | dp: a value that would fill the subset exactly refused | P1 1854 |
| M12 | dp: sets with an empty open subset not extended | P1 1854 |
| E1 | dp: any way to place every value accepted | none (equivalent) |
| E2 | dp: a set reached again overwritten | none (equivalent) |

P1 kills all twelve. M2, M4 and M5 fail only 24 to 42 problems: a value
left in its bucket, smaller values skipped after a failure, or a used
value taken again all go wrong only once the search has to back out of a
choice. P4 sees the mutants that refuse a value as large as the share
(M3) or answer before every subset is full (M9), and those that go wrong
only with two or more subsets (M1, M7), on the problems with k =
1, where adding the share makes a second subset. P2 and P3 see none:
three arms sort the values or visit every set regardless of order, and
doubling every value changes no comparison, a mutant's included.
E1 accepts any way of placing every value, which is the same thing,
because the values placed are all of them and their sum is a multiple of
the share; E2 lets a set reached a second way overwrite the first, which
writes the same amount, since a set's sum does not depend on the order
it was reached in.

## Verification

Every arm prints the same output as `can_partition_k_subsets.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and runs clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints its line under all three. `karac check` passes all four arms, the
differential and the bench program. All with the compiler at kara
`ec489d962f` for both the debug build and the release build that runs
`check` and `__mir-run`, with runtime archives rebuilt after the last
`runtime/src` change.

The frozen legacy backends refuse all four arms, the differential and
the bench program at type checking, at `total += *x` over `nums.iter()`:
legacy gives the value, while on v2 the loop variable is a reference.
The harness's `random_problem` would meet a second refusal, at
`next_random(mut seed)` where `seed` is already a `mut ref`, the
v2 spelling of a marked forward (kara B-2026-10-14-25). Legacy is
frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the bottom-up arm, the same in all five
languages: its cost depends on how many sets are reachable, not on the
order a search happens to try, so every language does the same work. It
builds 100 problems of 16 values once, k cycling through 1, 2, 4, 8 and
16, each problem k random splits of one target, with an amount moved
between two values in every second problem; then it answers every
problem in each of 2 rounds, putting each answer into a checksum. Every
call allocates the 65,536-entry table, as the arm does. Every
implementation prints `2 rounds of 100 problems of 16 values:
152 answers yes, checksum 164755942`, the Kāra program under `karac
__mir-run` included (in 27 s).

For the legacy row a copy of the bench program writes `total += x` and
passes `problems[p].clone()`, which legacy wants in place of a borrow of
an element; the clone copies 16 values per call against the 65,536-entry
table the call fills, and the copy prints the same line.

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and two of Python (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.55 to 0.63 s |
| Rust (`rustc -O`) | 0.54 to 0.60 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.51 to 0.58 s |
| Go | 0.65 to 0.70 s |
| Python | 8.2 s |
| Kāra (`karac build --mir`) | 0.51 to 0.59 s |
| Kāra, legacy (`karac build`, the copy) | 0.52 to 0.54 s (five runs) |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend. That edit is by hand, on top of the
`scripts/new-bench.sh` output. Under `karac __mir-llvm-run` the program
prints the same line in 2.2 s, compile included; that JITs the MIR's IR
without optimization passes, so it is not a benchmark.

So the v2 build is level with legacy, C and both Rust builds here, and
ahead of Go. The comparison with C and Rust waits until after M4.

## Compiler findings

None. `karac check` passed all four arms, the harness, the differential
and the bench program as first written. The first version of the fill
arm, which let a new subset start anywhere instead of with the first
unused value, ran for more than ten minutes on the harness's sixteen
values near 10,000; that was the algorithm, not the compiler, and the
arm was corrected before anything was recorded.
