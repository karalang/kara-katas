# 390. Elimination Game

Start with the numbers 1 to n in order. Remove the first number and every
other number after it, going left to right. Then do the same from right
to left on what is left: remove the rightmost number and every other
number before it. Keep alternating until one number is left, and return
it.

```
n = 9  -> 6   (1..9 -> 2 4 6 8 -> 2 6 -> 6)
n = 1  -> 1
```

**Constraints:** `1 <= n <= 10^9`.

## Approaches

| file | mechanism | time | space |
|---|---|---|---|
| `last_remaining.kara` ★ | the list stays an arithmetic progression, so track its first number, the gap and the count; a pass from the left always moves the head, a pass from the right only on an odd count | O(log n) | O(1) |
| `last_remaining_recursive.kara` | after the first pass the evens 2..2m are left and the game goes on from the right, which ends on the mirror of the game on 1..m: `f(n) = 2 * (m + 1 - f(m))`, `m = n / 2` | O(log n) | O(log n) stack |
| `last_remaining_simulate.kara` | play it out: each pass copies every second number into a new `Vec` | O(n) | O(n) |
| `last_remaining_deque.kara` | play it out on a `VecDeque`: pop from the pass's side, push the survivors on the other | O(n) | O(n) |
| `differential.kara` | the four arms against a direct sweep over alive flags and three laws of the game, for n up to 300 and 2,000 random n up to 2^45 | — | — |

Every arm prints the same 13 lines: the two LeetCode examples, the
answers for n = 1 to 24, nine single values of n (powers of two, an odd
and an even n near 100,000), and the sum and a checksum of the answers
for n = 1 to 2,000. `last_remaining.py` mirrors the ★ arm and its output
is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and `sweep`, which
plays the game as the problem states it, over an array of alive flags
walked from alternate ends.

| | property |
|---|---|
| P1 | every arm gives `sweep`'s answer, for n = 1 to 300 |
| P2 | `f(2m + 1) == f(2m)`: an odd n loses its last number in the first pass, which leaves the list of n - 1 |
| P3 | `f(2m) == 2 * (m + 1 - f(m))`: the evens left after the first pass, played from the right, end on the mirror of the game on 1..m |
| P4 | for n >= 2 the answer is even and at most n |
| P5 | the two O(log n) arms agree on 2,000 random n up to 2^45, which also get P2, P3 and P4 |

The two arms that play the game out see only n up to 300 (P1 to P4). It
prints `13592 checks, 0 failures` under `karac __mir-run`, and a count
for each property when anything fails.

## Mutation testing

Eight edits to `differential.kara`, each run under `karac __mir-run`.
All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | head: a pass from the right never moves the head | P1 247, P3 1144, P5 2000 |
| M2 | head: from the right, moves the head on an even count | P1 297, P3 1151, P5 2000 |
| M3 | head: rounds the count left up, not down | P1 281, P2 1146, P3 1144, P4 736, P5 2000 |
| M4 | recursive: the mirror is `m - f(m)`, not `m + 1 - f(m)` | P1 299, P3 1152, P4 30, P5 2000 |
| M5 | recursive: stops at `n <= 2` | P1 172, P2 1, P3 1, P4 1, P5 977 |
| M6 | simulate: a pass from the right starts on the wrong parity | P1 297, P3 149 |
| M7 | simulate: a pass from the left keeps the first number | P1 299, P2 148, P3 150, P4 299 |
| M8 | deque: a pass from the right keeps the first number it sees | P1 297, P3 149 |

P2 misses most mutations because it compares an arm with itself at a
neighbouring n, and most of these mistakes give the same wrong answer to
both. P3 is the law the recursive arm is built on, so it would miss a
mistake shared by the law and the arm; P1 and P5 do not depend on it.

## Verification

All four arms print the same output as `last_remaining.py` on every
backend: `karac __mir-run` (the v2 MIR interpreter),
`karac __mir-llvm-run`, `karac run --interp`, LLJIT, `karac build` and
`KARAC_AUTO_PAR=1 karac build`. `karac check` passes on every file. The
differential prints `13592 checks, 0 failures` under `karac __mir-run`,
`karac __mir-llvm-run` and `karac run --interp`.

The legacy native backends (LLJIT, `karac build` and
`KARAC_AUTO_PAR=1 karac build`) print `3200 checks, 0 failures`: they
drop the `*checks += 2` in `laws`, a compound assignment through a
`mut ref i64` parameter. A three-line program shows it: `fn add2(c: mut
ref i64) { *c += 2; }` leaves its argument at 0 under LLJIT and
`karac build`, and at 2 under both interpreters, while `*c = *c + 2`
works on all of them. The legacy backends are frozen, so this is noted
and not filed; the MIR backends get it right.

## Benchmarks

The bench program uses the ★ arm on 10,000,000 values of n from an LCG,
each between 1 and 2^30 (the problem allows up to 10^9), and folds the
answers into a sum and a checksum. A fresh n per call keeps the compiler
from reusing an answer. Every implementation prints
`10000000 values of n, sum 2862843657446448, checksum 305481418`. Spot
timings on a shared 4-core container (`bench.sh` timings need a quiet
machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.40 s |
| Rust (`rustc -O`) | 0.38 to 0.47 s |
| Kāra (`karac build`) | 0.95 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.06 to 1.12 s |
| Go | 1.26 s |
| Python | 27 s |

Kāra checks integer overflow by default, so the fair comparison is the
overflow-checked Rust build, which it matches. `karac __mir-llvm-run`
also prints the right line, in 3.66 s; it JITs the MIR's IR without
optimization passes, so that time is not a benchmark.

## Compiler findings

- **`VecDeque` front operations are O(n) in the MIR interpreter**
  (kara `B-2026-10-12-10`). The deque is stored as a plain `Vec`, and
  `push_front` and `pop_front` insert or remove at index 0, moving every
  element. The deque arm's harness takes 1 min 8 s under
  `karac __mir-run`, against 1.3 s for the simulating arm doing the same
  passes with a fresh `Vec` per pass. The spec gives `VecDeque` O(1)
  push and pop at both ends.
