# 745. Prefix and Suffix Search

Design `WordFilter`, built from a list of `words`, whose `f(pref, suff)`
returns the largest index `i` such that `words[i]` begins with `pref`
and ends with `suff`, or -1 if there is none.

```
WordFilter(["apple"]).f("a", "e")  ->  0
```

**Constraints:** 1 to 10,000 words of 1 to 7 lowercase letters; `pref`
and `suff` are 1 to 7 lowercase letters; at most 10,000 calls to `f`.

## Approaches

Words are short and queries many, so the arms differ in how much work
they move from the queries into the constructor. Each arm is a `struct
WordFilter` with `new(words)` and `f(self, pref, suff)`.

| file | mechanism |
|---|---|
| `prefix_and_suffix_search.kara` ★ | put every pair of a word's prefix and suffix, the empty ones included, joined by `{`, in a `Map[String, i64]`; later words overwrite earlier ones, so each key holds the largest index, and a query is one lookup; at most 64 keys a word |
| `prefix_and_suffix_search_scan.kara` | keep the words and walk them from the last, returning the first with `starts_with` and `ends_with` both true; nothing is built and a query is O(n) |
| `prefix_and_suffix_search_trie.kara` | put suffix + `{` + word, for every suffix of every word, in one trie of 27-way nodes in a flat `Vec`, each node remembering the last word through it; a query walks suff + `{` + pref |
| `prefix_and_suffix_search_lists.kara` | two `Map`s, from every prefix and from every suffix to the rising list of indices of the words that have it; a query merges the two lists from the back until they meet |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 7 lines: the LeetCode example; four small
filters asked several queries each, among them a repeated word, a prefix
and a suffix that overlap within a word, prefixes and suffixes as long
as the whole word, and queries that match nothing; a filter of
10,000 random words of up to 7 letters from `a` to `e` asked
3,000 random queries of up to 4 letters each way, with how many are
found and the sum of their indices; and 300 random filters of up to
10 short words asked 10 queries each, with how many are found and a
checksum. `prefix_and_suffix_search.py` mirrors the ★ arm and its output
is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
which compares each word's first and last letters with the query's
letter by letter and keeps the last word that matches. 3,000 random
filters are checked, each of 1 to 8 words of 1 to 4 letters from `a` to
`c`, asked one query: 1 or 2 random letters each way or, half the time,
a prefix and a suffix of one of the words. 1,642 of the queries are
found.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | the prefix and the suffix written together and added as a last word make that word the answer |
| P3 | every word reversed, asked with the suffix reversed as the prefix and the prefix reversed as the suffix, gives the same answer |
| P4 | every word written twice in a row gives the second copy of the same word, index 2i + 1, or -1 still |

It prints `3000 filters (1642 queries found), 4 arms, 48000 checks,
0 failures` under `karac __mir-run` and `karac __mir-llvm-run`, and the
same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed. Three more edits, E1 to
E3, change nothing that can be seen, and the differential rightly
reports no failure for them.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the first word with a key kept, not the last | P1 303, P2 1642, P4 1642 |
| M2 | ★: the key's second half a prefix, not a suffix | P1 862, P2 1891, P3 776 |
| M3 | ★: the whole word never a prefix | P1 790, P3 450 |
| M4 | scan: the last word never tried | P1 580, P2 3000, P4 580 |
| M5 | scan: the suffix tested against the prefix | P1 995, P2 1878, P3 1270 |
| M6 | scan: either match enough | P1 1473 |
| M7 | trie: a node keeping the first word through it, not the last | P1 303, P2 1642, P4 1642 |
| M8 | trie: the whole word never put in as a suffix | P1 772, P3 450 |
| M9 | trie: the word after the '{' put in reversed | P1 1063, P2 1896, P3 374 |
| M10 | lists: the suffix lists holding prefixes | P1 862, P2 1891, P3 776 |
| M11 | lists: the merge stepping past the smaller index | P1 518 |
| M12 | lists: the last word with the prefix skipped | P1 1345, P2 3000, P3 443, P4 1345 |
| E1 | scan: the suffix tested before the prefix | 0 |
| E2 | ★: no keys with an empty prefix | 0 |
| E3 | trie: the root not marked with the word | 0 |

