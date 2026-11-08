# 2006. Count Number of Pairs With Absolute Difference K

Given an integer array `nums` and an integer `k`, return the number of
pairs `(i, j)` where `i < j` such that `|nums[i] - nums[j]| == k`.

```
nums = [1,2,2,1],    k = 1  ->  4
nums = [1,3],        k = 3  ->  0
nums = [3,2,1,5,4],  k = 2  ->  3   ([3,1], [3,5], [2,4])
```

**Constraints:** `1 <= nums.length <= 200`; `1 <= nums[i] <= 100`;
`1 <= k <= 99`.

`k` is at least 1, so no value pairs with itself, and a pair is the same
whichever end is met first.

## Approaches

| file | mechanism |
|---|---|
| `pairs.kara` ★ | a count of each value seen so far in a `Vec` of 101; each value pairs with every earlier one `k` below it and `k` above it. O(n) |
| `pairs_brute.kara` | every pair `i < j` tried, `abs` of the difference compared with `k`. O(n^2) |
| `pairs_map.kara` | the values counted in a `Map` through `entry(..).or_insert(0)`; each distinct `v` pairs its copies with those of `v + k`. O(n) |
| `pairs_sorted.kara` | sorted, two pointers that only move forward bound the run of values exactly `k` above `nums[i]`. O(n log n) |
| `pairs_iter.kara` | `enumerate`, then for each value the ones after it by `skip(i + 1)`, `filter` on the difference and `count`, the counts `sum`med. O(n^2) |
| `pairs_solution.kara` | LeetCode's Rust template (a unit struct, `impl Solution`, `Vec<i32>`, a `[0; 101]` array, `for &x in &nums`, `usize` indices, a `&Vec` wrapper), carried by `karac fix` to a clean check |
| `differential.kara` | all six arms against the statement read literally, six properties |

Every arm prints the same 10 lines: the answers for LeetCode's three
examples and five more; then the sum and a checksum of the answers for 3000
arrays of 1 to 30 values up to 1 to 10 with `k` up to 5, and for 50 arrays
of 200 values up to 100 with any `k`. `pairs.py` mirrors the ★ arm and its
output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the
statement read literally: every pair `i < j`, the difference taken by
comparison rather than `abs`, kept when it is `k`. It checks 2000 problems
of 1 to 25 values, a quarter of them up to 100 with any `k` and the rest up
to 1 to 12 with `k` up to 6. Every random choice of a problem (the values,
a shuffle, a shift, a value to append) is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the values shuffled leave the answer |
| P3 | every value raised by the same amount (staying within 1 to 100) leaves the answer |
| P4 | every value `x` turned into `101 - x` leaves the answer |
| P5 | one more value `y` appended adds the values already there at `y - k` and `y + k` |
| P6 | each arm agrees with at least three of the other five |

The differential prints `2000 problems: checksum 582139588, 72000 checks
over 6 arms: 0 failures` under every lane in Verification. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Thirty edits to the differential, five to each of its arms, each run under
`karac __mir-run` and `karac __mir-llvm-run`. Seventeen are kept, three to
each of the five Kāra arms and two to the Rust arm. All thirty are killed,
each fails the same way under both backends, none by a crash, and no two
kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a partner at value 1 never counted | P1 503, P2 490, P3 496, P4 507, P5 133, P6 503 |
| M2 | ★: a partner at value 100 never counted | P1 6, P2 4, P3 18, P4 507, P6 6 |
| M3 | ★: a value's count kept at one | P1 753, P2 593, P5 508, P6 753 |
| M4 | brute: a difference up to `k` counted | P1 1879, P5 1903, P6 1879 |
| M5 | brute: the difference taken one way only | P1 987, P2 885, P4 982, P5 484, P6 987 |
| M6 | brute: the first value never paired | P1 745, P2 601, P5 196, P6 745 |
| M7 | map: the partner looked up one too high | P1 1090, P5 811, P6 1090 |
| M8 | map: the counts added, not multiplied | P1 1063, P5 641, P6 1063 |
| M9 | map: only the partner's count | P1 791, P4 735, P5 569, P6 791 |
| M10 | sorted: the values never sorted | P1 1085, P2 500, P4 560, P5 786, P6 1085 |
| M11 | sorted: the target one short | P1 1226, P5 1003, P6 1226 |
| M12 | sorted: the smallest value never a lower end | P1 842, P4 701, P5 201, P6 842 |
| M13 | iter: every value paired with all but the first | P1 1062, P2 601, P5 759, P6 1062 |
| M14 | iter: any multiple of `k` counted | P1 1666, P5 1409, P6 1666 |
| M15 | iter: values with a partner counted, not pairs | P1 776, P2 648, P5 552, P6 776 |
| M16 | Rust: the partner above one too high | P1 972, P2 954, P3 18, P4 1052, P5 506, P6 972 |
| M17 | Rust: the answer one pair short when any | P1 1116, P5 57, P6 1116 |

