# 2160. Minimum Sum of Four Digit Number After Splitting Digits

You are given a **positive** integer `num` consisting of exactly four
digits. Split `num` into two new integers `new1` and `new2` by using the
**digits** found in `num`. **Leading zeros** are allowed in `new1` and
`new2`, and **all** the digits found in `num` must be used.

- For example, given `num = 2932`, you have the following digits: two
  `2`'s, one `9` and one `3`. Some of the possible pairs `[new1, new2]`
  are `[22, 93]`, `[23, 92]`, `[223, 9]` and `[2, 329]`.

Return *the **minimum** possible sum of* `new1` *and* `new2`.

```
num = 2932  ->  52
num = 4009  ->  13
```

**Constraints:** `1000 <= num <= 9999`.

Two numbers of two digits each do best, since a third digit on one side
puts some digit in the hundreds; then the two smallest digits go to the
tens and the two largest to the ones. O(1).

## Approaches

| file | mechanism |
|---|---|
| `digits.kara` ★ | the digits from `num.to_string().chars()` by `to_digit`, sorted; `(d[0] * 10 + d[2]) + (d[1] * 10 + d[3])` |
| `digits_count.kara` | the digits counted by `% 10` and `/ 10` into an array of ten, then dealt out smallest first, the first two to the tens |
| `digits_network.kara` | the four digits by arithmetic into four bindings, put in order by a sorting network of five compare-exchanges, each a tuple of `min` and `max`; no collection |
| `digits_struct.kara` | a `struct Split` of the two numbers being built, which `take`s each digit in rising order onto the shorter one (`mut ref self`) and gives its `sum` (`ref self`); the digits in order from a `SortedMap` of counts |
| `digits_iter.kara` | the digits by `successors` dividing by 10, sorted, then weighed by `enumerate` and `map` and `sum`med |
| `digits_solution.kara` | LeetCode's Rust template: `(b - b'0') as i32` over `num.to_string().bytes()`, `sort_unstable`; carried by `karac fix` in two rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's two examples and four more
(the least and the most four digits, four digits in order, and two
digits twice with zeros), each with its sum; then the total and a
checksum over 2000 random numbers of four digits; then the same over
every number the constraints allow, 1000 to 9999. `digits.py` mirrors
the ★ arm and its output is byte-identical.

No compiler gap was met. The iterator arm was written with Rust's path
`std::iter::successors`, as `std.iter.successors`, and `karac fix` made
it `successors`, since Kāra's library needs no module path. `karac fix`
carries the template in two rounds of 4 and 3 edits: Rust's spellings
(`<..>` to `[..]`, `struct Solution;` to `struct Solution {}`,
`Solution::` to `.`); then the `.iter()` that Kāra's byte slice needs
before `map`, `sort_unstable` to `sort`, and the adapter's `as i64`
dropped, since an `i32` widens on return.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the four digits put in every order, each order cut in every
place into two numbers, and the least sum taken; no sorting and no rule
about tens. It checks 300 random numbers of four digits; then 30 with
two or more digits the same; then 30 holding a 0. All 360 are drawn
before any arm answers.

| | property |
|---|---|
| P1 | the sum is the statement read literally |
| P2 | the digits put largest first: the same sum |
| P3 | every digit one more, when none is 9: the sum 22 more |
| P4 | the largest digit made 9: the sum more by 9 less that digit |
| P5 | a smallest digit made 0, when one is not the first digit: the sum less by ten times it |
| P6 | each arm agrees with at least three of the other five |

P3 holds since the two tens and the two ones each gain one. P4 holds
since the largest digit stays the largest and is a ones digit, and P5
since a smallest digit stays a smallest and is a tens digit.

The differential prints `360 numbers: checksum 898921810, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading of the same
numbers by the same orders and cuts. On a failure it prints the first
ten and then the count by property.

## Mutation testing

Twenty-five edits to the differential, four or five to each arm, each
run under `karac __mir-llvm-run` and `karac __mir-run`. Seventeen are
kept, three to each Kāra arm and two to the Rust-template arm. Each kept
one is killed, fails the same way under both backends and not by a
crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the tens and ones paired wrongly | P1 291, P6 291 |
| M3 | ★: the digits never sorted | P1 282, P2 275, P4 136, P5 108, P6 282 |
| M25 | ★: the smallest digit in both tens | P1 291, P5 188, P6 291 |
| M4 | count: only the first digit to the tens | P1 340, P3 232, P6 340 |
| M5 | count: each digit counted once however often it comes | P1 182, P3 137, P4 61, P5 49, P6 182 |
| M6 | count: the 9s never dealt | P1 128, P3 90, P4 232, P6 128 |
| M8 | network: the last exchange left out | P1 182, P2 182, P6 182 |
| M10 | network: the hundreds digit read as the thousands | P1 320, P2 313, P4 136, P5 80, P6 320 |
| M11 | network: the tens the smallest and the largest | P1 351, P4 232, P6 351 |
| M13 | split: every digit on the first number | P1 359, P3 232, P5 188, P6 359 |
| M14 | split: a repeated digit taken once | P1 165, P3 137, P4 54, P5 53, P6 165 |
| M15 | split: the sum the first number twice | P1 351, P4 232, P5 188, P6 351 |
| M16 | iter: the last digit peeled never taken | P1 360, P2 247, P3 232, P4 75, P6 360 |
| M17 | iter: three digits weighing ten | P1 359, P3 232, P6 359 |
| M19 | iter: the digits never sorted | P1 275, P2 275, P4 96, P5 80, P6 275 |
| M21 | solution: the ones and tens swapped | P1 359, P4 232, P5 188, P6 359 |
| M24 | solution: the fourth digit dropped | P1 360, P3 232, P4 232, P6 360 |

P1 and P6 kill all seventeen, P4 eleven, P5 nine, P3 eight and P2
five. The answer is a small sum of four digits, so every wrong edit
shows against the literal reading; the properties tell apart where it
goes wrong. P2 puts the digits largest first, which sees an edit that
depends on the digits' order (M3, M8, M10, M16, M19); the ★ arm never
sorting (M3) and the iterator arm never sorting (M19) fail it alike,
but P1 sees them differently, since one reads the digits from the
front and the other from the back. P3 adds one to every digit, which
sees, among others, an edit whose weights do not add up to 22 (M4, M13,
M17, M24). P4
raises the largest digit, which sees an edit that does not keep it a
ones digit, and P5 lowers a smallest, which sees one that does not keep
it a tens digit (M25, which counts it twice). The two network edits
show the arm's shape: its last exchange matters (M8), but its first
does not (see below).

Of the twenty-five, eight were not kept. Two are equivalent: the
network's first exchange left out, since the sum needs only which two
digits are smallest, not their order, and the network still finds
them; and the split arm handing a tie to the second number, since the
two numbers are interchangeable. One crashes: the template's digits
read from `b'1'`, which overflows a `u8` at every 0. Five fail as a kept
one does: the ★ arm's digits sorted largest first and the iterator
arm's largest two weighing ten, as M21; the count arm's leading digit
never counted, as M16; the template's second tens the third digit, as
M1; and the template's second tens added as a ones digit, as M4.

## Verification

Every arm prints the same output as `digits.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.1 s to 0.4 s and the
differential 0.5 s.

## Benchmarks

The bench solves all 9000 numbers of four digits 200 times, each pass
starting at a different number so that no pass repeats the one before,
with the ★ arm in all five languages, each reading the digits from the
number's text and sorting them: C by `snprintf` and `qsort`. Every
implementation prints `1800000 solves: 120256200 in all, checksum
162681282`.

BENCHTAB
