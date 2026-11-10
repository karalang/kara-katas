# 2067. Number of Equal Count Substrings

You are given a 0-indexed string `s` consisting of only lowercase English
letters, and an integer `count`. A substring of `s` is said to be an
equal count substring if, for each unique letter in the substring, it
appears exactly `count` times in the substring.

Return the number of equal count substrings in `s`.

A substring is a contiguous non-empty sequence of characters within a
string.

```
s = "aaabcbbcc", count = 3  ->  3    ("aaa", "bcbbcc", "aaabcbbcc")
s = "abcd", count = 2       ->  0
s = "a", count = 5          ->  0
```

**Constraints:** `1 <= s.length <= 3 · 10^4`; `1 <= count <= 3 · 10^4`;
`s` consists only of lowercase English letters.

An equal count substring with `k` different letters is exactly `k ·
count` letters long, and `k` is at most 26. So there are only 26 lengths
to look at, and for each a window of that length slides over the text,
keeping its letters' counts and how many of them are at exactly
`count`: O(26 n). The approaches differ in how they keep the counts, and
one does not slide a window at all.

## Approaches

| file | mechanism |
|---|---|
| `count.kara` ★ | for each `k` from 1 to 26, a window of `k · count` letters over `bytes()`: an `Array[i64, 26]` of counts and the number of letters at exactly `count`, the window counted when that is `k`. O(26 n) |
| `count_extend.kara` | from every start, the substring grown a letter at a time with its letters counted, until a letter passes `count`; counted when its length is `count` times its different letters. O(n · 26 count) at most |
| `count_prefix.kara` | prefix counts, a `Vec[Array[i64, 26]]` of each prefix's letters, and for each end and each of the 26 lengths the window's counts as two prefixes' difference, checked with `(0..26).all(..)`: every letter 0 or `count` |
| `count_map.kara` | the window of `k · count` letters over `chars()` with its letters in a `Map[char, i64]` that drops a letter at 0; counted when the map holds `k` letters and `values().all(..)` are `count` |
| `count_struct.kara` | the window as a value: a `struct Window` of counts, the letters at `count` and `count` itself, with methods `take(mut ref self, ..)` and `let_go`; one window for each `k` up to the number of different letters, found first in a `SortedSet` |
| `count_solution.kara` | LeetCode's Rust template (`s.as_bytes()`, `count as usize`, `for k in 1..=26usize`, a `[0usize; 26]` window, `b'a'` arithmetic to a `usize` index), carried by `karac fix` in two rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 11 lines: LeetCode's three examples and five
more, each text, its `count` and the answer; then the sum of the answers
and a checksum for 500 random texts of 1 to 300 letters from the first 1
to 26 of the alphabet, count 1 to 10, each letter a run of `count` with
a chance of 0 to 100 in 100 and else a single letter; then the answers
for two texts of the largest length, 30000 letters from 4 kinds with
count 5 and from all 26 in runs of 3 with count 3. `count.py` mirrors
the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every substring taken out whole, each of the 26 letters
counted in it afresh, and kept when every letter there is there exactly
`count` times, O(26 n³). It checks 300 random texts of 1 to 40 letters
from 1 to 6 kinds, count 1 to 4, drawn as the harness draws them; then
20 with count 1 from all 26 letters, 20 of 41 to 120 letters, and 20
holding the whole alphabet shuffled, each letter once or twice, between
up to five random letters on either side. All 360 are drawn before any
arm answers; 334 have an answer above 0.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the text reversed has the same answer |
| P3 | the letters renamed in a cycle (`a` to `b`, ..., `z` to `a`) leave the answer |
| P4 | every letter written twice and `count` doubled never lowers the answer |
| P5 | the answer is at most the number of substrings whose length `count` divides, and with `count` 1 at least the number of letters |
| P6 | each arm agrees with at least three of the other five |

P4 holds because an equal count substring of the text, each letter
written twice, is one of the doubled text with every letter `2 · count`
times.

