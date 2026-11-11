# 2083. Substrings That Begin and End With the Same Letter

You are given a 0-indexed string `s` consisting of only lowercase English
letters. Return the number of substrings in `s` that begin and end with
the same character.

A substring is a contiguous non-empty sequence of characters within a
string.

```
s = "abcba"   ->  7
s = "abacad"  ->  9
s = "a"       ->  1
```

**Constraints:** `1 <= s.length <= 10^5`; `s` consists only of lowercase
English letters.

A substring is fixed by its two ends, so one that begins and ends with
the same letter is a pair of places `i <= j` holding that letter. A
letter that occurs `c` times gives `c` such substrings of one letter and
`c(c - 1) / 2` longer ones, `c(c + 1) / 2` in all, and the answer is that
sum over the letters: one pass to count, O(n). The approaches differ in
how they count.

## Approaches

| file | mechanism |
|---|---|
| `same.kara` ★ | the letters counted in an array of 26 through `bytes()`, and `c(c + 1) / 2` summed over the counts by `iter().map(..).sum()`. O(n) |
| `same_running.kara` | as the letters come: the `i`-th occurrence of a letter ends `i` new substrings, so a `Map[char, i64]` of occurrences so far, raised through `entry(c).or_insert(0)`, and their running sum |
| `same_sorted.kara` | the letters `collect`ed into a `Vec[char]` and sorted, so each letter is one run, and a run of `c` adds `c(c + 1) / 2`. O(n log n) |
| `same_letters.kara` | letter by letter over the char range `'a'..='z'`: the string walked again for each, its occurrences `filter(..).count()`ed. O(26 n) |
| `same_struct.kara` | a `struct Tally` of each letter's count and the substrings so far, with `add(b)` raising the count and adding it |
| `same_solution.kara` | LeetCode's Rust template (`s: String`, `[0i64; 26]`, `(b - b'a') as usize`, `iter().map(\|&c\| ..).sum()`), carried by `karac fix` in two rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's three examples and four
more, each string and its count; then the sum and a checksum of the
counts of 2000 random strings of 1 to 200 letters from the first 1, 2, 5
or 26 letters of the alphabet; then the count for the constraints'
largest, `10^5` letters of three. `same.py` mirrors the ★ arm and its
output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every pair of places `i <= j` looked at, and counted when the
letters there are the same. It checks 300 random strings of 1 to 30
letters from the first 1, 2, 5 or 26 of the alphabet; then 20 of one
letter, and 20 of letters all different. All 340 are drawn before any
arm answers.

| | property |
|---|---|
| P1 | the count is the statement read literally |
| P2 | the string reversed gives the same count |
| P3 | the letters renamed, each moved 7 on round the alphabet, give the same count |
| P4 | the string followed by the next one counts both, and for each letter its occurrences in the one times those in the other |
| P5 | the string with its first letter written again at its end counts that letter's occurrences, and one, more |
| P6 | each arm agrees with at least three of the other five |

