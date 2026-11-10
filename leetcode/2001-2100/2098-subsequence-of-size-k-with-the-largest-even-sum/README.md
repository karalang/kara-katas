# 2098. Subsequence of Size K With the Largest Even Sum

You are given an integer array `nums` and an integer `k`. Find the
largest even sum of any subsequence of `nums` that has a length of `k`.

Return this sum, or `-1` if such a sum does not exist.

A subsequence is an array that can be derived from another array by
deleting some or no elements without changing the order of the remaining
elements.

```
nums = [4,1,5,3,1], k = 3  ->  12
nums = [4,6,2], k = 3      ->  12
nums = [1,3,5], k = 1      ->  -1
```

**Constraints:** `1 <= nums.length <= 10^5`; `0 <= nums[i] <= 10^5`;
`1 <= k <= nums.length`.

The order does not matter, only which `k` numbers are taken. The `k`
largest make the largest sum; when it is odd, the best even sum changes
one number taken for one left out of the other parity, which flips the
sum's parity at the least cost. Another reading counts the odd numbers
taken: an even sum takes an even count of them, and for each count the
best is the largest odds with the largest evens.

## Approaches

| file | mechanism |
|---|---|
| `even_sum.kara` ★ | a copy sorted largest first with `sort_by`, the first `k` summed with `sum()` over a slice; when odd, the smallest odd and even taken and the largest odd and even left found with `filter` and `min`/`max` over the two slices, the two swaps compared through `if let` on tuples of `Option`s. O(n log n) |
| `even_sum_count.kara` | a counting sort: a `Vec.filled(100001, 0)` of counts walked down from the largest value, taking `k` numbers and noting the smallest of each parity taken and the largest of each left, in two-slot arrays indexed by `v % 2`. O(n + 10^5) |
| `even_sum_prefix.kara` | odds and evens split with `partition`, each sorted largest first and summed into prefixes; every even count of odds `2i` with the `k - 2i` largest evens tried. O(n log n) |
| `even_sum_heap.kara` | one pass with a smallest-first `PriorityQueue` holding the `k` largest so far; whatever is pushed out is left out for good and noted, what stays is drained for the sum and the smallest taken of each parity. O(n log k) |
| `even_sum_pairs.kara` | a `struct Picker` of the odds and the evens largest first and a cursor into each: an odd `k` first takes the largest even, then two at a time, the larger of the next two odds and the next two evens, matched as a tuple of `Option`s with a guard |
| `even_sum_solution.kara` | LeetCode's Rust template (`mut nums: Vec<i32>`, `nums.sort()`, `for &x in &nums[n - k..]`, the smallest taken of each parity in `[i32::MAX; 2]` and the largest left in `[-1i32; 2]`, both indexed by `(x & 1) as usize`), carried by `karac fix` in three rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 14 lines: LeetCode's three examples and five
more, each list with its answer; then how many of 3000 random lists of
1 to 30 numbers (below 10, 100 or 10^5 + 1 in turn), each asked for a
random `k`, have no even sum, and a checksum of the answers; then the
constraints' largest, 10^5 random numbers up to 10^5 asked for three
`k`, 10^5 odd numbers asked for `k` odd and even, and 10^5 copies of
10^5. `even_sum.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every choice of `k` of the numbers, by bit mask, and the
largest even sum among them, or -1. It checks 300 random lists of 1 to
10 numbers below 10; then 20 lists of 1 to 10 odd numbers below 20; then
20 lists of 1 to 12 numbers below 50000 (so that doubled they stay
within the constraints); each with a random `k`. All 340 are drawn
before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer is -1 or even, and no more than the sum of the `k` largest |
| P3 | the numbers in reverse order give the same answer |
| P4 | every number doubled: the answer is twice the sum of the `k` largest |
| P5 | every number 2 more: the answer is `2k` more, or -1 again |
| P6 | each arm agrees with at least three of the other five |

The differential prints `340 lists: checksum 39155145, 12240 checks over
6 arms: 0 failures` under every lane in Verification; the checksum of
the literal answers was checked against a Python reading of the same
lists with `itertools.combinations`. On a failure it prints the first
ten and then the count by property.

## Mutation testing

Thirty edits to the differential, five to each of its arms, each run
under `karac __mir-llvm-run` and `karac __mir-run`. Seventeen are kept,
three to each Kāra arm and two to the Rust-template arm. Each kept one
is killed, fails the same way under both backends and not by a crash,
and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: sorted smallest first | P1 162, P4 244, P6 162 |
| M2 | ★: an odd sum returned as it is | P1 340, P2 271, P4 340, P6 340 |
| M3 | ★: the even brought in from those taken | P1 117, P2 58, P6 117 |
| M4 | count: one of each value taken | P1 95, P4 129, P5 49, P6 95 |
| M5 | count: the same parity brought in | P1 113, P2 87, P5 40, P6 113 |
| M6 | count: zero never counted | P1 18, P5 18, P6 18 |
| M7 | prefix: odd counts of odds tried | P1 170, P2 170, P6 170 |
| M8 | prefix: the evens one short | P1 116, P4 96, P6 116 |
| M9 | prefix: each prefix only its last number | P1 209, P2 166, P4 240, P5 212, P6 209 |
| M10 | heap: the last odd left out noted, not the largest | P1 2, P3 5, P6 2 |
| M11 | heap: an odd brought in for the odd | P1 82, P2 65, P5 29, P6 82 |
| M12 | heap: a zero always left out | P1 57, P5 57, P6 57 |
| M13 | pairs: an odd `k` starting from the smallest even | P1 97, P4 159, P6 97 |
| M14 | pairs: a pair of odds moving on by one | P1 45, P2 44, P6 45 |
| M15 | pairs: `k = 1` without its even | P1 76, P2 49, P4 97, P5 56, P6 76 |
| M16 | solution: a zero always left out | P1 66, P2 29, P5 66, P6 66 |
| M17 | solution: the numbers never sorted | P1 109, P3 142, P4 194, P6 109 |

P1 and P6 kill all seventeen, P2 nine, P4 and P5 eight each, and P3
two. P3, the list reversed, sees only the edits whose answer depends on
the order the numbers come in: the heap arm noting the last odd pushed
out rather than the largest (wrong only twice on the lists themselves,
but five times reversed), and the Rust arm never sorting. P4, every
number doubled, makes every sum even, so it sees exactly the edits that
get the `k` largest wrong (M1, M2, M4, M8, M9, M13, M15, M17) and none
of those that only get the swap wrong. P5, every number 2 more, moves
the zeros: it sees the edits that treat zero apart (M6, M12, M16) and
those whose wrong swap lands differently once the numbers move (M4, M5,
M9, M11, M15). P2 sees an answer that is odd or larger than the `k`
largest allow (M2, M3, M5, M7, M9, M11, M14, M15, M16).

Of the thirty, thirteen were not kept, and none survives. Six fail the
same way as another and were left out in pairs: the largest odd taken
given way (★ and heap arms: P1 24, P6 24); the largest of a parity
noted as taken and the smallest noted as left (count arm: P1 39, P6
39); one fewer kept in the heap and the Rust adapter asking for one
fewer (P1 297, P4 301, P5 323, P6 297). Seven are killed with checks of
their own but were left out because their arm keeps its share: the ★
arm's odd alone given way (P1 30, P6 30), the prefix arm's all odds
never tried (P1 40, P6 40) and no odds never tried (P1 118, P4 340, P6
118), the pairs arm's smaller pair taken (P1 55, P6 55) and running out
of pairs with the sum so far (P1 23, P5 23, P6 23), and the Rust arm's
largest taken noted (P1 113, P6 113) and same parity brought in (P1
126, P2 109, P6 126).

## Verification

Every arm prints the same output as `even_sum.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them.

