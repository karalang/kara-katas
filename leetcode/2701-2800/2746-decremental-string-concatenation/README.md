# 2746. Decremental String Concatenation

You are given a **0-indexed** array `words` containing `n` strings.

Let's define a **join** operation `join(x, y)` between two strings `x`
and `y` as concatenating them into `xy`. However, if the last character
of `x` is equal to the first character of `y`, one of them is
**deleted**.

For example `join("ab", "ba") = "aba"` and `join("ab", "cde") =
"abcde"`.

You are to perform `n - 1` **join** operations. Let `str_0 = words[0]`.
Starting from `i = 1` up to `i = n - 1`, for the `i`-th operation, you
can do one of the following:

- Make `str_i = join(str_{i - 1}, words[i])`
- Make `str_i = join(words[i], str_{i - 1})`

Your task is to **minimize** the length of `str_{n - 1}`.

Return *an integer denoting the minimum possible length of*
`str_{n - 1}`.

```
words = ["aa", "ab", "bc"]   ->  4
words = ["ab", "b"]          ->  2
words = ["aaa", "c", "aba"]  ->  6
```

**Constraints:** `1 <= words.length <= 1000`, `1 <= words[i].length <=
50`, each character in `words[i]` is an English lowercase letter.

## Approaches

Whether a join loses a letter depends only on the string's first and
last letters and the word's, so the 26 by 26 pairs of first and last
letters are the whole state.

| file | mechanism |
|---|---|
| `decremental.kara` ★ | `best[f][l]`, the shortest string so far that starts with f and ends with l, in a 26 by 26 `Array`, rolled word by word with each word put after or before. O(26^2 n) |
| `decremental_backward.kara` | the same pairs filled from the last word back: the fewest letters the words still to come add, in one flat `Vec` of 676 rolled back to the second word; the answer is the first word's length plus its pair's. O(26^2 n) |
| `decremental_memo.kara` | top down from word i with the string's two end letters as `char`s, a `struct Joiner` holding the words and a `Map[(i64, i64, i64), i64]` memo. O(26^2 n) |
| `decremental_reachable.kara` | only the pairs some way of joining reaches, in a `SortedMap[(char, char), i64]` rolled word by word; the answer is the least value left. O(n s log s), s the pairs reached |
| `decremental_solution.kara` | a Rust solution as LeetCode's Rust users write it, a memoized `dfs` threading a `Vec<Vec<Vec<i32>>>` through as `&mut`, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 7 lines: LeetCode's three examples; one word;
1000 words of 50 "a"s, LeetCode's most; 3000 random lists of 1 to 12
words of 1 to 4 letters from the first 1 to 3; and 30 lists of 1000
words of up to 50 letters from the first 5, the last two with the sum
of the answers and a checksum. `decremental.py` mirrors the ★ arm and
its output is byte-identical.

```
4
2
6
3
49001
3000 small lists: lengths sum to 35498, checksum 426970288
30 lists of 1000 words: lengths sum to 750435, checksum 584282486
```

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every choice of each word joined after or before, the strings
themselves built by `join`, a letter dropped where the two ends meet on
the same one, and the shortest kept; nothing assumed about first and
last letters. It draws 1000 random lists of 1 to 10 words of 1 to 4
letters from the first 1 to 3, then 100 of up to 200 words of up to 20
letters from the first 1 to 5, all before any arm answers; the literal
reading is asked only of the first 1000.

| | property |
|---|---|
| P1 | up to 10 words, the answer is the literal reading's |
| P2 | every word reversed: the same answer |
| P3 | every letter moved on 5 places round the alphabet: the same answer |
| P4 | at most all the letters, and at least all of them less one a join |
| P5 | a word "z" put at the end: 1 longer |
| P6 | each arm agrees with at least three of the other four |

The differential prints `1100 cases: checksum 354534285, 33000 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases by the same search gives the same checksum. On
a failure it prints the first ten and then the count by property.

P5 puts the "z" only at the end. Put at the front, it is not always one
longer: the first word then joins "z" and loses its free end, and in 14
of 100 small lists the Python search found a longer answer than that.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends. Every one fails P1 and P6, and P2, the words
reversed, catches all but M3 and M8.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the word after loses a letter on its own last | P1 282, P2 364, P6 358 |
| M2 | ★: the word before priced as the word after | P1 359, P2 488, P6 442 |
| M3 | backward: the second word never joined | P1 698, P4 556, P5 101, P6 792 |
| M4 | backward: a word put before keeps its own last letter | P1 216, P2 307, P6 290 |
| M5 | memo: the memo keyed without the last letter | P1 162, P2 277, P6 234 |
| M6 | memo: a word put before leaves the first letter as it was | P1 190, P2 334, P6 271 |
| M7 | reachable: a later way of reaching a pair overwrites the shorter | P1 319, P2 46, P5 54, P6 404 |
| M8 | reachable: the longest pair's string answered | P1 542, P5 106, P6 627 |
| M9 | solution: only the word after ever kept | P1 453, P2 499, P6 538 |
| M10 | solution: the word before loses a letter on its own first | P1 272, P2 364, P6 348 |

## Benchmarks

The bench draws 100 lists of 1000 words, LeetCode's most, of 1 to 10
letters from all 26, so that most pairs are reached, all of them first,
then answers each 5 times by the ★ arm in all five languages. Every
implementation prints `100 lists of 1000 words, 5 rounds: lengths sum
to 2637635, checksum 36972878`.

BENCHTAB

## Verification

All five arms print the same output as `decremental.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The ★, memo and reachable arms checked clean as first written. The
backward arm gave its closure Rust's return type, `|w: Str| -> (i64,
i64) { .. }`, and `karac fix` took it off.

LeetCode's Rust template took 35 `karac fix` edits, the wrapper
included: `struct Solution {}` added; `Vec<String>` became
`Vec[String]` and the nested `vec![vec![vec![-1; 26]; 26]; n]` became
`Vec.filled(n, Vec.filled(26, Vec.filled(26, -1)))`; `as_bytes()`
became `bytes()`; every `usize` became `i64`; `&Vec<String>` became
`ref Vec[String]` and `&mut Vec<Vec<Vec<i32>>>` became `mut ref
Vec[Vec[Vec[i32]]]`, with `&words` and `&mut memo` at the calls written
`words` and `mut memo`; and `Self::` and `Solution::` became
`Solution.`, with the wrapper's `as i64` dropped.
