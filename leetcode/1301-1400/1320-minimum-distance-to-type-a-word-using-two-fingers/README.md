# 1320. Minimum Distance to Type a Word Using Two Fingers

A keyboard lays out the letters `A` to `Z` in rows of six: `A` to `F` in
row 0, `G` to `L` in row 1, and so on, with `Y` and `Z` alone in row 4.
The distance between two keys is the sum of how far apart their rows are
and how far apart their columns are. Given the string `word`, return the
minimum total distance to type it using only two fingers. The first
positions of the two fingers are free, so neither finger's first move
counts, and the two fingers need not start on the first or first two
letters.

```
word = "CAKE"   ->  3
word = "HAPPY"  ->  6
```

**Constraints:** `2 <= word.length <= 300`, `word` consists of upper
case English letters.

The arms are `fn minimum_distance(word: String) -> i64`, or `-> i32` for
the two Rust solutions.

## Approaches

| file | mechanism |
|---|---|
| `minimum_distance.kara` ★ | after each letter one finger is on it, so all that matters is where the other finger is, one of 26 keys or not yet placed; the least distance for each, one row of 27 carried from letter to letter, the next letter typed either by the finger on the last letter or by the other. O(27 n) |
| `minimum_distance_saving.kara` | one finger alone costs the sum of the steps between letters; the other finger can take a letter instead, saving that step at the price of its own move there. `saved[a]` is the most saved with the idle finger on key a; it starts at 0 everywhere, since the idle finger is placed for free, and the answer is the one-finger total less the most saved. O(26 n) |
| `minimum_distance_memo.kara` | top down: the cost of typing the rest of the word from letter i with the fingers on keys l and r (26 for a finger not yet placed) asked of a recursive call, which types letter i with either finger and asks for the rest; each answer remembered in a table of 27 by 27 by n. n calls deep |
| `minimum_distance_table.kara` | bottom up over every state: the least distance after i letters with the fingers on keys l and r, kept in an n + 1 by 27 by 27 `Vec[Vec[Vec[i64]]]`, 26 for a finger not yet placed. O(27² n) |
| `minimum_distance_solution.kara` | a Rust solution as LeetCode's Rust users write it (the letters by `word.bytes().map(\|b\| (b - b'A') as usize)`, a `dist` closure on `usize` keys with 26 for a free finger, and `dp: Vec<Vec<i32>>` over the two fingers, made afresh for each letter with `i32::MAX` for out of reach), carried to Kāra by `karac fix` |
| `minimum_distance_lee.kara` | a second Rust solution as LeetCode's Rust users write it (the saving form: `let mut dp = [0i32; 26];`, a nested `fn d`, each step taking `dp[b] = (0..26).map(\|a\| dp[a] + d(b, c) - d(a, c)).max().unwrap()`, and the one-finger total less `dp.iter().max()`), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, five more properties |

