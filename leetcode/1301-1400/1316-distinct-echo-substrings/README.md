# 1316. Distinct Echo Substrings

Return the number of **distinct** non-empty substrings of `text` that can
be written as the concatenation of some string with itself (i.e. it can be
written as `a + a` where `a` is some string).

```
text = "abcabcabc"         ->  3    ("abcabc", "bcabca", "cabcab")
text = "leetcodeleetcode"  ->  2    ("ee", "leetcodeleetcode")
```

**Constraints:** `1 <= text.length <= 2000`, `text` has only lowercase
English letters.

The arms are `fn distinct_echo_substrings(text: String) -> i32`.

## Approaches

| file | mechanism |
|---|---|
| `distinct_echo_substrings.kara` ★ | how far the suffixes from every two places agree, in a table filled from the back; a piece of length 2h from i is an echo when the suffixes from i and i + h agree for h letters, and it is counted at the first place it starts, which is when no earlier suffix agrees with the one from i for all 2h letters. O(n^2) time and space, no set |
| `distinct_echo_substrings_runs.kara` | for every half length h, the letters that match the one h places on, counted in runs from the back; a run of h or more from i makes the piece of length 2h from i an echo. Every echo kept as a `String`, the list sorted and its repeats dropped by `dedup`. O(n^2) to find, plus the sort |
| `distinct_echo_substrings_pieces.kara` | every place and every half length tried, the two halves compared as byte slices, and each echo's bytes put in a `Set[Vec[u8]]` so that a repeat is kept once. O(n^3) at worst |
| `distinct_echo_substrings_hash.kara` | a rolling hash of every prefix under two primes, so that any piece's hash is two lookups; the halves compared by hash, and each echo kept in a `Set` as its two hashes and its length. O(n^2), exact unless two pieces collide under both primes at once |
| `distinct_echo_substrings_solution.kara` | a Rust solution as LeetCode's Rust users write it (every half length `for len in 1..=n / 2` and place `for i in 0..=n - 2 * len`, the halves compared as `&text[..]` slices, each echo put in a `HashSet<&str>`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 2 lines: LeetCode's two examples, one letter,
four of one letter, with `aa` and `aaaa`, an echo found again later, and
300 of one letter (`3 2 0 2 1 150`); then 400 random strings of 1 to 300
letters over 1, 2, 3 or 26 letters, every other one a block of 1 to 6
letters said over and over with a few letters changed (`400 random
strings: echoes total 14246, checksum 131442996`).
`distinct_echo_substrings.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac __mir-run`,
`karac run` and `karac __mir-llvm-run`.

The Mend loop: the ★, runs and pieces arms checked clean as first
written. The hash arm took one fix: `s[i] as i64` is a widening `karac`
makes on its own, and `karac fix` dropped the cast. The Rust arm takes one
round of 8 fixes by `karac fix`'s count, from 7 errors: its `use` line
deleted, `struct Solution;` to `struct Solution {}`, `HashSet::new()` to
`Set.new()`, the `&` dropped from the three `&text[..]` slices, which
compare and go into the set as they are, and `::` to `.`. Its output
matches on the first run. No gap was met.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every piece of the string looked at, and when its length is
even and its first half is its second, it is kept unless an equal piece
was kept already. 2000 strings of 1 to 12 letters in four kinds, 500 each:
over 2 letters, over 3, and over all 26; and a block of 1 to 3 letters
over 3 said over and over, one letter changed every other time. Every
string, renaming and new letter is drawn before any arm answers.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the string reversed: the same answer, since an echo reversed is an echo |
| P3 | the letters renamed one for one, each moved the same number of places round the alphabet: the same answer |
| P4 | the string twice with a letter it does not have between: the same answer, since no echo can hold a letter found only once |
| P5 | the last letter dropped: no echo gained, and at most one lost for each half length, the ones that end at that letter |
| P6 | the ★ arm's answer |

All 60,000 checks pass on every arm: `2000 strings: checksum 426014727,
60000 checks over 5 arms: 0 failures`, under `karac __mir-run` and
`karac __mir-llvm-run`. Python gives the same checksum.

## Mutation testing

Ten edits to the differential, two to each arm, each run under both
`karac __mir-llvm-run` and `karac __mir-run`. Every one is killed, fails
the same way under both backends and not by a crash, and no two fail the
same checks, so all ten are kept.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a piece counted again when an earlier copy is exactly as long | P1 827, P2 161, P4 860, P5 30, P6 3308 |
| M2 | ★: two places' agreement never carried on from the next pair | P1 896, P4 1217, P6 3584 |
| M3 | runs: the repeats kept | P1 863, P4 1336, P6 863 |
| M4 | runs: the run not broken at a mismatch | P1 955, P2 841, P4 1468, P5 96, P6 955 |
| M5 | pieces: no echo found at the first place | P1 486, P2 396, P4 486, P6 486 |
| M6 | pieces: each place's longest half never tried | P1 887, P2 518, P4 887, P6 887 |
| M7 | hash: the halves compared without their last letters | P1 1199, P2 409, P4 988, P6 1199 |
| M8 | hash: the prefix hash a plain sum of the letters | P1 1336, P6 1336 |
| M9 | solution: the last place for each half length never tried | P1 524, P2 396, P4 524, P6 524 |
| M10 | solution: the longest half length never tried | P1 363, P4 363, P6 363 |

P1 and P6 kill all ten, P4 nine, P2 six and P5 two; P3 kills none.
Saying the string twice round a new letter (P4) doubles every place an
echo can start and leaves the set of echoes as it was, so it sees every
edit that loses an echo at one place, counts one twice, or finds one that
is not there; it misses only M8. Reversing the string (P2) catches the
edits that treat its two ends differently: the first or last place left
out (M5, M9), the longest half cut short where the string runs out (M6),
the halves cut at their ends (M7), the run counted from the back (M4) and
the copy counted twice by where it stands (M1); a whole kind of echo lost
or kept twice everywhere (M2, M3, M10) looks the same both ways. Dropping
the last letter (P5) only bounds the answer, and catches the two edits
that sometimes count more echoes in the shorter string (M1, M4). Renaming
the letters (P3) reaches no edit: four of the arms only ask whether two
letters are equal, and the broken hash of M8, which reads the letters'
codes, gives every renamed string here the same count as the string
itself.

## Benchmarks

The bench builds 4 strings of 2000 letters, the constraints' longest,
once from its own generator: over 2 letters, over 3, over 26, and a block
of 3 letters said over and over. It then makes 5 passes, each setting one
letter of every string from the checksum so far, so no answer carries
over, answering it with the ★ arm and folding the count plus the pass
into the checksum. Each call takes a fresh table in every language, a
`calloc` in C. Every implementation prints `5 passes over 4 strings of
2000: checksum 964235194`.

BENCHTAB
