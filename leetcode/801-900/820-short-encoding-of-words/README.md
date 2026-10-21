# 820. Short Encoding of Words

A valid encoding of an array of `words` is a reference string `s`,
ending in `'#'`, and an array of indices such that each word is the text
of `s` from its index up to the next `'#'`. Return the length of the
shortest reference string of any valid encoding of `words`.

```
words = ["time", "me", "bell"]  ->  10     s = "time#bell#", indices [0, 2, 5]
words = ["t"]                   ->  2      s = "t#"
```

**Constraints:** `1 <= words.length <= 2000`, `1 <= words[i].length <=
7`, and the words are lower-case English letters.

## Approaches

A word read from an index up to the next `'#'` is the end of the text
before that `'#'`, so a word can share the place of any word it ends,
and a word that ends no other word needs a place of its own: its letters
and a `'#'`. The answer is the sum of `length + 1` over the distinct
words that are not the end of a longer word.

| file | mechanism |
|---|---|
| `short_encoding.kara` ★ | every word in a set, then every proper suffix of every word taken out of it; the words left each cost their length and a `'#'`. O(n L^2) for n words of up to L letters |
| `short_encoding_trie.kara` | a trie of the words inserted back to front, in flat arrays of 26 child slots a node; a word whose last node has no children needs a place, and equal words, which end at one node, count once. O(n L) |
| `short_encoding_sort.kara` | the words reversed and sorted, so that every word a reversed word begins comes right after it; a reversed word that the next one starts with needs no place. O(n L log n) |
| `short_encoding_iter.kara` | the distinct words `collect`ed into a set, the ones no longer word `ends_with` kept by a `filter` over an `any`, and their costs added by a `sum`. O(n^2 L) |
| `differential.kara` | the four arms against the statement read letter by letter off the words, four properties |

Every arm prints the same 11 lines: LeetCode's two examples; six small
cases (a word twice; a word twice with two of its endings; three words
of one letter; endings of two words; a word with a reversed copy of
another; and words that end each other in pairs); two lists of
LeetCode's largest, 2,000 words of up to 7 letters, one of three
letters, where most words end others, and one of all 26; and 300 random
lists of up to 20 words of two letters, with a total and a checksum.
`short_encoding.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement
played out on the words: a word needs a place unless a longer word, or
an equal word earlier in the list, has the same letters at its end,
compared letter by letter from the back; each place is the word and a
`'#'`. It keeps no set, no trie and no sorted list. Its 1,600 cases come
in four kinds of 400: up to 30 words of two letters, which often end
each other or repeat; up to 30 of fifteen letters, which seldom do; one
to three long words of three letters mixed with their endings and some
short words; and up to 60 words of four letters. 1,402 cases have a word
that needs no place.

| | property |
|---|---|
| P1 | the statement's answer |
| P2 | the list reversed gives the same answer |
| P3 | the list with an ending of one of its words added gives the same answer |
| P4 | the list mixed with a second list over the letters `p` to `s`, which the first never uses, gives the sum of the two answers |

It prints `1600 cases (1402 with a word that needs no place), 25600
checks over 4 arms: 0 failures` under `karac __mir-run` and `karac
__mir-llvm-run`, and the same under `karac __mir-llvm-asan` with no
error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a word takes itself out | P1 1600, P4 1600 |
| M2 | ★: the `'#'` not counted | P1 1600, P4 1600 |
| M3 | ★: the last letter never taken out | P1 1253, P3 174, P4 636 |
| M4 | trie: equal words counted twice | P1 521, P3 320, P4 66 |
| M5 | trie: words inserted front to back | P1 1201, P3 411, P4 636 |
| M6 | trie: a node with one child counted | P1 1278, P3 470, P4 596 |
| M7 | sort: words not reversed | P1 1201, P3 411, P4 636 |
| M8 | sort: equal words counted twice | P1 1010, P3 944, P4 142 |
| M9 | sort: the list not sorted | P1 1357, P2 957, P3 1139, P4 951 |
| M10 | iter: the `'#'` not counted | P1 1600, P4 1600 |
| M11 | iter: a word that begins another dropped | P1 1201, P3 411, P4 636 |
| M12 | iter: a word one letter shorter never inside | P1 692, P3 184, P4 125 |

P1 kills all twelve, and P2 sees only M9: every other arm, and every
other mistake, gives the same answer in any order, while the unsorted
sort arm compares each word with whichever happens to follow it. M5, M7
and M11 fail on exactly the same cases. They are one mistake made three
ways, finding the words that begin others rather than end them, by a
trie built from the front, by a sort of the words as written, and by
`starts_with`. P4 sees M1, M2 and M10 on every case: an arm that answers
0, or leaves out the `'#'`s, is off by the second list's share too.

## Verification

Every arm prints the same output as `short_encoding.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The debug build that
runs `__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` is at kara
`385539fdac`, with the runtime archives built from that tree; the
release build that runs `check` and `__mir-run` is at `d5daf8420c`, two
compiler changes ahead of it (`b2ead3a82f`, `8dd3fa3bd1`).

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all five print their output and report no leak.

