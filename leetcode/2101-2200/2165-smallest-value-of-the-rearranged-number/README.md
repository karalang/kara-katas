# 2165. Smallest Value of the Rearranged Number

You are given an integer `num`. **Rearrange** the digits of `num` such
that its value is **minimized** and it does not contain **any** leading
zeros.

Return *the rearranged number with minimal value*.

Note that the sign of the number does not change after rearranging the
digits.

```
num = 310    ->  103
num = -7605  ->  -7650
```

**Constraints:** `-10^15 <= num <= 10^15`.

Below zero the smallest value is the largest arrangement of the digits,
so they go largest first. Otherwise they go smallest first, and the
first digit other than 0 is brought to the front, since the number may
not start with 0. O(d log d), d the digits.

## Approaches

| file | mechanism |
|---|---|
| `smallest.kara` ★ | the digits from the text of the number's size, sorted falling below zero and rising otherwise, the first digit other than 0 found by `position` and `swap`ped to the front, read back by `fold` |
| `smallest_count.kara` | the digits counted into ten by `% 10` and `/ 10`, never as text; the number built from the counts, below zero from 9 down, otherwise the least digit other than 0 first and then every digit from 0 up. O(d) |
| `smallest_text.kara` | the number's characters sorted, reversed below zero; otherwise the first character other than `'0'` `remove`d and `insert`ed in front; `collect`ed into a `String` and read back by `i64.parse` |
| `smallest_struct.kara` | a `struct Rearranged` holding the sign and the digits, made `of` a number; `smallest` puts the digits in order (`mut ref self`) and `value` reads them back (`ref self`) |
| `smallest_iter.kara` | the digits by `successors` dividing by 10, sorted; the lead found by `position` and put before the zeros and the rest by `once` and `chain`, the number read back by `fold` |
| `smallest_solution.kara` | LeetCode's Rust template: the bytes of `num.abs().to_string().into_bytes()`, `sort_unstable_by` and `sort_unstable`, `position(\|&c\| c != b'0')` and `swap`, read back by `String::from_utf8` and `parse::<i64>()`; carried by `karac fix` in two rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 10 lines: LeetCode's two examples and six
more (zero, the least and the most the constraints allow, zeros inside,
one digit below zero, and ten below zero), each with its answer; then
the total and a checksum over 2000 random numbers of 1 to 15 digits,
about half below zero, the digits from 0 to 1, 0 to 4 or 0 to 9 in
turn; then a checksum over the digits 0 to 9 in every rotation, each
way of signing. `smallest.py` mirrors the ★ arm and its output is
byte-identical.

The text arm was first written as Rust would, on the `String` itself:
`find` with a closure, then `remove` and `insert`. `find` was refused
with a message that names the needles it takes; `String.remove` and
`String.insert` with a bare "no method", with no word that a `Vec[char]`
has both. The struct arm first brought the lead forward by turning a slice of
the digits with `rotate_left`, which was refused just as barely, though
a `Vec` has it. The two bare refusals are ledger row B-2026-11-14-63,
fixed in karac 1617e3a972: each now names the Kāra spelling. The arms hold a
`Vec[char]` and the struct arm uses `remove` and `insert`. The iterator arm was carried by
`karac fix` in one round of 2 edits: the `.cloned()` that each `chain`
of `take` and `skip` needs, since they give `ref i64`.