The differential prints `340 strings: checksum 505159579, 12240 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal counts was checked against a Python reading of the same
strings. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Thirty-two edits to the differential, five to seven to each of its arms,
each run under `karac __mir-llvm-run` and `karac __mir-run`. Seventeen
are kept, three to each Kāra arm and two to the Rust-template arm. Each
kept one is killed, fails the same way under both backends and not by a
crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the letters merged in pairs | P1 204, P3 194, P4 245, P5 153, P6 204 |
| M2 | ★: every letter starting at one | P1 340, P4 340, P5 340, P6 340 |
| M3 | ★: each letter counted twice | P1 340, P4 266, P5 340, P6 340 |
| M4 | running: each letter adding one | P1 294, P4 266, P5 340, P6 294 |
| M5 | running: the sum taken before the count is raised | P1 340, P5 340, P6 340 |
| M6 | running: the first letter skipped | P1 340, P2 110, P4 235, P5 340, P6 340 |
| M7 | sorted: the letters left unsorted | P1 181, P4 243, P5 223, P6 181 |
| M8 | sorted: the last run never closed | P1 340, P3 29, P4 340, P5 178, P6 340 |
| M9 | sorted: each run after the first one longer | P1 223, P3 27, P4 180, P5 37, P6 223 |
| M10 | letters: `z` never counted | P1 34, P3 50, P4 4, P5 4, P6 34 |
| M11 | letters: `a` never counted | P1 256, P3 266, P4 209, P5 142, P6 256 |
| M12 | letters: the letters up to this one counted | P1 340, P3 339, P4 340, P5 340, P6 340 |
| M13 | tally: the letters folded onto half the alphabet | P1 70, P4 101, P5 50, P6 70 |
| M14 | tally: one substring before any letter | P1 340, P4 340, P6 340 |
| M15 | tally: an occurrence ending two substrings at most | P1 253, P4 246, P5 259, P6 253 |
| M16 | solution: the adapter adding an `a` | P1 340, P3 266, P4 340, P5 142, P6 340 |
| M17 | solution: the most common letter alone | P1 223, P4 273, P5 95, P6 223 |

P1 and P6 kill all seventeen, P4 and P5 sixteen each, P3 seven and P2
one. P4 and P5 are the problem's own arithmetic, a joined string's
count and one letter more, and see every edit that gets a letter's
`c(c + 1) / 2` wrong; P4 misses only an edit that counts each letter one
too few (M5), as both sides of the join lose the same, and P5 only a
constant added (M14), which the longer string carries too. P3, which
renames the letters, sees an edit that treats some letters apart: a
letter left out (M10, M11, M16) or merged with another (M1, M12), or a
sort whose runs end by the alphabet (M8, M9). P2, which reverses the
string, sees only the first letter skipped (M6), as every arm counts
letters regardless of where they stand.

Of the thirty-two, fifteen were not kept, and one survives, which is
equivalent: the sorted arm's run compared with the letter before rather
than the run's first, the same letter in a sorted run. Thirteen fail as a
kept one: the ★ arm's single letters not counted, the running arm's
letter seen once already and the tally arm's sum before its count and
counts starting at one as M5; the ★ arm's counts squared, the running
arm's twice its number less one, the sorted arm's run squared, the tally
arm's each occurrence the first and its number squared, and the Rust
arm's letters marked, not counted, as M4, all wrong as soon as a letter
repeats; the letters arm's count doubled as M3; the Rust arm's one more
per letter as M14; its adapter dropping the first letter as M6. One is
killed with checks of its own but was left out because its arm keeps
three: the letters arm's count capped at 3 (P1 216, P4 234, P5 217).

## Verification

Every arm prints the same output as `same.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them.

Under `karac __mir-run` the arms take 0.9 s to 1.2 s, but for the
letters arm's 17.6 s, which walks the largest string 26 times, and the
differential 3.2 s (timed while other work shared the machine).

The letters arm met two compiler gaps. The char range `'a'..='z'`
could not be iterated: the library's ranges step through any type with
`RangeStep`, which only the integers had, and `char` now has it, stepping
over the surrogate gap as Rust's does. And a `for` loop straight over a
char range was lowered as a counting loop, which the MIR interpreter
refused ("Add on Char") and which would walk into the surrogates; it now
iterates the library's range. Fixed in kara 81aca4606b, test
`tests/kata_2083_char_range.rs`.

The Rust arm was written as LeetCode's Rust template. `karac fix` carries
it in two rounds of 3 and 1 edits: the `&` of `|&c|` dropped, `struct
Solution;` to `struct Solution {}`, `Solution::` to `.`; then the `i64`
suffix of `0i64`. The fixed arm reads as the template does, `as usize`
index and all.

## Benchmarks

The bench builds one text of `10^6` letters, the first of the alphabet
far more often, and counts 5000 windows of `10^5` letters at random
places in it with the ★ arm in all five languages, each window a view
into the text where the language has one (a `Str`, a `&str`, a Go
substring, a pointer and a length) and a copied slice in Python: `5 ·
10^8` letters read. Every implementation prints `5000 windows: sum
2093446099032, checksum 838347794`.

BENCHTAB
