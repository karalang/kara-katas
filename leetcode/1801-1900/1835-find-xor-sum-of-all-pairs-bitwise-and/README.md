# 1835. Find XOR Sum of All Pairs Bitwise AND

The XOR sum of a list is the bitwise `XOR` of all its elements. If the
list only contains one element, then its XOR sum will be equal to this
element. For example, the XOR sum of `[1,2,3,4]` is equal to `1 XOR 2
XOR 3 XOR 4 = 4`, and the XOR sum of `[3]` is equal to `3`. You are
given two 0-indexed arrays `arr1` and `arr2` that consist only of
non-negative integers. Consider the list containing the result of
`arr1[i] AND arr2[j]` (bitwise `AND`) for every `(i, j)` pair where `0
<= i < arr1.length` and `0 <= j < arr2.length`. Return the XOR sum of
the aforementioned list.

```
arr1 = [1,2,3], arr2 = [6,5]  ->  0
arr1 = [12], arr2 = [4]       ->  4
```

**Constraints:** `1 <= arr1.length, arr2.length <= 10^5`, `0 <= arr1[i],
arr2[j] <= 10^9`.

The arms are `fn get_xor_sum(arr1: Vec[i64], arr2: Vec[i64]) -> i64`.

## Approaches

| file | mechanism |
|---|---|
| `get_xor_sum.kara` ★ | AND distributes over XOR, so the XOR of every `a & b` is the XOR of `arr1` ANDed with the XOR of `arr2`, each list walked once. O(n + m) |
| `get_xor_sum_rows.kara` | one row of the pairs at a time: the row of `a` is the XOR of `a & b` over `arr2`, which is `a` ANDed with the XOR of `arr2`, found once; the rows XORed together. O(n + m) |
| `get_xor_sum_bits.kara` | bit by bit: a bit is set in `a & b` for each of the pairs whose two numbers both have it, and set in the XOR sum when that count of pairs, the product of the counts in each list, is odd. O(30 (n + m)) |
| `get_xor_sum_fold.kara` | the ★ arm's two XORs as folds of each list by `^`, ANDed. O(n + m) |
| `get_xor_sum_solution.kara` | a Rust solution as LeetCode's Rust users write it (each list folded by `^` from `0`, ANDed), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 4 lines: LeetCode's two examples; six edges,
one number in each list, a zero, the largest numbers, a list whose
numbers cancel, lists with no bit in common, and one list twice (`5 0
512 0 0 10`); the constraints' most, two lists of 10^5 numbers from 0 to
10^9, and one of them against a list of one (`the most: 251658592
722995200`); and 3000 random cases of 1 to 8 numbers from 0 to 63 in
each list (`3000 random cases: checksum 924341760`). `get_xor_sum.py`
mirrors the ★ arm, and its output is byte-identical. Every arm gives the
same output under `karac __mir-run`, `karac run`, `karac build` and
`karac __mir-llvm-run`.

The Mend loop: every arm checks clean as first written. The harness was
first written with `get_xor_sum(first.clone(), second.clone())` before
the last use of `first`; check warned twice that the copy is for a
parameter that only borrows it, and `karac fix` took the two `.clone()`s
off, 2 fixes. The Rust solution takes 21 fixes by `karac fix`'s count,
and its diff is: `struct Solution {}` added above the `impl`; `Vec<i32>`
to `Vec[i32]`; `fold(0, |acc, &x| acc ^ x)` to `fold(0i32, |acc, x| acc
^ x)` in both folds, where check refused the `i32` return of `x1 & x2`
because `x1` took its type from the literal `0`, which defaults to
`i64`, and the fix writes the literal `0i32`; `Solution::` to
`Solution.` at the harness's 10 calls; and the harness's `as i64` on the
result taken off. The solution takes `Vec[i32]`s, so its harness builds
its lists as `Vec[i32]`. Every arm's output matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: `arr1[i] & arr2[j]` for every pair, all of them XORed
together. It runs 2000 random cases of 1 to 10 numbers from 0 to 255 in
each list. Each arm meets six properties on each case:

| property | what it checks |
|---|---|
| P1 | the statement read literally |
| P2 | a bit of the sum is in some number of each list |
| P3 | the lists swapped give the same sum |
| P4 | a number put in `arr1` twice changes nothing |
| P5 | every number doubled doubles the sum |
| P6 | the ★ arm's answer |

It checks clean as first written. All 60,000 checks pass on every arm:
`2000 cases: checksum 749644004, 60000 checks over 5 arms: 0 failures`,
under `karac __mir-run`, `karac run`, `karac build` and `karac
__mir-llvm-run`. Python, over the same cases, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: `arr1` folded by OR, not XOR | P1 1534, P3 1902, P4 326, P6 6136 |
| M2 | ★: the two XORs XORed, not ANDed | P1 2000, P2 825, P6 8000 |
| M3 | rows: each row `a` ORed with the XOR of `arr2` | P1 1996, P2 668, P3 1530, P6 1996 |
| M4 | rows: the XOR of `arr2` taken as its last number | P1 1648, P3 1921, P6 1648 |
| M5 | bits: only the low 7 bits counted | P1 507, P5 499, P6 507 |
| M6 | bits: a bit set when the sum of the counts is odd, not their product | P1 2000, P2 825, P6 2000 |
| M7 | fold: `arr1` folded by `+` | P1 1539, P2 171, P3 1868, P4 1740, P6 1539 |
| M8 | fold: the two folds ORed | P1 1992, P2 825, P6 1992 |
| M9 | solution: `arr1` folded by AND from 0 | P1 1800, P6 1800 |
| M10 | solution: the sum's bits above the low 7 dropped | P1 507, P5 499, P6 507 |

## Benchmarks

The bench builds 20 lists of 10^5 numbers from 0 to 10^9 once and makes
3000 calls of the ★ arm, each call's two lists drawn from the checksum
so far. The arm borrows both lists, so no call copies one. It checks
clean as first written. Every implementation prints `3000 calls:
checksum 339309274`.

BENCHTAB

Measured by hand, best of three on a machine shared with a test run,
Kāra takes 0.18 s against Rust's 0.18 s (0.18 s with overflow checks
on), C's 0.18 s and Go's 0.28 s; Python takes 16.3 s.
