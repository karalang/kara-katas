# 2419. Longest Subarray With Maximum Bitwise AND

You are given an integer array `nums` of size `n`.

Consider a **non-empty** subarray from `nums` that has the **maximum**
possible **bitwise AND**.

- In other words, let `k` be the maximum value of the bitwise AND of
  **any** subarray of `nums`. Then, only subarrays with a bitwise AND
  equal to `k` should be considered.

Return *the length of the **longest** such subarray*.

The bitwise AND of an array is the bitwise AND of all the numbers in it.

A **subarray** is a contiguous sequence of elements within an array.

```
nums = [1,2,3,3,2,2]   ->  2
nums = [1,2,3,4]       ->  1
```

**Constraints:** `1 <= nums.length <= 10^5`; `1 <= nums[i] <= 10^6`.

An AND never exceeds any of its values, so no subarray's AND is above
the largest value, and the largest value alone reaches it. A subarray
holding any smaller value has an AND below the largest, so the
subarrays that count are exactly the runs of the largest value, and the
answer is the longest of them.

## Approaches

| file | mechanism |
|---|---|
| `longest.kara` ★ | one scan: the largest value so far and the run of it ending here, a larger value starting the count again. O(n) |
| `longest_twopass.kara` | two passes: the largest value, then the longest run of it. O(n) |
| `longest_ands.kara` | every AND, kept compactly: the distinct ANDs of the subarrays ending at each index, at most 21 since each step down clears a bit, each with its longest length; the largest AND seen and its longest length are the answer. O(n log max), and no use of the observation above |
| `longest_runs.kara` | runs: the array cut into `(value, length)` runs, and the longest run of the largest value taken by comparing the tuples. O(n) |
| `longest_iter.kara` | iterators: the largest value by `max`, then one `fold` carrying the run and the longest so far. O(n) |
| `longest_solution.kara` | LeetCode's Rust template: `*nums.iter().max().unwrap()`, then `for &x in &nums` counting the run; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's two examples; one value;
five copies of one value; the largest at both ends; two runs of the
largest as long as each other; `10^5` values up to `10^6`, each a copy
of the one before with probability 1/2, and `10^5` of 1 to 3, a copy
with probability 1/50; then 3000 random arrays of up to 30 values up to
1 to 8, with a checksum and the total of the answers. `longest.py`
mirrors the ★ arm and its output is byte-identical, and the mirror was
checked on 20000 random arrays of up to 9 values against the AND of
every subarray.

`check` first reports 4 errors on the template, and `karac fix` carries
it in one call, reporting 8 edits: the `Vec<..>` given brackets; the
`&` of `for &x` dropped and `&nums` written `ref nums`; both counters
annotated `i32`, the type the template's `-> i32` gives them; and
`struct Solution;` given its braces. The `*` of `*nums.iter().max()`
stands as Kāra.

The runs arm keeps its best run with `best = r`, `r` a `ref (i64, i64)`
from `runs.iter()` and `best` bound by `let mut best = (0, 0)`. `check`
first refused that store as a reference where a tuple was expected,
though a `ref` to a `Copy` value is read as the value (core-semantics
§5.10) and the same store of a `ref i64` passed (B-2026-11-21-44,
fixed).

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the AND of every subarray, from every start to every end, the
largest of them, and the longest subarray whose AND is that largest. No
use of the largest value. It checks 300 random arrays of 1 to 12 values
up to 1 to 8, each a copy of the one before with probability 1 in 1 to
4; then 30 of up to 400 values up to `10^6`; then 30 of up to 400 of 1
to 3, in long runs. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | the answer is at least 1 and at most how many times the largest value appears |
| P3 | the array reversed: the same answer |
| P4 | every value doubled: the same answer |
| P5 | every value given twice in its place: twice the answer |
| P6 | each arm agrees with at least three of the other five |

P2 holds because a single largest value is a subarray of AND `k`, and
every subarray of AND `k` holds only the largest value. P3 holds
because reversing keeps every subarray's values, P4 because doubling
shifts every value one bit and keeps every comparison of ANDs, and P5
because doubling every value in place doubles every run.

