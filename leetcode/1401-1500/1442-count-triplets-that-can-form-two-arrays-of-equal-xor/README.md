# 1442. Count Triplets That Can Form Two Arrays of Equal XOR

Given an array of integers `arr`, we want to select three indices `i`,
`j` and `k` where `0 <= i < j <= k < arr.length`. Let's define `a` and
`b` as follows: `a = arr[i] ^ arr[i + 1] ^ ... ^ arr[j - 1]` and `b =
arr[j] ^ arr[j + 1] ^ ... ^ arr[k]`, where `^` denotes the bitwise-xor
operation. Return the number of triplets (`i`, `j` and `k`) where `a ==
b`.

```
arr = [2,3,1,6,7]                   ->  4
arr = [1,1,1,1,1]                   ->  10
arr = [2,3]                         ->  0
arr = [1,3,5,7,9]                   ->  3
arr = [7,11,12,9,5,2,7,17,22]       ->  8
```

**Constraints:** `1 <= arr.length <= 300`, `1 <= arr[i] <= 10^8`.

Each arm is `fn count_triplets(arr: Vec[i32]) -> i32`.

## Approaches

| file | mechanism |
|---|---|
| `count_triplets.kara` ★ | a = b exactly when the xor from i to k is 0, when the prefix xors before i and through k are equal, and then every j between serves: for each prefix xor met, in a `Map[i32, (i64, i64)]`, how many times and the sum of the places it was met at, so each place adds k - i for every earlier i at once. O(n) |
| `count_triplets_groups.kara` | the places of each prefix xor in a `SortedMap[i32, Vec[i64]]` through `entry().or_insert`, and every two places of the same xor giving a triplet for each j between them. O(n + the pairs of equal prefixes) |
| `count_triplets_prefix.kara` | the prefix xors in a list, and every two equal ones a distance d apart giving d - 1 triplets. O(n²) |
| `count_triplets_brute.kara` | every i, j and k, a grown one number at a time as j moves on and b as k does. O(n³) |
| `count_triplets_solution.kara` | a Rust solution as LeetCode's Rust users write it (`let n = arr.len()`, each i's running xor over k, `res += (k - i) as i32` whenever it is 0), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 3 lines: LeetCode's five examples and three
more (`4 10 0 3 8 0 1 2`); the constraints' most, 300 ones, 300 numbers
up to 10^8, and 300 numbers of 1 to 4 (`300 numbers: 2250050 0 588646`);
and 2000 random cases of 1 to 60 numbers up to 1, 3, 15 or 10^8 (`2000
random cases: 3862891 triplets, checksum 164129119`).
`count_triplets.py` mirrors the ★ arm, and its output is byte-identical.
Every arm gives the same output under `karac __mir-run`, `karac run`,
`karac build` and `karac __mir-llvm-run`.

The Mend loop: the prefix and brute arms check clean as first written.
The ★ and groups arms wrote the running xor as `let mut x = 0;` and `x
^= a`, and looked it up in a map keyed by `i32`, which `karac check`
refuses, saying `x` is an `i64` because its literal kept the default, an
operator not fixing a literal's type, and `karac fix` declares it `let
mut x: i32 = 0`, 1 fix each. The Rust solution takes one round of 9
fixes by `karac fix`'s count: `struct Solution;` to `struct Solution
{}`, `Vec<..>` to `Vec[..]`, `let mut res = 0` to `let mut res: i32 = 0`
for the same reason as the ★ arm's `x`, and `Solution::` to `Solution.`.
Every arm's output matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every i < j <= k, a and b each found afresh, and the triplets
with a == b counted, while there are at most 30 numbers. LeetCode's
examples, six edge cases (one number, two equal numbers, two different
ones, three whose xor is 0, four equal numbers, and the largest
numbers), the constraints' most three ways (300 ones, 300 numbers up to
10^8, and 300 numbers of 1 to 4), and 1989 random cases drawn as the
harness draws them. Each case also draws the number P4 and P5 add.

| | property |
|---|---|
| P1 | the statement read literally, while there are at most 30 numbers |
| P2 | the numbers in the other order give the same count |
| P3 | every number doubled gives the same count |
| P4 | one more number at the end never gives fewer |
| P5 | a number twice more at the end gives one more at least |
| P6 | the ★ arm's answer |

All 55,140 checks pass on every arm: `2003 cases: checksum 879374462,
55140 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and `karac __mir-llvm-run`. Python, by each i's
running xor, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: each earlier place counted as one place further back | P1 698, P6 5856 |
| M2 | ★: each place kept one too small | P1 671, P2 630, P6 5748 |
| M3 | groups: the empty prefix's place left out | P1 623, P2 883, P6 1374 |
| M4 | groups: every j between two places and one more | P1 698, P6 1464 |
| M5 | prefix: each two equal prefixes giving one triplet too few | P1 698, P5 629, P6 1464 |
| M6 | prefix: each prefix the last number alone | P1 695, P5 1918, P6 1461 |
| M7 | brute: b never a single number | P1 699, P5 556, P6 1463 |
| M8 | brute: a only the last number before j | P1 655, P2 921, P6 1418 |
| M9 | solution: each running xor started one number late | P1 562, P2 886, P6 1178 |
| M10 | solution: each zero xor counted once | P1 653, P6 1419 |

## Benchmarks

The bench draws 2000 arrays of 300 numbers of 1 to 1023 and counts each
one's triplets 50 times with the ★ arm, folding the counts to a
checksum. Each implementation makes a fresh map for every array, as the
★ arm makes a fresh `Map`: Rust's `HashMap` hashes with SipHash as
Kāra's does, Go's is its built-in map, and C's is a table of its own,
open addressing over 1024 slots, which the prefix xors of numbers below
1024 always fit. Every implementation prints `10^5 arrays of 300:
checksum 765850812`.

BENCHTAB

Measured by hand, Kāra takes 0.99 to 1.03 s against Rust's 1.27 to 1.41
s (1.27 to 1.31 s with overflow checks on), C's 0.16 s and Go's 3.1 to
3.4 s; Python takes 6.0 s.