`karac fix` carries the template in two rounds of 11 and 3 edits:
Rust's spellings (`Vec<u8>` to `Vec[u8]`, `String::from_utf8(..)
.unwrap().parse::<i64>()` to `i64.parse(String.from_utf8(..)
.unwrap())`, `|&c|` to `|c|`, `struct Solution;` to `struct Solution
{}`, `Solution::` to `.`); then `into_bytes()` to `bytes().to_vec()`,
and `sort_unstable` and `sort_unstable_by` to `sort` and `sort_by`,
since a stable sort is also an unstable one.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the digits put in every order, an order that starts with 0
passed over unless it is the only digit, each read back with the
number's sign, and the least taken; no sorting. It checks 300 random
numbers of 1 to 6 digits from 0 to 1, 0 to 4 or 0 to 9 in turn, about
half below zero; then 30 mostly zeros; then 30 of six different digits.
All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer's digits are the number's digits |
| P3 | the answer rearranged again: the same answer |
| P4 | the number's digits put largest first: the same answer |
| P5 | a 0 put after the number: below zero, the answer ten times as much; otherwise the answer with a 0 after its first digit |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 numbers: checksum 91174555, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading of the same
numbers by `itertools.permutations`. On a failure it prints the first
ten and then the count by property.

## Mutation testing

Twenty-seven edits to the differential, four to six to each arm, each
run under `karac __mir-llvm-run` and `karac __mir-run`. Seventeen are
kept, three to each Kāra arm and two to the Rust-template arm. Each kept
one is killed, fails the same way under both backends and not by a
crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M2 | ★: the first digit swapped with the last other than 0 | P1 107, P5 69, P6 107 |
| M4 | ★: the sign dropped | P1 162, P3 112, P5 121, P6 162 |
| M26 | ★: the zeros sorted last | P1 50, P5 119, P6 50 |
| M5 | count: the last digit never counted | P1 323, P2 323, P3 240, P4 108, P6 323 |
| M8 | count: the leading digit the largest | P1 90, P6 90 |
| M25 | count: the 9s never counted | P1 25, P2 25, P6 25 |
| M9 | text: below zero not reversed | P1 128, P2 71, P5 162, P6 128 |
| M10 | text: the lead put after the first character | P1 108, P2 66, P3 39, P5 95, P6 108 |
| M24 | text: the digits never sorted | P1 208, P2 31, P3 95, P4 185, P5 281, P6 208 |
| M12 | struct: the zeros counted one short | P1 66, P2 66, P5 161, P6 66 |
| M14 | struct: the lead put at the end | P1 123, P2 66, P5 161, P6 123 |
| M15 | struct: a 0 never a digit | P1 137, P2 137, P5 323, P6 137 |
| M16 | iter: the last digit dropped by `successors` | P1 272, P2 272, P3 199, P4 108, P5 51, P6 272 |
| M19 | iter: the lead digit read twice | P1 161, P2 161, P3 161, P6 161 |
| M27 | iter: the digits never sorted | P1 175, P3 94, P4 175, P6 175 |
| M22 | solution: the digits above zero sorted falling | P1 107, P5 119, P6 107 |
| M23 | solution: a digit other than 1 swapped to the front | P1 76, P2 28, P5 75, P6 76 |

P1 and P6 kill all seventeen, P5 twelve, P2 eleven, P3 seven and P4
four. P2 compares the answer's digits with the number's; it sees an
edit that drops a digit, reads one twice, or leaves a 0 in front, which
the answer's value then loses (M9, M10, M12, M14, M23). P3 rearranges
the answer again, which a smallest answer survives; it sees an answer
that is not the smallest of its own digits, as with the sign dropped
(M4) or the digits left unsorted (M24, M27). P4 puts the number's
digits in another order first, which a right answer ignores; it sees
only the edits whose answer depends on that order: the digits never
sorted (M24, M27), and the last digit lost (M5, M16), which is a
different digit once they are reordered. P5 puts a 0 after the number;
it sees the edits that misplace the zeros or the lead, or read the
digits the wrong way below zero, and misses five whose wrong answers
take the added 0 as a right one does (M5, M8, M19, M25, M27).

Of the twenty-seven, ten were not kept. None is equivalent and none
crashes; each fails as a kept one does. The digits read rising below
zero in the ★, counting, struct and iterator arms fail as M9; no digit
brought to the front in the ★ arm, the lead found among the zeros in the
text arm, the zeros before the lead dropped in the iterator arm, and
the template's swap with the first 0 fail as M12; the template's answer
never negated fails as M4; and the counting arm's leading digit left in
its count fails as M19.

## Verification

Every arm prints the same output as `smallest.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.1 s to 0.3 s and the
differential 0.7 s.

## Benchmarks

The bench builds 1000 numbers of 1 to 14 digits once, about half below
zero; then makes 1000 passes, each number moved by a step from -1000 to
1000 before it is solved so that no solve repeats one before, with the ★
arm in all five languages, each taking the digits from the number's
text: C by `snprintf` and `qsort`, Go by `strconv` and `sort.Slice`.
Every implementation prints `1000000 solves: checksum 605102486`.

BENCHTAB
