# 2366. Minimum Replacements to Sort the Array

You are given a **0-indexed** integer array `nums`. In one operation
you can replace any element of the array with **any two** elements that
**sum** to it.

- For example, consider `nums = [5,6,7]`. In one operation, we can
  replace `nums[1]` with `2` and `4` and convert `nums` to `[5,2,4,7]`.

Return *the minimum number of operations to make an array that is
sorted in **non-decreasing** order*.

```
nums = [3,9,3]      ->  2
nums = [1,2,3,4,5]  ->  0
```

**Constraints:** `1 <= nums.length <= 10^5`; `1 <= nums[i] <= 10^9`.

The last value never needs to change, since splitting it only lowers
what the values before it must fit under. Going from the right, a value
`v` over the bound `b` left by the values after it must be split into
at least `k = ceil(v / b)` pieces, in `k - 1` operations, and splitting
it into exactly that many as evenly as possible leaves the largest
smallest piece, `floor(v / k)`, as the bound for the values before it.
`10^5` values of `10^9` before a 1 take `99998999900001` operations,
past `i32`, which is why LeetCode's answer is an `i64`.

## Approaches

| file | mechanism |
|---|---|
| `replace.kara` ★ | greedy from the right: a value that fits becomes the bound, and a value over it is split into `ceil(v / b)` pieces and leaves `floor(v / k)`. O(n) |
| `replace_search.kara` | the same greedy, with the number of pieces found by binary search: the fewest `k` whose largest piece `ceil(v / k)` fits under the bound. O(n log v) |
| `replace_recursive.kara` | recursion: the operations for the values up to place `i` under a bound are those for place `i` plus those for the values before it under the smallest of its pieces; one call per place, `10^5` deep on the long lines |
| `replace_divmod.kara` | the pieces counted by quotient and remainder, `v / b` and one more when `v % b` is not 0, walking the values by `rev` and `skip` |
| `replace_iter.kara` | iterators: the values from the right but the last folded into (operations, bound) |
| `replace_solution.kara` | LeetCode's Rust template: the bound from `*nums.last().unwrap() as i64` and the walk by `iter().rev().skip(1)`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 7 lines: LeetCode's two examples; one value;
`10^5` values of `10^9` before a 1; `10^5` values falling from `10^9`;
`10^5` values rising; then 2000 random arrays of 1 to 40 values from 1
up to 1 to 60, with a checksum and how many are already sorted.
`replace.py` mirrors the ★ arm and its output is byte-identical, and
the mirror was checked on 1500 random arrays of up to 7 values up to 14
against a search that tries every number of pieces for every value and
every smallest piece those pieces could have.

`check` first reports 4 errors on the template, and `karac fix` carries
it in one call, reporting 5 edits: `struct Solution;` given its braces,
`Vec<i32>` its brackets, the `&` of `for &x` dropped, and `Solution::`
written with a dot. `*nums.last().unwrap() as i64` stands as Kāra.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: from the right, every way of splitting each value into `k`
parts that fit under the bound, with every smallest part those `k` parts
could have, tried, and the fewest operations kept, the answers for a
place and a bound kept in a table. No greedy choice of `k` or of the
smallest part. It checks 300 random arrays of 1 to 10 values from 1 up
to 1 to 20; then 30 of up to 2000 values up to `10^9`; then 30 of up to
300 values falling from up to 1000. All 360 are drawn before any arm
answers.

| | property |
|---|---|
| P1 | up to 10 values up to 20, the answer is the literal reading's |
| P2 | 0 exactly when the values never fall, and at most the sum of every value but the last less one |
| P3 | a 1 put in front: the same answer |
| P4 | the largest value appended: the same answer |
| P5 | the last value doubled: no more operations |
| P6 | each arm agrees with at least three of the other five |

P3 holds because a 1 fits under any bound, and P4 because the old last
value fits under the largest, so it stays whole and leaves the same
bound as before. P5 holds because a higher bound at the right end can
only leave each value before it as many pieces or fewer. The doubled
last value can pass `10^9`, outside the constraints, and stays inside
`i32`.

