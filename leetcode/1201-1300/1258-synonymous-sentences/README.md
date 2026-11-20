# 1258. Synonymous Sentences

You are given a list of equivalent string pairs `synonyms` where
`synonyms[i] = [si, ti]` indicates that `si` and `ti` are equivalent
strings. You are also given a sentence `text`.

Return all possible synonymous sentences sorted lexicographically.

```
synonyms = [["happy","joy"],["sad","sorrow"],["joy","cheerful"]]
text = "I am happy today but was sad yesterday"
  ->  ["I am cheerful today but was sad yesterday",
       "I am cheerful today but was sorrow yesterday",
       "I am happy today but was sad yesterday",
       "I am happy today but was sorrow yesterday",
       "I am joy today but was sad yesterday",
       "I am joy today but was sorrow yesterday"]
synonyms = [["happy","joy"],["cheerful","glad"]]
text = "I am happy today but was sad yesterday"
  ->  ["I am happy today but was sad yesterday",
       "I am joy today but was sad yesterday"]
```

**Constraints:** `0 <= synonyms.length <= 10`; `synonyms[i].length ==
2`; `1 <= si.length, ti.length <= 10`; `si != ti`; `text` consists of at
most 10 words; all the pairs of `synonyms` are unique; the words of
`text` are separated by single spaces.

The arms are `fn generate_sentences(synonyms: Vec[Vec[String]], text:
Str) -> Vec[String]`.

## Approaches

| file | mechanism |
|---|---|
| `synonymous_sentences.kara` ★ | by union-find: each word of a pair joined to its group's root in a `Map[String, String]`, the groups' words listed and sorted, every sentence built word by word by a recursive search, and the sentences sorted |
| `synonymous_sentences_bfs.kara` | by breadth-first search over sentences: from the text, every sentence one word's direct synonym away is queued once, the sentences met kept in a `Set`, and at the end listed and sorted. A sentence is split into a `Vec[Str]` of views, and a neighbour made by writing one view in a copy |
| `synonymous_sentences_product.kara` | by products: each word's synonyms found by a depth-first search over the pairs as a graph, sorted, and the sentences grown a word at a time; choices taken in sorted order give the sentences in sorted order with no sort at the end, as a space sorts before every letter |
| `synonymous_sentences_sorted.kara` | into a `SortedSet`: each word's synonyms grown to a fixed point by passes over the pairs, with no graph, and every sentence built by recursion into a `SortedSet`, which keeps them in order |
| `synonymous_sentences_solution.kara` | a Rust solution as LeetCode's Rust users write it (`HashMap` and `HashSet`, `entry().or_default()`, `Self::dfs` with `&mut` accumulators), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 10 lines: LeetCode's two examples; 400 random
cases (`400 random cases: 67226 sentences, checksum 275014359`); and the
constraints' top, 10 pairs making two groups of 6 words and a text of 10
words, 4 of them in the groups (`1296 sentences, checksum 515388754,
...`). `synonymous_sentences.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac run` and
`karac build`, and under the AddressSanitizer build, with the fix for
B-2026-11-19-140 below.

The Mend loop: the ★, product and sorted arms checked clean as first
written. The BFS arm was written `changed[i] = other;`, a `ref String`
from the synonym list into a `Vec[Str]` slot; the check said only
"expected 'Str', found 'ref String'", with no fix (B-2026-11-20-82, fixed
at FIX2011: it now names `.as_str()`, and `karac fix` adds it). The
solution arm takes one round of 64 fixes by `karac fix`'s count: the
`use std::collections` line dropped, `HashMap` and `HashSet` to `Map` and
`Set`, `or_default()` to `or_insert(Vec.new())`, `vec![]` to `Vec.new()`
and `[..]`, `&` and `&mut` parameters and arguments to Kāra's borrows,
`for s in &synonyms` to `for s in ref synonyms`, `Self::` to `Self.`,
`usize` to `i64`, and the rest of Rust's spelling.

## Gaps

Two gaps were met; both are fixed now.

