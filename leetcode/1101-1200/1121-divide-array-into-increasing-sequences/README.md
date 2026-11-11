# 1121. Divide Array Into Increasing Sequences

Given an integer array `nums` sorted in non-decreasing order and an
integer `k`, return `true` if this array can be divided into one or more
disjoint increasing subsequences of length at least `k`, or `false`
otherwise.

```
nums = [1,2,2,3,3,4,4], k = 3  ->  true    ([1,2,3,4] and [2,3,4])
nums = [5,6,6,7,8], k = 3      ->  false
```

**Constraints:** `1 <= k <= nums.length <= 10^5`; `1 <= nums[i] <=
10^5`; `nums` is sorted in non-decreasing order.

The arms are `fn can_divide_into_subsequences(nums: Vec[i32], k: i32) ->
bool`. A value that appears `f` times needs `f` sequences, one for each
copy, and `f` sequences of at least `k` values need `f * k` of them;
dealing the sorted values to `f` piles in turn meets that bound, so the
answer is whether the longest run of one value, times `k`, fits in the
array.

## Approaches

| file | mechanism |
|---|---|
| `can_divide.kara` ★ | the longest run of one value found in a single pass over the sorted array, times `k`, against the length. O(n) |
| `can_divide_counts.kara` | each value's count in a `Map`, the largest count against the length over `k`. The order the map walks in does not matter to a largest. O(n) |
| `can_divide_window.kara` | a window as wide as the number of sequences there can be: with `m = n / k`, the array divides unless some value equals the one `m` places after it. O(n) |
| `can_divide_piles.kara` | the division built: as many piles as the longest run, the values dealt to them in turn, and every pile checked to rise and to hold at least `k` values. O(n) |
| `can_divide_search.kara` | each run found by binary search for the first larger value after its start. O(d log n) for `d` distinct values |
| `can_divide_solution.kara` | a Rust solution as LeetCode's Rust users write it (`impl Solution`, the runs from `chunk_by`), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: the answers for LeetCode's two
examples and six more (one value, `k` as long as the array, a run as
long as the array, a run one too long, every value once, and two runs
that each just fit), then over 2000 random sorted arrays of up to 100000
values, LeetCode's longest, how many can be divided and a checksum
(`2000 random arrays: 1302 can be divided, checksum 621770292`).
`can_divide.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: each value in turn joins one of the sequences begun so far
whose last value is smaller, or begins a new one, every way tried, and
the array divides if some way leaves every sequence with at least `k`
values. It checks 2000 problems in four kinds of 500: up to 10 values
from 1 to 3 and up to 10 from 1 to 10, each with a random `k`; up to 10
values with one value repeated over a random stretch; and up to 300
values from 1 to a top of 1 to 300. The last two take the largest `k`
the longest run allows, or one more. Every random choice is drawn before
any arm answers.

| | property |
|---|---|
| P1 | the statement read literally, on the arrays of up to 10 values |
| P2 | by a second reading, the copies: no value has so many that, one to a sequence, the rest cannot give each of those sequences `k` |
| P3 | every value doubled, the same `k`, gives the same answer |
| P4 | the values renamed in order, each distinct value a random step above the one before, give the same answer |
| P5 | a yes stays a yes for a smaller `k`, and a no stays a no for a larger one |
| P6 | new values above the largest keep a yes a yes |

All 69,102 checks pass on every arm: `2000 problems: checksum 818045564,
69102 checks over 6 arms: 0 failures`. A Python reading of the same
problems, asking whether every value's copies fit, gives the same
checksum.

## Mutation testing

Thirty edits to the differential, five to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`, each failing the same way
under both. Twenty-nine are caught. Fifteen are kept, no two failing the
same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a repeat counted twice | P1 305, P2 530, P3 320 |
| M2 | ★: the second value never extends a run | P1 77, P2 81, P3 62 |
| M3 | ★: only the last run counted | P1 308, P2 538 |
| M4 | counts: the least count taken | P1 518, P2 768 |
| M5 | counts: one value spare | P1 81, P2 119, P3 119 |
| M6 | counts: the count added to `k` | P1 547, P2 800, P3 385 |
| M7 | window: one place narrower | P1 219, P2 418, P3 61, P6 7 |
| M8 | piles: dealt in blocks, not in turn | P1 430, P2 654, P3 399 |
| M9 | piles: one pile too many | P1 827, P2 1053 |
| M10 | piles: a run never ends | P1 114, P2 335, P3 185 |
| M11 | search: a run ends at its own value | P1 690, P2 947 |
| M12 | search: the last place never searched | P1 86, P2 90, P3 64, P6 20 |
| M13 | solution: runs of rising values | P1 299, P2 520 |
| M14 | solution: twice the room | P1 476, P2 733 |
| M15 | solution: runs of changing values | P1 432, P2 661, P3 880, P6 127 |

