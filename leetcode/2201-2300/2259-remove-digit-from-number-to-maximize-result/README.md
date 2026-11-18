# 2259. Remove Digit From Number to Maximize Result

You are given a string `number` representing a **positive integer** and
a character `digit`.

Return *the resulting string after removing **exactly one occurrence**
of* `digit` *from* `number` *such that the value of the resulting
string in **decimal** form is **maximized***. The test cases are
generated such that `digit` occurs at least once in `number`.

```
number = "123",  digit = '3'  ->  "12"
number = "1231", digit = '1'  ->  "231"
number = "551",  digit = '5'  ->  "51"
```

**Constraints:** `2 <= number.length <= 100`; `number` consists of
digits from `'1'` to `'9'`; `digit` is a digit from `'1'` to `'9'`;
`digit` occurs at least once in `number`.

Every candidate has the same length, so the larger number is the one
whose first differing digit is larger, and comparing the strings
compares the numbers. Cutting the occurrence at `i` shifts the next
digit into place `i`: the result beats every later cut exactly when
that digit is larger than `digit`. So the first occurrence followed by
a larger digit is the answer, and when there is none, the last
occurrence, which leaves every earlier digit where it was. One pass,
O(n); building and comparing every candidate is O(n^2), which the
length of 100 allows.

## Approaches

| file | mechanism |
|---|---|
| `remove.kara` ★ | one pass over `number.bytes()` remembering the last occurrence, stopped by `break` at the first one followed by a larger byte; the answer two `substring`s in an f-string |
| `remove_all.kara` | every candidate built from two `substring`s joined by `+`, the largest kept by `>` on `String` |
| `remove_iter.kara` | one chain: `char_indices`, `filter` to the occurrences, `map` to the cut, `max`, `unwrap` |
| `remove_compare.kara` | no candidate built until the end: `at(bytes, skip, k)` reads the `k`th digit of the number cut at `skip`, and each later occurrence challenges the best so far digit by digit over the whole length |
| `remove_struct.kara` | `struct Digits` of values 0 to 9 parsed by `to_digit`; `without(i)` a copy with one `remove`d, `greater` a `zip` over two, `to_string` a `join`; the best held in an `Option[Digits]` matched with `Some(ref b)` |
| `remove_solution.kara` | LeetCode's Rust template: `String` and `char` in, `String` out; the number as a `Vec<char>`, each occurrence's candidate a `clone` with `remove(i)` collected back into a `String`, the largest kept by `>`; carried by `karac fix` in one round |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 11 lines: LeetCode's three examples and four
more (a two-digit number of one digit twice; the digit in front; two
cuts that give the same number; a run of the digit before a larger
one), each with its answer; then 5000 numbers of 2 to 20 digits from
'1' up to '2', '3', '4' or '9' in turn, with how many lose their last
occurrence and a checksum of the answers; then three of the
constraints' longest, 100 digits: one digit a hundred times, digits
that only fall, and random ones, each with its first 30 digits and a
checksum. `remove.py` mirrors the ★ arm and its output is
byte-identical.

`karac fix` carries the template in one round of 6 edits: `Vec<char>`
to `Vec[char]`, `String::new()` to `String.new()`, `struct Solution;`
to `struct Solution {}`, and in the adapter `Solution::remove_digit` to
`Solution.remove_digit` with the `.clone()` of `number` dropped, since
a parameter borrows.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every occurrence of `digit` cut out in turn, each result
read as an `i64` by `i64.parse`, and the largest value written back.
No string comparison, no greedy rule; 18 digits fit in an `i64`. It
checks 300 random numbers of 2 to 18 digits from '1' up to '2', '3',
'4' or '9'; then 30 of one digit repeated with one other digit put in
somewhere; then 30 whose digits never fall or never rise. All 360 are
drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | the answer is the number with one occurrence of `digit` cut out |
| P3 | a digit other than `digit` put in front: the same digit in front of the answer |
| P4 | no other cut of `digit` gives a larger string |
| P5 | `digit` put on the end: the larger of the number and the answer with `digit` on the end |
| P6 | each arm agrees with at least three of the other five |

P5 holds because the candidates of `number` followed by `digit` are
`number` itself, cut at the new end, and every old candidate with
`digit` on the end, the best of which ends the best old one.

