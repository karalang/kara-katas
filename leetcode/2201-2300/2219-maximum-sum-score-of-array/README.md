# 2219. Maximum Sum Score of Array

You are given a **0-indexed** integer array `nums` of length `n`.

The **sum score** of `nums` at an index `i` where `0 <= i < n` is the
**maximum** of:

- The sum of the **first** `i + 1` elements of `nums`.
- The sum of the **last** `n - i` elements of `nums`.

Return *the **maximum** **sum score** of* `nums` *at any index.*

```
nums = [4, 3, -2, 5]  ->  10
nums = [-3, -5]       ->  -3
```

**Constraints:** `n == nums.length`; `1 <= n <= 10^5`;
`-10^5 <= nums[i] <= 10^5`.

With the total known, one pass keeps the sum of the numbers before `i`;
the first `i + 1` numbers sum to it plus `nums[i]`, and the last `n - i`
to the total less it. The answer is the largest of those. O(n).

## Approaches

| file | mechanism |
|---|---|
| `score.kara` ★ | the total first, then one pass keeping the sum before each index, both sums at it read from that and the total |
| `score_sums.kara` | both sums kept whole, a prefix `Vec` and a suffix `Vec` each filled by its own pass, the score at each index the larger of the two by `if` |
| `score_ends.kara` | every score is a prefix sum or a suffix sum, and each of those is matched or beaten by the score at its index, so the answer is the largest of them all: two running sums walk in from both ends in one `for` loop |
| `score_struct.kara` | a `struct Ledger` of the total and the sum taken, `take` (`mut ref self`) moving one number across and returning the score at it, `left` (`ref self`) the sum not yet taken; the best kept as an `Option[i64]` by a `match` with a guard |
| `score_iter.kara` | the prefix sums by `map` over a running sum the closure changes, `zip`ped with the numbers so the suffix sum is the total less the prefix plus the number, each pair's larger, then `max` |
| `score_solution.kara` | LeetCode's Rust template: a `Vec<i32>` in, `i64` out, the total by `map(\|&x\| x as i64).sum()`, the answer from `i64::MIN`, each number widened with `as i64`; carried by `karac fix` in one round |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's two examples and four more
(one number, all negative, the best a suffix, and a zero sum), each with
its answer; then a checksum of 3000 random arrays of 1 to 30 numbers
from -3, -100 and -10^5 to 3, 100 and 10^5 in turn; then the
constraints' largest, 10^5 numbers from -10^5 to 10^5, 10^5 of -10^5 and
10^5 of 10^5, whose answer of 10^10 is past `i32`. A number up to 10^5
is drawn from two draws, since one stops at 32767. `score.py` mirrors
the ★ arm and its output is byte-identical.

The ends arm was first written as a `while` loop over an index it
stepped by hand; `karac fix` rewrote it to `for i in 0..n` in three
edits, and the mutations to the ends arm were run on the rewrite.

`karac fix` carries the template in one round of 13 edits: `Vec<..>` to
`Vec[..]`, the `|&x|` and `for &x` patterns to `|x|` and `for x`, `0i64`
to `0`, `i64::MIN` to `i64.MIN`, `struct Solution;` to `struct Solution
{}` and `Solution::` to `Solution.`.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: at every index the first i + 1 numbers and the last n - i
numbers each summed afresh, the larger kept, and the largest of those;
no running sums. It checks 300 random arrays of 1 to 12 numbers from -3,
-100 and -10^5 to 3, 100 and 10^5 in turn; then 30 of numbers all
negative; then 30 of one number. All 360 are drawn before any arm
answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | it is at least the first number, the last and the total, and at most the positive numbers' sum, or the largest number if none is positive |
| P3 | the numbers reversed: the same answer |
| P4 | a 0 appended: the larger of the answer and 0 |
| P5 | every number doubled: the answer doubled |
| P6 | each arm agrees with at least three of the other five |

P4 holds because the appended 0 adds a suffix of its own, worth 0, and
leaves every other prefix and suffix sum as it was, the total among
them.

