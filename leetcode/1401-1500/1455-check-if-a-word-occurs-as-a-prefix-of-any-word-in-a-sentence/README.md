# 1455. Check If a Word Occurs As a Prefix of Any Word in a Sentence

Given a `sentence` that consists of some words separated by a single
space, and a `searchWord`, check if `searchWord` is a prefix of any word
in `sentence`. Return the index of the word in `sentence` (1-indexed)
where `searchWord` is a prefix of this word. If `searchWord` is a prefix
of more than one word, return the index of the first word (minimum
index). If there is no such word return `-1`. A prefix of a string `s`
is any leading contiguous substring of `s`.

```
sentence = "i love eating burger", searchWord = "burg"            ->  4
sentence = "this problem is an easy problem", searchWord = "pro"  ->  2
sentence = "i am tired", searchWord = "you"                       ->  -1
```

**Constraints:** `1 <= sentence.length <= 100`, `1 <= searchWord.length
<= 10`, `sentence` consists of lowercase English letters and spaces, and
`searchWord` consists of lowercase English letters.

Each arm is `fn is_prefix_of_word(sentence: String, search_word: String)
-> i32`.

## Approaches

| file | mechanism |
|---|---|
| `is_prefix_of_word.kara` ★ | the first word that starts with the search word, `sentence.split(" ").position(\|w\| w.starts_with(search_word))`, counted from 1. O(n) |
| `is_prefix_of_word_scan.kara` | one walk along the sentence's bytes: at each word's start the search word's bytes matched while they last, and the words counted. O(n) |
| `is_prefix_of_word_find.kara` | a space put before the sentence and before the search word, so a match by `find` is a word's start, and the word's number the spaces before the match, `text[..at + 1].matches(" ").count()`. O(n k) |
| `is_prefix_of_word_slices.kara` | each word by `split_whitespace` with its number from `enumerate`, and its first letters compared as a slice, `w[..k] == search_word`, when it has enough. O(n) |
| `is_prefix_of_word_solution.kara` | a Rust solution as LeetCode's Rust users write it (`split(' ')` and `enumerate()`, `find` on the pairs with `starts_with(&search_word)`, then `map(..).unwrap_or(-1)`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 8 lines: LeetCode's three examples and three
more, the search word the whole sentence, longer than every word, and
found only inside a word, a line each (`4`, `2`, `-1`, `1`, `-1`, `-1`);
the constraints' most, a sentence of 99 letters of one-letter words with
the word at the end, and one of words of up to 10 letters searched for
the start of its last word (`100 letters: 50 and 1`); and 2000 random
cases of sentences of up to 1 to 100 letters of words of 1 to 1 to 6
letters, with a search word of 1 to 3 letters, drawn from the first 1 to
3 letters of the alphabet (`2000 random cases: 1366 found, checksum
879975231`). `is_prefix_of_word.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac __mir-run`,
`karac run`, `karac build` and `karac __mir-llvm-run`.

The Mend loop: the ★, find and slices arms check clean as first written.
The scan arm took the bytes by `sentence.as_bytes()`, which `karac
check` refuses, a string's UTF-8 bytes being `.bytes()` in Kāra, and
`karac fix` writes `.bytes()`, 2 fixes. The Rust solution takes one
round of 4 fixes by `karac fix`'s count: `struct Solution;` to `struct
Solution {}`, `split(' ')` to `split(" ")`, `&search_word` to
`search_word`, and `Solution::` to `Solution.`. Every arm's output
matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the words found letter by letter between the spaces, and the
first whose first letters are the search word's, each letter compared in
turn, counted from 1. LeetCode's examples, the three edge cases above,
the constraints' most two ways, and 1992 random cases drawn as the
harness draws them.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the search word put after the sentence as a last word is found there when it is not found before, while the sentence stays within 100 letters |
| P3 | a word before the sentence that starts no search word moves the answer on by one, while the sentence stays within 100 letters |
| P4 | the search word's first letter alone is found no later |
| P5 | the sentence cut after the word found gives the same, and cut after its first word gives -1 when no word is found |
| P6 | the ★ arm's answer |

All 56,290 checks pass on every arm: `2000 cases: checksum 285564321,
56290 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and `karac __mir-llvm-run`. Python, by `str.find` on
the space-led text, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: a word that ends with the search word taken | P1 462, P4 63, P6 1848 |
| M2 | ★: the words counted from 0 | P1 1336, P2 1311, P3 657, P4 220, P5 1336, P6 5344 |
| M3 | scan: a word that matches all but the search word's last letter taken | P1 954, P3 676, P6 954 |
| M4 | scan: the words never counted | P1 673, P2 652, P3 1307, P5 673, P6 673 |
| M5 | find: no space put before the sentence, so the first word is never found | P1 916, P2 714, P3 657, P5 1274, P6 916 |
| M6 | find: the spaces counted before the match's own space | P1 1336, P2 1311, P3 657, P4 220, P5 1336, P6 1336 |
| M7 | slices: a word only as long as the search word passed over | P1 601, P2 992, P6 601 |
| M8 | slices: the words counted from 0 | P1 1336, P2 1311, P3 657, P4 220, P5 1336, P6 1336 |
| M9 | solution: an absent word answered 0, not -1 | P1 664, P3 656, P5 664, P6 664 |
| M10 | solution: 0 where no word is found | P1 664, P3 656, P5 664, P6 664 |

## Benchmarks

The bench draws 2000 sentences of up to 100 letters of words of 1 to 8
letters and 2000 search words of 1 to 4 letters, from the first 4
letters of the alphabet, once, then looks for every search word in every
sentence with the ★ arm, folding the answers to a checksum. Rust splits
lazily as the ★ arm does; Go's `strings.Split` makes the whole list of
words first, and C walks the words between the spaces by `strchr`,
having no library split. Every implementation prints `4 x 10^6 searches:
checksum 828360567`.

BENCHTAB

Measured by hand, best of three on a machine shared with a test run,
Kāra takes 0.59 s against Rust's 0.55 s (0.59 s with overflow checks
on), C's 0.40 s and Go's 1.5 s; Python takes 4.6 s.
