# 2117. Abbreviating the Product of a Range

You are given two positive integers `left` and `right` with `left <=
right`. Calculate the product of all integers in the inclusive range
`[left, right]`.

Since the product may be very large, you will abbreviate it following
these steps:

1. Count all trailing zeros in the product and remove them. Let us
   denote this count as `C`.
2. Denote the remaining number of digits in the product as `d`. If
   `d > 10`, then express the product as `<pre>...<suf>` where `<pre>`
   denotes the first 5 digits of the product, and `<suf>` denotes the
   last 5 digits of the product after removing all trailing zeros. If
   `d <= 10`, we keep it unchanged.
3. Finally, represent the product as a string `"<pre>...<suf>eC"`.

Return a string denoting the abbreviated product of all integers in the
inclusive range `[left, right]`.

```
left = 1,   right = 4    ->  "24e0"
left = 2,   right = 11   ->  "399168e2"
left = 371, right = 375  ->  "7219856259e3"
```

**Constraints:** `1 <= left <= right <= 10^4`.

The product of `[1, 10000]` has 35660 digits, so the arms that keep no
big number work from three smaller facts. A trailing zero is a 2 paired
with a 5, so the zeros are the smaller of the two counts. With the 2s
and 5s divided out, the rest gives the last five digits modulo 100000,
and the unpaired 2s or 5s go back in at the end. The first five digits
need only the leading digits of the product, which a float keeps. And
whether the product without its zeros has at most ten digits is decided
exactly, by the same product capped at 10^11: every factor is at least
1, so once the cap is reached the product stays above it.

## Approaches

| file | mechanism |
|---|---|
| `abbreviate.kara` ★ | one loop pulls the 2s and 5s out of each number, multiplies the rest modulo 100000 and, capped at 10^11, exactly, and keeps the leading digits in an `f64` divided by ten past 10^12; the unpaired 2s or 5s go back after. O((right - left) log right) |
| `abbreviate_limbs.kara` | the product exactly, a `Vec[i64]` in base 10000 multiplied limb by limb; the digits written out with `{:04}`, the zeros taken off with `strip_suffix` in a loop, the answer cut with string slices. O((right - left) * digits) |
| `abbreviate_legendre.kara` | the 2s and 5s counted per power over the range, as Legendre's formula counts them in a factorial; the unpaired ones put back by modular exponentiation, and the first five digits from the fractional part of the sum of `log10` |
| `abbreviate_struct.kara` | a `struct Product` of the ★ arm's state, with `times` and `abbreviated` methods (`mut ref self`) and a helper `mul` |
| `abbreviate_fold.kara` | a `fold` over `left..=right` with a tuple accumulator, each number split into its 2s, 5s and rest by a helper; a second `fold` over the unpaired factors, gathered with `map` and `chain` |
| `abbreviate_solution.kara` | LeetCode's Rust template: the ★ arm with `u64` state, `min(CAP)` and `format!`, carried by `karac fix` in two rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 11 lines: LeetCode's three examples and five
more (one number, ten alone, the constraints' last two, a product of
exactly ten digits after its zeros and one of eleven), each with its
answer; then the trailing zeros over 1000 random ranges of up to 60
numbers within 1 to 10000, and a checksum of the answers' bytes; then
two long ranges, `[1, 3000]` and `[9001, 10000]`. `abbreviate.py`
mirrors the ★ arm and its output is byte-identical. The answers to the
two long ranges were checked against Python's exact integers.

The limbs arm first bound its digits as `let mut kept: Str = digits;`,
so that the loop could reassign the view. That met a compiler gap,
fixed in karac with a test named for this kata (karac 115ea5b11c,
`tests/kata_2117_string_as_str_fix.rs`). The mismatch said only
"expected 'Str', found 'String'", though a `String` passes as a `Str`
at a call and strings.md names `as_str()` for every other place, and
the one edit `karac fix` offered was the borrow checker's `.clone()`
for the move it saw: a clone is a temporary, so the next round refused
the view of it. The mismatch now carries `.as_str()`, and an edit the
borrow checker would insert at the same spot gives way to it; `karac
fix` then carries the line in one round.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the product worked out one decimal digit at a time, its
trailing zeros counted off, and the answer cut from the digits that
are left. It checks 300 random ranges with `left` from 1 to 9999 and up
to 40 numbers; then 30 starting at 1 to 30 with up to 30 numbers, where
the short answers are; then 30 that end at 9999. All 360 are drawn
before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer is well formed: digits, `e` and the zero count; ten digits at most, or five, `...` and five; never a zero first, or last before `e` |
| P3 | one more number: a short answer times it, with its zeros moved to the count, is the next answer whenever that is short too |
| P4 | the zero count never falls when the range takes one more number at either end |
| P5 | one more number with no factor 2 or 5: when both answers are long, the last five digits are multiplied by it and the zeros stay |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 ranges: checksum 549328095, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against Python's exact integers over
the same ranges. P3 applies to 19 of the ranges and P5 to 114; on the
rest they hold trivially. On a failure it prints the first ten and then
the count by property.

