# 1480. Running Sum of 1d Array

Given an array `nums`. We define a running sum of an array as
`runningSum[i] = sum(nums[0]...nums[i])`.

Return the running sum of `nums`.

```
nums = [1,2,3,4]     ->  [1,3,6,10]
nums = [1,1,1,1,1]   ->  [1,2,3,4,5]
nums = [3,1,2,10,1]  ->  [3,4,6,16,17]
```

**Constraints:** `1 <= nums.length <= 1000` and `-10^6 <= nums[i] <=
10^6`.

The arms are `fn running_sum(nums: Vec[i32]) -> Vec[i32]`.

## Approaches

| file | mechanism |
|---|---|
| `running_sum.kara` ★ | one pass, each sum the one before it and the value at its place, pushed to a new list. O(n) |
| `running_sum_scan.kara` | `nums.iter().scan(0i32, \|sum, x\| { let sum = sum + x; Some((sum, sum)) })`, the iterator that carries a state from item to item. O(n) |
| `running_sum_in_place.kara` | in place: the list taken over, `nums: own Vec[i32]`, and each place from the second on given the sum so far by adding the place before it. O(n), no second list |
| `running_sum_fold.kara` | `fold` over the values, the list of sums carried along and each new sum the last one, `sums.last() ?? 0`, and the value. O(n) |
| `running_sum_solution.kara` | a Rust solution as LeetCode's Rust users write it (`mut nums: Vec<i32>`, `nums[i] += nums[i - 1]`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 7 lines: LeetCode's three examples; one value;
signs that cancel; the sums at the constraints' most, 1000 values of
10^6, of -10^6, and both in turn (`1000 values: 1000000000 -1000000000
1000000 0`); and 3000 random arrays of 1 to 1000 values from -top to
top, top from 0 to 10^6, each sum folded into a checksum (`3000 random
arrays: 1491745 sums, checksum 298883017`). `running_sum.py` mirrors the
★ arm, and its output is byte-identical. Every arm gives the same output
under `karac __mir-run`, `karac run`, `karac build` and `karac
__mir-llvm-run`.

The Mend loop: the in-place and fold arms check clean as first written.
The ★ arm was first written `let mut sum = 0;`, and check refused
`sums.push(sum)`: "`sum` is an 'i64' because its literal kept the
default, since an operator or a method does not fix a literal's type;
declare it `sum: i32`", which `karac fix` wrote. The scan arm was first
written as Rust's `scan` is, `|sum, x| { *sum += x; Some(*sum) }`, and
check said Kāra's `scan` closure takes the state by value and returns
`Some((next_state, item))`; `karac fix` wrote the closure that way and
the start `0i32`, 2 fixes. The Rust solution takes one round of 8 fixes
by `karac fix`'s count, and its diff is: `struct Solution;` to `struct
Solution {}`, Rust's `mut nums: Vec<i32>` to `nums: own Vec[i32]` and
`let mut nums = nums;` at the body's start, each `Vec<i32>` to
`Vec[i32]`, and the wrapper's parameter to `own` as well, since it hands
the list on. Every arm's output matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: `runningSum[i] = sum(nums[0]...nums[i])`, each one added up
afresh. LeetCode's examples, the edges, and 1992 random arrays, half of
1 to 10 values from -5 to 5 and half of 1 to 200 values from -top to
top, top from 0 to 10^6. Each arm meets six properties on each case:

| property | what it checks |
|---|---|
| P1 | the statement read literally |
| P2 | each sum less the one before it is the value at its place |
| P3 | every value negated negates every sum |
| P4 | the first half alone has the first half of the sums |
| P5 | the last sum is the whole array's total |
| P6 | the ★ arm's answer |

All 60,000 checks pass on every arm: `2000 cases: checksum 176229478,
60000 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and `karac __mir-llvm-run`. Python, adding up each
slice by `sum`, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: each sum pushed before its own value is added | P1 1992, P2 1992, P5 1896, P6 7968 |
| M2 | ★: the sums start from 1 | P1 2000, P2 2000, P3 2000, P5 2000, P6 8000 |
| M3 | scan: each value handed on, not the sum | P1 1896, P2 1896, P5 1851, P6 1896 |
| M4 | scan: the sums start from 1 | P1 2000, P2 2000, P3 2000, P5 2000, P6 2000 |
| M5 | in place: the second value never added to | P1 1843, P2 1843, P5 1843, P6 1843 |
| M6 | in place: each place copies the one before it | P1 1893, P2 1893, P5 1843, P6 1893 |
| M7 | fold: each value added to the first sum, not the last | P1 1763, P2 1763, P5 1720, P6 1763 |
| M8 | fold: each value pushed alone | P1 1896, P2 1896, P5 1851, P6 1896 |
| M9 | solution: the last value never added to | P1 1851, P2 1851, P4 1608, P5 1851, P6 1851 |
| M10 | solution: each place less the one before it | P1 1896, P2 1896, P5 1850, P6 1896 |

## Benchmarks

The bench makes 1000 arrays of 1000 values from -10^6 to 10^6 once; then
makes 200 passes, each punching one value of every array, chosen from
the checksum so far, and taking its running sums with the ★ arm, each
sum weighted by its place in the checksum. The C mirror writes into one
`malloc`ed array per call, Rust and Kāra grow a `Vec` by `push`, and Go
`append`s to a nil slice. Every implementation prints `200 passes over
1000 arrays of 1000 values: checksum 467289863`.

BENCHTAB

Measured by hand, best of three on a machine shared with a test run,
Kāra takes 0.32 s against Rust's 0.29 s (0.41 s with overflow checks
on), C's 0.17 s and Go's 1.6 s; Python takes 26.8 s.
