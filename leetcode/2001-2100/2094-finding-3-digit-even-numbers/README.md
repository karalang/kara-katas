# 2094. Finding 3-Digit Even Numbers

You are given an integer array `digits`, where each element is a digit.
The array may contain duplicates.

You need to find all the unique integers that follow the given
requirements:

- The integer consists of the concatenation of three elements from
  `digits` in any arbitrary order.
- The integer does not have leading zeros.
- The integer is even.

For example, if the given `digits` were `[1, 2, 3]`, integers `132` and
`312` follow the requirements.

Return a sorted array of the unique integers.

```
digits = [2,1,3,0]    ->  [102,120,130,132,210,230,302,310,312,320]
digits = [2,2,8,8,2]  ->  [222,228,282,288,822,828,882]
digits = [3,7,5]      ->  []
```

**Constraints:** `3 <= digits.length <= 100`; `0 <= digits[i] <= 9`.

There are only 450 even numbers from 100 to 998, so the answer can be
read off the other way round: count each digit in the list, and keep the
even numbers whose three digits the counts can pay for. Walking them in
order gives the sorted, unique answer at once. The approaches differ in
whether they start from the numbers or from the list, and how they
count.

## Approaches

| file | mechanism |
|---|---|
| `even.kara` ★ | the digits counted in an `[i64; 10]` array, then `(100..1000).step_by(2)`, each number's own counts made and checked against them with `(0..10).all(..)`. O(n + 450 · 10) |
| `even_triples.kara` | from the list: every choice of three different places, the first not a 0 and the last even, each number put in a `SortedSet`, which drops repeats and keeps the order. O(n³ log 450) |
| `even_backtrack.kara` | backtracking over the counts: a recursive `place` takes a digit still in hand for the hundreds, tens and units in turn, smallest first, through a `mut ref` array, and gives it back after |
| `even_text.kara` | by text: the digits written with `char.from_digit` and counted in a `Map[char, i64]`, each even number's `to_string()` counted the same way, and an iterator chain of `step_by`, `filter` and `collect` |
| `even_struct.kara` | a `struct Hand` of the counts with a method `spend` that takes a number's digits out of a copy, fed by an `impl Iterator` over the even three-digit numbers |
| `even_solution.kara` | LeetCode's Rust template (`digits: Vec<i32>`, the counts in a `[0; 10]` indexed by `usize`, three loops over the hundreds from 1, the tens, and `(0..10).step_by(2)`), carried by `karac fix` in two rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 10 lines: LeetCode's three examples and four
more, each list and its numbers; then the count and a checksum of the
numbers for 2000 random lists of 3 to 12 digits, each below 10, 5 or 3;
then the constraints' longest, 100 digits, all 7 but one 4 and one 0,
and every digit ten times. `even.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every number below 1000 that has three digits and is even,
kept when each of its digits can be found and taken out of a copy of the
list in turn. It checks 300 random lists of 3 to 8 digits, each below
10, 5 or 3; then 20 of only 0s and 1s, and 20 of 10 to 20 digits. All
340 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the numbers are the statement read literally |
| P2 | the list reversed and turned by one place gives the same numbers |
| P3 | the numbers are distinct, increasing, even, and from 100 to 998 |
| P4 | a digit more in the list loses no number |
| P5 | the list without its odd digits gives exactly the numbers whose digits are all even |
| P6 | each arm agrees with at least three of the other five |

The differential prints `340 lists: checksum 405702283, 12240 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal numbers was checked against a Python reading of the same
lists. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Thirty edits to the differential, five to each of its arms, each run
under `karac __mir-llvm-run` and `karac __mir-run`. Seventeen are kept,
three to each Kāra arm and two to the Rust-template arm. Each kept one
is killed, fails the same way under both backends and not by a crash,
and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the odd numbers walked too | P1 298, P3 298, P5 234, P6 298 |
| M2 | ★: the tens digit never counted | P1 330, P5 262, P6 330 |
| M3 | ★: the walk from 102 | P1 109, P6 109 |
| M4 | triples: the same place used twice | P1 255, P6 255 |
| M5 | triples: the last place's evenness read from the first | P1 302, P3 261, P5 234, P6 302 |
| M6 | triples: the middle taken only after the first | P1 214, P2 210, P6 214 |
| M7 | backtrack: a digit not given back | P1 294, P4 37, P5 159, P6 294 |
| M8 | backtrack: the evenness asked of the tens | P1 291, P3 291, P5 234, P6 291 |
| M9 | backtrack: the digit 9 never tried | P1 51, P6 51 |
| M10 | text: a character missing taken as one held | P1 338, P5 340, P6 338 |
| M11 | text: each character counted once | P1 284, P6 284 |
| M12 | text: steps of 4 | P1 294, P6 294 |
| M13 | struct: two digits spent | P1 333, P5 301, P6 333 |
| M14 | struct: the iterator ending at 996 | P1 9, P6 9 |
| M15 | struct: the iterator from 98 | P1 12, P3 12, P6 12 |
| M16 | solution: the hundreds from 0 | P1 233, P3 233, P6 233 |
| M17 | solution: the tens not taken out | P1 260, P5 97, P6 260 |

