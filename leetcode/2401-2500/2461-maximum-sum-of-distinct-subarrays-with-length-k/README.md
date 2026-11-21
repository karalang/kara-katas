# 2461. Maximum Sum of Distinct Subarrays With Length K

You are given an integer array `nums` and an integer `k`. Find the
maximum subarray sum of all the subarrays of `nums` that meet the
following conditions:

- The length of the subarray is `k`, and
- All the elements of the subarray are **distinct**.

Return *the maximum subarray sum of all the subarrays that meet the
conditions*. If no subarray meets the conditions, return `0`.

*A **subarray** is a contiguous non-empty sequence of elements within an
array.*

```
nums = [1,5,4,2,9,9,9], k = 3  ->  15
nums = [4,4,4], k = 3          ->  0
```

**Constraints:** `1 <= k <= nums.length <= 10^5`;
`1 <= nums[i] <= 10^5`.

There are `n - k + 1` windows, and checking each afresh is O(n k), up to
about `2.5 * 10^9`. But neighbouring windows share all but two values,
so a window can slide: a count of each value in it says whether it is
distinct, since it is exactly when it holds `k` different values, and
its sum changes by the value entering less the one leaving. The values
are positive, so a sum of 0 only ever means no window qualified.

## Approaches

| file | mechanism |
|---|---|
| `distinct.kara` ★ | a sliding window of `k` with a `Map` counting each value in it, a key removed when its count falls to 0, and the window's sum; the window is distinct when the map holds `k` keys. O(n) |
| `distinct_naive.kara` | the statement read directly: every subarray of length `k`, its values put in a `Set` to see whether they are distinct, and its sum taken when they are. O(n k) |
| `distinct_last.kara` | the last place of each value: walking right, a window ending here can start no earlier than one past the latest repeat seen, so it is distinct when that bound is `k` or more places back, and its sum comes from prefix sums. O(n) |
| `distinct_shrink.kara` | a window that grows and shrinks over a `Set`: before a value enters, the front is dropped until the value is not in the set, and a window that reaches `k` values is a candidate and then loses its front too. O(n) |
| `distinct_iter.kara` | iterators: the prefix sums by `scan`; the earliest start of a distinct window ending at each place by `enumerate` and `scan` over a `Map` of last places; then the windows that start no earlier, by `filter` and `map`, and the largest sum by `max`. O(n) |
| `distinct_solution.kara` | LeetCode's Rust template: `Vec<i32>` and `k: i32` in, `i64` out; a window over a `HashMap<i32, i32>` of counts, each raised by `*m.entry(x).or_insert(0) += 1` and lowered through `get_mut`, and the sum kept by `as i64`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 14 lines: LeetCode's two examples; then five
more, `k` of 1, `k` the whole array, a repeat only at the two ends, a
repeat that rules out the first window, and the best window at the very end;
2000 distinct values from `10^5` down with `k` of 1000 and of 2000, the
constraints' largest values, and 2000 equal ones; `10^5` random values
from 1 to `10^5`, the constraints' longest, with `k` of 5 and of 40, and
`10^5` from 1 to 50 with `k` of 8; and 3000 random arrays of 1 to 12
values from 1 to 6, each with a random `k`, as a checksum. The long
arrays keep `k` small, since the naive arm is O(n k). `distinct.py`
mirrors the ★ arm and its output is byte-identical, and the mirror was
checked on every array of 1 to 7 values from 1 to 4, with every `k`,
against every window's set of values and sum.

`check` first reports 8 errors on the template, and `karac fix` carries
it in one call, reporting 15 edits: the `use` line deleted; the
brackets of `Vec<..>` and `HashMap<..>`, and `HashMap` written `Map`;
`HashMap::new` written `Map.new`; `k as usize` written `k as i64`, since
lengths and indices are `i64` in Kāra; each `as i64` on an `i32` dropped,
the widening being implicit; the `&` on each key passed to `get_mut` and
`remove` dropped; `&&` written `and`; and `struct Solution;` given its
braces. `*m.entry(..).or_insert(0) += 1`, `get_mut(..).unwrap()` and
`*c -= 1` stand as Kāra.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every subarray of length `k` taken as its own list, its
values distinct when no two places in it hold the same value, compared
pair by pair, and the largest sum of a distinct one kept, 0 when there
is none. No count or set is kept. It checks 300 random arrays of 1 to 12
values from 1 to 6; then 30 of up to 200 values from 1 to 1000; then 30
of up to 200 values from 1 to 20; each with a random `k` from 1 to the
length, at most 30. All 360 are drawn before any arm answers; each
case's constant for P3 is drawn as the case is checked.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | the array reversed: the same answer |
| P3 | every value raised by one constant below 1000: the answer plus `k` times it, or 0 if it was 0 |
| P4 | `k` of 1: the largest value |
| P5 | the array followed by itself: an answer no smaller |
| P6 | each arm agrees with at least three of the other five |

