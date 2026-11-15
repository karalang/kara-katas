# 2151. Maximum Good People Based on Statements

There are two types of persons:

- The **good person**: The person who always tells the truth.
- The **bad person**: The person who might tell the truth and might lie.

You are given a **0-indexed** 2D integer array `statements` of size
`n x n` that represents the statements made by `n` people about each
other. More specifically, `statements[i][j]` could be one of the
following:

- `0` which represents a statement made by person `i` that person `j`
  is a **bad** person.
- `1` which represents a statement made by person `i` that person `j`
  is a **good** person.
- `2` represents that **no statement** is made by person `i` about
  person `j`.

Additionally, no person ever makes a statement about themselves.
Formally, we have that `statements[i][i] = 2` for all `0 <= i < n`.

Return *the **maximum** number of people who can be **good** based on
the statements made by the* `n` *people*.

```
statements = [[2,1,2],[1,2,2],[2,0,2]]  ->  2
statements = [[2,0],[0,2]]              ->  1
```

**Constraints:** `n == statements.length == statements[i].length`;
`2 <= n <= 15`; `statements[i][j]` is either `0`, `1`, or `2`;
`statements[i][i] == 2`.

A bad person's statements may be anything, so a choice of who is good
holds exactly when every statement a good person makes, `0` or `1`,
matches it. There are at most 15 people, so every choice is tried as the
bits of a mask, and the answer is the most good people of any choice
that holds. O(2^n n^2).

## Approaches

| file | mechanism |
|---|---|
| `statements.kara` ★ | every mask tried by nested loops, a good person's statements checked against the mask's bits; the best `count_ones` kept |
| `statements_search.kara` | a recursive search that settles one person at a time, good or bad, in a `Vec[i64]` behind a `mut ref`; a branch stops as soon as a statement between two settled people fails, or when it cannot beat the best so far with everyone left good |
| `statements_ranked.kara` | the masks ranked most good first by `sort_by_key` on `count_ones` turned round; the first that `holds`, by `find`, a mask holding when `all` its good people's statements are true under a nested `all` |
| `statements_struct.kara` | each row folded once into a `struct Testimony` of two masks, who a person vouches for and who they accuse, so that a choice is `borne_out` (`ref self`) by two `&` tests rather than a walk of the row |
| `statements_iter.kara` | one chain and no loop: the masks `filter`ed by every (speaker, subject) pair, made by `flat_map` over an inner `map`, `filter`ed to a good speaker's false claims, counting to none; then `count_ones` and `max` |
| `statements_solution.kara` | LeetCode's Rust template: a `1u32 << n` range of masks under a labelled loop left by `continue 'outer`, `s as u32`, `count_ones() as i32`; carried by `karac fix` in three rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's two examples and four more
(one person, three who say nothing, two who vouch for each other, and
one who accuses the person who vouches for them), each with its answer;
then the total and a checksum over 2000 random villages of 2 to 7
people, at random and with a hidden truthful set in turn; then the
constraints' largest, 15 people: all saying nothing, with a hidden
truthful set, and at random. `statements.py` mirrors the ★ arm and its
output is byte-identical.

No compiler gap was met in the language. The iterator arm was first
written with Rust's `move` on the inner closure, which Kāra has no use
for; `karac check` names it and `karac fix` deletes it. `karac fix`
carries the template in three rounds of 14, 2 and 1 edits: Rust's
spellings (`<..>` to `[..]`, `&&` to `and`, `|&s|` to a bare pattern,
`struct Solution;` to `struct Solution {}`, the adapter's `&Vec` to `ref
Vec`, `Solution::` to `.`); then `ans` given its type, `i32`, so that it
meets `count_ones() as i32` in `max`, and the adapter's `as i64` dropped,
since an `i32` widens on return; then the `ref` dropped from the
adapter's parameter, which borrows already. The labelled `continue
'outer` and the `u32` masks are Kāra as they stand.

The iterator arm takes 94 s under `karac __mir-run`, against 2.3 s for
the ★ arm's loops, and runs past the corpus's 60 s cap; compiled, the two
take 0.9 s and 0.2 s. A `flat_map` over an inner `map` costs the
interpreter about 2.6 µs an item, some 7 to 10 times the nested loop it stands
for, which is filed as karac B-2026-11-14-62.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every way to call each person good or bad is listed as a
`Vec[bool]`, built digit by digit, and every statement is checked as a
(speaker, subject, claim) triple, a good speaker's claim having to be
true; no mask is formed. It checks 300 random villages of 1 to 5 people,
at random and with a hidden truthful set in turn; then 30 where everyone
says nothing about one person in two; then 30 of 6 people with a hidden
truthful set. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the most good people is the statement read literally |
| P2 | the people numbered from the other end: the same answer |
| P3 | a person added who says nothing and of whom nothing is said: one more |
| P4 | a person added who says nothing and whom everyone accuses: the same, or 1 where it was 0 |
| P5 | everyone but the first person made silent: everyone good, less one if the first person accuses anyone |
| P6 | each arm agrees with at least three of the other five |

