# 679. 24 Game

Given four cards, each a number from 1 to 9, return whether an
expression using each card exactly once, with `+`, `-`, `*`, `/` and
parentheses, can equal 24. Division is real division, so `4 / (1 - 2 /
3)` is 12, and cards cannot be joined into numbers such as `12`.

```
[4, 1, 8, 7]  ->  true    ((8 - 4) * (7 - 1))
[1, 2, 1, 2]  ->  false
```

**Constraints:** `cards.length` == 4; 1 <= `cards[i]` <= 9.

## Approaches

Every arm is `fn judge_point24(cards: Vec[i64]) -> bool`. Any expression
ends with one operation joining two smaller ones, which the first three
arms use one way or another.

| file | mechanism |
|---|---|
| `twenty_four_game.kara` ★ | take two of the values left, replace them by their sum, either difference, product or either quotient, and recurse on the shorter list, in `f64`; 24 within 1e-6; at most 3,888 results |
| `twenty_four_game_fractions.kara` | the same search in exact fractions, kept in lowest terms with a positive denominator, so the test for 24 is exact |
| `twenty_four_game_trees.kara` | every expression written out: 24 orders of the cards, 64 choices of operators and the 5 ways to bracket four operands, 7,680 in all, in exact fractions |
| `twenty_four_game_subsets.kara` | for each subset of the cards as a bit mask, the `Set` of exact values its expressions take, built from the values of the two parts of every split |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 15 lines: the two LeetCode examples; ten
corners, among them hands that need a fraction on the way (`8 / (3 - 8 /
3)`, `5 * (5 - 1 / 5)`), a division that must come last, all one card,
and hands with no answer; how many of the 495 hands of four cards from
1 to 9 are solvable, by smallest card; a checksum over them; and how
many of them answer the same in four orders. `twenty_four_game.py`
mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition.
The definition is written apart from all four arms: for every order of
the cards, it lists every value of every bracketing by splitting the row
into a left and a right run, in exact fractions, and looks for
24. 600 random hands of cards from 1 to 13, a full deck's values, are
checked against it. Those make 24 rarely by chance, so 200 more hands
are built to be solvable: random cards and a random expression in one of
the five shapes, kept when it is exactly 24.

| | property |
|---|---|
| P1 | the answer is the definition's (the 600 random hands) |
| P2 | the same cards in another order give the same answer |
| P3 | a hand built from an expression worth exactly 24 is solvable |
| P4 | 404 of the 495 hands from 1 to 9 are solvable, the published count |

It prints `600 random hands and 200 with a witness (31290 tries),
4 arms, 5604 checks, 0 failures` under `karac __mir-run` and `karac
__mir-llvm-run`, and runs clean under `karac __mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac __mir-run`.
All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: only `a - b`, never `b - a` | P1 33, P2 21, P4 1 |
| M2 | ★: within 1 of 24 counted as 24 | P1 97, P4 1 |
| M3 | fractions: only `a / b`, never `b / a` | P1 3, P2 1, P4 1 |
| M4 | fractions: 24 tested on the numerator alone | P1 52, P4 1 |
| M5 | trees: no division in the innermost gap | P1 13, P3 3, P4 1 |
| M6 | trees: the cards in their given order only | P1 201, P2 163, P4 1 |
| M7 | subsets: no quotient of a part by the other | P1 6, P2 3, P3 1, P4 1 |
| M8 | subsets: no quotient of the other by a part | P1 10, P2 15, P4 1 |
| E1 | ★: within 1e-9 of 24, not 1e-6 | 0 |
| E2 | fractions: no `a / b` when `a` is 0 | 0 |
| E3 | subsets: every split tried both ways round | 0 |
| E4 | subsets: each split taken from the part without the lowest card | 0 |

P1 and P4 each kill all eight. P4 is one check per arm, the published
count of 404, and every mutant moves that count. P2 sees five: the
mutants that lose an operation in one direction, and the one that tries
the cards only in their given order, since another order of the cards
brings the lost case back. P3 sees two, M5 and M7, where a built hand
needs the quotient they lose. M2 and M4 accept values near 24, or
24 over a denominator, which a hand built to make 24 never needs, so
neither P2 nor P3 can see them. The four survivors change no answer
here. No hand lands between 1e-9 and 1e-6 of 24 in floating point. A
quotient of 0 by anything is 0, which the product already gives. And
every split of a subset joins its two parts in both directions, so
taking each split from either side covers them all.

## Verification

Every arm prints the same output as `twenty_four_game.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints its line under all three. `karac check` passes all four arms, the
differential and the bench program. All with the compiler at kara
`5e4d49c205` for both the debug build and the release build that runs
`check` and `__mir-run`, with runtime archives newer than the last
`runtime/src` change.

The frozen legacy backends print the same output for every arm under the
JIT and `karac build`, with and without `KARAC_AUTO_PAR=1`. The legacy
interpreter had printed 12 of the 15 lines of every arm when the 60 s
limit stopped it. They run the differential to the same line under
`karac build`. Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It asks about every ordered hand of
four cards from 1 to 13, a full deck's values, 28,561 hands, counts the
solvable ones and puts each answer into a checksum. Every implementation
prints `28561 hands: 22615 solvable, checksum 304441048`, the Kāra
program under `karac __mir-run` included (in 107 s).

Each implementation is the same recursive search, building a shorter
list of values for every result tried: a `Vec` in Kāra and Rust, a slice
in Go, a list in Python, and an array on the stack in C, which has no
growable array. So this measures the search and, outside C, its
allocations. Spot timings on a shared 4-core container, three runs each
(two for Python; `bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.15 to 0.21 s |
| Rust (`rustc -O`) | 1.53 to 1.88 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.49 to 1.71 s |
| Go | 1.74 to 1.89 s |
| Python | 15.1 s |
| Kāra (`karac build --mir`) | 1.51 to 1.85 s |
| Kāra, legacy (`karac build`) | 0.99 to 1.27 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend; the frozen legacy `karac build` builds it too, and
its row is above. Under `karac __mir-llvm-run` the program prints the
same line in 5.2 to 5.5 s, compile included; that JITs the MIR's IR
without optimization passes, so it is not a benchmark.

So the v2 build is about 1.5x legacy here, with Rust and Go close to
v2 and C some ten times faster. Every row but C allocates a list per
step; C keeps its values on the stack. Under callgrind the v2 build runs
17.1G instructions to legacy's 12.9G, and most of the difference is the
runtime calls around each allocation, `karac_mir_vec_reserve` for the
first `push` and `karac_mir_vec_alloc` for each clone:
B-2026-10-15-56. The comparison with C and Rust waits until after M4.

## Compiler findings

B-2026-10-15-56 (perf, open): on the v2 compiled backend the first
allocation of a pushed `Vec` and every `Vec` clone are out-of-line
runtime calls of some 40 to 70 instructions beyond the allocator. Found
on this bench, where they make the v2 build about 1.5x legacy.
