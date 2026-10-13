# 522. Longest Uncommon Subsequence II

Given an array of strings `strs`, return the length of the longest
uncommon subsequence between them. If the longest uncommon subsequence
does not exist, return `-1`.

An uncommon subsequence between an array of strings is a string that
is a subsequence of one string but not the others.

A subsequence of a string `s` is a string that can be obtained after
deleting any number of characters from `s`. For example, `"abc"` is a
subsequence of `"aebdc"`: delete the `e` and the `d`.

```
strs = ["aba","cdc","eae"]  ->  3
strs = ["aaa","aaa","aa"]   ->  -1
```

**Constraints:** `2 <= strs.length <= 50`; `1 <= strs[i].length <=
10`; `strs[i]` consists of lowercase English letters.

## Approaches

Every arm is `fn find_lus_length(strs: Vec[String]) -> i64`. As in
#521, an uncommon subsequence can be grown back to the whole word it
came from and stay uncommon, so the answer is the length of a whole
word that is a subsequence of no other word in the list, or `-1`.

| file | mechanism |
|---|---|
| `find_lus_length.kara` ★ | the words in order of length, longest first (a stable `sort_by` on their indices); the first one that is a subsequence of no other word gives the answer |
| `find_lus_length_every.kara` | no sorting: test every word against all the others and keep the longest that passes |
| `find_lus_length_longer.kara` | count the words in a `Map`; only words seen once are candidates, and each is tested only against longer words, the only ones that can hold it |
| `find_lus_length_brute.kara` | list every subsequence of every word (at most 2^10 each) in a `Map` with how many words have it; the longest only one word has |
| `differential.kara` | the four arms against the definition, five properties |

Every arm prints the same 8 lines: the answer for seven lists (the two
examples, two words different and equal, a word with a copy, a shorter
and a longer word, a copied word with a word it does not hold, and the
same with an unrelated longer word), then for 1,000 random lists of 2
to 50 words of 1 to 10 letters from 1 to 3 letters, one word in three
a copy of an earlier one, how many have none and a checksum over the
answers. `find_lus_length.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition:
every subsequence of every word, tried against every word with a plain
walk, the longest that exactly one word holds. Each arm is held to the
properties below on 400 cases of words from 1 to 3 letters, one word
in three a copy of an earlier one: a short list of 2 to 8 words of up
to 6 letters for P1, and a long one of 2 to 20 words of up to 10
letters for the rest.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | the list back to front gives the same answer |
| P3 | every word twice has none (`-1`) |
| P4 | the answer is `-1` or the length of a word the list holds once |
| P5 | a word of z's longer than every word in the list is the answer |

It prints `400 cases, 4 arms, 8000 checks, 0 failures` under `karac
__mir-run`.

## Mutation testing

Twelve edits to `differential.kara`, two to each arm that change its
answers, and four that do not, each run under `karac __mir-run`. All
eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the words tried shortest first | P1 107, P5 307 |
| M2 | ★: each word checked only against the words after it | P1 136, P3 400, P4 133 |
| M3 | every: each word checked against itself too | P1 287, P5 400 |
| M4 | every: the last uncommon word kept, not the longest | P1 53, P2 175 |
| M5 | longer: a word seen twice still a candidate | P1 89, P3 307, P4 75 |
| M6 | longer: words of the same length checked too, the word itself among them | P1 287, P5 400 |
| M7 | brute: the subsequences that use the last letter left out | P1 287, P4 190, P5 400 |
| M8 | brute: a subsequence two words have counts as uncommon | P1 89, P3 307, P4 75 |
| E1 | ★: sorted by a key, the negated length | 0 |
| E2 | every: the maximum taken the other way round | 0 |
| E3 | longer: seen more than once written `>= 2` | 0 |
| E4 | brute: the empty subsequence listed too | 0 |

M3 and M6 are the same mistake in two arms: each word is tested against
itself, which always holds it, so every list gets `-1`. M5 and M8 are
another pair: a word the list holds twice counts as uncommon. One edit
first tried as an equivalent was not one: dropping the longer arm's
skip of candidates no longer than the best so far fails P1 53 and P2
175, the same as M4, because the arm then keeps the last candidate that
passes rather than the longest. The skip is what makes `best =
s.len()` a maximum.

## Verification

Every arm prints the same output as `find_lus_length.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
runs clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints `8000 checks, 0 failures` on the first two and runs clean under
the third. `karac check` passes on every arm, the differential and the
bench program.

On the frozen legacy backends, `karac run --interp` runs the longer
arm and prints the seven example lines right, but its random line
reads `260 with none, checksum 273507664`: it draws other lists from
the same seed, as in kata 521, where `random_word(mut seed, 1 +
next_random(mut seed) % 10, letters)` is the likely cause (not checked
further). LLJIT and legacy `karac build` fail on the longer arm at
codegen, "no handler for method 'len' on variable 'small'", a `Str`
parameter. The other three arms, the differential and the bench
program are refused at type checking: legacy types the items of
`iter()` by value, so it refuses `*i` and `*n` ("unary '*' requires
'ref T' ... found 'i64'"), and it calls `strs[i]` passed to a `Str`
parameter a move out of an index. Legacy is frozen, so this is noted,
not filed.

## Benchmarks

The bench program uses the ★ arm. It makes 2,000 random lists of 50
words (the problem's most) of 1 to 10 letters from 1 to 3 letters, one
word in three a copy of an earlier one, once; then solves every list in
each of 100 rounds. Every implementation prints `2000 lists of 50
words, 100 rounds: total 1317600, checksum 34719291`, the Kāra program
under `karac __mir-run` included (in 276 s).

Every mirror does the ★ arm's allocations: a fresh array of indices
sorted stably by length for each list, and the shorter word's letters
collected into a fresh array for each subsequence test. Spot timings on
a shared 4-core container, three runs each (two for Python; `bench.sh`
timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.70 to 0.82 s |
| Rust (`rustc -O`) | 1.73 to 1.89 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.74 to 2.03 s |
| Go | 1.75 to 1.81 s |
| Python | 10.6 to 11.4 s |
| Kāra (`karac build --mir`) | 2.41 to 2.44 s |

The legacy `karac build` refuses this program (see Verification). So
`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend. That edit is by hand, on top of the
`scripts/new-bench.sh` output. The `--mir` row is timed at kara
`df61cbfff6`. Under `karac __mir-llvm-run` the program prints the same
line in 8.0 s, compile included; that JITs the MIR's IR without
optimization passes, so it is not a benchmark.

## Compiler findings

None filed. Every arm, the differential and the bench program run
right on the v2 backends, and `karac check` passes on all of them as
written.
