# 1397. Find All Good Strings

Given the strings `s1` and `s2` of size `n` and the string `evil`,
return the number of good strings.

A good string has size `n`, it is alphabetically greater than or equal
to `s1`, it is alphabetically smaller than or equal to `s2`, and it does
not contain the string `evil` as a substring. Since the answer can be a
huge number, return this modulo `10^9 + 7`.

```
n = 2, s1 = "aa", s2 = "da", evil = "b"                ->  51
n = 8, s1 = "leetcode", s2 = "leetgoes", evil = "leet"  ->  0
n = 2, s1 = "gx", s2 = "gz", evil = "x"                ->  2
```

**Constraints:** `s1.length == n`, `s2.length == n`, `s1 <= s2`, `1 <= n
<= 500`, `1 <= evil.length <= 50`, and all strings consist of lowercase
English letters.

Each arm is `fn find_good_strings(n: i32, s1: String, s2: String, evil:
String) -> i32`.

## Approaches

| file | mechanism |
|---|---|
| `find_good_strings.kara` ★ | the strings built a letter at a time, counted by how much of `evil` their end matches and whether they are still equal to s1's prefix and to s2's, in one flat `Vec` of m * 4 counts; the matches stepped through Knuth, Morris and Pratt's automaton, a table of the next match for every match and letter built from the failure table, and a string that would match all of `evil` dropped. O(n m 26) |
| `find_good_strings_count.kara` | the good strings no larger than a bound counted with a single flag, still equal to the bound's prefix, and the answer `upto(s2) - upto(s1)`, plus one when s1 is good itself (`s1.contains(evil)`); the next match found by falling back along the failure table at each letter, with no table. O(n m 26) for each bound, beside the falls back |
| `find_good_strings_memo.kara` | top-down: the good endings from a position, given the match and the two flags, by a recursive `mut ref self` method on a `struct` that holds the bytes, the failure table and a flat memo with -1 for unknown |
| `find_good_strings_text.kara` | each state the text itself, the longest end of the string so far that begins `evil`, as a `String`; its next state after a letter found by trying every shorter end with `starts_with` and kept in a `Map[(String, char), Option[String]]`, and the counts in a `Map` keyed by the state and the two flags, one `Map` a letter, the letters walked as a `char` range |
| `find_good_strings_solution.kara` | a Rust solution as LeetCode's Rust users write it (the prefix table built with one `while` loop, a nested `fn dfs` over position, evil index and the two tight flags as `usize`s, memoized in a four-deep `vec!`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 3 lines: LeetCode's three examples, one string
that is good and one that is not (`51 0 2 1 0`); the constraints' most,
n = 500 from a random s1 to `z` 500 times, with evil strings of 1, 8 and
50 letters (`n = 500: 169547125 531982015 57590800`); and 2000 random
cases of 1 to 12 letters, the evil string 1 to 4 letters (`2000 random
cases: 435974718 in all, checksum 188786757`). `find_good_strings.py`
mirrors the ★ arm, and its output is byte-identical; it also agrees with
every string tried, by brute force, on 300 cases of up to 3 letters.
Every arm gives the same output under `karac __mir-run`, `karac run`,
`karac build` and `karac __mir-llvm-run`.

