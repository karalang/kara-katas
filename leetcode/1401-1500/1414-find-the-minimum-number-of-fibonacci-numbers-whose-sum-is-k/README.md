# 1414. Find the Minimum Number of Fibonacci Numbers Whose Sum Is K

Given an integer `k`, return the minimum number of Fibonacci numbers
whose sum is equal to `k`. The same Fibonacci number can be used
multiple times. The Fibonacci numbers are defined as `F1 = 1`, `F2 = 1`,
`Fn = Fn-1 + Fn-2` for `n > 2`. It is guaranteed that for the given
constraints we can always find such Fibonacci numbers that sum up to
`k`.

```
k = 7   ->  2    (2 + 5)
k = 10  ->  2    (2 + 8)
k = 19  ->  3    (1 + 5 + 13)
```

**Constraints:** `1 <= k <= 10^9`.

Each arm is `fn find_min_fibonacci_numbers(k: i32) -> i32`. Taking the
largest Fibonacci number within what is left, each time, gives a
shortest sum, the sum Zeckendorf's theorem makes unique among those with
no two neighbours.

## Approaches

| file | mechanism |
|---|---|
| `find_min_fibonacci_numbers.kara` ★ | the Fibonacci numbers up to k in a `Vec`, grown while the next stays within k (tested as `last <= k - before` so no sum passes `i32`), then walked from the top, each that fits taken. O(log k) |
| `find_min_fibonacci_numbers_recursive.kara` | none for 0, and otherwise one more than for what is left once the largest Fibonacci number within k, found by climbing a pair of them, is taken. O(log^2 k), log k calls deep |
| `find_min_fibonacci_numbers_search.kara` | the Fibonacci numbers up to 10^9 in an `i64` `Vec` once, and the largest within what is left found by `partition_point` each time. O(log k log log k) |
| `find_min_fibonacci_numbers_walk.kara` | no list: a pair climbs to the largest Fibonacci number within k, then steps back down, `(a, b)` to `(b - a, a)`, each that fits taken. O(log k) |
| `find_min_fibonacci_numbers_solution.kara` | a Rust solution as LeetCode's Rust users write it (`vec![1, 1]` grown `while *fibs.last().unwrap() < k`, then `for &f in fibs.iter().rev()` with a `break` at 0), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 3 lines: LeetCode's three examples, then k
from 1 to 12 (`2 2 3 | 1 1 1 2 1 2 2 1 2 2 2 3`); the constraints' most,
the Fibonacci number 701408733 and one below it (`k = 10^9: 14 1 21`);
and 2000 random k up to 10^3, 10^6 or 10^9 (`2000 random k: 15814 in
all, checksum 779599156`). `find_min_fibonacci_numbers.py` mirrors the ★
arm, and its output is byte-identical. Every arm gives the same output
under `karac __mir-run`, `karac run`, `karac build` and `karac
__mir-llvm-run`.

The Mend loop: the ★ and search arms check clean as first written. The
recursive and walk arms each climb `let mut a = 1; let mut b = 1;` and
return `1 + ..(k - b)` or compare `b <= left` against `i32`s; their
literals kept the default beside the widening operators (design.md §8),
and `karac fix` declares `a: i32` and `b: i32`, 2 fixes each. The Rust
solution takes one round of 11 fixes by `karac fix`'s count: `struct
Solution;` to `struct Solution {}`, `vec![1, 1]` to `[1, 1]`, the
pattern `&f` to `f`, and `Solution::` to `Solution.`. Its
`*fibs.last().unwrap()` is taken as written. Its output matches on the
first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: for every sum up to 3000, the fewest Fibonacci numbers, each
as often as wanted, that make it, every last number tried, as a table
built once. Every k from 1 to 300, the constraints' most, 999999999, the
Fibonacci numbers 433494437 and 701408733 and the numbers either side of
them, and 1695 random k up to 3000, 10^6 or 10^9. Each case also draws a
place to split k in two.

| | property |
|---|---|
| P1 | the statement read literally, k up to 3000 |
| P2 | at least one number, and one exactly when k is a Fibonacci number |
| P3 | a shortest sum can take the largest Fibonacci number within k, the rest then one number shorter |
| P4 | k in two parts takes no fewer numbers than k whole |
| P5 | one Fibonacci number more adds at most one, while k stays within 10^9 |
| P6 | the ★ arm's answer |

All 53,180 checks pass on every arm: `2003 cases: checksum 626656940,
53180 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and `karac __mir-llvm-run`. Python, by the greedy
walk over a list built once, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: the list grown only while the next stays below k, so a Fibonacci number that ends exactly at k is left out | P1 13, P2 15, P3 59, P6 60 |
| M2 | ★: the list walked from the bottom up | P1 866, P2 15, P3 1987, P6 8008 |
| M3 | recursive: one number counted for nothing left | P1 867, P2 16, P6 2003 |
| M4 | recursive: the Fibonacci number before the largest taken in its place | P1 866, P2 15, P3 1987, P6 2002 |
| M5 | search: the list started 1, 3, so it holds numbers that are not Fibonacci numbers | P1 664, P2 26, P3 1635, P4 7, P5 544, P6 1600 |
| M6 | search: the list built only to 10^5 | P2 2, P3 1003, P5 767, P6 1005 |
| M7 | walk: a number counted at every step down, taken or not | P1 853, P3 1987, P4 27, P5 41, P6 1987 |
| M8 | walk: the pair's climb stopping short of a Fibonacci number that ends exactly at k | P1 13, P2 15, P3 59, P6 15 |
| M9 | solution: a number taken only when it is below what is left, not equal to it | P1 536, P2 29, P4 16, P6 1214 |
| M10 | solution: two counted for each number taken | P1 867, P2 16, P3 1987, P5 1173, P6 2003 |

## Benchmarks

The bench runs the ★ arm on 3 * 10^6 values of k up to 10^9, each drawn.
Every implementation prints `3 * 10^6 values of k: checksum 90457568`.

BENCHTAB

Kāra is level with Rust and C here, measured by hand at 0.93 s against
Rust's 0.96 s (0.88 s with overflow checks on), C's 0.85 s and Go's 1.36
s.
