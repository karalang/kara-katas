# 520. Detect Capital

We define the usage of capitals in a word to be right when one of the
following cases holds:

- All letters in this word are capitals, like `"USA"`.
- All letters in this word are not capitals, like `"leetcode"`.
- Only the first letter in this word is capital, like `"Google"`.

Given a string `word`, return `true` if the usage of capitals in it is
right.

```
word = "USA"   ->  true
word = "FlaG"  ->  false
```

**Constraints:** `1 <= word.length <= 100`; `word` consists of
lowercase and uppercase English letters.

## Approaches

Every arm is `fn detect_capital_use(word: Str) -> bool`.

| file | mechanism |
|---|---|
| `detect_capital_use.kara` ★ | count the capitals: right when there are none, when every letter is one, or when the only one is the first letter |
| `detect_capital_use_case.kara` | compare with the word recased: the word equal to its upper case, or everything after the first letter equal to its lower case |
| `detect_capital_use_second.kara` | the second letter decides: after a lower-case first letter no capital may follow, and every letter from the third on must match the second |
| `detect_capital_use_states.kara` | a state machine over the letters (start, first capital, lower-case run, capital run); a letter that does not fit ends the walk at false |
| `differential.kara` | the four arms against the rule written out, five properties |

Every arm prints the same 17 lines: the answer for 16 words (the two
examples, `leetcode` and `Google`, and every shape of one, two and
three letters that tells the rules apart), then for 3,000 random words
of 1 to 100 letters (all capitals, all lower case, a capital first, any
mix, or one of the first three with one letter's case turned) how many
use capitals right and a checksum over them. `detect_capital_use.py`
mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the rule written
out letter by letter. Each arm is held to the properties below on
2,000 random words of up to 5 and up to 100 letters in turn, drawn as
the harness draws them.

| | property |
|---|---|
| P1 | the answer is the rule's, checked letter by letter |
| P2 | the word in capitals is right |
| P3 | the word in lower case is right, and so is it with a capital first |
| P4 | a word of 3 or more letters in capitals, in lower case or with a capital first, with one letter from the third on turned, is wrong |
| P5 | only the cases matter: every capital an `A` and every lower-case letter an `a` gives the same answer |

It prints `2000 words, 4 arms, 40000 checks, 0 failures` under `karac
__mir-run`.

## Mutation testing

Twelve edits to `differential.kara`, two to each arm that
change its answers, and four that do not, each run under `karac
__mir-run`. All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: one capital is right wherever it is | P1 149, P4 504 |
| M2 | ★: every letter but one a capital counts as all | P1 571, P2 1787, P4 595 |
| M3 | case: only lower case counts after upper case, not a capital first | P1 398, P3 1787 |
| M4 | case: capitals after the first letter count as all capitals | P1 58 |
| M5 | second: the walk starts at the fourth letter | P1 81, P4 413 |
| M6 | second: a lower-case first letter never rules out capitals | P1 58 |
| M7 | states: a capital after lower case starts a run of capitals | P1 125, P4 279 |
| M8 | states: lower case after a first capital starts over | P1 43, P4 131 |
| E1 | ★: no capitals written `< 1` | 0 |
| E2 | case: the rest written as a closed range | 0 |
| E3 | second: one letter written `< 2` | 0 |
| E4 | states: the run of capitals with its test turned round | 0 |

M4 and M6 are the same mistake in two arms: both take a lower-case
first letter followed by capitals, such as `aBC`, as right. Only P1
sees them, in the same 58 cases, since P2 to P4 build their words from
the three right shapes and P5 compares an arm with itself. P5 kills
none: no edit here looks at which letter a letter is, only at its case.

## Verification

Every arm prints the same output as `detect_capital_use.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and runs clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints `40000 checks, 0 failures` on the first two and runs clean
under the third. `karac check` passes on every arm, the differential
and the bench program.

The ★ arm, and with it the differential and the bench program, ran as
written only from kara `2ef9b2ad96`, which fixed B-2026-10-13-26
(below). Before it, the differential and the mutants were run on a
copy that wrote `word.to_string().chars()`; on the files as written
the mutants fail the same checks, case for case.

The frozen legacy backends refuse every file at type checking: legacy
types the items of a `Vec`'s `iter()` by value, so it refuses the
harness's `*c` ("unary '*' requires 'ref T' ... found 'char'"), and on
the case arm it also cannot compare a `Str` with a `String` ("cannot
compare 'StringSlice' and 'String'"). Legacy is frozen, so this is
noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It makes 20,000 random words of 1 to
100 letters once, drawn as the harness draws them, then checks every
word in each of 200 rounds. Every implementation prints `20000 words,
200 rounds: 2459000 right, checksum 559196731`.

The legacy `karac build` refuses the bench program at the harness's
`*c`. So `bench.sh` builds it with `karac build --mir`, the v2
compiled backend; that edit is by hand, on top of the
`scripts/new-bench.sh` output.

Spot timings on a shared 4-core container, three runs each (two for
Python; `bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.19 to 0.22 s |
| Rust (`rustc -O`) | 0.20 to 0.25 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.24 to 0.28 s |
| Go | 0.26 s |
| Python | 7.1 to 7.4 s |
| Kāra (`karac build --mir`) | 1.99 to 2.15 s |

The Kāra row is timed at kara `5fa208779d`. It is about 9 times Rust,
and a large part of that is the walk over the word's chars: on the v2
compiled backend a `Str`'s `chars()` costs about 3.6 ns a char against
1.0 for its `bytes()`, and `is_ascii_uppercase` is a call into the
runtime that finds the method by name (kara B-2026-10-13-31, below).
Under `karac __mir-run` the program prints the same line in 428 s, and
under `karac __mir-llvm-run` in 23.8 s, compile included; that JITs the
MIR's IR without optimization passes, so it is not a benchmark.

## Compiler findings

- **B-2026-10-13-26** (fixed in kara `2ef9b2ad96`): on both v2
  backends, `chars()` on a `Str` was not an iterator value.
  `.filter(..)`, `.count()`, `.next()`, `.rev()`, `.all(..)` and
  `.enumerate()` were all refused at build, and `.map(..).collect()`
  into a `String` was typed as a `Vec[char]`, though `karac check`
  accepted every one of them and `docs/library/strings.md` gives
  `chars()` to `Str` and `String` alike. Found here in the ★ arm,
  whose `word` is a `Str`; the arm now runs as written.
- **B-2026-10-13-31** (perf, open), filed from this kata's bench: a
  walk over a `Str`'s `chars()` on the v2 compiled backend costs about
  3.6 times one over its `bytes()`, and the char predicates are runtime
  calls that match the method's name. The bench runs about 9 times
  Rust.
- **B-2026-10-13-32** (low, open), found while timing the bench: the
  v2 front end takes `*c` on a `filter` closure's `char` over
  `chars()`, which `karac check` refuses, as `docs/library/iterators.md`
  says it should.
