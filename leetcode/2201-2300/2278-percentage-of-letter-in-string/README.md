# 2278. Percentage of Letter in String

Given a string `s` and a character `letter`, return *the **percentage**
of characters in* `s` *that equal* `letter` ***rounded down** to the
nearest whole percent.*

```
s = "foobar", letter = "o"  ->  33
s = "jjjj", letter = "k"    ->  0
```

**Constraints:** `1 <= s.length <= 100`; `s` consists of lowercase
English letters; `letter` is a lowercase English letter.

Count the letter, then `count * 100 / len`: integer division rounds
down, and multiplying first keeps the hundredths that dividing first
would lose. O(n).

## Approaches

| file | mechanism |
|---|---|
| `percent.kara` ★ | one pass over `s.chars()` counting the letter, then `count * 100 / s.len()` |
| `percent_split.kara` | `s.split(letter.to_string()).count() - 1`: cutting at every occurrence leaves one piece more, empty pieces included |
| `percent_bytes.kara` | the letter as one byte, `letter as u32 as u8`, and a `fold` over `s.bytes()` counting it |
| `percent_struct.kara` | `struct Tally` of the letter, the characters seen and the hits; `see` (`mut ref self`) takes a character and `percent` divides |
| `percent_iter.kara` | one chain: `filter` and `count`, scaled, over `s.chars().count()` |
| `percent_solution.kara` | LeetCode's Rust template: `String` and `char` in, `i32` out; `filter(\|&c\| c == letter).count() * 100 / s.len()` cast `as i32`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's two examples and five
more (one letter, 100; a half, 50; a third, 33; two thirds, 66; a
tenth, 10), each with its percentage; then 3000 random strings of 1 to
100 letters from the first 2, 3 or 26, the letter one of the first 3,
with a checksum; then three of the constraints' longest, 100 letters:
random from the first 4 (30), all the letter (100), and the letter once
(1). `percent.py` mirrors the ★ arm and its output is byte-identical.

Two arms were first written as in Rust and carried by `karac fix`. The
split arm passed the `char` itself, `s.split(letter)`; Kāra's `split`
takes a string, and `karac check` names the mismatch and `karac fix`
writes `letter.to_string()`. The bytes arm cast `letter as u8`, which
`karac check` refuses as a narrowing from the Unicode scalar range, and
`karac fix` writes the explicit `letter as u32 as u8`.

`karac fix` carries the template in one round, reporting 4 edits: the
pattern `|&c|` to `|c|`, `struct Solution;` to `struct Solution {}`,
`Solution::` to `Solution.`, and the adapter's `as i64` dropped.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the letter counted by indexing every character, and the
percentage the largest whole `p` from 0 to 100 with `p` percent of the
length at most the count, found by trying each `p` in turn. No
division. It checks 300 random strings of 1 to 100 letters from the
first 1, 2, 3 or 26, the letter one of the first 3; then 30 with the
letter only at the end, after up to 19 `z`; then 30 of 3, 7 and 9
letters, where the rounding bites. All 360 are drawn before any arm
answers.

| | property |
|---|---|
| P1 | the percentage is the literal reading's |
| P2 | the string reversed: the same percentage |
| P3 | the letters relabelled, the alphabet turned by seven, the letter too: the same percentage |
| P4 | from 0 to 100, 0 exactly when the letter is absent and 100 exactly when every character is the letter |
| P5 | the string twice over: the same percentage |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 cases: checksum 427462332, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that floors
a `Fraction` of `s.count(letter)` over the length, times 100. On a
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
| M1 | ★: rounded up | P1 197, P6 197 |
| M3 | ★: the other letters counted | P1 353, P4 136, P6 353 |
| M5 | ★: the first character skipped | P1 74, P2 98, P4 24, P5 72, P6 74 |
| M7 | split: the pieces not less one | P1 360, P4 140, P5 330, P6 360 |
| M8 | split: split at `a` always | P1 219, P3 313, P4 126, P6 219 |
| M9 | split: split at the letter doubled | P1 247, P4 119, P5 13, P6 247 |
| M12 | bytes: the byte after the letter | P1 238, P4 124, P6 238 |
| M15 | bytes: every byte up to the letter counted | P1 200, P3 101, P4 147, P6 200 |
| M16 | bytes: each match counted twice | P1 247, P4 57, P6 247 |
| M17 | struct: each character seen twice | P1 247, P4 30, P6 247 |
| M19 | struct: every character a hit | P1 337, P4 337, P6 337 |
| M20 | struct: the letter taken from the string | P1 268, P2 160, P4 113, P6 268 |
| M22 | iter: the letters from it up counted | P1 193, P3 101, P4 140, P6 193 |
| M23 | iter: divided before scaling | P1 224, P4 224, P6 224 |
| M26 | iter: the length one more | P1 163, P4 23, P5 113, P6 163 |
| M30 | solution: only the first half and one counted | P1 216, P2 193, P4 69, P5 197, P6 216 |
| M31 | solution: the length at least 10 | P1 43, P4 5, P5 43, P6 43 |

P1 and P6 kill all seventeen, P4 sixteen, P5 six, P2 three, and P3
three. P4 checks the two ends without the literal reading, and misses
only rounding up, which keeps 0 and 100 where they belong. P5 catches
an edit whose count or length does not scale with the string: one
character skipped, a count from 1, a length one more, a floor of 10 on
the length, and pairs of the letter, which doubling the string can
join. P2 sees only the edits that read a place in the string, the first
character or the first half; P3 only those that compare letters by
order, or name one.

Of the thirty-one, fourteen were not kept, and none crashes or differs
between the backends. Seven fail as a kept one does: the ★ arm's count
from 1 and the bytes arm's fold from 1 (M2, M14) as the split arm's
pieces not less one (M7); the bytes, struct and template arms' other
letters counted and the struct arm's misses scored (M13, M18, M29,
M21) as the ★ arm's other letters counted (M3); and the ★ arm's length
one more (M4) as the iter arm's (M26). Seven fail in ways of their own
and are left out because their arms keep enough: the ★ arm's rounding
to the nearest (M6), the split arm's empty pieces dropped and its count
scaled by 99 (M10, M11), the iter arm's last character skipped and its
leading run only (M24, M25), and the template's rounding down to tens
and to even (M27, M28).

## Verification

Every arm prints the same output as `percent.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the ★ arm takes 0.4 s, the split arm and the
template 0.4 s, the bytes and struct arms 0.5 s, the iter arm 0.6 s,
and the differential 0.6 s.

## Benchmarks

The bench answers 100000 strings of the constraints' longest, 100
letters from the first 4, each asked for one of the first 4, with the
★ arm in all five languages. Every implementation prints `100000
strings of 100: checksum 88042791`. Each builds its string a letter at
a time from the same generator; Go by a `strings.Builder`, C into a
fresh buffer.

BENCHTAB
