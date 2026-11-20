# 2380. Time Needed to Rearrange a Binary String

You are given a binary string `s`. In one second, **all** occurrences of
`"01"` are **simultaneously** replaced with `"10"`. This process
**repeats** until no occurrences of `"01"` exist.

Return *the number of seconds needed to complete this process.*

```
s = "0110101"  ->  4
s = "11100"    ->  0
```

**Constraints:** `1 <= s.length <= 1000`; `s[i]` is either `'0'` or
`'1'`.

**Follow up:** Can you solve this problem in O(n) time complexity?

Each second moves a 1 one place left past a 0, so the process ends with
every 1 before every 0. A 1 with `z` 0s before it needs at least `z`
seconds, and since it never overtakes the 1 before it, at least one
second more than that 1 once both are moving; it takes the larger of
the two.

## Approaches

| file | mechanism |
|---|---|
| `seconds.kara` ★ | one pass: each 1 after some 0 takes the larger of one more second than the 1 before it and the 0s before it; the last one's seconds are the answer. O(n) |
| `seconds_simulate.kara` | the process simulated: each second one pass swaps every 01 into 10, stepping past each swap, until a pass swaps nothing. O(n^2) |
| `seconds_formula.kara` | the recurrence unrolled: the largest, over the 1s with a 0 before them, of the 0s before that 1 plus the 1s after it, from a table of the 1s after each place. O(n) |
| `seconds_zeros.kara` | the 0s from the right, the mirror of the ★ arm: each 0 with some 1 after it takes the larger of one more second than the 0 after it and the 1s after it. O(n) |
| `seconds_iter.kara` | iterators: the digits folded into the 0s so far and the seconds so far |
| `seconds_solution.kara` | LeetCode's Rust template: the `chars` walked once, the seconds raised by `std::cmp::max`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 4 lines: LeetCode's two examples; one 0; 500
0s then 500 1s, `01` 500 times, and 500 1s then 500 0s; then 2000
random strings of 1 to 60 digits, 1 with a chance of 0 to 10 in 10,
with a checksum and how many take no time. `seconds.py` mirrors the ★
arm and its output is byte-identical, and the mirror was checked on 5000
random strings of up to 40 digits against Python's `replace` run until
no `01` is left.

`check` first reports 3 errors on the template, and `karac fix` carries
it in one call, reporting 6 edits: `struct Solution;` given its braces;
`std::cmp::max` written `max`, which needs no path; `Solution::`
written with a dot and the wrapper's `as i64` dropped, since an `i32`
widens; and the counts `zeros` and `res`, which start from a bare
literal, given their `i32`, which the `i32` returned asks for. The
`chars()` walk and the `'0'` comparison stand as Kāra.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every `01` replaced by `10` at once, by the string's own
`replace`, and the seconds counted until `contains` finds no `01`. No
counting of 0s or 1s. It checks 300 random strings of 1 to 60 digits;
then 30 of up to 1000; then 30 of up to 1000 whose 1s grow likelier
from left to right. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | 0 exactly when no 0 stands before a 1, and below `n` |
| P3 | the string reversed and every digit flipped: the same answer |
| P4 | a 1 put in front and a 0 appended: the same answer |
| P5 | the string after one second: the answer less one, while it is above 0 |
| P6 | each arm agrees with at least three of the other five |

Two `01`s never overlap, so one `replace` of all of them is one second.
P3 holds because each second, read from the other end with the digits
flipped, is the same second; P4 because a 1 in front and a 0 at the end
are already where they end up, and nothing passes them; P5 because the
process is the same from its second second on.

The literal reading first took the string it was given as its own,
`let mut x = s;` over a borrowed parameter; `check` reports it, and
`karac fix` takes the parameter as `own String` and passes the caller's
`s.clone()`.

