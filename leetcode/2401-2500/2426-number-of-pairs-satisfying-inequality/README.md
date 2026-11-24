# 2426. Number of Pairs Satisfying Inequality

You are given two **0-indexed** integer arrays `nums1` and `nums2`, each
of size `n`, and an integer `diff`. Find the number of **pairs**
`(i, j)` such that:

- `0 <= i < j <= n - 1` **and**
- `nums1[i] - nums1[j] <= nums2[i] - nums2[j] + diff`.

Return *the **number of pairs** that satisfy the conditions.*

```
nums1 = [3,2,5], nums2 = [2,2,1], diff = 1     ->  3
nums1 = [3,-1], nums2 = [-2,2], diff = -1      ->  0
```

**Constraints:** `n == nums1.length == nums2.length`;
`2 <= n <= 10^5`; `-10^4 <= nums1[i], nums2[i] <= 10^4`;
`-10^4 <= diff <= 10^4`.

Moving the `j` terms to one side, the inequality is `a[i] <= a[j] +
diff` with `a[k] = nums1[k] - nums2[k]`. So the task counts, over one
array, the pairs `i < j` whose earlier value is at most the later one
plus `diff`: the shape of counting inversions, which a merge sort or a
Fenwick tree over the values does in O(n log n).

## Approaches

| file | mechanism |
|---|---|
| `pairs.kara` ★ | a merge sort over `a`: once both halves are sorted, a pointer into the left half moves on while its value is at most `a[j] + diff`, and it only moves forward as `j` rises through the right half, so each `j` adds the pointer's distance from the start. O(n log n) |
| `pairs_naive.kara` | the statement read directly: every pair `i < j` tested as written and counted. O(n^2) |
| `pairs_fenwick.kara` | a `Fenwick` struct over the values of `a`, shifted by 30001 so every index is at least 1: for each `j`, the earlier values at most `a[j] + diff` read off by a prefix sum, then `a[j]` added; the steps by `i & -i`. O(n log V) |
| `pairs_sorted.kara` | a sorted `Vec[i64]` of the values seen: for each `j`, `partition_point` counts those at most `a[j] + diff`, and `a[j]` is inserted where `partition_point` puts it. O(n log n) searches and O(n^2) moves at worst |
| `pairs_iter.kara` | iterators: `a` by `zip` and `map`, then for each `j` the earlier `i` with `a[i] <= a[j] + diff` by `filter` and `count`, added by `sum`. O(n^2) |
| `pairs_solution.kara` | LeetCode's Rust template: a `struct Bit` of `Vec<i64>` with `usize` indices stepped by `i & i.wrapping_neg()`, and the differences shifted by 30001 before they index it, `as usize`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 10 lines: LeetCode's two examples; all values
equal; a falling and a rising difference against `diff` 0; a `diff` too
small and one just large enough for the one pair, at the constraints'
extremes; then `10^4` values from `-10^4` to `10^4` against diffs of
`-100`, 0 and `10^4`, and `10^4` values from -3 to 3 against `diff` 0,
full of ties; and 3000 random cases of 2 to 12 values from -5 to 5,
`diff` from -5 to 5, as a checksum and the total. The largest cases
hold `10^4` values, not the constraints' `10^5`, because the naive and
iter arms test every pair. `pairs.py` mirrors the ★ arm and its output
is byte-identical, and the mirror was checked on 20000 random cases of
up to 10 values against every pair tested.

TEMPLATE

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every pair `i < j` tested as written, `nums1[i] - nums1[j] <=
nums2[i] - nums2[j] + diff`, with no difference array formed. It checks
300 random cases of 2 to 10 values from -1 to 1 up to -5 to 5, `diff`
from -5 to 5; then 30 of up to 200 values from -5000 to 5000, `diff`
from -5000 to 5000; then 30 of up to 200 values from -2 to 2, `diff`
from -1 to 1, full of ties. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | `nums1` shifted by one constant from -10 to 10: the same answer |
| P3 | both lists reversed and negated: the same answer |
| P4 | `diff` raised by 1: an answer no smaller, and none past `n (n - 1) / 2` |
| P5 | the lists swapped and `diff` made `-diff - 1`: the two answers add up to `n (n - 1) / 2` |
| P6 | each arm agrees with at least three of the other five |

P2 holds because the shift cancels in `nums1[i] - nums1[j]`. P3 holds
because reversing turns the pair `i < j` into `n - 1 - j < n - 1 - i`,
and negating both lists turns the inequality back to the one it was. P4
holds because a larger `diff` only lets more pairs through. P5 holds
because swapping the lists negates `a`, so the swapped count with
`-diff - 1` is of the pairs with `a[i] > a[j] + diff`, exactly the pairs
the original leaves out.

