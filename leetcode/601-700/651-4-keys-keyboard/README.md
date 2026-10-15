# 651. 4 Keys Keyboard

A special keyboard has four keys: `A` prints one `A` on the screen;
Ctrl-A selects the whole screen; Ctrl-C copies the selection to a
buffer; and Ctrl-V prints the buffer after what is already on the
screen. Return the most `A`s that `n` presses can print.

```
n = 3  ->  3    A, A, A
n = 7  ->  9    A, A, A, Ctrl-A, Ctrl-C, Ctrl-V, Ctrl-V
```

**Constraints:** 1 <= n <= 50.

## Approaches

Every arm is `fn max_a(n: i64) -> i64`.

| file | mechanism |
|---|---|
| `four_keys_keyboard.kara` ★ | the most for every count of presses up to `n`, each the better of one more `A` and every place the last Ctrl-A, Ctrl-C could have gone; O(n^2) |
| `four_keys_keyboard_window.kara` | the same table, with the last copy pasted only two to five times; O(n) |
| `four_keys_keyboard_blocks.kara` | the `A`s typed first, then blocks of Ctrl-A, Ctrl-C and Ctrl-Vs: the best factor for every count of presses spent on blocks, and the best split between typing and blocks; O(n^2) |
| `four_keys_keyboard_frontier.kara` | the screens and buffers reachable in each count of presses, keeping only those no other beats on both, a handful; O(n) |
| `differential.kara` | the four arms against the definition, five properties |

Every arm prints the same 14 lines: the two LeetCode examples; eleven
more counts of presses (one; six, the most for which typing alone is
best; the first counts where copies win; and up to the largest allowed,
50), each with its answer; and the total and a checksum of the answers
for every count from 1 to 50. `four_keys_keyboard.py` mirrors the ★ arm
and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
which assumes no plan: the four keys pressed literally from an empty
screen, buffer and selection, every state reached kept in a `Set`, and
the answer for `n` the largest screen within `n` presses. It checks
every count of presses from 1 to 50, against the definition up to 22.

| | property |
|---|---|
| P1 | the answer is the definition's, up to 22 presses |
| P2 | one more press prints more |
| P3 | never fewer than `n`, and more than `n` from 7 presses on |
| P4 | at least the answer for `a` presses times `n - a - 1`, a copy after `a` pasted `n - a - 2` times |
| P5 | from 11 presses on, five more print four times as many |

P5 is not in the problem; the ★ arm in Python holds it for every count
up to 300, and only 1, 2, 6 and 10 break it.

It prints `50 counts, 4 arms, 848 checks, 0 failures` under `karac
__mir-run` and `karac __mir-llvm-run`, and runs clean under `karac
__mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac __mir-run`.
All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a block counted one Ctrl-V short | P1 16, P3 1, P4 44, P5 40 |
| M2 | ★: the copy taken one press later than made | P1 18, P3 2, P5 40 |
| M3 | window: a block taking one press fewer | P1 18, P3 2, P5 40 |
| M4 | window: a copy pasted four times never tried | P1 9, P4 22, P5 30 |
| M5 | blocks: a block multiplying by one less | P1 16, P3 1, P4 44, P5 40 |
| M6 | blocks: typing every press not allowed | P1 5, P2 2, P3 5 |
| M7 | frontier: the states sorted smallest first | P1 22, P2 50, P3 50 |
| M8 | frontier: Ctrl-A, Ctrl-C taking one press | P1 18, P3 2, P5 40 |
| E1 | ★: a copy of nothing tried | 0 |
| E2 | window: a copy of nothing tried | 0 |
| E3 | blocks: a block of two presses tried | 0 |
| E4 | frontier: states with equal buffers all kept | 0 |

P1 kills all eight. P2 sees M7, whose answer is the smallest screen
rather than the largest and can fall from one count to the next, and
M6, which loses the small counts where typing every press is best.
P4 sees the mutants that undercount a block of copies, M1, M4 and
M5, since the arm's own copy-then-paste is then beaten by its plain
bound; the others overcount or, in M6, lose only counts too small for a
copy, and P4 holds for them. Two first mutants survived and were
replaced, both equivalent: the ★ arm never trying a block of three
presses last, and the window arm never pasting a copy five times. The
best plans use only blocks that multiply by 3 or 4 (checked in Python
for every count up to 300), so a block that doubles, or one that
multiplies by 5, is never needed. The window arm still looks back to
blocks of three to six presses, the bound it argues. The four survivors
cannot change an answer: a copy of an empty screen multiplies 0, a block
of two presses multiplies by 1, and a state whose buffer equals a kept
one with a smaller screen is beaten anyway.

## Verification

Every arm prints the same output as `four_keys_keyboard.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints its line under all three. `karac check` passes all four arms, the
differential and the bench program. All with the compiler at kara
`8d40e1a762` for the debug build and `abbdbaf131` for the release build
that runs `check` and `__mir-run`, with runtime archives newer than the
last `runtime/src` change.

The frozen legacy backends run the ★, window and blocks arms and print
the same output under `karac run --interp`, `karac run`, `karac build`
and a `KARAC_AUTO_PAR=1` build. They refuse the frontier arm and the
differential at type checking, which read `*state` from `v.iter()`,
typed by value under legacy. Legacy is frozen, so this is noted, not
filed.

## Benchmarks

The bench program uses the ★ arm. It makes 200,000 calls, the count of
presses for each picked by the call from 1 to 150, three times the
problem's limit and about the most whose answer fits in 64 bits, and
adds the answers up and puts them into a checksum in order. Every
implementation prints `200000 calls: total 452517472, checksum
247036752`, the Kāra program under `karac __mir-run` included (in
363 s).

Each implementation is the same table in 64-bit integers, allocated for
each call: Kāra `vec!`, C `calloc`, Rust `vec!`, Go `make` and Python a
list. Spot timings on a shared 4-core container, three runs each (two
for Python; `bench.sh` timings need a quiet machine), each including the
allocations:

| | time |
|---|---|
| C (`clang -O3`) | 0.40 to 0.42 s |
| Rust (`rustc -O`) | 0.64 to 0.71 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.63 to 0.66 s |
| Go | 0.75 to 0.80 s |
| Python | 94 to 96 s |
| Kāra (`karac build --mir`) | 1.97 to 2.09 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend; that edit is by hand, on top of the
`scripts/new-bench.sh` output. The legacy `karac build` builds the bench
program unchanged and takes 0.66 to 0.71 s over six runs. Under `karac
__mir-llvm-run` the program prints the same line in 6.3 s, compile
included; that JITs the MIR's IR without optimization passes, so it is
not a benchmark.

So the v2 build takes about three times as long as legacy, past the
M2 bar of 1.5 times, and three times Rust's time with the same `max`
update. That is open row B-2026-10-15-36: the inner loop's `best[i] =
best[i].max(...)` stores into the `Vec` on every step, and on v2 every
such store makes the loop reload the `Vec`'s data pointer and length and
reload `best[i]`. With the running max in a local and one store per row,
the same program takes 0.72 s built with `--mir` and 0.67 s under
legacy. The comparison with C and Rust waits until after M4.

## Compiler findings

B-2026-10-15-36 (open, filed from this kata): on the v2 compiled backend
`best[i] = best[i].max(best[j] * (i - j - 1))` in the inner loop reloads
the `Vec`'s data pointer and length and loads and stores `best[i]`
through memory on every step. The bench keeps that natural spelling, and
the row has the measurements. All four arms, the differential and the
bench program pass `karac check` and run the same on both v2 backends.
The legacy refusals above are not filed because legacy is frozen.
