# 779. K-th Symbol in Grammar

Row 1 of a table is `0`. Each later row is the row before with every `0`
replaced by `01` and every `1` by `10`, so row 2 is `01` and row 3 is
`0110`. Given `n` and `k`, return the `k`-th symbol (from 1) of row `n`.

```
n = 1, k = 1  ->  0
n = 2, k = 1  ->  0
n = 2, k = 2  ->  1
```

**Constraints:** `n` is from 1 to 30, and `k` from 1 to `2^(n - 1)`.

## Approaches

Symbol `k` of row `n` is made from symbol `(k + 1) / 2` of row `n - 1`:
the same symbol for an odd `k`, the other one for an even `k`. Going up
from `k - 1` in binary, each step drops the last bit and flips the
symbol when that bit is 1, so the symbol is the parity of the 1 bits in
`k - 1`, and `n` only has to be large enough to hold `k`. The rows are
prefixes of the Thue–Morse sequence.

| file | mechanism |
|---|---|
| `kth_symbol_in_grammar.kara` ★ | the parity of the 1 bits in `k - 1`, by `count_ones`; O(1) |
| `kth_symbol_in_grammar_parent.kara` | recursion up to the parent symbol, flipping for an even `k`, down to row 1; O(n) |
| `kth_symbol_in_grammar_halves.kara` | row `n` is row `n - 1` followed by its flipped copy, so walk down from row `n`, taking a `k` in the second half to the same place in the first and flipping; O(n) |
| `kth_symbol_in_grammar_kernighan.kara` | the 1 bits of `k - 1` cleared one by one with `x & (x - 1)`, flipping each time; O(the number of 1 bits) |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 13 lines: LeetCode's three examples; the
first, last and next-to-last symbols of row 30, LeetCode's largest, and
the first of its second half; rows 1 to 5 in full; then 1,000 random
queries of rows 1 to 30 with how many answers are 1 and a checksum.
`kth_symbol_in_grammar.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition:
the rows built by the replacement itself, as strings. P1 checks every
symbol of rows 1 to 13; P2 to P4 check 3,000 random places in rows 2 to
30, each `k` drawn from the first half of its row.

| | property |
|---|---|
| P1 | every symbol of rows 1 to 13 is the definition's |
| P2 | the first half of row `n` is row `n - 1` |
| P3 | the second half of row `n` is the first half flipped |
| P4 | symbol `k` of row `n - 1` makes symbols `2k - 1` and `2k` of row `n`, the first the same and the second the other one |

It prints `rows 1 to 13 (4095 ones) and 3000 random places, 4 arms,
68764 checks, 0 failures` under `karac __mir-run` and `karac
__mir-llvm-run`, and the same under `karac __mir-llvm-asan` with no
error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the ones in `k` counted, not `k - 1` | P1 5461, P3 232, P4 3000 |
| M2 | ★: only the last bit of `k - 1` | P1 4094, P3 2892, P4 1428 |
| M3 | ★: every symbol flipped | P1 8191 |
| M4 | parent: the parent at `k / 2` | P1 4542, P2 2768, P4 1948 |
| M5 | parent: odd and even `k` swapped | P1 2730, P2 3000, P4 3000 |
| M6 | parent: the recursion stopping at row 2 | P1 4095, P2 1419, P3 3000, P4 108 |
| M7 | halves: the middle symbol taken as the second half | P1 5454, P2 144, P3 144, P4 3000 |
| M8 | halves: the half twice as long | P1 4095, P3 108, P4 3000 |
| M9 | halves: the walk stopping at row 2 | P1 4095, P3 108, P4 3000 |
| M10 | kernighan: every bit of `k - 1` counted, not its ones | P1 4083, P3 1020, P4 2788 |
| M11 | kernighan: the ones in `k` counted | P1 5461, P3 232, P4 3000 |
| M12 | kernighan: any 1 bit giving 1 | P1 4083, P3 2788, P4 2788 |

P1 kills all twelve, and M3 only P1: the flipped sequence keeps every
structural property, and only row 1 being `0` tells it from the right
one. P2 sees only mutants whose answer depends on `n`, the ★ and
kernighan arms never reading it; M8 and M9 read it and still do not
depend on it, being the same mutant: with the half twice as long, the
first step of the walk never fires and each later one does the next
row's work, so the walk again ends without the last split, and both
answer as if the last bit of `k - 1` were 0. P3 then sees them only in
row 2, where the second half is that last bit. No first choice
survived.

## Verification

Every arm prints the same output as `kth_symbol_in_grammar.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The debug build that
runs `__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` and the
release build that runs `check` and `__mir-run` are both at kara
`4f079681eb`, whose last compiler change is `ecb1a0322e`. The runtime
archives were built after the last runtime change, `176f59738b`.

Since kara `3c8e763161` (B-2026-10-18-31) the sanitizer lane sees leaks
itself. The leak check also copied each arm's and the differential's
lane executable as it was linked and ran it with the preloaded shim from
kata 708, which refuses the lane's hand-made stack so that LeakSanitizer
sees `main`: all five print their output and report no leak.

The frozen legacy backends accept all four arms, the differential and
the bench program, and print the same output under the legacy
interpreter (`karac run --interp`), the legacy JIT (`karac run`),
`karac build` and an auto-par build.

## Benchmarks

The bench program uses the ★ arm in all five languages. It answers
200,000,000 queries of row 30, LeetCode's largest, one after another:
each `k` comes from a linear congruential step that takes in the answer
before, so no two queries can run side by side and nothing can be
vectorized. Every implementation prints `200000000 queries of row 30:
99755646 ones, last state 1106351549`, the Kāra program under `karac
__mir-run` included (in 159 s).

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and two of Python (`bench.sh`
timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.76 to 0.78 s |
| Rust (`rustc -O`) | 0.75 to 0.81 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.78 to 0.88 s |
| Go | 1.47 to 1.56 s |
| Python | 120.9 to 123.5 s |
| Kāra (`karac build --mir`) | 0.77 to 0.89 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as every kata's does since the v2 redesign; that edit
is by hand, on top of the `scripts/new-bench.sh` output. Under `karac
__mir-llvm-run` the program prints the same line in 4.5 s, compile
included; that JITs the MIR's IR without optimization passes, so it is
not a benchmark.

At the medians of the interleaved runs the v2 build takes 0.79 s, as do
Rust (0.79 under overflow checks too) and C (0.78); Go takes 1.49 s.
Under valgrind's cachegrind v2 runs 3.20 billion instructions and 400
million branches, C and Rust 2.80 billion and 200 million: one branch
more for each query, which in v2 is an overflow check. None of the three
uses the `popcnt` instruction, which the generic x86-64 target they
build for may not have, so each counts the bits with a sequence of
shifts, masks and a multiply. The legacy build of the same program ran
0.53 to 0.64 s, a median of 0.53 s, so v2 takes 1.49 times legacy:
legacy's binary uses `popcnt`, and runs 2.10 billion instructions. The
comparison with C and Rust waits until after M4.

## Compiler findings

Nothing new.
