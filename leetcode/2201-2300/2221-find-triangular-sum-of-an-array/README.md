# 2221. Find Triangular Sum of an Array

You are given a **0-indexed** integer array `nums`, where `nums[i]` is a
digit between `0` and `9` (**inclusive**).

The **triangular sum** of `nums` is the value of the only element present
in `nums` after the following process terminates:

1. Let `nums` comprise of `n` elements. If `n == 1`, **end** the process.
   Otherwise, **create** a new **0-indexed** integer array `newNums` of
   length `n - 1`.
2. For each index `i`, where `0 <= i < n - 1`, **assign** the value of
   `newNums[i]` as `(nums[i] + nums[i + 1]) % 10`, where `%` denotes the
   modulo operator.
3. **Replace** the array `nums` with `newNums`.
4. **Repeat** the entire process starting from step 1.

Return *the triangular sum of* `nums`.

```
nums = [1, 2, 3, 4, 5]  ->  8
nums = [5]              ->  5
```

**Constraints:** `1 <= nums.length <= 1000`; `0 <= nums[i] <= 9`.

The rounds can be done in place: writing `(nums[i] + nums[i + 1]) % 10`
over `nums[i]` from left to right reads `nums[i + 1]` before it is
written, and each round the live part shrinks by one. O(n^2), with no
row allocated per round.

## Approaches

| file | mechanism |
|---|---|
| `triangle.kara` ★ | the rounds in place over a clone, the live part shrinking from n - 1 to 1, the first digit the answer |
| `triangle_rows.kara` | the process as the statement tells it, a new `Vec` one shorter each round replacing the old |
| `triangle_binomial.kara` | each digit reaches the bottom along C(n - 1, i) paths, so the answer is the sum of C(n - 1, i) * nums[i] mod 10; the coefficients built by Pascal's rule in one row mod 10, updated from the right |
| `triangle_struct.kara` | a `struct Triangle` holding the row, `step` (`mut ref self`) folding it down in place and `pop`ping its last digit, `done` and `top` (`ref self`) |
| `triangle_iter.kara` | a `fold` over the n - 1 rounds carrying the row, each new row the row `zip`ped with itself one along (`skip(1)`) and `map`ped to the pair's sum mod 10 |
| `triangle_solution.kara` | LeetCode's Rust template: `mut nums: Vec<i32>` in, `i32` out, the rounds done in place on the parameter with `usize` indices; carried by `karac fix` in one round |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's two examples and four more
(two nines, all zeros, a lone 1 at the start of eight, and 1 to 9), each
with its answer; then a checksum of 3000 random arrays of 1 to 40
digits; then the constraints' largest, 1000 random digits and 1000
nines. `triangle.py` mirrors the ★ arm and its output is byte-identical.

`karac fix` carries the template in one round of 12 edits: `mut nums:
Vec<i32>` to `nums: own Vec[i32]` with `let mut nums = nums;` at the top
of the body, as Kāra has no `mut` on a parameter and the body changes
the vector it owns, `Vec<..>` to `Vec[..]`, the `|&x|` to `|x|`, the
adapter's `as i64` on the `i32` result dropped, since an `i32` widens to
`i64` on its own, `struct Solution;` to `struct Solution {}` and
`Solution::` to `Solution.`.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally with the sums kept whole: every round adds neighbours without
taking mod 10, and the one number left is taken mod 10 at the end, which
agrees since mod 10 keeps sums. It checks 300 random arrays of 1 to 14
digits; then 30 of one digit throughout; then 30 of one digit among
zeros. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | it is a digit, 0 to 9 |
| P3 | the digits reversed: the same answer |
| P4 | every digit d made (10 - d) % 10: the answer made so too |
| P5 | a second array of the same length added digit by digit mod 10: the two answers added mod 10 |
| P6 | each arm agrees with at least three of the other five |

P3 holds because C(n - 1, i) = C(n - 1, n - 1 - i), and P4 and P5
because the answer is a sum of the digits times fixed coefficients, mod
10.

