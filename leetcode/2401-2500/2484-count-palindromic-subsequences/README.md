# 2484. Count Palindromic Subsequences

Given a string of digits `s`, return *the number of **palindromic
subsequences** of* `s` *having length* `5`. Since the answer may be very
large, return it **modulo** `10^9 + 7`.

**Note:**

- A string is **palindromic** if it reads the same forward and backward.
- A **subsequence** is a string that can be derived from another string
  by deleting some or no characters without changing the order of the
  remaining characters.

```
s = "103301"      ->  2
s = "0000000"     ->  21
s = "9999900000"  ->  2
```

**Constraints:** `1 <= s.length <= 10^4`; `s` consists of digits.

A palindrome of five digits reads `a b c b a`, so for each place of the
middle `c` the count is the sum, over the hundred digit pairs `a b`, of
the pairs `a b` before it times the pairs `b a` after it. Counts of the
single digits on either side keep the pair counts up to date as the
middle moves, so each place costs a hundred products.

## Approaches

| file | mechanism |
|---|---|
| `palin.kara` ★ | pairs either side of the middle: the pairs after counted once from the right and taken off as the middle moves on, the pairs before added as it passes, each in a list of a hundred. O(100 n) |
| `palin_table.kara` | whole tables: the hundred pair counts before every place and after every place, each row built from the one beside it, then every middle's products summed. O(100 n) time and room |
| `palin_map.kara` | pairs in a `Map`: the ★ arm's running counts kept in `Map[(i64, i64), i64]` keyed by the pair, a missing pair read as none, and each middle's products taken over the pairs present before it. O(100 n) |
| `palin_pattern.kara` | by patterns: each of the hundred shapes `a b ? b a` counted as a subsequence on its own, the ways to match each prefix of the shape moved on by every digit, the last place first, `?` matching any digit. O(100 n) |
| `palin_iter.kara` | iterators: the ★ arm's running counts updated by `for_each` closures, each middle's hundred products by `map` and `sum`, and the middles folded by `fold`. O(100 n) |
| `palin_solution.kara` | LeetCode's Rust template: `String` in, `i32` out; the digits as `usize` from `bytes()`, and for each pair `a b` a `[0i64; 5]` of the ways to match `a b ? b a`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 12 lines: LeetCode's three examples; then
four more, a string too short, exactly five digits that read the same
both ways, five that do not, and every digit once each way round; then
the constraints' largest, `10^4` digits, all `0`, `0` and `1` taking
turns, and random from all ten digits and from two; and 3000 random
strings of 1 to 30 digits drawn from the first 1 to 10, as a checksum.
`palin.py` mirrors the ★ arm and its output is byte-identical, and the
mirror was checked on 3000 random strings of 1 to 14 digits against
every choice of five places, and on the `10^4` zeros against `C(10^4,
5)` taken modulo `10^9 + 7`. They agreed every time.

`check` first reports 3 errors on the template, the brackets of
`Vec<usize>`, the `&` in the pattern `for &c` and the `&` on `&s`, and
`karac fix` carries it in one call, reporting 8 edits: those brackets,
two edits; the pattern's `&` goes and `&s` becomes `ref s`; `bytes()`
becomes `bytes().iter()`, since Kāra's `bytes()` is a list and `map`
needs an iterator; `[0i64; 5]` loses its suffix; `struct Solution {}`
is added; and the wrapper's `as i64` on the `i32` answer goes, since an
`i32` widens by itself. The `const` inside the method, the fixed
`[0; 5]` array, `(b - b'0') as usize` and the `usize` digits compared
with the `i64` loop counters stand as Kāra.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every choice of five places in order taken in turn, and
counted when its digits read the same both ways. No pair is counted.
It checks 300 random strings of 1 to 10 digits, then 60 of up to 14,
each drawn from the first 1 to 10 digits; 120 of the 360 have a
palindrome. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the count is the literal reading's |
| P2 | the string reversed: the same count |
| P3 | every digit renamed, `d` to `(3 d + 7) % 10`: the same count |
| P4 | a digit the string lacks put last, when it lacks one: the same count |
| P5 | every digit made `0`: the ways to choose five of the `n` places |
| P6 | each arm agrees with at least three of the other five |

