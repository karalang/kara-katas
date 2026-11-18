# 2243. Calculate Digit Sum of a String

You are given a string `s` consisting of digits and an integer `k`.

A **round** can be completed if the length of `s` is greater than `k`.
In one round, do the following:

1. **Divide** `s` into **consecutive groups** of size `k` such that the
   first `k` characters are in the first group, the next `k` characters
   are in the second group, and so on. **Note** that the size of the
   last group can be smaller than `k`.
2. **Replace** each group of `s` with a string representing the sum of
   all its digits. For example, `"346"` is replaced with `"13"` because
   `3 + 4 + 6 = 13`.
3. **Merge** consecutive groups together to form a new string. If the
   length of the string is greater than `k`, repeat from step `1`.

Return `s` *after all rounds have been completed*.

```
s = "11111222223", k = 3  ->  "135"
s = "00000000", k = 3     ->  "000"
```

**Constraints:** `1 <= s.length <= 100`; `2 <= k <= 100`; `s` consists
of digits only.

A group of `k >= 2` digits sums to at most `9k`, which never has more
digits than the group, so a round never lengthens the string; every arm
repeats rounds until it is no longer than `k`, as the statement does.
Each round is O(n).

## Approaches

| file | mechanism |
|---|---|
| `digits.kara` ★ | while the string is longer than `k`, it is rebuilt group by group: each group cut with `substring(start, (start + k).min(len))`, its digits summed by `(ch as i64) - ('0' as i64)`, the sum written back with `f"{sum}"` |
| `digits_groups.kara` | a `struct Groups` over one round's characters with an `impl Iterator` whose `next` (`mut ref self`) yields each group's digit sum, `None` past the end; a round is a `for` over `Groups.over(s, k)` |
| `digits_iter.kara` | iterator chains: a round is the characters `collect`ed and cut by `chunks(k)`, each chunk `map`ped to its digit sum (an inner `map` and `sum` bound to a typed `let`) and `to_string`, the pieces `collect`ed into a `Vec[String]` and `join`ed |
| `digits_list.kara` | no string until the end: the digits a `Vec[i64]`, each round summing every `k` of them and writing each sum's digits back, most significant first, through a small stack of `sum % 10` that is then popped |
| `digits_recursive.kara` | recursion: a string no longer than `k` is the answer, otherwise the answer is that of `one_round`, which sums each group with `to_digit(10)` and joins the sums' `to_string`s |
| `digits_solution.kara` | LeetCode's Rust template: `String` and `i32` in, `String` out, a `while s.len() > k as usize` loop over `s.as_bytes().chunks(k as usize)`, each chunk's bytes summed as `(b - b'0') as u32` and written with `to_string()` by `push_str`; carried by `karac fix` in one round |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 7 lines: LeetCode's two examples and four more
(no round needed; one digit a group; nines whose group sums carry back
to the same length; the constraints' longest string, 100 nines), each
with its answer; then the total length of the answers to 3000 random
strings of 1 to 100 digits, half with `k` from 2 to 100 and half from 2
to 5, with a checksum. `digits.py` mirrors the ★ arm and its output is
byte-identical.

`karac fix` carries the template in one round of 11 edits: `own` on the
parameter `s`, which `let mut s = s;` takes over, `k as usize` dropped
from the comparison and from `chunks` (the `i32` is widened), `as_bytes()`
to `bytes()`, `String::new()` to `String.new()`, the `&` dropped from the
closure pattern and from `push_str`'s argument, `struct Solution;` to
`struct Solution {}`, and `Solution::` to `Solution.`. Before kara
B-2026-11-17-146 the reassignment `s = next;` was fixed to `s = ref
next;`, a borrow of the loop's own `next`, which the next round cloned.
While the iter arm was written, its first draft's turbofish
(`sum::[i64]()` inside the `map` closure) was reported twice at one
place; that did not happen again (kara B-2026-11-17-148), and the arm
binds the sum to a typed `let`.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: each round the string is walked one character at a time into
a group, the group closed when it holds `k` characters or the string
ends, and each closed group replaced by its digit sum, counted up one
unit at a time and written out; no slicing and no division. It checks
300 random strings of 1 to 40 digits with `k` from 2 to 12; then 30 of
nines only, whose sums carry; then 30 of length `k + 1`, one round and a
group of one. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the rounds read literally |
| P2 | only digits, and no longer than `k`, or the string itself when it is no longer than `k` |
| P3 | the digit sum keeps its remainder by 9 |
| P4 | one round done first, by the literal reading: the same answer, when the string is longer than `k` |
| P5 | the last group padded with zeros to `k`: the same answer, when the string is longer than `k` |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 cases: checksum 186809994, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that cuts
each round with range steps and sums the digits through `int()`. On a
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
| M1 | ★: the last short group dropped | P1 285, P3 243, P4 197, P5 197, P6 285 |
| M2 | ★: a string of exactly `k` cut again | P1 78, P2 9, P6 78 |
| M3 | ★: each group's first digit only | P1 301, P3 242, P4 302, P6 301 |
| M8 | list: a sum's digits written backwards | P1 276, P4 225, P6 276 |
| M10 | list: the answer written backwards | P1 338, P2 50, P6 338 |
| M11 | list: the rounds stopping at `k + 1` | P1 80, P2 80, P4 34, P5 34, P6 80 |
| M13 | recursive: a character skipped between groups | P1 299, P3 249, P4 297, P5 86, P6 299 |
| M14 | recursive: one round only | P1 131, P2 131, P4 131, P6 131 |
| M15 | recursive: each group's first digit skipped | P1 302, P3 254, P4 294, P6 302 |
| M17 | groups: a last group of one dropped | P1 130, P3 107, P4 62, P5 62, P6 130 |
| M18 | groups: every other character read | P1 301, P3 256, P4 302, P5 41, P6 301 |
| M21 | groups: the first character skipped | P1 302, P3 251, P4 291, P5 53, P6 302 |
| M23 | iter: the first group's sum only | P1 302, P3 247, P4 296, P6 302 |
| M24 | iter: each digit taken by 5 | P1 298, P3 262, P4 299, P6 298 |
| M26 | iter: each sum's tens only | P1 302, P3 264, P4 274, P6 302 |
| M29 | solution: chunks of `k + 1` | P1 295, P4 290, P5 84, P6 295 |
| M30 | solution: `k` handed in one larger | P1 298, P2 67, P4 297, P5 84, P6 298 |

P1 and P6 kill all seventeen, P4 fifteen, P3 ten, P5 eight, and P2
five. P3 sees every edit that loses or changes a digit, since a digit
sum keeps the remainder by 9; it misses the ones that only cut the
groups elsewhere or write digits in another order (M8, M10, M29). P2 fails
the edits that stop too early or too late (M2, M11, M14, M30) and the
answer written backwards (M10), which is no longer the string itself
when that string was short enough from the start. P5 fails the edits that read
the last group by its length.

Of the thirty-one, fourteen were not kept, and none survives, crashes
or differs between the backends. Seven fail as a kept one does: the ★
arm's first character never read (M4) as the groups arm's skipped
(M21); the recursive arm's string of exactly `k` cut again (M12) as the
★ arm's (M2); groups of `k + 1` in the list, groups and iter arms (M9,
M20, M22) as the template's chunks (M29); and the rounds stopping at
`k + 1` in the iter arm and the template (M25, M27) as the list arm's
(M11). Six fail alike in two groups: each sum's last digit only in the
★, list, groups and template arms (M5, M7, M19, M31), and each digit
halved in the recursive arm and the template (M16, M28). The ★ arm's
string handed back unchanged (M6) fails in a way of its own and is left
out because its arm keeps three.

## Verification

Every arm prints the same output as `digits.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the ★ arm takes 0.6 s, the groups and recursive
arms 0.6 to 0.7 s, the list arm 0.8 s, the template 0.9 s, the iter arm
1.1 s, and the differential 1.0 s.

## Benchmarks

The bench builds 1000 strings of 100 digits once, then makes 200 passes
over all of them with `k` from 2 to 5, one string drawn again before
each pass, with the ★ arm in all five languages. Every implementation
prints `200 passes over 1000 strings: checksum 339899322`.

BENCHTAB
