# 2527. Find Xor-Beauty of Array

You are given a **0-indexed** integer array `nums`.

The **effective value** of three indices `i`, `j`, and `k` is defined as
`((nums[i] | nums[j]) & nums[k])`.

The **xor-beauty** of the array is the XORing of **the effective values
of all the possible triplets** of indices `(i, j, k)` where
`0 <= i, j, k < n`.

Return *the xor-beauty of* `nums`.

**Note** that `val1 | val2` is bitwise OR of `val1` and `val2`, and
`val1 & val2` is bitwise AND of `val1` and `val2`.

```
nums = [1, 4]                                  ->  5
nums = [15, 45, 20, 2, 34, 35, 5, 44, 32, 30]  ->  34
```

**Constraints:** `1 <= nums.length <= 10^5`; `1 <= nums[i] <= 10^9`.

The `n^3` triples fold to the xor of the numbers themselves: `&`
distributes over `^`, the pairs `(i, j)` and `(j, i)` cancel, and what
is left is each number once. The approaches differ in how much of that
identity they take on trust.

## Approaches

| file | mechanism |
|---|---|
| `xor.kara` ★ | the xor of every number in one loop. O(n) |
| `xor_bits.kara` | for each of the 30 bits a number below `2^30` can hold, how many numbers have it; the bit is set in the answer exactly when that count is odd. O(30 n) |
| `xor_pairs.kara` | the identity one step at a time: with `c` numbers holding a bit, `n^2 - (n - c)^2` pairs whose `|` holds it and that times `c` triples; the bit set when that count is odd. No pair is formed. O(30 n) |
| `xor_rec.kara` | divide and conquer: the xor of a stretch is the xor of its two halves', a single number its own. At most 18 deep |
| `xor_iter.kara` | iterators: a `reduce` with `^` over the numbers, a list of one being its number |
| `xor_solution.kara` | LeetCode's Rust template: `Vec<i32>` in, `i32` out, the xor as a `fold` with a `&x` pattern; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 12 lines: LeetCode's two examples and six
more, among them a single `10^9`, a pair that cancels, and three
numbers whose xor is 0; then 2000 random lists of 1 to 20 numbers from
1 to 64 and 2000 of 1 to 200 from 1 to `10^9`, as the sum of the answers
and a checksum; then the constraints' largest, `10^5` numbers, once 1
to `10^5` in turn and once random to `10^9`. `xor.py` mirrors the ★ arm
and its output is byte-identical, and the mirror was checked on 2000
random lists of 1 to 10 numbers from 1 to 64 against the `n^3` triples
formed and xor'd, and the two agreed on every list.

`check` reported nothing on the five Kāra arms as first written.