P1 and P2 catch all twenty-nine, P3 nineteen, P6 three, and P4 and P5
none. Every edit changes the run an arm finds or the bound it holds it
to, and the arm still answers by a run's length against `k`: renaming
the values in order keeps every run, so P4 cannot see the change, and a
bound that grows with `k` keeps a yes for a smaller `k` and a no for a
larger one, so P5 cannot either. P3 sees the edits whose answer does not
double with the array: a run counted from the wrong place (M2, M10,
M12), a fixed amount added (M1, M5, M6), or the wrong runs (M8, M15). P6
catches the three whose answer can fall when the array grows (M7, M12,
M15).

Of the fifteen not kept, three fail as a kept edit: the counts and
window arms losing the first value as M2, and the solution arm taking
the shortest run as M4. Seven fail in three groups as each other: the ★
arm's strict comparison and the window as wide as one value fewer
allows; a new run starting at zero, the window one place wider, and each
searched run one short; and each count or run one too many in the counts
and solution arms. Four fail in ways of their own but were not needed:
one pile too few, a pile one short accepted, the search starting a place
late, and the value after each run skipped. The window arm answering
yes when no window fits is never caught, and cannot be: its width is
zero only when `k` is larger than the array, which the constraints rule
out.

## Verification

Every arm prints the same output as `can_divide.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing
on any file, and `karac fix` has nothing to apply.

The kata found one gap, fixed. The ★, counts and search arms were
written with `longest * (k as i64) <= nums.len()`, and the window arm
with `nums.len() / (k as i64)`, `k` being an `i32`. The cast widens
implicitly there, and `karac fix` deleted its `as i64` and left `(k)`
behind, parentheses around a single name (B-2026-11-11-43); a cast in parentheses
of its own now goes with them, and the four arms say `longest * k` and
`nums.len() / k`. The piles, ★, counts, window and search arms were
written as Kāra, the solution arm as Rust writes it. `karac fix` carried
the solution arm to a clean check in five rounds: `Vec<i32>` to
`Vec[i32]` and `Solution::` to `Solution.`, `struct Solution {}`
declared, `.iter()` after `chunk_by(..)`, `k as usize` to `k as i64`,
and that cast dropped as above.

## Benchmarks

The bench builds 4 sorted arrays of 100000 values, LeetCode's longest,
from 1 to 2000, 1000, 500 and 200, once. Each of 250 rounds copies one
value over its neighbour in every array, which keeps it sorted and moves
a run's length, and answers it with the ★ arm for a new `k` from 1 to
2000: 1000 calls over 10^8 values. Every implementation prints `250
rounds over 4 arrays of 100000 values: 402 can be divided, checksum
864723965`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `c57d79254b`
on LLVM 22. karac builds for the x86-64-v3 baseline, so the C and
overflow-checked Rust programs are also built at `-march=x86-64-v3`:

| | time | median |
|---|---|---|
| Rust (`rustc -O`) | 0.076 to 0.123 s | 0.086 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.065 to 0.136 s | 0.087 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.077 to 0.146 s | 0.102 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.081 to 0.151 s | 0.103 s |
| Kāra (`karac build`) | 0.075 to 0.187 s | 0.113 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.091 to 0.126 s | 0.115 s |
| C (`clang -O3`) | 0.106 to 0.140 s | 0.119 s |
| Go | 0.116 to 0.188 s | 0.138 s |
| Python | 12.1 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Each program runs for about a tenth of a second, so the medians
are close to the noise between runs. Kāra's sequential binary ties
Rust's and is about 1.2x faster than overflow-checked Rust, 1.4x faster
than C and 1.6x faster than Go; the gap to C and Go was not traced.
Python takes about 140x Kāra's time.
