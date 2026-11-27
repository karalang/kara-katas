# 1816. Truncate Sentence

A sentence is a list of words separated by a single space, with no
leading or trailing spaces, and each word is made of English letters,
upper or lower case. Given a sentence `s` and an integer `k`, truncate
`s` so that it holds only its first `k` words, and return it.

```
s = "Hello how are you Contestant",          k = 4  ->  "Hello how are you"
s = "What is the solution to this problem",  k = 4  ->  "What is the solution"
s = "chopper is not a tanuki",               k = 5  ->  "chopper is not a tanuki"
```

**Constraints:** `1 <= s.length <= 500`, `k` is in the range `[1, the
number of words in s]`, `s` is made of English letters and spaces, and
its words are separated by a single space.

The arms are `fn truncate_sentence(s: String, k: i64) -> String`.

## Approaches

| file | mechanism |
|---|---|
| `truncate_sentence.kara` ★ | the sentence split at its spaces, the first `k` words taken by `take(k)` and joined again. O(n) |
| `truncate_sentence_scan.kara` | one walk of the chars, counting the spaces met: the `k`-th space ends the `k`-th word, so the chars before it are the answer. O(n) |
| `truncate_sentence_find.kara` | the `k`-th space found by `find` from just past the one before it, and the sentence cut there by its byte offset; with fewer than `k` spaces it is kept whole. O(n) |
| `truncate_sentence_words.kara` | the words gathered by `split_whitespace` into a `Vec`, and the slice of its first `k` joined. O(n) |
| `truncate_sentence_solution.kara` | a Rust solution as LeetCode's Rust users write it (`s.split(' ').take(k as usize).collect::<Vec<&str>>().join(" ")`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 6 lines: LeetCode's three examples, one to a
line; three edges, one word, every word kept, and letters of both cases
(`[a] [ab cd] [Aa]`); the constraints' most, a sentence of 499
characters, 250 words of one letter, cut to 125 words and to all 250
(`the most: 499 249 499`); and 3000 random sentences of 1 to 12 words of
1 to 5 letters, each cut at a random `k` (`3000 random sentences: 41640
characters kept, checksum 402789209`). `truncate_sentence.py` mirrors
the ★ arm, and its output is byte-identical. Every arm gives the same
output under `karac __mir-run`, `karac run`, `karac build` and `karac
__mir-llvm-run`.

The Mend loop: the ★, scan and words arms check clean as first written.
The harness passed `longest.clone()` to the two calls on the longest
sentence; check warns that each copies `longest` for a parameter that
only borrows it, and `karac fix` passed `longest`, 2 fixes. The find arm
returns `s` itself when the sentence has fewer than `k` spaces; a bare
parameter borrows, so check refused giving it away, and `karac fix` made
it `s: own String` and passed the harness's first call
`longest.clone()`, 2 fixes. The Rust solution takes 15 fixes by `karac
fix`'s count, and its diff is: `struct Solution {}` added above the
`impl`; `s.split(' ').take(k as usize).collect::<Vec<&str>>().join(" ")`
to `Vec[Str].from_iter(s.split(" ").take(k)).join(" ")`; and
`Solution::` to `Solution.` at the harness's 9 calls. The solution takes
an `i32` `k`, so its harness passes `k as i32`. Every arm's output
matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: a word is a run of letters between spaces, and the chars are
kept, one at a time, until the `k`-th word has ended. It runs 2000
random sentences of 1 to 12 words of 1 to 5 letters, each with a `k`
from 1 to its words. Each arm meets six properties on each case:

| property | what it checks |
|---|---|
| P1 | the statement read literally |
| P2 | the answer is the start of the sentence |
| P3 | the answer has `k` words |
| P4 | truncating the answer to `k` again changes nothing, and truncating to every word keeps the sentence |
| P5 | the answer for `k` is the start of the answer for `k + 1` |
| P6 | the ★ arm's answer |

It checks clean as first written. All 60,000 checks pass on every arm:
`2000 cases: checksum 789854713, 60000 checks over 5 arms: 0 failures`,
under `karac __mir-run`, `karac run`, `karac build` and `karac
__mir-llvm-run`. Python, cutting the same sentences, gives the same
checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: one word fewer kept | P1 2000, P3 1492, P4 2000, P6 8000 |
| M2 | ★: the words joined with no spaces | P1 1492, P2 1492, P3 1492, P4 1853, P6 5968 |
| M3 | scan: the cut at the space before the k-th | P1 1853, P3 1853, P4 1853, P5 361, P6 1853 |
| M4 | scan: every space dropped | P1 1492, P2 1492, P3 1492, P4 1853, P6 1492 |
| M5 | find: the k-th space kept on the end | P1 1502, P3 1502, P6 1502 |
| M6 | find: each space's offset taken from the last cut, not the start | P1 1394, P3 1276, P4 1655, P5 571, P6 1394 |
| M7 | words: the last k words kept | P1 1501, P2 1501, P5 1501, P6 1501 |
| M8 | words: the words read backwards | P1 1852, P2 1852, P4 1853, P6 1852 |
| M9 | solution: the first word skipped | P1 2000, P2 1851, P3 351, P4 2000, P6 2000 |
| M10 | solution: the sentence split at the letter a | P1 1514, P3 1481, P4 12, P6 1514 |

## Benchmarks

The bench builds 1000 sentences of 20 to 100 words once and makes `2 *
10^6` calls of the ★ arm, each sentence and its `k` drawn from the
checksum so far. The C mirror splits into an array of word starts and
lengths and joins the first `k` into a new string, as `split`, `take`
and `join` do; Go's `strings.SplitN` stops at the `k`-th space as `take`
does. It checks clean as first written. Every implementation prints
`2000000 calls: checksum 297610203`.

BENCHTAB

Measured by hand, best of three on a machine shared with a test run,
Kāra takes 3.0 s against Rust's 2.3 s (2.2 s with overflow checks on),
C's 1.5 s and Go's 2.5 s; Python takes 6.8 s.
