# 2062. Count Vowel Substrings of a String

A substring is a contiguous (non-empty) sequence of characters within a
string.

A vowel substring is a substring that only consists of vowels (`'a'`,
`'e'`, `'i'`, `'o'`, and `'u'`) and has all five vowels present in it.

Given a string `word`, return the number of vowel substrings in `word`.

```
word = "aeiouu"         ->  2    ("aeiou", "aeiouu")
word = "unicornarihan"  ->  0
word = "cuaieuouac"     ->  7
```

**Constraints:** `1 <= word.length <= 100`; `word` consists of lowercase
English letters only.

A consonant ends every substring through it, so the word falls into runs
of vowels and each run is counted alone. Within a run, a substring
ending at a given place holds all five vowels exactly when it starts at
or before the least of the five vowels' last places: an O(n) pass. The
constraints allow the O(n²) scan from every start, which the ★ arm is.

## Approaches

| file | mechanism |
|---|---|
| `vowels.kara` ★ | every start, extended while the letters are vowels: the vowels met in a `Set[char]`, each end counted once all five are in it; a vowel test `"aeiou".contains(c.to_string())`. O(n²) |
| `vowels_window.kara` | one pass over `chars().enumerate()` with a `match` on or-patterns: a `Map[char, i64]` of each vowel's last place in the current run, `last.values().min()` the earliest start that holds all five; a consonant clears the map. O(n) |
| `vowels_atmost.kara` | a difference of two sliding windows: the substrings of vowels with at most five different vowels, less those with at most four; each window keeps a `Vec` of how many of each vowel it holds and moves its left end on while it holds too many. O(n) |
| `vowels_mask.kara` | every start, the vowels met as bits of a `u8` over `bytes()`: `bit` gives `Option[u8]`, a consonant's `None` ending the inner loop at a `let .. else`, an end counted at `0b11111`. O(n²) |
| `vowels_runs.kara` | inclusion and exclusion over each run of vowels (`chunk_by` splits the letters where a vowel meets a consonant): for each of the 32 sets of vowels, the substrings missing that set, counted from the pieces it cuts the run into, signed by the set's size; what is left misses no vowel |
| `vowels_solution.kara` | LeetCode's Rust template (`use std::collections::HashMap`, a closure over `"aeiou".contains(c)`, `for (r, &c) in s.iter().enumerate()`, a `HashMap<char, i32>` window shrunk with `get_mut` and `remove`, `usize` ends), carried by `karac fix` in three rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 13 lines: LeetCode's three examples and seven
more, each word and its answer; then the sum of the answers and a
checksum for 500 random words of 1 to 100 letters, each a vowel with a
chance of 50 to 100 in 100 and else one of `xyz`; then the answers for a
word of 100 vowels and for `aeiou` twenty times. `vowels.py` mirrors the
★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every substring taken out whole and kept when each of its
letters is a vowel and each vowel is among them, O(n³). It checks 300
random words of 1 to 40 letters drawn as the harness draws them, then 40
of vowels only and 20 with one vowel never used. All 360 are drawn before
any arm answers; 128 have an answer above 0.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the word reversed has the same answer |
| P3 | a consonant put in at any place makes the answer the two sides' answers added |
| P4 | the vowels renamed in a cycle (`a` to `e`, ..., `u` to `a`) leave the answer |
| P5 | a vowel added at the end never lowers the answer, and a consonant leaves it |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 words: checksum 493222808, 12960 checks over
6 arms: 0 failures` under every lane in Verification; the checksum of the
literal answers was checked against a Python reading of the same words.
On a failure it prints the first ten and then the count by property.

## Mutation testing

Thirty-three edits to the differential, four to six to each of its arms,
each run under `karac __mir-llvm-run`, and the kept ones under `karac
__mir-run` too. Seventeen are kept, three to each Kāra arm and two to the
Rust-template arm. Each kept one is killed, fails the same way under both
backends and not by a crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a consonant skipped over | P1 161, P2 151, P3 203, P6 161 |
| M2 | ★: no substring starting at the first letter | P1 80, P2 95, P3 44, P6 80 |
| M3 | ★: no substring ending at the last letter | P1 77, P2 95, P3 37, P5 77, P6 77 |
| M4 | window: the run starting at the consonant | P1 53, P2 64, P3 44, P6 53 |
| M5 | window: the latest place, not the earliest | P1 128, P2 112, P6 128 |
| M6 | window: the places kept across a consonant | P1 153, P2 157, P3 159, P5 145, P6 153 |
| M7 | atmost: at most three subtracted | P1 219, P6 219 |
| M8 | atmost: `u` counted as `o` | P1 128, P6 128 |
| M9 | atmost: the counts kept across a consonant | P1 47, P2 48, P3 46, P6 47 |
| M10 | mask: `a` not needed | P1 106, P4 150, P6 106 |
| M11 | mask: a vowel met twice taken out again | P1 125, P6 125 |
| M12 | mask: the mask kept from one start to the next | P1 216, P2 206, P3 159, P6 216 |
| M13 | runs: the signs the wrong way round | P1 128, P5 86, P6 128 |
| M14 | runs: a run's last piece not counted | P1 128, P2 112, P5 23, P6 128 |
| M15 | runs: a piece's substrings one length short | P1 128, P2 111, P6 128 |
| M16 | solution: the run starting at the consonant | P1 250, P2 209, P3 270, P6 250 |
| M17 | solution: the window shrunk by one letter at most | P1 111, P2 114, P6 111 |

P1 and P6 kill all seventeen, P2 twelve, P3 eight, P5 four and P4 one.
Many edits fail every word with an answer, and nothing else (`P1 128,
P6 128`): any that merges two vowels or loses one gives 0 everywhere.
Only one of those could be kept (M8); the properties that tell the
others apart are the ones that see where in the word a mistake sits. P2
sees an edit that treats the two ends of a run differently (M2, M3, M5,
M14, M15); P3 one that lets a substring run through a consonant or
across from the run before (M1, M6, M9, M12, M16); P4 the mask arm's
test for four of the five bits, which renaming moves onto a different
vowel (M10); P5, which grows the word at its end, the edits
that miscount there (M3, M6, M13, M14).

Of the thirty-three, sixteen were not kept. Three survive, and all three
are equivalent: the atmost arm's windows each one substring short (every
vowel ends exactly one window in each count, so the difference loses
nothing); the runs arm's sets taken only to 31 (the set of all five
vowels cuts a run into nothing, adding 0); and the runs arm with the
consonant runs counted too (a run with no vowel has nothing to cut, so
its 16 even sets and 16 odd ones cancel). Twelve fail as a kept one: the
★ arm's four vowels enough as M7; its `u` not a vowel, the atmost arm's
window shrunk only past one more, the mask arm's `u` the same bit as `o`
and every substring counted twice, the window arm's `u` taken for a
consonant, and the Rust arm's adapter word in capitals and `o` not a
vowel as M8; the ★ arm's substrings never ending where they start as
M2; the window arm's substring short of the earliest place as M15; the
mask arm's consonant skipped over as M1; the runs arm's piece cut where
the vowels are kept as M13. One is killed with checks of its own but
left out because the Rust arm keeps two: one more counted at every vowel
(P1 355, P6 355).

## Verification

Every arm prints the same output as `vowels.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every arm
and the differential. `karac check --output=json` reports nothing on any
of them.

