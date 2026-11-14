# 2119. A Number After a Double Reversal

Reversing an integer means to reverse all its digits. For example,
reversing `2021` gives `1202`. Reversing `12300` gives `321` as the
leading zeros are not retained.

Given an integer `num`, reverse `num` to get `reversed1`, then reverse
`reversed1` to get `reversed2`. Return `true` if `reversed2` equals
`num`. Otherwise return `false`.

```
num = 526   ->  true    (526 -> 625 -> 526)
num = 1800  ->  false   (1800 -> 81 -> 18)
num = 0     ->  true
```

**Constraints:** `0 <= num <= 10^6`.

Reversing drops the zeros a number ends with, which become leading
zeros, and drops nothing else; the second reversal puts every other
digit back. So the answer is the last digit: `true` exactly when `num`
does not end in a zero, or is zero itself.

## Approaches

| file | mechanism |
|---|---|
| `reversed.kara` ★ | the last digit: `num == 0 or num % 10 != 0`. O(1) |
| `reversed_twice.kara` | the statement as it reads: the digits reversed by peeling them off with `% 10` and `/ 10`, twice, and compared. O(digits) |
| `reversed_string.kara` | the number written out with an f-string, its `chars().rev()` collected and parsed back with `i64.parse`, which drops the leading zeros, twice |
| `reversed_struct.kara` | a `struct Digits` of a number's digits, most significant first; `reversed` turns them around with `rev().skip_while(..)` so the zeros that come first go, and the digits are compared after two |
| `reversed_iter.kara` | the digits from `successors` dividing by ten, folded back with `acc * 10 + d`, twice |
| `reversed_solution.kara` | LeetCode's Rust template: a closure reversing through `to_string().chars().rev().collect::<String>().parse::<i32>()`, applied twice, carried by `karac fix` in two rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's three examples and four
more (one digit, a zero inside, the constraints' largest, a number
ending in four zeros), each with its answer; then the count that come
back the same among 5000 random numbers up to 10^6, a third of them
multiplied by a power of ten so that some end in zeros, and a checksum.
`reversed.py` mirrors the ★ arm and its output is byte-identical.

The ★ harness first wrote `10.pow(next_random(mut seed) % 4)`; `karac
fix` made the exponent `(.. % 4) as u32`, the `u32` that `pow` takes.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the decimal digits written out, reversed, and read back with
their leading zeros dropped, twice. It checks 300 random numbers from 0
to 10^6; then 30 that are a power of ten times a number up to 1000;
then 0 to 29. All 360 are drawn before any arm answers; 297 come back
the same.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | a nonzero number with a zero written after it: false |
| P3 | a number with a nonzero digit written after it: true |
| P4 | a nonzero number with a 1 written before it: the same answer |
| P5 | a true answer stays true for the number reversed |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 numbers: checksum 973409774, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading of the same
numbers through `str` and `int`. On a failure it prints the first ten
and then the count by property.

## Mutation testing

Thirty-two edits to the differential, five to seven to each arm, each
run under `karac __mir-llvm-run` and `karac __mir-run`. Seventeen are
kept, three to each Kāra arm and two to the Rust-template arm. Each kept
one is killed, fails the same way under both backends and not by a
crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M2 | ★: the last two digits read | P1 42, P2 296, P6 42 |
| M4 | ★: an odd last digit only | P1 139, P3 171, P5 70, P6 139 |
| M5 | ★: a last 5 taken as a zero | P1 30, P3 42, P5 12, P6 30 |
| M7 | twice: the last digit dropped | P1 338, P2 296, P3 360, P5 42, P6 338 |
| M9 | twice: the loop one step short | P1 296, P3 360, P6 296 |
| M10 | twice: zero changed | P1 1, P6 1 |
| M12 | string: the text not reversed | P1 63, P2 359, P6 63 |
| M14 | string: a one-digit number counted as zero | P1 9, P3 1, P4 9, P6 9 |
| M15 | string: the second reversal of a short number skipped | P1 18, P3 9, P4 26, P6 18 |
| M18 | struct: every zero dropped, not just the leading ones | P1 68, P3 131, P6 68 |
| M19 | struct: one reversal only | P1 282, P3 355, P4 12, P6 282 |
| M20 | struct: the first digit lost | P1 35, P3 43, P4 35, P5 20, P6 35 |
| M23 | iter: the fold adding | P1 287, P3 359, P4 9, P6 287 |
| M25 | iter: the fold seeded with 1 | P1 297, P3 360, P6 297 |
| M31 | iter: a 9 read as a 0 | P1 97, P3 136, P6 97 |
| M29 | solution: a seventh digit dropped | P3 8 |
| M30 | solution: a ten stays | P1 1, P2 1, P4 1, P6 1 |

P1 and P6 kill sixteen, P3 thirteen, P4 six, P2 and P5 four. P3 is the
broad one: every arm that loses or garbles a digit fails on the number
with one more digit written after it, which must always come back. P2
sees the edits that let a trailing zero through: the last two digits
read (M2), the text never reversed (M12), a ten kept (M30), and the
last digit dropped, which also gets zero-ending numbers wrong (M7). P4
sees edits that depend on how long the number is (M14, M15, M20, M23)
or that break one value (M19's single reversal, M30's ten). P5 sees
answers that turn when the number is turned around. M29 is the one kept
edit P1 misses: it truncates to six characters, and only P3's
seven-digit numbers have more.

Of the thirty-two, fifteen were not kept, all killed. Thirteen fail as
a kept one does: one reversal only in the twice, string, iter and Rust
arms as M19; the text not reversed in the Rust arm, the first digit
read by the ★ arm, the struct arm's zeros kept or digits not turned
around, and the iter arm's digits read most significant first, as M12;
the twice arm's digits added and the iter arm's last step of
`successors` dropped as M23; the string arm's first character dropped
as M9; the ★ arm's zero taken as changed as M10. The Rust arm's comparison
negated (P1 360, P2 359, P3 360, P5 63, P6 360) and the iter arm's last
five digits only (P3 219, P4 178) are killed with checks of their own
but were left out because their arms keep their share.

## Verification

Every arm prints the same output as `reversed.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.2 s to 0.3 s, and the
differential 0.4 s.

`karac fix` carries the template in two rounds of 5 and 2 edits: the
closure's `-> i32` deleted, `collect::<String>()` rewritten as
`String.from_iter(..)`, `struct Solution;` to `struct Solution {}` and
`::` to `.`; then `parse::<i32>()` to `i32.parse(..)`.

The template met a compiler gap, fixed in karac with a test named for
this kata (karac 115ea5b11c, `tests/kata_2119_collect_then_parse_fix.rs`).
A `collect::<String>()` whose result is the receiver of a further call
had no fix, only a message to bind it first, while the `parse::<i32>()`
after it did: `karac fix` moved the `collect` into the argument of
`i32.parse(..)`, then deleted its list there, and the program was left
with a `collect` into the `Str` that `parse` reads, refused with "an
expression whose type does not lower". A named `collect` that is a
receiver is now rewritten as its collection's `from_iter`, which needs
nothing from where it is used, and the `parse` on it waits for that
round.

## Benchmarks

The ★ arm is one remainder, which leaves nothing to time, so the bench
runs the arithmetic arm instead, the statement's own work. It builds
1000000 numbers up to 10^6 once, a third of them ending in three
zeros, then checks every one 100 times, raising one number by one
before each round. Every implementation prints `100000000 checks:
60964892 the same, checksum 956707119`.

BENCHTAB
