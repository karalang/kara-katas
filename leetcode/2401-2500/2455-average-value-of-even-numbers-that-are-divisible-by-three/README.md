# 2455. Average Value of Even Numbers That Are Divisible by Three

Given an integer array `nums` of **positive** integers, return *the
average value of all even integers that are divisible by* `3`*.*

Note that the **average** of `n` elements is the **sum** of the `n`
elements divided by `n` and **rounded down** to the nearest integer.

```
nums = [1,3,6,10,12,15]  ->  9
nums = [1,2,4,7,10]      ->  0
```

**Constraints:** `1 <= nums.length <= 1000`; `1 <= nums[i] <= 1000`.

Two and three share no factor, so a value both even and divisible by
three is a multiple of six. One pass sums and counts those, and the
answer is the sum divided by the count, which rounds down since every
value is positive, or 0 when no value qualifies.

## Approaches

| file | mechanism |
|---|---|
| `average.kara` ★ | one pass: the values with `x % 6 == 0` summed and counted, then the sum divided by the count, or 0. O(n) |
| `average_naive.kara` | the statement read directly: a value kept when it is even and when it is divisible by three, tested apart, the kept values collected into a `Vec`, then summed and divided by their number. O(n) |
| `average_digits.kara` | by digits, as the schoolbook rules test it: even when the last decimal digit is, divisible by three when the digit sum is, each digit read off by `% 10` and `/ 10`. O(n log max) |
| `average_table.kara` | a table: each value's count in a `Vec` of 1001, then only the multiples of six visited, stepping by 6, each adding its value times its count. O(n + 1000) |
| `average_iter.kara` | iterators: the multiples of six kept by `filter` and folded into a `(sum, count)` pair by `fold` with a tuple pattern, then divided. O(n) |
| `average_solution.kara` | LeetCode's Rust template: the multiples of six collected by `into_iter().filter(\|&x\| ..)`, summed by `iter().sum::<i32>()` and divided by `v.len() as i32`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 10 lines: LeetCode's two examples; one value,
6; even values none divisible by three with multiples of three none
even; an average rounded down; 1000 values of 996, the largest multiple
of six up to 1000; every value from 1 to 1000; then 1000 random values
up to 1000 and 1000 up to 20; and 3000 random arrays of 1 to 8 values
up to 60, as a checksum and the total. `average.py` mirrors the ★ arm
and its output is byte-identical, and the mirror was checked on 50000
random arrays of up to 10 values against the statement's two tests and
the average rounded down by `math.floor`.

`check` first reports 5 errors on the template, and `karac fix` carries
it in one call, reporting 8 edits: the angle brackets of both
`Vec<i32>` made square; the `&` of the closure pattern `|&x|` dropped;
the turbofish `::<i32>` on `sum` dropped, since Kāra has no call-site
type arguments; `struct Solution;` given its braces; and, once the
template parses, the parameter `nums` declared `own`, since
`into_iter()` consumes it and a parameter borrows by default. The bare
`sum()`, whose type comes from the `i32` it is divided by, and `v.len()
as i32` stand as Kāra. The values fit an `i32`, as LeetCode's signature
has them; the other arms take `i64`.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: a value kept when two divides it and three divides it, each
tested by stepping that number up from 0 until it reaches or passes the
value; the average rounded down found as the largest whole number whose
product with the count is no more than the sum, tried from 0 upward. No
remainder or quotient is taken. It checks 300 random arrays of 1 to 10
values up to 40; then 30 of up to 100 values up to 994; then 30 of up
to 30 values, all multiples of six up to 990. All 360 are drawn before
any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | the values in reverse order: the same answer |
| P3 | the values twice over: the same answer |
| P4 | every value raised by 6: the answer plus 6, or 0 when no value is kept |
| P5 | the odd values 1 and 999 added: the same answer |
| P6 | each arm agrees with at least three of the other five |

P2 holds because a sum and a count ignore order, and P3 because both
double. P4 holds because a value raised by 6 is a multiple of six
exactly when it was one, and the sum then grows by 6 for each kept
value, so the average does by 6. P5 holds because odd values are never
kept. The cases stop at 994 and 990 so that P4 stays within the
constraints' 1000.

The differential prints `360 cases: checksum 933443113, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and tests evenness and divisibility by three apart. On a
failure it prints the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: multiples of three | P1 207, P4 76, P5 360, P6 207 |
| M3 | ★: rounded up | P1 36, P6 36 |
| M6 | ★: each value one more | P1 221, P6 221 |
| M7 | naive: even or by three | P1 295, P4 127, P5 360, P6 295 |
| M9 | naive: one too many to divide by | P1 221, P3 220, P4 198, P6 221 |
| M10 | naive: the first kept left out of the sum | P1 221, P2 117, P3 221, P4 203, P6 221 |
| M12 | digits: an odd last digit | P1 294, P4 161, P5 360, P6 294 |
| M13 | digits: the digit sum by nine | P1 184, P4 221, P6 184 |
| M14 | digits: the leading digit dropped | P1 296, P4 261, P6 296 |
| M18 | table: 996 left out | P4 4 |
| M20 | table: each multiple counted once | P1 221, P3 61, P4 221, P6 221 |
| M21 | table: repeats counted once | P1 28, P6 28 |
| M23 | iter: never counted | P1 221, P4 221, P6 221 |
| M25 | iter: the sum started at 6 | P1 197, P3 191, P6 197 |
| M26 | iter: the first kept skipped | P1 214, P2 117, P3 213, P4 95, P6 214 |
| M27 | solution: multiples of twelve | P1 144, P4 218, P6 144 |
| M31 | solution: the values halved | P1 259, P4 248, P5 230, P6 259 |

P1 and P6 kill sixteen, P4 thirteen, P3 five, P5 four and P2 two. The
table arm's 996 left out (M18) is killed by P4 alone: no case holds 996,
the largest multiple of six up to 1000, until P4 raises a 990 to it.

Fourteen are not kept. Five fail exactly as a kept one: the ★ arm's
each counted twice and the iter arm's each value doubled (M4, M24) as
the iter arm's never counted (M23), all three wrong on every case that
keeps a value, the 221 whose answer is not 0; the naive arm's divisible
by four for even (M8) as the template's multiples of twelve (M27),
which keep the same values; and the template's one too many to divide
by and first kept left out of the sum (M28, M30) as the naive arm's
(M9, M10). Nine fail apart from every kept one and were left out
because those arms keep their share already: the ★ arm's even values
(M2); the ★, naive and template arms' none answered 6, -1 and 1 (M5,
M11, M29), which fail alike on the 139 cases that keep nothing; the
digits arm's every other digit and tens digit for the last (M15, M16);
the table arm's 6 skipped and every other multiple (M17, M19); and the
iter arm's 6 itself left out (M22), which fails as M17 does.

## Verification

Every arm prints the same output as `average.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` every arm takes 0.2 to 0.4 s, and the
differential 0.6 s; under `karac __mir-llvm-asan` the differential
takes 0.6 s and under `karac run` 0.5 s.

## Benchmarks

The bench builds 1000 arrays of 1000 values up to 1000, the
constraints' largest, once from its own generator. It then makes 250
passes; each sets one value of every array from the checksum so far, so
no answer carries over, then answers every array, folding the answer
plus the pass into the checksum. The bench uses the ★ arm, one pass
summing and counting the multiples of six, in all five languages. Every
implementation prints `250 passes over 1000 arrays of 1000 values:
checksum 45278468`.

BENCHTAB
