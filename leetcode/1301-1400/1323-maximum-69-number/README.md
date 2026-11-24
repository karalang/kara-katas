# 1323. Maximum 69 Number

You are given a positive integer `num` consisting only of digits `6` and
`9`.

Return the maximum number you can get by changing **at most** one digit
(`6` becomes `9`, and `9` becomes `6`).

```
num = 9669  ->  9969
num = 9996  ->  9999
num = 9999  ->  9999
```

**Constraints:** `1 <= num <= 10^4`, `num` consists of only `6` and `9`
digits.

The arms are `fn maximum69_number(num: i32) -> i32`.

## Approaches

Turning a 9 into a 6 only loses, and a 6 into a 9 gains 3 times its
place, so the answer turns the first 6, the highest, if there is one.

| file | mechanism |
|---|---|
| `maximum69_number.kara` ★ | the number written out, its first 6 turned to a 9 by `replacen`, and the text read back by `i32.parse`. O(digits) |
| `maximum69_number_place.kara` | the digits read off from the right by `% 10` and `/ 10`, the place of the last 6 met, which is the highest, kept, and 3 times that place added. O(digits) |
| `maximum69_number_every.kara` | every single digit changed in turn, a 6 to a 9 or a 9 to a 6, each change worked out from the digit's place by an `if` value, and the largest of those and the number itself kept. O(digits) |
| `maximum69_number_digits.kara` | the number taken apart into a `Vec` of digits, most significant first, the first 6 found by `position` turned to a 9, and the digits folded back into a number. O(digits) |
| `maximum69_number_solution.kara` | a Rust solution as LeetCode's Rust users write it (`num.to_string().replacen('6', "9", 1).parse().unwrap()`), carried to Kāra by `karac fix` |
| `maximum69_number_bytes.kara` | a second Rust solution as LeetCode's Rust users write it (the digits as `num.to_string().into_bytes()`, the first `b'6'` found by a `for` loop with `break` and set to `b'9'`, and the bytes made back into a number by `String::from_utf8(..).unwrap().parse()`), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, five more properties |

Every arm prints the same 2 lines: LeetCode's three examples, a lone 6
and a lone 9, and 6666 (`9969 9999 9999 9 9 9666`); then every number the
constraints allow, 1 to 4 digits each a 6 or a 9 (`every one of the 30
numbers: answers total 166917, checksum 379424935`).
`maximum69_number.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac __mir-run`,
`karac run` and `karac __mir-llvm-run`.

The Mend loop: the digits arm checked clean as first written. The ★ arm
read its text back with `.parse().unwrap()` as the tail of a function
returning `i32`; Kāra's `parse` is called on the target type, the method
form takes its target only from an expected `Option[T]`, and `karac fix`
wrote `i32.parse(f"{num}".replacen("6", "9", 1)).unwrap()` (1 fix). The
place arm's `let mut place = 1` and `let mut highest_six = 0` kept the
default `i64` and met `num: i32`; `karac fix` declared both `i32` (2
fixes). The every arm is the one B-2026-11-21-64 was filed from when
this kata was first written: its `let changed = if d == 6 { num + 3 *
place } else { num - 3 * place }`, with `place` a defaulted literal, was
refused at an `i32` slot with no fix, where the same arithmetic without
the `if` was told to declare `place: i32`. Fixed since, the diagnostic
names `place` through the `if`, and `karac fix` declares it (1 fix). The
first Rust arm takes one round of 4 fixes by `karac fix`'s count, from 2
errors: `struct Solution;` to `struct Solution {}`, `::` to `.`,
`replacen('6', ..)` to `replacen("6", ..)`, since a pattern is a `Str`,
and the `.parse()` to `i32.parse(..)`. The second takes one round of 5
fixes from 3 errors: the same, with `into_bytes()` to `bytes().to_vec()`
and `String::from_utf8` to `String.from_utf8`. Both outputs match on the
first run.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the number itself and every number made by changing one of its
digits, a 6 to a 9 or a 9 to a 6, and the largest of them. It asks every
one of the 30 numbers the constraints allow.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | no less than the number, and no more than a 6 turned in its first place would give |
| P3 | as many digits, at most one of them changed, and that one a 6 made a 9 |
| P4 | a 9 put in front, which stays: the answer with that 9 in front |
| P5 | a 6 put in front, which is then the first 6: the number itself with a 9 in front |
| P6 | the ★ arm's answer |

