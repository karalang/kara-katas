# 1420. Build Array Where You Can Find The Maximum Exactly K Comparisons

You are given three integers `n`, `m` and `k`. Consider the following
algorithm to find the maximum element of an array of positive integers:

```
maximum_value = -1
maximum_index = -1
search_cost = 0
n = arr.length
for (i = 0; i < n; i++) {
    if (maximum_value < arr[i]) {
        maximum_value = arr[i]
        maximum_index = i
        search_cost = search_cost + 1
    }
}
return maximum_index
```

You should build the array `arr` which has the following properties:
`arr` has exactly `n` integers, `1 <= arr[i] <= m` where `0 <= i < n`,
and after applying the mentioned algorithm to `arr`, the value
`search_cost` is equal to `k`. Return the number of ways to build the
array `arr` under the mentioned conditions. As the answer may grow
large, the answer must be computed modulo `10^9 + 7`.

```
n = 2, m = 3, k = 1    ->  6    [1, 1], [2, 1], [2, 2], [3, 1], [3, 2], [3, 3]
n = 5, m = 2, k = 3    ->  0    no array satisfies the conditions
n = 9, m = 1, k = 1    ->  1    [1, 1, 1, 1, 1, 1, 1, 1, 1]
```

**Constraints:** `1 <= n <= 50`, `1 <= m <= 100`, `0 <= k <= n`.

Each arm is `fn num_of_arrays(n: i32, m: i32, k: i32) -> i32`.

## Approaches

| file | mechanism |
|---|---|
| `num_of_arrays.kara` ★ | `ways[j][c]`, the arrays so far whose largest is j and whose search cost is c, one element more at a time: at most the largest, j ways, or a new largest, which costs one search more, from the arrays of cost c - 1 whose largest is below j, summed as j climbs. O(n m k) |
| `num_of_arrays_memo.kara` | a recursion on what is left to fill, from an empty prefix whose largest is 0, each answer kept in a three-level memo once found; a new largest is tried at every value above the old. O(n m² k) |
| `num_of_arrays_push.kara` | the arrays pushed forward instead of pulled: from largest j and cost c, j ways stay put and one way goes to every larger largest at cost c + 1, added over the range at once through a difference array. O(n m k) |
| `num_of_arrays_in_place.kara` | one table brought up to one element more in place, the cost and the largest counted downward so that every entry read is still the old one, and the old entries' sums below each largest taken first. O(n m k) |
| `num_of_arrays_solution.kara` | a Rust solution as LeetCode's Rust users write it (`const MOD`, `n`, `m` and `k` cast to `usize`, a `vec![vec![vec![0i64; k + 1]; m + 1]; n + 1]` table, the new largest summed over every smaller one in an inner loop), carried to Kāra by `karac fix`. O(n m² k) |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 3 lines: LeetCode's three examples and five
more (`6 0 1 1 0 1 7 34549172`); the constraints' most, n = 50 and m =
100 with k = 1, 2 and 50 (`n = 50, m = 100: 435886633 993116649
538992043`); and 2000 random cases with n up to 12, m up to 30 and k up
to n (`2000 random cases: 536 with no array, checksum 177538904`).
`num_of_arrays.py` mirrors the ★ arm, and its output is byte-identical.
Every arm gives the same output under `karac __mir-run`, `karac run`,
`karac build` and `karac __mir-llvm-run`.

The Mend loop: the ★, push and in-place arms check clean as first
written. The memo arm passed `n as i64`, `k as i64` and `m as i64` to
`i64` parameters, casts the widening makes unneeded, and `karac fix`
drops them, 3 fixes. The Rust solution takes one round of 15 fixes by
`karac fix`'s count: `struct Solution;` to `struct Solution {}`, the `as
usize` casts to `as i64`, the `vec![..]` table to `Vec.filled(n + 1,
Vec.filled(m + 1, Vec.filled(k + 1, 0)))`, `j as i64` dropped where `j`
already is one, `0i64` to `0`, and `Solution::` to `Solution.`; its
`const MOD: i64 = 1_000_000_007;` is taken as written. Every arm's
output matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every array of n values from 1 to m, counted in turn like an
odometer, and the statement's search run on each, its cost counted,
while there are at most 20000 arrays. LeetCode's examples, the edges
(one place, one value, no search, a search longer than there are
values), the constraints' most three times (k = 1, 25 and 50), and 1990
random cases: every array listable two times in three, n up to 6 and m
up to 5, and n up to 50 with m up to 40 otherwise, ten of them at m =
100.

| | property |
|---|---|
| P1 | the statement read literally, while the arrays are at most 20000 |
| P2 | a count taken modulo 10^9 + 7, and none when the search costs nothing or more than there are values or places |
| P3 | summed over every k from 0 to n, every array once, m^n in all, while n is at most 8 and m at most 10 |
| P4 | at k = 1 the first value is the largest, j^(n - 1) ways for each j; at k = n with n at most m the array climbs, m choose n ways |
| P5 | one allowed value more loses no array, while no count wraps |
| P6 | the ★ arm's answer |

All 38,620 checks pass on every arm: `2003 cases: checksum 227422183,
38620 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and `karac __mir-llvm-run`. The differential checks
clean as first written. Python, by a table of prefix sums over the
largest, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: a number no larger than the largest given one choice too few | P1 512, P3 253, P4 279, P6 3616 |
| M2 | ★: a new largest counted from arrays of the same cost, not one less | P1 572, P4 358, P6 3932 |
| M3 | memo: a full array counted whatever its cost | P1 633, P2 424, P3 253, P4 121, P6 1170 |
| M4 | memo: a number equal to the largest taken as a new largest | P1 764, P2 424, P3 364, P4 252, P6 1301 |
| M5 | push: each new largest also allowed to equal the old one | P1 633, P2 424, P3 253, P4 121, P6 1170 |
| M6 | push: a number no larger than the largest given one choice too many | P1 512, P3 253, P4 279, P6 904 |
| M7 | in place: the costs brought up from the lowest, so new entries are read as old | P1 320, P3 162, P4 108, P5 5, P6 696 |
| M8 | in place: the sums below each largest taken up to it, not below it | P1 633, P2 424, P3 253, P4 121, P6 1170 |
| M9 | solution: a new largest allowed to equal the old one | P1 633, P2 424, P3 253, P4 121, P6 1170 |
| M10 | solution: each one-number array counted j times | P1 542, P3 300, P4 427, P5 1, P6 943 |

## Benchmarks

The bench runs the ★ arm 1000 times at the constraints' most, n = 50 and
m = 100, each time with k drawn from 0 to 50. The C bench holds its
tables as rows each allocated apart, as the Kāra and Rust programs hold
a `Vec` of `Vec`s. Every implementation prints `1000 values of k at n =
50, m = 100: checksum 708205512`.

BENCHTAB

Kāra is level with Rust and C here, measured by hand at 0.81 to 0.85 s
against Rust's 0.78 to 0.83 s (0.77 to 0.80 s with overflow checks on),
C's 0.75 s and Go's 1.23 to 1.28 s; Python takes 16 s.