Under `karac __mir-run` the arms take 0.3 s to 0.6 s, except the runs
arm at 4.8 s, which goes over every run 32 times, and the differential
11.7 s (timed while other work shared the machine).

The ★ arm was written with Rust's vowel test, `"aeiou".contains(c)` for
a `c: char`. Every pattern parameter of the string methods is a `Str`
(docs/library/strings.md), so the checker refuses a char there with the
edit `c.to_string()`, which `karac fix` applied; the Rust arm's closure
took the same edit. The fixed test allocates a `String` on every call:
see Benchmarks.

The mask arm was written with a `while` over `j` and `j += 1` at the end
of its body; `karac fix` made it a `for j in i..bytes.len()`, a style
lint `karac check` allows.

The Rust arm was written as LeetCode's Rust template. `karac fix` carries
it in three rounds of 12, 2 and 3 edits: Rust's spellings (`<..>` to
brackets, the `HashMap` import deleted, `struct Solution;` to `struct
Solution {}`, `!` to `not`, the `&` of `&c`, `&lc` dropped, `Solution::`
to `Solution.`), then `HashMap` to `Map`, then the closure's
`c.to_string()`, `ans: i32` for an answer whose literal kept the default
`i64`, and the adapter's `as i64` that the `i32` widens to anyway. The
fixed arm reads as the template does.

## Benchmarks

The bench answers 20000 words of 100 letters with the ★ arm in all five
languages, each letter a vowel with a chance of 90 in 100 and else one of
`xyz`, so most starts run far. C keeps the vowels met from a start as
five flags; Rust and Go a set, as Kāra's `Set[char]`. Every implementation
prints `20000 words: sum 5584636, checksum 855783590`.

Kāra's vowel test is the one `karac fix` gave, `"aeiou".contains(c.to_string())`,
and the `String` it allocates on every letter visited makes the Kāra
build about 2.4 times slower than the same program with a `match` on the
letter (B-2026-11-10-25). The kata keeps the fixed form, as the Mend loop
produced it.

BENCHTAB
