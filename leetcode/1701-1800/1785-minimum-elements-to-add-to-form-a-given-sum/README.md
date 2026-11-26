# 1785. Minimum Elements to Add to Form a Given Sum

You are given an integer array `nums` and two integers `limit` and
`goal`. Every element of `nums` satisfies `abs(nums[i]) <= limit`.
Return the minimum number of elements you need to add to make the sum of
the array equal to `goal`, while every element, old or new, keeps
`abs(x) <= limit`.

```
nums = [1, -1, 1],     limit = 3,   goal = -4  ->  2
nums = [1, -10, 9, 1], limit = 100, goal = 0   ->  1
```

**Constraints:** `1 <= nums.length <= 10^5`, `1 <= limit <= 10^6`,
`-limit <= nums[i] <= limit`, and `-10^9 <= goal <= 10^9`.

The arms are `fn min_elements(nums: Vec[i32], limit: i32, goal: i32) ->
i32`.

## Approaches

| file | mechanism |
|---|---|
| `min_elements.kara` ★ | each element added closes the gap between the sum and the goal by at most the limit, and the last can close whatever is left, so the answer is the gap over the limit rounded up, `(gap + limit - 1) / limit`. The sum is an `i64`, since 10^5 numbers up to 10^6 pass `i32`. O(n) |
| `min_elements_divmod.kara` | the sum by a loop, the gap divided by the limit, and one more element when there is a remainder. O(n) |
| `min_elements_fold.kara` | the numbers folded off the goal from an `i64` start, a gap of 0 needing nothing, else `(gap - 1) / limit + 1`. O(n) |
| `min_elements_float.kara` | the gap over the limit as an `f64`, rounded up with `ceil`; the gap is below 2^53 and a quotient's fraction is at least one over the limit, so the rounding is exact. O(n) |
| `min_elements_solution.kara` | a Rust solution as LeetCode's Rust users write it (`struct Solution;`, `Vec<i32>`, `.map(\|&x\| x as i64)`, the `i32`s cast to `i64` by hand), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 4 lines: LeetCode's two examples (`2 1`); five
edges, the goal met already, a gap that is a multiple of the limit, one
more than a multiple, a goal below the sum, and a limit of 1 with a goal
of 10^9 (`0 2 3 2 999999999`); the constraints' most, 100000 numbers at
the limit of 10^6 with a goal of -10^9, 100000 random numbers under a
limit of 1 with a goal of 10^9, and 100000 random numbers under the
largest limit with the least goal (`the most: 101000 999999944 1262`);
and 3000 random cases of 1 to 20 numbers, a limit of 1 to 10 and a goal
within 100 of 0 (`3000 random cases: checksum 254735798`).
`min_elements.py` mirrors the ★ arm, and its output is byte-identical.
Every arm gives the same output under `karac __mir-run`, `karac run`,
`karac build` and `karac __mir-llvm-run`.

The Mend loop: the divmod arm and the harness check clean as first
written. The ★ arm was first written with Rust's casts, `goal as
i64 - sum` and `limit as i64` twice; `karac fix` drops all three, 3
fixes, since an `i32` widens to `i64` implicitly. The fold arm loses `x
as i64` and `limit as i64` the same way, 2 fixes, and the float arm its
`goal as i64`, 1 fix. The `x as i64` in `.map(|x| x as i64)` stays in
each arm: it is what makes the sum an `i64`. The Rust solution takes one
round of 10 fixes by `karac fix`'s count, and its diff is: `struct
Solution;` to `struct Solution {}`, `Vec<i32>` to `Vec[i32]`, `|&x|` to
`|x|`, the three casts dropped, and `Solution::` to `Solution.`. Every
arm's output matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: `k` added elements, each from `-limit` to `limit`, can make
any sum from `-k * limit` to `k * limit`, so the least `k` whose range
reaches what the goal still needs, counted up from 0. LeetCode's
examples, six edges (the five above with a goal of 1000 in place of
10^9, and `[-3, -3]` with a limit and goal of 3), and 1992 random cases
of 1 to 12 numbers, a limit of 1 to 8 and a goal within 60 of 0. Each
arm meets six properties on each case:

| property | what it checks |
|---|---|
| P1 | the statement read literally |
| P2 | 0 exactly when the sum is the goal, and never more elements than the gap |
| P3 | the numbers in reverse give the same answer |
| P4 | every number and the goal negated give the same answer |
| P5 | the goal moved one limit further from the sum needs one more element |
| P6 | the ★ arm's answer |

The differential checks clean as first written. All 60,000 checks pass
on every arm: `2000 cases: checksum 173299060, 60000 checks over 5 arms:
0 failures`, under `karac __mir-run`, `karac run`, `karac build` and
`karac __mir-llvm-run`. Python, counting `k` up as the literal reading
does, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: one element too many when the gap is a multiple of the limit | P1 668, P2 254, P6 2672 |
| M2 | ★: the gap's sign kept | P1 988, P2 110, P4 1989, P5 988, P6 3952 |
| M3 | divmod: a remainder needing no element | P1 1332, P2 114, P6 1332 |
| M4 | divmod: each number's size summed in place of the number | P1 1682, P2 241, P4 1908, P5 257, P6 1682 |
| M5 | fold: one element too many when the gap is a multiple of the limit | P1 657, P2 243, P5 11, P6 657 |
| M6 | fold: the numbers added to the goal, not taken from it | P1 1681, P2 197, P5 166, P6 1681 |
| M7 | float: the quotient rounded down | P1 1332, P2 114, P6 1332 |
| M8 | float: the quotient rounded to the nearest | P1 529, P2 45, P6 529 |
| M9 | solution: the gap divided by one more than the limit | P1 1633, P2 31, P5 452, P6 1633 |
| M10 | solution: the gap taken as the goal's size less the sum's | P1 958, P2 131, P5 90, P6 958 |

## Benchmarks

The bench builds 4000 lists of 100 random numbers from -10^6 to 10^6
once and makes 6000000 calls of the ★ arm, each list, limit and goal
drawn from the checksum so far. It checks clean as first written. Every
implementation prints `6000000 calls over 4000 lists: checksum
824043713`.

BENCHTAB

Measured by hand, best of three on a machine shared with a test run,
Kāra takes 0.48 s against Rust's 0.41 s (0.48 s with overflow checks
on), C's 0.32 s and Go's 0.47 s; Python takes 8.0 s.