P1 kills all twelve. M1 and M7 are one mistake in two arms, the first
matching word kept instead of the last, and fail exactly the same
checks; so do M2 and M10, which file prefixes where suffixes belong.
P2 sees every edit that can miss the added word, which matches by
construction and is the last: keeping the first match (M1, M7), never
trying the last word (M4, which fails all 3,000), skipping the last
prefix match (M12, likewise), mixing up the two halves of a key
(M2, M5, M9, M10). P4 sees the same first-or-last mistakes from the
other side, since of two copies the second is the answer:
M1, M4, M7, M12. P3 sees the edits that treat prefixes and suffixes
unalike: M3 and M8 leave out the whole word on one side only,
M2, M5, M9 and M10 confuse the two sides, and M12 skips a candidate on
the prefix side only. M6 lets either half match and M11 steps the merge
past the wrong index; P1 alone sees them. E1 tests the suffix before the
prefix; E2 drops the keys with an empty prefix, which no query asks for
since every prefix has at least one letter; E3 leaves the trie's root
unmarked, and no query ends at the root since every suffix has at least
one letter.

## Verification

Every arm prints the same output as `prefix_and_suffix_search.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The debug build that
runs `__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` and the
release build that runs `check` and `__mir-run` are both at kara
`1d96cab833`, whose last compiler change is `afe886a96d`. The runtime
archives were built after the last runtime change, `b09cd37112`.

Since kara `3c8e763161` (B-2026-10-18-31) the sanitizer lane sees leaks
itself. The leak check also copied each arm's and the differential's
lane executable as it was linked and ran it with the preloaded shim from
kata 708, which refuses the lane's hand-made stack so that LeakSanitizer
sees `main`: all five print their output and report no leak.

The frozen legacy backends refuse every program here. The trie arm and
the differential stop at type checking, at a `*` over a vector's
`iter()` (`*b` over a word's bytes), since legacy gives those by value
where v2 gives references, and the lists arm at its `Map.get_mut`, which
legacy's `Map` lacks. The ★ and scan arms and the bench program
type-check but stop at the harness's `as_str()`: the legacy interpreter
has no `as_str` on a `String`, and legacy code generation does not
support it, so `karac run` and `karac build` fail too. Legacy is frozen,
so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. In each of
5 rounds it builds a filter of 10,000 random words of up to 7 letters
from `a` to `e`, the most words LeetCode allows, and asks 10,000 random
queries of up to 4 letters each way, so that the constructor's key
insertions, about 290,000 a round, weigh more than the queries. Each
language uses its own standard hash map with owned string keys: Kāra's
`Map` and Rust's `HashMap`, both SipHash-1-3, Go's `map` and Python's
`dict`; C has none, so its version is a hand-written open-addressing
table hashed by FNV-1a, which makes C's time a measure of that table as
much as of C. Every implementation prints `5 rounds of 10000 words and
10000 queries: 31461 found, indices sum to 256968507`, the Kāra program
under `karac __mir-run` included (in 4.6 s).

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and two of Python (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.24 to 0.27 s |
| Rust (`rustc -O`) | 0.30 to 0.41 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.31 to 0.36 s |
| Go | 0.29 to 0.38 s |
| Python | 0.68 to 0.70 s |
| Kāra (`karac build --mir`) | 0.29 to 0.38 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend; the legacy `karac build` refuses it (above). That
edit is by hand, on top of the `scripts/new-bench.sh` output. Under
`karac __mir-llvm-run` the program prints the same line in 2.7 s,
compile included; that JITs the MIR's IR without optimization passes, so
it is not a benchmark.

So at the medians of the interleaved runs the v2 build, Rust with and
without overflow checks and Go are level (0.33 s, 0.34, 0.33 and
0.33), and C's hand-written table is about a quarter faster
(0.25). Under valgrind's cachegrind v2 runs 1.9 billion instructions
against C's 0.9 and Rust's 1.3, and 0.27 billion branches against
0.16 and 0.18, with about the same mispredictions (11 million against
10 and 10); the bench spends its time in hashing and allocating, and
v2's extra instructions were not traced further. The legacy build
refuses the program, so there is no legacy time to set against M2's
limit; new katas' benches are outside M2's frozen set in any case. The
comparison with C and Rust waits until after M4.

## Compiler findings

None new.