The frozen legacy interpreter (`karac run --interp`) prints the output
of the ★ and sort arms. The legacy JIT (`karac run`) and `karac build`
panic in codegen on the ★ arm, finding an integer where they expect the
`String` that `word[k..]` views, and refuse the sort arm's
`chars().rev()`. Legacy refuses the trie arm and the differential, as it
types the items of a `Vec[u8]`'s `iter()` as values and so refuses their
`*`, and the bench program, as it takes `lists[round % count]` passed to
a function as a move out of an index. Its interpreter finds no `cloned`
for the iterator arm, and its codegen no `collect`. Legacy is frozen, so
this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. It draws 64
lists once, each of 2,000 words of up to 7 letters, LeetCode's largest,
over five letters so that many words end others. Each of 12,000 rounds
answers the next list afresh: 2,000 inserts into a hash set and up to 6
removals for each word, so the work is hashing short strings and probing
the set. Every implementation prints `12000 rounds of 64 lists of 2000
words: total 70409075, checksum 234109170`, the Kāra program under
`karac __mir-run` included, in 164 s with the interpreter's step limit
raised by `KARAC_MIR_MAX_STEPS`.

Spot timings on a shared 4-core container, six runs of each compiled
program and nine of v2's, five of them interleaved, and one of Python
(`bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 2.14 to 2.28 s |
| Rust (`rustc -O`) | 2.57 to 2.95 s |
| Rust (`rustc -O -C overflow-checks=on`) | 2.61 to 2.74 s |
| Go | 3.63 to 3.98 s |
| Python | 10.9 s |
| Kāra (`karac build --mir`) | 4.99 to 5.32 s |

The legacy backend refuses the program (Verification), so there is no
legacy time. `bench.sh` builds the Kāra program with `karac build
--mir`, the v2 compiled backend; that edit is by hand, on top of the
`scripts/new-bench.sh` output.

At the medians of the interleaved runs v2 takes 5.25 s, against C's
2.19, Rust's 2.66 (2.69 under overflow checks) and Go's 3.82, so about
2.4 times C's time and twice Rust's. Under valgrind's cachegrind v2 runs
36.5 billion instructions, against C's 10.8 billion and Rust's 20.1
billion, and 5.4 billion branches against C's 2.6 billion and Rust's 1.5
billion. Where the extra instructions go is not traced; the C mirror
hashes with FNV-1a and Rust and v2 with SipHash-1-3, so part of the gap
to C is the hash. Built for `x86-64-v3`, the target `karac build` uses,
C takes 2.05 to 2.16 s and Rust with overflow checks 2.56 to 2.68 s,
against v2's 4.94 to 5.12 s in the same five interleaved runs. Python
takes 10.9 s, about five times C's time. The comparison with C and Rust
waits until after M4.

## Compiler findings

Nothing new in v2: every arm, the differential and the bench program run
on every v2 lane as written, and in the first spelling tried. The ★ arm
cuts each ending with `word[k..]`, a `Str` view, and passes it to
`Set.remove` with no copy, by the library's lookup by view.