Under `karac __mir-run` the arms take 2.6 s to 15.2 s, except the
counting arm, 42.7 s: each of its 3000 small lists fills and walks a
table of 100001 counts. The differential takes 19.8 s, most of it the
same table (timed while other work shared the machine).

The prefix arm met a gap in `karac fix`. It was first written in Rust's
shape, `let (mut odds, mut evens): (Vec[i64], Vec[i64]) =
nums.iter().partition(..)`. The fix moved the `mut` before the pattern;
then the declaration was refused, rightly: `partition` keeps its items
as they come (library/iterators.md, "Items read through a reference"),
`ref i64` from `iter()`, so the halves are `Vec[ref i64]`, where
`collect` would have read them as values. The refusal carried no repair.
`karac fix` now writes `.cloned()` before the `partition` when the
declared halves hold the items' own type. Fixed in kara PARTSHA, test
`tests/kata_2098_partition_cloned_fix.rs`.

`karac fix` carries the template in three rounds of 17, 6 and 1 edits:
Rust's spellings (`Vec<i32>` to brackets, `&nums[..]` to `nums[..]` and
the patterns' `&` dropped, `i32::MAX` to `i32.MAX`, `&&` to `and`,
`Solution::` to `.`, `struct Solution;` to `struct Solution {}`), and the
parameter `mut nums` to `own nums` with a `let mut nums = nums;`; then
the `as usize` casts to `as i64` and the `as i64` widenings dropped;
then the adapter's `ref` parameter to a bare one, which borrows already.

## Benchmarks

The bench asks 200 lists of 100000 numbers up to 10^5, the constraints'
largest, each for a random `k`, with the ★ arm in all five languages: a
sorted copy, largest first (`sort_by`, `sort_by`, `qsort`, `sort.Slice`,
`sorted`), then the sum of the first `k` and, when it is odd, one pass
over each part for the swaps. Every implementation prints `200 answers:
sum 653088378074, checksum 820060632`.

BENCHTAB
