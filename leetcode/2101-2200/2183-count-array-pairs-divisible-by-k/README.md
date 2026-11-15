# 2183. Count Array Pairs Divisible by K

Given a **0-indexed** integer array `nums` of length `n` and an integer
`k`, return *the **number of pairs*** `(i, j)` *such that:*

- `0 <= i < j <= n - 1` *and*
- `nums[i] * nums[j]` *is divisible by* `k`.

```
nums = [1, 2, 3, 4, 5], k = 2  ->  7
nums = [1, 2, 3, 4],    k = 5  ->  0
```

**Constraints:** `1 <= nums.length <= 10^5`; `1 <= nums[i], k <= 10^5`.

Every pair is too many at 10^5 numbers. But whether x * y is a multiple
of k depends on each number only through its gcd with k: x * y is one
exactly when gcd(x, k) * gcd(y, k) is. So the numbers are counted by
their gcd with k, a divisor of k each, of which there are at most 128,
and every two divisors whose product is a multiple of k add their
counts' pairs. O(n log k + sqrt(k) + divisors^2).

## Approaches

| file | mechanism |
|---|---|
| `pairs_divisible.kara` ★ | the numbers counted by their gcd with k in a `Vec.filled(k + 1, 0)`, the divisors of k found in pairs up to the square root, and every two of them whose product is a multiple of k paired |
| `pairs_divisible_running.kara` | a running count over the divisors of k: each number pairs with the earlier multiples of k / gcd(x, k), which the table already holds, and is then added under every divisor of k it is a multiple of; O(n * divisors) |
| `pairs_divisible_multiples.kara` | for each divisor d of k, the numbers that are multiples of d, summed from the gcd counts over the divisors that d divides; each number then pairs with the multiples of k / gcd(x, k), itself among them when its square is a multiple of k, and the sum, met from both ends, less those, halved |
| `pairs_divisible_struct.kara` | a `struct GcdTally` of the gcd counts in a `SortedMap[i64, i64]`, made `for_k` a k, that each number is `add`ed to (`mut ref self`, `entry`, `or_insert`) and that counts its `pairs` (`ref self`) |
| `pairs_divisible_iter.kara` | the gcd counts `fold`ed into a `SortedMap` and `collect`ed into a list; for each, `enumerate`d, the gcds from it on `skip`ped to, `filter`ed to those that pair with it, `map`ped to their pairs and `sum`med, and those sums `sum`med |
| `pairs_divisible_solution.kara` | LeetCode's Rust template: `use std::collections::HashMap`, `Vec<i32>`, an inner `fn gcd`, `*cnt.entry(..).or_insert(0) += 1`, its `iter()` walked twice with `&a` patterns, `&&`; carried by `karac fix` in three rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's two examples and four more
(one number, three that pair only two by two, two whose product alone
is a multiple, and the constraints' largest three times), each with its
count; then the total and a checksum over 2000 random lists of 1 to 30
numbers, of 1 to 20 with a k of 1 to 12 and of 1 to 10^5 with a k of 1
to 10^5 in turn; then the constraints' largest, 10^5 numbers: all 10^5
with k 10^5, then at random with k 10^5, 83160 (which has 128 divisors)
and 99991 (a prime). `pairs_divisible.py` mirrors the ★ arm and its
output is byte-identical.

The iterator arm's inner sum was written `.sum::<i64>()`, Rust's
turbofish, and `karac fix` drops the `::[i64]`, since the `sum` it
feeds already fixes the type.

`karac fix` carries the template in three rounds of 21, 2 and 1 edits:
Rust's spellings (the `use` dropped, `Vec<..>` and `HashMap<..>` to
brackets, the inner `fn gcd` moved out to the top level, the `&x`,
`&a` and `&ca` patterns to `x`, `a` and `ca`, `&&` to `and`, `struct
Solution;` to `struct Solution {}`, and `Solution::` to `.`, among
them); then `HashMap` to `Map`, once the `use` that named it is gone;
then the `as i64` on each number dropped, as an `i32` widens to the
`i64` gcd takes. Its `Map` is walked in hash order, but every pair of
gcds is added up, so the count does not depend on the order.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every pair of indices i < j tried, and counted when the
product of their numbers is a multiple of k. No gcds and no divisors.
It checks 300 random lists of 1 to 10 numbers of 1 to 30, with a k of 1
to 30; then 30 with k a prime, 13, 17, 19 or 23; then 30 with k 36 or
60, which have many divisors. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the count is the statement read literally |
| P2 | the list reversed: the same count |
| P3 | a k of 1: every pair |
| P4 | every number k more: the same count |
| P5 | the count at least the pairs with a multiple of k in them, and at most every pair |
| P6 | each arm agrees with at least three of the other five |