The differential prints `360 cases: checksum 945940463, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading over
`math.comb`, the sum of C(n - 1, i) * nums[i] mod 10. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Thirty-three edits to the differential, six to the ★ arm, seven to the
iter arm, and five to each of the other arms, each run under `karac
__mir-llvm-run` and `karac __mir-run`; two of the iter arm's first five
crashed, so two more were written. Seventeen are kept, three to each
Kāra arm and two to the Rust-template arm. Each kept one is killed,
fails the same way under both backends and not by a crash, and no two
kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M3 | ★: each sum taken mod 9 | P1 282, P4 285, P5 272, P6 282 |
| M5 | ★: every other round skipped | P1 266, P3 246, P6 266 |
| M6 | ★: a 7 to the right counted as 14 | P1 198, P3 201, P4 230, P5 247, P6 198 |
| M7 | rows: each digit less its right neighbour | P1 251, P3 125, P6 251 |
| M10 | rows: each digit added to itself | P1 278, P3 246, P6 278 |
| M11 | rows: each sum taken mod 100 | P1 284, P2 284, P4 313, P5 284, P6 284 |
| M14 | binomial: the coefficients from 2, not 1 | P1 324, P6 324 |
| M15 | binomial: Pascal's row updated from the left, over its new values | P1 247, P3 244, P6 247 |
| M16 | binomial: the coefficients mod 5 | P1 107, P6 107 |
| M17 | struct: the first digit dropped, not the last, once three are left | P1 296, P3 276, P6 296 |
| M20 | struct: done at two digits | P1 287, P3 276, P6 287 |
| M21 | struct: each sum one more | P1 329, P4 261, P5 329, P6 329 |
| M24 | iter: neighbours multiplied | P1 295, P4 82, P5 137, P6 295 |
| M25 | iter: each sum capped at 9, not taken mod 10 | P1 282, P4 316, P5 325, P6 282 |
| M33 | iter: the row zipped with itself reversed | P1 276, P3 253, P6 276 |
| M28 | solution: each sum taken mod 11 before mod 10 | P1 276, P4 268, P5 273, P6 276 |
| M29 | solution: the first digit never folded | P1 295, P3 266, P6 295 |

P1 and P6 kill all seventeen, P3 nine, P4 and P5 seven each, and P2
one. P3, P4 and P5 together see an edit that makes the answer lopsided
or not linear in the digits, and only P1 can see one that keeps it
both: the binomial arm's coefficients from 2 or mod 5 (M14, M16) are
still symmetric and still a sum of digits times fixed coefficients, just
the wrong ones. P2 kills only the rows arm's sums mod 100 (M11); every
other edit still takes a last mod 10 or adds digits that stay digits.

Of the thirty-three, sixteen were not kept. One survives and is
equivalent: the struct arm's `top` reading the last digit (M18), which
at one digit is the first. Two crash under both backends, as they
should: the iter arm's row zipped two along empties it a round early,
and its rounds from 0 run one too many; either way the row is empty
when `last[0]` is read (M22, M26). The other thirteen are killed, and
none differs between the backends. Nine fail as a kept one does: seven
stop one round short, as the struct arm's done at two digits (M20): the
★ arm's live part from 2, the rows arm's stop at two, the binomial
arm's rows to n - 1 and each row's update from r - 1, the struct arm's
step missing its last pair, the iter arm's rounds from 2 and the
template's rounds from n - 1 (M2, M8, M12, M13, M19, M23, M27); the ★
arm's in-place round run right to left (M1) as the binomial arm's
Pascal's row from the left (M15), each reading a value already written;
and the rows arm's first digit kept as it is (M9) as the template's
first digit never folded (M29). Four fail alike in pairs and neither of
a pair is kept: the ★ arm's and the template's last digit returned (M4,
M30), and the template's and the iter arm's left digit counted twice
(M31, M32).

## Verification

Every arm prints the same output as `triangle.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` every arm but the iter arm takes 0.7 s to 1.0 s,
the iter arm 4.6 s, and the differential 0.6 s.

## Benchmarks

The bench draws 8 arrays of 1000 digits once, then punches each array 8
times, one digit drawn again each time, and answers it after each punch
with the ★ arm in all five languages. Every implementation prints `8
arrays of 1000 digits, 8 punches: checksum 363494729`.

BENCHTAB