The differential prints `360 cases: checksum 540821640, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and runs the same search with `lru_cache`. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the pieces counted rounding down | P1 142, P2 42, P6 195 |
| M4 | ★: each split counted by its pieces | P1 231, P2 101, P6 291 |
| M6 | ★: a value that fits never lowers the bound | P1 128, P2 57, P4 234, P6 158 |
| M7 | search: the search stopping one short of v pieces | P1 161, P2 12, P6 186 |
| M8 | search: the pieces needing to fit strictly under the bound | P1 161, P2 8, P4 113, P6 207 |
| M11 | search: at least two pieces always | P1 219, P2 102, P3 360, P4 360, P6 259 |
| M12 | recursive: the first value skipped | P1 196, P2 21, P3 256, P6 256 |
| M13 | recursive: the bound passed on unchanged | P1 176, P2 57, P4 234, P6 227 |
| M14 | recursive: each split counted by its pieces | P1 264, P2 151, P3 360, P4 360, P6 324 |
| M17 | divmod: a split into two counted as none | P1 160, P2 41, P6 207 |
| M19 | divmod: half the pieces counted | P1 190, P6 250 |
| M21 | divmod: the second last value skipped too | P1 164, P2 25, P4 144, P6 205 |
| M22 | iter: the bound started one high | P1 60, P2 6, P4 71, P6 71 |
| M23 | iter: the bound one over the smallest piece | P1 200, P2 22, P4 71, P6 251 |
| M26 | iter: folded from the left | P1 215, P2 31, P3 227, P4 288, P5 195, P6 275 |
| M28 | solution: the bound the largest piece | P1 85, P6 129 |
| M31 | solution: the bound started at the first value | P1 122, P2 14, P3 262, P4 228, P6 162 |

P1 and P6 kill all seventeen, P2 fifteen, P4 ten, P3 five and P5 one.
P5, the last value doubled, fails only the fold from the left (M26):
every other edit still walks from the right, where a higher bound at
the end can only leave each value as many pieces or fewer, so it never
adds operations there. P3, a 1 put in front, fails the edits that skip
or misread the first value, or that count a value that fits: at least
two pieces always (M11), the first value skipped (M12), each split
counted by its pieces (M14), the fold from the left and the bound
started at the first value (M31).

The divmod arm's first five held two crashes, its remainder test
inverted and its pieces sized one over the bound, each a division by
zero once a value that fits counted no pieces, and one edit that changes nothing, which
left it two to keep. The two that crashed were replaced by a split into
two counted as none (M17) and the bound what the last piece holds (M20).

Of the thirty-one, fourteen were not kept. The bound left as it was
after a split in the ★ and search arms (M2, M9) fail alike and apart
from every kept one, and were left out with nothing to keep them for.
The bound the largest piece in the ★ and recursive arms (M3, M16) fails
as in the template (M28); the ★ arm's first value never looked at (M5)
as the recursive arm's first value skipped (M12); each split counted by
its pieces in the search and iter arms (M10, M25) as in the recursive
arm (M14); the iter arm's bound never changed (M24) as the recursive
arm's bound passed on unchanged (M13); and the template's half the
pieces counted and second last value skipped (M29, M27) as the divmod
arm's (M19, M21). One piece too many when the bound divides, in the
recursive arm and the template (M15, M30), stops with a division by
zero: a value of 1 split into two pieces leaves a bound of 0. The
divmod arm's bound never above the last one (M18) changes nothing,
since `v / pieces` is never above the bound when `pieces` is at least
`v / bound`. Its bound what the last piece holds (M20) fails apart from
every kept one, and was left out to keep three to an arm.

## Verification

Every arm prints the same output as `replace.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.7 to 1.2 s but the search arm,
3.0 s, with up to 30 steps of binary search for each value; the
differential takes 2.4 s there and 0.53 s under `karac __mir-llvm-run`.

## Benchmarks

The bench builds 10 arrays of `10^5` values once from the harness's
generator, array 0 falling from `10^9` and array `a` above 0 holding
random values from 1 to `10^(a - 1)`, then makes 100 passes, pass `p`
folding each answer plus `p` into the checksum, with the ★ arm in all
five languages. Every implementation prints `100 passes over 10 arrays
of 10^5 values: checksum 991591990`. No implementation allocates in the
counted loop.

BENCHTAB