P2 holds since a pair does not care which of its numbers comes first.
P3 holds since every product is a multiple of 1. P4 holds since x + k
has the same gcd with k as x, so each product is a multiple of k
exactly when it was. P5 holds since a pair with a multiple of k in it
has a product that is one.

The differential prints `360 lists: checksum 648362671, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading of the same
lists. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Twenty-eight edits to the differential, five to each Kāra arm and three
to the template, each run under `karac __mir-llvm-run` and `karac
__mir-run`. Seventeen are kept, three to each Kāra arm and two to the
Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a gcd's own pairs counted as its square halved | P1 63, P3 330, P5 9, P6 63 |
| M2 | ★: two gcds paired by their sum | P1 174, P5 111, P6 174 |
| M4 | ★: no gcd paired with itself | P1 63, P3 330, P5 37, P6 63 |
| M6 | running: every number added under k too | P1 295, P2 156, P6 295 |
| M7 | running: the earlier multiples of the gcd itself | P1 305, P2 219, P5 17, P6 305 |
| M9 | running: the square root itself never tried | P1 21, P2 14, P3 330, P5 10, P6 21 |
| M11 | multiples: a number never kept from pairing with itself | P1 77, P3 330, P5 9, P6 77 |
| M12 | multiples: the divisors of each divisor summed | P1 302, P5 167, P6 302 |
| M14 | multiples: a number pairing with itself when a multiple of k | P1 24, P6 24 |
| M17 | struct: two gcds' pairs the larger count | P1 48, P5 36, P6 48 |
| M18 | struct: the gcd taken with k + 1 | P1 177, P5 113, P6 177 |
| M19 | struct: a remainder of 1 let through | P1 263, P6 263 |
| M22 | iter: a gcd always paired with itself | P1 295, P6 295 |
| M23 | iter: a gcd's own pairs one too many each | P1 171, P3 360, P5 26, P6 171 |
| M25 | iter: the gcds from half way | P1 166, P5 35, P6 166 |
| M26 | solution: the adapter's numbers halved | P1 201, P4 192, P5 61, P6 201 |
| M28 | solution: a gcd's own pairs counted in both orders | P1 63, P3 330, P5 15, P6 63 |

P1 and P6 kill all seventeen, P5 thirteen, P3 six, P2 three and P4 one.
P2 reverses the list, and sees only the running arm's edits, since it
alone reads the numbers in order: a number added under k (M6), the
multiples of the gcd itself (M7), and the square root left out (M9),
each of which treats the earlier numbers apart from the later. P3 sets k
to 1, where every number has gcd 1 and all of them pair with each
other, and sees an edit that miscounts a gcd's pairs with itself: as
its square (M1), not at all (M4), the self-pairs kept (M11), one too
many (M23), both orders (M28), and the square root of 1 never tried
(M9). P4 adds k to every number, and sees only the halving that moves a
number's gcd with k (M26). P5 misses an edit that miscounts within the
bounds: a number added under k (M6), a number taken to pair with
itself only when it is a multiple of k (M14), a remainder of 1 let through (M19), and a gcd always
paired with itself (M22).

Of the twenty-eight, eleven were not kept. One is equivalent: the
multiples arm's halving rounded up (M15), since a pair met from both
ends is always counted twice, so the sum is even. One crashes: the ★
arm's gcd stopping at a remainder of 1 (M5) indexes the counts past k.
Two fail as a kept one does: the struct arm's and the iter arm's gcd
never paired with itself, as M4. Seven were left out to keep three to
an arm: the ★ arm's square root listed twice (M3), the running arm's
divisors only up to the square root and each number added twice (M8,
M10), the multiples arm's numbers with gcd k left out (M13), the struct
arm's counts from 1 (M20), the iter arm's numbers counted twice (M24),
and the template's product against k + 1 (M27).

## Verification

Every arm prints the same output as `pairs_divisible.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the iter, template, ★ and struct arms take 1.8
s to 2.3 s, the multiples arm 3.5 s and the running arm 5.5 s, which
walks every divisor of k for every number. The differential takes 0.6
s.

## Benchmarks

The bench builds one row of 10^6 numbers of 1 to 10^5 once; then solves
200 windows of 10^5 numbers, the constraints' longest, each at a random
start and with a k of 1 to 10^5, so that no solve repeats one before,
with the ★ arm in all five languages. C works over a pointer and a
length, Rust and Go over a slice of the row; Kāra and Python copy each
window into a list of its own. Every implementation prints `200 solves:
checksum 567004895`.

BENCHTAB
