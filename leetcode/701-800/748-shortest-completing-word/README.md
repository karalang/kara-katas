# 748. Shortest Completing Word

A word completes the licence plate `licensePlate` when it holds every
letter of the plate at least as often as the plate does, ignoring case,
digits and spaces. Return the shortest word in `words` that completes
the plate, the first of them if several are shortest. Some word always
does.

```
licensePlate = "1s3 PSt"
words = ["step", "steps", "stripe", "stepple"]  ->  "steps"
licensePlate = "1s3 456"
words = ["looks", "pest", "stew", "show"]       ->  "pest"
```

**Constraints:** the plate is 1 to 7 characters, letters of either case,
digits and spaces; 1 to 1,000 words of 1 to 15 lowercase letters.

## Approaches

A word completes the plate when, letter by letter, it has at least the
plate's count; the arms differ in how they test that and in the order
they try the words.

| file | mechanism |
|---|---|
| `shortest_completing_word.kara` ★ | count the plate's letters, lower-cased, in 26 slots; walk the words in order, skip any not strictly shorter than the best so far, and count the rest's letters to compare; O(26 + total letters) |
| `shortest_completing_word_markoff.kara` | keep the plate's letters as a list and, for each word, mark off one unused occurrence for each plate letter in turn, giving the word up at its first missing letter; O(plate letters x word length) a word |
| `shortest_completing_word_bysize.kara` | bucket the word indices by length, 1 to 15, keeping their order, and return the first completing word met from the shortest bucket up; longer words are never looked at |
| `shortest_completing_word_map.kara` | count the plate's letters in a `Map[char, i64]`; for each word pay off a copy of the map one letter at a time, and keep the shortest word that leaves nothing owed |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 10 lines: the two LeetCode examples; three
plates of letters and digits against ten everyday words each; a plate
whose letters differ only in case; a plate with no letters, which every
word completes; a plate with one letter three times; 30 lists of
1,000 random words, the last of them the plate's own letters; and
300 random lists of 2 to 9 short words, each line with the total length
of the answers and a checksum. `shortest_completing_word.py` mirrors the
★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
which, for each word and each letter of the alphabet, counts that letter
in the plate in either case and in the word, and keeps the first of the
shortest words that has every count. 3,000 random plates are checked,
each of up to 7 characters, letters from a to c of either case, digits
and spaces, against 1 to 8 words of 1 to 5 letters from a to e and,
last, the plate's own letters lower-cased, so that some word completes
it; the answers are 8,092 letters long in all.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | the plate reversed, with every letter's case swapped, gives the same answer |
| P3 | an `f`, which no plate holds, added to the end of every word gives the answer with its `f` |
| P4 | the answer reversed, put in front of the words, is the answer, since it completes the plate as well and comes first |

It prints `3000 plates (answers 8092 letters long in all), 4 arms,
48000 checks, 0 failures` under `karac __mir-run` and `karac
__mir-llvm-run`, and the same under `karac __mir-llvm-asan` with no
error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed. Three more edits, E1 to
E3, change nothing that can be seen, and the differential rightly
reports no failure for them.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a tie in length going to the later word | P1 134, P4 1657 |
| M2 | ★: capital letters on the plate not counted | P1 983, P2 1618 |
| M3 | ★: a word one letter short counted complete | P1 1463 |
| M4 | markoff: capital letters on the plate dropped | P1 983, P2 1618 |
| M5 | markoff: a letter of the word never marked off | P1 502 |
| M6 | markoff: a tie in length going to the later word | P1 134, P4 1657 |
| M7 | bysize: one-letter words never tried | P1 893, P3 893 |
| M8 | bysize: the plate not lowercased | P1 983, P2 1618 |
| M9 | bysize: only a and b checked | P1 531 |
| M10 | map: a letter the word has to spare still paying | P1 80 |
| M11 | map: one letter still owed counted complete | P1 913 |
| M12 | map: a tie in length going to the later word | P1 134, P4 1657 |
| E1 | ★: one more unused count | 0 |
| E2 | markoff: the search going on after a letter is missing | 0 |
| E3 | bysize: one more unused length | 0 |

