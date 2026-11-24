# 1332. Remove Palindromic Subsequences

You are given a string `s` consisting only of letters `'a'` and `'b'`. In
a single step you can remove one palindromic subsequence from `s`. Return
the minimum number of steps to make the given string empty.

```
s = "ababa"  ->  1
s = "abb"    ->  2
s = "baabb"  ->  2
```

**Constraints:** `1 <= s.length <= 1000`, `s[i]` is either `'a'` or
`'b'`.

The arms are `fn remove_palindrome_sub(s: String) -> i32`.

## Approaches

Every a together is a palindromic subsequence, and so is every b, so two
steps always do, and one does exactly when the whole string is a
palindrome. The arms differ in how they decide that.

| file | mechanism |
|---|---|
| `remove_palindrome_sub.kara` ★ | the string's bytes read from both ends at once, `s.bytes()` indexed in place; the first pair that differs answers 2. O(n) |
| `remove_palindrome_sub_reverse.kara` | the letters collected backwards into a second `String`, and the two strings compared. O(n) |
| `remove_palindrome_sub_longest.kara` | the longest palindromic subsequence of every stretch, by the interval recurrence, one row at a time; one step when the longest covers the whole string. O(n^2) |
| `remove_palindrome_sub_iter.kara` | the bytes forwards zipped with the bytes backwards, and one step when `all` of the pairs agree. O(n) |
| `remove_palindrome_sub_solution.kara` | a Rust solution as LeetCode's Rust users write it (`as_bytes()`, two `usize` ends walked inward from `let (mut i, mut j)`, an early `return 2`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 4 lines: LeetCode's three examples; one and
two letters (`1 1 2 1`); 1000 letters, the constraints' longest, all a,
a palindrome, and that palindrome with its first letter changed (`1000
letters: 1 1 2`); and 600 random strings of 1 to 1000 letters, most of
them short, a third drawn at random, a third palindromes and a third
palindromes with one letter changed (`600 random strings: 277
palindromes, checksum 420621119`). `remove_palindrome_sub.py` mirrors the
★ arm, and its output is byte-identical. Every arm gives the same output
under `karac __mir-run`, `karac run` and `karac __mir-llvm-run`.

The Mend loop: the reverse and longest arms check clean. The ★ arm was
first written with Rust's habit, `let b: Vec[u8] = s.bytes().collect();`,
and `check` refused it: `bytes()` is a byte view, a `Slice`, and an
iterator method on it needs `.iter()` first; `karac fix` wrote
`s.bytes().iter().collect()`, and the arm now indexes the view in place,
with no copy. The iterator arm, written `s.bytes().zip(s.bytes().rev())`,
takes 2 fixes from 3 errors, the same `.iter()` on each side (the third
error, a tuple pattern on an unknown type, follows from the first). The
Rust arm takes one round of 7 fixes from 4 errors: `struct Solution;` to
`struct Solution {}`, `as_bytes()` to `bytes()`, `0usize` to `0`, `let
(mut i, mut j)` to `let mut (i, j)`, and `Solution::` to `Solution.`. Its
output matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: a breadth-first search over the sets of letters left, from
all of them to none, where a step removes any set of the letters left
that reads as a palindrome in order. 2000 strings of 1 to 7 letters in
four kinds, 500 each: letters drawn at random; palindromes; palindromes
with one letter changed; and a run of a then a run of b. Every string is
drawn before any arm answers.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the string read backwards: the same answer |
| P3 | every a made b and every b made a: the same answer |
| P4 | the string followed by itself backwards, a palindrome: one step |
| P5 | every letter doubled: the same answer |
| P6 | the ★ arm's answer |

All 60,000 checks pass on every arm: `2000 strings: checksum 240207232,
60000 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run` and `karac __mir-llvm-run`. Python, searching the same sets, gives
the same checksum and agrees with the palindrome test on every string.

## Mutation testing

Eleven edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`. One is left out: the Rust arm
starting its right end one place in fails exactly as many checks under
every property as the iterator arm starting its forward bytes one place
in (M8). One tests the string less its last letter and the other the
string less its first. Every kind of string here is drawn as often as
its reverse, or, for the runs, as its reverse with a and b swapped, which
is a palindrome exactly when the reverse is, so the counts match property
by property. The ten kept,
two to each arm, are each killed, fail the same way under both backends
and not by a crash, and no two fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the outermost pair never compared | P1 490, P5 490, P6 1960 |
| M2 | ★: the middle pair of an even length never compared | P1 219, P5 219, P6 876 |
| M3 | reverse: the letters collected forwards | P1 937, P6 937 |
| M4 | reverse: the backwards copy one letter short | P1 1063, P4 2000, P6 1063 |
| M5 | longest: a matching pair of ends adding one | P1 800, P4 2000, P5 263, P6 800 |
| M6 | longest: one letter short of the whole taken as a palindrome | P1 708, P5 708, P6 708 |
| M7 | iter: one agreeing pair enough | P1 755, P6 755 |
| M8 | iter: the forwards bytes started one place in | P1 710, P2 464, P4 1274, P5 373, P6 710 |
| M9 | solution: the right end walked in two places at a time | P1 303, P2 183, P4 954, P5 296, P6 303 |
| M10 | solution: the right end never moved | P1 337, P4 1274, P6 337 |

P1 and P6 kill all ten, P5 six, P4 five, P2 two and P3 none. Doubling
every letter (P5) keeps a palindrome a palindrome but moves every pair,
so it catches the edits that skip a pair (M1, M2), take a near miss for a
palindrome (M6), count the longest short (M5), or compare the wrong
places (M8, M9). A string
followed by itself backwards (P4) is always a palindrome of even length,
so it catches every edit that can answer 2 for a palindrome (M4, M5, M8,
M9, M10). Reading backwards (P2) catches only the two edits that walk the
two ends unevenly (M8, M9). Swapping the letters (P3) catches none: no
edit here treats a and b differently.

## Benchmarks

The bench builds 1000 strings of 1000 letters, the constraints' longest,
once: palindromes, half of them with one letter beside the middle
changed, so nearly every answer reads to the middle. Then it makes 500
passes, each setting one letter of one string from the checksum so far,
rebuilding that string, and answering every string with the ★ arm,
folding each answer plus the pass into the checksum. Every implementation
prints `500 passes over 1000 strings of 1000 letters: checksum
560235752`.

BENCHTAB
