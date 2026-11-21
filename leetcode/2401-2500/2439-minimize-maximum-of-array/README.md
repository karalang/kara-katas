# 2439. Minimize Maximum of Array

You are given a **0-indexed** array `nums` comprising of `n`
non-negative integers.

In one operation, you must:

- Choose an integer `i` such that `1 <= i < n` and `nums[i] > 0`.
- Decrease `nums[i]` by 1.
- Increase `nums[i - 1]` by 1.

Return *the **minimum** possible value of the **maximum** integer of
`nums` after performing **any** number of operations*.

```
nums = [3,7,1,6]  ->  5
nums = [10,1]     ->  10
```

**Constraints:** `n == nums.length`; `2 <= n <= 10^5`;
`0 <= nums[i] <= 10^9`.

Value only ever moves one place left, so the first `i + 1` values never
lose any of their sum to the rest, and the largest of them is at least
that sum's ceiling average. Every prefix gives such a bound, and the
largest of them is reached: levelling each prefix down to its own bound
never pushes a value past the largest. So the answer is the largest
ceiling average of any prefix, O(n) in one pass.

## Approaches

| file | mechanism |
|---|---|
| `minmax.kara` ★ | one pass: the running sum, and the largest `(sum + i) / (i + 1)` kept by `max`. O(n) |
| `minmax_naive.kara` | every prefix's bound computed afresh: the first `i + 1` values summed again from the start for each `i`. O(n^2) |
| `minmax_search.kara` | a binary search on the answer: a cap fits when, walking from the right, every value above it hands its excess to the one before, and the first value, with all it was handed, ends at most the cap. O(n log V) |
| `minmax_stack.kara` | a stack of levelled blocks, a `Block` struct of sum and length: each value starts a block, merged with the one below while its average is at least that one's, compared by cross multiplication in `i128`; the bottom block is the prefix of largest average. O(n) |
| `minmax_iter.kara` | iterators: the prefix sums by `scan`, their lengths by `enumerate`, each ceiling average by `map`, the largest by `max`. O(n) |
| `minmax_solution.kara` | LeetCode's Rust template: the values as `i32` read by `for (i, &x) in nums.iter().enumerate()`, the sum and answer declared `i64`, each widened by `as i64`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 10 lines: LeetCode's two examples; two zeros;
`10^9` after a zero; then `10^4` values with `10^9` first, with `10^9`
last, all `10^9`, rising by `10^5`, and random from 0 to `10^9`; and
3000 random arrays of 2 to 12 values from 0 to 20, as a checksum and the
total. The largest cases hold `10^4` values, not the constraints'
`10^5`, because the naive arm sums every prefix again. `minmax.py`
mirrors the ★ arm and its output is byte-identical, and the mirror was
checked on all 1799 arrays of 2 to 5 values from 0 to 4 (0 to 3 for
five values) against a search of every array the operation reaches.

`check` first reports 3 errors on the template, and `karac fix` carries
it in one call, reporting 7 edits: the brackets of `Vec<i32>`; the `&`
dropped from the pattern `&x`, since a Kāra pattern already matches
through a reference; `struct Solution;` given its braces; and, once the
template parses, the two `i as i64` casts on the index, which is
already an `i64`, and the harness's `as i64` on the `i64` the template
returns. `x as i64` on each `i32` value, the declared `i64`s and `ans as
i32` stand as Kāra.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: each cap tried from 0 upward, and for each the one operation
made one unit at a time, always at the rightmost value past the first
that is above the cap, until none is; the first cap that the first value
then fits under is the answer. No sum is taken and no average formed. It
checks 300 random arrays of 2 to 6 values from 0 to 9; then 30 of 2 to
12 values from 0 to 30; then 30 of 2 to 12 values, all 0 but one from 0
to 200 placed at random. The values stay small because the literal
reading moves one unit at a time. All 360 are drawn before any arm
answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | one unit moved one place left: an answer no smaller |
| P3 | every value times `k` from 2 to 5: between `k` times the answer less `k - 1`, and `k` times the answer |
| P4 | the answer is at least the first value and the whole array's ceiling average, and at most the largest value |
| P5 | a 0 appended: the same answer |
| P6 | each arm agrees with at least three of the other five |

