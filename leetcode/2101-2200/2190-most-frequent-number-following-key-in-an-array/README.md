# 2190. Most Frequent Number Following Key In an Array

You are given a **0-indexed** integer array `nums`. You are also given
an integer `key`, which is present in `nums`.

For every unique integer `target` in `nums`, **count** the number of
times `target` immediately follows an occurrence of `key` in `nums`. In
other words, count the number of indices `i` such that:

- `0 <= i <= nums.length - 2`,
- `nums[i] == key` and,
- `nums[i + 1] == target`.

Return *the* `target` *with the **maximum** count*. The test cases will
be generated such that the `target` with maximum count is unique.

```
nums = [1, 100, 200, 1, 100], key = 1  ->  100
nums = [2, 2, 2, 2, 3],       key = 2  ->  2
```

**Constraints:** `2 <= nums.length <= 1000`; `1 <= nums[i] <= 1000`;
the test cases are generated such that the answer is unique.

Each number right after the key is counted, and the most counted is the
answer; with values up to 1000 the counts fit in a list. O(n).

## Approaches

| file | mechanism |
|---|---|
| `follow.kara` ★ | each number after the key counted in a `Vec.filled(1001, 0)`, the most counted kept as it is met |
| `follow_map.kara` | the numbers after the key counted in a `Map[i64, i64]` with `entry` and `or_insert`, then the entry with the most found over `iter`; the answer is unique, so the map's order does not matter |
| `follow_sorted.kara` | the numbers after the key gathered and `sort`ed, so each target's count is a run, and the longest run's number taken; O(n log n) |
| `follow_struct.kara` | a `struct Tally` of the counts and the leader so far, made `empty`; it `record`s a number (`mut ref self`) and names its `leader` (`ref self`); the pairs read by `windows(2)` |
| `follow_iter.kara` | the list `zip`ped with itself one on, `filter`ed to the pairs that start with the key, `fold`ed into counts; the counts `enumerate`d and the most found by `max_by_key` |
| `follow_solution.kara` | LeetCode's Rust template: `use std::collections::HashMap`, `Vec<i32>`, `windows(2)`, `*cnt.entry(w[1]).or_insert(0) += 1`, `max_by_key(\|&(_, &c)\| c)`, `struct Solution;`, `Solution::`; carried by `karac fix` in three rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's two examples and four more
(the shortest list, the key followed by itself, the key last as well,
and the largest values), each with its target; then the targets' total
and a checksum over 2000 random lists of 2 to 30 numbers, of 1 to 5 and
1 to 1000 in turn, each drawn again until its answer is unique; then
the constraints' longest, 1000 numbers: a key followed by 1, 2, 3 and 1
in turn, and numbers at random. `follow.py` mirrors the ★ arm and its
output is byte-identical.

`karac fix` carries the template in three rounds of 15, 2 and 1 edits:
Rust's spellings (the `use` dropped, `Vec<..>` and `HashMap<..>` to
brackets, `HashMap::new()` to `.new()`, the `&(_, &c)` and `&x`
patterns to `(_, c)` and `x`, `struct Solution;` to `struct Solution
{}`, and `Solution::` to `.`, among them); then `HashMap` to `Map`,
once the `use` that named it is gone; then the adapter's widening `as
i64` dropped.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: for every number in the list, its count the indices i with
nums[i] the key and nums[i + 1] that number, found by trying every i,
and the number of the largest count kept. No table of counts. It checks
300 random lists of 2 to 12 numbers of 1 to 4; then 30 of 1 to 9; then
30 where the key is everywhere but one place. Each is drawn again until
its answer is unique, as the constraints promise, and all 360 are drawn
before any arm answers.

| | property |
|---|---|
| P1 | the target is the statement read literally |
| P2 | every number v made 1001 - v, the key too: the target made so too |
| P3 | the list twice, a number that is not the key between: the same target |
| P4 | a number that is not the key put in front: the same target |
| P5 | the target follows the key, and at least as often as the number after the key's first place |
| P6 | each arm agrees with at least three of the other five |

P2 holds since a renaming keeps which numbers follow which. P3 holds
since every count doubles, and the number between gains at most one,
from a key at the end, which cannot reach twice the unique largest
count. P4 holds since the number in front follows nothing that counts.
P5 holds since the target's count is the largest.

The differential prints `360 lists: checksum 945579460, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading of the same
lists. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Thirty-four edits to the differential, five to each of the ★, map,
sorted and iter arms and seven to the struct arm and the template, each
run under `karac __mir-llvm-run` and `karac __mir-run`. Seventeen are
kept, three to each Kāra arm and two to the Rust-template arm. Each
kept one is killed, fails the same way under both backends and not by
a crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the number before the key counted | P1 184, P2 80, P3 83, P4 122, P5 180, P6 184 |
| M3 | ★: the first pair skipped | P1 118, P2 109, P3 117, P4 118, P5 118, P6 118 |
| M4 | ★: every pair counted | P1 85, P3 45, P4 121, P5 77, P6 85 |
| M6 | map: the least counted | P1 110, P3 83, P5 85, P6 110 |
| M8 | map: the key's own count | P1 253, P5 240, P6 253 |
| M9 | map: the largest number counted | P1 55, P2 110, P3 9, P5 44, P6 55 |
| M11 | sorted: never sorted | P1 3, P6 3 |
| M12 | sorted: a run one short | P1 196, P2 196, P3 196, P5 196, P6 196 |
| M14 | sorted: the first run never counted | P1 296, P2 351, P3 72, P5 287, P6 296 |
| M17 | struct: the leader never displaced | P1 25, P6 25 |
| M29 | struct: a leader displaced only by two more | P1 199, P2 196, P3 198, P5 196, P6 199 |
| M30 | struct: the last pair never read | P1 92, P2 82, P3 91, P5 82, P6 92 |
| M21 | iter: the pairs that do not start with the key | P1 267, P2 175, P3 119, P4 145, P5 256, P6 267 |
| M23 | iter: the least found | P1 360, P2 360, P5 360, P6 360 |
| M24 | iter: the list zipped two on | P1 235, P2 136, P3 96, P5 232, P6 235 |
| M31 | solution: the adapter's numbers one more, the key too | P1 360, P2 360, P5 352, P6 360 |
| M33 | solution: the target one less | P1 360, P2 360, P5 349, P6 360 |

