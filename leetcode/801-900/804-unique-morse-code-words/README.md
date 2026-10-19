# 804. Unique Morse Code Words

Each of the 26 lowercase letters has a code in International Morse Code
made of dots and dashes: `"a"` is `".-"`, `"b"` is `"-..."`, and so on.
A word is written out by joining its letters' codes with nothing between
them, so `"cab"` becomes `"-.-..--..."`. Given a list of words, return
how many different codes they are written as.

```
words = ["gin", "zen", "gig", "msg"]  ->  2
words = ["a"]                         ->  1
```

**Constraints:** `1 <= words.length <= 100`, `1 <= words[i].length <=
12`, and every word is lowercase letters.

## Approaches

| file | mechanism |
|---|---|
| `unique_morse.kara` ★ | write each word in Morse code and put the codes in a `Set[String]`; the answer is its size. O(total letters) |
| `unique_morse_sorted.kara` | write each word in Morse code, sort the codes so that equal ones sit together, and count each run once |
| `unique_morse_bits.kara` | a word of at most 12 letters is at most 48 dots and dashes, so its code fits in a number: start from 1 and for each dot or dash double it and add 0 or 1, the leading 1 keeping codes of different lengths apart; sort the numbers and count each run once |
| `unique_morse_pairs.kara` | count a word when its code differs from the code of every word before it. O(words² · letters) |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 8 lines: LeetCode's two examples; `"a"` and
`"et"`, both `".-"`; `"n"`, `"te"` and `"tn"`, two codes; six words made
of dots alone, three codes; three words of 12 letters and 2; three words
of 12 letters, two the same; and 300 random lists of up to 30 words of 1
to 4 letters from `eitamn`, whose codes are one or two dots and dashes,
so that many words share a code, with how many codes there were in all
and a checksum. `unique_morse.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition:
write each word as a list of numbers, 0 for a dot and 1 for a dash, from
a second copy of the alphabet's codes written that way, and count the
words whose list differs from that of every word before them. Its 1,600
cases have 1 to 12 words of up to 6 letters and come in four kinds of
400: letters from `etiman`; letters from `etimansougrkwd`, whose codes
with every dot and dash turned over are codes of letters too; any
letter, made by cutting three random runs of up to 12 dots and dashes
into letters again and again, so that words of any letters share a code;
and words drawn from a pool of four, so that many repeat.

| | property |
|---|---|
| P1 | the definition's count |
| P2 | between 1 and the number of words, and the same with the words in the other order |
| P3 | the same with every word given twice |
| P4 | the same with every dot made a dash and every dash a dot, by swapping each letter for its opposite: `e` and `t`, `i` and `m`, `a` and `n`, and so on; for the three kinds whose letters all have one |

It prints `1600 cases (7049 codes), 4 arms, 24000 checks, 0 failures`
under `karac __mir-run` and `karac __mir-llvm-run`, and the same under
`karac __mir-llvm-asan` with no error. P4 is checked in 1,200 of the
cases, so there are 24,000 checks rather than 25,600.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: each letter read as the code of the one after it | P1 358, P4 5 |
| M2 | ★: a space put after each letter's code | P1 357 |
| M3 | ★: z written as q's code | P1 53 |
| M4 | sorted: the codes never sorted | P1 612 |
| M5 | sorted: each code compared with the first, not the one before | P1 646, P3 1413, P4 265 |
| M6 | sorted: the second half of the alphabet read as the first | P1 377, P4 33 |
| M7 | bits: no leading 1 | P1 172, P4 234 |
| M8 | bits: only the dots and dashes counted, not their order | P1 532, P4 419 |
| M9 | bits: the keys never sorted | P1 612 |
| M10 | pairs: the word just before never compared | P1 474, P2 312, P3 1548 |
| M11 | pairs: codes compared by length only | P1 644 |
| M12 | pairs: the table read from the end | P1 358, P4 7 |

P1 kills all twelve. P3 sees the two edits that count a code again when
it is given again (M5, M10), and P2 the one of those that turns on the
order of the words (M10). P4 sees six, the edits whose answer changes
when every letter is swapped for its opposite: the three that read the
table wrongly for some letters (M1, M6, M12), the two that weaken the
number keys (M7, M8), and M5. Five are seen by P1 alone: a space after
each letter's code (M2), `z` written as `q`'s code (M3), the codes or
keys never sorted (M4, M9), and codes compared by length (M11). A first
version of the differential drew most of its words from a few letters,
and M3, which writes `z` as `q`'s code, failed one case of 1,600; the
kind that cuts random dots and dashes into letters brought that to 53.

## Verification

Every arm prints the same output as `unique_morse.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The debug build that
runs `__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` and the
release build that runs `check` and `__mir-run` are both at kara
`d29967ddf0`, whose last compiler change is `6c0f4f4e70`. The runtime
archives were built after the last runtime change, `216d20e28a`.

