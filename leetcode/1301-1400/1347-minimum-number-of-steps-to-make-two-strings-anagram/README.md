# 1347. Minimum Number of Steps to Make Two Strings Anagram

You are given two strings of the same length `s` and `t`. In one step you
can choose any character of `t` and replace it with another character.
Return the minimum number of steps to make `t` an anagram of `s`.

```
s = "bab",      t = "aba"        ->  1    (an a of t replaced by b)
s = "leetcode", t = "practice"   ->  5
s = "anagram",  t = "mangaar"    ->  0
```

**Constraints:** `1 <= s.length <= 5 * 10^4`, `s.length == t.length`,
`s` and `t` consist of lowercase English letters only.

The arms are `fn min_steps(s: Str, t: Str) -> i32`.

## Approaches

| file | mechanism |
|---|---|
| `min_steps.kara` ★ | one count per letter, up for each letter of s and down for each of t; a letter left positive is one t lacks that many times, and each lack takes one step. O(n) |
| `min_steps_map.kara` | a `Map` from each letter of s to how often it appears; each letter of t uses one up if any is left, and a letter with none left is replaced, one step. O(n) |
| `min_steps_sorted.kara` | both words' letters sorted and walked together, a matching letter kept by both; every letter of t not kept is replaced. O(n log n) |
| `min_steps_halves.kara` | each word's letters counted apart; the words are the same length, so the letters t has too many of and those it lacks are equally many, and the answer is half the sum of the differences. O(n) |
| `min_steps_solution.kara` | a Rust solution as LeetCode's Rust users write it (a `[0i32; 26]` counted up through `s.bytes()` and down through `t.bytes()` at `(b - b'a') as usize`, and `cnt.iter().filter(\|&&c\| c > 0).sum()`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 2 lines: LeetCode's three examples; one letter
the same and one different; 5 * 10^4 a's against as many b's, the
constraints' longest; and two random words of that length over the
whole alphabet (`1 5 0 0 1 50000 508`); and 2000 random pairs of 1 to
300 letters, most of them short, over 2, 5 or 26 letters (`2000 random
pairs: 8661 steps in all, checksum 291496410`). `min_steps.py` mirrors
the ★ arm, and its output is byte-identical. Every arm gives the same
output under `karac __mir-run`, `karac run` and `karac __mir-llvm-run`.

The Mend loop: the map and halves arms check clean. The ★ arm was
written with `count[(b - b'a') as i64]`, and `karac check` warns that the
cast is unnecessary, a `u8` widening to `i64` implicitly (W0310,
`lossless_cast`); the arm drops it, as the lint's fix does. The sorted
arm was written as Rust writes it, `s.bytes().collect()` and `let (mut
i, mut j, mut kept) = (0, 0, 0);`; `karac check` says that `bytes()` is
a `Slice[u8]`, whose adaptors need an explicit `.iter()` (E0236), and
that `mut` goes before the whole pattern (E0001), and `karac fix`
applies both, 6 fixes by its count. The Rust solution takes one round of
4 fixes: `struct Solution;` to `struct Solution {}`, `|&&c|` to `|c|`,
and `.to_string()` on each argument where the free function passes its
`Str`s to the method's `String` parameters. Every arm matches on the
first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: a letter of t can stay only if it pairs with an equal letter
of s that no other letter of t has taken, so each letter of t takes the
first such letter of s, and every letter left without one is replaced.
2000 pairs of words of 1 to 10 letters in four kinds, 500 each: over a
and b; over x, y and z, where the rotation below wraps; over the whole
alphabet; and t an anagram of s, the letters of s shuffled, with up to
two of them then changed. Every pair is drawn before any arm answers.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | s and t swapped: the letters t lacks and those it has too many of are equally many, so the same answer |
| P3 | both words' letters moved one place on in the alphabet, z to a: the same answer |
| P4 | s then t against t then s: anagrams already, 0 |
| P5 | t's first letter set to s's first: one letter changed, so within one step of the answer |
| P6 | the ★ arm's answer |

All 60,000 checks pass on every arm: `2000 pairs: checksum 434972692,
60000 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run` and `karac __mir-llvm-run`. Python, summing the letters t has more
of than s, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash, and no two
fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a letter lacking only once not counted | P1 1233, P2 406, P5 244, P6 4932 |
| M2 | ★: each letter t lacks counted once, however often | P1 574, P2 410, P6 2296 |
| M3 | map: a letter of t that matches uses nothing up | P1 781, P2 461, P6 781 |
| M4 | map: the kept letters counted, not the replaced | P1 1861, P4 2000, P6 1861 |
| M5 | sorted: s's letters never sorted | P1 1223, P2 974, P3 343, P4 1813, P6 1223 |
| M6 | sorted: both walks moved on at a mismatch | P1 500, P3 309, P5 130, P6 500 |
| M7 | halves: only the letters s has more of, halved | P1 1600, P6 1600 |
| M8 | halves: z left out of the sum | P1 516, P3 412, P6 516 |
| M9 | solution: a letter of t clears its count | P1 856, P2 461, P5 143, P6 856 |
| M10 | solution: s's first letter never counted | P1 1116, P2 565, P6 1116 |

P1 and P6 kill all ten, P2 six, P3 three, P5 three and P4 two. Swapping
the words (P2) catches the edits that treat s and t differently (M1,
M2, M3, M5, M9, M10); M7 halves what it finds, but what it finds is the
same both ways round, so only the statement catches it. Moving every
letter on (P3) catches the edits that depend on which letters they are:
z left out (M8), and the sorted walk, whose order changes where the
alphabet wraps (M5, M6). Joining the words both ways (P4), a pair of
anagrams of up to 20 letters, catches the kept letters counted (M4) and
s left unsorted (M5). Changing one letter of t (P5) catches the edits
whose answer can jump by more than one step: a lack of one ignored and
then two counted (M1), a walk that loses its place (M6), and a count
wiped by one letter (M9).

## Benchmarks

The bench builds a text of 10^6 random letters once; then answers 1000
queries, each comparing two stretches of it of 40,000 to 50,000 letters,
the constraints' longest or nearly, placed and sized from the checksum
so far, so no answer carries over, with the ★ arm's counts, and folds
the answer plus the query into the checksum. Each language passes the
stretches as views into the text: `text[a..a + len]` in Kāra and Rust, a
pointer and a length in C, a string slice in Go; Python copies them.
Every implementation prints `1000 queries over a text of 10^6: checksum
261967406`.

BENCHTAB