The Mend loop: the ★ and text arms check clean as first written. The
count arm passed `s2.bytes()` to a `bound: Vec[u8]` parameter; `bytes()`
gives a `Slice[u8]`, and check says so and names both a `.to_vec()` copy
and a `Slice[u8]` parameter. `karac fix` writes the copy,
`upto(s2.bytes().to_vec(), e.to_vec(), border)`, 4 fixes. The memo arm
put the same slices into its struct's `Vec[u8]` fields and wrote `n as
i64`, which an `i32` needs no cast to become; `karac fix` writes 3
`.to_vec()`s and drops the cast. The Rust solution takes one round of 50
fixes by `karac fix`'s count, and its output matches on the first run:
`struct Solution;` to `struct Solution {}`, the nested `fn dfs` moved to
the top level (Kāra has no nested items, and a nested `fn` captures
nothing, so it means the same there), every `usize` to `i64`, `&[u8]` to
`Slice[u8]`, `&mut Vec<..>` to `mut ref Vec[..]`, `as_bytes()` to
`bytes()`, `vec![vec![..]; n]` to `Vec.filled(n, Vec.filled(..))`, `&&`
to `and`, the `&` dropped from arguments and `&mut memo` written `mut
memo`, and `Solution::` to `Solution.`.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every string from s1 to s2 in order, each one tried for
`evil` at every place. LeetCode's three examples and 2000 random cases,
either two strings of 1 to 3 letters from the first 1 to 8, so the range
between them is wide, or a string of 1 to 12 letters and the one 0 to
2000 after it, so the strings are long, half of them from the first 1 to
3 letters, where `evil` matches, fails and matches again, and half from
the first 1 to 26; the evil string 1 to 4 letters from the first 1 to 3.
Every case is drawn before any arm answers.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the range cut at its middle string: the two halves' counts, the middle counted once |
| P3 | every letter turned the other way round the alphabet, so s2's mirror comes first: the same count |
| P4 | `evil` with a letter put after it: no fewer good strings, and none more than the range holds |
| P5 | a range of s1 alone and of s2 alone: one when the string is good, none when not |
| P6 | the ★ arm's answer |

All 60,090 checks pass on every arm: `2003 cases: checksum 902149946,
60090 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and `karac __mir-llvm-run`. Python, trying every
string with `in`, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the automaton with no fall back, so a letter that breaks a match starts from nothing even when it begins `evil` | P1 54, P2 3, P5 10, P6 216 |
| M2 | ★: s1's flag never released, so every letter after the first is held at s1's or above | P1 884, P2 1056, P3 1134, P6 3536 |
| M3 | count: s1 counted as good whether it holds `evil` or not | P1 324, P2 239, P3 186, P5 372, P6 324 |
| M4 | count: the bound's own letter counted as below the bound | P1 301, P2 15, P3 301, P4 119, P6 301 |
| M5 | memo: the memo's key without s2's flag | P1 987, P2 981, P3 1050, P4 1057, P6 987 |
| M6 | memo: a broken match falling back to nothing, not to its border, before `evil`'s first letter is tried | P1 7, P5 3, P6 7 |
| M7 | text: the whole text never its own next state, so a match one letter short of `evil` is lost | P1 374, P2 95, P5 162, P6 374 |
| M8 | text: s2's flag kept after a letter below s2's | P1 1107, P2 1064, P3 1134, P6 1107 |
| M9 | solution: the base cases swapped, so a string that ends in all of `evil` counts | P1 592, P2 56, P5 144, P6 592 |
| M10 | solution: s2's flag set by a letter equal to s2's whether the prefix was still at s2's or not | P1 614, P2 331, P3 620, P6 614 |

P1 and P6 kill all ten, P2 nine, P3 six, P5 five and P4 two. M6 is the
weakest: after falling back it still tries `evil`'s first letter, so it
errs only where a border of `evil` must be kept, as with `aab` inside
`aaab`, and 7 cases of 2003 have one. M1, which does not try even the
first letter, errs wherever a letter that breaks a match begins a new
one, `a` after `a` for `evil` = `ab`. Both needed the long strings over
1 to 3 letters: with every long string over 1 to 26 letters, as the
differential first drew them, M6 was killed by one case and M1 by 18. A
first M9, the prefix table's fall back cut to 0 in the solution's
`while` loop, was replaced: it builds the same table as the right one
for every `evil` of up to 5 letters over `a`, `b` and `c` (all 363
tried; the first that differs is `aabaaa`), and the differential's are 1
to 4 letters from those three, so here it is an equivalent mutant. The
bound on the count (P4) catches only the edits that count strings
outside the range (M4, M5); the mirror (P3) misses the edits that
miscount matches, which mirroring every letter keeps as they were (M1,
M6, M7, M9).

## Benchmarks

The bench runs the ★ arm at the constraints' most: s1 500 letters from
`a` to `c`, s2 500 from `x` to `z`, and an evil string of 50 letters
from `a` to `c`, one letter of each changed, at places drawn from the
checksum so far, before each of 200 rounds. Every implementation prints
`200 rounds at n = 500, evil of 50 letters: checksum 45721893`. A count
is skipped when it is zero, so the work is the matches a string can
reach, a few of the 50, times the 26 letters, at each of the 500 places.

BENCHTAB