The differential prints `360 cases: checksum 439794585, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that takes
the largest `int` of the cuts. On a failure it prints the first ten and
then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M4 | ★: the first digit cut instead | P1 263, P2 208, P3 353, P4 149, P5 167, P6 263 |
| M5 | ★: the next digit read two on | P1 42, P4 42, P5 38, P6 42 |
| M6 | ★: the cut one place late | P1 360, P2 360, P4 158, P5 235, P6 360 |
| M8 | all: only the first digits compared | P1 91, P3 32, P4 91, P5 144, P6 91 |
| M10 | all: every digit cut, not only `digit` | P1 234, P2 234, P3 34, P6 234 |
| M11 | all: the position not moved past `digit` | P1 103, P2 86, P4 28, P5 86, P6 103 |
| M13 | iter: the two sides of the cut swapped | P1 253, P2 241, P3 296, P4 65, P5 205, P6 253 |
| M14 | iter: the cut digit left in, its successor cut | P1 309, P2 298, P4 90, P5 40, P6 309 |
| M15 | iter: the cut taking two digits | P1 281, P2 273, P4 140, P5 7, P6 281 |
| M18 | compare: the comparison inverted | P1 200, P4 200, P5 268, P6 200 |
| M19 | compare: the skip read one early | P1 103, P3 30, P4 103, P5 127, P6 103 |
| M21 | compare: only the first occurrence compared | P1 104, P4 104, P5 163, P6 104 |
| M23 | struct: the digit after the one removed | P1 248, P2 223, P4 90, P6 248 |
| M24 | struct: every candidate better | P1 109, P4 109, P5 103, P6 109 |
| M26 | struct: the first digit skipped in the comparison | P1 46, P3 46, P4 46, P5 45, P6 46 |
| M30 | solution: the last char never a candidate | P1 47, P2 22, P3 22, P4 47, P5 117, P6 47 |
| M31 | solution: the chars reversed back | P1 303, P2 300, P3 359, P4 165, P5 316, P6 303 |

P1 and P6 kill all seventeen, P4 sixteen, P5 fifteen, P2 ten and P3
eight. P2 catches the edits that cut the wrong place or keep the
digit: their answer is not one of the cuts at all. P3 catches the ones
that read the number from its front or compare from the wrong place,
since a digit put in front moves everything they read. P4 and P5 catch
the wrong choice among right cuts.

Of the thirty-one, fourteen were not kept, and none differs between the
backends. Two survive and are equivalent: the `compare` arm's
challenger winning a tie (M17) and its last digit never compared (M20)
change nothing, since two cuts that give the same string are the same
answer, and two cuts at `i < j` differ only before `j`, where the last
place is reached only when every digit from `i` on is `digit`. The
`all` arm's first candidate kept on a tie was equivalent for the first
reason and was replaced by M8. One crashes: the struct arm's digits read one less (M25)
never finds a `1`, and its `unwrap` panics, under both backends alike;
the `iter` arm's other digits cut panicked the same way on a number of
one digit only and was replaced by M13. Ten fail as a kept one does:
the largest-for-smallest edits in the ★, `all`, `iter`, struct and
template arms (M3, M7, M12, M22, M27) as `compare`'s comparison
inverted (M18); the first occurrence always taken in the ★, `iter` and
template arms (M1, M16, M29) as `compare`'s (M21); the `all` arm's
position counted from 1 (M9) as `iter`'s successor cut (M14); and the
template's next char removed (M28) as the struct arm's (M23). The ★
arm's stop at an equal next digit (M2) fails in a way of its own and is
left out because its arm keeps enough.

## Verification

Every arm prints the same output as `remove.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the ★ and `all` arms take 0.4 s, `compare`
0.5 s, `iter` 0.6 s, the struct arm 0.9 s, the template 1.2 s, and the
differential 0.8 s.

## Benchmarks

The bench answers 10^6 numbers of 100 digits, each a window of a pool
of 10^6 random digits from '1' to '9' at a random offset, the digit to
remove the window's middle one, with the ★ arm in all five languages,
and folds every answer's bytes into a checksum. Every implementation
prints `10^6 numbers of 100 digits: checksum 506707119`. The C mirror
copies each window into a stack buffer and writes the answer into
another; the others build a new string per answer.

BENCHTAB