The differential prints `360 cases: checksum 565056678, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and tests every pair. On a failure it prints the first
ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a range of two never counted | P1 286, P3 204, P5 335, P6 286 |
| M4 | ★: the merge reversed | P1 233, P3 196, P5 171, P6 233 |
| M6 | ★: the last merged value never written back | P1 191, P3 197, P5 209, P6 191 |
| M8 | naive: a strict inequality | P1 192, P5 235, P6 192 |
| M10 | naive: the first index never paired | P1 276, P3 209, P5 360, P6 276 |
| M11 | naive: diff subtracted | P1 302, P4 189, P5 235, P6 302 |
| M14 | fenwick: queries capped at zero | P1 210, P2 207, P3 234, P5 293, P6 210 |
| M15 | fenwick: nodes counted, not their counts | P1 360, P2 304, P3 300, P4 333, P5 360, P6 360 |
| M16 | fenwick: the climb twice as far | P1 259, P2 210, P3 206, P4 100, P5 322, P6 259 |
| M17 | sorted: each value stored one higher | P1 186, P3 80, P5 230, P6 186 |
| M18 | sorted: each value appended | P1 196, P3 196, P5 210, P6 196 |
| M21 | sorted: the values above counted | P1 348, P4 189, P6 348 |
| M22 | iter: each index paired with itself | P1 192, P4 149, P5 360, P6 192 |
| M24 | iter: the lists added | P1 273, P5 264, P6 273 |
| M26 | iter: at most one pair per j | P1 260, P3 166, P5 313, P6 260 |
| M28 | solution: the sum stopped above the shift | P1 284, P2 209, P3 254, P5 330, P6 284 |
| M30 | solution: the answer started at 1 | P1 360, P4 81, P5 360, P6 360 |


P1 and P6 kill all seventeen, P5 sixteen, P3 eleven, P4 six and P2
four.

Fourteen are not kept. Eleven fail exactly as a kept one: the ★ and
Fenwick arms' strict inequality (M2, M12) as the naive arm's (M8); the ★
arm's failing pairs counted (M3) as the sorted arm's values above
counted (M21), both the complement of the answer; the naive arm's index
paired with itself and the Fenwick and sorted arms' value counted
against itself (M7, M13, M19) as the iter arm's index paired with itself
(M22), each adding the `n` pairs `(j, j)` when `diff >= 0`; the naive
arm's `nums2` differenced the wrong way (M9) as the iter arm's lists
added (M24), both reading `nums1[i] + nums2[i]`; the sorted arm's `diff`
subtracted and the iter arm's `diff` moved to the other side (M20, M23)
as the naive arm's `diff` subtracted (M11); and the iter arm's index 0
never paired and the template's first index skipped (M25, M31) as the
naive arm's first index never paired (M10). Three fail apart from
every kept one and were left out because those arms keep their share
already: the ★ arm's and the template's difference taken the other way
(M5, M29), which fail alike and which P1 and P6 alone catch, since
negating `a` keeps every other property; and the template's each value
added twice (M27).

The first run had no valid choice: the naive, sorted and iter arms'
mutations fell into six shared signatures between them, one short of
the seven they need. The sorted arm's strict inequality, a fourth
copy of one signature, was replaced by each value stored one higher
(M17), which fails apart.

## Verification

Every arm prints the same output as `pairs.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 1.1 to 4.9 s, but for the naive
and iter arms, which test every pair: on the cases of `10^4` values
that is `5 * 10^7` pairs each, and they take 70 s and 105 s there, 14 s
and 45 s under `karac __mir-llvm-asan`, and 1.2 s and 1.0 s under
`karac run`. The iter arm's pair is a closure call, which the
interpreter and the sanitized build pay for. The differential takes
9.1 s under `karac __mir-run`, 4.6 s under `karac __mir-llvm-asan` and
0.8 s under `karac run`.

## Benchmarks

The bench builds 10 cases once from its own generator, each two lists of
`10^5` values from `-10^4` to `10^4`, the constraints' largest, case `c`
taking `diff = 2000 c - 10^4`. It then makes 4 passes, pass `p` moving
every `diff` by `p - 2`, answering every case and folding the answer
plus the pass into the checksum. The bench uses the ★ arm, the merge
sort that counts while it merges, in all five languages. Every
implementation prints `4 passes over 10 cases of 10^5 values: checksum
816397970`. Every merge fills a fresh growable list, pushed one value at
a time (`Vec`, `Vec`, a slice by `append`, a Python list), and in C a
buffer grown by doubling with `realloc`, so each language pays for the
allocation the same way.

BENCHTAB
