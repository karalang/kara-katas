# 1300. Sum of Mutated Array Closest to Target

Given an integer array `arr` and a target value `target`, return the
integer `value` such that when we change all the integers larger than
`value` in the given array to be equal to `value`, the sum of the array
gets as close as possible (in absolute difference) to `target`.

In case of a tie, return the minimum such integer.

Notice that the answer is not necessarily a number from `arr`.

```
arr = [4,9,3], target = 10                                ->  3
arr = [2,3,5], target = 10                                ->  5
arr = [60864,25176,27249,21296,20204], target = 56803     ->  11361
```

**Constraints:** `1 <= arr.length <= 10^4`, `1 <= arr[i], target <=
10^5`.

The arms are `fn find_best_value(arr: Vec[i64], target: i64) -> i64`.

## Approaches

The capped sum only grows with the cap, and stops growing at the largest
number, so the answer is never past it; it can be 0, when a target of 1
is as close to 0 as to the array's length.

| file | mechanism |
|---|---|
| `find_best_value.kara` ★ | the numbers sorted and walked from the smallest with the sum of those passed; at the first number that, as the cap of it and everything after it, brings the sum to the target or past it, the best cap is the target's share of what is left, rounded down or up, whichever sum is closer, the smaller on a tie; past every number, the largest. O(n log n) |
| `find_best_value_binary.kara` | a binary search for the smallest cap whose sum reaches the target, or the largest number, each try summing the array; the answer is it or the cap one below, whichever sum is closer. O(n log max) |
| `find_best_value_down.kara` | the numbers sorted from the largest, and the cap brought down through them, one number at a time joining those held at the cap; once the cap at the next number down would bring the sum to the target or below, the best cap is the target's share for the capped numbers, rounded down or up. O(n log n) |
| `find_best_value_every.kara` | each cap from 0 to the largest number tried in turn, its sum kept in O(1) from running totals over a count of each value, the first with the least distance kept. O(n + max) |
| `find_best_value_solution.kara` | a Rust solution as LeetCode's Rust users write it (a binary search between 0 and `*arr.iter().max().unwrap()`, a `sum` closure over `a.min(v)`, then `.abs()` comparing the cap found with the one below), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 2 lines: LeetCode's three examples, a target
past the whole sum, a target of 1 over two numbers (a tie between 0 and
1), and a cap that lands exactly (`3 5 11361 3 0 6`); then 900 random
arrays of 1 to 200 numbers up to 10, 1000 or `10^5`, with targets up to
`10^5` (`900 random arrays: values total 476381, checksum 150350185`).
`find_best_value.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac __mir-run`,
`karac run` and `karac __mir-llvm-run`. The every-cap arm takes about 20
s under `karac __mir-run`, a step for each cap up to `10^5` on a third of
the arrays, which is why there are 900 of them.

The Mend loop: the four Kāra arms checked clean as first written. The
Rust arm takes one round of 13 fixes by `karac fix`'s count, from 8
errors: `struct Solution;` to `struct Solution {}`, `Vec<..>` to
`Vec[..]`, `let (mut lo, mut hi) = (0, ..)` to `let mut (lo, hi) =
(0i32, ..)`, the closure `|v: i32| -> i32 { .. }` to `let sum: Fn(i32)
-> i32 = |v: i32| { .. }`, `|&a|` to `|a|`, `::` to `.`, and the
wrapper's `|&x|` to `|x|` and its `as i64` dropped as a widening. Its
output matches on the first run. No gap was met.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every value from 0 to the largest number, the array copied
with each number larger than the value changed to it and summed, and the
closest sum kept, the first on a tie. 2000 arrays of 1 to 8 numbers in
four kinds, 500 each: numbers up to 5 with a target up to a little past
the sum, so that ties are common; numbers up to 50; one number
throughout; and a target below the length or past the sum. Every array,
target and raise is drawn before any arm answers.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the array reversed: the same answer |
| P3 | every number twice and the target doubled: the same answer |
| P4 | the target raised: an answer no smaller |
| P5 | the array changed by its own answer: the same answer |
| P6 | the ★ arm's answer |

All 60,000 checks pass on every arm: `2000 arrays: checksum 960644796,
60000 checks over 5 arms: 0 failures`, under `karac __mir-run` and
`karac __mir-llvm-run`. Python gives the same checksum.

## Mutation testing

Ten edits to the differential, two to each arm, each run under both
`karac __mir-llvm-run` and `karac __mir-run`. Every one is killed, fails
the same way under both backends and not by a crash, and no two fail the
same checks, so all ten are kept.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a tie going to the larger cap | P1 233, P6 932 |
| M2 | ★: the smallest number returned past every number | P1 283, P4 182, P5 119, P6 1132 |
| M3 | binary: the search stopped a step short | P1 777, P5 803, P6 777 |
| M4 | binary: the cap above compared, not the one below | P1 597, P6 597 |
| M5 | pull-down: the share only rounded down | P1 364, P6 364 |
| M6 | pull-down: the cap never brought below the smallest number | P1 843, P6 843 |
| M7 | every cap: the numbers below the cap counted, not summed | P1 571, P4 52, P6 571 |
| M8 | every cap: the largest number never tried | P1 536, P5 1768, P6 536 |
| M9 | solution: each number raised to the cap, not lowered | P1 1967, P5 1725, P6 1967 |
| M10 | solution: the search bounded by the smallest number | P1 707, P6 707 |

P1 and P6 kill all ten, P5 four and P4 two; P2 and P3 kill none. Every
arm sorts, counts or sums, so the order of the array (P2) cannot reach
an edit, and every edit here measures distances that double with the
array and the target (P3). Changing the array by its own answer (P5)
makes the answer its largest number, so it sees the edits that treat the
largest number or the top of the search specially (M2, M3, M8), and M9,
whose answers are wrong almost everywhere. Raising the
target (P4) sees M2, whose answer drops to the smallest number once the
target passes the sum, and M7, whose wrong sums need not grow with the
cap.

## Benchmarks

The bench builds 50 arrays of `10^4` numbers, the constraints' longest,
up to 20, 100, 1000, `10^4` and `10^5` in turn, so that the answer lands
anywhere from inside the numbers to below the smallest, once from its own
generator; then makes 200 passes, each setting one number of every array
and a target up to `10^5` from the checksum so far, so no answer carries
over, answering it with the ★ arm and folding the answer plus the pass
into the checksum. Each call sorts a fresh copy: `sort` in Kāra and Rust,
`slices.Sort` in Go, `sorted` in Python, and `qsort` in C. Every
implementation prints `200 passes over 50 arrays of 10^4: checksum
104992289`.

BENCHTAB
