# 2486. Append Characters to String to Make Subsequence

You are given two strings `s` and `t` consisting of only lowercase
English letters.

Return *the minimum number of characters that need to be appended to
the end of* `s` *so that* `t` *becomes a **subsequence** of* `s`.

A **subsequence** is a string that can be derived from another string
by deleting some or no characters without changing the order of the
remaining characters.

```
s = "coaching", t = "coding"  ->  4
s = "abcde", t = "a"          ->  0
s = "z", t = "abcde"          ->  5
```

**Constraints:** `1 <= s.length, t.length <= 10^5`; `s` and `t`
consist only of lowercase English letters.

Whatever is appended, `t` must find some start of itself inside `s`
and the rest in the appended letters, so the answer is `t`'s length
less the longest start of `t` that `s` holds in order. Matching each
letter of `t` at the first place it can is never worse, so one walk of
`s` finds that start.

## Approaches

| file | mechanism |
|---|---|
| `append.kara` ★ | by two pointers: one walk of `s`, each letter that matches the next letter of `t` wanted moving `t`'s pointer on. O(m + n) |
| `append_places.kara` | by letter positions: each letter's places in `s` listed in order, and `t` walked with a cursor into `s`, each letter taken at its first place at or past the cursor, found by `partition_point`. O(n + m log n) |
| `append_jump.kara` | by a jump table: for every place in `s` and every letter, the first place at or past it holding that letter, filled from the end, and `t` walked by jumping. O(26 n + m) time and room |
| `append_driven.kara` | driven by `t`: for each letter of `t`, `s` read on as bytes from where the last match left it until the letter turns up, running off the end leaving the rest. O(m + n) |
| `append_iter.kara` | iterators: `fold` over the letters of `s`, the state the count of `t`'s letters matched, the next one read by `get` so that a finished `t` matches nothing. O(m + n) |
| `append_solution.kara` | LeetCode's Rust template: two `String`s in, `i32` out; both read by `as_bytes()`, the pointer into `t` moved by a `for &c in s` walk; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 14 lines: LeetCode's three examples; then
five more, one letter each, the same and not, `t` longer than `s` but
begun by it, `t` the reverse of `s`, and a letter of `t` that `s` holds
only before the place it is needed; then the constraints' largest,
`10^5` letters each, `t` all of `s`, `t` the reverse of `s`, one letter
repeated against another, and random words from 2 and from 26 letters;
and 3000 random pairs of 1 to 30 letters from the first 1 to 4, as a
checksum. `append.py` mirrors the ★ arm and its output is
byte-identical, and the mirror was checked on 5000 random pairs of 1 to
10 letters against the longest start of `t` that is a subsequence of
`s`, each start tested on its own. The two agreed on every pair.

`check` first reports 2 errors on the template, the `&` in `for &c`
and the `&&`, and `karac fix` carries it in one call, reporting 6
edits: that `&` goes and `&&` becomes `and`; both `as_bytes()` become
`bytes()`; `struct Solution {}` is added; and the wrapper's `as i64` on
the `i32` answer goes, since an `i32` widens by itself. The tuple
`let (s, t)` rebinding both names, the byte comparison and `(t.len() -
j) as i32` stand as Kāra.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: for `k` from 0 up, the last `k` letters of `t` appended to
`s`, and the least `k` for which `t` is then a subsequence, that tested
by a table of the longest common subsequence of the two words. No
pointer walks `t`. It checks 300 random pairs of 1 to 8 letters each,
then 60 of up to 20, both words drawn from the first 1 to 4 letters.
All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the count is the literal reading's |
| P2 | `t` appended to `s`: none |
| P3 | `t` cut to its first `m - k` letters, those `s` already holds: none |
| P4 | a letter put after `t` when `k` is more than 0: one more |
| P5 | a `z`, a letter neither word has, put in the middle of `s`: the same count |
| P6 | each arm agrees with at least three of the other five |

The literal reading appends `t`'s own last letters, which is enough:
whatever letters make `t` a subsequence, the last `k` of `t` do too.
P2 holds because `t` is then in `s` whole. P3 holds because the letters
an arm says need not be appended are those `s` holds. P4 holds because
with `k` above 0 the walk stops inside `t`, so a letter after its end
is never reached and must be appended too. P5 holds because a letter
`t` lacks matches nothing.

