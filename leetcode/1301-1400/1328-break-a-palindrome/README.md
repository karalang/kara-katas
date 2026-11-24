# 1328. Break a Palindrome

Given a palindromic string of lowercase English letters `palindrome`,
replace exactly one character with any lowercase English letter so that
the resulting string is not a palindrome and that it is the
lexicographically smallest one possible. Return the resulting string. If
there is no way to replace a character to make it not a palindrome,
return an empty string.

```
palindrome = "abccba"  ->  "aaccba"
palindrome = "a"       ->  ""
```

**Constraints:** `1 <= palindrome.length <= 1000`, `palindrome` consists
of only lowercase English letters.

The arms are `fn break_palindrome(palindrome: String) -> String`.

## Approaches

| file | mechanism |
|---|---|
| `break_palindrome.kara` ★ | the letters into a `Vec[char]`; the first letter of the first half that is not an a made an a, or, when the first half is all a, the last letter made a b; one letter cannot be broken. O(n) |
| `break_palindrome_every.kara` | every place tried with every letter other than the one there, and the smallest of the results that are not palindromes kept. O(26 n^2) |
| `break_palindrome_slices.kara` | the first half, a `Str` view, searched for a letter that is not an a, and the answer put together from the text's slices around the one changed letter. O(n) |
| `break_palindrome_solution.kara` | a Rust solution as LeetCode's Rust users write it (the text taken apart with `into_bytes()`, the first half searched by index for a byte other than `b'a'`, the bytes made back into text with `String::from_utf8(s).unwrap()`), carried to Kāra by `karac fix` |
| `break_palindrome_position.kara` | a second Rust solution as LeetCode's Rust users write it (a `Vec<char>`, the first half's slice searched with `iter().position(\|&c\| c != 'a')`, a `match` on the place found, the chars collected back into a `String`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 2 lines: LeetCode's two examples; two of one
letter; a middle letter, which changes nothing when changed; a first half
with no a; a first half of nothing but a around a middle b; and 1000 of
a, the constraints' longest, whose answer ends in b (`[aaccba] [] [ab]
[abb] [azz] [aabab] 1000 true`); then 600 random palindromes of 1 to 200
letters, most of them short, over a alone, a and b, or all 26 letters
(`600 random palindromes: 40 left unbroken, checksum 50087877`).
`break_palindrome.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac __mir-run`,
`karac run` and `karac __mir-llvm-run`.

The Mend loop: the ★ and every arms check clean. The first Rust arm
takes one round of 6 fixes by `karac fix`'s count, from 5 errors:
`struct Solution;` to `struct Solution {}`, each `::` path to `.`, and
`into_bytes()` to `bytes().to_vec()`. The second takes one round of 5
fixes from 4 errors: the same `struct` and `::` rewrites, `Vec<char>` to
`Vec[char]`, and `|&c|` to `|c|`. Both outputs match on the first run.

The slices arm was written with Rust's habits: four `&` before slices,
which `karac fix` drops (a Kāra slice is already a view), and the search
as Rust writes it, `half.find(|c: char| c != 'a')`. `check` refused that
with only "'find' takes a `Str` pattern, found 'Fn(char) -> bool'" and no
fix (kara B-2026-11-24-42): the fix to `char_indices().find(..).map(|(i, _)| i)`
reached a `String` receiver with an unannotated closure, and `half` is a
`Str` view whose parameter is annotated. Since that row's fix, `karac fix`
writes `half.char_indices().find(|(_, c)| c != 'a').map(|(i, _)| i)`,
which is the arm as committed.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every one letter put in place of every other letter, the
results that do not read the same backwards kept, and the smallest of
them, or the empty string when none is kept. 2000 palindromes of 1 to 9
letters in four kinds, 500 each, over a alone, a and b, a to c, and all
26 letters. Every palindrome is drawn before any arm answers.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | one letter changed, the length kept; nothing for a single letter |
| P3 | what comes back does not read the same backwards |
| P4 | the palindrome between two z: its first z becomes an a |
| P5 | the palindrome between two a: the same change one place on, or, when the first half was all a, the last a made a b |
| P6 | the ★ arm's answer |

All 60,000 checks pass on every arm: `2000 palindromes: checksum
344581844, 60000 checks over 5 arms: 0 failures`, under `karac
__mir-run` and `karac __mir-llvm-run`. Python, trying every change, gives
the same checksum.

## Mutation testing

Fifteen edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`. Three are left out: the ★ arm
trying the middle letter of an odd length fails the same checks as the
position arm searching the middle letter too (M11), apart from P6, which
fails four times as often when the ★ arm is the one edited; and the
position arm refusing two letters, then making the last letter a c, fail
exactly the checks of the slices arm's M7 and M8. The twelve kept, two or
three to each arm, are each killed, fail the same way under both backends
and not by a crash, and no two fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the mirror letter made an a | P1 1180, P4 2000, P6 4720 |
| M2 | ★: a single letter changed rather than refused | P1 216, P2 216, P6 864 |
| M3 | ★: a b left as it is | P1 535, P2 321, P3 321, P6 2140 |
| M4 | every: the largest change kept | P1 1784, P4 2000, P5 2000, P6 1784 |
| M5 | every: the outermost pair never compared | P1 1572, P2 464, P3 464, P4 2000, P5 1788, P6 1572 |
| M6 | slices: the changed letter kept beside its a | P1 1180, P2 1180, P4 2000, P6 1180 |
| M7 | slices: two letters refused | P1 220, P2 220, P3 220, P5 220, P6 220 |
| M8 | slices: the first letter made a b | P1 604, P5 820, P6 604 |
| M9 | solution: the middle letter made a b | P1 498, P2 33, P3 280, P5 322, P6 498 |
| M10 | solution: the first letter never tried | P1 968, P2 160, P3 160, P4 2000, P5 968, P6 968 |
| M11 | position: the middle letter searched too | P1 46, P3 46, P5 116, P6 46 |
| M12 | position: the first letter not an a made a b | P1 1180, P2 535, P3 535, P4 2000, P5 388, P6 1180 |

P1 and P6 kill all twelve, P2 and P5 eight each, P3 seven and P4 six.
Wrapping the palindrome in z (P4) catches every edit that changes the
wrong letter or keeps the wrong answer, since its answer is fixed by its
first letter: the mirror letter (M1), the largest change (M4), a letter
kept beside its a (M6). Wrapping it in a (P5) moves the first letter that
is not an a one place on and catches the edits that go wrong at the
middle or the ends: the middle letter tried (M11), the first letter made
a b (M8). A mirror letter changed in place of its twin (M1) keeps one
letter changed and the result unbalanced, so P2 and P3 cannot see it.

## Benchmarks

The bench builds 20 palindromes of `10^5` letters once, in four kinds:
all a; a until the last tenth of the half, then random letters; a with a
rare b; and random letters. Then it makes 800 passes, each setting one
mirrored pair of every palindrome from the checksum so far to a or b, so
no answer carries over, answering it with the ★ arm and folding two of
the answer's letters plus the pass into the checksum. Each call copies its
input into a fresh `String` and takes a fresh array of chars and a fresh
answer in every language. Every implementation prints `800 passes over 20
palindromes of 10^5: checksum 576310614`.

BENCHTAB
