# 1770. Maximum Score from Performing Multiplication Operations

You are given two 0-indexed integer arrays `nums` and `multipliers` of
size `n` and `m` respectively, where `n >= m`. You begin with a score of
0. You want to perform exactly `m` operations. On the `i`th operation
(0-indexed) you will choose one integer `x` from either the start or the
end of the array `nums`, add `multipliers[i] * x` to your score, and
remove `x` from `nums`. Note that `multipliers[0]` corresponds to the
first operation, `multipliers[1]` to the second operation, and so on.
Return the maximum score after performing `m` operations.

```
nums = [1,2,3], multipliers = [3,2,1]                       ->  14
nums = [-5,-3,-3,-2,7,1], multipliers = [-10,-5,3,4,6]      ->  102
```

**Constraints:** `n == nums.length`, `m == multipliers.length`, `1 <= m
<= 300`, `m <= n <= 10^5`, and `-1000 <= nums[i], multipliers[i] <=
1000`.

The arms are `fn maximum_score(nums: Vec[i32], multipliers: Vec[i32]) ->
i32`.

## Approaches

| file | mechanism |
|---|---|
| `maximum_score.kara` ★ | a table over the operations, filled from the last back to the first and kept as one row: before operation `i`, `best[left]` is the most the operations from `i` on can score with `left` numbers taken from the front, and the rest from the back. O(m^2) time, O(m) space |
| `maximum_score_memo.kara` | top-down: the best score from operation `i` on with `left` taken from the front, the better of the two ends, each answer remembered in a `Vec[Vec[Option[i32]]]`. O(m^2) |
| `maximum_score_forward.kara` | forward: after `i` operations, `most[left]` is the best score so far with `left` taken from the front; each operation spreads every entry to its two successors, and the answer is the best entry at the end. O(m^2) |
| `maximum_score_table.kara` | a square table by how many numbers were taken from each end, `dp[l][r]`, filled by `l + r` falling. O(m^2) |
| `maximum_score_solution.kara` | a Rust solution as LeetCode's Rust users write it (`vec![vec![0; m + 1]; m + 1]`, `std::cmp::max`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 4 lines: LeetCode's two examples (`14 102`);
five edges, one number, as many multipliers as numbers, everything
negative, a zero multiplier, and a case where taking the worse end first
wins (`-21 -2 31 10 900`); the constraints' most, 300 multipliers over
100000 numbers, all of them 1000 and then the same sizes at random (`the
most: 300000000 76839266`); and 3000 random cases of 1 to 12 multipliers
over up to 10 numbers more (`3000 random cases: checksum 242890232`).
`maximum_score.py` mirrors the ★ arm, and its output is byte-identical.
Every arm gives the same output under `karac __mir-run`, `karac run`,
`karac build` and `karac __mir-llvm-run`.

The Mend loop: the ★, memo, forward and table arms check clean as first
written. The Rust solution takes one round of 14 fixes by `karac fix`'s
count, and its diff is: `struct Solution;` to `struct Solution {}`,
`Vec<i32>` to `Vec[i32]` in both signatures, `vec![vec![0; m + 1]; m +
1]` to `Vec.filled(m + 1, Vec.filled(m + 1, 0i32))`, `std::cmp::max(` to
`max(`, and `Solution::` to `Solution.`. Every arm's output matches on
the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every way of choosing the front or the back at each
operation, the chosen number removed from a copy of `nums`, the products
added up and the best score kept. LeetCode's examples, the edges, and
1992 random cases of 1 to 10 multipliers over up to 10 numbers more,
half of them with values up to 5 either side so that ties are common.
Each arm meets six properties on each case:

| property | what it checks |
|---|---|
| P1 | the statement read literally |
| P2 | no worse than always taking the front or always the back, and no more than every multiplier on the widest number |
| P3 | the numbers reversed give the same score |
| P4 | both lists negated give the same score, and the multipliers doubled give it doubled |
| P5 | a number put where no operation can reach it changes nothing |
| P6 | the ★ arm's answer |

P5 runs where `n >= 2m`, so there is room between the two ends' reach.
The literal reading first kept its running score as `let mut score = 0`
and added `multipliers[i] * x` with `+=`; check refused
`most.max(score)`, since a compound assignment does not fix an open
literal's type and `score` kept the default `i64` (design.md §8
Literals), and `karac fix` declared it `score: i32`. All 55,000 checks
pass on every arm: `2000 cases: checksum 617681072, 55000 checks over 5
arms: 0 failures`, under `karac __mir-run`, `karac run`, `karac build`
and `karac __mir-llvm-run`. Python, trying every choice with
`itertools.product`, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash. No edit
breaks P4 or P5.

| | edit | failures by property |
|---|---|---|
| M1 | ★: the worse end kept instead of the better | P1 1928, P2 1926, P6 7712 |
| M2 | ★: the back taken as though the front were | P1 1507, P2 256, P3 1653, P6 6028 |
| M3 | memo: the front's score remembered, not the best | P1 750, P3 819, P6 750 |
| M4 | memo: the back read as though nothing came from the front | P1 1314, P3 1517, P6 1314 |
| M5 | forward: unreached entries started at 0, not the least | P1 730, P6 730 |
| M6 | forward: the back's product read from the front | P1 1656, P2 373, P3 1837, P6 1656 |
| M7 | table: the front's step moved on as a back step | P1 1553, P2 248, P3 1653, P6 1553 |
| M8 | table: the back's number read from the front's count | P1 1385, P2 58, P3 1509, P6 1385 |
| M9 | solution: the all-front entry never filled | P1 1936, P2 1402, P6 1936 |
| M10 | solution: the back taken as though the front were | P1 1507, P2 256, P3 1653, P6 1507 |

## Benchmarks

The bench builds 100 lists of 1000 numbers and 100 of 300 multipliers
once, and makes 2000 calls of the ★ arm, each on a pair chosen from the
checksum so far. Every implementation prints `2000 calls over 100 lists:
checksum 567770494`.

BENCHTAB

Measured by hand, best of three on a machine shared with a test run,
Kāra takes 0.16 s against Rust's 0.06 s (0.17 s with overflow checks
on), C's 0.06 s and Go's 0.16 s; Python takes 16.6 s.
