# 1307. Verbal Arithmetic Puzzle

Given an equation, represented by `words` on the left side and the
`result` on the right side, you need to check if the equation is solvable
under the following rules:

- Each character is decoded as one digit (0 - 9).
- No two characters can map to the same digit.
- Each `words[i]` and `result` are decoded as one number **without**
  leading zeros.
- Sum of numbers on the left side (`words`) will equal to the number on
  the right side (`result`).

Return `true` if the equation is solvable, otherwise return `false`.

```
words = ["SEND","MORE"], result = "MONEY"          ->  true
words = ["SIX","SEVEN","SEVEN"], result = "TWENTY" ->  true
words = ["LEET","CODE"], result = "POINT"          ->  false
```

**Constraints:** `2 <= words.length <= 5`, `1 <= words[i].length,
result.length <= 7`, `words[i]` and `result` contain only uppercase
English letters, and the number of different characters used in the
expression is at most 10.

The arms are `fn is_solvable(words: Vec[String], result: String) ->
bool`.

## Approaches

A one-letter word may be 0; only a number of more than one digit has a
first digit that may not be.

| file | mechanism |
|---|---|
| `is_solvable.kara` ★ | the sum done by hand, a column at a time from the right with its carry: the letters of each column given a digit as they are met, and the result's letter in that column fixed by the column's sum, so that a wrong guess fails in its own column; a word longer than the result refused at once. O(10!) at worst, far less in practice |
| `is_solvable_bound.kara` | the puzzle as one sum, each letter weighed by the place values it stands at, plus in the words and minus in the result, so that a solution makes the weighted digits add up to 0; the letters tried heaviest first, and a branch dropped once the letters still free could no longer bring the sum back to 0, even ignoring that their digits must differ |
| `is_solvable_modular.kara` | the same weighted sum, but the letters taken in the order they first appear reading the columns from the right; once every letter of the rightmost k columns has a digit, the sum so far must already end in k zeros, since the letters still free only add multiples of `10^k` |
| `is_solvable_solution.kara` | a Rust solution as LeetCode's Rust users write it (each letter's weight summed in a `HashMap<u8, i64>` through `*weight.entry(c).or_insert(0) += p`, the letters sorted heaviest first by `sort_by_key(\|&(_, w)\| -w.abs())`, and a `fn dfs` nested in the method trying every free digit for each letter, the sum checked only at the end), carried to Kāra by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, five more properties |

Every arm prints the same 2 lines: LeetCode's three examples, a
one-letter word that is 0 (`A + B = A`), a result shorter than a word, a
letter on both sides (`A + A = B`), and two words whose first letters may
not be 0 (`AB + BA = CC`) (`true true false true false true true`); then
600 random puzzles, half of them a true sum of 2 to 4 numbers of 1 to 3
digits written with a letter for each digit, no more than 6, and half 2
to 4 words over 2 to 5 letters with a result of random letters (`600
random puzzles: 335 solvable, checksum 32623508`). `is_solvable.py`
mirrors the ★ arm, and its output is byte-identical. Every arm gives the
same output under `karac __mir-run`, `karac run` and `karac
__mir-llvm-run`. The Rust arm, which checks the sum only once every
letter has a digit, takes about 21 s under `karac __mir-run`.

The Mend loop: the three Kāra arms checked clean as first written. The
Rust arm takes one round of 46 fixes by `karac fix`'s count, from 20
errors: the `use std::collections::HashMap;` line deleted, since `Map` is
in Kāra's prelude, `HashMap<..>` and `HashMap::new` to `Map[..]` and
`Map.new`, `struct Solution;` to `struct Solution {}`, `Vec<..>` to
`Vec[..]`, `[bool; 26]` to `Array[bool, 26]`, the nested `fn dfs` moved
out of the method to the top level, its `&` and `&mut` parameters to
`ref` and `mut ref` and the `&` and `&mut` at its calls to nothing and
`mut`, `for w in &words` to `for w in ref words`, `as_bytes()` to
`bytes()`, `|&(_, w)|` and `for &c` to `|(_, w)|` and `for c`, `||` and
`&&` to `or` and `and`, and the `as usize` and `as i64` casts dropped, with
`1i64` to `1`. Its output matches on the first run. No
gap was met.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every way to give the letters, from the first, different
digits, true when one decodes every word and the result with no leading
zero and the words add up to the result. 2000 puzzles of 2 or 3 words in
four kinds, 500 each: a true sum of numbers of 1 or 2 digits written with
a letter for each digit it uses, no more than 4; and random words of 1 to
3 letters with a result of 1 to 3 letters over 2, 3 and 4 letters. Every
puzzle, renaming and longer word is drawn before any arm answers.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the words in the reverse order: the same answer |
| P3 | the letters renamed one for one, each moved the same number of places round A to J: the same answer |
| P4 | a puzzle written from a true sum: true |
| P5 | one more word, a letter longer than the result: false |
| P6 | the ★ arm's answer |

All 42,000 checks pass on every arm: `2000 puzzles: checksum 221054757,
42000 checks over 4 arms: 0 failures`, under `karac __mir-run` and
`karac __mir-llvm-run`. Python gives the same checksum. The run takes
about 56 s under `karac __mir-run`.

## Mutation testing

Eleven edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`. One is left out: the Rust arm
never freeing a digit once tried fails a different number of checks on
every run, under either backend, since which digits it leaves held depends
on the order the `Map` hands the letters over, which is random per
process. The ten kept, two or three to each arm, are each killed, fail the
same way under both backends and not by a crash, and no two fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a carry out of the last column let through | P1 47, P6 141 |
| M2 | ★: the result's first letter allowed 0 | P1 13, P6 39 |
| M3 | ★: a word longer than the result let through | P1 354, P5 315, P6 1062 |
| M4 | bounding: a branch dropped when it can just reach 0 | P1 221, P4 173, P6 221 |
| M5 | bounding: leading letters allowed 0 | P1 4, P6 4 |
| M6 | modular: each finished column asked for one zero too many | P1 276, P4 203, P6 276 |
| M7 | modular: the first word taken for the result | P1 551, P2 461, P4 308, P5 91, P6 551 |
| M8 | solution: the result's weights added | P1 699, P4 499, P6 699 |
| M9 | solution: a letter's digit taken from 1 to 9 only | P1 128, P4 78, P6 128 |
| M10 | solution: a word as long as the result refused | P1 534, P4 355, P6 534 |

P1 and P6 kill all ten, P4 six, P5 two and P2 one; P3 kills none. A
puzzle written from a true sum (P4) can only catch an edit that refuses a
solution, so it sees the six that do (M4, M6, M7, M8, M9, M10) and none of
the four that let a wrong one through (M1, M2, M3, M5). A word longer than
the result (P5) can never be balanced, its first digit not being 0; the ★
and Rust arms refuse it at once, and M3 deletes the ★ arm's check, while M7
reads the puzzle with another word as the result. Only M7 cares
which word comes where (P2). Every arm treats a letter as a name and
nothing more, and a renaming keeps which letters lead, so no edit sees P3.

## Benchmarks

The bench makes 40 passes of 50 puzzles, each pass's puzzles drawn from a
generator seeded by the checksum so far, so no answer carries over: 2 to 5
numbers of 1 to 6 digits and their sum, written with the ten letters A to
J shuffled for the ten digits, and every other puzzle's result with one
letter changed; it answers each with the ★ arm and folds the count of
solvable puzzles plus the pass into the checksum. Every implementation
prints `40 passes of 50 puzzles: checksum 955604306`.

BENCHTAB
