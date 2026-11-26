# 1771. Maximize Palindrome Length From Subsequences

You are given two strings, `word1` and `word2`. You want to construct a
string in the following manner: choose some non-empty subsequence
`subsequence1` from `word1`, choose some non-empty subsequence
`subsequence2` from `word2`, and concatenate the subsequences:
`subsequence1 + subsequence2`, to make the string. Return the length of
the longest palindrome that can be constructed in the described manner.
If no palindromes can be constructed, return `0`. A subsequence of a
string `s` is a string that can be made by deleting some (possibly none)
characters from `s` without changing the order of the remaining
characters. A palindrome is a string that reads the same forward as well
as backward.

```
word1 = "cacb", word2 = "cbba"  ->  5     ("abcba")
word1 = "ab", word2 = "ab"      ->  3     ("aba")
word1 = "aa", word2 = "bb"      ->  0
```

**Constraints:** `1 <= word1.length, word2.length <= 1000`, and `word1`
and `word2` consist of lowercase English letters.

The arms are `fn longest_palindrome(word1: String, word2: String) ->
i32`.

## Approaches

| file | mechanism |
|---|---|
| `longest_palindrome.kara` ★ | the longest palindromic subsequence of every stretch of the two words joined, a table filled from the right; a stretch whose end letters match, one in each word, is a palindrome with letters from both, and the answer is the longest such. O((n1 + n2)^2) |
| `longest_palindrome_rolling.kara` | the ★ arm's table kept as two rows, the row for stretches starting at `i` built from the row for `i + 1`, over the words' `chars()` chained. O((n1 + n2)^2) time, O(n1 + n2) space |
| `longest_palindrome_memo.kara` | top-down: for every pair of matching letters, one in each word, the pair around the longest palindromic subsequence between them, found by recursion with each stretch's answer remembered. O((n1 + n2)^2) |
| `longest_palindrome_outer.kara` | by the outermost pair: for each letter, its first place in `word1` and its last in `word2` leave the most between them, so the answer is the best of 26 lookups in a table of every stretch's longest palindromic subsequence, filled by length, with `position` and `rposition`. O((n1 + n2)^2) |
| `longest_palindrome_solution.kara` | a Rust solution as LeetCode's Rust users write it (`word1.clone() + &word2`, `as_bytes()`, `vec![vec![0; n]; n]`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 4 lines: LeetCode's three examples (`5 3 0`);
five edges, one letter in each word, alike and not, one word the other
reversed, a word of one letter repeated, and the only match at the far
ends (`2 0 6 5 3`); the constraints' most, two words of 1000 a's and
then two of 1000 random letters (`the most: 2000 655`); and 3000 random
pairs of 1 to 15 letters each from the first 2 to 26 of the alphabet
(`3000 random pairs: checksum 279157719`). `longest_palindrome.py`
mirrors the ★ arm, and its output is byte-identical. Every arm gives the
same output under `karac __mir-run`, `karac run`, `karac build` and
`karac __mir-llvm-run`.

The Mend loop: the ★, rolling, memo and outer arms each kept the best
length so far as `let mut best = 0`, raised with `best = best.max(..)`
and returned as the `i32`. Check refused the return as a narrowing,
since a method call does not fix an open literal's type and `best` kept
the default `i64` (design.md §8 Literals), and `karac fix` declared it
`best: i32`, one fix each. The Rust solution takes one round of 9 fixes
by `karac fix`'s count, and its diff is: `struct Solution;` to `struct
Solution {}`, `+ &word2` to `+ ref word2`, `as_bytes()` to `bytes()`,
`vec![vec![0; n]; n]` to `Vec.filled(n, Vec.filled(n, 0i32))`, `let mut
ans = 0` to `let mut ans: i32 = 0`, `&&` to `and`, and `Solution::` to
`Solution.`. Every arm's output matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every choice of letters from the two words joined, with at
least one from each word, kept where it reads the same both ways, and
the longest such length. LeetCode's examples, the edges, and 1992 random
pairs of 1 to 6 letters each from the first 1 to 8 of the alphabet. Each
arm meets six properties on each case:

| property | what it checks |
|---|---|
| P1 | the statement read literally |
| P2 | 0 exactly when the words share no letter, and otherwise from 2 to the two words' letters together |
| P3 | the words swapped, each reversed, give the same length |
| P4 | the letters rotated one on in the alphabet give the same length |
| P5 | one letter put before `word1` and after `word2` adds at least 2 |
| P6 | the ★ arm's answer |

P2 first asked whether the words share a letter as `word2.contains(c)`
with `c` a `char`; check refused it, since `contains` takes a `Str`
pattern (docs/library/strings.md), and `karac fix` wrote
`c.to_string()`. The same round dropped two `as i64` casts the
`lossless_cast` lint found widening implicitly. All 60,000 checks pass
on every arm: `2000 cases: checksum 291963981, 60000 checks over 5 arms:
0 failures`, under `karac __mir-run`, `karac run`, `karac build` and
`karac __mir-llvm-run`. Python, trying every choice of letters, gives
the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: a matching pair counted as one letter | P1 1632, P2 92, P5 1607, P6 6528 |
| M2 | ★: a stretch inside one word counted | P1 280, P2 239, P6 1120 |
| M3 | rolling: a mismatch's shorter stretch only from below | P1 269, P3 421, P5 513, P6 269 |
| M4 | rolling: a single letter not a palindrome | P1 1019, P6 1019 |
| M5 | memo: a single letter not a palindrome | P1 1019, P6 1019 |
| M6 | memo: word2's first letter never an end | P1 331, P2 314, P3 480, P6 331 |
| M7 | outer: each letter's last place in word1 taken, not its first | P1 548, P3 612, P6 548 |
| M8 | outer: the stretch between the pair one letter short | P1 829, P3 439, P5 314, P6 829 |
| M9 | solution: a mismatch's shorter stretch only from the left | P1 282, P3 421, P5 515, P6 282 |
| M10 | solution: the answer started at 1 | P1 368, P2 368, P6 368 |

## Benchmarks

The bench builds 100 words of 1000 letters once, each from its own first
2 to 26 letters of the alphabet, and makes 40 calls of the ★ arm, each
on a pair chosen from the checksum so far. Every implementation prints
`40 calls over 100 words: checksum 395394966`.

BENCHTAB

Measured by hand, best of three on a machine shared with a test run,
Kāra is ahead of Rust here at 0.23 s against Rust's 0.49 s (0.42 s with
overflow checks on), C's 0.41 s and Go's 0.44 s; Python takes 11.5 s.
