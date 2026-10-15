# 678. Valid Parenthesis String

Given a string `s` of `(`, `)` and `*`, return whether it is valid. Each
`*` may stand for `(`, for `)` or for nothing. A valid string closes
every `(` with a later `)`, and never closes more than it has opened.

```
"()"    ->  true
"(*)"   ->  true
"(*))"  ->  true   (the * read as `(`)
```

**Constraints:** 1 <= `s.length` <= 100; each character is `(`, `)` or
`*`.

## Approaches

Every arm is `fn check_valid_string(s: String) -> bool`.

| file | mechanism |
|---|---|
| `valid_parenthesis_string.kara` ★ | the least and the most number of `(` that could be open so far, a `*` lowering the least and raising the most; the most never below 0, the least kept at 0, and valid when the least ends at 0; O(n), O(1) space |
| `valid_parenthesis_string_interval.kara` | whether each piece `s[i..j]` can be balanced: its first character, a `*`, read as nothing, or its first character read as a `(` closed at some later `k`; O(n^3) |
| `valid_parenthesis_string_stacks.kara` | the places of the unmatched `(` and of the `*`; a `)` closes the latest `(`, or else the latest `*`; then each `(` left is paired, from the end, with a `*` after it; O(n) |
| `valid_parenthesis_string_passes.kara` | left to right with every `*` as `(`, then right to left with every `*` as `)`; the balance may never fall below 0 in either; O(n), O(1) space |
| `differential.kara` | the four arms against the definition, five properties |

Every arm prints the same 24 lines: the three LeetCode examples;
fourteen corners, among them one character of each kind, stars that must
open, close or vanish, and a `)` before any `(`; five strings of
100 characters, the problem's longest; how many of the 3^n strings of
each length up to 8 are valid; and a checksum of 1,000 random strings.
`valid_parenthesis_string.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition.
The definition tries every reading of the stars, each as `(`, `)` or
nothing, 3^k readings for k stars, and accepts the string when some
reading never closes more than is open and ends with nothing open. Every
string of up to 7 characters, 3,279 of them, is checked against it. A
further 2,000 random strings of up to 60 characters are held to the
other four properties: a third with the three characters equally likely,
a third with fewer stars and a third with more.

| | property |
|---|---|
| P1 | the answer is the definition's (strings of up to 7 characters) |
| P2 | the string reversed, with `(` and `)` swapped, has the same answer |
| P3 | the string with `()` put in at a random place has the same answer |
| P4 | a valid string stays valid with one of its characters made a `*` |
| P5 | two valid strings joined are valid |

It prints `5279 strings (3279 against the definition), 4 arms,
45116 checks, 0 failures` under `karac __mir-run` and `karac
__mir-llvm-run`, and runs clean under `karac __mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac __mir-run`.
All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the least open count not kept at 0 | P1 956, P2 75, P4 16, P5 36 |
| M2 | ★: valid when the most ends at 0 | P1 875, P2 24, P4 14 |
| M3 | ★: a `*` never read as `)` | P1 392, P2 305, P4 22 |
| M4 | interval: a `*` never read as nothing | P1 669, P5 148 |
| M5 | interval: a `(` closed by a `(` | P1 764, P2 826 |
| M6 | stacks: a `(` closed by a `*` before it | P1 335, P2 516 |
| M7 | stacks: a `)` never closes a `*` | P1 392, P2 305, P4 22, P5 118 |
| M8 | passes: the right-to-left pass dropped | P1 875, P2 892 |
| E1 | ★: valid when the least ends at most 0 | 0 |
| E2 | ★: the least clamped only while the most is not negative | 0 |
| E3 | stacks: a `(` failing when at or after its `*` | 0 |
| E4 | stacks: failing as soon as fewer `*` than `(` are left | 0 |

P1 kills all eight, and P2 kills seven of them. M4 is the exception: the
interval arm with no `*` read as nothing is wrong the same way on a
string and on its mirror, and only P5 sees it besides P1, joining two
valid strings whose stars must vanish. P3 sees none of the eight. A `()`
put in anywhere is matched by itself in every arm, mutant or not, so it
never changes an answer. The four survivors cannot change one either.
The least open count is never below 0 at the end. The most is never
below 0 where the least is clamped, since the arm has returned by then.
No `(` and `*` share a place. And with fewer `*` than `(` left, the
pairing runs out of `*` and fails anyway.

## Verification

Every arm prints the same output as `valid_parenthesis_string.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and runs clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints its line under all three. `karac check` passes all four arms, the
differential and the bench program. All with the compiler at kara
`5e4d49c205` for both the debug build and the release build that runs
`check` and `__mir-run`, with runtime archives newer than the last
`runtime/src` change.

The frozen legacy backends print the same output for every arm under the
JIT and `karac build`, with and without `KARAC_AUTO_PAR=1`. They do the
same under the interpreter for the ★, stacks and passes arms. The
interval arm had printed 19 of its 24 lines when the 60 s limit stopped
the legacy interpreter. They run the differential to the same line under
`karac build`, and the legacy interpreter does not finish it within
60 s. Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It makes 20,000 strings of 1 to
100 characters once, from the same generator as the tests in every
language. Then, in each of 100 rounds, it checks every string in an
order that changes with the round, so no check can be hoisted out of the
rounds, and puts each answer and length into a checksum. Every
implementation prints `100 rounds of 20000 strings: 1165800 valid,
checksum 65734786`, the Kāra program under `karac __mir-run` included
(in 53 s).

Each implementation is the same loop over the bytes with two counters
and a branch on each character, on data that makes the branches hard to
predict, so this measures the loop and its branches. Spot timings on a
shared 4-core container: three runs each, then five more interleaved for
the compiled rows, leaving out one interleaved round that ran slow for
every row and one C run at 1.37 s (two runs for Python; `bench.sh`
timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.64 to 0.71 s |
| Rust (`rustc -O`) | 0.67 to 0.74 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.70 to 0.75 s |
| Go | 0.66 to 0.78 s |
| Python | 6.8 to 7.1 s |
| Kāra (`karac build --mir`) | 0.61 to 0.73 s |
| Kāra, legacy (`karac build`, a copy) | 0.70 to 0.74 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend, since the legacy `karac build` refuses the bench
program at type checking. `check_valid_string(strings[k])` moves an
element out of `strings` under legacy, where a bare parameter is owned,
but v2 borrows it. That edit is by hand, on top of the
`scripts/new-bench.sh` output. A copy outside the kata whose parameter
is `ref String` builds under legacy, and its row is above. Under `karac
__mir-llvm-run` the program prints the same line in 2.5 s, compile
included; that JITs the MIR's IR without optimization passes, so it is
not a benchmark.

So the v2 build is level with legacy, C, Rust and Go here. Every
compiled row is the same loop, and its branches on characters that are
hard to predict seem to set the time. That is inferred from the rows
being level, not profiled. The comparison with C and Rust waits until
after M4.

## Compiler findings

None new. All four arms, the differential and the bench program pass
`karac check` and run the same on both v2 backends.
