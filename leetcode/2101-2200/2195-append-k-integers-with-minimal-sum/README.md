# 2195. Append K Integers With Minimal Sum

You are given an integer array `nums` and an integer `k`. Append `k`
**unique positive** integers that do **not** appear in `nums` to `nums`
such that the resulting total sum is **minimum**.

Return *the sum of the* `k` *integers appended to* `nums`.

```
nums = [1, 4, 25, 10, 25], k = 2  ->  5     (2 and 3)
nums = [5, 6],             k = 6  ->  25    (1, 2, 3, 4, 7 and 8)
```

**Constraints:** `1 <= nums.length <= 10^5`; `1 <= nums[i] <= 10^9`;
`1 <= k <= 10^8`.

The smallest `k` positive numbers the list does not hold. The numbers
sorted, and the gaps between them walked from 0 up: each gap's missing
numbers taken, as many as are still wanted, and added as a run by the sum
of an arithmetic series. O(n log n).

## Approaches

| file | mechanism |
|---|---|
| `minimal.kara` ★ | the numbers sorted and the gaps walked from 0 up, each gap cut to what is still wanted and added by the sum of an arithmetic series; past the largest number the rest run on |
| `minimal_bump.kara` | 1 to k taken first, then the distinct numbers walked in order from a `SortedSet`: one at or below the largest taken is already there, so the next free number is taken in its place, which adds the difference |
| `minimal_search.kara` | the largest number appended found by binary search, the smallest x with k numbers missing up to it; the distinct numbers sorted, with prefix sums, and counted by `partition_point`; the sum is 1 to x less the distinct numbers up to x |
| `minimal_struct.kara` | a `struct Gaps` over the sorted numbers with `impl Iterator`, each `next` the next run of missing numbers as a `Gap` of its first and last (the last run open to the top), taken from the front |
| `minimal_iter.kara` | `once(0)` chained before the numbers, sorted and deduplicated; their `windows(2)` the gaps, `scan`ned with the count still wanted as the state, each handing on what it takes and its series, then `sum`med; the rest run on past the largest |
| `minimal_solution.kara` | LeetCode's Rust template: `mut nums: Vec<i32>`, `k: i32`, `-> i64`, `sort_unstable()`, `dedup()`, `for &x in &nums`, `struct Solution;`, `Solution::`, the bump written as Rust; carried by `karac fix` in two rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's two examples and four more
(one number, the numbers 1 to 5 already there, repeats, and the
constraints' largest number with the largest k), each with its sum; then
a checksum over 3000 random cases, of 1 to 30 numbers below 10, 100 and
10^9 in turn with k up to 50, 1000 and 10^8; then the constraints'
longest, 10^5 numbers below 10^9 with k = 10^8, and the numbers 1 to
10^5 shuffled with k = 1. `minimal.py` mirrors the ★ arm and its output
is byte-identical.

`karac fix` carries the template in two rounds of 8 and 1 edits: first
Rust's spellings (`mut nums: Vec<i32>` to `nums: own Vec[i32]` with a
`let mut nums = nums;`, `for &x in &nums` to `for x in ref nums`,
`struct Solution;` to `struct Solution {}`, `Solution::` to `.`); then
`sort_unstable()` to `sort()`.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the positive numbers counted up from 1, each one the list does
not hold appended, until k are; no series and no sort. It checks 300
random cases of 1 to 10 numbers of 1 to 20, k from 1 to 30; then 30
where the list is 1 to m shuffled, so nothing is missing below m; then
30 of numbers up to 10^9 with k from 70000 to 99999, whose sums pass
2^31. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the sum is the statement read literally |
| P2 | the sum lies between 1 + .. + k and that plus k times the count of distinct numbers |
| P3 | every number listed twice: the same sum |
| P4 | the list reversed: the same sum |
| P5 | k one more: the sum grows by a number the list does not hold, larger than the growth from k - 1 to k |
| P6 | each arm agrees with at least three of the other five |

P2 holds since the smallest k positive numbers are the least any k can
sum to, and each number the list holds among them pushes one appended
number up by at most k. P5 holds since the k + 1st number appended is
missing from the list and larger than the kth.

