# 1800. Maximum Ascending Subarray Sum

Given an array of positive integers `nums`, return the largest possible
sum of an ascending subarray of `nums`. A subarray is a contiguous run
of the array, and it is ascending when each number in it is larger than
the one before; a subarray of one number is ascending.

```
nums = [10,20,30,5,10,50]       ->  65
nums = [10,20,30,40,50]         ->  150
nums = [12,17,15,13,10,11,12]   ->  33
```

**Constraints:** `1 <= nums.length <= 100` and `1 <= nums[i] <= 100`.

The arms are `fn max_ascending_sum(nums: Vec[i32]) -> i32`.

## Approaches

| file | mechanism |
|---|---|
| `max_ascending_sum.kara` ★ | one pass with the sum of the ascending run that ends here, which a number no larger than the one before starts afresh, and the best of those sums. O(n) |
| `max_ascending_sum_chunk.kara` | the ascending runs cut out with `chunk_by`, each pair inside a run rising, and the largest run's sum taken. O(n) |
| `max_ascending_sum_brute.kara` | every subarray tried: from each start, grown while it keeps rising, every prefix of that run summed. O(n^2) |
| `max_ascending_sum_fold.kara` | one `fold` carrying the best sum, the current run's and the number before, as a tuple. O(n) |
| `max_ascending_sum_solution.kara` | a Rust solution as LeetCode's Rust users write it (`nums.windows(2)`, `w[1] > w[0]`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 4 lines: LeetCode's three examples (`65 150
33`); five edges, one number, two alike, which do not ascend, numbers
falling all the way, the best run last, and a run broken by an equal
pair (`7 5 9 6 7`); the constraints' most, 100 numbers of 100, 1 to 100
rising, and 100 at random (`the most: 100 5050 224`); and 3000 random
cases of 1 to 20 numbers (`3000 random cases: checksum 251743201`).
`max_ascending_sum.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac __mir-run`,
`karac run`, `karac build` and `karac __mir-llvm-run`.

The Mend loop: the ★ and chunk arms check clean as first written. The
brute arm starts its best as `let mut best = 0;`, which check refuses
where an `i32` is returned, since the literal kept its default `i64`,
and `karac fix` annotated it `best: i32`, 1 fix. The fold arm seeds its
tuple as `(0, 0, 0)`, and check refused it twice, the branches `run + x`
and `x` meeting as an `i64` and a `ref i32`, and the best returned as an
`i64`; `karac fix` wrote `(0i32, 0i32, 0)`, 2 fixes. The Rust solution
takes one round of 6 fixes by `karac fix`'s count, and its diff is:
`struct Solution;` to `struct Solution {}`, `Vec<i32>` to `Vec[i32]` in
both signatures, and `Solution::` to `Solution.`. Its `nums.windows(2)`
and `w[1] > w[0]` stay. Every arm's output matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every subarray from `i` to `j`, kept when each number in it
is larger than the one before, its sum found afresh, and the largest
kept. LeetCode's examples, the edges, the constraints' most, 100 down to
1 falling, and 1988 random cases of 1 to 30 numbers. Each arm meets six
properties on each case:

| property | what it checks |
|---|---|
| P1 | the statement read literally |
| P2 | the first number written twice, which does not ascend, gives the same answer |
| P3 | every number doubled doubles the answer |
| P4 | every number one larger keeps the same runs, so raises the answer by at least 1 and at most the count of numbers |
| P5 | the answer lies between the largest number and the sum of all of them |
| P6 | the ★ arm's answer |

P4 was first written as "the numbers twice over with a 1 between give
the same answer", which is wrong: the 1 starts a run, and the second
copy's first number rises from it, so the run that opens the array, once
more and with a 1 in front, can beat the answer. Every arm failed it,
and it was replaced. All 60,000 checks pass on every arm: `2000 cases:
checksum 30584670, 60000 checks over 5 arms: 0 failures`, under `karac
__mir-run`, `karac run`, `karac build` and `karac __mir-llvm-run`.
Python, running the ★ arm's mirror over the same cases, gives the same
checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: an equal number taken as ascending | P1 801, P2 838, P6 3204 |
| M2 | ★: a run never started afresh | P1 1704, P6 6816 |
| M3 | chunk: an equal pair kept in one run | P1 801, P2 838, P6 801 |
| M4 | chunk: the smallest run's sum taken | P1 1825, P2 385, P5 1769, P6 1825 |
| M5 | brute: each number compared with the run's first, not the one before | P1 1586, P6 1586 |
| M6 | brute: a run longer than one never scored | P1 1788, P6 1788 |
| M7 | fold: a run started afresh at 0, the number that starts it dropped | P1 1495, P2 396, P6 1495 |
| M8 | fold: the number before never moved on | P1 1895, P2 2000, P6 1895 |
| M9 | solution: a rise of 1 taken as a break | P1 661, P3 661, P6 661 |
| M10 | solution: a fresh run started from the number before | P1 1494, P6 1494 |

## Benchmarks

The bench builds 4000 random lists of 100 numbers from 1 to 100 once,
and makes 400000 calls of the ★ arm, each list drawn from the checksum
so far. It checks clean as first written. Every implementation prints
`400000 calls over 4000 lists of 100 numbers: checksum 703158038`.

BENCHTAB

Measured by hand, best of three on a machine shared with a test run,
Kāra takes 0.21 s against Rust's 0.06 s (0.18 s with overflow checks
on), C's 0.05 s and Go's 0.22 s; Python takes 3.2 s.
