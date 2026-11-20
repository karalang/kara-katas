# 1262. Greatest Sum Divisible by Three

Given an integer array `nums`, return *the **maximum possible sum** of
elements of the array such that it is divisible by three*.

```
nums = [3,6,5,1,8]   ->  18   (pick 3, 6, 1 and 8)
nums = [4]           ->  0    (4 is not divisible by 3; pick nothing)
nums = [1,2,3,4,4]   ->  12   (pick 1, 3, 4 and 4)
```

**Constraints:** `1 <= nums.length <= 4 * 10^4`; `1 <= nums[i] <= 10^4`.

The arms are `fn max_sum_div_three(nums: Vec[i64]) -> i64`.

## Approaches

Only a sum's remainder modulo 3 decides what a later number can do with
it, so three best sums are enough: the best with each remainder. And
since every number is positive, the answer is the total less the
cheapest numbers that clear its remainder: one number with the same
remainder, or two with the other.

| file | mechanism |
|---|---|
| `max_sum_div_three.kara` ★ | by remainders: the best sum with each remainder in an `Array[i64, 3]`, copied before each number is added to each of the three |
| `max_sum_div_three_greedy.kara` | greedily: the total, less the cheaper of the smallest number with its remainder and the two smallest with the other, the two smallest of each remainder kept in one pass in an `(Option[i64], Option[i64])` that a `match` picks by `mut ref` |
| `max_sum_div_three_sorted.kara` | by sorting: the same cheapest removal, its candidates cut from the sorted numbers by `filter(..).take(..)` |
| `max_sum_div_three_table.kara` | by a table: row `i` holds the best sum of a choice among the first `i` numbers for each remainder, `None` where no choice has it, each row from the one above by skipping or taking the next number |
| `max_sum_div_three_fold.kara` | by a fold: the three best sums carried as a tuple through `Iterator.fold`, a `match` on each number's remainder saying which carried sum each new one grows from, and a closure keeping `i64.MIN` for a remainder not yet reached |
| `max_sum_div_three_solution.kara` | a Rust solution as LeetCode's Rust users write it (`[0, i32::MIN, i32::MIN]`, `for &x in nums.iter()`, `Vec<i32>`), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, five more properties |

Every arm prints the same 3 lines: LeetCode's three examples; 1000 random
lists of 1 to 10 numbers from 1 to 9 and 1000 of 1 to 200 from 1 to
10^4 (`2000 random lists: total 477696678, checksum 140454326`); and the
constraints' top, 4 * 10^4 numbers that are all 10^4, at random, and all
2 but one 1. `max_sum_div_three.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac run` and
`karac build`, and under the AddressSanitizer build.

The Mend loop: the ★, sorted, table and fold arms checked clean as first
written. The greedy arm first chose its pair with `1 => mut ones`, the
marker a call argument takes; check says a borrow for writing is `mut
ref ones`, and `karac fix` writes it in both arms. The solution arm takes
one round of fixes, 11 by `karac fix`'s count: `Vec<i32>` to brackets,
`i32::MIN` to `i32.MIN`, the `&x` patterns to `x`, `struct Solution;` to
`struct Solution {}`, `Solution::` to `Solution.`, and `let mut next =
dp;` to `dp.clone()`. That last one is where Rust and Kāra part: Rust's
`[0, i32::MIN, i32::MIN]` is an array, copied by `next = dp`, and Kāra's
is a `Vec`, which the assignment moves; the fix keeps the program right
with a clone, a heap allocation for every number. All six check clean.

## Gaps

The solution's `dp.clone()` is correct and costs time: on the bench's
workload the fixed solution takes 2.60 s and the same code with
`dp: Array[i32, 3]` and a plain copy 1.40 s. A fix that read the literal
as the array Rust wrote would keep Rust's cost (B-2026-11-20-86, a perf
row, open).

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the best sum divisible by three over every one of the `2^n`
subsets. 2000 random lists of 1 to 12 numbers from 1 to 30.

