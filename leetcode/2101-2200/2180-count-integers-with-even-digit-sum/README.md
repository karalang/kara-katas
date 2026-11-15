# 2180. Count Integers With Even Digit Sum

Given a positive integer `num`, return *the number of positive integers
**less than or equal to*** `num` *whose digit sums are **even***.

The **digit sum** of a positive integer is the sum of all its digits.

```
num = 4   ->  2
num = 30  ->  14
```

**Constraints:** `1 <= num <= 1000`.

At most 1000, so every number from 1 to num can be tried. A faster
reading sees that the digit sums of two numbers in a row differ in
parity, except across a decade's turn, and that each decade from 0 on
holds five of each: the count is num / 2 when num's own digits sum
evenly, and (num - 1) / 2 when they do not. O(num log num).

## Approaches

| file | mechanism |
|---|---|
| `even_digits.kara` ★ | every number from 1 to num, its digits summed by remainders of 10, counted when the sum is even |
| `even_digits_formula.kara` | in closed form: num / 2 or (num - 1) / 2, by the parity of num's own digit sum; O(log num) |
| `even_digits_table.kara` | a `Vec.filled(num + 1, false)` of whose digit sums are odd, each number's from that of the number with its last digit dropped, x / 10, flipped by its last digit's parity |
| `even_digits_struct.kara` | a `struct Odometer` of the digits, lowest first, and their running sum, made `at_zero`; it `tick`s one on (`mut ref self`), carrying each 9 over to a 0, and says whether it reads `even` (`ref self`) |
| `even_digits_iter.kara` | the numbers from 1 to num `filter`ed to those whose digits, the `chars` of the number written out by an f-string `map`ped through `to_digit` and `sum`med, are even, and `count`ed |
| `even_digits_solution.kara` | LeetCode's Rust template: `num: i32`, `-> i32`, `for x in 1..=num`, `struct Solution;`, `Solution::`; carried by `karac fix` in two rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 7 lines: LeetCode's two examples and four more
(1, 2, 11, the first past a decade whose digits sum evenly, and the
constraints' largest, 1000), each with its count; then the total and a
checksum over every number the constraints allow, 1 to 1000.
`even_digits.py` mirrors the ★ arm and its output is byte-identical.

`karac fix` carries the template in two rounds of 2 and 1 edits: Rust's
spellings, `struct Solution;` to `struct Solution {}` and `Solution::`
to `.`; then the adapter's widening `as i64` dropped, as the `i32`
widens to the `i64` it returns. Kāra takes the template's `1..=num` as
it is.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every number from 1 to num written out, each of its
characters read as the digit it stands for by finding it in
"0123456789", the digits added, and the number counted when the sum is
even. No remainders and no division. It checks 300 random numbers of 1
to 300; then 30 multiples of 10 up to 300; then 30 of 1 to 30. All 360
are drawn before any arm answers.

| | property |
|---|---|
| P1 | the count is the statement read literally |
| P2 | the number 1 less: one fewer when its own digits sum evenly, the same otherwise |
| P3 | the decade the number is in, from 10a to 10a + 9: five of them |
| P4 | the number times 10, plus 9: five times the number, plus 4 |
| P5 | the count from (num - 1) / 2 to num / 2 |
| P6 | each arm agrees with at least three of the other five |

P2 holds since the counts of num and num - 1 differ by num alone. P3
holds since the digits of 10a to 10a + 9 sum to a's sum plus 0 to 9,
five of them even. P4 holds since 0 to 10n + 9 is n + 1 decades of five
each, and 0, whose sum is even, is not counted. P5 holds by the closed
form above.

The differential prints `360 numbers: checksum 561687704, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading of the same
numbers. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Thirty edits to the differential, five to each Kāra arm, seven to the
iter arm and three to the template, each run under `karac
__mir-llvm-run` and `karac __mir-run`. Seventeen are kept, three to each
Kāra arm and two to the Rust-template arm. Each kept one is killed,
fails the same way under both backends and not by a crash, and no two
kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: 0 counted too | P1 360, P4 360, P5 252, P6 360 |
| M3 | ★: the leading digit left out | P1 360, P2 178, P4 360, P5 360, P6 360 |
| M4 | ★: the digits counted, not added | P1 354, P2 178, P3 340, P4 360, P5 348, P6 354 |
| M6 | formula: the two halves swapped | P1 218, P2 359, P6 218 |
| M8 | formula: the digit sum of the number before | P1 156, P2 270, P6 156 |
| M10 | formula: an even sum's half rounded up | P1 72, P2 174, P3 322, P4 178, P5 72, P6 72 |
| M11 | table: the last digit never read | P1 360, P2 178, P3 340, P4 360, P5 360, P6 360 |
| M12 | table: two digits dropped | P1 106, P2 179, P6 106 |
| M14 | table: the last digit's parity by 4 | P1 326, P2 116, P3 340, P4 345, P5 296, P6 326 |
| M16 | struct: a carry taking 10 | P1 108, P2 180, P6 108 |
| M18 | struct: no carry | P1 307, P2 182, P3 150, P4 344, P5 285, P6 307 |
| M19 | struct: even by 4 | P1 359, P2 95, P3 340, P4 360, P5 352, P6 359 |
| M21 | iter: the odd sums kept | P1 250, P2 360, P4 360, P5 250, P6 250 |
| M25 | iter: the next number written out | P1 179, P2 337, P3 307, P4 179, P5 71, P6 179 |
| M30 | iter: the count rounded down to even | P1 171, P2 182, P3 340, P4 142, P5 126, P6 171 |
| M26 | solution: the adapter's number 1 less | P1 182, P2 297, P3 322, P4 178, P5 72, P6 182 |
| M28 | solution: each digit halved | P1 324, P2 187, P3 340, P4 346, P5 313, P6 324 |

P1 and P6 kill all seventeen, P2 sixteen, P4 and P5 thirteen each, and
P3 ten. P2 misses only 0 counted too (M1), which adds the same one to
every count, so the steps from one number to the next are right. P3
asks a whole decade, and misses an edit whose errors cancel across one:
0 counted (M1), the leading digit left out (M3), the odd sums (M21),
and the four that keep the count within one of half: the two halves
swapped (M6), the number before (M8), two digits dropped (M12), and a
carry of 10 (M16). P4 and P5 miss those same four: on these numbers each
still gives num / 2 or (num - 1) / 2, only the wrong one of the two
at times, and a number times 10 plus 9 is odd, where the two are the
same; P1 and P2 see them.

Of the thirty, thirteen were not kept. Three are equivalent: the table
arm's 100 read as odd (M15), as its digit sum, 1, is odd already; the
iter arm's digits read in base 16 (M22), where 0 to 9 mean the same;
and the template counting from 2 (M27), as 1's digit sum is odd. Ten
fail as a kept one does: the ★ arm's num left out and the struct arm's
one tick fewer, as M26; the ★ arm's and the table arm's odd sums
counted, as M21; the formula arm's always half, as M16; its every
other digit added, as M12; the struct arm's odometer from 1 and the
iter arm's one number past num, as M25; and the iter arm's first
character skipped and each character worth 1, as M3 and M4.

## Verification

Every arm prints the same output as `even_digits.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the formula arm takes 0.1 s, the table,
template, ★ and struct arms 0.4 s to 0.8 s, and the iter arm 4.9 s,
which writes every number out as a string. The differential takes 10 s:
P4 asks each arm a number ten times as large, and the literal reading
looks every character up.

## Benchmarks

The bench solves 200000 random numbers of 1 to 1000, with the ★ arm in
all five languages. Every implementation prints `200000 solves:
checksum 19857595`.

BENCHTAB