The differential prints `360 texts: checksum 950182775, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading of the same
texts. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Thirty-one edits to the differential, four to six to each of its arms,
each run under `karac __mir-llvm-run`, and the kept ones and the
survivors under `karac __mir-run` too. Seventeen are kept, three to each
Kāra arm and two to the Rust-template arm. Each kept one is killed, fails
the same way under both backends and not by a crash, and no two kept
ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a letter one past `count` left at `count` | P1 306, P2 235, P4 26, P5 67, P6 306 |
| M2 | ★: only up to 25 different letters | P1 20, P6 20 |
| M3 | ★: the window one letter too long | P1 317, P2 181, P4 117, P5 103, P6 317 |
| M4 | extend: a stop one letter late | P1 152, P4 65, P6 152 |
| M5 | extend: the counts kept from one start to the next | P1 326, P2 114, P4 5, P5 103, P6 326 |
| M6 | extend: the last start never tried | P1 107, P5 17, P6 107 |
| M7 | prefix: the earlier prefix's count taken modulo `count` | P1 334, P5 107, P6 334 |
| M8 | prefix: the last letter of the alphabet not checked | P1 2, P3 6, P6 2 |
| M9 | prefix: an `a` counted twice in its prefix | P1 278, P3 281, P5 43, P6 278 |
| M10 | map: only one letter needed at `count` | P1 152, P2 134, P6 152 |
| M11 | map: the letter let go one place too early | P1 241, P2 194, P4 115, P6 241 |
| M12 | map: each window one letter past `(k - 1) · count` | P1 227, P4 107, P6 227 |
| M13 | struct: a letter one past `count` left at `count` | P1 306, P2 225, P4 28, P5 73, P6 306 |
| M14 | struct: only the letters the text has, less one | P1 196, P5 17, P6 196 |
| M15 | struct: a letter let go not counted down | P1 324, P2 208, P5 72, P6 324 |
| M16 | solution: the adapter's count one more | P1 333, P4 10, P5 106, P6 333 |
| M17 | solution: only up to 13 different letters | P1 21, P6 21 |

P1 and P6 kill all seventeen, P5 ten, P4 eight, P2 seven and P3 two.
334 of the 360 texts have an answer, so `P1 334` is an arm wrong on all
of them. The 20 texts holding the whole alphabet are what kill M2 and
M17 nearly alone: few other texts have so many different letters in
one window, and before that family was drawn M2 survived and M17 failed
on one text. P2 sees an edit that treats the two ends of a window or a
substring differently (M1, M3, M5, M10, M11, M13, M15); P3, which moves `z` to `a`, the two edits that
tell one letter from another (M8, M9), which no correct arm does; P4,
which doubles every count, the edits off by a fixed step that does not
double with it (M3, M4, M12, M16); P5 an answer above the number of
substrings of a fitting length, or a count-1 text not counting every
single letter.

Of the thirty-one, fourteen were not kept. Two survive, and both are
equivalent: the ★ arm's window counted before it is full (a window
shorter than `k · count` cannot hold `k` letters at `count`), and the
struct arm's kinds a `Vec` with repeats, which tries more values of `k`
than there are different letters, and none of those can be counted.
Three fail as a kept one: the extend arm's length one short as M7, the
Rust arm's letter let go never counted down as M15, and its good count
kept at `count` and above as M1. Three fail alike and none is kept: the
prefix arm's window as long as the text left out, the struct arm's
windows counted from the second letter on, and the Rust adapter's text
without its first letter (P1 284, P2 181, P5 18). Six are killed with
checks of their own but were left out because their arm keeps three:
the ★ arm's letter let go taken out before it is checked (P1 323, P2
224, P4 56, P5 92); the extend arm with no stop when a letter passes (P1
162) and a letter's first time not counted when `count` is 1 (P1 107,
P5 107); the prefix arm's windows ending at the last letter left out
(P1 245, P2 181, P5 19); the map arm's letter at 0 kept (P1 257, P2 207,
P5 86) and the letters' number not checked (P1 275, P2 187, P5 20).

## Verification

Every arm prints the same output as `count.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every arm
and the differential. `karac check --output=json` reports nothing on any
of them.

VERTIMES

No arm met a compiler gap. The ★ arm's text was first taken as `let
bytes: Vec[u8] = s.bytes().collect()`, Rust's way to an indexable list of
bytes; `bytes()` is already a `Slice[u8]`, and the checker said that a
`Slice` takes no iterator adaptor without `.iter()`. The arm indexes the
slice itself.

The Rust arm was written as LeetCode's Rust template. `karac fix` carries
it in two rounds of 2 and 6 edits: `struct Solution;` to `struct
Solution {}` and `Solution::` to `Solution.`; then `as_bytes()` to
`bytes()`, and the `usize` of `count as usize`, the `26usize` bound, the
`[0usize; 26]` window and the two `as usize` indices to `i64`, Kāra's
type for counts and places. The fixed arm reads as the template does.

## Benchmarks

The bench answers 60 texts of 30000 letters with the ★ arm in all five
languages: the first 1 to 26 letters of the alphabet, half of them in
runs of `count`, count 1 to 7, so every one of the 26 windows slides
over the whole text. Every implementation prints `60 texts: sum 1807731,
checksum 234740632`.

BENCHTAB