The differential prints `360 cases: checksum 980382037, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading of the same
cases. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to each
other arm, each run under `karac __mir-llvm-run` and `karac __mir-run`.
Seventeen are kept, three to each Kāra arm and two to the Rust-template
arm. Each kept one is killed, fails the same way under both backends and
not by a crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a gap counted one wider | P1 251, P5 25, P6 251 |
| M2 | ★: the list unsorted | P1 233, P4 219, P5 25, P6 233 |
| M5 | ★: a series one short | P1 360, P2 209, P5 178, P6 360 |
| M7 | bump: a number equal to the top passed by | P1 43, P5 51, P6 43 |
| M9 | bump: the bump by the old top | P1 288, P5 36, P6 288 |
| M10 | bump: the series to k - 1 | P1 360, P2 133, P5 36, P6 360 |
| M12 | search: the repeats kept | P1 115, P2 20, P3 296, P5 1, P6 115 |
| M13 | search: the search one low | P1 202, P2 41, P5 13, P6 202 |
| M15 | search: the first enough passed | P1 145, P2 21, P5 11, P6 145 |
| M18 | struct: a gap's seen left behind | P1 251, P2 244, P3 198, P5 77, P6 251 |
| M19 | struct: no tail gap | P1 202, P2 195, P5 215, P6 202 |
| M20 | struct: the series from the second | P1 360, P2 77, P5 30, P6 360 |
| M23 | iter: no dedup | P1 144, P2 20, P3 360, P6 144 |
| M24 | iter: a gap counted one wider | P1 288, P5 56, P6 288 |
| M26 | iter: the state never spent | P1 128, P2 91, P5 61, P6 128 |
| M30 | solution: the sum in i32 | P1 30, P2 30, P6 30 |
| M31 | solution: the bump by one | P1 276, P5 82, P6 276 |

P1 and P6 kill all seventeen, P5 fifteen, P2 eleven, P3 three and P4
one. P5 misses the iter arm's repeats kept (M23): each repeat's gap of
length -1 subtracts the repeat and asks for one number more, so the sum
is wrong but still grows by a missing number. It also misses the sum's
first series kept in i32 (M30), which only the 30 large cases reach,
since the wrap at k and at k + 1 is the same multiple of 2^32. P2 misses
the six edits whose sums stay inside the bounds: a gap one wider (M1,
M24), the list unsorted (M2), a number equal to the top passed by (M7),
the bump by the old top (M9) and the bump by one (M31). P3 sees only
three: the repeats kept (M12, M23) and the struct arm's seen left
behind (M18); P4 only the list unsorted (M2), since every other arm
sorts first.

Of the thirty-one, fourteen were not kept. Three are equivalent: the ★
arm's last number set at a repeat (M4), since a repeat equals it; the
bump arm's walk carried on past the top (M11), since once a number is
above the top every later one is too; and the search arm's prefix
counted below the answer rather than at it (M16), since the answer is
missing from the list. Seven fail all alike and are left out to keep
three to an arm: the tail run started one low (M3, M21, M25, across
three arms), the gap below the first number skipped (M6, M22), and the
repeats kept in the bump and template arms (M8, M28). Two fail as a
kept one does: the struct arm's gap one longer (M17) as M1, and the
template's number equal to the top passed by (M29) as M7. Two more fail
their own way and are left out for the count: the search arm's missing
numbers counted below x (M14), and the template adapter's k one more
(M27).

## Verification

Every arm prints the same output as `minimal.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the struct, search, ★ and template arms take
0.7 s to 1.3 s and the iter arm 3.3 s; the bump arm, which builds a
`SortedSet` of each list, takes 12.3 s. The differential
takes 2.1 s.

## Benchmarks

The bench builds 10^5 numbers below 10^9 once, then solves 300 times
with the ★ arm in all five languages, k from 10^8 down by 1000; each
solve sorts its own copy. Every implementation prints `300 solves over
100000 numbers: checksum 145155237`.

BENCHTAB
