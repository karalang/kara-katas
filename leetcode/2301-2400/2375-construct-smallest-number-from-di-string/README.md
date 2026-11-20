# 2375. Construct Smallest Number From DI String

You are given a **0-indexed** string `pattern` of length `n` consisting
of the characters `'I'` meaning **increasing** and `'D'` meaning
**decreasing**.

A **0-indexed** string `num` of length `n + 1` is created using the
following conditions:

- `num` consists of the digits `'1'` to `'9'`, where each digit is used
  **at most** once.
- If `pattern[i] == 'I'`, then `num[i] < num[i + 1]`.
- If `pattern[i] == 'D'`, then `num[i] > num[i + 1]`.

Return *the lexicographically **smallest** possible string* `num` *that
meets the conditions.*

```
pattern = "IIIDIDDD"  ->  "123549876"
pattern = "DDD"       ->  "4321"
```

**Constraints:** `1 <= pattern.length <= 8`; `pattern` consists of only
the letters `'I'` and `'D'`.

The answer always uses the digits 1 to `n + 1`: written in order they
fit every I, and each run of D's, with the place after it, takes its
digits turned around, which keeps every digit before the run as small
as it can be.

## Approaches

| file | mechanism |
|---|---|
| `di.kara` ★ | a stack: each place's digit pushed in order, and at each I and at the end the stack emptied into the number, so that the digits of a run of D's come out falling. O(n) |
| `di_reverse.kara` | the digits 1 to `n + 1` written in order, and each run of D's turned around in place over its digits and the one after it. O(n) |
| `di_place.kara` | place by place: place `i` lies in a block of places joined by D's, from `s` to `j`, and holds `j + 1 - (i - s)`, found by looking left and right from it. O(n^2) |
| `di_search.kara` | backtracking: each place tries the unused digits from 1 up, keeping one only when it rises or falls from the last as the pattern says; the first number completed is the smallest |
| `di_iter.kara` | iterators: the pattern split at each I into runs of D's, and a run of `k` D's folded in as the next `k + 1` digits, falling |
| `di_solution.kara` | LeetCode's Rust template: the pattern's `chars` with one more I chained on by `std::iter::once`, each digit pushed as a `char`, and the stack emptied into the `String` at every I; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 4 lines: LeetCode's two examples; `I` and `D`;
then every pattern of 1 to 8 letters, 510 in all, with a checksum of the
numbers and how many begin with 1. `di.py` mirrors the ★ arm and its
output is byte-identical, and the mirror was checked on every pattern of
up to 7 letters against the first permutation of the digits 1 to 9, in
order, that fits it.

The harness first read each number back with `number.parse()`, its type
named only by the `i64` it was bound to; `check` reports it, and `karac
fix` writes it `i64.parse(number)`.

`check` first reports 6 errors on the template, and `karac fix` carries
it in one call, reporting 7 edits: `struct Solution;` given its braces;
`String::new`, `Vec::new` and `Solution::` written with a dot; `Vec<char>`
given its brackets; and `std::iter::once` written `once`, which needs no
path. The `(b'1' + i as u8) as char` digit and the `while let Some(d) =
stack.pop()` loop stand as Kāra.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every number of `n + 1` different digits from 1 to 9, tried
from the smallest up, and the first whose digits rise at each I and fall
at each D. No stack, no runs, and no use of the digits 1 to `n + 1`. It
checks every pattern of 1 to 5 letters, 62 in all, which the literal
reading answers; then 298 random patterns of 6 to 8 letters. All 360 are
drawn before any arm answers.

| | property |
|---|---|
| P1 | up to 5 letters, the answer is the literal reading's |
| P2 | `n + 1` different digits that rise at each I and fall at each D |
| P3 | an I appended, up to 7 letters: the answer followed by `n + 2` |
| P4 | an I put in front, up to 7 letters: 1, then the answer with every digit one higher |
| P5 | the digits are exactly 1 to `n + 1` |
| P6 | each arm agrees with at least three of the other five |

P3 holds because the answer already uses 1 to `n + 1`, and the new last
digit must rise above the old last: `n + 2` keeps every digit before it
as it was. P4 holds because a number beginning with 1 is smaller than
any other, and an I after the 1 lets the rest be the old answer's digits,
each one higher. Past 7 letters P3 and P4 would ask for a tenth digit.

