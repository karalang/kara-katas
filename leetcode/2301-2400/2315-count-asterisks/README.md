# 2315. Count Asterisks

You are given a string `s`, where every **two** consecutive vertical
bars `'|'` are grouped into a **pair**. In other words, the 1st and 2nd
`'|'` make a pair, the 3rd and 4th `'|'` make a pair, and so forth.

Return *the number of* `'*'` *in* `s`*, **excluding** the* `'*'`
*between each pair of* `'|'`.

**Note** that each `'|'` will belong to **exactly** one pair.

```
s = "l|*e*et|c**o|*de|"           ->  2
s = "iamprogrammer"               ->  0
s = "yo|uar|e**|b|e***au|tifu|l"  ->  5
```

**Constraints:** `1 <= s.length <= 1000`; `s` consists of lowercase
English letters, vertical bars `'|'`, and asterisks `'*'`; `s` contains
an **even** number of vertical bars `'|'`.

A star lies between a pair exactly when an odd number of bars come
before it: the bars before it close every pair they open but the last.
So one walk that flips a flag at each bar counts the stars seen with
the flag down. O(n).

## Approaches

| file | mechanism |
|---|---|
| `count.kara` ★ | one walk over `s.chars()`, a `bool` flipped with `not` at each bar, and a star counted while it is down |
| `count_naive.kara` | each star on its own, the bars before it counted from the start, and the star counted when they are even. O(n^2) |
| `count_split.kara` | `s.split("\|")` `enumerate`d: the pieces at even places lie outside every pair, and their stars are counted with `matches("*")` |
| `count_pairs.kara` | all the stars less those inside: each pair's two bars found with `find` on the slice from where the last pair ended, and the stars between them taken off |
| `count_iter.kara` | `s.chars().fold` of `(bars, count)` through a `match` with a guard, a star counting while the bars are even |
| `count_solution.kara` | LeetCode's Rust template: a `bool` flipped with `!`, a `match` on each character with a guard, an `i32` count; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's three examples; a star
inside the only pair, stars and no bars, two empty pairs around stars,
and stars on both sides of two pairs; 999 characters, a third of them
bars, and a bar more when they come out odd; then 2000 random strings
of 1 to 40 characters, bars one time in 2 to 8 and stars one time in 1
to 4 of the rest, with a checksum and the stars in all. `count.py`
mirrors the ★ arm and its output is byte-identical.

`karac fix` carries the template in one call, reporting 5 edits:
`struct Solution;` to `struct Solution {}`; the two `!inside` to `not
inside`; and, in the harness's wrapper, `Solution::count_asterisks` to
`Solution.count_asterisks` and the `as i64` on the `i32` answer
dropped, as it widens on its own.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the places of the bars are listed and taken two at a time,
the first and second, the third and fourth, and a star is counted
unless some pair has it strictly between its two bars. No flag and no
parity. It checks 300 random strings of 1 to 40 characters; then 30
with no bars; then 30 of up to 998 characters, a bar one time in 2. All
360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | the answer is at most the number of stars |
| P3 | the string reversed: the same answer |
| P4 | a star put at each end: two more |
| P5 | the string between two more bars: the stars it holds less the answer |
| P6 | each arm agrees with at least three of the other five |

P3 holds because the bars are even, so reversing keeps each pair
together, and P5 because the two new bars pair with the first and last
of the old ones, turning every star between pairs to one outside and
back.

