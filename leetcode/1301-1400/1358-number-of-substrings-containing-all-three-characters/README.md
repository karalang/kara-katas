# 1358. Number of Substrings Containing All Three Characters

Given a string `s` consisting only of characters `a`, `b` and `c`.

Return the number of substrings containing at least one occurrence of
all these characters `a`, `b` and `c`.

```
s = "abcabc"  ->  10    abc, abca, abcab, abcabc, bca, bcab, bcabc, cab, cabc, abc
s = "aaacb"   ->  3     aaacb, aacb, acb
s = "abc"     ->  1
```

**Constraints:** `3 <= s.length <= 5 * 10^4`, `s` only consists of
`a`, `b` or `c` characters.

Each arm is `fn number_of_substrings(s: Str) -> i32`.

## Approaches

| file | mechanism |
|---|---|
| `number_of_substrings.kara` ★ | where each of a, b and c was last seen. A substring ending at i holds all three exactly when it starts at or before the earliest of those three places, so it adds that place + 1 starts. O(n) |
| `number_of_substrings_window.kara` | two pointers and the counts of a, b and c between them. For each start the window grows until it holds all three, and every end from there to the string's end makes one more substring; then the start's letter leaves. O(n) |
| `number_of_substrings_prefix.kara` | how many of each letter the first i letters hold, for every i. For each start, the first end where all three counts have grown is found by a binary search per letter, `partition_point`, and every end from the latest of those makes a substring. O(n log n) |
| `number_of_substrings_complement.kara` | every substring, less the ones that miss a letter, by inclusion and exclusion: a substring missing a lies in a run of the other two letters, a run of r letters holding r (r + 1) / 2 of them, and one missing two letters lies in a run of the third. O(n) |
| `number_of_substrings_solution.kara` | a Rust solution as LeetCode's Rust users write it (a sliding window over `s.as_bytes()` with `let mut count = [0; 3]` indexed by `(s[right] - b'a') as usize`, adding `s.len() - right` for each start let go), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 2 lines: LeetCode's three examples, a string
missing c, and 5 * 10^4 letters, the constraints' most: "abc" repeated,
all a then a b and a c, and at random (`10 3 1 0 1249925001 49998
1249800798`); and 2000 random strings of 3 to 300 letters, most of them
short, the letters evenly drawn or c rare (`2000 random strings:
2595465 substrings in all, checksum 625495463`). The most a string of
5 * 10^4 letters can have is 1,250,025,000, under 2^31, so the count
fits an `i32`. `number_of_substrings.py` mirrors the ★ arm, and
its output is byte-identical. Every arm gives the same output under
`karac __mir-run`, `karac run` and `karac __mir-llvm-run`.

The Mend loop: the ★, window, prefix and complement arms check clean.
The Rust solution takes one round of 4 fixes by `karac fix`'s count:
`struct Solution;` becomes `struct Solution {}`, `s.as_bytes()`
`s.bytes()`, and each `&&` `and`. The fixed-size `[0; 3]` and the `as
usize` index casts stand: Kāra indexes with any integer. Every arm
matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every substring `s[i..j]` taken in turn, and counted when an
a, a b and a c each occur in it. 2000 strings of 3 to 12 letters in four
kinds, 500 each: the letters evenly drawn; c rare; runs of one letter,
each of 1 to 4; and "abc" with letters drawn around it. Every string is
drawn before any arm answers.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the letters renamed, a to b, b to c and c to a: the same count |
| P3 | the string backwards: the same count |
| P4 | "abc" put after the string: at least n + 1 more, every start ending at the last c |
| P5 | every a made a b: none |
| P6 | the ★ arm's count |

All 60,000 checks pass on every arm: `2000 strings: checksum 29820975,
60000 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run` and `karac __mir-llvm-run`. Python, testing every substring's set
of letters, gives the same checksum. The differential's `arm` was
written `got as i64` over an `i32`, and `karac fix` drops the cast
(W0310).

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash, and no two
fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the earliest place counted, not the starts up to it | P1 2000, P4 521, P5 2000, P6 8000 |
| M2 | ★: the first place of each letter kept, not the last | P1 1101, P3 964, P4 2000, P6 4404 |
| M3 | window: the first end holding all three not counted | P1 1229, P3 964, P4 759, P6 1229 |
| M4 | window: the start's letter never leaves | P1 1229, P3 964, P6 1229 |
| M5 | prefix: only c's first end taken | P1 1583, P2 1870, P5 1583, P6 1583 |
| M6 | prefix: a substring ending at the last letter not counted | P1 549, P3 674, P4 559, P6 549 |
| M7 | complement: the substrings of one letter taken out twice | P1 2000, P4 560, P5 2000, P6 2000 |
| M8 | complement: a run never broken | P1 1229, P4 2000, P6 1229 |
| M9 | solution: a window without c accepted | P1 1441, P2 1576, P6 1441 |
| M10 | solution: one start let go for each end | P1 1053, P3 1016, P4 841, P6 1053 |

P1 and P6 kill all ten, P4 seven, P3 five, P5 three and P2 two. A
string with no a (P5) has no such substring, and catches the edits that
count one anyway: the earliest place counted where a letter was never
seen, -1 (M1), c's end taken alone (M5), and the one-letter runs taken
out twice (M7). Renaming the letters (P2) catches the edits that treat
one letter apart from the others (M5, M9). The string backwards (P3)
catches the edits whose miscount depends on where the letters lie: the
first places kept (M2), the window's off-by-ones (M3, M4, M10) and the
last letter's substring (M6). "abc" put after the string (P4) must add
a start for every place up to the new a, and catches every edit that
misses starts at the end or loses count over a longer string.

## Benchmarks

The bench builds 20 strings of 5 * 10^4 letters, the constraints' most,
c drawn one time in 1000 and a and b evenly, once; then makes 1000
rounds, each setting one letter of one string, both drawn from the
checksum so far, so no answer carries over, and counting that string's
substrings with the ★ arm's last places. Every implementation prints
`1000 rounds over 20 strings of 5 * 10^4 letters: checksum 489630734`.
C takes the least of the three places by two comparisons, Go with the
built-in `min`, Rust, Kāra and Python with an iterator's or the
built-in `min` over the three.

BENCHTAB