The differential prints `360 cases: checksum 842356494, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the answers was checked against a Python reading that builds the
same cases and tries the permutations of the digits in order. On a
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
| M1 | ★: the stack never emptied at an I | P1 57, P2 350, P3 267, P4 267, P6 350 |
| M2 | ★: the stack emptied whenever it holds four | P1 4, P2 63, P6 63 |
| M5 | ★: the first letter taken as an I | P1 31, P2 178, P4 133, P6 178 |
| M8 | reverse: a run never past its first D | P1 31, P2 242, P6 242 |
| M9 | reverse: the digits counted down | P1 62, P2 360, P3 267, P4 267, P6 360 |
| M11 | reverse: the digits from two | P1 62, P2 93, P3 267, P4 267, P5 360, P6 360 |
| M13 | place: the run before stopping one letter short | P1 31, P2 178, P4 133, P5 178, P6 178 |
| M14 | place: the run after stopping one letter early | P1 31, P2 178, P3 131, P5 178, P6 178 |
| M16 | place: the run after taken to the end | P1 57, P2 350, P3 267, P4 267, P5 350, P6 350 |
| M19 | search: a used digit never freed | P1 57, P2 353, P3 260, P4 260, P5 353, P6 353 |
| M20 | search: the digits tried from 9 down | P1 62, P3 267, P4 267, P5 267, P6 357 |
| M21 | search: each step read against the next letter | P1 52, P2 343, P3 133, P4 133, P6 343 |
| M22 | iter: each run counted up | P1 57, P2 353, P6 353 |
| M23 | iter: each run one digit short | P1 62, P2 360, P3 267, P4 267, P5 360, P6 360 |
| M26 | iter: each run all its first digit | P1 57, P2 353, P5 353, P6 353 |
| M27 | solution: the closing I left off | P1 62, P2 360, P3 267, P5 360, P6 360 |
| M30 | solution: the stack emptied before the digit is pushed | P1 62, P2 360, P3 267, P4 133, P5 360, P6 360 |

P1 and P6 kill all seventeen, P2 sixteen, P3 and P4 eleven and P5 ten.
P2 passes only the digits tried from 9 down (M20), whose number fits
the pattern and is the largest that does, not the smallest. P5 fails
the edits that write a digit outside 1 to `n + 1` or leave one out, and
passes those that only put the right digits in the wrong order. P3 and
P4 pass the edits that go wrong only inside a long run of D's, as the
stack emptied whenever it holds four (M2), which differs from the
answer only where a run of three or more D's stands.

The first thirty-one edits fell into sixteen classes, one short of
seventeen, so two of the ★ arm's were replaced: a D read as an I, which
failed as the reverse arm's digits counted down (M9), and the digits
counted from zero, which failed as the iter arm's runs one digit short
(M23). Their places hold the stack emptied whenever it holds four (M2)
and the stack emptied one place early at the end (M3).

Of the thirty-one, fourteen were not kept. One digit popped at each I
in the ★ arm (M4), the place arm's run before never counted and added
(M12, M15) fail as the iter arm's runs all their first digit (M26); the
last place never pushed in the ★ arm (M6) as the template's closing I
left off (M27); each run reversed one short and the reverse starting
one later in the reverse arm (M7, M10) and the template's stack emptied
from the bottom (M31) as the iter arm's runs counted up (M22); the digit
0 tried too in the search (M17), each run one longer (M25) and the
template's D read as an I (M28) as the iter arm's runs one digit short
(M23); the iter arm's split at each D (M24) as the reverse arm's digits
counted down (M9); and the template's digits from two (M29) as the
reverse arm's (M11). The ★ arm's stack emptied one place early at the
end (M3) fails apart from every kept one and was left out to keep three
to an arm. The search arm's rising step allowed to fall (M18) survives:
the search takes the digits from 1 up, and a Python copy of it gives the
same answer as the arm on all 510 patterns of 1 to 8 letters, so the
check it removes never decides.

## Verification

Every arm prints the same output as `di.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.2 to 0.3 s, and the differential
2.0 s there and 0.57 s under `karac __mir-llvm-run`.

## Benchmarks

The bench lists the 510 patterns of 1 to 8 letters once, then makes
2000 passes, pass `p` folding each digit of each answer plus `p` into
the checksum, with the ★ arm in all five languages. Every
implementation prints `2000 passes over 510 patterns: checksum
489453336`. Every implementation builds each number afresh in each
call.

BENCHTAB
