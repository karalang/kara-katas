# 1760. Minimum Limit of Balls in a Bag

You are given an integer array `nums` where the `i`th bag contains
`nums[i]` balls. You are also given an integer `maxOperations`. You can
perform the following operation at most `maxOperations` times: take any
bag of balls and divide it into two new bags with a positive number of
balls. Your penalty is the maximum number of balls in a bag. You want to
minimize your penalty after the operations. Return the minimum possible
penalty after performing the operations.

```
nums = [9], maxOperations = 2           ->  3
nums = [2,4,8,2], maxOperations = 4     ->  2
```

**Constraints:** `1 <= nums.length <= 10^5` and `1 <= maxOperations,
nums[i] <= 10^9`.

The arms are `fn minimum_size(nums: Vec[i32], max_operations: i32) ->
i32`.

## Approaches

To leave no bag above `p`, a bag of `x` balls needs `(x - 1) / p`
divisions and no fewer, and that count only falls as `p` grows, so the
answer is the least `p` whose total fits the operations.

| file | mechanism |
|---|---|
| `minimum_size.kara` ★ | a binary search on the penalty from 1 to the largest bag, each step summing `(x - 1) / p` over the bags. O(n log m) |
| `minimum_size_bits.kara` | the largest penalty that needs too many operations built bit by bit from the top, through a closure over the bags, and the answer one more. O(n log m) |
| `minimum_size_grouped.kara` | the bags sorted and grouped by size, each size's divisions counted once and multiplied by how many bags have it, inside the binary search. O(n log n + k log m) |
| `minimum_size_recursive.kara` | the binary search written as a recursion on the penalties still open, each test stopping as soon as the operations run out. O(n log m) |
| `minimum_size_solution.kara` | a Rust solution as LeetCode's Rust users write it (`let (mut left, mut right) = (1, *nums.iter().max().unwrap())`, `.map(\|&x\| ..)`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 4 lines: LeetCode's two examples (`3 2`); six
edges, no operation needed, one ball, enough operations to make every
ball its own bag, one operation short of that, bags all the same, and
the largest bag alone (`1 1 1 2 4 500000000`); the constraints' most,
100000 bags of up to 1000000000 balls with 1, 100000 and 1000000000
operations (`100000 bags: 999975341 321340360 46873`); and 3000 random
cases of 1 to 20 bags of 1 to 60 balls (`3000 random cases: checksum
597412859`). `minimum_size.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac __mir-run`,
`karac run`, `karac build` and `karac __mir-llvm-run`.

The Mend loop: the bits and recursive arms check clean as first written.
The ★ arm's `let mut lo = 1;` took 1 fix, to `let mut lo: i32 = 1;`,
since `lo` meets the `i32` largest bag in `mid` and `mid` is stored back
in `hi`. The grouped arm took 2 fixes, two `as i64` casts dropped. The
Rust solution takes one round of 12 fixes by `karac fix`'s count, and
its diff is: `struct Solution;` to `struct Solution {}`, `Vec<i32>` to
`Vec[i32]` twice, `let (mut left, mut right) = (1, ..)` to `let mut
(left, right) = (1i32, ..)`, `|&x|` to `|x|`, `max_operations as i64` to
`max_operations`, and `Solution::` to `Solution.`. Every arm's output
matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: for each penalty from 1 up, the fewest divisions that leave
every part of each bag at most that penalty, every division of a bag
into two tried (memoized), and the first penalty whose total fits.
LeetCode's examples, the edges, and 1993 random cases of 1 to 8 bags of
1 to 30 balls with 1 to 20 operations. Each arm meets six properties on
each case:

| property | what it checks |
|---|---|
| P1 | the statement read literally |
| P2 | the bags in reverse order give the same |
| P3 | one more operation gives no more |
| P4 | a bag of one ball more changes nothing |
| P5 | no more than the largest bag, and at least the balls shared out evenly over the most bags there can be |
| P6 | the ★ arm's answer |

All 60,000 checks pass on every arm: `2000 cases: checksum 680427002,
60000 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and `karac __mir-llvm-run`. Python, trying every
division with `lru_cache`, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: a bag of x balls counted x / p operations, not (x - 1) / p | P1 733, P4 11, P6 2932 |
| M2 | ★: a penalty that uses every operation refused | P1 844, P6 3376 |
| M3 | bits: the lowest bit never set | P1 983, P5 472, P6 983 |
| M4 | bits: a penalty that uses every operation counted as too many | P1 844, P6 844 |
| M5 | grouped: each repeat of a size counted twice | P1 266, P6 266 |
| M6 | grouped: the search capped at the smallest bag | P1 988, P4 1607, P5 920, P6 988 |
| M7 | recursive: a penalty that uses every operation refused | P1 844, P6 844 |
| M8 | recursive: the lower of two penalties left taken untried | P1 905, P5 428, P6 905 |
| M9 | solution: the search's top moved below a penalty that fits | P1 857, P5 386, P6 857 |
| M10 | solution: the search started at a penalty of 2 | P1 129, P5 12, P6 129 |

## Benchmarks

The bench keeps one list of 100000 bags of up to 1000000000 balls and
makes 100 calls of the ★ arm, each with a number of operations from 1 to
1000000000 chosen from the checksum so far and first changing one bag,
so each call is about 30 rounds of 100000 divisions. Every
implementation prints `100 calls over 100000 bags: checksum 463783612`.

BENCHTAB

Measured by hand, best of three on a machine shared with a test run,
Kāra takes 0.83 s against Rust's 0.82 s (0.74 s with overflow checks
on), C's 0.77 s and Go's 1.2 s; Python takes 19.5 s.
