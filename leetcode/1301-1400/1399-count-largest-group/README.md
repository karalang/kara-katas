# 1399. Count Largest Group

You are given an integer `n`.

We need to group the numbers from `1` to `n` according to the sum of its
digits. For example, the numbers 14 and 5 belong to the same group,
whereas 13 and 3 belong to different groups.

Return the number of groups that have the largest size, i.e. the maximum
number of elements.

```
n = 13  ->  4    [1,10], [2,11], [3,12], [4,13], [5], [6], [7], [8], [9]
n = 2   ->  2    [1], [2]
```

**Constraints:** `1 <= n <= 10^4`.

Each arm is `fn count_largest_group(n: i32) -> i32`. A digit sum up to
10^4 is at most 36, for 9999.

## Approaches

| file | mechanism |
|---|---|
| `count_largest_group.kara` ★ | each number's digit sum found by peeling off its last digit with `% 10` and `/ 10`, the groups' sizes counted in a `Vec` of 37 indexed by the sum, then the largest size by `max()` and the groups of that size by `filter(..).count()`. O(n log n) |
| `count_largest_group_map.kara` | the groups in a `Map[i64, i64]` from digit sum to size, filled through `entry(sum).or_insert(0)`, the sum read off the number's decimal text with `chars()` and `to_digit(10)` |
| `count_largest_group_table.kara` | each digit sum from an earlier one, x's sum being the sum of x / 10 plus x's last digit, kept in a table, so one addition a number; the largest size and its count kept up to date as each group grows. O(n) |
| `count_largest_group_sorted.kara` | every digit sum written down by a `map` closure, the list sorted so each group is a run, and the runs' lengths walked for the longest and how many runs are that long. O(n log n) |
| `count_largest_group_solution.kara` | a Rust solution as LeetCode's Rust users write it (a `HashMap<i32, i32>` filled through `entry().or_insert`, the digit sum by `to_string().chars()` and `to_digit`, the largest from `values().max()`, and the groups of that size counted by `filter(\|&&v\| v == max)`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 3 lines: LeetCode's two examples and two more
(`4 2 6 5`); the constraints' most and the turns of the decades below
it, 10^4, 9999, 1000, 999, 100, 99, 10, 9 and 1 (`ends: 1 1 2 2 1 1 1 9
1`); and every n from 1 to 10^4 (`n = 1 to 10^4: 11887 in all, checksum
318568885`). `count_largest_group.py` mirrors the ★ arm, and its output
is byte-identical. Every arm gives the same output under `karac
__mir-run`, `karac run`, `karac build` and `karac __mir-llvm-run`.

The Mend loop: the ★, map and table arms check clean as first written.
The sorted arm's closure summed into `let mut sum = 0;` and returned it
to a `collect()` into a `Vec[i32]`; an operator or a method does not fix
a literal's type (design.md §8 Literals), so `sum` kept `i64`, check
says so and names `sum: i32`, and `karac fix` writes it, 1 fix. The Rust
solution takes one round of 11 fixes by `karac fix`'s count: the `use`
line deleted, `struct Solution;` to `struct Solution {}`, `HashMap<i32,
i32>` to `Map[i32, i32]`, `HashMap::new` to `Map.new`, the `&&` dropped
from the closure's pattern `|&&v|`, which matches through the reference
already, and `Solution::` to `Solution.`. Its output matches on the
first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every number from 1 to n put in the group of its digits' sum,
each digit read off its decimal text, and the groups as long as the
longest counted. Every n from 1 to 1000, the constraints' most and the
turns of the decades above 1000, and 993 n drawn from 1001 to 10^4.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | at least one group, and no more than n, or than the 36 sums a number up to 10^4 can have |
| P3 | one more number joins one group, so the count for n is the count for n - 1, one more, or 1 |
| P4 | below 10 every number is its own group: n |
| P5 | for 99, 999 and 9999 the digit sums lie symmetric about 9k / 2, so the middle sum is the one largest group when 9k is even and the two middle sums are when it is odd |
| P6 | the ★ arm's answer |

All 40,115 checks pass on every arm (P3 to P5 apply to some n only):
`2003 cases: checksum 741185552, 40115 checks over 5 arms: 0 failures`,
under `karac __mir-run`, `karac run`, `karac build` and `karac
__mir-llvm-run`. Python, summing `int(c)` over `str(x)`, gives the same
checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the numbers from 1 to n - 1, n left out | P1 199, P2 1, P4 9, P6 796 |
| M2 | ★: the digit sum stopped before the leading digit | P1 701, P4 8, P5 1, P6 2804 |
| M3 | map: the smallest group's size taken for the largest | P1 625, P3 8, P5 1, P6 625 |
| M4 | map: 0 put in a group of its own | P1 9, P2 9, P4 9, P6 9 |
| M5 | table: a group pulling ahead adding to the count instead of restarting it at 1 | P1 1994, P2 1961, P5 3, P6 1994 |
| M6 | table: a group as large as the largest taken as larger, restarting the count | P1 634, P4 8, P5 1, P6 634 |
| M7 | sorted: the sums left unsorted, so a group is split into runs | P1 1994, P2 1967, P5 3, P6 1994 |
| M8 | sorted: the walk starting at the second sum, so the first number is left out | P1 19, P2 1, P4 9, P6 19 |
| M9 | solution: the groups not of the largest size counted | P1 1998, P2 10, P3 122, P4 9, P5 3, P6 1998 |
| M10 | solution: the largest digit taken for the digit sum | P1 631, P5 1, P6 631 |

## Benchmarks

The bench runs the ★ arm for 6000 values of n from 1 to 10^4, each drawn
from the checksum so far, so each round walks up to 10^4 numbers and
their digits. Every implementation prints `6000 rounds of n up to 10^4:
checksum 189021227`.

BENCHTAB