P2 holds because a window reversed is a window with the same values. P3
holds because raising every value keeps every equality and adds `k`
times the constant to every window's sum. P4 holds because a single
value is always distinct. P5 holds because every window of the array is
still a window of the doubled one.

The differential prints `360 cases: checksum 356566899, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and takes every window's set. On a failure it prints the
first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the key kept at a count of 0 | P1 151, P2 182, P4 270, P6 151 |
| M2 | ★: the leaving value never subtracted | P1 190, P2 80, P3 190, P4 340, P6 190 |
| M4 | ★: the window one too long | P1 183, P2 170, P3 148, P4 283, P6 183 |
| M7 | naive: the last window never tried | P1 74, P2 71, P4 67, P6 74 |
| M8 | naive: the window read one short | P1 234, P4 360, P6 234 |
| M10 | naive: the first value counted twice | P1 234, P2 134, P3 234, P4 360, P6 234 |
| M12 | last: the bound one place early | P1 65, P2 38, P6 65 |
| M13 | last: the bound allowed back | P1 46, P2 33, P6 46 |
| M14 | last: the last place never updated | P1 50, P2 42, P6 50 |
| M17 | shrink: the front dropped once at most | P1 46, P2 59, P3 51, P6 46 |
| M18 | shrink: the front kept after a full window | P1 92, P2 115, P4 229, P6 92 |
| M19 | shrink: the front value never subtracted | P1 82, P2 109, P3 86, P6 82 |
| M23 | iter: the prefix one value short | P1 122, P2 120, P3 24, P4 67, P6 122 |
| M25 | iter: the first window skipped | P1 69, P2 71, P4 54, P6 69 |
| M26 | iter: every window accepted | P1 176, P6 176 |
| M28 | solution: the leaving value added | P1 190, P2 186, P3 190, P4 340, P6 190 |
| M30 | solution: the answer started at 100 | P1 327, P3 327, P4 330, P6 327 |

P1 and P6 kill all seventeen, P2 fourteen, P4 eleven and P3 eight. P5
kills none of the kept ones; of the thirty-one it kills only the naive
arm's least kept (M11), whose answer can fall when windows are added.

Fourteen are not kept. Six fail exactly as a kept one: the ★ arm's first
full window never counted (M5) as the iter arm's first window skipped
(M25); the naive arm's sum of every window kept (M9) as the iter arm's
every window accepted (M26); the iter arm's bound one place early and
bound reset at each repeat (M22, M24) as the last arm's (M12, M13); and
the template's count never lowered and window one too long (M27, M29)
as the ★ arm's key kept at a count of 0 and window one too long (M1,
M4). Six fail apart from every kept one and were left out because those
arms keep their share already: the ★ arm's window of `k - 1` keys taken
as distinct (M3), which fails exactly as the template's (M31); the ★
arm's best started at 1 (M6); the naive arm's least kept (M11); the last
arm's window read one place late (M15); and the shrink arm's entering
value added twice (M21).

One ends in a runtime error, not a wrong answer, under both backends:
the last arm's window one short accepted (M16) reads `prefix[i + 1 -
k]` when only `k - 1` values have been seen, one place before the
array.

One survives, and is equivalent: the shrink arm's window of more than
`k` accepted (M20). The window never holds more than `k` values: each
value enters one at a time, and as soon as `k` are held the front is
dropped, so `>= k` and `== k` are the same test.

## Verification

Every arm prints the same output as `distinct.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` every arm takes 1.1 to 3.4 s but the naive arm,
5.3 s, and the differential 1.9 s; under `karac __mir-llvm-asan` the
differential takes 1.0 s and under `karac run` 0.6 s.

## Benchmarks

The bench builds 10 arrays of `10^5` values from 1 to 2000 once from its
own generator, so repeats inside a window are common, then makes 28
passes; each sets one value of every array from the checksum so far, so
no answer carries over, then answers every array with `k` of `5 + 7p mod
40`, folding the answer plus the pass into the checksum. The bench uses
the ★ arm, the window of counts, in all five languages. Every
implementation prints `28 passes over 10 arrays of 10^5: checksum
786296436`. The counts are the language's own hash map, `Map` in Kāra,
`HashMap` in Rust, `map` in Go and `dict` in Python; C has none, and
uses an open-addressing table of `2^12` slots keyed by the value, with
tombstones for removed keys, cleared for every answer.

BENCHTAB
