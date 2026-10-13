# 524. Longest Word in Dictionary through Deleting

Given a string `s` and a string array `dictionary`, return the longest
string in the dictionary that can be formed by deleting some of the
characters of `s`. If there is more than one, return the longest word
with the smallest lexicographical order. If there is none, return the
empty string.

```
s = "abpcplea", dictionary = ["ale","apple","monkey","plea"] -> "apple"
s = "abpcplea", dictionary = ["a","b","c"]                   -> "a"
```

**Constraints:** `1 <= s.length <= 1000`; `1 <= dictionary.length <=
1000`; `1 <= dictionary[i].length <= 1000`; `s` and `dictionary[i]`
consist of lowercase English letters.

## Approaches

Every arm is `fn find_longest_word(s: Str, dictionary: Vec[String]) ->
String`. A word can be formed by deleting letters of `s` exactly when
it is a subsequence of `s`, so the answer is the best word, longest
first and then smallest, that is one.

| file | mechanism |
|---|---|
| `find_longest_word.kara` ★ | keep the best word so far, and walk `s` only for a word that would beat it |
| `find_longest_word_sorted.kara` | sort a copy of the dictionary, longest first and then smallest; the first word that is a subsequence is the answer |
| `find_longest_word_table.kara` | a table of where each letter next appears after each place in `s`, so a word is matched one jump per letter |
| `find_longest_word_waiting.kara` | walk `s` once with every word in hand: each word waits in the bucket of the next letter it needs, and moves on when `s` shows it |
| `differential.kara` | the four arms against the definition, five properties |

Every arm prints the same 10 lines: the answer for eight cases (the
two examples, no word that fits, a tie between two words of one
length, a word the same as `s` given twice, a word longer than `s`, a
single letter, and three ties with a longer word that does not fit),
then for 1,000 random cases (`s` of 1 to 60 letters from 1 to 4
letters, and 1 to 30 words of 1 to 8 letters, a third of them taken
from `s`) how many have none and a checksum over the answers, and last
the largest case: `s` of 1,000 letters and 1,000 words of up to 1,000
letters, half of them taken from `s`. `find_longest_word.py` mirrors
the ★ arm and its output is byte-identical.

The waiting arm empties a bucket with `mem.replace(mut waiting[c],
Vec.new())`, the spelling core-semantics.md §3.7 gives. Until kara
B-2026-10-13-25 (below) was fixed, no checker or backend resolved it.
Its first spelling, `take(mut waiting[c])`, was refused for another
reason: `take` needs `T: Default`, and no `Vec` had one (kara
B-2026-10-13-27, below, since fixed). So the checks of that arm and of
the differential below were first run on copies that wrote the bare
`replace(...)`, the only change. Rechecked at kara `2b8238c108`: the
files as they stand pass `karac check`, print the same as before under
`karac __mir-run` and `karac __mir-llvm-run`, and run clean under `karac
__mir-llvm-asan`.

## Differential

`differential.kara` holds copies of the four arms and the definition:
every subsequence of `s` listed in a `Set`, and the best word of the
dictionary among them. Each arm is held to the properties below on
1,000 cases of words from 1 to 3 letters, a third of the words taken
from `s`: a short case of up to 10 letters and 10 words for P1, and a
longer one of up to 60 letters and 30 words for the rest.

| | property |
|---|---|
| P1 | the answer is the definition's, on the short case |
| P2 | the dictionary back to front gives the same answer |
| P3 | with `s` itself put in the dictionary, `s` is the answer |
| P4 | without every copy of the answer, the answer is no better |
| P5 | `s` and every word back to front give an answer just as long |

It prints `1000 cases, 4 arms, 20000 checks, 0 failures` under `karac
__mir-run`.

## Mutation testing

Twelve edits to `differential.kara`, two to each arm that change its
answers, and four that do not, each run under `karac __mir-run`. All
eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: words of one length, the larger kept | P1 56, P4 21 |
| M2 | ★: a word missing its last letter counts as a subsequence | P1 197, P3 43, P5 13 |
| M3 | sorted: the words sorted shortest first | P1 640, P3 967, P4 640 |
| M4 | sorted: words of one length sorted largest first | P1 56, P4 21 |
| M5 | table: each row starts empty, not copied from the next | P1 226, P5 78 |
| M6 | table: a letter of `s` used twice (`pos = at`) | P1 298, P3 57 |
| M7 | waiting: a word done one letter early | P1 187, P3 42, P5 13 |
| M8 | waiting: a word moved to the bucket of the letter it just matched | P1 353, P3 650, P5 252 |
| E1 | ★: the test written from the best word's side | 0 |
| E2 | sorted: the loop's two bounds tested the other way round | 0 |
| E3 | table: the end tested with `>=` | 0 |
| E4 | waiting: a tie kept with `<=` | 0 |

