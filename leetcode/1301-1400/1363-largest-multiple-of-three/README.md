# 1363. Largest Multiple of Three

Given an array of digits `digits`, return the largest multiple of three
that can be formed by concatenating some of the given digits in any
order. If there is no answer return an empty string.

Since the answer may not fit in an integer data type, return the answer
as a string. Note that the returning answer must not contain
unnecessary leading zeros.

```
digits = [8,1,9]        ->  "981"
digits = [8,6,7,1,0]    ->  "8760"
digits = [1]            ->  ""
```

**Constraints:** `1 <= digits.length <= 10^4`, `0 <= digits[i] <= 9`.

Each arm is `fn largest_multiple_of_three(digits: Vec[i32]) -> String`;
the Rust solution's takes `own Vec[i32]`.

## Approaches

| file | mechanism |
|---|---|
| `largest_multiple_of_three.kara` ★ | the digits counted, and their sum's residue r mod 3 put right by dropping the smallest digit of residue r, or failing that the two smallest of residue 3 - r; the rest written from 9 down, a lead 0 meaning the answer is "0". O(n) |
| `largest_multiple_of_three_residues.kara` | the digits sorted from largest down and dealt into three lists by residue, each ending at its smallest; the last of list r popped, or two from list 3 - r, and the lists merged back. O(n log n) |
| `largest_multiple_of_three_search.kara` | residue 0 always kept; of the c1 digits of residue 1 and c2 of residue 2, the kept k1 and k2 must agree mod 3, and dropping three of one residue never helps, so each is tried from its count down by at most 2, the smallest dropped, and the longest, then largest, answer kept. O(n) |
| `largest_multiple_of_three_dp.kara` | for each residue of the sum, the best choice of digits so far, kept as how many of each digit; each digit skipped or added, and of two choices the better keeps more digits, or as many with more 9s, then 8s, which is the larger string. O(n) |
| `largest_multiple_of_three_solution.kara` | a Rust solution as LeetCode's Rust users write it (`digits.sort_unstable_by(\|a, b\| b.cmp(a))`, `digits.remove(i)` from the end, `digits.iter().map(\|d\| d.to_string()).collect()`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 3 lines: LeetCode's three examples, all
zeros, nothing to keep of [2, 2], and two digits of residue 2 dropped
when none of residue 1 is there (`"981" "8760" "" "0" "" "9"`); 10^4
digits, the constraints' most (`10^4 digits: 9999 kept, checksum
515115717`); and 2000 random arrays of up to 30 digits folded into a
checksum (`2000 random arrays: 58 with none, checksum 830905099`).
`largest_multiple_of_three.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac
__mir-run`, `karac run` and `karac __mir-llvm-run`.

The Mend loop: the search and dp arms check clean. The ★ arm wrote its
digits as `('0' as u8 + d as u8) as char`; a `char` does not narrow to
a `u8` (E_CHAR_AS_NARROW_INT), and `karac fix` writes the byte literal
`b'0'`, as it drops the harness's `b as i64`, a `u8` widening
implicitly (W0310). The residues arm joined its digits with
`.collect::[Vec[String]]().join("")`; Kāra has no call-site type
arguments, and `karac fix` writes `Vec[String].from_iter(..)`. The Rust
solution takes 11 fixes: `struct Solution;` becomes `struct Solution
{}`, `Vec<i32>` becomes `own Vec[i32]` here and at the wrapper, since
the method rebinds the vector it sorts, `sort_unstable_by` becomes
`sort_by`, `!` and `&&` become `not` and `and`, `String::new()` becomes
`String.new()`, and the closing `collect()` into a `String` becomes
`Vec[String].from_iter(..).join("")` (B-2026-11-21-63). Every arm
matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: every nonempty choice of the digits whose sum is a
multiple of three, each written in its largest order, from the largest
digit down, its leading zeros trimmed, and the largest number of them
kept. That reading takes 2^n choices, so it answers up to 12 digits;
the other properties cover 300 random arrays of up to 200 digits and
one of 10^4 as well.

| | property |
|---|---|
| P1 | the statement read literally, for up to 12 digits |
| P2 | a multiple of three, written with no unnecessary leading zero |
| P3 | made of the given digits, none used more often than given |
| P4 | the digits given in the opposite order, the same answer |
| P5 | three 9s more put 999 in front; a 0 more puts a 0 at the end, where the answer is a number other than 0 |
| P6 | the ★ arm's answer |

All 61,620 checks pass on every arm: `1807 cases: checksum 454398336,
61620 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run` and `karac __mir-llvm-run`. Python, trying every choice of up to
12 digits, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash, and no two
fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the largest digit of residue r dropped | P1 439, P6 2512 |
| M2 | ★: a lead 0 kept | P1 6, P2 6, P5 31, P6 24 |
| M3 | residues: one digit of residue r not enough | P1 367, P2 215, P6 369 |
| M4 | residues: the lists merged unsorted | P1 1060, P5 1366, P6 1348 |
| M5 | search: only counts that are multiples of three | P1 762, P6 952 |
| M6 | search: never two of residue 1 dropped | P1 44, P5 106, P6 44 |
| M7 | dp: fewer digits taken as better | P1 1425, P5 3614, P6 1713 |
| M8 | dp: of two as long, the smaller kept | P1 449, P6 638 |
| M9 | solution: one digit of residue 3 - r dropped, not two | P1 103, P2 103, P6 103 |
| M10 | solution: the digits sorted smallest first | P1 1273, P5 1433, P6 1561 |

P1 and P6 kill all ten, P5 five and P2 three; P3 and P4 kill none. Every
arm counts the digits or sorts them, so none sees the order they come in
(P4), and each answer is built from the given digits with some dropped,
so none uses a digit more often than given (P3); those two stand for an
arm that would. A multiple of three with no lead zero (P2) catches the
edits that leave the residue wrong or a lead 0 in place: a lead 0 kept
(M2), two of the other residue dropped where one of residue r would do,
which leaves the residue wrong when there are not two (M3), and one
dropped where two were needed (M9). Three 9s or a 0 more (P5) catch the
edits that put digits in the wrong place or keep too few: the lead 0
(M2), lists merged unsorted (M4) and digits smallest first (M10) put a 9
or a 0 out of place, and the dp's fewer digits (M7) and the search's
missing pair of 1s (M6) answer the longer input with too little. The
edits that keep a multiple of three, in order, but not the largest (M1,
M5, M8) are caught only by the literal reading and the ★ arm.

## Benchmarks

The bench builds 20 arrays of 10^4 digits, the constraints' most, once;
then makes 10^4 rounds, each setting one digit of one array, both drawn
from the checksum so far, so no answer carries over, and answering with
the ★ arm. Every implementation prints `10000 rounds over 20 arrays of
10^4 digits: checksum 597057599`. The work is counting 10^4 digits and
writing up to 10^4 back out, the same in every language.

BENCHTAB
