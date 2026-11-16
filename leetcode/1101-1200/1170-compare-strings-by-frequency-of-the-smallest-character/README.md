# 1170. Compare Strings by Frequency of the Smallest Character

Let the function `f(s)` be the frequency of the lexicographically smallest
character in a non-empty string `s`. For example, if `s = "dcce"` then
`f(s) = 2` because the lexicographically smallest character is `'c'`,
which has a frequency of 2.

You are given an array of strings `words` and another array of query
strings `queries`. For each query `queries[i]`, count the number of words
in `words` such that `f(queries[i]) < f(W)` for each `W` in `words`.

Return an integer array `answer`, where each `answer[i]` is the answer to
the `i`th query.

```
queries = ["cbd"], words = ["zaaaz"]                          ->  [1]
queries = ["bbb","cc"], words = ["a","aa","aaa","aaaa"]       ->  [1,2]
```

**Constraints:** `1 <= queries.length <= 2000`; `1 <= words.length <=
2000`; `1 <= queries[i].length, words[i].length <= 10`; `queries[i][j]`
and `words[i][j]` consist of lowercase English letters.

The arms are `fn num_smaller_by_frequency(queries: Vec[String], words:
Vec[String]) -> Vec[i64]`.

## Approaches

A string of at most 10 letters has a frequency from 1 to 10, so the arms
differ in how they find each string's frequency and in how they count the
words above a query's.

| file | mechanism |
|---|---|
| `compare_strings.kara` ★ | counts by frequency: each frequency found in one pass over the bytes, the smallest so far and its count; the words counted by frequency in a fixed `[0; 12]`, the counts summed from the top down, and each query answered by one look-up. O(total letters + 10) |
| `compare_strings_pairs.kara` | every pair: each frequency found with `bytes().iter().min()` and `filter(..).count()`, once per string, and every query compared with every word. O(total letters + queries x words) |
| `compare_strings_sorted.kara` | sorted frequencies: each string's letters tallied in 26 counters and the first counter above zero taken; the words' frequencies sorted and each query answered with `partition_point`, a binary search for the first frequency above its own. O(total letters + (queries + words) log words) |
| `compare_strings_tree.kara` | a sorted map: each frequency found with `chars().min()` and a count over `chars()`; the words counted by frequency in a `SortedMap[i64, i64]`, and each query answered by summing its `range` of frequencies above its own. O(total letters + words log words + queries x 10) |
| `compare_strings_solution.kara` | a Rust solution as LeetCode's Rust users write it (`impl Solution` with a nested `fn f(s: &str) -> i32` taking `chars().min()` and counting it with `filter(\|&c\| c == min)`, the frequencies sorted with `sort_unstable`, each query answered with `partition_point`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's two examples; an equal
frequency not counted (`ab aab / ba bba zz -> [1, 0]`); ten of one letter,
the most, which no word exceeds; the smallest letter last, first, and
twice apart (`zzza azzz zaza`); then 300 random lists of 1 to 50 queries
and 1 to 50 words of 1 to 10 letters, half over the first three letters so
that the smallest one repeats, half over all 26 (`300 random lists: total
46133, checksum 778495680`); and three lists of 2000 queries and 2000
words, the constraints' most, over 2, 5 and 26 letters.
`compare_strings.py` mirrors the ★ arm and its output is byte-identical;
with `lit` it reads the statement literally, `s.count(min(s))` for each
string and every query against every word, and gives the same output.
Every arm gives the same output under `karac run` and `karac build`.

The Mend loop: the harness takes one fix in every arm, `'a' as u8` to
`b'a'`. Beside it, the pairs arm takes `let mut out = []` to
`Vec.new()`; the ★, sorted and tree arms none. The Rust arm takes one
round of 16 edits: the generics to brackets, `&str` to `Str`, the `|&c|`
and `|&x|` patterns to `|c|` and `|x|`, the nested `fn f` moved out of
`num_smaller_by_frequency` to the top level, `struct Solution {}`,
`sort_unstable()` to `sort()`, and the harness's fix. Its output matches
on the first run.

The differential takes one round of 4 edits: the `-> i64` and `->
String` written on two closures dropped, since a Kāra closure's return
type is inferred; `c.letter_to[(b - b'a') as i64]` to `c.letter_to[b -
b'a']`, since a `u8` index needs no cast; and `let mut draw` to `let
draw`, since the closure is never written. Before kara `88d7d6ee97` the
index's fix kept the parentheses, `c.letter_to[(b - b'a')]` (kara
B-2026-11-15-50).

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: each string's smallest character found and counted, and every
query compared with every word. It checks 600 lists in four kinds of
150: 1 to 10 queries and 1 to 10 words over two letters; 1 to 40 of each
over three; 30 to 120 of each over all 26; and 1 to 40 of each made to a
frequency from 1 to 10, the smallest letter that many times and larger
ones after it, shuffled, so that equal frequencies and the most, 10, are
common. Every random choice the properties make is drawn before any arm
answers.