The differential prints `360 cases: checksum 478274811, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and tests each appended suffix with an iterator. On a
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
| M1 | ★: the last letter of t never matched | P1 113, P2 360, P3 269, P4 113, P6 113 |
| M2 | ★: one fewer appended | P1 360, P2 360, P3 113, P4 72, P6 360 |
| M5 | ★: the first letter of s skipped | P1 114, P5 24, P6 114 |
| M7 | places: the cursor's own place skipped | P1 181, P2 231, P5 35, P6 181 |
| M8 | places: a place used twice | P1 102, P6 102 |
| M11 | places: a letter skipped after each match | P1 123, P2 207, P5 40, P6 123 |
| M12 | jump: each place one late | P1 187, P2 258, P5 29, P6 187 |
| M13 | jump: each row only its own letter | P1 159, P2 256, P5 87, P6 159 |
| M15 | jump: a missing letter skipped over | P1 101, P3 101, P4 29, P6 101 |
| M17 | driven: stopping at the first letter that differs | P1 281, P2 161, P5 202, P6 281 |
| M19 | driven: running off the end not stopping | P1 247, P6 247 |
| M20 | driven: the rest of s counted | P1 323, P2 360, P3 254, P4 293, P5 360, P6 323 |
| M22 | iter: a mismatch starting t over | P1 188, P2 160, P3 13, P4 34, P5 84, P6 188 |
| M23 | iter: each letter matched against the one after | P1 265, P2 360, P3 272, P4 104, P6 265 |
| M24 | iter: s walked backwards | P1 85, P2 137, P6 85 |
| M27 | solution: a later letter matching | P1 116, P5 181, P6 116 |
| M28 | solution: two letters of t for each match | P1 230, P2 184, P3 88, P6 230 |

P1 and P6 kill all seventeen, P2 twelve, P5 nine, P3 seven, and P4 six.

Fourteen are not kept. Ten fail exactly as a kept one. The ★ arm's
letter that differs moving on (M3) fails as the driven arm's stopping
at the first letter that differs (M17); the ★ arm's letter of `s`
matching two of `t`, the jump arm's place used twice and the driven
arm's matched letter used again (M4, M14, M18) as the places arm's
place used twice (M8); the ★ arm's and the template's rest of `s`
counted (M6, M29) as the driven arm's (M20); the places arm's one fewer
appended and the template's `t` walked against itself (M9, M31) as the
driven arm's running off the end (M19); and the places arm's first place
passed over and the driven arm's first letter of `s` skipped (M10, M21)
as the ★ arm's (M5). The iter arm's and the template's first letter of
`t` taken as matched (M26, M30) fail as each other, P1 and P6 on 157
cases. The jump arm's first letter of `s` never in the table (M16) and
the iter arm's one more appended (M25) fail in ways of their own, but
their arms already hold three kept edits.

One edit was replaced before this table was drawn: the places arm's
places counted from 1, which survived every check. It moves every
place of every letter one later, and the cursor, set one past the place
it matched, moves with them, while the first search, from 0, finds the
same first place either way, so every answer is the same. It was
replaced by the first place passed over (M10).

## Verification

Every arm prints the same output as `append.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 1.8 to 6.8 s, but for the places arm's 125 s (it clones each letter's list of places at every lookup), and the differential 0.7 s; under `karac __mir-llvm-asan` the arms take 0.8 to 2.0 s, the places arm 29 s, and the differential 0.9 s; and under `karac run` the differential takes 0.6 s.

## Benchmarks

The bench builds 20 pairs of random words of `10^4` letters from `a`
to `d` once from its own generator, then makes 600 passes; each changes
one letter of every `s`, place and letter chosen by the checksum so
far, so no answer repeats the last, and folds the count plus the pass
into the checksum. The bench uses the ★ arm in all five languages,
each `s` kept as a list of letters and joined into a fresh string for
every answer; C copies it into one buffer. Every implementation prints
`600 passes over 20 pairs of 10^4 letters: checksum 416679606`.

BENCHTAB