Every arm prints the same 2 lines: LeetCode's two examples, two letters,
one finger each, one letter said over and over, the alphabet, and the two
far corners in turn, 300 letters, the constraints' longest (`3 6 0 0 36
0`); then 400 random words of 2 to 300 letters over 2, 5 or 26 letters
next to each other (`400 random words: distance total 53706, checksum
683814702`). `minimum_distance.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac __mir-run`,
`karac run` and `karac __mir-llvm-run`.

The Mend loop: the four Kāra arms checked clean as first written. The
first Rust arm takes one round of 22 fixes by `karac fix`'s count, from 9
errors: `struct Solution;` to `struct Solution {}`, `Vec<..>` to
`Vec[..]`, `word.bytes().map` to `word.bytes().iter().map`, every `usize`
to `i64`, the closure's `-> i32` dropped, `i32::MAX` to `i32.MAX`,
`vec![vec![..; 27]; 27]` to `Vec.filled(27, Vec.filled(27, ..))`, `for &c
in &w` to `for c in ref w`, `.flatten().copied()` to `.flat_map(|v|
v.iter()).cloned()`, `::` to `.`, and the wrapper's `as i64` dropped, since
an `i32` widens to `i64` by itself. The second takes one round of 9 fixes
from 4 errors: the nested `fn d` moved out to the top level, `let mut
total = 0` declared `i32` where it met the `i32` distances, `(0..26)` to
`(0i32..26)`, and the same rewrites of the struct, `Vec<..>`, `::` and
`as i64`. Both outputs match on the first run.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every way to share the letters between the two fingers tried,
as a bit mask, each finger's distance the sum of its moves from letter to
letter, its first letter free. 2000 words of 2 to 10 letters in four
kinds, 500 each: over 2 letters next to each other, over 5, over `A` to
`X`, and over `A` to `Z`. Every word and extra letter is drawn before any
arm answers.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the word backwards: the same answer |
| P3 | the keyboard's rows `A` to `X` turned upside down, which keeps every distance, for a word without `Y` or `Z`: the same answer |
| P4 | every letter typed twice: the same answer |
| P5 | one more letter at the end: no shorter, and longer by at most the step to it from the last letter |
| P6 | the ★ arm's answer |

All 70,734 checks pass on every arm (P3 asks only the 1789 words without
`Y` or `Z`): `2000 words: checksum 269781487, 70734 checks over 6 arms: 0
failures`, under `karac __mir-run` and `karac __mir-llvm-run`. Python
gives the same checksum and check count.

## Mutation testing

Seventeen edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`. Five are left out: three more that,
like the saving arm's M3, make every answer 0 (the memo arm's left finger
costed from the right finger's key, its right finger left where it was
after typing, and the table's right finger's move written to the left
finger's place); the table's answer read only where the right finger
never moved, which is one finger's total, as M1 gives; and the lee arm's
last step left out, which fails exactly the checks of the table's answer
read a letter early (M7). The twelve kept, two to each arm, are each
killed, fail the same way under both backends and not by a crash, and no
two fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the other finger's move costed as the step from the last letter | P1 1927, P6 9635 |
| M2 | ★: a free finger's first move costed from A | P1 1858, P2 1050, P3 1222, P6 9290 |
| M3 | saving: the idle finger's move never paid for | P1 1256, P6 1256 |
| M4 | saving: the answer less the saving with the idle finger on A | P1 1847, P2 232, P3 399, P4 28, P5 36, P6 1847 |
| M5 | memo: the right finger left out of the memo's key | P1 1244, P6 1244 |
| M6 | memo: the dearer of the two fingers taken | P1 1927, P4 1880, P5 453, P6 1927 |
| M7 | table: the answer read a letter early | P1 1058, P2 788, P4 1058, P5 177, P6 1058 |
| M8 | table: the left finger started on A | P1 1799, P2 772, P3 1304, P6 1799 |
| M9 | solution: a free finger's first move costing 1 | P1 2000, P6 2000 |
| M10 | solution: the row distance read in rows of five | P1 678, P3 651, P5 196, P6 678 |
| M11 | lee: each saving kept under the key just typed, not the one left idle | P1 1324, P2 707, P6 1324 |
| M12 | lee: Z never a key for the idle finger | P1 62, P2 95, P4 1, P6 62 |

P1 and P6 kill all twelve, P2 six, and P3, P4 and P5 four each. Four
edits are caught only by the literal reading and the ★ arm (M1, M3, M5,
M9): each still answers something a reversed word, a flipped board and
doubled letters leave alone, and which one more letter raises by no more
than its step, as one finger's total (M1) and 0 (M3) do. Turning the
board upside down (P3) catches the edits that cost a key by where it
sits rather than by how far it is from another: a free finger's first
move costed from A (M2, M8, and the saving with the idle finger on A,
M4) and rows read as five wide (M10). Typing every letter twice (P4)
catches the edits that let a repeated letter cost something or save
something it should not (M4, M6, M7, M12).

## Benchmarks

The bench builds 100 words of 300 letters, the constraints' longest, over
2, 5 or 26 letters, once; then makes 80 passes, each setting one letter
of every word from the checksum so far, so no answer carries over,
answering it with the ★ arm and folding the answer plus the pass into the
checksum. Each call takes a fresh row for every letter in every language,
a `malloc` in C. Every implementation prints `80 passes over 100 words of
300: checksum 127234723`.

BENCHTAB
