# 521. Longest Uncommon Subsequence I

Given two strings `a` and `b`, return the length of the longest
uncommon subsequence between `a` and `b`. If no such uncommon
subsequence exists, return `-1`.

An uncommon subsequence between two strings is a string that is a
subsequence of exactly one of them.

```
a = "aba", b = "cdc"  ->  3
a = "aaa", b = "bbb"  ->  3
a = "aaa", b = "aaa"  ->  -1
```

**Constraints:** `1 <= a.length, b.length <= 100`; `a` and `b`
consist of lower-case English letters.

## Approaches

Every arm is `fn find_lus_length(a: Str, b: Str) -> i64`. The answer
is a whole word or nothing: equal words share every subsequence, and
otherwise the longer word (either, when they are as long) is a
subsequence of itself and not of the other.

| file | mechanism |
|---|---|
| `find_lus_length.kara` ★ | equal words have none; otherwise the longer length |
| `find_lus_length_subseq.kara` | try each whole word, and keep its length when a greedy walk finds it is not a subsequence of the other |
| `find_lus_length_walk.kara` | different lengths give the longer one; words of one length are walked side by side, and the first letter that differs gives that length |
| `find_lus_length_count.kara` | words whose letter counts differ get the longer length at once; only words with the same counts are compared in full |
| `differential.kara` | the four arms against a brute force over every subsequence, five properties |

Every arm prints the same 10 lines: the answer for nine pairs (the
three examples, single letters equal and not, a word with and without
a letter at the end both ways round, a word and its reverse, and a
four-letter word with its first three), then for 3,000 random pairs of
1 to 100 letters from 1 to 3 letters (a third equal, a third the first
word with a letter added, a third unrelated) how many have none and a
checksum over the answers. `find_lus_length.py` mirrors the ★ arm and
its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and a brute force
that lists every subsequence of both words. Each arm is held to the
properties below on 2,000 cases of words from 1 to 3 letters: a short
pair of up to 8 letters for P1 (a third equal, a third with a letter
put in anywhere, a sixth the word back to front, a sixth unrelated), a
long pair of up to 100 for P2, P3 and P5 (a third equal), and the long
word with a letter added at the end for P4.

| | property |
|---|---|
| P1 | the answer is the brute force's, on the short pair |
| P2 | the words the other way round give the same answer |
| P3 | a word with itself has none (`-1`) |
| P4 | a letter added to the end of a word makes the longer word the answer |
| P5 | the answer is `-1` or one word's length |

It prints `2000 cases, 4 arms, 40000 checks, 0 failures` under `karac
__mir-run`.

## Mutation testing

Twelve edits to `differential.kara`, two to each arm that change its
answers, and four that do not, each run under `karac __mir-run`. All
eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the first word's length, not the longer | P1 821, P2 1314, P4 2000 |
| M2 | ★: words of one length count as equal | P1 179 |
| M3 | subseq: a word missing its last letter counts as a subsequence | P1 435, P4 2000 |
| M4 | subseq: the first word kept one letter short | P1 129, P2 1314, P5 656 |
| M5 | walk: only a longer first word skips the walk (`>` for `!=`) | P1 821, P2 1314, P4 2000 |
| M6 | walk: a difference gives the length less one | P1 179, P5 14 |
| M7 | count: the second word's letters added, not taken off | P1 871, P3 2000 |
| M8 | count: words with the same counts never compared | P1 153 |
| E1 | ★: the test turned round | 0 |
| E2 | subseq: the walk's end tested with `>=` | 0 |
| E3 | walk: the letters compared from the end | 0 |
| E4 | count: the words compared the other way round | 0 |

M1 and M5 fail the same checks: both are wrong exactly when the second
word is the longer, M1 giving the first word's length and M5 walking
only the first word's letters. M2 and M6 are wrong on the same 179
short pairs, the different words of one length. M8 takes two words
with the same letters for equal, so only P1's anagram pairs (the word
back to front, and a few unrelated pairs) catch it: before those were
added to the short pairs it failed only 9 checks.

## Verification

Every arm prints the same output as `find_lus_length.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
runs clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints `40000 checks, 0 failures` on the first two and runs clean
under the third. `karac check` passes on every arm, the differential
and the bench program.

On the frozen legacy backends, `karac run --interp` runs the ★, subseq
and walk arms and prints the nine example lines right, but its random
line reads `1006 with none, checksum 779130698`: it draws other words
from the same seed. The likely cause, not checked further, is that it
evaluates `random_word(mut seed, 1 + next_random(mut seed) % 100,
letters)` in another order than v2 and the mirrors do. LLJIT and
legacy `karac build` fail on those three at codegen, "no handler for
method 'len' on variable 'a'", a `Str` parameter. The count arm, the
differential and the bench program are refused at type checking:
legacy types the items of a slice's `iter()` by value, so it refuses
`*c` ("unary '*' requires 'ref T' ... found 'u8'"), and the bench
program's `firsts[i]` is "cannot move out of an index expression".
Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It makes 20,000 random pairs of 1 to
100 letters from 1 to 3 letters once (a third equal, a third the first
word with a letter added, a third unrelated), then answers every pair
in each of 5,000 rounds. Every implementation prints `20000 pairs, 5000
rounds: total 3929935000, checksum 902395218`, the Kāra program under
`karac __mir-run` included (in 197 s).

The C mirror keeps each word's length beside its letters, as Kāra's
strings do, and compares with `memcmp` only when the lengths match.
Spot timings on a shared 4-core container, taken while a corpus run
was busy on it, three runs each (two for Python; `bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.59 to 0.71 s |
| Rust (`rustc -O`) | 0.73 to 0.79 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.63 to 0.68 s |
| Go | 0.71 to 0.80 s |
| Python | 21.2 to 21.7 s |
| Kāra (`karac build --mir`) | 0.91 to 0.96 s |

The legacy `karac build` refuses this program (see Verification). So
`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend. That edit is by hand, on top of the
`scripts/new-bench.sh` output. The `--mir` row is timed at kara
`df61cbfff6`. Under `karac __mir-llvm-run` the program prints the same
line in 5.6 s, compile included; that JITs the MIR's IR without
optimization passes, so it is not a benchmark.

## Compiler findings

None filed. Every arm, the differential and the bench program run
right on the v2 backends, and `karac check` passes on all of them as
first written.
