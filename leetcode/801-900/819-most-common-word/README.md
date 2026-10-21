# 819. Most Common Word

Given a string `paragraph` and a list of `banned` words, return the most
frequent word that is not banned. Words are compared without case, and
the answer is in lower case. LeetCode guarantees that one word is not
banned and that the answer is unique.

```
paragraph = "Bob hit a ball, the hit BALL flew far after it was hit.", banned = ["hit"]  ->  "ball"
paragraph = "a.", banned = []                                                         ->  "a"
```

**Constraints:** `1 <= paragraph.length <= 1000`, and the paragraph is
English letters, spaces and the marks `!?',;.`; `0 <= banned.length <=
100`, `1 <= banned[i].length <= 10`, and the banned words are lower-case
letters.

## Approaches

A word is a run of letters, so every mark and space separates words, and
`"bob's"` is the two words `bob` and `s`. The kata's random tests can
tie, so every arm settles a tie the same way: of two words counted as
often, the one first in alphabetical order. Every arm also returns an
empty word when every word is banned, which the statement rules out and
the differential reaches.

| file | mechanism |
|---|---|
| `most_common_word.kara` ★ | lower every letter and turn everything else into a space, split at the spaces, and count each word not in a set of the banned words in a map; then walk the map for the most counted. O(n) for n characters |
| `most_common_word_scan.kara` | one pass over the characters, growing the current word letter by letter and counting it in a `SortedMap` when a non-letter or the end closes it; a walk in key order meets the words alphabetically, so the first with the highest count that is not banned answers. O(n log w) for w distinct words |
| `most_common_word_sort.kara` | collect the words that are not banned, lowered, and sort them, so that equal words sit together; the first longest run answers. No hashing. O(n log n) |
| `most_common_word_iter.kara` | the cleaned text `collect`ed from a `map` over the characters, the words counted by a `fold` into a map after a `filter`, and the answer the `min_by_key` of the counts, keyed on the count negated and then the word |
| `differential.kara` | the four arms against the statement read word by word off the text, four properties |

Every arm prints the same 9 lines: LeetCode's two examples; five small
cases (the most frequent word banned, with words joined by commas alone;
mixed case with two words banned; banned words that start like each
other; two words tied for most; and one-letter words between marks);
LeetCode's largest, 993 characters with 101 banned words; and 300 random
paragraphs of up to 21 words, with a total and a checksum.
`most_common_word.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement
played out on the text: find each run of letters, and for each one that
is not banned count again, letter by letter and case aside, the runs
that spell the same word; the answer is the word with the highest count,
the first alphabetically on a tie. It keeps no map and no sorted list.
Its 1,600 cases come in four kinds of 400: up to 30 words of six; up to
30 of two, so that counts often tie; words of `a` and `b` up to four
letters long, many of them the start of others; and the first kind's
words joined by bare marks such as `'` and `!?`, mostly with no space.
Each word is written in random case, some of the words are banned but
never the first, and one time in two a word that is not there is banned
too. 321 cases have a tie for the most counted word.

| | property |
|---|---|
| P1 | the statement's answer |
| P2 | a word of the paragraph, in lower case and not banned |
| P3 | the same words with their case and marks drawn afresh give the same answer |
| P4 | with the answer banned too, the answer is another word that occurs no more often, or there is none |

It prints `1600 cases (321 with a tie for most), 25600 checks over 4
arms: 0 failures` under `karac __mir-run`. Under `karac __mir-llvm-run`
the iterator arm fails, 1,510 and 1,445 checks in two runs and none in
the other arms, and under `karac __mir-llvm-asan` it stops at a
heap-buffer-overflow in that arm's `min_by_key`: B-2026-10-21-4, below.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a tie goes to the later word | P1 321 |
| M2 | ★: the banned words ignored | P1 771, P2 771, P4 1600 |
| M3 | ★: case kept | P1 1253, P2 1220, P3 1366, P4 307 |
| M4 | scan: the last word never counted | P1 67, P2 23, P3 56, P4 38 |
| M5 | scan: a tie goes to the later word | P1 321 |
| M6 | scan: a mark does not end a word | P1 334, P2 316, P3 334, P4 37 |
| M7 | sort: the last word lost | P1 67, P2 23, P3 56, P4 38 |
| M8 | sort: the shortest run kept | P1 878, P4 451 |
| M9 | sort: a word's first letter dropped | P1 1587, P2 1564, P4 193 |
| M10 | iter: case kept | P1 1253, P2 1220, P3 1366, P4 307 |
| M11 | iter: the banned words ignored | P1 771, P2 771, P4 1600 |
| M12 | iter: a tie goes to the later word | P1 321 |

P1 kills all twelve. The three tie edits fail on exactly the 321 cases
with a tie and are seen by P1 alone: the other properties hold for
either word of a tie. Each mistake made twice by different code fails on
the same cases, case kept in M3 and M10, the banned words ignored in M2
and M11, and the last word lost in M4 and M7, the scan arm by never
closing it and the sort arm by stopping its loop one place early. P4
catches M2 and M11 on every case: banning the answer changes nothing
when the banned words are never read.

