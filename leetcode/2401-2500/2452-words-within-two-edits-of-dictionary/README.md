# 2452. Words Within Two Edits of Dictionary

You are given two string arrays, `queries` and `dictionary`. All words
in each array comprise of lowercase English letters and have the same
length.

In one **edit** you can take a word from `queries`, and change any
letter in it to any other letter. Find all words from `queries` that,
after a **maximum** of two edits, equal some word from `dictionary`.

Return *a list of all words from* `queries`*, that match with some word
from* `dictionary` *after a maximum of **two edits***. Return the words
in the **same order** they appear in `queries`.

```
queries = ["word","note","ants","wood"], dictionary = ["wood","joke","moat"]  ->  ["word","note","wood"]
queries = ["yes"], dictionary = ["not"]                                        ->  []
```

**Constraints:** `1 <= queries.length, dictionary.length <= 100`;
`n == queries[i].length == dictionary[j].length`; `1 <= n <= 100`; all
`queries[i]` and `dictionary[j]` are composed of lowercase English
letters.

An edit changes one letter in place, so two edits reach exactly the
words that differ from the query in at most two places. Each query is
then a scan of the dictionary for a word with at most two differences,
which can stop at the third.

## Approaches

| file | mechanism |
|---|---|
| `edits.kara` ★ | each query against each word, the differing places counted over the bytes until a third rules the word out, and the query kept at the first word that passes. O(q d n) |
| `edits_naive.kara` | the statement read directly: for each query the differences from every dictionary word counted in full over its `chars()`, and the query kept when the least count is at most two. O(q d n) |
| `edits_mask.kara` | wildcards: every dictionary word with each two of its places, or its one place, written `*`, in a `Set[String]`; a query is kept when one of its own masks is in the set. O((q + d) n^3) |
| `edits_split.kara` | pigeonhole: every word cut into three parts at the same places, so a word within two differences matches the query on some part; a `Map` from each part and its text to the dictionary words holding it gives each query its candidates, which alone are counted out |
| `edits_iter.kara` | iterators: the queries kept by `filter` when `any` dictionary word has at most two places that differ, counted by `zip` over the bytes, `filter` and `count`, then `cloned` and collected. O(q d n) |
| `edits_solution.kara` | LeetCode's Rust template: the queries taken by `into_iter()` and kept by `filter` when `any` word's bytes, paired by `q.bytes().zip(d.bytes())`, differ in at most two; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's two examples; one-letter
words, always within two edits; two letters, both changed; three
letters, one query two away and one three; then 100 queries against 100
words of 100 letters, the constraints' most, each query a dictionary
word with 0 to 4 places redrawn, from 26 letters and from 2, as a
count and a checksum; and 3000 random cases of 1 to 5 queries against
1 to 5 words of 1 to 6 letters from `a` to `c`, as a total and a
checksum. `edits.py` mirrors the ★ arm and its output is
byte-identical, and the mirror was checked on 5000 random cases of up
to 4 letters against every word that two edits reach.

`check` first reports 4 errors on the template, and `karac fix` carries
it in one call, reporting 10 edits: each of the six angle brackets of
the three `Vec<String>` made square; `struct Solution;` given its
braces; and, once the template parses, `.clone()` put before
`into_iter()`, since the parameter is borrowed and `into_iter` takes it
by value, and `.iter()` put after each `bytes()`, which gives a slice
in Kāra. The closure pattern `|(a, b)|`, `!=` on bytes and the bare
`collect()` into the declared `Vec[String]` stand as Kāra.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: from each query every word that one edit and then a second
reach, an edit setting one place to any letter the case's words are
drawn from, the only letters a dictionary word can hold, all kept in a
`Set[String]`; the query is kept when the words reached include a
dictionary word. No places are compared and no differences counted. It
checks 300 random cases of 1 to 5 queries and 1 to 5 words of 1 to 5
letters from 2 to 4; then 30 of up to 8 letters from 3, each query a
dictionary word with 0 to 4 places redrawn; then 30 of up to 10 queries
and words of 1 to 3 letters from 2. All 360 are drawn before any arm
answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | the queries in reverse order: the answer reversed |
| P3 | the dictionary in reverse order: the same answer |
| P4 | the letters of every query and word reversed: each answer reversed |
| P5 | the queries added to the dictionary: every query |
| P6 | each arm agrees with at least three of the other five |