## Mutation testing

Thirty-two edits to the differential, five or six to each arm, each run
under `karac __mir-llvm-run` and `karac __mir-run`. Seventeen are kept,
three to each Kāra arm and two to the Rust-template arm. Each kept one
is killed, fails the same way under both backends and not by a crash,
and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M3 | ★: the short answer up to eleven digits | P1 2, P2 2, P6 2 |
| M4 | ★: the last digits unpadded | P1 32, P2 32, P5 24, P6 32 |
| M6 | ★: the right end left out | P1 360, P3 27, P5 111, P6 360 |
| M8 | limbs: the inner limbs unpadded | P1 257, P3 12, P4 30, P5 19, P6 257 |
| M9 | limbs: one zero stripped only | P1 295, P2 295, P3 5, P6 295 |
| M10 | limbs: the first six digits | P1 333, P2 333, P6 333 |
| M12 | legendre: only the first power counted | P1 347, P3 8, P6 347 |
| M13 | legendre: the range counted from `left` | P1 219, P6 219 |
| M17 | legendre: the exact product never capped | P1 10, P3 6, P6 10 |
| M18 | struct: each number's last 5 left in it | P1 338, P2 338, P3 11, P6 338 |
| M19 | struct: the unpaired 5s never put back | P1 2, P3 2, P6 2 |
| M22 | struct: the first number skipped | P1 359, P6 359 |
| M23 | fold: the 2s of each number counted once | P1 345, P3 7, P6 345 |
| M25 | fold: the last digits modulo 10^4 | P1 301, P5 103, P6 301 |
| M27 | fold: the zeros the larger count | P1 355, P3 7, P6 355 |
| M31 | solution: a factor's 5s left in it | P1 340, P2 335, P3 9, P6 340 |
| M32 | solution: a ten-digit short answer refused | P1 1, P6 1 |

P1 and P6 kill all seventeen, P3 ten, P2 six, P5 four and P4 one. P3
sees the edits that get the zero count or the digits wrong on short
answers, since it multiplies one more number in by hand. P2 sees a
wrong shape: a short answer of eleven digits (M3), last digits that
lost a leading zero (M4), zeros left on the end (M9, M18, M31), six
leading digits (M10). P5 sees last digits that do not multiply: a
lost leading zero (M4), the range one short (M6), base-10000 limbs printed without their zeros
(M8), a modulus of 10^4 (M25). P4 sees only the unpadded limbs, which
can lose zeros in the middle of the product and so count fewer at its
end.

Of the thirty-two, fifteen were not kept. Two are equivalent: the
limbs arm's carry pushed once rather than in a loop, since a carry
below 10^8 over base 10000 always fits one limb, and the struct arm's
cap at 10^10, which still answers "too long" for a capped product at
the same test. The ★ arm's lead kept below 10^6 survives: a float's
relative precision does not depend on its size, so the six digits it
keeps carry the same first five. Eleven fail as a kept one does or as
another left out does: the ★ arm's zeros counted by the 2s and its
unpaired 2s never put back alike (P1 353, P3 7, P6 353); the
legendre and fold arms' unpaired factor always 2, and the Rust arm's
zeros counted by the 5s and its cap applied before the 5s, as M19; the
lead off by a digit in the legendre, struct, fold and Rust arms as M10;
the limbs arm's nine-digit short answer as M32. The legendre arm's
power one short (P1 333, P6 333) is killed with checks of its own but
was left out because its arm keeps its share.

## Verification

Every arm prints the same output as `abbreviate.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.2 s to 0.4 s, the limbs arm
1.3 s, and the differential 1.2 s; compiled it takes 0.6 s.

`karac fix` carries the template in two rounds of 10 edits and 1: the
`mut` inside the tuple patterns moved before them (`let mut (twos,
fives)`), `format!` to f-strings, `struct Solution;` to `struct Solution
{}` and `::` to `.`; then the redundant `f64` suffix of `1.0f64`.

## Benchmarks

The bench solves 40000 random ranges of 1 to 3000 numbers within 1 to
10000, each once, with the ★ arm in all five languages; the float of
the leading digits is the same IEEE `f64` arithmetic in each. Every
implementation prints `40000 solves: 39947 long answers, checksum
230660300`.

BENCHTAB