M1 and M4 are one mistake in two arms, and fail the same checks: of
two words of one length, both keep the larger. M2 and M7 are another
pair, a word one letter short of matching counted as matched; M2
fails 11 checks more because it also takes a one-letter word whose
letter `s` lacks, while M7 moves a word on only once its first letter
is seen. P2 kills none of the eight: each mutant still picks
its answer by a fixed rule, so the order of the dictionary does not
change it. P2 is there for a mistake none of these make, keeping the
first word of the best length rather than the smallest.

## Verification

The ★, sorted and table arms print the same output as
`find_longest_word.py` under `karac __mir-run` (the v2 MIR
interpreter) and `karac __mir-llvm-run`, and run clean under `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer): output
identical, no error, no leak. The waiting arm and the differential
stop at `mem` on every backend (above); on the copies that write
`replace`, the waiting arm does the same as the other three, and the
differential prints `20000 checks, 0 failures` on both v2 backends and
runs clean under the third. `karac check` passes on the ★, sorted and
table arms, the bench program and both copies.

On the frozen legacy backends, `karac run --interp` runs the ★ and
sorted arms and prints the eight example lines right, but its random
line reads `6 with none, checksum 910364937`: it draws other cases
from the same seed, as in kata 521, where `random_word(mut seed, 1 +
next_random(mut seed) % 60, letters)` is the likely cause (not checked
further). LLJIT and legacy `karac build` fail on those two at codegen,
"no handler for method 'len'" and "'bytes' on variable 'word'", a
`Str` parameter. The table arm is refused at type checking: legacy
types the items of a slice's `iter()` by value, so it refuses `*b`
("unary '*' requires 'ref T' ... found 'u8'"). The bench program is
refused at `texts[c]` passed to a `Str` parameter, "cannot move out of
an index expression". Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It makes 20 cases once, each `s` of
1,000 letters (the problem's longest) from 2 to 5 letters and 1,000
words of 1 to 1,000 letters, a third of them taken from `s` with each
letter kept with chance one in 2 to 31; then solves every case in each
of 20 rounds. Every implementation prints `20 cases, 20 rounds: total
219620, checksum 547527281`, the Kāra program under `karac __mir-run`
included (in 138 s).

Every mirror does the ★ arm's allocations: each subsequence test
copies the word's letters into a fresh array, and each new best word
is copied. Spot timings on a shared 4-core container, taken while a
corpus run was busy on it, three runs each (two for Python; `bench.sh`
timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.40 to 0.41 s |
| Rust (`rustc -O`) | 0.45 to 0.50 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.46 to 0.49 s |
| Go | 0.98 to 1.02 s |
| Python | 9.3 to 9.7 s |
| Kāra (`karac build --mir`) | 1.21 to 1.28 s |

The legacy `karac build` refuses this program (see Verification). So
`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend. That edit is by hand, on top of the
`scripts/new-bench.sh` output. The `--mir` row is timed at kara
`df61cbfff6`. Under `karac __mir-llvm-run` the program prints the same
line in 3.2 s, compile included; that JITs the MIR's IR without
optimization passes, so it is not a benchmark.

## Compiler findings

- **B-2026-10-13-25** (fixed by kara `e02c3c14e2`, filed from kata
  516): `mem.swap`, `mem.replace` and `mem.take`, the spelling
  core-semantics.md §3.7 and design.md give, did not resolve
  ("undefined name 'mem'"); only the bare prelude `swap`, `replace`
  and `take` worked. Met here in the waiting arm's `mem.replace` and
  in the differential's copy of it, which now pass as written.
- **B-2026-10-13-27** (fixed by kara `2649217dc8`, filed from this
  kata): no standard type had a usable `Default`. `String.default()`,
  `i64.default()`, `Vec.default()` and `Map.default()` did not
  resolve; `#[derive(Default)]` on a struct with a `Vec` field was
  refused; and `take(place)` accepted a `String` or `i64` place but
  refused a `Vec` one as not `Default`. Found here when the waiting
  arm was first written with `take(mut waiting[c])`.
