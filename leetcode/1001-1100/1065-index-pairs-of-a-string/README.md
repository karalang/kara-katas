# 1065. Index Pairs of a String

Given a string `text` and an array of strings `words`, return every index
pair `[i, j]` such that the substring `text[i..j]` (both ends included)
is one of the words. Return the pairs sorted by their first index, and
by their second index when the first ties.

```
text = "thestoryofleetcodeandme", words = ["story", "fleet", "leetcode"]
    ->  [[3, 7], [9, 13], [10, 17]]
text = "ababa", words = ["aba", "ab"]
    ->  [[0, 1], [0, 2], [2, 3], [2, 4]]    (matches may overlap)
```

**Constraints:** `1 <= text.length <= 100`; `1 <= words.length <= 20`;
`1 <= words[i].length <= 50`; `text` and the words are lowercase English
letters; the words are distinct.

The arms return the pairs as `Vec[(i64, i64)]`, which prints as `[(3, 7),
(9, 13), (10, 17)]`.

## Approaches

| file | mechanism |
|---|---|
| `index_pairs.kara` ★ | every start of the text against every word (`text[i..].starts_with(w)`), then the pairs sorted. O(n * total word length) plus the sort |
| `index_pairs_find.kara` | each word found again and again (`text[from..].find(w)`), one letter past the last match so that overlapping matches count, then the pairs sorted |
| `index_pairs_set.kara` | the words in a `Set[String]`, every substring no longer than the longest word looked up, by start and then by end, so the pairs come out in order |
| `index_pairs_trie.kara` | a trie of the words (`Vec[Array[i64, 26]]` of edges), walked from each start for as long as the letters follow one of its paths; each word's end on the way is a pair, in order |
| `index_pairs_kmp.kara` | Knuth-Morris-Pratt for each word: its failure function, then one pass over the text that falls back along it on a mismatch, then the pairs sorted. O(n + m) per word |
| `index_pairs_solution.kara` | LeetCode's Rust template (`struct Solution;`, `Vec<Vec<i32>>`, `vec![]`, `for w in &words`, `w.as_str()`, `Solution::`), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 11 lines: the answers for LeetCode's two
examples and five more; the count and a checksum of the pairs for 3000
texts of 1 to 20 letters over 1 to 3 with 1 to 5 words of 1 to 4 letters,
and for 300 texts of 50 to 100 letters over 2 to 26 with 1 to 20 words
of 1 to 8; and the pairs for 100 `a`s against every run of 1 to 20 of
them (1810 pairs), and for 100 alternating letters against `ab`, `ba`,
`aba` and `bab` (197). Every other word is cut from the text, so most
problems have matches. `index_pairs.py` mirrors the ★ arm and its output
is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every pair of a start and an end at or after it whose letters,
compared as a `String`, are one of the words, by start and then by end.
It checks 2000 texts: 1000 of 1 to 12 letters over 1 to 3 with 1 to 5
words of 1 to 4 letters, and 1000 of 1 to 40 over 2 to 26 with 1 to 10
words of 1 to 6; 10711 pairs in all. Every random choice of a problem is
drawn before any arm answers, so a wrong arm cannot change the problems
the others see.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the pairs are in range, strictly ascending, and each holds a word |
| P3 | the letters renamed by a random permutation, in the text and the words alike, and the words in reverse order, leave the answer |
| P4 | the text and every word reversed answer the pairs mirrored |
| P5 | a letter appended to the text keeps every pair and adds only pairs ending at it, and a word dropped removes exactly the pairs holding it |
| P6 | each arm agrees with at least three of the other five |

The differential prints `2000 problems: checksum 575253296, 84000 checks
over 6 arms: 0 failures` under every lane in Verification; a Python
reading of the same 2000 texts gives the same checksum. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Thirty edits to the differential, five to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. Fifteen are kept, two or three to
each arm. All thirty are killed, each fails the same way under both
backends, none by a crash, and no two kept ones fail the same checks. Two
first edits to the find arm crashed and were replaced: reading a match's
offset as if from the start of the text sends the search back over it,
so the pairs grow without end until the process is killed, and resuming
two letters past a match runs off the text's end.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the pairs left unsorted | P1 414, P2 414, P3 699, P4 377, P6 414 |
| M2 | ★: the last start dropped | P1 512, P4 640, P5 512, P6 512 |
| M3 | ★: a word anywhere after the start taken (`contains`) | P1 1288, P2 1288, P4 1333, P5 813, P6 1288 |
| M4 | find: overlapping matches refused | P1 372, P4 289, P6 372 |
| M5 | find: a one-letter word matched once | P1 822, P4 822, P6 822 |
| M6 | find: only the first match of each word | P1 1069, P4 1069, P6 1069 |
| M7 | set: the longest words never looked up | P1 1115, P5 270, P6 1115 |
| M8 | set: substrings only as long as the shortest word | P1 1280, P5 239, P6 1280 |
| M9 | set: each substring one letter short | P1 1741, P2 1199, P4 1136, P5 842, P6 1741 |
| M10 | trie: the walk begun one letter late | P1 1741, P2 1556, P4 1332, P5 1056, P6 1741 |
| M11 | trie: a root edge rebuilt for each word | P1 971, P3 1107, P4 711, P5 258, P6 971 |
| M12 | KMP: the failure function all zeros | P1 409, P4 350, P6 409 |
| M13 | KMP: one fall back per letter | P1 20, P2 20, P4 25, P5 2, P6 20 |
| M14 | solution: the first word left out | P1 794, P3 1224, P5 401, P6 794 |
| M15 | solution: the pairs in descending order | P1 1441, P2 1441, P4 1441, P6 1441 |

