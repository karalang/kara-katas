# 1402. Reducing Dishes

A chef has collected data on the `satisfaction` level of his `n` dishes.
Chef can cook any dish in 1 unit of time.

Like-time coefficient of a dish is defined as the time taken to cook
that dish including previous dishes multiplied by its satisfaction level
i.e. `time[i] * satisfaction[i]`.

Return the maximum sum of like-time coefficient that the chef can obtain
after preparing some amount of dishes.

Dishes can be prepared in any order and the chef can discard some dishes
to get this maximum value.

```
satisfaction = [-1, -8, 0, 5, -9]  ->  14    -1, 0 and 5 cooked: -1*1 + 0*2 + 5*3
satisfaction = [4, 3, 2]           ->  20    2*1 + 3*2 + 4*3
satisfaction = [-1, -4, -5]        ->  0     nothing cooked
```

**Constraints:** `1 <= n <= 500`, `-1000 <= satisfaction[i] <= 1000`.

Each arm is `fn max_satisfaction(satisfaction: Vec[i32]) -> i32`. The
answer is at most 1000 * (1 + 2 + .. + 500) = 125,250,000, inside `i32`.

## Approaches

| file | mechanism |
|---|---|
| `max_satisfaction.kara` ★ | greedy from the largest down: sorted with `sort()` and `reverse()`, each dish added to a running sum, and the running sum added to the total, since cooking one more dish first moves every dish already chosen one unit later; it stops when the running sum would no longer be positive. O(n log n) |
| `max_satisfaction_dp.kara` | a 0/1 knapsack over the sorted dishes: `best[k]`, an `Option[i32]`, the most k cooked dishes can give, each dish tried as the k-th with k running downward so it is cooked once, and the largest by `filter_map(..).max()`. O(n^2) |
| `max_satisfaction_suffix.kara` | the dishes cooked are always a suffix of the sorted list, so every suffix is summed by `enumerate().map(..).sum()` over the slice `order[start..]`, and the largest taken. O(n^2) |
| `max_satisfaction_memo.kara` | recursion over the sorted dishes, each cooked at the current time or skipped, memoized in a `Map[(i64, i64), i64]` keyed by the dish and the time. O(n^2) |
| `max_satisfaction_solution.kara` | a Rust solution as LeetCode's Rust users write it (sorted falling by `sort_unstable_by(\|a, b\| b.cmp(a))`, the running sum and the total kept in a tuple), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 3 lines: LeetCode's three examples and three
more (`14 20 0 0 35 1000`); the constraints' most, 500 dishes of 1000,
of -1000, and drawn (`500 dishes: 125250000 0 39073602`); and 2000
random cases of 1 to 30 dishes (`2000 random cases: 46151068 in all,
checksum 284173946`). `max_satisfaction.py` mirrors the ★ arm, and its
output is byte-identical. Every arm gives the same output under `karac
__mir-run`, `karac run`, `karac build` and `karac __mir-llvm-run`.

The Mend loop: the dp and memo arms check clean as first written. The ★
arm's `let mut running = 0;` took `running += s` from a `Vec[i32]`; an
operator does not fix a literal's type (design.md §8 Literals), so
`running` kept `i64`, check says so and names `running: i32`, and `karac
fix` writes it and `total: i32` after it, 2 fixes. The suffix arm's
`best = best.max(sum)` is the same case through a method's receiver, 1
fix. The Rust solution takes one round of 21 fixes by `karac fix`'s
count: `struct Solution;` to `struct Solution {}`, the parameter `mut
satisfaction: Vec<i32>` to `satisfaction: own Vec[i32]` with `let mut
satisfaction = satisfaction;` in the body, `sort_unstable_by` to
`sort_by`, `let (mut sum, mut res) = (0, 0);` to `let mut (sum, res) =
(0i32, 0i32);`, and `Solution::` to `Solution.`. Its output matches on
the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every order of every choice of dishes is cooked, the dish
cooked at time t adding t times its satisfaction, on up to 7 dishes.
LeetCode's examples and seven edge cases (one dish of each sign and 0,
the extremes, all equal, one positive dish among negatives), and 1993
random cases, 1 to 7 dishes two times in three and else 8 to 40, from
-1000 to 1000, leaning negative to 100, from -5 to 5, or from -30 to 10.
Each case is also given one more dish, drawn from -1000 to 1000.

| | property |
|---|---|
| P1 | the statement read literally, on up to 7 dishes |
| P2 | never below 0, cooking nothing, nor below the dishes worth more than nothing cooked in rising order |
| P3 | the order the dishes come in does not matter: the list reversed gives the same |
| P4 | one more dish never lowers it, since it may be discarded |
| P5 | every satisfaction doubled doubles it, when every one is within 500 |
| P6 | the ★ arm's answer |

All 52,245 checks pass on every arm (P1 and P5 apply to some cases
only): `2003 cases: checksum 998246637, 52245 checks over 5 arms: 0
failures`, under `karac __mir-run`, `karac run`, `karac build` and
`karac __mir-llvm-run`. Python, by the ★ arm's greedy, gives the same
checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: stopping at the first dish worth nothing or less, rather than when the running sum would stop being positive | P1 546, P6 4580 |
| M2 | ★: each dish's own satisfaction added to the total, not the running sum, so no dish is weighted by its time | P1 628, P2 1218, P4 212, P6 4956 |
| M3 | dp: k run upward, so one dish can be cooked at several times | P1 811, P6 1442 |
| M4 | dp: the dish cooked k-th weighted by k - 1 | P1 350, P2 102, P6 525 |
| M5 | suffix: the dish at place i of the suffix weighted by i, not i + 1 | P1 350, P2 102, P6 525 |
| M6 | suffix: the walk starting at the second suffix, so every dish is never cooked together | P1 350, P2 102, P6 525 |
| M7 | memo: a skipped dish still taking a unit of time | P1 756, P6 1387 |
| M8 | memo: the dishes left unsorted | P1 514, P2 380, P3 1215, P6 1104 |
| M9 | solution: sorted rising instead of falling | P1 811, P2 1442, P4 44, P6 1442 |
| M10 | solution: the running sum starting at 1 | P1 902, P5 882, P6 1534 |

M4 to M6 fail the same number of checks. Weighting every dish one less
cooks the list as if its first dish had weight 0, which is the next
suffix's sum, so each of the three in effect loses only the choice of
cooking every dish; that is inferred from the arithmetic, and the counts
agree.

## Benchmarks

The bench draws a pool of 10^5 satisfactions from -1000 to 1000 and runs
the ★ arm on 20000 windows of 500 dishes in a row, each window's start
drawn from the checksum so far. Every implementation prints `20000
windows of 500 dishes: checksum 341052924`.

BENCHTAB