The differential prints `360 cases: checksum 984107555, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and ANDs every subarray. On a failure it prints the
first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a larger value keeping the run | P1 80, P2 70, P3 119, P6 80 |
| M2 | ★: the longest never cleared | P1 55, P2 51, P3 89, P6 55 |
| M4 | ★: the run counted before the check | P1 360, P2 115, P5 360, P6 360 |
| M8 | twopass: the first value never compared | P1 35, P2 35, P3 19, P5 35, P6 35 |
| M10 | twopass: the run never counted past two | P1 190, P5 245, P6 190 |
| M11 | twopass: the count of the largest taken | P1 82, P6 82 |
| M13 | ands: a merged AND kept short | P1 245, P5 360, P6 245 |
| M14 | ands: an equal AND restarting the length | P1 41, P3 48, P6 41 |
| M16 | ands: an OR for the AND | P1 225, P2 225, P6 225 |
| M19 | runs: the first run of the largest kept | P1 44, P3 48, P6 44 |
| M20 | runs: the last run never read | P1 171, P2 147, P3 66, P6 171 |
| M21 | runs: a run grown by two | P1 245, P2 200, P5 360, P6 245 |
| M22 | iter: the smallest value sought | P1 157, P2 58, P6 157 |
| M25 | iter: the run starting at 1 after a break | P1 186, P2 112, P3 85, P5 186, P6 186 |
| M26 | iter: the first value skipped | P1 174, P2 40, P3 85, P5 174, P6 174 |
| M30 | solution: values compared halved | P1 58, P2 28, P4 58, P6 58 |
| M31 | solution: the answer one too long | P1 360, P2 278, P5 360, P6 360 |

P1 and P6 kill all seventeen, P2 twelve, P3 and P5 eight each, and P4
one. P4 doubles every value, which keeps every comparison and every
AND, so only a mutant whose error depends on the values' low bit fails
it: the template's values compared halved (M30), which takes 6 and 7
for one value but not 12 and 14.

Of the thirty-one, fourteen were not kept. Eleven fail the same checks
as a kept one: a run never broken in the ★ and iter arms and the
template (M3, M23, M28) as the count of the largest taken (M11), which
is the same answer; a value as large taken as larger (M5) and equal
values never joined (M17) as a merged AND kept short (M13); the last
run alone kept and the longest only the last run (M6, M24) as an equal
AND restarting the length (M14); the smallest value sought in the
twopass arm and the template (M7, M27) as the iter arm's (M22); and the
value alone never counted and the template's run counted after the
check (M15, M29) as the run counted before the check (M4). The runs
arm's longer run of a smaller value taken (M18) fails apart from every
kept one, and was left out because that arm keeps three already. Two
are not killed and cannot be: the twopass arm's run kept across one
other value (M9) writes `else if run > 0 { run = 0 }`, which ends in
the same `run` as `else { run = 0 }`; and the ands arm's ANDs never
merged (M12) keeps two entries for an AND where it kept one, each with
its own length, and the longest of them is the same.

## Verification

Every arm prints the same output as `longest.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.8 to 2.4 s. The differential
takes 4.1 s there, 1.2 s under `karac __mir-llvm-asan` and 1.0 s under
`karac run`.

## Benchmarks

The bench builds 10 arrays of `10^5` values once from its own generator.
Array `i` holds values from 1 to `2 + 100 i`, and each value repeats the
one before it with probability 1/2, so the arrays have long runs and the
small arrays have many runs of their maximum. It then makes 500 passes,
answering every array and folding the answer plus the pass into the
checksum. The bench uses the ★ arm, one scan that keeps the largest
value so far and the run of it, in all five languages. Every
implementation prints `500 passes over 10 arrays of 10^5 values:
checksum 432314724`. The slices are borrowed, not copied: Kāra's
parameter borrows by default, Rust takes `&[i64]`, C a pointer and a
length, Go a slice header, and Python a list.

BENCHTAB