P2 holds because a palindrome read backwards is the same five places in
the reversed string. P3 holds because `3 d + 7` modulo 10 takes the ten
digits to the ten digits, one to one, so equal digits stay equal and
unequal ones unequal. P4 holds because the new digit equals no other,
so it cannot stand at either end, and as the last place it cannot be
the middle. P5 holds because five places of one digit always read the
same both ways.

The differential prints `360 cases: checksum 488966870, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and tries every choice of five places. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the pairs after stored backwards | P1 231, P2 188, P4 271, P6 231 |
| M2 | ★: the middle's pairs taken off before it leaves | P1 229, P2 200, P4 264, P5 281, P6 229 |
| M4 | ★: a digit paired with itself | P1 137, P2 112, P5 244, P6 137 |
| M7 | table: the pairs before stored backwards | P1 105, P6 105 |
| M8 | table: the middle counted in the pairs after | P1 155, P5 244, P6 155 |
| M11 | table: each row after built afresh | P1 91, P5 183, P6 91 |
| M12 | map: a pair before read the other way round | P1 53, P2 56, P6 53 |
| M15 | map: a pair before counted once however many | P1 63, P2 55, P5 183, P6 63 |
| M16 | map: the pairs before not multiplied | P1 280, P4 319, P5 259, P6 280 |
| M17 | pattern: a digit used for two places | P1 360, P4 360, P5 360, P6 360 |
| M20 | pattern: each pair of digits once | P1 60, P3 63, P6 60 |
| M21 | pattern: four places matched | P1 184, P2 162, P5 208, P6 184 |
| M24 | iter: the pair 9 9 left out | P3 2 |
| M25 | iter: the pairs with 9 never taken off | P1 6, P2 7, P3 68, P4 7, P6 6 |
| M26 | iter: the first digit passed over | P1 145, P2 162, P4 148, P6 145 |
| M27 | solution: a middle never the outer digit | P1 72, P5 213, P6 72 |
| M30 | solution: the digit 0 never outside | P1 55, P3 78, P5 213, P6 55 |

P1 and P6 kill sixteen each, P5 ten, P2 eight, P4 six, and P3 four.
The iter arm's pair 9 9 left out (M24) is killed by P3 alone: a 9 is
drawn only into strings of all ten digits, and the renaming of P3 turns
every 4 into a 9.

Fourteen are not kept. Nine fail exactly as a kept one: four count the
shape `a b ? a b` in place of `a b ? b a`, the ★, map and iter arms'
pairs after read the same way round and the pattern arm's shape `a b ?
a b` (M3, M14, M22, M18), as the table arm's pairs before stored
backwards (M7), every one of them killed by P1 and P6 alone, since that
count too is the same reversed, renamed or lengthened; the ★ arm's
pairs after counted from the left (M6) as its pairs after stored
backwards (M1); the table arm's middle counted in the pairs before
(M10) as in the pairs after (M8); the iter arm's digit paired with
itself (M23) as the ★ arm's (M4); the template's first place counted
once (M28) as the map arm's pair before counted once however many
(M15); and the template's four places counted (M29) as the pattern
arm's four places matched (M21). Four fail alike, apart from every kept
one, each doubling every count or keeping only part of it: the ★ arm's
only the last middle counted, the table and map arms' every digit
before counted twice and the pattern arm's every count doubled (M5, M9,
M13, M19). The template's last place matched to `b` (M31) fails apart
from every kept one, the template having its two kept already. No edit
crashes, and every edit is killed by some check.

Three edits to the map arm were replaced before this table was drawn,
each ending with a key not found where the arm reads a pair it expects
to have stored: a pair after stored the other way round, the middle
never leaving the digits after, and every digit after counted twice. A
fourth, a pair after needing two digits later, ended the same way and
was replaced in turn.

## Verification

Every arm prints the same output as `palin.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 4.1 to 11.2 s, the pattern arm 45.7 s, and the differential 11.4 s; under `karac __mir-llvm-asan` the arms take 1.1 to 4.4 s, the pattern arm 8.3 s, and the differential 2.9 s, and under `karac run` the differential takes 0.6 s.

## Benchmarks

The bench builds 4 random strings of 2000 digits once from its own
generator, then makes 110 passes; each changes one digit of every
string, place and digit chosen by the checksum so far, so no answer
repeats the last, and folds the count plus the pass into the checksum.
The bench uses the ★ arm in all five languages, each string kept as a
list of digits and written out as fresh text for every answer. Every
implementation prints `110 passes over 4 strings of 2000 digits:
checksum 812470864`.

BENCHTAB
