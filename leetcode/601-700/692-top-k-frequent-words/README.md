# 692. Top K Frequent Words

Given an array of strings `words` and an integer `k`, return the `k`
most frequent strings, sorted by frequency from highest to lowest, and
words with the same frequency in lexicographical order.

```
words = ["i","love","leetcode","i","love","coding"], k = 2
  ->  ["i","love"]
words = ["the","day","is","sunny","the","the","the","sunny","is","is"],
k = 4  ->  ["the","is","sunny","day"]
```

**Constraints:** 1 <= `words.length` <= 500; 1 <= `words[i].length` <=
10; lowercase English letters; `k` is in the range [1, the number of
unique words]. **Follow-up:** O(n log k) time and O(n) extra space.

## Approaches

Every arm is `fn top_k_frequent(words: Vec[String], k: i64) ->
Vec[String]`. Kata [347](../../301-400/347-top-k-frequent-elements/) has
an older string-keyed sibling of its own algorithm, written for the
legacy backend; this kata is the problem itself, on v2.

| file | mechanism |
|---|---|
| `top_k_frequent_words.kara` ★ | a `Map` counts each word; the distinct words with their counts are sorted by count down, then alphabetically, and the first k taken; O(n + d log d) for d distinct words |
| `top_k_frequent_words_heap.kara` | the follow-up: after counting, a `PriorityQueue` of at most k, weakest first, dropping the weakest when it passes k; the weakest has the fewest occurrences and, on a tie, comes last in the alphabet, so `Ord` is written by hand; O(n + d log k) |
| `top_k_frequent_words_buckets.kara` | bucket c holds the words that occur c times; buckets are walked from n down, each sorted alphabetically when reached, until k are taken; O(n + d log d) at worst |
| `top_k_frequent_words_select.kara` | no hashing: a sorted copy puts equal words side by side, one pass gives each word and its count in alphabetical order, then k rounds each pick the largest count not yet taken, the first of equal counts winning; O(n log n + k d) |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 7 lines: the two LeetCode examples; one word;
six words once each, so all of them in alphabetical order with a prefix
before its longer word; equal counts among prefixes of `apple`; the top
10 of 500 words of up to 3 letters from 3 letters; and 300 random
problems of up to 500 words of up to 10 letters from 1 to 26 letters,
`k` from 1 to the number of distinct words, with a checksum over the
answers. `top_k_frequent_words.py` mirrors the ★ arm and its output is
byte-identical. No arm prints a `Map` in its walk order: each ranks by a
total order first.

## Differential

`differential.kara` holds copies of the four arms and the definition.
The definition is written apart from all four arms: each distinct word
is counted by a scan of the whole list, and a word's place in the answer
is the number of words that beat it, by more occurrences or by as many
and earlier in the alphabet; the words whose place is below k go at
their places. 1,000 random problems are checked, 1 to 40 words of 1 to
4 letters from an alphabet of 1 to 5 letters, so that counts tie often,
and `k` from 1 to the number of distinct words.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | the words in another order answer the same |
| P3 | the answer for k is the start of the answer for k + 1, or has every distinct word when k is all of them |
| P4 | every letter moved one on in the alphabet moves every letter of the answer on |