| | property |
|---|---|
| P1 | the statement read literally: the best of every subset's sum divisible by three |
| P2 | a multiple of three, from 0 to the total |
| P3 | the numbers reversed, the same answer |
| P4 | a multiple of three inserted anywhere, the answer grown by exactly it |
| P5 | a number added at the end, the answer no smaller |
| P6 | the ★ arm's answer |

All 72,000 checks pass on every arm: `2000 lists: checksum 758925675,
72000 checks over 6 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and the AddressSanitizer build. Python gives the
same checksum.

## Mutation testing

Twelve edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac run`, each failing the same way under both.

| # | mutation | failures by property |
|---|---|---|
| S1 | ★: a remainder counted reached only above 0, so the empty sum never grows | P1 1841, P4 2000, P6 9205 |
| S2 | ★: a sum stored under the remainder it grew from | P1 1347, P2 1347, P6 6735 |
| G1 | greedy: a new smallest no longer pushes the old one to second | P1 71, P3 152, P4 62, P5 35, P6 71 |
| G2 | greedy: the dearer of the two removals taken | P1 649, P5 179, P6 649 |
| O1 | sorting: the sort left out | P1 537, P3 740, P5 182, P6 537 |
| O2 | sorting: one number of the other remainder taken, not two | P1 204, P4 141, P5 106, P6 204 |
| T1 | table: the smaller of skipping and taking kept | P1 1841, P4 2000, P6 1841 |
| T2 | table: the empty choice's 0 never set | P1 1841, P4 2000, P6 1841 |
| F1 | fold: a number with remainder 1 grows remainder 0 from remainder 1 | P1 1114, P2 942, P3 1097, P6 1114 |
| F2 | fold: an unreached remainder grown to 0 | P1 345, P2 345, P3 486, P4 110, P6 345 |
| L1 | solution: each number's new row starts afresh, not from the old one | P1 981, P3 1122, P4 507, P5 507, P6 981 |
| L2 | solution: a sum overwrites its remainder's best, larger or not | P1 649, P3 883, P5 258, P6 649 |

All twelve are caught, every one by P1 and P6. T1 and T2 fail
identically: keeping the smaller of skipping and taking keeps the empty
choice everywhere, so both answer 0 for every list. P4, a multiple of
three added, catches each answer stuck at 0 (S1, T1, T2) on every list,
since the true answer grows and a stuck one does not. A first T1 changed
which remainder a number is taken from, `r + x` for `r - x`: it
survived, and is equivalent. It reads every number's remainder negated,
and negation maps remainder 0 to itself, so the best sum divisible by
three is the same; it was replaced.

## Benchmarks

`bench/` runs the same workload in Kāra, C, Rust, Go and Python: the ★
arm (the best sum with each remainder modulo 3, in an `Array[i64, 3]`
copied before each number) on 100 random lists of 4 * 10^4 numbers from
1 to 10^4 built once, 30 rounds; every answer folded into a checksum.
Every program prints `30 rounds of 100 lists of 40000: checksum
824354777`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `684b860a50`
on LLVM 22. A plain `karac build` targets x86-64-v2, so the C and
overflow-checked Rust programs are also built at x86-64-v3 for
comparison:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 1.116 to 1.167 s | 1.140 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 1.118 to 1.168 s | 1.136 s |
| Rust (`rustc -O`) | 1.179 to 1.221 s | 1.207 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.118 to 1.181 s | 1.134 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 1.112 to 1.173 s | 1.134 s |
| C (`clang -O3`) | 1.134 to 1.221 s | 1.152 s |
| C (`clang -O3 -march=x86-64-v3`) | 1.139 to 1.182 s | 1.162 s |
| Go | 1.695 to 1.816 s | 1.766 s |
| Python | 53.24 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Rust with overflow checks on runs level with Kāra (1.134 s
against 1.136 s), and the two ranges overlap. C runs level with Kāra
(1.152 s against 1.136 s); Go takes about 1.6x Kāra's time. Python takes
about 47x Kāra's time. No profile was taken.
