# 800. Similar RGB Color

A colour `#AABBCC` has three parts written as two hex digits each. The
shorthand `#ABC` stands for `#AABBCC`, a colour whose every part has its
two digits alike. The similarity of two colours is minus the sum of the
squared differences of their parts. Given a colour of six lowercase hex
digits, return the shorthand colour most similar to it, written out as
six digits.

```
color = "#09f166"  ->  "#11ee66"
color = "#4e3fe1"  ->  "#5544dd"
```

**Constraints:** `color` is `#` and six lowercase hex digits.

## Approaches

| file | mechanism |
|---|---|
| `similar_rgb.kara` ★ | the shorthand parts are the multiples of 17, 0x00 to 0xff, and the similarity is a sum over the parts, so round each part on its own to the nearest multiple of 17, `17 · ((part + 8) / 17)`; no part is ever halfway between two |
| `similar_rgb_nearest.kara` | for each part, try the sixteen doubled digits and keep the closest |
| `similar_rgb_whole.kara` | try all 4,096 shorthand colours, score each one's similarity and keep the first with the highest |
| `similar_rgb_digits.kara` | a part with digits `d` and `e` is `16d + e` and the doubled digit is `17d`, so the part lies above `dd` when `e > d` and below it when `e < d`: the answer is `dd` or its neighbour on the side of `e`, whichever is closer |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 10 lines: LeetCode's two examples; black and
white; `#080808` and `#090909`, the two sides of halfway between 0x00
and 0x11; `#f7f7f7`; `#123456`; `#abcdef`; and 300 random colours, every
other one with each part's two digits alike so that it is its own
answer, with how many already were shorthand and a checksum of the
answers. `similar_rgb.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition:
score every shorthand colour `#XYZ`, whose parts are `17X`, `17Y` and
`17Z`, and keep the first that is most similar, with the colour's parts
read by looking each digit up in `0123456789abcdef`. Its 1,600 cases
come in four kinds of 400: any colour; parts at `17k + 8` or `17k + 9`,
the two sides of halfway between doubled digits; parts within one of a
doubled digit; and parts at the ends, 0x00 to 0x09 and 0xf6 to 0xff.

| | property |
|---|---|
| P1 | the definition's colour |
| P2 | the answer is shorthand, and its own answer |
| P3 | taking the colour's parts in the order g, b, r takes the answer's parts in that order |
| P4 | each part of the answer is within 8 of the colour's |

It prints `1600 cases (16 already shorthand), 4 arms, 25600 checks, 0
failures` under `karac __mir-run` and `karac __mir-llvm-run`, and the
same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: each part rounded down | P1 1294, P4 1294 |
| M2 | ★: halfway taken at 17k + 8 | P1 528, P4 528 |
| M3 | ★: the letters a to f read one low | P1 1248, P2 1161, P4 1248 |
| M4 | nearest: 0x11 never tried | P1 240, P4 240 |
| M5 | nearest: 0xff never tried | P1 486, P4 486 |
| M6 | nearest: a part's two digits read the wrong way round | P1 1584, P4 1584 |
| M7 | whole: the last part left out of the score | P1 1385, P3 1524, P4 1385 |
| M8 | whole: the first and last parts swapped in the answer | P1 1365, P2 1365, P3 1521, P4 1365 |
| M9 | whole: the letters a to f not found | P1 1378, P4 1378 |
| M10 | digits: the doubled digit above never taken | P1 381, P4 381 |
| M11 | digits: the test below the wrong way round | P1 1314, P4 1314 |
| M12 | digits: the second digit doubled, not the first | P1 1531, P4 1531 |

P1 and P4 kill all twelve, and on the same cases: as no part is ever
halfway between two multiples of 17, exactly one of them lies within 8
of it, so P4 is P1 told another way. P2 kills the two whose answers are
not their own answers, the letters read one low, which turns `ff` into
`ee`, and the swapped parts. P3 kills the two that treat one part unlike
the others. A first version of the differential wrote out all 4,096
candidates as strings and parsed each back, and ran for over ten minutes
under `karac __mir-run`; scoring the candidates from their digits keeps
it to 15 s.

## Verification

Every arm prints the same output as `similar_rgb.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The debug build that
runs `__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` and the
release build that runs `check` and `__mir-run` are both at kara
`b95ac9a0c5`, whose last compiler change is `e6d52d2c4b`. The runtime
archives were built after the last runtime change, `216d20e28a`.

Since kara `3c8e763161` (B-2026-10-18-31) the sanitizer lane sees leaks
itself. The leak check also copied each arm's and the differential's
lane executable as it was linked and ran it with the preloaded shim from
kata 708, which refuses the lane's hand-made stack so that LeakSanitizer
sees `main`: all five print their output and report no leak.

The frozen legacy interpreter (`karac run --interp`) prints the same
output for all four arms unchanged. The legacy JIT (`karac run`) and
`karac build` refuse them and the differential, having no `bytes` on a
`Str` parameter; copies with the parameters written `ref String` print
the same output under the legacy interpreter, the legacy JIT, `karac
build` and an auto-par build. Legacy also refuses the bench program's
`similar_rgb(colors[r % 4096])` as a move out of an index; a copy with
`ref String` parameters and the colour bound with `ref colors[r % 4096]`
first builds and prints the same line, and the bench timing below is of
it. Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. 4,096 colours
are made once, each of their six digits drawn at random. Each of
40,960,000 rounds finds the most similar shorthand colour to the next
one, adding up a checksum of the answers. Every implementation prints
`40960000 colours: checksum 704468751`, the Kāra program under `karac
__mir-run` included (in 805 s).

The bench measures a short function that reads six hex digits and builds
a new seven-byte string, so it is mostly the cost of making and freeing
that string. Spot timings on a shared 4-core container, eight runs of
each compiled program, five of them interleaved, and two of Python
(`bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.25 to 0.36 s |
| Rust (`rustc -O`) | 1.27 to 1.50 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.17 to 1.62 s |
| Go | 2.42 to 2.63 s |
| Python | 53.18 to 55.06 s |
| Kāra (`karac build --mir`) | 1.87 to 2.15 s |

The C program `malloc`s each answer and `free`s it after reading three
of its bytes, and `clang -O3` removes the pair, leaving no allocation at
all, so its time is not the same work as the others'.

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, since the legacy `karac build` refuses it (see
Verification); that edit is by hand, on top of the
`scripts/new-bench.sh` output. Under `karac __mir-llvm-run` the program
prints the same line in 10.9 s, compile included; that JITs the MIR's IR
without optimization passes, so it is not a benchmark.

At the medians of the interleaved runs the v2 build takes 2.01 s,
against C's 0.31, Rust's 1.30 (1.54 under overflow checks) and Go's
2.55. Under valgrind's cachegrind v2 runs 24.7 billion instructions and
3.61 billion branches, against Rust's 18.2 billion and 2.25 billion and
C's 3.48 billion and 41 million. The legacy build of the copy ran 0.98
to 1.43 s, a median of 1.06 s in the interleaved runs, with 16.2 billion
instructions and 2.25 billion branches, so v2 takes 1.90 times legacy,
under the 2 times at which this corpus files a row. v2 and legacy both
mispredict 41 million branches where Rust and C mispredict almost none.
The one test in the program that turns on random data is whether a digit
is a letter, so those are likely that branch, which the other two would
then compile without one; that is inferred, not read from the assembly.
The comparison with C and Rust waits until after M4.

## Compiler findings

Nothing new in v2.
