# 1577. Number of Ways Where Square of Number Is Equal to Product of Two Numbers

Given two arrays of integers `nums1` and `nums2`, return the number of
triplets formed (type 1 and type 2) under the following rules:

- Type 1: triplet `(i, j, k)` if `nums1[i]^2 == nums2[j] * nums2[k]`
  where `0 <= i < nums1.length` and `0 <= j < k < nums2.length`.
- Type 2: triplet `(i, j, k)` if `nums2[i]^2 == nums1[j] * nums1[k]`
  where `0 <= i < nums2.length` and `0 <= j < k < nums1.length`.

```
nums1 = [7,4],     nums2 = [5,2,8,9]   ->  1
nums1 = [1,1],     nums2 = [1,1,1]     ->  9
nums1 = [7,7,8,3], nums2 = [1,2,9,7]   ->  2
```

**Constraints:** `1 <= nums1.length, nums2.length <= 1000`;
`1 <= nums1[i], nums2[i] <= 10^5`.

## Approaches

Each arm counts one type in a `ways(squares, products)` and adds the two
types as the same count with the arrays swapped.

| file | mechanism |
|---|---|
| `triplets.kara` ★ | for each `x`, a walk over the other array that keeps a `Map` of the values seen so far and, at each `y` dividing `x^2`, adds how many times `x^2 / y` was seen. O(n · m) expected |
| `triplets_pairs.kara` | the squares counted in a `Map`, then every pair `j < k` of the other array looked up by its product. O(n + m²) expected |
| `triplets_sorted.kara` | the other array sorted once; for each `x`, two pointers close in on the pairs whose product is `x^2`, a run of equal values on each side counted as a block. O(m log m + n · m) |
| `triplets_solution.kara` | LeetCode's Rust template (`num_triplets(..) -> i32` with a nested `fn count` over a `HashMap` of value counts, each distinct value `p` paired with `x^2 / p` once), carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

The template walks its `Map` in hash order, which a sum does not see.

Every arm prints the same 9 lines: LeetCode's four examples, then `[1]`
against `[1]` and `[100000]` against two of them (whose square is `10^10`);
then the sum of the answers and a checksum for 3000 random pairs of
arrays of up to 6 values, 300 of up to 100 and 10 of up to 1000, each
value a factor times a few 2s and 3s so that squares and products meet.
`triplets.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every triplet of each type tried. It checks 3000 pairs of
arrays of 1 to 6 values from 1 to 12, every random choice drawn before
any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the two arrays swapped leave the answer |
| P3 | every value doubled leaves the answer |
| P4 | both arrays reversed leave the answer |
| P5 | both arrays sorted leave the answer |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 110890386, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends.

The first M10 paired `p` with `q` when `p <= q + 1` rather than
`p < q`, which was equivalent: `p = q + 1` would need `q(q + 1)` to be a
square, which it never is for `q >= 1`. It was replaced.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a value counted as seen before it is tested, so it pairs with itself | P1 1732, P6 1732 |
| M2 | ★: type 1 counted twice and type 2 never | P1 767, P2 767, P6 767 |
| M3 | ★: the other array's first value skipped | P1 476, P4 519, P5 431, P6 476 |
| M4 | pairs: `j` paired with itself | P1 1732, P6 1732 |
| M5 | pairs: equal squares counted once | P1 109, P6 109 |
| M6 | sorted: a run of equal values counted in both orders | P1 536, P6 536 |
| M7 | sorted: two blocks added in place of multiplied | P1 5, P6 5 |
| M8 | sorted: the left pointer moves past a match | P1 845, P6 845 |
| M9 | template: `cp * cp / 2` for the pairs inside a value's count | P1 536, P6 536 |
| M10 | template: each pair of distinct values counted in both orders | P1 426, P6 426 |

## Benchmarks

The bench draws 20 arrays of 1000 values first, each a factor below 100
times up to three 2s and 3s, then counts the triplets of 10 pairs of them
by the ★ arm, in all five languages: 20000 maps made, each filled with
1000 values. Every implementation prints `10 pairs of arrays of 1000
values: triplets total 1485886, checksum 176087587`.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `76e5a13ad` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`, an open-addressing table with a cheap mixer) | 0.284 s |
| Rust (`rustc -O`) | 0.504 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.520 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.520 s |
| Kāra (`karac build`) | 0.525 s |
| Go | 0.712 s |
| Python | 1.9 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time is below its real time (0.475 s and 0.480 s on one run).

Kāra is 1.00x Rust under overflow checks by median: both maps hash with
SipHash-1-3, and the time is the hashing. C's table uses a cheap
integer mixer and is nearly twice as fast; Python's dict hashes a small
integer as itself, which is why it is only 4x behind here.

## Verification

All four arms print the same output as `triplets.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them and the differential. `karac check` reports nothing on any of them,
and `karac fix` has nothing left to change. Checked at kara `76e5a13ad`.

## Writing it

The ★, pairs and sorted arms were written in Kāra and checked as
written.

The Rust template took four rounds of `karac fix`:

1. the `use std::collections::HashMap;` line removed, the `Vec<..>` and
   `HashMap<..>` types to `[..]`, `HashMap::new()` to `HashMap.new()`,
   `&Vec<i32>` to `ref Vec[i32]`, the `&y`, `&x`, `(&p, &cp)` and `|&x|`
   patterns to plain names, `freq.get(&q)` with `Some(&cq)` to
   `freq.get(q).cloned()` with `Some(cq)`, `count(&nums1, &nums2)` to
   `count(nums1, nums2)`, and `Solution::` to `Solution.`;
2. the nested `fn count` moved above the `impl`;
3. `HashMap` to `Map`;
4. `ref Vec[i32]` to `Vec[i32]`, `y as i64` to `y`, `0i64` to `0`, and
   the wrapper's `as i64` dropped.

It then checks and agrees with no hand edit.