## Verification

The ★, scan and sort arms print the same output as `most_common_word.py`
under `karac __mir-run` (the v2 MIR interpreter) and `karac
__mir-llvm-run`, and under `karac __mir-llvm-asan` (AddressSanitizer)
with no error. The iterator arm prints it under `karac __mir-run` only:
on the compiled lanes its answers are wrong and the sanitizer lane exits
86 (B-2026-10-21-4). `karac check` passes all four arms, the
differential and the bench program. The debug build that runs
`__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` is at kara
`385539fdac`, with runtime archives rebuilt from that tree; the release
build that runs `check` and `__mir-run` is at `c3f84545bb`.

The leak check copied each arm's sanitizer lane executable as it was
linked and ran it with the preloaded shim from kata 708, which refuses
the lane's hand-made stack so that LeakSanitizer sees `main`: the ★,
scan and sort arms print their output and report no leak, and the
iterator arm and the differential stop at the overflow above.

The frozen legacy compiler refuses all four arms and the bench program.
It types the items of a map's or a `Vec[u8]`'s `iter()` as values, not
references, and so refuses their `*`, and it wants an `.iter()` on the
`Vec` that `split_whitespace` returns before a `filter`. Legacy is
frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. It draws 64
paragraphs once, each about 1,000 characters, LeetCode's largest, from
300 words of up to 10 letters with the earlier words more often, one
word in four in capitals and the words separated by spaces and marks,
and for each 100 banned words, half of them common. Each of 200,000
rounds answers the next paragraph afresh, so the work is a pass over the
characters, a hash map of up to a few hundred words and a set of the
banned ones. Every implementation prints `200000 rounds of 64
paragraphs: total 840625, checksum 876064349`, the Kāra program under
`karac __mir-run` included, in 876 s with the interpreter's step limit
raised by `KARAC_MIR_MAX_STEPS`.

Spot timings on a shared 4-core container, two sets of five interleaved
runs of each compiled program and two runs of Python (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 2.48 to 2.91 s |
| Rust (`rustc -O`) | 3.72 to 4.31 s |
| Rust (`rustc -O -C overflow-checks=on`) | 3.80 to 4.60 s |
| Go | 3.73 to 4.73 s |
| Python | 21.1 to 21.7 s |
| Kāra (`karac build --mir`) | 9.65 to 11.43 s |

The legacy backend refuses the program (Verification), so there is no
legacy time. `bench.sh` builds the Kāra program with `karac build
--mir`, the v2 compiled backend; that edit is by hand, on top of the
`scripts/new-bench.sh` output.

The two interleaved sets ran either side of a rebuild of the runtime
archives, on a machine busier the second time: v2 took 9.65 to 10.32 s
and then 10.92 to 11.37 s, against C's 2.48 to 2.58 s and then 2.66 to
2.91 s, so v2 runs about four times C's time and two and a half times
Rust's. Under valgrind's cachegrind v2 runs 99.1 billion instructions,
against C's 16.8 billion and Rust's 32.3 billion, and 906 million
indirect branches, a third of them mispredicted, against C's 44 million
and Rust's 33 million. Callgrind at 2,000 rounds puts a third of v2's
instructions in `karac_mir_char`, the runtime call that answers
`is_ascii_alphabetic` and `to_ascii_lowercase` for each character by
finding the method by its name: B-2026-10-13-31, filed by kata 520,
which now carries this kata's measurement. Hashing the words is a tenth.
Built for `x86-64-v3`, the target `karac build` uses, C takes 2.82 to
3.02 s and Rust with overflow checks 4.07 to 4.50 s, against v2's 11.03
to 11.43 s in the same five interleaved runs. Python takes 21 s, about
eight times C's time, as its `str.lower` and `split` run in C. The
comparison with C and Rust waits until after M4.

## Compiler findings

The iterator arm's answer is wrong on the v2 compiled backend:
B-2026-10-21-4. Its `min_by_key` over the map of counts returns the key
of one word with the count of another, or a count no word has, under
`karac __mir-llvm-run`, `karac __mir-llvm-asan` and `karac build --mir`,
while `karac __mir-run` is right. The same holds for `max_by_key` over a
`SortedMap`, and the same calls over a `Vec` of tuples are right on
every lane. The differential reports 1,510 failures in the iterator arm
under `karac __mir-llvm-run`, and the arm stays as written until the row
closes.

The same arm types its `fold`'s map by hand, `let mut counts:
Map[String, i64] = counts;`: B-2026-10-21-3. Left to inference, a
`Map.new()` whose first use is `counts.get(w)` with a `Str` is fixed at
a `Str` key, and the `String` insert after it is refused, though lookup
by a view is the library's spelling for a `String`-keyed map. The ★ arm
annotates its map and set as a matter of course, so it is not affected.
The annotation goes when the row closes.
