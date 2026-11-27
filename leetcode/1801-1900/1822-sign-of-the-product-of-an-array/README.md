# 1822. Sign of the Product of an Array

There is a function `signFunc(x)` that returns `1` if `x` is positive,
`-1` if `x` is negative, and `0` if `x` is equal to `0`. You are given
an integer array `nums`. Let `product` be the product of all values in
the array `nums`. Return `signFunc(product)`.

```
nums = [-1,-2,-3,-4,3,2,1]  ->   1
nums = [1,5,0,2,-3]         ->   0
nums = [-1,1,-1,1,-1]       ->  -1
```

**Constraints:** `1 <= nums.length <= 1000`, `-100 <= nums[i] <= 100`.

The arms are `fn array_sign(nums: Vec[i64]) -> i64`.

## Approaches

| file | mechanism |
|---|---|
| `array_sign.kara` ★ | the product is never formed: a zero makes it zero, and otherwise each negative number flips its sign. O(n) |
| `array_sign_fold.kara` | the signs multiplied in place of the numbers: `signum` folded over the list by `*`, which stays in -1, 0 and 1. O(n) |
| `array_sign_count.kara` | two questions of the list: whether it holds a zero, by `contains`, and whether it holds an odd number of negatives, by `filter` and `count`. O(n) |
| `array_sign_match.kara` | the ★ arm's walk as a `match` on each number's `cmp` against zero, with the sign held as a `bool` for "negative so far". O(n) |
| `array_sign_solution.kara` | a Rust solution as LeetCode's Rust users write it (`nums.iter().map(\|x\| x.signum()).product()`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 4 lines: LeetCode's three examples; six edges,
one number of each sign, the values at their ends, and a zero after the
negatives (`1 -1 0 -1 -1 0`); the constraints' most, 1000 numbers of
-100, whose product no integer type holds, and 999 of them with a 1
(`the most: 1 -1`); and 3000 random cases of 1 to 12 numbers from -100
to 100, one number in 30 made a zero (`3000 random cases: 1164 negative,
654 zero, 1182 positive, checksum 641044764`). `array_sign.py` mirrors
the ★ arm, and its output is byte-identical. Every arm gives the same
output under `karac __mir-run`, `karac run`, `karac build` and `karac
__mir-llvm-run`.

The Mend loop: every arm and the harness check clean as first written.
The harness's random cases were first written with a zero rarer than the
other values, and only 18 of the 3000 came out zero; one number in 30 is
now made a zero. The Rust solution takes 15 fixes by `karac fix`'s
count, and its diff is: `struct Solution {}` added above the `impl`;
`Vec<i32>` to `Vec[i32]`; and `Solution::` to `Solution.` at the
harness's 12 calls. `nums.iter().map(|x| x.signum()).product()` is Kāra
as it stands. The solution takes a `Vec[i32]`, so its harness builds its
lists as `Vec[i32]`. Every arm's output matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the product formed, in an `i128`, which holds 10 numbers of
at most 100, and `signFunc` of it. It runs 2000 random cases of 1 to 10
numbers from -100 to 100, one number in 20 made a zero. Each arm meets
six properties on each case:

| property | what it checks |
|---|---|
| P1 | the statement read literally |
| P2 | the answer is -1, 0 or 1 |
| P3 | the numbers in reverse order give the same sign |
| P4 | every number negated flips the sign once for each number |
| P5 | a -1 more flips the sign |
| P6 | the ★ arm's answer |

Check warned that `product *= x as i128` widens an `i64` to `i128` with
a cast it does not need, and `karac fix` wrote `product *= x`, 1 fix.
All 60,000 checks pass on every arm: `2000 cases: checksum 719745797,
60000 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and `karac __mir-llvm-run`. Python, over the same
cases, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: a -1 never flips the sign | P1 41, P4 70, P5 1498, P6 164 |
| M2 | ★: a zero answered as positive | P1 502, P4 246, P5 502, P6 2008 |
| M3 | fold: every sign taken as positive | P1 745, P4 772, P5 1498, P6 745 |
| M4 | fold: the product started at -1 | P1 1498, P6 1498 |
| M5 | count: the parity read the wrong way round | P1 1498, P6 1498 |
| M6 | count: the zero never looked for | P1 502, P4 433, P6 502 |
| M7 | match: a negative sets the sign, not flips it | P1 597, P4 637, P5 1342, P6 597 |
| M8 | match: a zero passed over | P1 502, P4 433, P6 502 |
| M9 | solution: the first number left out | P1 850, P3 869, P4 1596, P6 850 |
| M10 | solution: a negative's sign taken as zero | P1 1342, P4 321, P5 156, P6 1342 |

## Benchmarks

The bench builds one list of 2000 numbers from -100 to 100, none of them
zero, once and makes 300000 calls of the ★ arm on runs of 500 to 999 of
its numbers, each run's start and length drawn from the checksum so far.
Each call copies its run, as the arm takes its list by value, and walks
all of it. It checks clean as first written. Every implementation prints
`300000 calls: checksum 253458671`.

BENCHTAB

Measured by hand, best of three on a machine shared with a test run,
Kāra takes 0.26 s against Rust's 0.26 s (0.26 s with
overflow checks on), C's 0.26 s and Go's 0.74 s; Python takes 9.4 s.
