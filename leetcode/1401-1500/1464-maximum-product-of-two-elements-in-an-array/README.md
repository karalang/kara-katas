# 1464. Maximum Product of Two Elements in an Array

Given the array of integers `nums`, you will choose two different
indices `i` and `j` of that array. Return the maximum value of
`(nums[i]-1)*(nums[j]-1)`.

```
nums = [3,4,5,2]   ->  12
nums = [1,5,4,5]   ->  16
nums = [3,7]       ->  12
```

**Constraints:** `2 <= nums.length <= 500` and `1 <= nums[i] <= 10^3`.

The arms are `fn max_product(nums: Vec[i32]) -> i32`.

## Approaches

| file | mechanism |
|---|---|
| `max_product.kara` ★ | every value is at least 1, so the product grows with each factor and is the two largest values' own: one pass keeping the largest so far and the next, a value above the largest pushing it down to the next. O(n) |
| `max_product_sort.kara` | a clone sorted, and the last two values taken. O(n log n) |
| `max_product_pairs.kara` | every pair of places once, the second after the first, by `(0..n).flat_map(\|i\| (i + 1..n).map(\|j\| ..))`, and the largest product by `.max().unwrap()`. O(n^2) |
| `max_product_heap.kara` | a `PriorityQueue[i32]` made largest-first by `PriorityQueue.max_first_from(nums.iter().collect())`, popped twice. O(n log n) |
| `max_product_solution.kara` | a Rust solution as LeetCode's Rust users write it (`nums` taken as a `mut` parameter, sorted in place by `sort_unstable` and the last two read through `nums.len()`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 3 lines: LeetCode's three examples and four
more, two 1s, two of the most, the largest value once among 1s, and 500
values of 1000 (`12 16 12 0 998001 0 998001`); the constraints' most,
500 values from 1 to 1000 (`500 values: 995006`); and 3000 random arrays
of 2 to 60 values from 1 to top, top from 2 to 1000 (`3000 random
arrays: total 849446388, checksum 819499012`). `max_product.py` mirrors
the ★ arm, and its output is byte-identical. Every arm gives the same
output under `karac __mir-run`, `karac run`, `karac build` and `karac
__mir-llvm-run`.

The Mend loop: the ★ and sort arms check clean as first written. The
pairs arm, written with Rust's `move |j|` on the inner closure, takes
one fix by `karac fix`, the `move` deleted: Kāra infers a closure's
captures. The heap arm, written with Rust's `BinaryHeap[i32]` filled by
`collect`, takes two: the type renamed to `PriorityQueue`, and, since
Kāra's queue pops the smallest first where Rust's heap pops the largest,
the `collect` wrapped in `PriorityQueue.max_first_from(..)`, which keeps
the order. The Rust solution takes one round of 8 fixes by `karac fix`'s
count: `struct Solution;` to `struct Solution {}`, `Vec<i32>` to
`Vec[i32]`, the `mut nums: Vec<i32>` parameter to `nums: own Vec[i32]`
with `let mut nums = nums;` at the body's start, `sort_unstable` to
`sort`, and `Solution::max_product` to `Solution.max_product`; the
parameter's `own` carries to the harness's `max_product` that calls the
method. Every arm's output matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every two different indices in either order, and the largest
product among them. LeetCode's examples, six edge cases (two 1s, two of
the most, the largest once among 1s, and the two largest first, last and
apart), 500 values of 1000, the constraints' most, and 1992 random
arrays, half of 2 to 6 values and half of 2 to 60, from 1 to top, top
from 1 to 1000.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | `nums` reversed gives the same answer |
| P3 | `nums` shuffled gives the same answer |
| P4 | a 1 more gives the same answer |
| P5 | the answer is the largest value less 1 times a number from 0 to that: at most its square and, past 1, a multiple of it |
| P6 | the ★ arm's answer |

All 60,090 checks pass on every arm: `2003 cases: checksum 208289653,
60090 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and `karac __mir-llvm-run`. Python, sorting each
array, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: the largest so far never pushed down to second | P1 915, P2 1883, P3 1126, P4 158, P5 158, P6 3660 |
| M2 | ★: second taken only above the largest | P1 1055, P2 1974, P3 1332, P5 379, P6 4220 |
| M3 | sort: the values never sorted | P1 1635, P2 1759, P3 1629, P4 1974, P5 1286, P6 1635 |
| M4 | sort: the smallest taken for the second largest | P1 1764, P4 1855, P6 1764 |
| M5 | pairs: each pair's first value squared | P1 1942, P2 723, P3 462, P4 352, P5 349, P6 1942 |
| M6 | pairs: two taken off the second value of each pair | P1 1998, P2 1923, P3 973, P5 943, P6 1998 |
| M7 | heap: the largest taken for both | P1 1944, P6 1944 |
| M8 | heap: a min-first heap, so the two smallest taken | P1 1764, P4 1855, P5 1612, P6 1764 |
| M9 | solution: `nums` never sorted | P1 1635, P2 1759, P3 1629, P4 1974, P5 1286, P6 1635 |
| M10 | solution: 1 taken off the product, not each factor | P1 2002, P5 1998, P6 2002 |

## Benchmarks

The bench draws 1000 arrays of 500 values from 1 to 1000, the
constraints' most, once; then makes 100 passes, each setting one value
of every array to a value chosen from the checksum so far, so no answer
carries over, answering it with the ★ arm and folding the answer into
the checksum. Every implementation makes the same single pass. Every
implementation prints `100 passes over 1000 arrays of 500 values:
checksum 203092597`.

BENCHTAB

Measured by hand, best of three on a machine shared with a test run,
Kāra takes 0.08 s against Rust's 0.06 s (0.06 s with overflow checks
on), C's 0.06 s and Go's 0.09 s; Python takes 2.0 s.
