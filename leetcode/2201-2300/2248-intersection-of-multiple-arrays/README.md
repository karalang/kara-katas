# 2248. Intersection of Multiple Arrays

Given a 2D integer array `nums` where `nums[i]` is a non-empty array of
**distinct** positive integers, return *the list of integers that are
present in **each array** of* `nums` *sorted in **ascending order***.

```
nums = [[3,1,2,4,5],[1,2,3,4],[3,4,5,6]]  ->  [3,4]
nums = [[1,2,3],[4,5,6]]                  ->  []
```

**Constraints:** `1 <= nums.length <= 1000`; `1 <= sum(nums[i].length)
<= 1000`; `1 <= nums[i][j] <= 1000`; all the values of `nums[i]` are
**unique**.

The values within one array are distinct, so a value is in every array
exactly when it is counted as many times as there are arrays. The values
are at most 1000, so a count per value read in order gives the answer
already sorted. O(total + 1000).

## Approaches

| file | mechanism |
|---|---|
| `common.kara` ★ | a count for every value from 1 to 1000, kept where it reaches the number of arrays, read in order |
| `common_set.kara` | the first array as a `Set`, narrowed by `intersection` with a `Set` of each later array, then collected and sorted |
| `common_merge.kara` | sorted merging: the first array sorted is the running answer, and each later array, sorted, is walked beside it with two indices |
| `common_struct.kara` | a `struct Tally` of a `SortedMap` from value to how many arrays hold it and the number of arrays: `add` (`mut ref self`) and `everywhere` (`ref self`), the latter in key order |
| `common_iter.kara` | iterator chains: the first array's values kept by `filter` when `all` the arrays `contains` them, then sorted |
| `common_solution.kara` | LeetCode's Rust template: `Vec<Vec<i32>>` in, `Vec<i32>` out, a `HashMap` of counts filled by `*cnt.entry(x).or_insert(0) += 1`, then `into_iter().filter(..).map(..)` and a sort; carried by `karac fix` in one round |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 10 lines: LeetCode's two examples and four
more (one array, three alike, the ends of the range, and two arrays
sharing everything), each with its answer; then how many values 2000
cases of 1 to 6 arrays of 1 to 12 values from 1 to 20 have in common,
with a checksum of the answers; then the constraints' largest three
ways: one array of all 1000 values, 1000 arrays of one value, and 10
arrays of 100 values from 1 to 120. `common.py` mirrors the ★ arm and
its output is byte-identical.

The set arm would narrow its set in place with `retain`, as Rust's
`HashSet::retain` does, but the library gives `Set` no `retain` (it
gives one to `Vec`, `Map`, `SortedMap`, `SortedSet` and `VecDeque`), so
the arm uses `intersection`.

`karac fix` carries the template in one round of 25 edits: `Vec<..>` to
`Vec[..]`, the `use std::collections::HashMap` removed, `HashMap::new()`
to `Map.new()`, `for arr in &nums` and `for &x in arr` to `for arr in
ref nums` and `for x in arr`, the `&` patterns dropped from the closures,
`struct Solution;` to `struct Solution {}`, and `Solution::` to
`Solution.`.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every value from 1 to 1000 tried in increasing order, and
kept when a scan of each array finds it there; no counting, sets or
sorting. It checks 300 random cases of 1 to 5 arrays of 1 to 8 values
from 1 to 12; then 30 whose arrays are all orderings of one set; then
30 of one array of up to 30 values from 1 to 1000. All 360 are drawn
before any arm answers.

| | property |
|---|---|
| P1 | the answer is the values in every array, read literally, in order |
| P2 | the arrays in reverse order, each one reversed: the same answer |
| P3 | a copy of the first array added: the same answer |
| P4 | every value `v` written `1001 - v`: the answer mirrored the same way, in order |
| P5 | the answer strictly increasing, and itself added as one more array (or `[1]` when empty): the same answer |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 cases: checksum 872664450, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that
intersects the arrays as `frozenset`s and sorts. On a failure it prints
the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under `karac __mir-llvm-run`, and the kept
ones under `karac __mir-run` too. Seventeen are kept, three to each
Kāra arm and two to the Rust-template arm. Each kept one is killed,
fails the same way under both backends and not by a crash, and no two
kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a count one short taken as everywhere | P1 312, P3 199, P5 201, P6 312 |
| M2 | ★: values up to 999 only | P1 1, P4 43, P6 1 |
| M3 | ★: half the arrays enough | P1 236, P3 208, P5 3, P6 236 |
| M7 | set: the second array skipped too | P1 111, P2 92, P6 111 |
| M8 | set: union in place of intersection | P1 247, P6 247 |
| M9 | set: difference in place of intersection | P1 216, P2 217, P3 254, P5 254, P6 216 |
| M12 | merge: the wrong side advanced past a smaller value | P1 65, P2 32, P4 51, P6 65 |
| M13 | merge: the later arrays not sorted | P1 95, P2 44, P3 92, P4 71, P6 95 |
| M14 | merge: the first array not sorted | P1 148, P2 128, P3 67, P4 150, P5 67, P6 148 |
| M18 | struct: a value held by most arrays kept | P1 170, P3 182, P5 17, P6 170 |
| M19 | struct: every value counted once | P1 116, P3 86, P5 86, P6 116 |
| M20 | struct: the first array not added | P1 199, P2 155, P3 199, P5 86, P6 199 |
| M22 | iter: any array enough | P1 242, P2 246, P6 242 |
| M23 | iter: not sorted | P1 116, P2 118, P4 129, P5 116, P6 116 |
| M24 | iter: the last array not checked | P1 118, P2 155, P3 118, P5 118, P6 118 |
| M30 | solution: the last array dropped on the way in | P1 204, P2 155, P3 204, P5 204, P6 204 |
| M31 | solution: values one higher on the way out | P1 202, P4 202, P5 202, P6 202 |

P1 and P6 kill all seventeen, P5 eleven, P2 and P3 ten each, and P4
six. P3 adds a copy of an array, so an arm that counts and compares
with the number of arrays wrongly (M1, M3, M18, M19) or skips one array
answers differently; P2 reverses the order of the arrays and of each
one, and catches the arms that treat the first or last array apart or
lean on an order. P4 mirrors every value, and catches the edits that
break the order of the answer or the ends of the range (M2's value
1000 is value 1 mirrored). P5's own-answer array catches an answer out
of order or holding a value not everywhere.

Of the thirty-one, fourteen were not kept, and none survives or
crashes. Two differ between the backends and from run to run, and are
left out for that: the set arm's and the template's answers in the
set's or the map's own order (M10, M28), which is random per process.
Three fail alike in a group of their own: counts begun at one, or a
count one short taken as everywhere, in the struct arm and the template
(M21, M27, M29); and two pairs alike: the ★ arm's answer reversed and
the iter arm's sorted largest first (M5, M25), and the ★ arm's last
array not counted and the struct arm's arrays never counted (M6, M17),
both of which answer nothing. Five fail their own way and are left out
for the count of three: the ★ arm's arrays counted from their second
value (M4), the set begun from the last array (M11), the merge arm's
last value never matched and smaller values kept (M15, M16), and the
iter arm's values 1 and 2 never kept (M26).

## Verification

Every arm prints the same output as `common.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.4 s to 0.7 s and the
differential 2.0 s.

## Benchmarks

The bench answers 20000 cases with the ★ arm in all five languages,
each 10 arrays of 100 distinct values from 1 to 150, drawn by a partial
shuffle of one pool, so every case is at the constraints' total of
1000. Every implementation prints `20000 cases: checksum 614380970`.

BENCHTAB
