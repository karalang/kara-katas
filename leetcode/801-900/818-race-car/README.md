# 818. Race Car

A car starts at position 0 with speed +1 on an infinite number line, and
drives by a sequence of two instructions. `A` accelerates: the position
grows by the speed and the speed doubles. `R` reverses: a positive speed
becomes -1 and any other speed +1, and the position stays where it is.
Return the length of the shortest sequence that ends at position
`target`.

```
target = 3  ->  2     AA: 0 -> 1 -> 3
target = 6  ->  5     AAARA: 0 -> 1 -> 3 -> 7 -> 7 -> 6
```

**Constraints:** `1 <= target <= 10^4`.

## Approaches

n accelerations from a standing start at speed 1 cover `2^n - 1`, so a
target t with n bits lies beyond `2^(n-1) - 1` and no further than
`2^n - 1`. A shortest run either drives all the way to `2^n - 1`, turns
and covers the overshoot back, or stops at `2^(n-1) - 1`, turns, backs
up m accelerations, turns again and covers what is left ahead. Each of
those leaves a shorter distance to cover from speed 1, which is the same
question again.

| file | mechanism |
|---|---|
| `racecar.kara` ★ | a table of the best run to every distance from 1 to t, bottom up, each entry the better of the overshoot and the n - 1 ways to stop short. O(t log t) |
| `racecar_bfs.kara` | breadth-first search over the car's states, a position and a speed, from (0, 1); both instructions lead to one next state, so the first level that reaches the target answers. Positions are kept between `-target` and `2 * target`, the bound LeetCode solutions use, which the differential holds against a search eight times wider |
| `racecar_memo.kara` | the ★ arm's two ways as a recursion that works out only the distances it needs, each once, in a table shared by the calls. O(t log t) at worst |
| `racecar_iter.kara` | the ★ arm's table built by a `fold` over the distances, each entry the `min` over a `map` of the ways to stop short, chained with the overshoot |
| `differential.kara` | the four arms against every instruction sequence played out, shortest first, four properties |

