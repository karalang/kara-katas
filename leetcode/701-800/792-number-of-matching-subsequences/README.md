# 792. Number of Matching Subsequences

Given a string `s` and a list of words, count the words that are
subsequences of `s`: those that can be spelled by deleting letters from
`s` and keeping the rest in order. A word that is in the list more than
once counts each time.

```
s = "abcde"
words = ["a", "bb", "acd", "ace"]  ->  3

s = "dsahjpjauf"
words = ["ahjpjau", "ja", "ahbwzgqnuk", "tnmlanowax"]  ->  2
```

**Constraints:** `s` has 1 to 50,000 lowercase letters, and there are 1
to 5,000 words of 1 to 50 lowercase letters each.

## Approaches

| file | mechanism |
|---|---|
| `num_matching_subseq.kara` ★ | every word at once: each word waits in the bucket of the next letter it needs, as a (word, letters matched) pair; walking `s`, each letter's bucket is emptied with `mem.take` and its words move on one letter, into the bucket of the letter after, or are counted; O(\|s\| + total length of the words) |
| `num_matching_subseq_table.kara` | a table of next places, `next[i * 26 + c]` the first place at or after `i` with letter `c`, filled from the end of `s` back; each word walks it, one look-up a letter; O(26 \|s\| + total length) |
| `num_matching_subseq_search.kara` | the places of each letter of `s` in order, and for each letter of a word a binary search for the first place at or after the last one found; O(\|s\| + total length × log \|s\|) |
| `num_matching_subseq_memo.kara` | two pointers, the word's and `s`'s, run once for each different word, the answer kept in a `Map` and given again for its repeats; O(\|s\| × different words) |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 6 lines: LeetCode's two examples; a one-letter
`s` with a word in the list twice; `s` of five `a`s and words of `a`s up
to one longer than it; words that keep `s`'s order and words that
reverse it; and 300 random cases, `s` of 1 to 300 letters over the first
1 to 26 letters of the alphabet and 1 to 50 words, a quarter of them
repeats of an earlier word, a quarter pieces of `s` of up to 50 letters
and the rest random words of 1 to 8 letters, with the matching words in
all and a checksum. `num_matching_subseq.py` mirrors the ★ arm and its
output is byte-identical.

`Vec.binary_search` returns `Option[i64]`, whether the value is there
(docs/design.md), and gives no place to insert it, so the search arm
writes out its search for the first place at or after.

## Differential

`differential.kara` holds copies of the four arms and the definition: a
word matches when the number of ways to spell it from `s`, counted by
dynamic programming over the letters of `s` and held at a billion, is
not 0. Its 1,600 cases have `s` of 1 to 40 letters and 1 to 15 words, a
quarter of them repeats; a quarter are over a random number of letters,
a quarter have `s` over one or two letters, so that words can be spelled
in very many ways, a quarter have most words pieces of `s`, and a
quarter have words over more letters than `s` and up to three letters
longer than it.

| | property |
|---|---|
| P1 | the count is the definition's |
| P2 | the same words in a random order give the same count |
| P3 | adding `s` itself and a piece of `s` to the words adds 2 |
| P4 | more letters after `s` never lower the count |

It prints `1600 cases (12977 words, 5893 matching), 4 arms, 25600
checks, 0 failures` under `karac __mir-run` and `karac __mir-llvm-run`,
and the same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a word done a letter early | P1 287 |
| M2 | ★: every word started in the bucket of its last letter | P1 454, P3 1137 |
| M3 | ★: a word moved to its next bucket without counting the letter | P1 947, P3 1566 |
| M4 | table: each place pointing one past its own letter | P1 663, P3 1600 |
| M5 | table: a letter of s used twice | P1 212 |
| M6 | table: each place seeing only its own letter | P1 814, P3 1244 |
| M7 | search: the first place after, not at or after | P1 653, P3 1600 |
| M8 | search: a letter of s used twice | P1 212 |
| M9 | search: the search never says there is none | P1 522 |
| M10 | memo: the word's letter moved on when it differs | P1 1317, P3 1600 |
| M11 | memo: every repeat taken as matching | P1 731 |
| M12 | memo: a word matched once its first letter is | P1 1053 |

P1 kills all twelve. P3 kills the six that can miss a word that does
match, `s` itself among them; the other six only count words that do not
match, and adding two words that do still adds 2. P2 and P4 kill none:
no edit makes the count depend on the order of the words, and none makes
more letters after `s` lose a word.

