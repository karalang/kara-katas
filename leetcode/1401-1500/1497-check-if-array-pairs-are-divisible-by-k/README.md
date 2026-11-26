# 1497. Check If Array Pairs Are Divisible by k

Given an array of integers `arr` of even length `n` and an integer `k`.
We want to divide the array into exactly `n / 2` pairs such that the sum
of each pair is divisible by `k`. Return `true` if you can find a way to
do that or `false` otherwise.

```
arr = [1,2,3,4,5,10,6,7,8,9], k = 5  ->  true
arr = [1,2,3,4,5,6], k = 7           ->  true
arr = [1,2,3,4,5,6], k = 10          ->  false
```

**Constraints:** `arr.length == n`, `1 <= n <= 10^5`, `n` is even,
`-10^9 <= arr[i] <= 10^9` and `1 <= k <= 10^5`.

The arms are `fn can_arrange(arr: Vec[i32], k: i32) -> bool`.

## Approaches

| file | mechanism |
|---|---|
| `can_arrange.kara` ★ | each value's remainder by k counted, made non-negative as `(x % k + k) % k`; the pairs exist exactly when the 0s are even in number and each other remainder r is as common as k - r. O(n + k) |
| `can_arrange_sort.kara` | the remainders, by `rem_euclid`, sorted: the 0s come first and pair among themselves, then the smallest remainder left must pair with the largest, and so on inward, each pair summing to k. O(n log n) |
| `can_arrange_map.kara` | one pass with the remainders still waiting for a partner counted in a `Map`: each value takes a waiting partner whose remainder makes k, or waits itself. O(n) |
| `can_arrange_fold.kara` | the counts built by one `fold`, then checked from both ends at once by `zip`ping count r with count k - r, a remainder that is its own partner needing an even count. O(n + k) |
| `can_arrange_solution.kara` | a Rust solution as LeetCode's Rust users write it (`vec![0; k as usize]`, `for &num in arr.iter()`, the remainders checked up to `k / 2`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 4 lines: LeetCode's three examples (`true true
false`); six edges, k = 1, a pair of negatives, a negative with its
positive partner, the two halves of an even k, a half beside a 0, and
the most and least values (`true true true true false true`); the
constraints' most, 100000 values in pairs with k = 100000, the same with
one value moved by 1, and 100000 values drawn so that most pair with the
one before them (`100000 values: true false false`); and 3000 random
arrays of 2 to 20 values with k from 1 to 12 (`3000 random arrays: 1867
pair, checksum 351296433`). `can_arrange.py` mirrors the ★ arm, and its
output is byte-identical. Every arm gives the same output under `karac
__mir-run`, `karac run`, `karac build` and `karac __mir-llvm-run`.

The Mend loop: the four Kāra arms check clean as first written. The Rust
solution takes one round of 9 fixes by `karac fix`'s count, and its diff
is: `struct Solution;` to `struct Solution {}`, each `Vec<i32>` to
`Vec[i32]`, `vec![0; k as usize]` to `Vec.filled(k, 0)`, `for &num` to
`for num` and `Solution::` to `Solution.`. Every arm's output matches on
the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the first value not yet paired tried with each later one
whose sum k divides, and the rest paired the same way, backtracking when
they cannot be. LeetCode's examples, the edges, and 1991 random arrays
of 2 to 12 values from -50 to 50, most of them drawn to pair with the
one before, k from 1 to 10. Each arm meets six properties on each case:

| property | what it checks |
|---|---|
| P1 | the statement read literally |
| P2 | values that pair up have a sum k divides |
| P3 | the values in reverse order pair as they do |
| P4 | each value moved by a multiple of k pairs as it does |
| P5 | a value and its negative added pair as they do |
| P6 | the ★ arm's answer |

All 60,000 checks pass on every arm: `2000 cases: checksum 349301243,
60000 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and `karac __mir-llvm-run`. Python, pairing the
sorted remainders by a memoised search, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: the 0s never checked | P1 47, P2 47, P6 188 |
| M2 | ★: a negative value's remainder taken from its absolute value | P1 741, P2 21, P4 165, P5 386, P6 2964 |
| M3 | sort: the innermost pair never checked | P1 100, P2 100, P5 35, P6 100 |
| M4 | sort: the remainders never sorted | P1 821, P3 146, P5 336, P6 821 |
| M5 | map: a 0 waits for a remainder of k, which never comes | P1 782, P5 121, P6 782 |
| M6 | map: a partner taken stays waiting | P1 598, P2 147, P3 136, P5 204, P6 598 |
| M7 | fold: a remainder that pairs with itself never checked even | P1 47, P2 47, P6 47 |
| M8 | fold: count r checked against count k - 1 - r | P1 1110, P2 5, P5 56, P6 1110 |
| M9 | solution: an even k's half never checked | P1 23, P2 23, P6 23 |
| M10 | solution: each remainder taken one more | P1 1105, P2 20, P5 140, P6 1105 |

## Benchmarks

The bench keeps one array of 100000 values, each a partner of the one
before for k = 1000, and makes 1000 calls of the ★ arm: every other call
with k = 1000, the rest with k from 1 to 100000 chosen from the checksum
so far, each first moving one value by 1000. Every implementation prints
`1000 calls over 100000 values: checksum 576577913`.

BENCHTAB

Measured by hand, best of three on a machine shared with a test run,
Kāra takes 0.52 s against Rust's 0.48 s (0.50 s with overflow checks
on), C's 0.49 s and Go's 0.71 s; Python takes 5.4 s.