P4 and P5 ask only for numbers of up to 3 digits, 14 of the 30, so that
the new number stays within the constraints. All 888 checks pass on every
arm: `30 numbers: checksum 379424935, 888 checks over 6 arms: 0
failures`, under `karac __mir-run` and `karac __mir-llvm-run`. Python
gives the same checksum.

## Mutation testing

Fifteen edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`. Three are left out: the digits arm
turning the last 6 rather than the first fails exactly the checks the
place arm keeping the lowest 6 fails; the Rust arm turning up to two 6s
fails exactly the checks the ★ arm turning every 6 fails, since no
number here has a third 6 where the two differ in passing; and one
version of the every arm's edit was refused as written, its `0` a
defaulted `i64` that `karac` asks to declare. The twelve kept, two to
each arm, are each killed, fail the same way under both backends and not
by a crash, and no two fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: every 6 turned to a 9 | P1 16, P2 11, P3 16, P5 11, P6 80 |
| M2 | ★: the first 9 turned to a 6 | P1 30, P2 26, P3 26, P4 14, P5 14, P6 150 |
| M3 | place: the lowest 6 kept, not the highest | P1 16, P5 11, P6 16 |
| M4 | place: a 6 adding 4 times its place | P1 26, P2 15, P3 26, P5 14, P6 26 |
| M5 | every: the number itself never a candidate | P1 4, P2 4, P3 4, P6 4 |
| M6 | every: a 9 made a 6 counted as a gain | P1 15, P3 15, P4 14, P6 15 |
| M7 | digits: the digits left least significant first | P1 10, P2 6, P3 8, P4 5, P5 6, P6 10 |
| M8 | digits: the fold started from 1 | P1 30, P2 30, P3 30, P4 14, P5 14, P6 30 |
| M9 | solution: only a 6 followed by a 6 turned | P1 15, P5 7, P6 15 |
| M10 | solution: a 6 turned to an 8 | P1 26, P3 26, P5 14, P6 26 |
| M11 | bytes: the last digit never looked at | P1 4, P6 4 |
| M12 | bytes: the first digit never looked at | P1 15, P4 7, P5 14, P6 15 |

P1 and P6 kill all twelve, P5 nine, P3 eight, P2 six and P4 five. A 6 in
front (P5) must become the 9, so it catches every edit that turns the
wrong 6, more than one, or a wrong digit (M1 to M4, M7 to M10, M12), and
misses only the edits that go wrong on the number's own digits alone
(M5, M6, M11). The shape of the answer (P3) catches every edit that
writes a digit other than a 9 for a 6, changes two digits, or loses one
(M1, M2, M4 to M8, M10), and misses the four that turn a single 6 the
wrong way round in place (M3, M9) or not at all (M11, M12). The bounds
(P2) catch the edits whose answer falls below the number or rises past
its first place's gain. A 9 in front (P4) must change nothing behind it,
and catches the edits that touch that 9 or read the number's first digit
wrong (M2, M6, M7, M8, M12). M11, which misses a 6 only when it is the
last digit and the only one, shows only against the statement and the ★
arm.

## Benchmarks

The bench asks the 30 numbers the constraints allow, 100000 times over:
each pass starts at a place chosen by the checksum so far and folds every
answer plus the pass into it. Each call writes the number into fresh
text in every language, a `malloc` in C. Every implementation prints
`100000 passes over the 30 numbers: checksum 825792792`.

BENCHTAB