P4 holds because the outsider can be good only if everyone who accuses
them is bad, which is everyone else; so the answer is the old one, or
the outsider alone. P5 holds because with one speaker, either the
speaker is good and everyone they accuse is bad, or the speaker is bad
and everyone else is good.

The differential prints `360 villages: checksum 347323275, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading of the same
villages by every mask. On a failure it prints the first ten and then
the count by property.

## Mutation testing

Twenty-nine edits to the differential, four to five to each arm, each
run under `karac __mir-llvm-run` and `karac __mir-run`. Fourteen are
kept: three to the search and iterator arms and two to each other. Each
kept one is killed, fails the same way under both backends and not by a
crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M2 | ★: each claim checked against the speaker | P1 160, P4 106, P6 160 |
| M4 | ★: one good person short | P1 348, P3 12, P4 174, P5 360, P6 348 |
| M7 | search: only good tried | P1 234, P3 246, P4 360, P5 168, P6 234 |
| M9 | search: the bound one person short | P1 165, P2 3, P3 190, P4 174, P5 128, P6 165 |
| M10 | search: the new person's claims read the wrong way | P1 153, P2 160, P6 153 |
| M11 | ranked: the masks unranked | P1 348, P3 360, P4 360, P5 360, P6 348 |
| M13 | ranked: the bad people's claims checked | P1 246, P4 360, P5 168, P6 246 |
| M16 | struct: a vouch taken as an accusation | P1 158, P5 77, P6 158 |
| M17 | struct: one vouched for good enough | P1 49, P6 49 |
| M22 | iter: one false claim let through | P1 143, P4 74, P5 96, P6 143 |
| M23 | iter: a claim checked when its subject is good | P1 141, P4 56, P5 72, P6 141 |
| M24 | iter: only claims about earlier people | P1 118, P2 147, P4 360, P5 168, P6 118 |
| M27 | solution: the adapter turning every claim round | P1 199, P4 321, P5 154, P6 199 |
| M28 | solution: the template never trying everyone good | P1 114, P3 17, P4 48, P5 192, P6 114 |

P1 and P6 kill all fourteen, P4 and P5 eleven each, P3 five and P2
three. P4 adds an outsider everyone accuses, which is a statement by
every person about one more: it sees nearly every edit to how a claim
is read (M2, M13, M22, M23, M24, M27), and every edit that loses good
people (M4, M7, M9, M11, M28). P5 leaves only the first person
speaking, whose answer is everyone or everyone but one: it sees the edits
that lose good people too, and those that misread a claim even when
one speaker makes them all (M13, M16, M22, M23, M24, M27). P3 adds a person no
one speaks of, who is always good: it sees an edit that cannot reach
the choice with everyone good, or near it (M4, M7, M9, M11, M28). P2
numbers the people from the other end, which sees an edit tied to who
comes first: the search's claims read the wrong way and its bound one
short (M9, M10), and the iterator reading only the claims about earlier
people (M24).

Of the twenty-nine, fifteen were not kept. Three are equivalent: the
search not cutting a branch that can only tie the best, the ranked arm
taking a village where nothing holds as one good, though the choice of
no one good always holds, and the struct's loop not stopped at a
failure, which only goes on to find more. Twelve fail as a kept one
does. Five take silence as a claim, by the ★, ranked, iterator and
template arms, and the struct taking it as an accusation, which leave
almost no choice holding, as M11. Three check the bad people's claims
where the good people's should be, or check them all, as M13: the ★
arm, the struct never checking accusations, and the template leaving
its inner loop where it should leave the outer. Two read a claim at the
speaker, the ranked arm's and the template's, as M2. The ★ arm never
trying everyone good, as M28; and the search never checking the claims
about the new person, as M24.

## Verification

Every arm prints the same output as `statements.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.3 s to 2.3 s, but for the
iterator arm's 94 s, and the differential 5.7 s.

## Benchmarks

The bench builds 4 villages of 15 people once, each with a hidden
truthful set; then solves every village 25 times, one statement
redrawn before each so that no solve repeats one before, with the ★ arm
in all five languages. Every implementation prints `100 solves: 323
good in all, checksum 45726079`.

BENCHTAB