The differential prints `360 cases: checksum 852797779, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading over slices
at every index. On a failure it prints the first ten and then the count
by property.

## Mutation testing

Thirty-six edits to the differential, six to the ★ arm, five to each of
the sums, struct and iter arms, eight to the ends arm, and seven to the
template arm, each run under `karac __mir-llvm-run` and `karac
__mir-run`; the first thirty-one gave the ends arm only two edits, and
the template one, that failed in a way no kept edit elsewhere did, so
five more were written. Seventeen are kept, three to each Kāra arm and
two to the Rust-template arm. Each kept one is killed, fails the same
way under both backends and not by a crash, and no two kept ones fail
the same checks.

| # | mutation | failures by property |
|---|---|---|
| M3 | ★: only the prefix sums looked at | P1 121, P2 72, P3 267, P4 116, P6 121 |
| M4 | ★: only the suffix sums looked at | P1 146, P2 82, P3 267, P6 146 |
| M5 | ★: the total of the positive numbers only | P1 296, P2 248, P3 267, P4 117, P6 296 |
| M7 | sums: the last suffix sum 0, not the last number | P1 194, P2 101, P3 208, P4 112, P6 194 |
| M9 | sums: the smaller of the two sums taken as the score | P1 213, P2 85, P3 176, P4 134, P6 213 |
| M11 | sums: a number above 50 counted twice in the suffix sums | P1 128, P2 90, P3 141, P4 88, P5 34, P6 128 |
| M12 | ends: the best starting at 0 | P1 86, P2 71, P6 86 |
| M13 | ends: the walk stopping one short | P1 37, P2 37, P4 37, P6 37 |
| M32 | ends: the walk stepping by two | P1 223, P2 66, P4 132, P6 223 |
| M18 | struct: every number taken as its size | P1 313, P2 313, P6 313 |
| M19 | struct: the smaller of the two sums returned as the score | P1 325, P2 304, P4 177, P6 325 |
| M21 | struct: the total without the first number | P1 169, P2 101, P3 257, P4 90, P6 169 |
| M23 | iter: the least of the scores, not the largest | P1 316, P2 298, P4 194, P6 316 |
| M24 | iter: the running sums before each number, not through it | P1 297, P2 183, P3 238, P6 297 |
| M26 | iter: the total doubled | P1 220, P2 164, P3 262, P4 103, P6 220 |
| M30 | solution: the total of the numbers' sizes | P1 313, P2 313, P3 267, P4 117, P6 313 |
| M36 | solution: the number counted twice in the suffix sum | P1 240, P2 135, P3 285, P6 240 |

P1, P2 and P6 kill all seventeen, P4 twelve, P3 eleven and P5 one.
P3 reverses the numbers, so prefixes become suffixes; it kills the
edits that treat the two kinds of sum differently, and misses those
that spoil both alike (M12, M13, M18, M19, M23, M32). P5 doubles
every number, and every edit but one scales with it; only the sums
arm's number above 50 counted twice (M11) breaks the doubling, as a
number of 30 becomes 60. P2's upper bound, the positive numbers' sum,
is what kills the edits that fail only on arrays all negative: the
ends arm's best from 0 gives 0 there, above every sum (M12).

Of the thirty-six, nineteen were not kept. Two crash under both
backends, as they should: the iter arm's numbers zipped from the
second leave one number with no pair, and `max().unwrap()` panics on
the empty list (M25); and the template's first number skipped leaves
one number's answer at `i64.MIN`, which overflows when the differential
doubles it for P5 (M35). The other seventeen are killed, and none
differs between the backends. Thirteen fail as a kept one does. Seven
let a 0 into the answer of an array all negative, as the ends arm's
best from 0 (M12): the ★ arm's suffix sum taken after its number and
best from 0, the ends arm's front checked before its number is added,
the struct arm's sum left read after the number is taken, the iter
arm's and the template's suffix sum without the number, and the
template's answer from 0 (M1, M2, M16, M17, M22, M27, M28). Three look
at prefix sums only, as the ★ arm's (M3): the ends arm's back sum
walking from the front and never checked, and the template's prefix
only (M14, M15, M31). The ★ arm's smaller of the two (M6) fails as the
struct arm's (M19), the struct arm's guard reversed (M20) as the iter
arm's least score (M23), and the template's prefix added after the
score (M29) as the iter arm's running sum before each number (M24).
Four fail their own way and are left out for the count of three: the
sums arm's scores from the third index and its prefix sums one number
behind (M8, M10), and the ends arm's front setting the best to the back
sum and its back sum from the second last number (M33, M34).

## Verification

Every arm prints the same output as `score.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` every arm takes 0.4 s to 1.5 s, and the
differential 0.3 s.

## Benchmarks

The bench draws 30 arrays of 10^5 numbers from -10^5 to 10^5 once, then
punches each array 10 times, one number drawn again each time, and
answers it after each punch with the ★ arm in all five languages. Every
implementation prints `30 arrays of 10^5, 10 punches: checksum
885647680`.

BENCHTAB
