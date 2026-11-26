# 1451. Rearrange Words in a Sentence

Given a sentence `text` (a sentence is a string of space-separated
words) in the following format: the first letter is in upper case, and
each word in `text` is separated by a single space. Your task is to
rearrange the words in `text` such that all words are rearranged in an
increasing order of their lengths. If two words have the same length,
arrange them in their original order. Return the new text following the
format shown above.

```
text = "Leetcode is cool"       ->  "Is cool leetcode"
text = "Keep calm and code on"  ->  "On and keep calm code"
text = "To be or not to be"     ->  "To be or to be not"
```

**Constraints:** `text` begins with a capital letter and then contains
lowercase letters and single spaces between words, and `1 <= text.length
<= 10^5`.

Each arm is `fn arrange_words(text: String) -> String`.

## Approaches

| file | mechanism |
|---|---|
| `arrange_words.kara` ★ | the words lowered, sorted by length with ties kept in order by the stable `sort_by_key`, joined, and the first letter raised as `joined[..1].to_uppercase() + ..`. O(n log n) |
| `arrange_words_buckets.kara` | the words dealt into a `Vec[Vec[Str]]` of buckets by length, then read back from the shortest bucket, each bucket in the order its words came, the first letter raised through a `Vec[char]`. O(n) |
| `arrange_words_pairs.kara` | each word keyed by its length and its place, so a plain `sort` of the `(i64, i64, String)` keys keeps words of one length in order. O(n log n) |
| `arrange_words_merge.kara` | a merge sort by length written out, taking from the left half on a tie so words of one length keep their order, the first letter raised through `split_at(1)`. O(n log n) |
| `arrange_words_solution.kara` | a Rust solution as LeetCode's Rust users write it (`split(' ')` and `to_lowercase()` into a `Vec<String>`, `sort_by_key(\|w\| w.len())`, and the first letter raised as `s[..1].to_uppercase() + &s[1..]`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 8 lines: LeetCode's three examples and three
more, one letter, one word, and two words of one length, a line each;
the constraints' most, a text of 50,000 one-letter words and one of
15,000 words of 1 to 10 letters (`10^5 letters: checksum 191344321`);
and 2000 random texts of 1 to 60 words of 1 to 1 to 12 letters (`2000
random texts: checksum 843543285`). `arrange_words.py` mirrors the ★
arm, and its output is byte-identical. Every arm gives the same output
under `karac __mir-run`, `karac run`, `karac build` and `karac
__mir-llvm-run`.

The Mend loop: the pairs arm checks clean as first written. The ★ arm
raised the first letter by `joined[..1].to_uppercase() + joined[1..]`,
which `karac check` refuses, `+` on a `String` taking an owned `String`
and `joined[1..]` being a `Str`, and `karac fix` writes
`joined[1..].to_string()`, 1 fix. The buckets arm read its buckets back
by `buckets.into_iter().flatten()`, which is refused, Kāra's `flatten`
wanting items that are themselves iterators and a `Vec[Str]` being none,
and `karac fix` writes `.flat_map(|v| v.into_iter())`, 1 fix. The merge
arm wrote its two places as `let (mut i, mut j) = (0, 0);`, and `karac
fix` writes `let mut (i, j) = (0, 0);`, 3 fixes by its count. The Rust
solution takes one round of 7 fixes by `karac fix`'s count: `struct
Solution;` to `struct Solution {}`, `Vec<String>` to `Vec[String]`,
`split(' ')` to `split(" ")`, `&s[1..]` to `s[1..].to_string()`, and
`Solution::` to `Solution.`. Every arm's output matches on the first
run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: again and again the first of the words left with the fewest
letters, so words of one length keep their order, then written with
single spaces and the first letter raised, while there are at most 1000
words. LeetCode's examples, the three edge cases above, the constraints'
most two ways, and 1995 random texts drawn as the harness draws them.

| | property |
|---|---|
| P1 | the statement read literally, while there are at most 1000 words |
| P2 | the same words, lowered, in some order |
| P3 | the lengths never fall, and the words of each length come in the order the text has them |
| P4 | the answer rearranged again is itself |
| P5 | as long as the text, the first letter raised and every other lowered |
| P6 | the ★ arm's answer |

All 60,080 checks pass on every arm: `2003 cases: checksum 493903380,
60080 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and `karac __mir-llvm-run`. Python, by sorting the
places by length and place, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: the words sorted by half their length | P1 1480, P3 1481, P6 5924 |
| M2 | ★: the first letter left lowered | P1 2001, P5 2003, P6 8012 |
| M3 | buckets: the words dealt by half their length | P1 1480, P3 1481, P6 1481 |
| M4 | buckets: the first letter lowered, not raised | P1 2001, P5 2003, P6 2003 |
| M5 | pairs: words of one length keyed in the reverse of their order | P1 1832, P3 1833, P4 1833, P6 1833 |
| M6 | pairs: the words joined by commas | P1 1971, P2 1973, P3 1973, P5 1973, P6 1973 |
| M7 | merge: a tie taken from the right half | P1 1832, P3 1833, P4 1833, P6 1833 |
| M8 | merge: the right half's leftover words dropped | P1 1950, P2 1952, P3 1952, P4 1398, P5 1952, P6 1952 |
| M9 | solution: the words sorted by their length modulo 5 | P1 1262, P3 1263, P6 1263 |
| M10 | solution: every letter raised | P1 1992, P5 1994, P6 1994 |

## Benchmarks

The bench draws 200 texts of 15,000 words of 1 to 10 letters, the
constraints' most, and arranges each with the ★ arm, folding its letters
to a checksum. Each implementation sorts with its own library's stable
sort, but C, which has none and sorts by a merge sort written out; Go
lowers the whole text before it splits it. Every implementation prints
`200 texts of 15000 words: checksum 814030169`.

BENCHTAB

Kāra is ahead of Rust here, measured by hand at 0.45 s against Rust's
0.50 to 0.52 s (0.50 to 0.54 s with overflow checks on), C's 0.65 s and
Go's 1.6 s; Python takes 5.9 s.