The differential prints `360 cases: checksum 490687092, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that
builds the same cases, splits each on its bars and counts the stars of
every other piece. On a failure it prints the first ten and then the
count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the flag never flipped back | P1 203, P3 175, P4 300, P5 272, P6 203 |
| M4 | ★: an opening bar counted as a star | P1 300, P2 155, P5 360, P6 300 |
| M5 | ★: each star counted twice | P1 313, P2 213, P4 360, P5 343, P6 313 |
| M7 | naive: the first character never a bar | P1 73, P3 146, P4 73, P5 247, P6 73 |
| M9 | naive: a star counted only before the second bar | P1 251, P3 216, P4 300, P5 317, P6 251 |
| M10 | naive: stars counted as bars | P1 286, P3 71, P4 360, P6 286 |
| M14 | split: split on two bars together | P1 245, P3 108, P4 120, P5 279, P6 245 |
| M15 | split: the first piece left out | P1 221, P3 175, P4 360, P5 221, P6 221 |
| M16 | split: stars counted in twos | P1 313, P4 343, P5 343, P6 313 |
| M19 | pairs: only the first pair taken off | P1 169, P3 129, P5 227, P6 169 |
| M20 | pairs: the stars inside counted to the end | P1 227, P2 168, P3 258, P4 300, P5 272, P6 227 |
| M21 | pairs: every character but a bar counted | P1 282, P2 270, P5 282, P6 282 |
| M22 | iter: a star counted while the bars are odd | P1 320, P4 360, P6 320 |
| M24 | iter: a bar counted as a star | P1 300, P2 217, P5 360, P6 300 |
| M25 | iter: each letter counted as a star | P1 339, P2 282, P5 357, P6 339 |
| M29 | solution: the count begun at 1 | P1 360, P2 119, P5 360, P6 360 |
| M31 | solution: the first character skipped | P1 219, P3 187, P4 204, P5 239, P6 219 |

P1 and P6 kill all seventeen, P5 fifteen, P4 eleven, P3 nine and P2
seven. P5, the string between two more bars, turns every star inside a
pair out and every one outside in, so nearly any miscount shows twice
in it; it misses the iter arm's stars counted while the bars are odd,
whose count of the inside stars is just what P5 asks of it, and the
naive arm's stars counted as bars, whose shifts the two new bars
undo. P4, a star
at each end, fails where the ends are read wrongly or a star is not
worth one: the first character skipped or never a bar, the first piece
left out, the stars counted twice or in twos, the inside counted. P3,
the string reversed, fails where the walk leans on its direction: a
flag never flipped back, the bars before a star miscounted, only the
first pair taken off. P2 fails for more stars than the string holds.

Of the thirty-one, fourteen were not kept. The stars inside counted in
place of those outside, in the ★ arm by its flag (M2) and its walk
begun inside (M6), the naive (M8) and split (M12) arms by parity and
the template's guard (M30), all fail as the iter arm's (M22); every
star counted, in the ★ (M3) and split (M13) arms, the pairs arm's
opening bar taken inside its pair (M17) and its inside never taken off
(M18), the iter arm's bars not counted (M23) and the template's guard
dropped (M28), all fail alike, and none is kept; the template's flag
never flipped back (M27) fails as the ★ arm's (M1), the iter arm's
count begun at 1 (M26) as the template's (M29). The naive arm's count
set, not added to (M11), fails apart from every kept one, and was left
out to keep three to an arm. M19 replaces the pairs arm's search
resumed two past the closing bar, which sliced past the end of the
string and crashed.

## Verification

Every arm prints the same output as `count.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` every arm takes 0.25 to 0.4 s, the naive arm,
which counts the bars before each star again, at the top. The
differential takes 1.9 s there and 0.5 s under `karac __mir-llvm-run`.

## Benchmarks

The bench builds 1000 strings of 1000 characters once, bars one time in
2 to 9 and stars one time in 2 of the rest, the last character a bar
when the bars before it are odd, then makes 100 passes, pass `p` taking
string `(7 a + p) % 1000` at step `a`, with the ★ arm in all five
languages. Every implementation prints `100 passes over 1000 strings of
1000 characters: checksum 306224139`. Each walks the characters with a
flag and a 64-bit count: Kāra's and Rust's `chars()`, Go's `range` over
the string's runes, Python's loop over the string, and C's bytes.

BENCHTAB