P1 and P6 kill all seventeen, P5 fifteen, P2 twelve, P3 eleven and P4
three. P4 puts a number that is not the key in front, and sees only the
edits that count a pair not starting with the key: the number before
the key (M1), every pair (M4), and the pairs that do not start with it
(M21). P3 doubles the list, and misses an edit whose answer the doubled
list keeps: the key's own count (M8), always the key; the leader never
displaced (M17), the first number after the key; the least found
(M23), here a number that never follows; the numbers one more (M31)
and the target one less (M33); and the unsorted runs (M11). P2 renames
every v as 1001 - v, and misses an edit that does not read the values'
order: every pair (M4), the least counted (M6), the key's own count
(M8), M11 and M17. P5 misses the two that still answer a number that
follows the key: the unsorted runs, which split a count only when the
same number follows the key at two places with another between, so
that only 3 lists see it (M11), and the leader never displaced (M17).

Of the thirty-four, seventeen were not kept. Six are equivalent, all
since the answer is unique: the ★ arm's and the sorted arm's tie taking
the later number (M2, M13), the struct arm's leader compared with
itself (M16), and the iter arm's counts ranked by their numbers too
(M25), as no tie reaches the largest count; the map arm's counts from 1
(M7) and the struct arm's record counting two (M19), which move or
scale every count alike. Three crash, each the template's map left empty
so `unwrap` finds `None`: the adapter's key one more (M26), the key's
place read for the key (M32), and windows of three (M34). Two fail
differently under the two backends: the map arm's pairs after a key's
follower (M10) and the template's map's least (M27) each leave a tie,
and the tie's winner is the map's order, which is per process. That is
the kata's edit, not the compiler: a `Map`'s order is unspecified, and
the kept arms rely on it only where the answer is unique. Three fail as
a kept one does: the struct arm's pair read backward, as M1; and the
iter arm's list zipped with itself and the template's window's first
counted, as M8, each counting the key. Three were left out to keep
three to an arm: the ★ arm's key never a target (M5), the sorted arm's
last follower dropped (M15), and the struct arm's leader one place on
(M20), which fails as M31.

## Verification

Every arm prints the same output as `follow.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the map, sorted, ★, template and struct arms
take 0.4 s to 0.8 s, and the iter arm 5.0 s, which folds a fresh list
of 1001 counts for every list. The differential takes 4.5 s.

## Benchmarks

The bench builds one row of 10^6 numbers of 1 to 100 once; then solves
200000 windows of 1000 numbers, the constraints' longest, each at a
random start and with the number there as the key, with the ★ arm in all
five languages. C works over a pointer and a length, Rust and Go over a
slice of the row; Kāra and Python copy each window into a list of its
own. Every implementation prints `200000 solves: checksum 685104246`.

BENCHTAB
