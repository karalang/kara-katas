# 2535. Difference Between Element Sum and Digit Sum of an Array

You are given a positive integer array `nums`.

- The **element sum** is the sum of all the elements in `nums`.
- The **digit sum** is the sum of all the digits (not necessarily
  distinct) that appear in `nums`.

Return *the **absolute** difference between the **element sum** and
**digit sum** of* `nums`.

**Note** that the absolute difference between two integers `x` and `y`
is defined as `|x - y|`.

```
nums = [1,15,6,3]  ->  9
nums = [1,2,3,4]   ->  0
```

**Constraints:** `1 <= nums.length <= 2000`; `1 <= nums[i] <= 2000`.

A number is never less than its digit sum, and the two leave the same
remainder by 9, so the answer is the sum of each number less its own
digits: never negative, and always a multiple of 9. The approaches
differ in how the digits are taken off.

## Approaches

| file | mechanism |
|---|---|
| `difference.kara` ★ | one pass: each number added to the element sum, and its digits, taken off by `% 10` and `/ 10`, to the digit sum; the answer the absolute difference. O(n log max) |
| `difference_each.kara` | number by number, with no absolute value: each number less its digits, read by place from the thousands down |
| `difference_rec.kara` | a recursion: a number's digit sum is its last digit plus the digit sum of the rest, and the list's difference its first number's less its digits plus the difference of the rest. At most 2000 deep |
| `difference_iter.kara` | iterators: the element sum a `sum`, the digit sum a `flat_map` of each number's digits, made by `successors` dividing by 10 while the number is 10 or more |
| `difference_text.kara` | each number written out with `to_string`, and each character's `to_digit(10)` added to the digit sum |
| `difference_solution.kara` | LeetCode's Rust template: `Vec<i32>` in, `i32` out; the element sum and the digit sum each a `sum` over the numbers, the digits taken off in a loop in a closure; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 10 lines: LeetCode's two examples and six
more; then 3000 random lists of 1 to 20 numbers from 1 to 2000, and 1000
of 1 to 2000 numbers, each as the sum of the answers and a checksum.
`difference.py` mirrors the ★ arm and its output is byte-identical.

The iter arm's `successors` starts from `*x`. Written `Some(x)`, with
`x` the `ref i64` that `nums.iter()` gives, the item type is `ref i64`,
and the closure's new `r / 10` cannot be one. B-2026-11-15-34 had
already moved that refusal to the seed with the `*` as its fix, but it
read only a closure that returns `Some(..)` directly, and this one
returns it from an `if`; so `check` gave the bare E0509 "the result
borrows a temporary value" at the closure, naming neither the seed nor
the fix (B-2026-11-24-3). The check now reads every branch of an `if`
or `match`.

`check` first reports 3 errors on the template, all Rust's spellings:
`struct Solution;`, `Vec<i32>` in angle brackets, and the `&` pattern in
`|&x|`. `karac fix` carries it in one call, reporting 6 edits. Among
them, the closure's digit sum, `let mut s = 0;` grown by `s += x % 10`,
is an `i64`, since an operator does not fix a literal's type (design.md
§8 Literals), so summing the closures into an `i32` is a narrowing; the
fix declares it `s: i32`. That fix was made for a function's tail
binding, and a closure whose body has statements before its tail got
none: `karac fix` stopped with the error unfixed (B-2026-11-24-4).

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: each number written out with an f-string, and every
character's code less `'0'`'s added to the digit sum. It checks 400
random lists of 1 to 12 numbers to 2000; then 10 lists of 2000s, 10 of
1999s, and 20 of one-digit numbers. All 440 are drawn before any arm
answers, and 20 of them have answer 0.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer is at least 0 and a multiple of 9 |
| P3 | the numbers in the other order: the same answer |
| P4 | the digits 1 to 9 added: the same answer, since a one-digit number is its own digit sum |
| P5 | every number written twice: twice the answer |
| P6 | each arm agrees with at least three of the other five |

The differential prints `440 cases, 20 with answer 0: checksum
666575497, 15840 checks over 6 arms: 0 failures` under every lane in
Verification; the checksum of the literal answers was checked against a
Python reading that builds the same cases. On a failure it prints the
first ten and then the count by property.

## Mutation testing

Ten edits to the differential's arms, two to each of the five, and two
to the Rust-template arm, each run under `karac __mir-run`. Every one is
killed. For each, a Python reading of the edited arm over the same 440
cases counted the cases where it differs from the statement, and that
count is the P1 count the differential printed, every time.

| # | mutation | failures | P1 | Python's count |
|---|---|---|---|---|
| M1 | ★: the leading digit left off (`rest > 9`) | 1725 | 440 | 440 |
| M2 | ★: each digit taken `% 9` | 1639 | 417 | 417 |
| M3 | each: the places from the hundreds | 1139 | 380 | 380 |
| M4 | each: the units place left off | 1654 | 425 | 425 |
| M5 | rec: the rest divided by 100 | 1209 | 418 | 418 |
| M6 | rec: the last number never asked | 2032 | 419 | 419 |
| M7 | iter: the walk stopped at 10 (`r > 10`) | 357 | 119 | 119 |
| M8 | text: the first character skipped | 1725 | 440 | 440 |
| M9 | solution: the number divided by 100 | 1209 | 418 | 418 |
| M10 | solution: the difference unsigned, digits less elements | 1260 | 420 | 420 |

## Verification

Every arm prints the same output as `difference.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 1.7 to 7.2 s, but for the iter arm,
13.6 s, and the differential 0.7 s; under `karac __mir-llvm-asan` the
arms take 0.8 to 3.5 s and the differential 0.6 s.

## Benchmarks

The bench builds 50 lists of 2000 numbers to 2000 once from its own
generator, then makes 1000 passes. Each pass, for every list, sets the
number at place `check % 2000` to `(check + p) % 2000 + 1`, asks, and
folds the answer plus the pass into the checksum. The bench uses the ★
arm in all five languages. Every implementation prints `1000 passes over
50 lists of 2000: checksum 174244073`.

BENCHTAB