`check` first reports 5 errors on the template: the unit struct
`struct Solution;`, Rust's `Vec<i32>`, the two `&x` closure patterns,
and the path call `Solution::xor_beauty`. `karac fix` carries it in two
calls, reporting 7 edits: `struct Solution {}`, the two brackets of
`Vec[i32]`, both `&` dropped, and `Solution.` in the first; and in the
second the `as i64` on the call's result, which an `i32` widens to
without a cast.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every triple `(i, j, k)` of indices, repeats allowed, its
effective value `(nums[i] | nums[j]) & nums[k]` formed, and all `n^3`
of them xor'd together. It checks 300 random lists of 1 to 12 numbers
from 1 to 64, and 60 of 1 to 12 from 1 to `10^9`, each with one more
number drawn from the same range. All 360 are drawn before any arm
answers, and 6 of them have beauty 0.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer is below `2^30`, and every bit it holds is held by some number |
| P3 | the list reversed: the same answer |
| P4 | the extra number appended: the answer xor'd with it |
| P5 | the list split in two (when `n > 1`): the xor of the halves' answers |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 cases, 6 with beauty 0: checksum 914395729,
12960 checks over 6 arms: 0 failures` under every lane in Verification;
the checksum of the literal answers was checked against a Python
reading that builds the same lists and xors the `n^3` triples. On a
failure it prints the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M2 | ★: and for xor | P1 354, P4 360, P6 354 |
| M5 | ★: the sum for the xor | P1 320, P2 320, P4 313, P5 298, P6 320 |
| M6 | ★: the last number skipped | P1 360, P3 319, P4 356, P5 324, P6 360 |
| M7 | bits: 29 bits only | P1 31, P4 26, P6 31 |
| M8 | bits: the lowest bit skipped | P1 185, P4 188, P6 185 |
| M9 | bits: a bit set on an even count | P1 360, P2 325, P5 324, P6 360 |
| M12 | pairs: the pairs as n times c | P1 166, P4 356, P5 238, P6 166 |
| M13 | pairs: the triples of 1 mod 4 | P1 273, P4 355, P5 307, P6 273 |
| M15 | pairs: the bit read one place up | P1 354, P2 73, P4 360, P6 354 |
| M19 | rec: the walk from the second number | P1 324, P3 319, P4 36, P5 322, P6 324 |
| M20 | rec: a single number read as the first | P1 319, P3 152, P4 355, P5 145, P6 319 |
| M21 | rec: a single number cut to 10 bits | P1 60, P4 60, P6 60 |
| M22 | iter: or for xor | P1 315, P4 348, P5 320, P6 315 |
| M25 | iter: and for xor | P1 317, P4 360, P5 220, P6 317 |
| M26 | iter: the largest for the xor | P1 323, P4 360, P5 324, P6 323 |
| M27 | solution: the fold begun at 1 | P1 360, P2 26, P5 324, P6 360 |
| M31 | solution: the first number twice | P1 360, P3 319, P5 324, P6 360 |

P1 and P6 kill all seventeen, P4 fourteen, P5 twelve, and P2 and P3
four each.

Five of the first thirty-one edits were replaced: two survived and
three did not run to an answer. The pairs arm's triples without the `c`
and its pairs holding the bit twice both survived, and both are
equivalent: `n^2 - (n - c)^2` is odd exactly when `c` is, so the count
of triples, the pairs alone and `c * c` all share the parity of `c`.
The bits arm's count kept across bits does not compile, the count no
longer declared; the rec arm's halves overlapping recurses without end
on a stretch of two; and the template's number added overflows its
`i32`. They became the bits arm's bit set on a count of 1 mod 4, the
pairs arm's triples of 1 mod 4 and first number not counted, the rec
arm's single number cut to 10 bits, and the template's fold begun at
the first number (M11, M13, M14, M21, M29).

Fourteen are not kept, and none survives. Ten fail exactly as a kept
one. The ★, rec and template arms' `|` for `^`, and the bits arm's bit
set on any count, which is that `|` again (M1, M18, M28, M10), fail as
the iter arm's `|` for `^` (M22); the ★ arm's xor begun at 1 (M3) as the template's fold begun at
1 (M27); the ★ arm's first number skipped, the pairs arm's first number
not counted and the template's fold begun at the first number (M4, M14,
M29) as the template's first number twice (M31), each off by the first
number; the pairs arm's pairs as `n^2` (M16) as its pairs as `n * c`
(M12); and the template's numbers halved on the way (M30) as the pairs
arm's bit read one place up (M15). The other four fail in two ways of
their own, in arms that already hold their kept edits: the bits arm's
bit set on a count of 1 mod 4 (M11), and the rec arm's left half alone
with the iter arm's newest dropped and last one alone (M17, M23, M24),
each answering from part of the list.

## Verification

Every arm prints the same output as `xor.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.9 to 10.2 s and the differential 1.0 s; under `karac __mir-llvm-asan` the arms take 0.5 to 2.9 s and the differential 0.7 s; and under `karac run` the differential takes 0.5 s.

## Benchmarks

The bench builds 1000 random lists of 100 numbers from 1 to `10^9` once
from its own generator, then makes 3000 passes. Each pass asks every
list, starting at an offset the checksum so far picks, and folds each
answer plus the pass into the checksum. The bench uses the ★ arm in all
five languages. Every implementation prints `3000 passes over 1000 lists
of 100 numbers: checksum 519650085`.

BENCHTAB