P2 holds because each query is kept or not on its own, and P3 because
the dictionary is searched as a whole. P4 holds because reversing two
words keeps the number of places where they differ. P5 holds because a
query is no edits from itself.

The differential prints `360 cases: checksum 347748712, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and counts every pair's differences. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: two differences rule a word out | P1 146, P6 146 |
| M3 | ★: the first place never compared | P1 60, P4 33, P6 60 |
| M5 | ★: only the first word tried | P1 107, P3 123, P5 157, P6 107 |
| M7 | naive: the most differences kept | P1 270, P5 292, P6 270 |
| M9 | naive: matching places counted | P1 99, P5 10, P6 99 |
| M10 | naive: the least started at 0 | P1 83, P6 83 |
| M12 | mask: one place masked | P1 183, P4 112, P6 183 |
| M13 | mask: only neighbouring places masked | P1 64, P6 64 |
| M14 | mask: a one-letter word never masked | P1 68, P5 68, P6 68 |
| M18 | split: the last part never indexed | P1 29, P4 47, P6 29 |
| M19 | split: three differences allowed | P1 47, P4 42, P6 47 |
| M20 | split: each part indexed without its place | P1 54, P4 79, P6 54 |
| M23 | iter: every word needed | P1 149, P5 195, P6 149 |
| M25 | iter: the query's first byte skipped | P1 87, P4 52, P5 22, P6 87 |
| M26 | iter: the queries that fail kept | P1 360, P5 360, P6 360 |
| M28 | solution: three differences allowed | P1 72, P6 72 |
| M31 | solution: the last query dropped | P1 310, P2 256, P5 360, P6 310 |

P1 and P6 kill all seventeen, P5 eight, P4 six, and P2 and P3 one
each.

Fourteen are not kept. Eight fail exactly as a kept one: the ★ arm's
three differences allowed (M2) as the template's (M28); the ★ arm's last
place never compared (M6) as its first place never compared (M3); the naive, iter and template
arms' fewer than two differences (M8, M22, M27) as the ★ arm's two
differences ruling a word out (M1); the iter and template arms' matching
places counted (M24, M30) as the naive arm's (M9); and the template's
only the first word tried (M29) as the ★ arm's (M5). Five fail apart
from every kept one and were left out because those arms keep their
share already: the ★ arm's query kept once for each word (M4), the naive
arm's last word alone (M11), the mask arm's dictionary's first word left
out and every mask of the query needed (M15, M16), and the split arm's
first candidate alone checked (M21).

One survives, and is equivalent: the split arm's two parts (M17). The
cuts `[0, n / 2, n, n]` leave the third part empty, and the empty text
is the same in every word, so every dictionary word is indexed under it
and every query finds every word as a candidate; the count of
differences then decides alone, as the naive arm does.

## Verification

Every arm prints the same output as `edits.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.6 to 4.1 s, but for the mask
arm, which builds 4950 masks of 100 letters for each word on the cases
of 100 words: it takes 19 s there, 3.7 s under `karac __mir-llvm-asan`
and 0.9 s under `karac run`. The differential takes 1.9 s under `karac
__mir-run`, 1.1 s under `karac __mir-llvm-asan` and 0.8 s under `karac
run`.

## Benchmarks

The bench builds 100 cases once from its own generator, each 100
queries against 100 words of 100 letters from `a` to `d`, the
constraints' largest, each query a dictionary word with 0 to 4 places
redrawn. It then makes 45 passes; pass `p` redraws one letter of every
case's query `p`, so the answers change from pass to pass, then
answers every case and folds how many queries it keeps plus the pass
into the checksum. The bench uses the ★ arm, the scan that stops at a
third difference, in all five languages. Every implementation prints
`45 passes over 100 cases of 100 queries: checksum 979068560`. The
queries are rebuilt as strings for every answer and the kept ones are
copied out in every language, in C by `strdup`.

BENCHTAB
