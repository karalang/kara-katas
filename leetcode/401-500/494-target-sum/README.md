# 494. Target Sum

You are given an integer array `nums` and an integer `target`.

You want to build an expression out of `nums` by adding one of the
symbols `'+'` and `'-'` before each integer in `nums` and then
concatenating all the integers. For example, if `nums = [2, 1]`, you
can add a `'+'` before `2` and a `'-'` before `1` and concatenate them
to build the expression `"+2-1"`.

Return the number of different expressions that you can build, which
evaluates to `target`.

```
nums = [1,1,1,1,1], target = 3  ->  5
nums = [1],         target = 1  ->  1
```

**Constraints:** `1 <= nums.length <= 20`; `0 <= nums[i] <= 1000`;
`0 <= sum(nums[i]) <= 1000`; `-1000 <= target <= 1000`.

## Approaches

Every arm is `fn find_target_sum_ways(nums: Vec[i64], target: i64) ->
i64`.

| file | mechanism |
|---|---|
| `target_sum.kara` ★ | counting ways by running sum: after each number, how many sign choices reach each sum from `-total` to `total`, in a `Vec` shifted by the total; each number moves every count up and down by itself into a fresh `Vec` |
| `target_sum_signs.kara` | every choice of signs, recursively: 2^n leaves |
| `target_sum_subset.kara` | as a subset count: the plus numbers must sum to `(total + target) / 2`, so count the subsets with that sum, one array walked from the top down |
| `target_sum_memo.kara` | the recursion, remembered: the count from each (position, running sum) kept in a `Map[(i64, i64), i64]` |
| `differential.kara` | the four arms on 1,500 random arrays, five properties |

Every arm prints the same 8 lines: the two LeetCode examples, zeros
(each doubles the count), a target out of reach, a target of the wrong
parity, a negative target, all minus, and for 300 random arrays (1 to
14 numbers from 0 to 20, a target from -30 to 30) how many targets
could be reached, the total number of ways and a checksum.
`target_sum.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and runs them on
1,500 random arrays of 1 to 11 numbers, from 0 to 3, 0 to 10 or 0 to
50 in turn, with a target within three of the reachable range and one
more number `x`. The reference runs through every choice of signs as
the bits of a number from 0 to 2^n - 1.

| | property |
|---|---|
| P1 | the count is the reference's |
| P2 | the target negated has as many ways (flip every sign) |
| P3 | the numbers reversed have as many ways |
| P4 | a 0 appended doubles the ways (`+0` and `-0` are different expressions) |
| P5 | `x` appended gives the ways to `target - x` plus the ways to `target + x` without it |

It prints `1500 cases, 4 arms, 30000 checks, 0 failures` under
`karac __mir-run`, in 17 s, and a count for each property when
anything fails.

## Mutation testing

Eight edits to `differential.kara`, two to each arm, each run under
`karac __mir-run`. All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a minus sign overwrites the count instead of adding to it | P1 341, P4 453, P5 307 |
| M2 | ★: every negative target is out of reach | P1 222, P2 443, P5 83 |
| M3 | signs: a sum at or above the target counts | P1 1338, P2 1351 |
| M4 | signs: the last number is never given a sign | P1 616, P3 444, P4 564, P5 594 |
| M5 | subset: a number is never a subset on its own | P1 434, P2 75, P4 39, P5 35 |
| M6 | subset: the parity check is left out | P1 391, P2 354, P5 27 |
| M7 | memo: a count is stored under the negated sum | P1 404, P2 404, P3 157, P4 83, P5 112 |
| M8 | memo: a plus sign adds the number twice | P1 578, P2 553, P5 380 |

P3 sees only M4 and M7. M4 ignores the last number, so reversing the
array changes which number is ignored. M7 hands a count to the wrong
sum at the same position, and which sums meet at a position depends on
the order of the numbers before it (inferred, not traced). The other
mutants treat every position alike.

## Verification

All four arms print the same output as `target_sum.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
`karac check` passes on every file, the bench program included. The
differential prints `30000 checks, 0 failures` on both. The four arms
and the differential also run clean under `karac __mir-llvm-asan`
(AddressSanitizer and LeakSanitizer): output identical, no error, no
leak.

The frozen legacy backends agree on all four arms: `karac run
--interp`, LLJIT, legacy `karac build` and a `KARAC_AUTO_PAR=1` build
print the same output. Legacy `karac build` warns on the signs and memo
arms, and on the differential, that `nums` is "moved here, used again
here", where the recursion lends it twice and legacy reads the first
as a move; the output is right all the same, and the legacy-built
differential prints `30000 checks, 0 failures`. Under `karac run
--interp` the differential printed nothing within the 900 s the
verification script allows it. The bench program does not build on
legacy (see Benchmarks). Legacy is frozen, so this is noted, not
filed.

## Benchmarks

The bench program uses the ★ arm. It builds 40,000 arrays of 20
numbers (the problem's most) from 0 to 50, so each sum stays within
the problem's limit of 1,000, each with a target from -100 to 100,
once, then solves each once. Every implementation prints `40000 arrays
of 20: 20056 reachable, checksum 476720652`, the Kāra program under
`karac __mir-run` included (in 169 s).

Every mirror fills a fresh zeroed array of counts for each number, as
the ★ arm does with `vec![0; width]`: Rust `vec![0; width]`, Go `make`,
Python `[0] * width`, C `calloc` and `free`. Spot timings on a shared
4-core container, three runs each (two for Python; `bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.86 to 0.99 s |
| Rust (`rustc -O`) | 0.76 to 0.86 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.75 to 0.82 s |
| Go | 2.20 to 2.24 s |
| Python | 32.3 s |
| Kāra (`karac build --mir`) | 0.95 to 1.08 s |

The legacy `karac build` refuses this program: "cannot move out of an
index expression", on `find_target_sum_ways(arrays[k], targets[k])`,
which v2 reads as a borrow. So `bench.sh` builds the Kāra program with
`karac build --mir`, the v2 compiled backend. That edit is by hand, on
top of the `scripts/new-bench.sh` output. The `--mir` row is timed at
kara `d9a7136c58`. Under `karac __mir-llvm-run` the program prints the
same line in 5.0 s, compile included; that JITs the MIR's IR without
optimization passes, so it is not a benchmark.

## Compiler findings

None. Every arm, the differential and the bench program ran first time
on the v2 backends.
