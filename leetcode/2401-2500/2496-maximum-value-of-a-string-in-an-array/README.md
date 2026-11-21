# 2496. Maximum Value of a String in an Array

The **value** of an alphanumeric string can be defined as:

- The **numeric** representation of the string in base `10`, if it
  comprises of digits **only**.
- The **length** of the string, otherwise.

Given an array `strs` of alphanumeric strings, return *the **maximum
value** of any string in* `strs`.

```
strs = ["alic3","bob","3","4","00000"]  ->  5
strs = ["1","01","001","0001"]          ->  1
```

**Constraints:** `1 <= strs.length <= 100`; `1 <= strs[i].length <= 9`;
`strs[i]` consists of only lowercase English letters and digits.

Nine digits make at most 999999999, so every value fits an `i32`. A
string of digits with leading zeros is worth its number, not its
length: `"00000"` is worth 0. The approaches differ in how they tell a
string of digits from a word and read its number.

## Approaches

| file | mechanism |
|---|---|
| `value.kara` ★ | one pass over each string's characters builds its number with `is_ascii_digit` and notes whether any character is not a digit; the string's worth is the number or the length. O(total length) |
| `value_rec.kara` | recursion: a string's number built a character at a time, -1 at the first that is not a digit; the list's best as the larger of its first string's worth and the best of the rest. O(total length) |
| `value_parse.kara` | the library's parser: `match i64.parse(s)`, a refused string worth its length. O(total length) |
| `value_bytes.kara` | over bytes: a `match` with the range pattern `b'0'..=b'9'` adds a digit to the number, and any other byte sets the length and `break`s. O(total length) |
| `value_iter.kara` | iterators: each string `map`ped to its worth, its characters asked by `all` and `fold`ed into the number, then the `max`. O(total length) |
| `value_solution.kara` | LeetCode's Rust template: `Vec<String>` in, `i32` out; `s.parse::<i32>().unwrap_or(s.len() as i32)` over `iter().map`, then `max().unwrap()`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 21 lines: LeetCode's two examples and seven
more; then, for each chance of a digit from none in 8 to all, 2000
random lists of 1 to 100 strings of 1 to 9 characters as a checksum;
then the constraints' largest, 100 strings of 9 characters: all
`999999999`; words and strings of digits with a letter at the end; and
99 strings of a letter and eight nines before `100000000`. `value.py`
mirrors the ★ arm and its output is byte-identical, and the mirror was
checked on 20000 random lists against Python's `isdigit` and `int`, and
the two agreed on every list.

`check` first reports 3 errors on the template: `struct Solution;`,
`Vec<String>`, and the turbofish of `s.parse::<i32>()`. `karac fix`
carries it in one call, reporting 6 edits: `struct Solution {}`; the
brackets; `s.parse::<i32>()` becomes `i32.parse(s)`, the type to parse
to named before the call; and the wrapper's `as i64` on the template's
answer is dropped, since an `i32` widens to `i64` on its own. The
`s.len() as i32` stands, a narrowing written out.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: a string is all digits when every character is one of
`"0123456789"`, its number then the sum of each digit's place value, a
power of ten counted from the right, each digit found by its place in
`"0123456789"`; any other string is worth its length. No character is
asked whether it is a digit, and nothing is parsed. It checks 300 random
lists of 1 to 8 strings of 1 to 9 characters, each a digit with a chance
from none in 4 to all; then 20 lists of one string, and 40 of 100. All
360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer is some string's worth, and no string with a letter is longer |
| P3 | the strings in the other order: the same answer |
| P4 | a 0 put before every string of digits shorter than 9: the same answer |
| P5 | when no string is longer than 8, an `a` put after every one: one more than the longest length |
| P6 | each arm agrees with at least three of the other five |

P4 holds because a leading zero leaves a number as it was. P5 holds
because every string then has a letter, so each is worth its length,
one more than before.

The differential prints `360 cases: checksum 864866536, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases. On a failure it prints the first ten and then the count
by property.

The literal reading first asked `"0123456789".contains(c)` of a `char`,
which `check` refuses: `contains` takes a `Str` pattern
(`docs/library/strings.md`), and the message names `c.to_string()`. It
asks `"0123456789".chars().any(|d| d == c)` instead.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a letter never noticed | P1 252, P2 252, P5 203, P6 252 |
| M4 | ★: the digits added up | P1 148, P2 141, P6 148 |
| M5 | ★: the least kept | P1 358, P2 353, P5 205, P6 358 |
| M7 | rec: a letter ends the number with what it has | P1 213, P2 213, P5 201, P6 213 |
| M9 | rec: the last character never read | P1 170, P2 156, P5 86, P6 170 |
| M11 | rec: a number of 0 taken for a word | P1 2, P2 2, P4 2, P6 2 |
| M13 | parse: a number worth its length | P1 156, P2 85, P4 64, P6 156 |
| M15 | parse: every worth one over | P1 360, P2 360, P5 205, P6 360 |
| M16 | parse: only the last string counted | P1 231, P2 165, P3 278, P5 106, P6 231 |
| M18 | bytes: 9 not a digit | P1 59, P2 7, P4 5, P6 59 |
| M19 | bytes: 0 not a digit | P1 62, P2 9, P4 126, P6 62 |
| M21 | bytes: every digit one over | P1 159, P2 159, P4 143, P6 159 |
| M22 | iter: any digit enough | P1 186, P2 186, P5 155, P6 186 |
| M24 | iter: the fold begun at 1 | P1 175, P2 175, P4 143, P6 175 |
| M26 | iter: the digits read backwards | P1 146, P2 145, P4 147, P6 146 |
| M30 | solution: the length one over | P1 204, P2 204, P5 205, P6 204 |
| M31 | solution: parsed to an i16 | P1 90, P2 9, P4 8, P6 90 |

P1, P2 and P6 kill all seventeen, P4 and P5 eight each, and P3 one.

Fourteen are not kept, and none survives. Three fail exactly as a kept
one: the ★ arm's every string worth its digits' number (M3) as its
letter never noticed (M1), since both give a string with a letter the
number its digits make; and the ★ and template arms' every string worth
its length (M2, M28) as the parse arm's number worth its length (M13).
Ten fail as one another, in four sets, none of whose members could be
kept beside the kept edits of their arms: the ★ arm's first string only
and the rec arm's rest never asked (M6, M8); the rec arm's empty rest
worth 1 and the parse arm's best begun at 1 (M10, M14), wrong only on
the 2 lists whose every string is a run of zeros; the parse, bytes and
template arms' string with a letter worth 0 and the iter arm's length
one short (M12, M20, M27, M25), all of which lower every string with a
letter, and so fail on the cases whose answer is such a string's length;
and the iter and template arms' least taken (M23, M29). The bytes arm's
break forgotten (M17) fails in a way of its own, but its arm already
holds its three.

## Verification

Every arm prints the same output as `value.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 11.0 to 13.4 s and the differential 3.0 s; under `karac __mir-llvm-asan` the arms take 1.9 to 2.4 s and the differential 0.8 s; and under `karac run` the differential takes 0.6 s.

## Benchmarks

The bench builds 2000 lists of 100 strings once from its own generator,
each character a digit or a letter with even chance; then makes 90
passes. Each puts the checksum so far, written in digits, in place of
one string of every list, asks, and puts the string back, folding the
answer plus the pass into the checksum. The bench uses the ★ arm in all
five languages: C with each string a 10-byte array and `snprintf`, Go
with `strconv`, and Rust and Kāra cloning the replaced string out and
moving it back. Every implementation prints `90 passes over 2000 lists
of 100: checksum 18760984`.

BENCHTAB