P1 and P6 kill all fifteen, P4 twelve, P5 nine, P2 six and P3 three. P4
reads the text backwards, where a word's matches overlap differently and
the first match is a different one, so it sees every edit that loses an
overlap or a later match (M4 to M6, M12). P3 puts the words in reverse
order, which only an edit that depends on the words' order notices: the
pairs left in that order (M1), a trie whose later words overwrite the
earlier ones' first edge (M11), and the first word left out (M14). The
set arm's length limits (M7, M8) are caught only by P1, P5 and P6: a
dropped word changes the longest and shortest lengths.

Of the fifteen not kept, the solution sorted by start only fails as M1,
and the ★ and solution arms' ends one past the word fail alike. The ★
and trie arms never matching a one-letter word fail alike, as do the find
arm begun at the second letter and the set arm's first start dropped, the
set and trie arms stopping at the shortest word at each start, the trie
walk never reaching the last letter and the solution dropping a word that
ends the text, and the KMP match restarting from nothing and M4. The find
arm's pairs left unsorted, the KMP failure function skipping its second
letter and the KMP start one letter early each fail in a way of their
own.

## Verification

Every arm prints the same output as `index_pairs.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any file. Under `karac __mir-run` the arms take 0.5 s (find) to 1.0 s (★) and the
differential 11.1 s.

Every file went through `karac fix`, which applies the style lints that
`karac check` leaves at allow: it dropped the harness's `.to_string()` on
each string literal, 28 in each arm (`("ababa", ["aba", "ab"])` is
already a `(String, Vec[String])`), and turned the trie's `fn insert(mut
self, ..)`, Rust's spelling, into `mut ref self`. In the differential it
made `let answer = answers[a]`, a move out of an index, `ref answers[a]`.
The Rust arm reaches a clean check in three rounds: the syntax (`struct
Solution {}`, `Vec[Vec[i32]]`, `for w in ref words`, `Solution.`), then
`vec![]` to `Vec.new()` and the inner `vec![..]` to a list literal, then
the harness's literals. Nothing was left by hand, and the kata met no
compiler gap.

## Benchmarks

The bench builds 40 texts of 20000 letters over 2 to 4 letters, each with
up to 100 distinct words of 1 to 12 letters (every other one cut from the
text), once in all five languages, then answers each with the ★ arm's
search: every start against every word, then the pairs sorted, 1817648
pairs in all. Rust sorts a `Vec<(i64, i64)>` with `sort()`, Go uses
`sort.Slice`, C `qsort` over a struct, and Python `list.sort`. Every
implementation prints `40 calls: 1817648 pairs, checksum 155635159`.

Timings on a 4-core container, ten interleaved runs of each compiled
program and one of Python, with kara `92cb060c13` on LLVM 22:

| | time | median |
|---|---|---|
| Rust (`rustc -O`) | 0.224 to 0.249 s | 0.228 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.214 to 0.267 s | 0.229 s |
| C (`clang -O3`) | 0.253 to 0.321 s | 0.266 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.315 to 0.414 s | 0.324 s |
| Kāra (`karac build`) | 0.319 to 0.428 s | 0.327 s |
| Go | 0.516 to 0.588 s | 0.544 s |
| Python | 3.2 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time (0.325 s) is below its real time.

Kāra takes 1.41x the time of Rust under overflow checks. With the sort
line deleted from both, Kāra runs in 0.215 s and Rust in 0.158 s, so the
search (and building the texts) is 1.36x and the sort about 1.5x, 0.109
s against 0.071 s for 40 sorts of about 45000 pairs that arrive almost in
order. Kāra sorts a `Vec[(i64, i64)]` with the runtime's stable bottom-up
merge (`karac_mir_sort`), calling the tuple's comparator through a
function pointer for each comparison; Rust's driftsort is inlined and
takes the runs already in order as they come. kara B-2026-11-06-34
(open) is the row on the merge's cost under `sort_by`; this `sort()` of
tuples is the same merge (inferred from the IR, not measured apart).