P2 holds because the moved array is one the operation reaches from the
original, so whatever it reaches the original does too. P3 holds
because scaling a prefix's sum by `k` takes its ceiling average to
between `k` times it less `k - 1` and `k` times it. P4 holds because the
first value can only grow, the total never changes, and leaving the
array alone is allowed. P5 holds because the new prefix's average is the
whole array's spread over one more place, no more than the bound before
it.

The differential prints `360 cases: checksum 487912995, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and moves the same units. On a failure it prints the
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
| M1 | ★: the floor average | P1 152, P3 128, P4 81, P6 152 |
| M3 | ★: the first value skipped | P1 263, P2 78, P4 226, P6 263 |
| M5 | ★: each prefix one longer | P1 330, P4 262, P6 330 |
| M7 | naive: each prefix one short | P1 348, P4 280, P5 117, P6 348 |
| M9 | naive: the least bound kept | P1 315, P2 38, P4 282, P5 144, P6 315 |
| M11 | naive: the values summed from the end | P1 292, P2 77, P4 106, P5 334, P6 292 |
| M14 | search: the search below the largest | P1 127, P2 22, P3 127, P4 118, P6 127 |
| M15 | search: the search a step short | P1 183, P2 24, P3 188, P4 144, P6 183 |
| M16 | search: the walk stopped at the second value | P1 177, P2 25, P4 69, P6 177 |
| M17 | stack: the top block answered | P1 234, P2 83, P4 231, P5 317, P6 234 |
| M19 | stack: a merged block one longer | P1 156, P2 29, P4 75, P6 156 |
| M20 | stack: the larger sum kept on a merge | P1 192, P2 39, P4 172, P6 192 |
| M24 | iter: the least bound | P1 335, P4 322, P5 114, P6 335 |
| M25 | iter: the first prefix skipped | P1 336, P4 216, P6 336 |
| M26 | iter: the whole array never a prefix | P1 76, P4 76, P5 76, P6 76 |
| M28 | solution: each prefix two longer | P1 343, P3 86, P4 290, P6 343 |
| M30 | solution: one added at every value | P1 360, P3 339, P4 232, P5 360, P6 360 |


P1, P4 and P6 kill all seventeen, P2 nine, P5 seven and P3 five.

Fourteen are not kept. Six fail exactly as a kept one: the naive arm's
first value left out of every sum, the search arm's first value never
checked and the template's first value skipped (M8, M13, M31) as the ★
arm's first value skipped (M3), each answering as if the first value
were 0; the naive arm's whole array never a prefix (M10) as the iter
arm's (M26); the stack arm's floor average (M18) as the ★ arm's (M1);
and the iter arm's sum before each value (M22) as the naive arm's each
prefix one short (M7), both dividing the sum before a value by the
length after it. Two more pairs fail alike and apart from every kept
one, and neither is kept: the ★ arm's only the last prefix kept and the
search arm's carry let go below 0 (M2, M12), both answering the whole
array's ceiling average, since a negative carry lets a later gap absorb
an earlier excess; and the ★ arm's ceiling one too high and the iter
arm's ceiling always rounded up (M4, M23), `(sum + i + 1) / (i + 1)`
and `sum / (i + 1) + 1` being the same number. The rest fail apart
from every kept one and were left out because those arms keep their
share already: the ★ arm's and the template's sum reset to each value
(M6, M27), which fail alike, answering the largest value; the stack
arm's bottom block never merged (M21); and the template's least bound
(M29), which answers 0 from its start at 0.

## Verification

Every arm prints the same output as `minmax.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.3 to 1.0 s, but for the naive
arm, which sums every prefix again: on the cases of `10^4` values that
is `5 * 10^7` additions each, and it takes 33 s there, 9.8 s under
`karac __mir-llvm-asan`, and 0.5 s under `karac run`. The differential
takes 0.9 s under `karac __mir-run`, 0.6 s under `karac
__mir-llvm-asan` and 0.6 s under `karac run`.

## Benchmarks

The bench builds 10 arrays of `10^5` values from 0 to `10^9`, the
constraints' largest, once from its own generator. It then makes 100
passes; each sets one value of every array, so no answer can be carried
from one pass to the next, then answers every array, folding the answer
plus the pass into the checksum. The bench uses the ★ arm, the largest
ceiling average of any prefix, in all five languages. Every
implementation prints `100 passes over 10 arrays of 10^5 values:
checksum 410437515`.

BENCHTAB