It prints `1000 problems, 4 arms, 16000 checks, 0 failures` under `karac
__mir-run` and `karac __mir-llvm-run`, and runs clean under `karac
__mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: equal counts in reverse alphabetical order | P1 631 |
| M2 | ★: every word counted once | P1 688 |
| M3 | ★: the fewest occurrences first | P1 812 |
| M4 | heap: on equal counts the earlier word taken as weaker | P1 631 |
| M5 | heap: k + 1 candidates kept | P1 722, P3 561 |
| M6 | heap: the drained queue not reversed | P1 721, P3 722 |
| M7 | buckets: one word too many taken from a bucket | P1 455, P3 410 |
| M8 | buckets: each bucket in reverse alphabetical order | P1 631 |
| M9 | buckets: counts 1 and 2, 3 and 4, and so on sharing a bucket | P1 436 |
| M10 | select: the last of equal counts picked | P1 631 |
| M11 | select: a picked word's count lowered by one, not cleared | P1 564 |
| M12 | select: the copy left unsorted | P1 730, P2 755 |

P1 kills all twelve. The four that reverse the alphabetical tie-break,
M1, M4, M8 and M10, fail the same 631 problems, the ones whose answer
holds two words of equal count. P3 sees the mutants whose answers have
the wrong length or run backwards, and P2 only M12, the one arm that
reads the list by position. P4 sees none, and could not: moving every
letter on keeps every count and every comparison between words, so a
mutant gives the moved answer to its own wrong answer too. It stays as a
check on byte handling, not on ranking. The buckets walk is the one
place an edit is easily equivalent: putting each word one bucket lower
keeps the order of the buckets, so that candidate, run as a check,
changed no answer and was replaced by M9.

## Verification

Every arm prints the same output as `top_k_frequent_words.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and runs clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints its line under all three. `karac check` passes all four arms, the
differential and the bench program. All with the compiler at kara
`de50d67b07` for both the debug build and the release build that runs
`check` and `__mir-run`, with runtime archives rebuilt after the last
`runtime/src` change.

The frozen legacy backends refuse all four arms, the differential and
the bench program at type checking: at `*c` over `counts.get(w)` in the
three arms that count with a map, at `*b` over `w.bytes().iter()`, since
legacy gives both by value where v2 gives references, and at
`next_random(mut seed)` inside the harness's `random_word`, whose `seed`
is already a `mut ref`: legacy wants the marker dropped, while on v2 the
marked forward is the spelling (kara B-2026-10-14-25). Legacy is frozen,
so this is noted, not filed.

## Benchmarks

The bench program uses the select arm, the same algorithm in all five
languages; C has no map. It builds 100 lists of 500 words once, each
word 1 to 4 letters from the first 6, so that about 255 of each 500 are
distinct and most words occur more than once, then in each of 60 rounds
asks every list for its top 10, putting each answer into a checksum.
Every implementation prints `60 rounds of 100 lists of 500 words:
60000 words answered, checksum 477069357`, the Kāra program under `karac
__mir-run` included (in 8 s).

Each implementation sorts a fresh copy of the list, so the copy is part
of the work: Kāra and Rust copy every string, Go copies only the string
headers, since its strings cannot change, C copies an array of pointers
and sorts it with `qsort` and `strcmp`, and Python's `sorted` makes a
new list of the same strings. Spot timings on a shared 4-core container,
eight runs of each compiled program, five of them interleaved, and five
of Python (`bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.29 to 0.38 s |
| Rust (`rustc -O`) | 0.34 to 0.45 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.36 to 0.46 s |
| Go | 0.40 to 0.44 s |
| Python | 1.13 to 1.23 s |
| Kāra (`karac build --mir`) | 0.54 to 0.62 s |
| Kāra, legacy (`karac build`, a copy) | 0.46 to 0.53 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend, since the legacy `karac build` refuses the bench
program at `*b` as above. That edit is by hand, on top of the
`scripts/new-bench.sh` output. A copy outside the kata that reads `b as
i64` builds under legacy, and its row is above. Under `karac
__mir-llvm-run` the program prints the same line in 2.8 s, compile
included; that JITs the MIR's IR without optimization passes, so it is
not a benchmark.

So the v2 build is about 1.2 times the legacy copy here, inside the
M2 bar of 2 for any one kata, and behind the other compiled languages,
about 1.4 times Go and Rust. Python is close behind because its `sorted`
and string comparisons run in C. The comparison with C and Rust waits
until after M4.

## Compiler findings

None new. `karac check` passed all four arms and the differential as
first written, apart from one warning, a discarded `Option` from
`best.pop()` in the heap arm, now `let _ = best.pop();`.