- **A write of a new view through a `mut ref` was lost in compiled code**
  (B-2026-11-19-140, fixed at FIX140). The BFS arm's `changed[i] =
  other.as_str()` replaces one `Str` in a `Vec[Str]`; under `karac
  __mir-run` it did, and under `karac run`, `karac build` and the
  AddressSanitizer build the element kept its old view, and the arm's
  sentences came out wrong. The backend laid out a `mut ref` to a `Str` or a
  `Slice` as the view itself, two words, rather than as a pointer to it,
  and a write through it went to a copy; it is a pointer now, and a
  write through `mut ref Str`, into a `Vec[Str]` element, and into a
  `Slice` element all land.
- **A borrowed `String` into a `Str` slot** (B-2026-11-20-82, fixed at
  FIX2011), above.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: two words are synonyms when a chain of pairs joins them, a
word being its own synonym (closed by Floyd-Warshall over a table); the
sentences are every text of the same length with each word replaced by
one of its synonyms, enumerated position by position as an odometer,
sorted, and without repeats. 2000 random cases: up to 6 pairs among 5
words from `a` to `f`, and a text of 1 to 6 words, at most 3 of them
from the pairs' words.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | sorted, without repeats, and holding the text |
| P3 | each pair and the pairs' order reversed: the same sentences |
| P4 | the last sentence as the text: the same sentences |
| P5 | every word given a prefix: the same sentences with it |
| P6 | the ★ arm's sentences |

All 60,000 checks pass on every arm: `2000 cases: checksum 497876801,
60000 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and the AddressSanitizer build. Python gives the same
checksum.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac run`, nine failing the same way under both.

| # | mutation | failures by property |
|---|---|---|
| S1 | ★: a pair joins its first word, not that word's root | P1 394, P3 600, P6 1576 |
| S2 | ★: the search stops a word short | P1 2000, P2 2000, P4 1653, P5 347, P6 8000 |
| B1 | BFS: only each word's first direct synonym followed | P1 871, P3 883, P4 330, P6 871 |
| B2 | BFS: the sentences not sorted | P1 1098, P2 1098, P3 712, P4 1052, P6 1098 (one `__mir-run`) |
| P1 | product: a word's synonyms not sorted | P1 1075, P2 1075, P3 713, P4 1211, P6 1075 |
| P2 | product: the search never goes past a direct synonym | P1 826, P4 632, P6 826 |
| O1 | sorted: a pair grows a group only from its first word | P1 941, P3 1173, P4 519, P6 941 |
| O2 | sorted: the first word given a leading space | P1 2000, P2 2000, P4 2000, P5 2000, P6 2000 |
| L1 | solution: the word itself not marked seen | P1 1822, P2 1822, P6 1822 |
| L2 | solution: each pair's edge one way only | P1 941, P3 1173, P4 519, P6 941 |

All ten are caught, every one by P1, the statement read literally. B2 is
the one whose counts differ between the two runs: without the sort, the
sentences come out in the `Set`'s iteration order, which is random per
process, so its counts change from run to run in either mode (P4 1211, 795
and 663 in three runs) and agree under `KARAC_HASH_SEED`. P3, the pairs
reversed, sees the edits that depend on which word of a pair comes first
or on the order of the pairs, and P5, every word prefixed, only S2 and O2,
the two that change what a sentence holds.

## Benchmarks

`bench/` runs the same workload in Kāra, C, Rust, Go and Python: the ★
arm (union-find over the pairs' words, the groups sorted, every sentence
built by a recursive search, the sentences sorted) on 100 random cases
built once, each 10 pairs of 8 words and a text of 10 words, 4 of them
from the pairs, asked 80 rounds; the sentences counted and the middle
one of each answer folded into a checksum. Every program prints `80
rounds of 100 cases: 21979760 sentences, checksum 841536787`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `684b860a50`
on LLVM 22. A plain `karac build` targets x86-64-v2, so the C and
overflow-checked Rust programs are also built at x86-64-v3 for
comparison:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 5.580 to 6.094 s | 5.766 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 5.537 to 6.040 s | 5.718 s |
| Rust (`rustc -O`) | 2.879 to 3.171 s | 2.996 s |
| Rust (`rustc -O -C overflow-checks=on`) | 2.852 to 3.392 s | 3.034 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 2.815 to 3.241 s | 2.945 s |
| C (`clang -O3`) | 3.677 to 3.985 s | 3.791 s |
| C (`clang -O3 -march=x86-64-v3`) | 3.688 to 4.478 s | 3.837 s |
| Go | 3.007 to 3.770 s | 3.224 s |
| Python | 6.646 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Kāra takes about 1.9x Rust with overflow checks on's time (5.718
s against 3.034 s). Kāra takes about 1.5x C's time (5.718 s against
3.791 s); Kāra takes about 1.8x Go's time (5.718 s against 3.224 s).
Kāra is about 14% ahead of Python (5.718 s against 6.646 s). No profile
was taken.