| | property |
|---|---|
| P1 | the answer is the literal one |
| P2 | the queries in another order answer in that order; the words in another order change nothing |
| P3 | each string's letters in another order change nothing |
| P4 | every letter renamed by a map that keeps their order changes nothing |
| P5 | every word given twice doubles every answer |
| P6 | a word of ten equal letters adds at most one to each answer, and one to the answer of each query under ten letters; a word of one letter changes nothing |

All 18,000 checks pass on every arm: `600 lists: checksum 41485542, 18000
checks over 5 arms: 0 failures`, in 24 s under `karac __mir-run`, and the
same under `karac __mir-llvm-run` and `karac build`. A Python reading of
the same draws, with the mirror against the literal reading, gives the
same checksum.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run` with `KARAC_HASH_SEED=1`,
each failing the same way under both. All fifteen are caught.

| # | mutation | failures by property |
|---|---|---|
| B1 | ★: a smaller letter adds to the count instead of restarting it | P1 566, P3 570 |
| B2 | ★: words of the query's own frequency counted | P1 584, P6 532 |
| B3 | ★: each repeat of the smallest letter restarts the count | P1 590, P6 598 |
| P1 | pairs: equal frequencies counted | P1 584, P6 532 |
| P2 | pairs: the largest letter counted | P1 587 |
| P3 | pairs: the other letters counted | P1 592, P6 598 |
| S1 | sorted: equal frequencies counted | P1 584, P6 532 |
| S2 | sorted: the frequencies left unsorted | P1 540, P2 497, P5 482, P6 523 |
| S3 | sorted: the first letter that comes twice taken | P1 494 |
| T1 | tree: a frequency of 10 left out | P1 119, P6 598 |
| T2 | tree: equal frequencies counted | P1 584, P6 532 |
| T3 | tree: the first word of each frequency counted twice | P1 590, P5 590, P6 481 |
| X1 | solution: equal frequencies counted | P1 584, P6 532 |
| X2 | solution: the frequencies left unsorted | P1 540, P2 497, P5 482, P6 523 |
| X3 | solution: the search's test turned around | P1 570, P6 599 |

P2 and S3 are caught by P1 alone. Counting the largest letter, or the
first letter that comes twice, gives a frequency that every property but
P1 leaves unchanged: no shuffle, order-keeping renaming, doubling or added
word tells the smallest letter from the largest. The literal reading is
the only check on which letter is counted.

## Benchmarks

`bench/` times the ★ arm against the same counting in C, Rust, Go and
Python. 16 lists of 2000 queries and 2000 words, the constraints' most,
over 2, 3, 5 or 26 letters, are built once; each of 300 rounds gives one
query and one word of every list new letters and answers every query.
Every program prints `300 rounds over 16 lists of 2000 queries and 2000
words: total 5564057039, checksum 249789002`.

Timings on a 4-core container (Intel Xeon, 2.3 GHz), twelve interleaved
runs of each compiled program and two of Python, with karac
`1bebe70be8` on LLVM 22. karac builds for the x86-64-v3 baseline, so the
C and overflow-checked Rust programs are also built at
`-march=x86-64-v3`:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 0.519 to 0.565 s | 0.543 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.516 to 0.630 s | 0.552 s |
| Rust (`rustc -O`) | 0.260 to 0.390 s | 0.279 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.500 to 0.588 s | 0.515 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.484 to 0.713 s | 0.518 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.229 to 0.297 s | 0.248 s |
| C (`clang -O3`) | 0.233 to 0.297 s | 0.248 s |
| Go | 0.522 to 0.595 s | 0.543 s |
| Python | 6.6 to 6.9 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane; user time equals wall time for both Kāra rows, so
both ran on one core. Kāra takes about 1.07x overflow-checked Rust's
time, the equal-safety comparison, and the same as Go. Overflow checks
cost Rust 1.85x here: most of the work is the checksum's `check * 131 +
x + 1` and the generator's multiply, each checked, beside a ten-byte
scan per string. C takes about 0.45x Kāra's time: its strings are fixed
`char[11]` arrays rewritten in place, where Kāra, Rust and Go allocate a
new string for each changed query and word and a new answer vector on
every call. These causes are read from the programs, not profiled.
Python takes about 12x.
