# 1764. Form Array by Concatenating Subarrays of Another Array

You are given a 2D integer array `groups` of length `n`. You are also
given an integer array `nums`. You are asked if you can choose `n`
disjoint subarrays from the array `nums` such that the `i`th subarray is
equal to `groups[i]` (0-indexed), and if `i > 0`, the `(i-1)`th subarray
appears before the `i`th subarray in `nums` (that is, the subarrays must
be in the same order as `groups`). Return `true` if you can do this
task, and `false` otherwise. Subarrays are disjoint if and only if there
is no index `k` such that `nums[k]` belongs to more than one subarray.

```
groups = [[1,-1,-1],[3,-2,0]], nums = [1,-1,0,1,-1,-1,3,-2,0]  ->  true
groups = [[10,-2],[1,2,3,4]],  nums = [1,2,3,4,10,-2]          ->  false
groups = [[1,2,3],[3,4]],      nums = [7,7,1,2,3,4,7,7]        ->  false
```

**Constraints:** `1 <= groups.length <= 10^3`, `1 <= groups[i].length,
sum(groups[i].length) <= 10^3`, `1 <= nums.length <= 10^3` and `-10^7 <=
groups[i][j], nums[k] <= 10^7`.

The arms are `fn can_choose(groups: Vec[Vec[i32]], nums: Vec[i32]) ->
bool`.

## Approaches

| file | mechanism |
|---|---|
| `can_choose.kara` ★ | greedy: each group matched at the first place it fits at or after where the last one ended, compared value by value with `(0..len).all`. Taking the first place never hurts, since any later place leaves less room for the rest. O(n m) |
| `can_choose_kmp.kara` | each group found with Knuth-Morris-Pratt from where the last one ended: the group's failure table, then one pass over `nums` that never steps back. O(n + m) |
| `can_choose_windows.kara` | each group looked for with `windows` over the rest of `nums` and `position`, the slices compared whole. O(n m) |
| `can_choose_hash.kara` | Rabin-Karp: a rolling hash of each window of `nums` the group's length, and the values compared only where the hashes agree. O(n + m) expected |
| `can_choose_solution.kara` | a Rust solution as LeetCode's Rust users write it (`&nums[i..i + g.len()] == g.as_slice()`, `!found`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 4 lines: LeetCode's three examples (`true
false false`); five edges, one group that is the whole array, two groups
that would have to overlap, a group longer than the array, a near match
before the real one, and the same group twice (`true false false true
true`); the constraints' most, one group of up to 1000 values, 1000
groups of one value, and 20 groups with one value changed (`the most:
true true false`); and 3000 random cases of 1 to 5 groups of 1 to 4
values, one in three with a value changed (`3000 random cases: checksum
345284041`). `can_choose.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac __mir-run`,
`karac run`, `karac build` and `karac __mir-llvm-run`.

The Mend loop: the ★, kmp and windows arms check clean as first written.
The hash arm's `v as i64 % MOD` took 1 fix, the cast dropped. The Rust
solution takes one round of 14 fixes by `karac fix`'s count, and its
diff is: `struct Solution;` to `struct Solution {}`, `Vec<Vec<i32>>` and
`Vec<i32>` to `Vec[Vec[i32]]` and `Vec[i32]` in both signatures,
`&nums[i..i + g.len()]` to `nums[i..i + g.len()]`, `!found` to `not
found` and `Solution::` to `Solution.`. Every arm's output matches on
the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every place each group could start, at or after the last
group's end, tried in turn, with no greedy step. LeetCode's examples,
the edges, and 1990 random cases of 1 to 4 groups of 1 to 4 values from
1 to 3 values, up to 3 other values around each group, one in three with
a value changed. Each arm meets six properties on each case:

| property | what it checks |
|---|---|
| P1 | the statement read literally |
| P2 | the groups fit their own concatenation |
| P3 | every group and `nums` read backwards, the groups in reverse order, answer the same |
| P4 | a value no group holds, at both ends of `nums`, changes nothing |
| P5 | every value negated changes nothing |
| P6 | the ★ arm's answer |

All 60,000 checks pass on every arm: `2000 cases: checksum 131551538,
60000 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and `karac __mir-llvm-run`. Python, trying every
place, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: a group that ends at the last value refused | P1 1116, P2 2000, P3 433, P4 1116, P6 4464 |
| M2 | ★: each group may share its last value with the next | P1 44, P6 176 |
| M3 | kmp: a failure table of zeros, so no match restarts inside another | P1 28, P3 41, P6 28 |
| M4 | kmp: the failure table built a value late | P1 24, P3 38, P6 24 |
| M5 | windows: each group may overlap the next | P1 23, P3 24, P6 23 |
| M6 | windows: the place found taken from the array's start, not the last group's end | P1 34, P3 18, P4 7, P6 34 |
| M7 | hash: the outgoing value's power one short | P1 331, P3 206, P4 623, P6 331 |
| M8 | hash: negative values hashed as negatives | P5 543 |
| M9 | solution: no group may end at the last value | P1 1116, P2 2000, P3 433, P4 1116, P6 1116 |
| M10 | solution: a group not found passed over | P1 181, P6 181 |

## Benchmarks

The bench builds 200 cases once, each 10 groups of 1 to 40 values from
2, with up to 60 other values before each group and one value changed in
every other case, and makes 200000 calls of the ★ arm, each on a case
chosen from the checksum so far. Every implementation prints `200000
calls over 200 cases: checksum 814240724`.

BENCHTAB

Measured by hand, best of three on a machine shared with a test run,
Kāra takes 0.73 s against Rust's 0.65 s (0.73 s with overflow checks
on), C's 0.64 s and Go's 0.65 s; Python takes 25.8 s.