P1 and P6 kill all seventeen, P5 eight, P3 five, and P2 and P4 one
each. P5 sees an arm that lets a number through the counts cannot pay
for, since the list of even digits then answers with numbers holding an
odd digit or a digit too often (M1, M2, M5, M7, M8, M10, M13, M17). P3
sees a number that is odd, below 100 or above 998 (M1, M5, M8, M15,
M16). P2 sees only M6, the one edit that makes the answer depend on the
order of the list, and P4 only M7, whose digits run out as it goes, so
a longer list can lose a number. The rest are numbers missed or let
through that keep the shape, which only the literal reading and the
other arms see (M3, M4, M9, M11, M12, M14).

Of the thirty, thirteen were not kept, and none survives. Six fail as a
kept one: a leading 0 allowed, in the triples and backtrack arms, as
M16; the triples arm's tens and units swapped as M8; the backtrack arm's
digit never taken out, and the struct arm's digit spent but never taken
out, as M11; the text arm's walk stopping at 900 as M9. Two fail the
same way as each other and were left out together: a digit wanted once
more than held, in the ★ and text arms (P1 340, P5 340). Five are
killed with checks of their own but were left out because their arm
keeps its share: the ★ arm's digit 9 never checked (P1 319, P5 333),
the struct arm's units spent twice (P1 333, P5 219), and the Rust arm's
units from 1 (P1 337, P3 298, P5 234), hundreds not taken out (P1 270)
and adapter dropping the first digit (P1 254, P2 202, P5 52).

## Verification

Every arm prints the same output as `even.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them.

Under `karac __mir-run` the arms take 0.6 s to 2.4 s, but for the ★
arm's 10 s, whose `(0..10).all(..)` calls its closure ten times for each
of the 450 numbers, and the text arm's 15 s, which builds a string and a
`Map` for each; the differential takes 21 s (timed while other work
shared the machine).

No arm met a compiler gap. The text arm writes each digit as Rust does,
`char.from_digit(d as u32, 10)`; without the `as u32` the checker says
so plainly, then adds a second error that the `collect` has no
`FromIterator[<error>]`, which follows from the first. The Rust arm was
written as LeetCode's Rust template. `karac fix` carries it in two
rounds of 18 and 1 edits: Rust's spellings (`Vec<i32>` to brackets, `&`
to `ref` and the `&` of patterns dropped, `Vec::new()` and
`Solution::` to `.`, `struct Solution;` to `struct Solution {}`); then
the adapter's `ref` parameter to a bare one, which borrows already. The
fixed arm reads as the template does.

## Benchmarks

The bench draws 100000 random lists of 3 to 100 digits, each below 10, 6
or 4, and answers each with the ★ arm in all five languages: the counts
in a fixed array of ten, the walk over the even numbers, and the answer
in a growable array (a `Vec`, a `Vec`, a slice, a `list`, a `malloc`'d
buffer). Every implementation prints `100000 answers: 16002243 numbers,
checksum 952655057`.

BENCHTAB