## Verification

Every arm prints the same output as `num_matching_subseq.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The debug build that
runs `__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` and the
release build that runs `check` and `__mir-run` are both at kara
`cfbbf3e8eb`, whose last compiler change is `b115567cf2`. The runtime
archives were built after the last runtime change, `176f59738b`.

Since kara `3c8e763161` (B-2026-10-18-31) the sanitizer lane sees leaks
itself. The leak check also copied each arm's and the differential's
lane executable as it was linked and ran it with the preloaded shim from
kata 708, which refuses the lane's hand-made stack so that LeakSanitizer
sees `main`: all five print their output and report no leak.

The frozen legacy backends refuse all four arms and the differential at
the type check, at the harness's `word.push(*b as char)` over `t.iter()`
and the memo arm's `Some(known) => *known`, since they take those items
for `u8` and `bool` rather than references. With those `*`s removed, the
legacy `karac build` still fails: it panics in its `for` lowering on the
★ arm's `for b in s.bytes()` over a `Str` parameter, it has no handler
for `bytes` on a `Str` parameter in the other three, and it does not
lower `mem.take` of a `Vec`. Copies with the parameters written `ref
String` and `ref Vec[String]`, and with the `mem.take` written
`mem.replace(mut waiting[c], Vec.new())` after binding the index to `c`
(legacy refuses `mem.replace` on the index written in place), print the
same output as v2 under the legacy JIT (`karac run`), `karac build` and
an auto-par build. Under the legacy interpreter (`karac run --interp`)
the arms agree with each other and the differential reports no failure,
but over other random cases: the sixth line is `300 random cases: 6507
matching words, checksum 175393594`. In `random_word(mut seed, 1 +
next_random(mut seed) % 300, letters)` the legacy interpreter hands
`random_word` the seed as it was before the second argument drew from
it, and keeps only what `random_word` writes back. Legacy also refuses
the bench program's `num_matching_subseq(strings[r % 16], lists[(r / 16)
% 64])` as moves out of an index; a copy with the same `ref` parameters
and `mem.replace` builds and prints the same line, and the bench timing
below is of it. Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. 16 strings of
50,000 letters, LeetCode's longest, each over the first 13 to 26 letters
of the alphabet, and 64 lists of 5,000 words, LeetCode's most, each word
of 1 to 50 letters over all 26, are made once. Each of 4,000 rounds
counts the words of one list that one string spells, so a word matches
only when all its letters are among the string's. Every implementation
prints `4000 rounds of 5000 words: 4021328 matching, checksum
763716988`, the Kāra program under `karac __mir-run` included (in 14
minutes).

The bench measures pushing small pairs onto many short vectors and
taking them back, 50,000 times a round. Kāra and Rust take a bucket
whole with `mem.take`, Go sets the slice to `nil`, C moves the bucket's
array out and frees it once walked, and Python swaps in a new list. Spot
timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and two of Python (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 2.08 to 2.37 s |
| Rust (`rustc -O`) | 2.24 to 2.65 s |
| Rust (`rustc -O -C overflow-checks=on`) | 2.15 to 2.75 s |
| Go | 3.77 to 4.27 s |
| Python | 38.94 to 42.53 s |
| Kāra (`karac build --mir`) | 1.85 to 2.32 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, since the legacy `karac build` refuses it (see
Verification); that edit is by hand, on top of the
`scripts/new-bench.sh` output. Under `karac __mir-llvm-run` the program
prints the same line in 8.1 s, compile included; that JITs the MIR's IR
without optimization passes, so it is not a benchmark.

At the medians of the interleaved runs the v2 build takes 2.15 s, the
same as C's 2.15, against Rust's 2.41 (2.45 under overflow checks) and
Go's 3.96. Under valgrind's cachegrind v2 runs 14.5 billion instructions
and 2.85 billion branches, against C's 13.0 billion and 2.07 billion and
Rust's 15.8 billion and 2.67 billion, and it mispredicts 41 million
branches to C's 62 million and Rust's 80 million. Why v2's mispredicts
are fewer is not profiled. The legacy build of the copy ran 1.76 to 2.07
s, a median of 1.94 s in the interleaved runs, so v2 takes 1.11 times
legacy. The comparison with C and Rust waits until after M4.

## Compiler findings

Nothing new in v2.