P1 and P6 kill all seventeen, P5 sixteen, P2 nine, P4 seven and P3
three. P3 sees only the edits at the ends of the range: the ★ arm's (M1,
M2) and the Rust arm's partner above clamped at 100 (M16); every other arm
reads values only through their differences, which a shift keeps.
M2 is the faintest, 6 problems in 2000: a partner at 100 needs a quarter's
wide values and a pair `k` apart at the top; P4 turns 100 into 1 and sees
it 507 times. P2 sees the edits that depend on order: a pair seen from one
end only (M5), a first value or position treated apart (M6, M13), the
values unsorted (M10), a count that forgets repeats (M3, M15). P4 sees the
edits that treat smaller and larger values unevenly (M5, M9, M12). P5
misses only M2: it would fail only when the appended value sits `k` below
a 100 already there, and none of the 2000 draws does that. The Rust arm's
answer one short (M17) is wrong exactly when a pair exists, and P5 sees it
only where the appended value adds the first pair.

The other thirteen fail as a kept one does, or with counts of their own that
add nothing. The brute arm trying every pair both ways, the map arm's
counts each one more and the sorted arm's run start one past it fail alike
(each is wrong exactly when a pair exists, and off by the appended pairs
under P5); the brute and iterator arms leaving neighbours out fail alike,
and the iterator arm's one-way difference fails as M5, as does the Rust
arm never looking a partner up below; the Rust arm stopping the partners
above below 100 fails as M2, and its values each counted twice as the
brute arm's pairs both ways. The ★ arm counting
only earlier values below, its counts all starting at one, the map arm's
pairs halved and the sorted arm keeping only the longest run fail with
counts of their own. Five drafts were set aside before running, as
equivalent. Three because `k >= 1` keeps a value from pairing with itself:
the brute arm's inner loop from `i`, the iterator arm's `skip(i)`, and a
`take(i + 1)` for the values before. Two by symmetry: the map arm looking
down at `v - k` counts every pair from its larger end instead, and the ★
arm counting a value before its lookups changes nothing when `k` is never
0.

## Verification

Every arm prints the same output as `pairs.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every arm
and the differential. `karac check --output=json` reports nothing on any of
them. Under `karac __mir-run` the arms take 0.19 s (sorted) to 2.4 s
(iter) and the differential 5.1 s.

The five arms were written in Kāra and checked clean. The Rust arm was
written as LeetCode's Rust template and reaches a clean check through
`karac fix` alone, in four rounds (10, 1, 1 and 1 edits). The first carries
the unit struct, `Vec<..>` three times, the `&` in `for &x in &nums` and in
`|&x|`, the `&Vec` parameter and the `::` path. Rust types `let mut ans =
0` and the `[0; 101]` array's `0` as `i32` from their later uses; under
design.md §8 an operator's operand does not fix a literal's type, so both
take the default `i64`, and the second and third rounds write the fixes
the ruling names: the annotation `let mut ans: i32 = 0` at the binding
(B-2026-11-08-20) and the suffix `[0i32; 101]` in the fill
(B-2026-11-08-53). The fourth drops the wrapper's `ref`, which a bare
parameter already is.

## Benchmarks

The bench builds 20000 arrays of 200 values up to 100 once in all five
languages and runs the ★ arm on each for 25 rounds, `k` moving with the
round: 500000 calls, 100 million values counted. Every implementation
prints `500000 calls: sum 99497483, checksum 393192376`. Every language
allocates the 101 counts per call, as the Kāra program does.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with kara `64bba595f2` on LLVM 22:

| | time | median |
|---|---|---|
| Rust (`rustc -O`) | 0.641 to 0.673 s | 0.649 s |
| C (`clang -O3`) | 0.670 to 0.712 s | 0.690 s |
| Go | 0.709 to 0.808 s | 0.723 s |
| Kāra (`karac build`) | 0.726 to 0.760 s | 0.744 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.728 to 0.772 s | 0.749 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.761 to 0.819 s | 0.781 s |
| Python | 9.9 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`, the
sequential lane. A plain `karac build` parallelizes nothing here: its user
time (0.721 s) is not above its real time (0.744 s).

The sequential Kāra program is 0.96x Rust under overflow checks and 1.09x
C.