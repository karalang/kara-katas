# 2845. Count of Interesting Subarrays

You are given a **0-indexed** integer array `nums`, an integer
`modulo`, and an integer `k`.

Your task is to find the count of subarrays that are **interesting**.

A **subarray** `nums[l..r]` is **interesting** if the following
condition holds:

- Let `cnt` be the number of indices `i` in the range `[l, r]` such
  that `nums[i] % modulo == k`. Then, `cnt % modulo == k`.

Return *an integer denoting the count of interesting subarrays*.

**Note:** A subarray is *a contiguous non-empty sequence of elements
within an array*.

```
nums = [3,2,4], modulo = 2, k = 1    ->  3
nums = [3,1,9,6], modulo = 3, k = 0  ->  2
```

**Constraints:** `1 <= nums.length <= 10^5`; `1 <= nums[i] <= 10^9`;
`1 <= modulo <= 10^9`; `0 <= k < modulo`.

## Approaches

| file | mechanism |
|---|---|
| `interesting.kara` ★ | a subarray's count is a difference of two prefix counts, so it is interesting when the earlier prefix is the later one less k, mod modulo: a `Map` from each prefix count mod modulo to how often it has come up, read with `get(..) ?? 0` before each new prefix is added |
| `interesting_each.kara` | every subarray in turn, the count carried on from each start as the end moves right; O(n^2), for the harness's sizes |
| `interesting_places.kara` | the prefix counts first, then each prefix's places listed under its value in a `Map[i64, Vec[i64]]` through `entry().or_insert()`; for each prefix the earlier ones it pairs with counted by `partition_point` in the list of the value it wants, read by `if let Some(list)` |
| `interesting_halves.kara` | divide and conquer: the subarrays inside each half by recursion, and those across the middle by pairing the left half's suffix counts, tallied in a `SortedMap`, with the right half's prefix counts |
| `interesting_solution.kara` | a Rust solution as LeetCode's Rust users write it: a `HashMap<i32, i64>` of prefix counts read with `*cnt.get(&key).unwrap_or(&0)`, the prefix kept as `0i32` and the key made non-negative with `rem_euclid`, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 5 lines: LeetCode's two examples; one number
counted and not; 4000 numbers with modulo 1, every subarray
interesting, then with a modulo of 10^9 that no count reaches; then
3000 random arrays of 1 to 10 numbers up to 10 with modulo up to 5,
and 50 of up to 1000 numbers up to 10^9 with modulo up to 10 or up to
10^9, as totals and checksums. `interesting.py` mirrors the ★ arm and
its output is byte-identical.

```
3 2
0 1
8002000 0
3000 short arrays: 30846 subarrays, checksum 494088514
50 long arrays: 1073723 subarrays, checksum 224036214
```

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: every subarray `nums[l..=r]`, its places with
`nums[i] % modulo == k` counted afresh, and kept when that count `%
modulo == k`. It draws 2000 random arrays of 1 to 10 numbers up to 10
with modulo up to 5, then 50 of up to 300 numbers up to 10^9 with
modulo up to 10 or up to 10^9, all before any arm answers; the literal
reading is asked only of the first 2000.

| | property |
|---|---|
| P1 | up to 10 numbers, the answer is the literal reading's |
| P2 | the array reversed: the same answer |
| P3 | every number replaced by its remainder plus modulo: the same answer |
| P4 | the array written twice: at least twice the answer |
| P5 | modulo 1 and k 0: every subarray, n(n + 1) / 2 |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2050 cases: checksum 389653661, 61500 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases gives the same checksum. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the empty prefix not counted | P1 1394, P2 553, P5 2050, P6 1416 |
| M2 | ★: the prefix added before it is read | P1 902, P5 2050, P6 909 |
| M3 | ★: the wanted prefix k more, not less | P1 502, P6 517 |
| M4 | each: the count compared without its modulo | P1 702, P5 2050, P6 722 |
| M5 | places: a prefix paired with itself | P1 902, P4 64, P5 2050, P6 909 |
| M6 | places: the prefix not wrapped by modulo | P1 623, P2 247, P4 33, P5 1862, P6 643 |
| M7 | halves: one number alone never counted | P1 1277, P5 2050, P6 1286 |
| M8 | halves: the left suffixes' counts not reduced | P1 514, P2 203, P5 1862, P6 531 |
| M9 | halves: the right half's subarrays left out | P1 1235, P2 671, P4 115, P5 1862, P6 1257 |
| M10 | solution: the key's sign kept | P1 242, P2 152, P4 110, P6 257 |

## Benchmarks

The bench draws 10 arrays of 10^5 numbers, LeetCode's most, up to
10^9, half with a modulo up to 10 and half up to 10^5, all of them
first, then answers each 20 times by the ★ arm in all five languages.
Kāra, Rust, Go and Python count in their own hash maps (Kāra's and
Rust's SipHash); C, with none of its own, counts in an open-addressed
table. Every implementation prints `10 arrays of 100000, 20 rounds:
165001390580 subarrays, checksum 530673655`.

BENCHTAB

## Verification

All five arms print the same output as `interesting.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The four own arms checked clean as first written. The harness first
held 10^5 numbers, LeetCode's most, for its modulo-1 line, which the
O(n^2) arm cannot answer in time; it holds 4000, and the bench keeps
10^5.

LeetCode's Rust template took 19 `karac fix` edits in one run, the
wrapper included: `use std::collections::HashMap;` gave way to `struct
Solution {}` for the `impl`; `Vec<..>` became `Vec[..]`, `HashMap<..>`
`Map[..]` and `HashMap::new()` `Map.new()`; `0i64` lost its suffix,
`i64` being the default; `for &x in` and `|&x|` lost their `&`;
`cnt.get(&key).unwrap_or(&0)` lost both `&`; `Solution::` took `.`.
The `0i32` suffix, not the default, `rem_euclid`, and the `*` on the
read were accepted as written.
