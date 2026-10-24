# 966. Vowel Spellchecker

Given a `wordlist`, implement a spellchecker that converts a query word
into a correct word. For a given `query` word, the spell checker handles
two categories of spelling mistakes:

- **Capitalization:** if the query matches a word in the wordlist
  (case-insensitive), the query word is returned with the same case as
  the case in the wordlist.
- **Vowel errors:** if after replacing the vowels `('a', 'e', 'i', 'o',
  'u')` of the query word with any vowel individually, it matches a word
  in the wordlist (case-insensitive), the query word is returned with the
  same case as the match in the wordlist.

The spell checker operates under the following precedence rules: when
the query exactly matches a word in the wordlist (case-sensitive), you
should return the same word back; when the query matches a word up to
capitalization, you should return the first such match in the wordlist;
when the query matches a word up to vowel errors, you should return the
first such match in the wordlist; if the query has no matches in the
wordlist, you should return the empty string.

Given some `queries`, return a list of words `answer`, where `answer[i]`
is the correct word for `query = queries[i]`.

```
wordlist = ["KiTe","kite","hare","Hare"],
queries = ["kite","Kite","KiTe","Hare","HARE","Hear","hear","keti","keet","keto"]
  ->  ["kite","KiTe","KiTe","Hare","hare","","","KiTe","","KiTe"]
wordlist = ["yellow"], queries = ["YellOw"]  ->  ["yellow"]
```

**Constraints:** `1 <= wordlist.length, queries.length <= 5000`;
`1 <= wordlist[i].length, queries[i].length <= 7`; `wordlist[i]` and
`queries[i]` consist only of English letters.

## Approaches