Every arm prints the same 10 lines: LeetCode's two examples; the answers
for the targets 1 to 32; LeetCode's largest, 10,000; 9,999, 8,191
(`2^13 - 1`), 8,192 and 4,097, around powers of two; 5,461
(`1010101010101` in binary); and 300 random targets up to 200, with a
total and a checksum. `racecar.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement
played out: one search from position 0 at speed 1 tries every sequence
of instructions, one instruction more at each level, and the first level
that reaches a position is its answer, for every target up to 300 at
once. The car is kept far wider than any short run goes, within 2,400 of
the start either way and at speeds up to `2^13`. Its 1,600 cases come in
four kinds of 400: targets up to 40; up to 300; within 2 of a power of
two up to 256; and `2^k - 2^m`, the end of a run that stops short and
backs up. 289 cases are a run of ones, `2^n - 1`, and the longest answer
is 24 instructions.

| | property |
|---|---|
| P1 | the statement's answer |
| P2 | at least n, the bits of the target, and exactly n only when the target is `2^n - 1` |
| P3 | no more than a run to a random a below the target, two turns to stand facing ahead at speed 1, and a run over the rest |
| P4 | no more than driving to `2^n - 1`, one turn and a run back over the overshoot |

It prints `1600 cases (the longest run 24 instructions), 25600 checks
over 4 arms: 0 failures` under `karac __mir-run` and `karac
__mir-llvm-run`, and the same under `karac __mir-llvm-asan` with no
error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the overshoot's turn not counted | P1 711 |
| M2 | ★: never backs up after stopping short | P1 343, P3 6 |
| M3 | ★: the second turn not counted | P1 926 |
| M4 | search: a turn keeps the direction | P1 1189, P4 439 |
| M5 | search: never past the target | P1 482, P4 423 |
| M6 | search: the speed never doubles | P1 1529, P2 289, P4 837 |
| M7 | memo: a run of ones one instruction more | P1 1600, P2 289 |
| M8 | memo: always backs up after stopping short | P1 481, P3 86 |
| M9 | memo: the overshoot measured one short | P1 663, P4 221 |
| M10 | iter: the overshoot never tried | P1 567, P4 488 |
| M11 | iter: the turns of a short stop not counted | P1 926 |
| M12 | iter: the longest way kept | P1 1240, P3 267, P4 848 |

P1 kills all twelve. P3 and P4 are upper bounds, so they see only the
edits that make a run longer than it needs to be, and M1, M3 and M11,
which leave out an instruction, are seen by P1 alone. M3 and M11 fail on
the same 926 cases, the same mistake in two arms. P2 sees M6 and M7.
M6's car needs t instructions to reach t: too many for every run of ones
but 1, and for 2 exactly its two bits, which only a run of ones may
take. M7 makes every run of ones one instruction too long, and fails P1
on every case because every answer is built on runs of ones, where the
memo arm's recursion ends.

## Verification

Every arm prints the same output as `racecar.py` under `karac __mir-run`
(the v2 MIR interpreter) and `karac __mir-llvm-run`, and under `karac
__mir-llvm-asan` (AddressSanitizer) with no error; the differential
prints its line under all three. `karac check` passes all four arms, the
differential and the bench program. The debug build that runs
`__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` is at kara
`d0ad6409f5`, whose last compiler change is `c120cafada`; the release
build that runs `check` and `__mir-run` is at `f6f2efb14`, one parser
change behind it. The runtime archives were built after the last runtime
change in that tree, `45d6c491fc`.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all five print their output and report no leak.

The frozen legacy interpreter (`karac run --interp`), the legacy JIT
(`karac run`), `karac build` and an auto-par build print the same output
for the ★ and memo arms. The search arm prints it under the JIT, `karac
build` and auto-par, and the legacy interpreter does not finish it
within the lane's 60 s limit. The legacy interpreter prints the iterator
arm's output, and the JIT and `karac build` refuse it in codegen,
finding no handler for `min` on the chained iterator. Legacy refuses the
differential, as it types the items of `level.iter()` over a `Vec` of
tuples as values rather than references and so refuses their `*`. Legacy
is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. Each of 40,000
rounds draws a target from 1 to 10,000, LeetCode's largest, and builds
the table up to it afresh: an array of up to 10,001 entries, each the
best of about a dozen ways, so the work is integer arithmetic and reads
from the table. Every implementation prints `40000 rounds of targets up
to 10000: total 1414182, checksum 369243084`, the Kāra program under
`karac __mir-run` included, in 859 s. That run takes more than 10^11
steps, past the interpreter's default limit of 4 x 10^10, so it raises
the limit with `KARAC_MIR_MAX_STEPS`.

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and two of Python (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 2.89 to 3.32 s |
| Rust (`rustc -O`) | 3.13 to 4.03 s |
| Rust (`rustc -O -C overflow-checks=on`) | 3.12 to 4.10 s |
| Go | 5.08 to 6.34 s |
| Python | 188.9 to 190.6 s |
| Kāra (`karac build --mir`) | 3.15 to 4.05 s |
| Kāra, legacy (`karac build`) | 3.17 to 3.84 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend; that edit is by hand, on top of the
`scripts/new-bench.sh` output. Under `karac __mir-llvm-run` the program
prints the same line in 21.1 s, compile included; that JITs the MIR's IR
without optimization passes, so it is not a benchmark.

At the medians of the interleaved runs the v2 build takes 3.75 s,
against legacy's 3.69, C's 3.30, Rust's 3.93 (3.73 under overflow
checks) and Go's 6.13; the interleaved runs came after a restart of the
container, on a busier machine than the first three of each. Under
valgrind's cachegrind v2 runs 45.5 billion instructions, fewer than C's
47.9 billion and Rust's 51.6 billion, but 13.3 billion branches against
C's 5.8 billion and Rust's 9.0 billion; v2 mispredicts 1.5% of them, C
3.2% and Rust 4.2%. The extra branches are most likely v2's checks on
each table index and each addition (not traced). Built for `x86-64-v3`,
the target `karac build` uses, C (`clang -O3 -march=x86-64-v3`) takes
2.76 to 2.91 s and Rust with overflow checks (`-C target-cpu=x86-64-v3`)
3.12 to 3.49 s, against v2's 3.50 to 3.86 s in the same five interleaved
runs. Python takes 190 s, about 60 times C's time. The comparison with C
and Rust waits until after M4.

## Compiler findings

Nothing new in v2 that this kata does not share with an open row: every
arm, the differential and the bench run on every v2 lane as written. The
iterator arm was first written with the overshoot chained as
`.chain([n + 1 + best[full - t]])`. `chain` takes an `Iterator`
(library/iterators.md), so `karac check` is right to refuse an array,
but it does so with two errors at the same span, the first listing all
29 `Iterator` types, and no `.into_iter()` hint: the shape of
B-2026-10-20-33, filed for a `flat_map` closure that returns a
collection and widened by this kata to a collection passed as an
argument; fixed in kara 0ddbf56292, where it is one error per call with
an `.into_iter()` that `karac fix` applies. The arm now writes
`.chain([..].into_iter())`. The same arm first subtracted
`t.leading_zeros()`, then a `u32`, from an `i64`, which `karac check`
refused as a mix of integer types, so it cast with `as i64`. Bit counts
return `i64` since kara B-2026-10-29-19, and the cast is gone.
