# 788. Rotated Digits

A number is good when turning each of its digits upside down, one by
one, gives a valid number different from it. 0, 1 and 8 turn into
themselves, 2 and 5 into each other, 6 and 9 into each other, and 3, 4
and 7 into nothing. Return how many numbers from 1 to `n` are good.

```
n = 10  ->  4      (2, 5, 6 and 9)
n = 1   ->  0
n = 2   ->  1
```

**Constraints:** `n` is from 1 to 10,000.

## Approaches

A number is good exactly when all its digits turn and at least one of
them is a 2, 5, 6 or 9.

| file | mechanism |
|---|---|
| `rotated_digits.kara` ★ | every number from 1 to `n` checked digit by digit with `%` and `/`, stopping at a 3, 4 or 7; O(n log n) |
| `rotated_digits_table.kara` | each number is of one of three kinds, ordered: it turns into itself, into another number, or into none; the kind of `x` is the larger of the kinds of `x / 10` and of its last digit, so one pass from 0 to `n` fills a table and counts the second kind; O(n) |
| `rotated_digits_counting.kara` | the numbers whose digits all turn, less those whose digits all turn into themselves, each counted from 0 to `n` down `n`'s digits: every allowed digit below `n`'s at a place leaves the later places free, a power of 7 or 3, and the count stops at the first digit of `n` not allowed; O(log n) |
| `rotated_digits_strings.kara` | every number written out with an f-string, each character turned by a `match` into an `Option[char]`, and the turned text compared with the original; O(n log n) |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 11 lines: LeetCode's three examples; 9, 100,
857, 1,000, 2,019, 9,999 and 10,000; and 300 random `n` up to 10,000,
with the sum of the answers and a checksum. `rotated_digits.py` mirrors
the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition:
the numbers from 1 to `n` whose turned number, built as a number from a
table of what each digit turns into, exists and is not the number
itself. Its 240 numbers are a quarter up to 10,000, a quarter up to 200,
a quarter next to a multiple of 100 up to 3,000, and a quarter made only
of digits that turn, of 1 to 4 digits. The run is kept short, at 28 s
under `karac __mir-run`, since the four arms are asked for up to six
counts for each number.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | the count for `n` is the count for `n - 1`, plus one exactly when `n` is good |
| P3 | the ten numbers `10a` to `10a + 9` hold 4 good ones when `a` turns into itself, 7 when `a` is good and none when `a` does not turn |
| P4 | for `n = 100q + r` with `q` at least 1: when `q` does not turn, the count is the count for `100q - 1`; when `q` turns into itself, it is that plus the count for `r` |

It prints `240 numbers (answers sum to 117334), 4 arms, 3168 checks, 0
failures` under `karac __mir-run` and `karac __mir-llvm-run`, and the
same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a 6 not taken as turning into another digit | P1 225, P2 15, P3 53 |
| M2 | ★: a 7 taken as turning | P1 206, P2 19, P3 137, P4 15 |
| M3 | ★: n itself left out | P1 126, P2 73, P3 71, P4 65 |
| M4 | table: the smaller kind kept | P1 213, P2 121, P3 135, P4 64 |
| M5 | table: a 9 taken as not turning | P1 219, P2 54, P3 150 |
| M6 | table: only the last two digits looked at | P1 131, P2 35, P3 65, P4 33 |
| M7 | counting: six digits that turn, not seven | P1 217, P2 20, P3 119, P4 65 |
| M8 | counting: n itself never counted | P1 126, P2 73, P3 71, P4 65 |
| M9 | counting: n's own digit counted with those below it | P1 199, P2 82, P3 119, P4 75 |
| M10 | strings: a 2 turning into itself | P1 234, P2 15, P3 49 |
| M11 | strings: a digit that does not turn left out | P1 231, P2 92, P3 217, P4 45 |
| M12 | strings: a number turning into itself counted | P1 240, P2 16, P3 33, P4 56 |

P1, P2 and P3 each kill all twelve. M3 and M8 both leave `n` itself out
of the count, in different arms, and fail the same checks.

## Verification

Every arm prints the same output as `rotated_digits.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The debug build that
runs `__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` and the
release build that runs `check` and `__mir-run` are both at kara
`cfbbf3e8eb`, whose last compiler change is `b115567cf2`. The runtime
archives were built after the last runtime change, `176f59738b`.

Since kara `3c8e763161` (B-2026-10-18-31) the sanitizer lane sees leaks
itself. The leak check also copied each arm's and the differential's
lane executable as it was linked and ran it with the preloaded shim from
kata 708, which refuses the lane's hand-made stack so that LeakSanitizer
sees `main`: all five print their output and report no leak.

The frozen legacy backends accept all four arms, the differential and
the bench program unchanged. Each arm prints the same output under the
legacy interpreter (`karac run --interp`), the legacy JIT (`karac run`),
`karac build` and an auto-par build, and the differential prints its
line under all four; the builds of the counting arm and the differential
warn that a borrowed `digits` is used after a move, since legacy
predates borrowed parameters. The legacy bench timing below is of the
bench program as it is.

## Benchmarks

The bench program uses the ★ arm in all five languages. Each of 50,000
rounds counts the good numbers up to a random `n` from 1 to 10,000,
LeetCode's most, so about 250 million numbers are checked digit by
digit. Every implementation prints `50000 rounds of n up to 10000:
answers sum to 55432377, checksum 328266109`, the Kāra program under
`karac __mir-run` included (in 204 s).

The bench measures integer division by 10 and a chain of comparisons on
each digit, whose branches depend on the digits and are hard to predict.
Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and four of Python (`bench.sh`
timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.90 to 1.16 s |
| Rust (`rustc -O`) | 0.87 to 1.35 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.12 to 1.27 s |
| Go | 2.24 to 2.42 s |
| Python | 50.63 to 57.10 s |
| Kāra (`karac build --mir`) | 1.08 to 1.42 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as for the other katas since the redesign; the legacy
`karac build` also builds this one unchanged. Under `karac
__mir-llvm-run` the program prints the same line in 6.5 s, compile
included; that JITs the MIR's IR without optimization passes, so it is
not a benchmark.

At the medians of the interleaved runs the v2 build takes 1.16 s,
against C's 1.08, Rust's 1.15 (1.20 under overflow checks) and Go's
2.32. Under valgrind's cachegrind v2 runs 13.4 billion instructions and
1.80 billion branches, of which it mispredicts 205 million, against C's
14.6 billion, 2.09 billion and 398 million and Rust's 10.6 billion, 2.14
billion and 326 million. The legacy build ran 0.94 to 1.52 s, a median
of 1.02 s in the interleaved runs, so v2 takes 1.14 times legacy. The
comparison with C and Rust waits until after M4.

## Compiler findings

Nothing new.
