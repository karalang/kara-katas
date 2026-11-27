# 1819. Number of Different Subsequences GCDs

You are given an array `nums` of positive integers. The GCD of a
sequence of numbers is the greatest integer that evenly divides all of
them: the GCD of `[4,6,16]` is `2`. A subsequence of an array is a
sequence formed by removing some of its elements, possibly none. Return
the number of different GCDs among all non-empty subsequences of `nums`.

```
nums = [6,10,3]       ->  5     the GCDs are 6, 10, 3, 2 and 1
nums = [5,15,40,5,6]  ->  7
```

**Constraints:** `1 <= nums.length <= 10^5`, `1 <= nums[i] <= 2 * 10^5`.

The arms are `fn count_different_subsequence_gcds(nums: Vec[i64]) ->
i64`.

## Approaches

| file | mechanism |
|---|---|
| `count_different_subsequence_gcds.kara` ★ | a value `g` is the gcd of some subsequence exactly when the gcd of every number `g` divides is `g`, so each `g` up to the largest number walks its multiples in a table of the numbers present, and stops once the gcd reaches `g`. O(M log M), M the largest number |
| `count_different_subsequence_gcds_divisors.kara` | from the numbers up: each number's divisors listed by trial up to its square root, and each divisor keeps the gcd of the numbers it divides, so a divisor that ends equal to that gcd is the gcd of those numbers. O(n sqrt M) |
| `count_different_subsequence_gcds_set.kara` | the ★ arm's walk over the multiples of each `g`, with the numbers kept in a `Set` and asked whether each multiple is there, the gcd folded over the multiples found, all as one chain of `filter`, `step_by` and `fold`. O(M log M) expected |
| `count_different_subsequence_gcds_factor.kara` | the divisors arm's tally with each divisor list built from the number's primes: a sieve gives every value's least prime factor, a number is factored by it, and its divisors are every product of its prime powers. O(M log log M + n D), D the most divisors of a number |
| `count_different_subsequence_gcds_solution.kara` | a Rust solution as LeetCode's Rust users write it (the ★ arm's walk, with `gcd` a `fn` nested in the method), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 4 lines: LeetCode's two examples; five edges,
one number, one number many times, a number and its multiples, two
coprime numbers, and the largest value alone (`1 1 3 3 1`); the
constraints' most, the 10^5 numbers 1 to 10^5, each a gcd, and the 10^5
even numbers up to 2 * 10^5 (`the most: 100000 100000`); and 3000 random
cases of 1 to 8 numbers from 1 to 60 (`3000 random cases: checksum
450152874`). `count_different_subsequence_gcds.py` mirrors the ★ arm,
and its output is byte-identical. Every arm gives the same output under
`karac __mir-run`, `karac run`, `karac build` and `karac
__mir-llvm-run`.

The Mend loop: the ★, divisors, set and factor arms and the harness
check clean as first written. The Rust solution takes 21 fixes by `karac
fix`'s count, and its diff is: the nested `fn gcd` moved above the
`impl`, as Kāra has no nested items and it captures nothing, and `struct
Solution {}` added; `Vec<i32>` to `Vec[i32]`;
`*nums.iter().max().unwrap() as usize` to `as i64`, so the walk over the
table runs in `i64`; `vec![false; max + 1]` to `Vec.filled(max + 1,
false)`; `for &x in &nums` to `for x in ref nums`, and `seen[x as
usize]` to `seen[x]`; `Solution::` to `Solution.` at the harness's 10
calls; and the harness's `as i64` on the result taken off. LeetCode
names the method `count_different_subsequence_gc_ds`, and the solution
keeps the name. It takes a `Vec[i32]`, so its harness builds its lists
as `Vec[i32]`. Every arm's output matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every non-empty subsequence, one bit of a mask to a number,
its gcd taken and kept in a set, and the set counted. It runs 2000
random cases of 1 to 10 numbers from 1 to 60, all multiplied by a common
factor up to 20 in a quarter of them. Each arm meets six properties on
each case:

| property | what it checks |
|---|---|
| P1 | the statement read literally |
| P2 | every number is a gcd, its own, and no gcd passes the largest number |
| P3 | the numbers in reverse order give the same count |
| P4 | every number doubled doubles every gcd, so the count stays |
| P5 | a number given again changes nothing |
| P6 | the ★ arm's answer |

It checks clean as first written. All 60,000 checks pass on every arm:
`2000 cases: checksum 303177510, 60000 checks over 5 arms: 0 failures`,
under `karac __mir-run`, `karac run`, `karac build` and `karac
__mir-llvm-run`. Python, over the same cases, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: the multiples walked short of the largest number | P1 2000, P2 480, P6 8000 |
| M2 | ★: every g with a multiple present counted | P1 1994, P4 2000, P6 7976 |
| M3 | divisors: a square root never taken as a divisor | P1 184, P2 10, P4 262, P6 184 |
| M4 | divisors: the cofactor's gcd set, not folded | P1 1100, P2 99, P3 828, P4 589, P5 311, P6 1100 |
| M5 | set: every g with a multiple present counted | P1 1973, P4 2000, P6 1973 |
| M6 | set: the multiples walked short of the largest number | P1 2000, P2 480, P6 2000 |
| M7 | factor: each power of a prime taken as the prime | P1 1723, P2 839, P4 1314, P6 1723 |
| M8 | factor: each divisor folded with itself | P1 1973, P4 2000, P6 1973 |
| M9 | solution: every other multiple walked | P1 1280, P6 1280 |
| M10 | solution: 1 never counted | P1 1245, P2 27, P4 1245, P6 1245 |

## Benchmarks

The bench builds one list of 10^5 numbers from 1 to 2 * 10^5 once and
makes 100 calls of the ★ arm on runs of its first 50000 to 99999
numbers, each run's length drawn from the checksum so far. Each call
copies its run, as the arm takes its list by value. It checks clean as
first written. Every implementation prints `100 calls: checksum
177937602`.

BENCHTAB

Measured by hand, best of three on a machine shared with a test run,
Kāra takes 0.28 s against Rust's 0.28 s (0.27 s with overflow checks
on), C's 0.28 s and Go's 0.35 s; Python takes 5.6 s.