The differential prints `360 cases: checksum 365231130, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and runs `replace` until no `01` is left. On a failure it
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
| M2 | ★: no second more than the 1 before | P1 205, P3 254, P5 167, P6 205 |
| M4 | ★: only one more than the 1 before | P1 184, P3 254, P5 152, P6 184 |
| M6 | ★: a 1 clearing the 0s before it | P1 262, P3 244, P5 241, P6 262 |
| M8 | simulate: one second counted too many | P1 360, P2 94, P5 88, P6 360 |
| M10 | simulate: the last pair never looked at | P1 165, P2 6, P3 176, P4 165, P5 38, P6 165 |
| M11 | simulate: each pass from the second digit | P1 149, P2 5, P3 176, P4 149, P5 33, P6 149 |
| M12 | formula: the 1s after counting the 1 itself | P1 272, P2 6, P5 2, P6 272 |
| M13 | formula: a 1 with no 0 before it a candidate | P1 110, P2 44, P3 184, P4 134, P5 130, P6 110 |
| M14 | formula: the 0s after counted, not the 1s | P1 235, P3 259, P4 272, P5 271, P6 235 |
| M17 | zeros: a 0 with no 1 after it counted too | P1 100, P2 46, P3 225, P4 179, P5 137, P6 100 |
| M19 | zeros: two seconds more than the 0 after | P1 222, P2 128, P3 259, P5 109, P6 222 |
| M20 | zeros: each 1 counted twice | P1 272, P2 162, P3 260, P5 98, P6 272 |
| M22 | iter: the 0s never counted | P1 272, P2 272, P6 272 |
| M24 | iter: the smaller taken | P1 270, P5 234, P6 270 |
| M26 | iter: the 0s returned | P1 281, P2 46, P3 345, P4 360, P5 318, P6 281 |
| M29 | solution: a 1 with no 0 before it counted too | P1 134, P2 48, P3 225, P4 203, P5 163, P6 134 |
| M30 | solution: the 1s and 0s swapped | P1 245, P2 12, P4 360, P5 272, P6 245 |

P1 and P6 kill all seventeen, P5 sixteen, P2 and P3 twelve and P4
eight. P5, the string one second on, passes only the iter arm's 0s
never counted (M22), which answers 0 everywhere and so one less only
where the answer is already 0. P4, a 1 in front and a 0 appended, fails
the edits that misread a digit at either end, as the last pair never
looked at (M10), each pass from the second digit (M11), a 1 with no 0
before it a candidate (M13, M29) and a 0 with no 1 after it counted
(M17), and those that confuse the 0s with the 1s (M14, M26, M30). P3,
the string reversed and flipped, passes the edits that are as wrong
read from either end: one second too many (M8), the 1s after counting
the 1 itself (M12), the 0s never counted (M22), the smaller taken (M24)
and the 1s and 0s swapped (M30).

Of the thirty-one, fourteen were not kept. The ★ arm's only the 0s
before it (M3), the simulate arm's pass not stepping past its swap (M7)
and the template's no second more than the 1 before (M27) fail as the ★
arm's (M2); a 1 with no 0 before it counted in the ★ and iter arms (M1,
M25) as in the template (M29); the iter arm's 1 clearing the 0s before
it (M23) as the ★ arm's (M6); the template's one second too many (M31)
as the simulate arm's (M8); the zeros arm's last digit skipped (M21) as
the simulate arm's last pair never looked at (M10); its 0s walked from
the left (M18) as the template's 1s and 0s swapped (M30); and the
simulate arm's swap not marked (M9) as the iter arm's 0s never counted
(M22). The 0s counted from one in the ★ arm and the template (M5, M28)
fail alike, and the formula arm's only the first candidate and 1s after
summed from the left (M15, M16) each fail apart from every kept one; all
four were left out to keep three to an arm and two to the template. The
simulate arm's M9 was first one swap a second, which at `O(n^3)` ran
past the time limit under `karac __mir-run`; it was replaced.

## Verification

Every arm prints the same output as `seconds.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.27 to 2.0 s, the simulate arm
the slowest as it runs every second, and the differential 20.9 s there
and 0.52 s under `karac __mir-llvm-run`.

## Benchmarks

The bench builds 100 strings of 1000 digits once from the harness's
generator, string `s` 1 with a chance of `1 + s % 10` in 12, then makes
500 passes, pass `p` asking for string `(s + 7 p) % 100` in turn and
folding each answer plus `p` into the checksum, with the ★ arm in all
five languages. Every implementation prints `500 passes over 100
strings of 1000 digits: checksum 341787790`.

BENCHTAB