| file | mechanism |
|---|---|
| `spellchecker.kara` ★ | three maps, one per rule: the words in a `Set`, and each word's lowercase form and its lowercase form with every vowel blanked out in `Map`s to the first word that has it (`entry().or_insert()` keeps the first). A query takes the first rule that matches. O(total length) time and space |
| `spellchecker_scan.kara` | a scan per query: the words' lowercase and vowel-blanked forms made once, then every query scans the list once per rule, in the rules' order, and takes the first word the first matching rule finds. O(n · q) time |
| `spellchecker_buckets.kara` | one bucket per vowel pattern: every rule's match shares the query's vowel-blanked lowercase form, so one `Map` from that form to the indices of its words, in order, holds every candidate. A query looks in its bucket only: the word itself if it is there, else the first word of the same lowercase form, else the bucket's first word |
| `spellchecker_sorted.kara` | sorted keys in place of maps: the words sorted, and each word's lowercase and vowel-blanked forms paired with its index and sorted. A pair sorts after an equal key with a smaller index, so the first pair at or after a key, found by binary search, is that key's first word. O(total length · log n) |
| `spellchecker_trie.kara` | three tries, one per rule, over the letters as the rule sees them: as written (52 letters), folded to lowercase (26), and with every vowel folded into one letter. Each node keeps the first word ending there; a query walks each trie in turn and takes the first word it ends on. The tries are flat `Vec`s of child indices |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's two examples and four more
(one-letter words where a vowel query falls back on an earlier word,
lowercase and vowel matches that pick the first of two candidates, words
of one repeated vowel in both cases, and a word with no vowels); for 300
random cases of 1 to 12 words and as many queries of 1 to 4 letters, how
many answers came from each rule and a checksum; and the same for one
case of LeetCode's largest size, 5,000 words and 5,000 queries of up to 7
letters. The words are drawn from the five vowels and two consonants in
both cases, so the rules often collide; a query is a random word itself,
the word with some letters' case flipped, the word with some vowels
replaced by any vowel in either case, or a new word.
`spellchecker.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally, letter by letter on the bytes: a word matches a query by case
when every letter is the same up to case, and by vowels when every
letter is, or both are vowels. It checks 3,200 random cases of the same
kind: 3,000 of up to 6 words and 6 queries of up to 3 letters against
the statement, and 200 of up to 50 words and 50 queries of up to 7
letters against the other properties; 15,740 words and 15,723 queries in
all, whose answers were 6,755 words themselves, 3,250 by case, 2,992 by
vowels and 2,726 empty.

| | property |
|---|---|
| P1 | the statement's answers, on the small cases |
| P2 | each answer is empty exactly when no word matches its query by vowels, and otherwise a word of the list that does |
| P3 | the same answers with the word list given twice over, and the answers reversed for the queries reversed |
| P4 | each query asked alone gets the answer it got in the batch |
| P5 | the words asked as queries answer themselves, and each word in uppercase answers a word of the same lowercase form |
| P6 | each arm agrees with at least two of the other four |

It prints `3200 cases of 15740 words and 15723 queries: 6755 words, 3250
by case, 2992 by vowels, 2726 unmatched, checksum 129185076, 95000
checks over 5 arms: 0 failures` under `karac __mir-run` (47 s)
and `karac __mir-llvm-run`, and the same under `karac __mir-llvm-asan`
with no error.

## Mutation testing

Twenty-seven edits to the differential, each run under `karac
__mir-run` and `karac __mir-llvm-run` with the same failures; fifteen are
kept, three to each arm, and all fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: u not a vowel | P1 739, P2 858, P6 915 |
| M2 | ★: the last word of a lowercase form kept | P1 8, P6 14 |
| M3 | ★: the words themselves never looked up | P1 80, P5 226, P6 118 |
| M4 | scan: the vowel rule comparing lowercase forms | P1 1310, P2 1497, P6 1497 |
| M5 | scan: the first word never matched by vowels | P1 646, P2 517, P3 517, P6 706 |
| M6 | scan: vowels blanked without folding case | P1 1134, P2 1290, P6 1319 |
| M7 | buckets: uppercase vowels kept | P1 1891, P2 2039, P5 2809, P6 2085 |
| M8 | buckets: the bucket's last word the fallback | P1 326, P6 444 |
| M9 | buckets: the case rule without folding the word | P1 138, P5 586, P6 218 |
| M10 | sorted: the search one past its key | P1 2165, P2 2360, P5 2977, P6 2360 |
| M11 | sorted: the neighbour taken when the key is missing | P1 1656, P2 1809, P6 1849 |
| M12 | sorted: o not a vowel | P1 709, P2 831, P6 883 |
| M13 | trie: the last word ending at a node kept | P1 332, P6 451 |
| M14 | trie: e not folded into the vowel | P1 712, P2 828, P6 886 |
| M15 | trie: i not folded into the vowel | P1 730, P2 856, P6 906 |

P1 and P6 kill all fifteen, P2 ten (M1, M4 to M7, M10 to M12, M14,
M15), P5 four (M3, M7, M9, M10) and P3 one (M5). P4 kills none. An
answer that is wrong but still a word of the query's vowel pattern
passes P2, so M2, M3, M8, M9 and M13, which take the wrong one of
several candidates, leave it alone. P3 and P4 ask whether an answer
depends on the other queries or on later copies of a word, which none of
these edits changes, except M5: skipping the first word loses it from
the list, but the doubled list still holds its copy. They guard against
an arm that caches across queries or lets a later duplicate win.

Twelve other edits were tried and set aside. Eight failed exactly the
same checks as a kept one: scan and buckets taking the last word of a
lowercase form, as M2; scan matching a word to itself in lowercase, as
M3; scan and the trie leaving u out, as M1; the trie never looking the
words themselves up and folding the word as written to lowercase, as
M3; and the trie never asking the vowel rule, as M4. Four were sound
but beyond three an arm: ★ keeping the last word of a vowel pattern and
blanking vowels without folding case, scan never matching the last word
by case, and sorted searching the words in lowercase. None was
equivalent and none crashed.

## Verification

Every arm prints the same output as `spellchecker.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and under
`karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `e04ae2b46b`, the runtime
archives rebuilt at the same commit. Under `karac __mir-run` the ★ arm
takes 0.52 s, buckets 0.76 s, the trie 0.90 s, sorted 4.8 s and scan
10.3 s, the last two mostly on the case of 5,000 words and 5,000
queries; the differential takes 47 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The legacy compiler was removed from kara at M3, so there is no legacy
lane.

## Benchmarks

The bench program makes five cases of LeetCode's largest size once,
5,000 words and 5,000 queries of up to 7 letters each, made as in the
arms. In each of 200 rounds it runs the ★ arm on one case in turn and
folds every answer into a checksum. Every implementation prints `200
rounds over 5 cases of 5000 words and 5000 queries: 982440 matched,
checksum 684907998`. Kāra, Rust, Go and Python build three hash tables
of owned strings on every call, Kāra's and Rust's under SipHash-1-3. C
uses three open-addressing tables of 16,384 slots keyed by FNV-1a, with
the words in fixed 8-byte arrays, so it allocates nothing per call.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python, with karac at `e04ae2b46b`:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.17 to 0.20 s | 0.18 s |
| Rust (`rustc -O`) | 0.53 to 0.70 s | 0.59 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.52 to 0.62 s | 0.56 s |
| Go | 0.72 to 0.79 s | 0.76 s |
| Python | 2.0 s | |
| Kāra (`karac build --mir`) | 0.50 to 0.58 s | 0.52 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Python's run is about 11 times
C's.

v2 took 0.92 times Rust's median time under overflow checks and 2.9
times C's. Under valgrind's cachegrind v2 ran 4.97 billion instructions
and 816 million branches with 27.4 million mispredicted, Rust with
overflow checks 4.30 billion, 632 million and 30.4 million, and C 816
million, 153 million and 12.7 million. The gap to C is the strings and
hash tables the other languages build per call and C does not.