P1 kills all twelve. Three mistakes are made in two or three arms each
and fail exactly the same checks. M1, M6 and M12 let a tie in length go
to the later word; P4 sees them strongly, since the reversed answer put
first is as short as the answer and must win. M2, M4 and M8 ignore the
plate's capital letters; P2 sees them, since swapping the plate's case
changes which letters are ignored. M3, M5, M9, M10 and M11 test
completion wrongly in ways that P2 to P4 cannot see: those properties
change the plate's case and order, add a letter no plate holds, or
reverse a word, and none of these changes which letters a word has.
M7 never tries one-letter words; P3 sees it on exactly the plates
P1 does, since with an `f` added no word has one letter, so the arm then
answers right and differs from its own wrong answer plus `f`. E1 and
E3 add a count or a length bucket that is never used; E2 lets the
mark-off arm go on searching after a letter is missing, which still
finds the word incomplete.

## Verification

Every arm prints the same output as `shortest_completing_word.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The debug build that
runs `__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` and the
release build that runs `check` and `__mir-run` are both at kara
`1a5c083e3a`, whose last compiler change is `4655692faa`. The runtime
archives were built after the last runtime change, `b09cd37112`.

Since kara `3c8e763161` (B-2026-10-18-31) the sanitizer lane sees leaks
itself. The leak check also copied each arm's and the differential's
lane executable as it was linked and ran it with the preloaded shim from
kata 708, which refuses the lane's hand-made stack so that LeakSanitizer
sees `main`: all five print their output and report no leak.

The frozen legacy backends refuse all four arms, the differential and
the bench program at type checking, at a `*` over a vector's `iter()`
(`*b` over a string's bytes), since legacy gives those by value where
v2 gives references. Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. It makes a list
of 1,000 random words of 1 to 15 letters from a to f once, and for each
of 100,000 plates gives 5 random words new letters, makes a random plate
of up to 7 characters (letters from a to f of either case, digits and
spaces), puts the plate's own letters, lower-cased, as the last word so
that some word completes it, and finds the shortest completing word.
Every implementation prints `100000 plates against 1000 words: answers
274166 letters long in all, checksum 973521121`, the Kāra program under
`karac __mir-run` included (in 343 s).

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and two of Python (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.45 to 0.63 s |
| Rust (`rustc -O`) | 0.61 to 0.69 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.64 to 0.72 s |
| Go | 0.90 to 1.06 s |
| Python | 21.2 to 21.3 s |
| Kāra (`karac build --mir`) | 2.06 to 2.46 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend; the legacy `karac build` refuses it (above). That
edit is by hand, on top of the `scripts/new-bench.sh` output. Under
`karac __mir-llvm-run` the program prints the same line in 8.8 s,
compile included; that JITs the MIR's IR without optimization passes, so
it is not a benchmark.

So at the medians of the interleaved runs the v2 build takes 2.34 s,
4.3 times C's 0.55, 3.6 times Rust's 0.65 (0.67 under overflow checks)
and 2.5 times Go's 0.94. Under valgrind's cachegrind v2 runs
27.8 billion instructions against C's 4.4 billion and Rust's
4.9 billion. Callgrind puts 52% of v2's instructions in
`karac_mir_vec_reserve` and what it calls, 70 million calls of it: the
26-slot count is built by `Vec.new()` and 26 pushes in a `for` loop,
which v2 grows in four allocations (4, 8, 16 and 32 elements) where
legacy reserves the 26 at once. The legacy backends refuse the program.
To have a legacy time at all, the bench was copied for legacy alone with
`*b` written `b` in its `bytes().iter()` loops: the legacy build of that
copy ran 0.66 to 0.83 s, a median of 0.74 s, so v2 takes 3.2 times as
long as legacy, over M2's limit of twice legacy. That copy is a
measurement only and is not in the kata, and new katas' benches are
outside M2's frozen set in any case. The same v2 program with the
count's fill loop written as a `while` loop, which v2's pre-size pass
does recognise, takes 1.35 s, and with `vec![0; 26]` 1.04 s. The kata
keeps the natural `for` loop and the gap is filed as
B-2026-10-18-51. The comparison with C and Rust waits until after M4.

## Compiler findings

B-2026-10-18-51 (filed, open): v2's pre-size pass (`src/mir/presize.rs`)
reserves room ahead of a `while i < n` counting loop's pushes but not a
`for` loop's, so `let mut v: Vec[i64] = Vec.new(); for _ in 0..26 {
v.push(0); }` allocates four times where the `while` spelling and legacy
allocate once. This kata's bench, which builds such a count for every
word it tests, is 3.2 times legacy because of it (see Benchmarks). The
kata keeps its natural spelling.
