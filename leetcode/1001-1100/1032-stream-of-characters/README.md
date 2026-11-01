# 1032. Stream of Characters

Design an algorithm that accepts a stream of characters and checks if a
suffix of these characters is a string of a given array of strings
`words`. Implement the `StreamChecker` class: `StreamChecker(words)`
initializes the object with the strings array `words`, and
`query(letter)` accepts a new character from the stream and returns
`true` if any non-empty suffix from the stream forms a word that is in
`words`.

```
words = ["cd","f","kl"], queries a b c d e f g h i j k l
  ->  false false false true false true false false false false false true
```

**Constraints:** 1 to 2,000 words of 1 to 200 lowercase English
letters; each query is a lowercase English letter; at most 40,000
queries.

## Approaches

| file | mechanism |
|---|---|
| `stream_checker.kara` ★ | a trie of the reversed words: put every word in backwards and, on each query, walk the stream back from the newest letter through the trie until a word ends or an edge is missing. O(longest word) per query |
| `stream_checker_sets.kara` | a set of the words: keep the words in a `Set[String]` and the lengths they come in, and look up the stream's last that many letters, `substring`, for every length. O(lengths x longest word) per query |
| `stream_checker_aho.kara` | an Aho-Corasick automaton: a forward trie with failure links found breadth-first through a `VecDeque`, a move for every letter at every node, and a match flag passed down the failure links. One move per query |
| `stream_checker_active.kara` | every match still open: a forward trie and the nodes reached by the suffixes of the stream that are still prefixes of some word; each query moves them all along its letter and starts one more at the root. O(longest word) per query |
| `stream_checker_endings.kara` | the words by their last letter: a `Map[char, Vec[String]]`, and on each query only the words ending in that letter are asked whether the stream `ends_with` them |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 14 lines: the answers, `T` or `F` per query,
for six word lists and streams, LeetCode's example among them; for six
groups of random checkers (1,000 of 3 words up to 3 letters over 2
letters with 30 queries, down to 2 of 2,000 words up to 200 letters
over 26 letters with 20,000 queries), how many queries found a word and
a checksum of the answers; and two of the largest cases: `"a"`, and 200
a's with `"b"`, each against 40,000 a's. `stream_checker.py` mirrors
the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: after each letter, whether some word is exactly the last as
many letters of the stream, compared letter by letter. It checks 666
cases: every set of one or two words of one or two letters over a and b
against every stream of four letters (336), then 300 random cases of up
to 8 words of up to 4 letters with streams of up to 30 letters, and 30
of up to 50 words of up to 15 letters with streams of 300, over 2 to 4
letters. Each case is also asked with the words in the opposite order,
each given twice; with one more word holding a `z`, which no stream
has; by a fresh checker on the first half of the stream; and with one
more word, a random piece of the stream.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the order of the words and repeats of them do not matter |
| P3 | a word that never occurs changes no answer |
| P4 | each answer depends only on the stream so far: a fresh checker asked the first half answers the first half the same |
| P5 | one more word turns `F` into `T` exactly where it ends, and nowhere else |
| P6 | each arm agrees with at least two of the other four |

The differential prints `666 cases: checksum 761281467, 19980 checks
over 5 arms: 0 failures` under `karac __mir-run` (5.4 s), `karac
__mir-llvm-run` and `karac __mir-llvm-asan` with no error.

## Mutation testing

Thirty edits to the differential, each run under `karac __mir-run` and
`karac __mir-llvm-run`. Fifteen are kept, three to each arm. All fifteen
are killed, each fails the same checks under both backends, and no two
kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a word found only when it is the whole stream | P1 535, P5 570, P6 535 |
| M2 | ★: a new edge pointing at the node before | P1 376, P2 204, P5 70, P6 376 |
| M3 | ★: the newest letter put first in the stream | P1 483, P5 297, P6 483 |
| M4 | sets: only the first word's length tried | P1 244, P2 299, P5 356, P6 244 |
| M5 | sets: the stream's ending read one letter short | P1 471, P3 82, P5 407, P6 471 |
| M6 | sets: words cut to 20 letters | P5 11 |
| M7 | aho: matches never passed down the failure links | P1 135, P3 39, P5 183, P6 135 |
| M8 | aho: every failure link to the root | P1 228, P3 43, P5 236, P6 228 |
| M9 | aho: a missing edge restarts at the root | P1 149, P3 15, P5 104, P6 149 |
| M10 | active: no match ever started | P1 578, P5 666, P6 578 |
| M11 | active: the node before the move asked | P1 578, P3 33, P5 583, P6 578 |
| M12 | active: stops at the first match, leaving the rest unmoved | P1 216, P5 142, P6 216 |
| M13 | endings: the words filed by their first letter | P1 238, P5 135, P6 238 |
| M14 | endings: a word anywhere in the stream | P1 175, P5 55, P6 175 |
| M15 | endings: only the first word for each last letter kept | P1 189, P2 283, P5 302, P6 189 |