Since kara `3c8e763161` (B-2026-10-18-31) the sanitizer lane sees leaks
itself. The leak check also copied each arm's and the differential's
lane executable as it was linked and ran it with the preloaded shim from
kata 708, which refuses the lane's hand-made stack so that LeakSanitizer
sees `main`: all five print their output and report no leak.

The frozen legacy interpreter (`karac run --interp`) prints the same
output for all four arms. The legacy JIT (`karac run`) and `karac build`
refuse them at the harness's `["e", "i", "t", "a", "m",
"n"][next_random(mut seed) % 6]`, an index on a list literal; copies
taking the letter with `"eitamn".slice(at, at + 1)` print the same
output under the legacy interpreter, the legacy JIT, `karac build` and
an auto-par build. Legacy refuses the differential at
`swapped(words[j])` as a move out of an index, legacy taking a bare
parameter as owned rather than borrowed; a copy with `words[j].clone()`
runs under all four and reports `1600 cases (7245 codes), 4 arms, 24000
checks, 0 failures`. Its cases are not v2's: legacy draws the random
numbers differently somewhere in making them, and its first case's first
word is `neimi` where v2 and a Python model of the generator give `nei`;
that was not traced further. Legacy also refuses the bench program at
`unique_morse_representations(lists[r % 64])`; a copy with `ref`
parameters and the list bound by `ref` first builds and prints the same
line, and the bench timing below is of it. Legacy is frozen, so this is
noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. 64 lists of 100
words, LeetCode's most, are made once, each word 1 to 12 letters long,
the letters drawn from `etianm` half the time and from the whole
alphabet otherwise, so that some codes repeat. Each of 100,000 rounds
counts the codes of the next list. Every implementation prints `100000
rounds of 100 words: 9645305 codes in all, checksum 900631683`, the Kāra
program under `karac __mir-run` included (in 191 s). Rust uses a
`HashSet<String>` and Go a `map[string]struct{}`; C has no set, so its
program keeps the codes in a 256-slot open-addressing table with an
FNV-1a hash, each code built in a string of its own.

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and two of Python (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 1.54 to 1.66 s |
| Rust (`rustc -O`) | 2.22 to 2.61 s |
| Rust (`rustc -O -C overflow-checks=on`) | 2.08 to 2.75 s |
| Go | 2.04 to 2.23 s |
| Python | 7.19 to 7.57 s |
| Kāra (`karac build --mir`) | 8.36 to 9.04 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, since the legacy `karac build` refuses it (see
Verification); that edit is by hand, on top of the
`scripts/new-bench.sh` output. Under `karac __mir-llvm-run` the program
prints the same line in 35.5 s, compile included; that JITs the MIR's IR
without optimization passes, so it is not a benchmark.

At the medians of the interleaved runs the v2 build takes 8.50 s,
against C's 1.61, Rust's 2.37 (2.31 under overflow checks), Go's 2.07
and Python's 7.19 to 7.57. Under valgrind's cachegrind v2 runs 86.8
billion instructions and 14.9 billion branches, against Rust's 15.4
billion and 2.11 billion and C's 9.45 billion and 1.68 billion. The
legacy build of the copy ran 3.09 to 3.40 s, a median of 3.23 s in the
interleaved runs, with 21.4 billion instructions and 3.24 billion
branches, so v2 takes 2.63 times legacy, over the 2 times at which this
corpus files a row: **B-2026-10-19-34**. Under callgrind,
`karac_mir_string_from` takes 41% of v2's instructions and `malloc` and
`free` 58%, which reads as the 26 literals of `morse`'s table each being
made into a new heap `String` on every call. A copy with the table built
once in `main` and passed to `morse` runs in 2.46 s, under legacy. The
comparison with C and Rust waits until after M4.

## Compiler findings

- **B-2026-10-19-34** (v2 codegen, perf, open): an array of string
  literals in a function body is built as heap `String`s on every call,
  which makes the bench 2.63 times legacy and slower than Python. The
  kata keeps the table inside `morse`, where it belongs; nothing here
  works around the row.
