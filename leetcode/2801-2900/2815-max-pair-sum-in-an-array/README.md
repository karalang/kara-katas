# 2815. Max Pair Sum in an Array

You are given an integer array `nums`. You have to find the **maximum**
sum of a pair of numbers from `nums` such that the **largest digit** in
both numbers is equal.

Return *the **maximum** sum or* `-1` *if no such pair exists.*

```
nums = [51,71,17,24,42]  ->  88
nums = [1,2,3,4]         ->  -1
```

**Constraints:** `2 <= nums.length <= 100`; `1 <= nums[i] <= 10^4`.

## Approaches

| file | mechanism |
|---|---|
| `pair.kara` ★ | one pass, holding in a `[0; 10]` array the largest number seen for each largest digit; each number is paired with the one held for its digit before taking its place, the digit found by `% 10` and `/ 10` |
| `pair_pairs.kara` | every pair i < j, the largest digits worked out once into a `Vec` by a closure with a loop in it |
| `pair_groups.kara` | the numbers gathered into a `Map` from their largest digit, read as the greatest `char` of the number written out by an f-string; each group of two or more sorted in place through `iter_mut`, its two largest summed |
| `pair_sorted.kara` | largest first: the numbers sorted down, each digit's first number held in a `Vec[Option[i64]]` and the next with the same digit completing that digit's best pair; the digit found by recursion |
| `pair_solution.kara` | a Rust solution as LeetCode's Rust users write it, a `[0; 10]` of the best per digit, the digit by `to_string().chars().max()` and `to_digit(10)`, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 7 lines: LeetCode's two examples; two numbers whose largest digits differ; two 9999s; 1 to
100, LeetCode's longest; 3000 random arrays of 2 to 8 numbers up to 100;
and 50 of 2 to 100 numbers up to 10^4, the last two with how many have
no pair and a checksum. `pair.py` mirrors the ★ arm and its output is
byte-identical.

```
88
-1
-1
19998
197
3000 small arrays: 922 without a pair, checksum 872081787
50 large arrays: 1 without a pair, checksum 850889265
```

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every pair i < j, each number's largest digit read from the
number written out as the greatest of its digit characters, and the
best sum over the pairs whose largest digits are equal, or -1; no table
and no sort. It draws 2000 random arrays of 2 to 8 numbers up to 100,
then 50 of 2 to 100 numbers up to 10^4, all before any arm answers; the
literal reading is asked only of the first 2000.

| | property |
|---|---|
| P1 | up to 8 numbers, the answer is the literal reading's |
| P2 | -1, or the sum of two numbers of the array, at most its two largest |
| P3 | the numbers reversed: the same answer |
| P4 | the array written twice over: twice its largest number |
| P5 | every number times 10: the answer times 10, or still -1 |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2050 cases: checksum 702411105, 61500 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases gives the same checksum. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the digit's holder replaced before the pairing | P1 1943, P2 1993, P6 1993 |
| M2 | ★: the largest digit read as the last one | P1 897, P6 904 |
| M3 | pairs: a number paired with itself | P1 1943, P2 1993, P6 1993 |
| M4 | pairs: the last number never paired | P1 547, P3 748, P4 490, P6 550 |
| M5 | groups: a group's two smallest summed | P1 349, P4 877, P6 396 |
| M6 | groups: the groups keyed by the first digit | P1 897, P6 904 |
| M7 | sorted: sorted up, not down | P1 349, P4 877, P6 396 |
| M8 | sorted: a number of two or more digits read as its last | P1 1200, P5 1829, P6 1245 |
| M9 | solution: a pair made only when the newcomer is larger | P1 739, P3 1357, P4 2050, P6 765 |
| M10 | solution: the digit read by min | P1 1432, P5 1806, P6 1474 |

## Benchmarks

The bench draws 20000 arrays of 100 numbers, LeetCode's most, up to
10^4, all of them first, then answers each 10 times by the ★ arm in all
five languages. Every implementation prints `20000 arrays of 100, 10
rounds: sums total 3934836970, checksum 201518405`.

BENCHTAB

## Verification

All five arms print the same output as `pair.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The four own arms and the harness checked clean as first written.

LeetCode's Rust template took 11 `karac fix` edits in one run, the
wrapper included: `struct Solution {}` added; `Vec<..>` became
`Vec[..]`; `for &x` and `|&v|` lost their `&`; `Solution::` took `.`;
the wrapper's `as i64` went, an `i32` widening implicitly; and
`[0; 10]` became `[0i32; 10]` and `let mut ans = -1` became `let mut
ans: i32 = -1`. Those two are design.md §8 at work: `ans.max(..)` and
`best[d].max(x)` call a method on the literal's value, which settles a
literal no use has fixed yet to `i64`, where Rust would carry `i32` back
from the return; the fix writes the type the function returns. The
`to_string().chars().max().unwrap().to_digit(10).unwrap() as usize`
chain is Kāra as written.