P5 kills all fifteen, and P1 and P6 fourteen. M6 is the one only P5
sees: the words the cases draw have at most 15 letters, and only P5's
extra word, a piece of the stream, can be longer than 20. P3 kills the
five whose answers change when an extra word adds nodes to a trie or
lengths to a set, though the word never matches: three aho edits, sets
reading one letter short (M5), and active asking the node before the
move (M11). P2 kills the three that depend on which word comes first:
a new edge pointing at whatever node was made before (M2), only the
first word's length tried (M4), and only the first word for each last
letter kept (M15). P4 kills none: no edit here makes an answer depend
on letters not yet seen. The checks draw random numbers for every case
whatever the answers, so every mutant sees the same cases and their
counts can be compared.

Fifteen other edits were tried and set aside. Two change no answer and
are equivalent: active restarting a dead match at the root (the root is
no word's end, and the new match starts there anyway) and putting the
new match first. One stops on an index out of bounds (exit 101) under
both backends: aho filling the failure links from a stack, which can
read a move before it is filled in. One does not compile, and found a gap: sets
asking `self.stream.substring(0, len)`, with `len` a `ref i64` from
`self.lengths.iter()`, is refused with "'substring' expects integer
byte indices, found 'ref i64'", where `n - len` and a user function's
`i64` parameter take it. That is kara `B-2026-11-01-4`; the arm itself
writes `substring(n - len)`, which checks. The other eleven were
killed too, beyond three per arm. Seven fail as another does: ★ never
reading the stream's first letter and sets never finding a word as long
as the stream (`P1 319, P5 211, P6 319`); ★ never marking one-letter
words and endings never finding them (`P1 373, P5 276, P6 373`); aho
passing a node's match to itself, which is M7; and aho starting every
query at the root and active dropping its open matches after every
query (`P1 335, P5 236, P6 335`). Four fail on their own: ★ putting the
words in forwards, sets never trying the first length, endings needing
every word ending in the letter, and endings adding every letter twice.

## Verification

Every arm prints the same output as `stream_checker.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and under
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. The differential prints its line under all three. `karac run` and
a `karac build` binary print the same output for every arm and the
differential. `karac check --output=json` flagged the ★ draft's harness
three ways. Two f-strings escaped their quotes inside an interpolation
(E0001) and two `*c` derefs were on a `char` (E0209). All four came
with machine-applicable replacements. `karac fix` applied the two
f-string ones, and the two derefs were dropped by hand, together with
the harness copy the other arms share. The
third was `i64 as char` (E0210, `E_INT_AS_CHAR`), which names
`char.try_from` and offers no replacement; the harness casts through
`u8`, as other katas do. Every file then checks clean. The release build is kara
`6697158faf`, with runtime archives rebuilt at that commit. Under
`karac __mir-run` the arms take 7.9 s (★) to 14.4 s (sets).

## Benchmarks

The bench draws 2,000 random words of 50 to 200 letters and a
40,000-letter stream over a and b once, in all five languages, then 50
times builds the ★ checker from the words and asks it every letter of
the stream, folding the answers into a count and a checksum. Each node
of the trie is its own 26-entry row: a `Vec` in Kāra and Rust, a slice
in Go and a list in Python. C keeps the rows in one `realloc`'d array.
Every implementation prints `2000 words, 40000 queries, 50 rounds: 28350
found, checksum 460234650`.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with karac as above:

| | time | median |
|---|---|---|
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.956 to 1.144 s | 1.035 s |
| Kāra (`karac build`) | 0.952 to 1.151 s | 1.049 s |
| C (`clang -O3`) | 1.367 to 1.802 s | 1.641 s |
| Rust (`rustc -O -C overflow-checks=on`) | 2.367 to 2.750 s | 2.458 s |
| Rust (`rustc -O`) | 2.301 to 2.663 s | 2.543 s |
| Go | 2.527 to 2.702 s | 2.655 s |
| Python | 15.2 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here
(its user time stays below its real time) and runs as fast as the
sequential one.

Kāra's lead is the allocator's settings, not its code. Each round
builds and frees about 250,000 rows. Rust and C, on glibc's defaults,
hand the freed memory back to the kernel and fault it in again the
next round: 710,031 and 599,011 minor page faults, 1.1 and 1.0 s of
system time. Kāra's runtime raises glibc's trim threshold at start-up
(`mallopt`, kara `runtime/src/lib.rs`), so it keeps that memory: 14,523
faults and 0.03 s of system time. With `KARAC_MALLOC_TUNE=0`, which
turns that off, the Kāra binary takes 2.24 to 2.46 s over three runs,
level with Rust. Callgrind counts 6.55 billion instructions for Kāra
and 6.56 billion for Rust, about half of each in glibc's `malloc` and
`free`, against 0.79 billion for C's single array.
