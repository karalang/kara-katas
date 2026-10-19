# 772. Basic Calculator III

Evaluate an expression of non-negative integers, the operators `+`, `-`,
`*` and `/`, and brackets, with the usual precedence; integer division
truncates toward zero. The expression is always valid, and every
intermediate value is from -2^31 to 2^31 - 1. A built-in evaluator is
not allowed.

```
"1+1"                  ->  2
"6-4/2"                ->  4
"2*(5+5*2)/3+(6/2+8)"  ->  21
```

**Constraints:** the expression has from 1 to 10,000 characters, digits,
`+`, `-`, `*`, `/` and brackets only.

## Approaches

All four arms read the expression byte by byte, a run of digits being
one number; they differ in how they apply precedence and brackets.

| file | mechanism |
|---|---|
| `basic_calculator_iii.kara` ★ | recursive descent, one method for each level of precedence: a sum of terms, a term of factors, a factor a number or a bracketed sum |
| `basic_calculator_iii_postfix.kara` | Dijkstra's shunting-yard into postfix order, then a stack of numbers |
| `basic_calculator_iii_frames.kara` | a frame for each open bracket, a stack of signed terms where `*` and `/` fold a number into the top term; a closing bracket sums its frame into a number for the frame outside |
| `basic_calculator_iii_reduce.kara` | tokens, then while a bracket is left an innermost one and its contents replaced by their value, found in two passes, `*` and `/` and then `+` and `-`; O(n^2) in the worst case |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 13 lines: LeetCode's three examples;
`0`; `1-1-1` and `8/3/2`, which group from the left; `(1-8)/2`, which
truncates to -3 where rounding down would give -4; the largest value;
brackets four deep; a long run with no brackets; `2-(5-8)`; a product of
negatives divided by a negative; then 300 random expressions of up to
12 numbers, with their total length and a checksum of the values. A
random expression brackets a side where precedence needs it and, a
quarter of the time, where it does not; one with a division by zero or a
value beyond 32 bits is drawn again. `basic_calculator_iii.py` mirrors
the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition:
the expression's tree evaluated bottom up, division truncating toward
zero. Each random tree is written three ways: as in the harness; with
every operator's operands bracketed; and with brackets only where
precedence needs them. Trees with a division by zero or a value beyond
32 bits are drawn again. Of the 1,800 random expressions, 1,500 have up
to 10 numbers and 300 up to 30, each with a second expression of up to
6 numbers for P4.

| | property |
|---|---|
| P1 | the answer is the definition's value |
| P2 | every operator's operands bracketed changes nothing |
| P3 | brackets only where precedence needs them change nothing |
| P4 | `(E)-(F)` and `(E)*(F)` give the difference and the product of the two answers |

It prints `1800 expressions (41489 characters), 4 arms, 28800 checks,
0 failures` under `karac __mir-run` and `karac __mir-llvm-run`, and the
same under `karac __mir-llvm-asan` with no error; the length is that of
the first spelling.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed. Nine of them stop the
differential at a division by zero, a divisor having come out 0 on a
valid expression; since a stop shows only that an arm went wrong, the
table also gives their failures from a second run with `/` left out of
the random expressions.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: minus read as plus | stops; without `/`, P1 1236, P4 1726 |
| M2 | ★: division rounding down, not toward zero | P1 168 |
| M3 | ★: a closing bracket left unread | stops; without `/`, P1 1359, P2 1139, P3 937, P4 1792 |
| M4 | postfix: operators of equal binding grouped from the right | stops; without `/`, P1 514, P2 514, P3 238 |
| M5 | postfix: an operator's operands swapped | stops; without `/`, P1 1172, P2 330, P3 141, P4 1789 |
| M6 | postfix: * and / binding no tighter than + and - | stops; without `/`, P1 572, P2 572, P3 282 |
| M7 | frames: a term after a minus not negated | stops; without `/`, P1 1236, P4 1726 |
| M8 | frames: a bracket's value its last term alone | stops; without `/`, P1 1187, P2 498, P3 259, P4 1463 |
| M9 | frames: a bracket's value added whatever the operator before it | P1 1277, P2 1335, P3 774, P4 1795 |
| M10 | reduce: division starting a new term, subtracted | P1 1019, P2 275, P3 121 |
| M11 | reduce: a run's first number subtracted | stops; without `/`, P1 1543, P2 1423, P3 1228, P4 1709 |
| M12 | reduce: multiplication read as addition | stops; without `/`, P1 1353, P4 1800 |

P1 kills all twelve; the three spellings and P4 show what kind of
mistake each is. An edit that gets one operator wrong the same way
wherever it appears leaves P2 and P3 blind, since every spelling is
misread alike: M1 and M7 read a minus as a plus, M12 a times as a plus,
and M2 rounds a quotient down rather than toward zero, which P1 caught
168 times, only where the signs differ and the division is inexact.
P4 sees M1, M7 and M12 on almost every pair, since `(E)-(F)` and
`(E)*(F)` then come out as sums, but not M2, as neither has a division
across its brackets. An edit that gets grouping or binding wrong is seen
by P2 exactly when P1 sees it, as full brackets leave nothing to group:
M4 groups equal binding from the right and M6 binds `*` and `/` as
loosely as `+` and `-`; P3 sees them when the fewest brackets read
differently from the first spelling, and P4 cannot, its outer brackets
fixing the grouping. M10, whose `/` starts a new term and subtracts it,
is seen by P2 and P3 as well, since brackets around a quotient keep it
whole, but not by P4. The edits that mishandle a bracket or an operand,
M3, M5, M8, M9 and M11, fail all four. M9 replaces a first choice, `/`
read as `*`, which stopped at an overflow and with `/` left out would
change nothing.

## Verification

Every arm prints the same output as `basic_calculator_iii.py` under
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

The frozen legacy backends accept three arms and, through a copy, the
bench. The ★, postfix and reduce arms print the same output under the
legacy JIT (`karac run`), `karac build` and an auto-par build. The
legacy interpreter prints a different random line, 6802 characters and
checksum 435895128, for the reason kata 771 found: in `random_piece(mut
seed, 1 + next_random(mut seed) % 12)` it passes the first argument as
`seed` was before the second advanced it. Legacy refuses the frames arm
and so the differential at `n += *term`, since a `for` over a `Vec[i64]`
gives it the elements by value. It refuses the bench at
`calculate(pool[round % 64])`, as a move out of an index; its timing
below is of a copy whose parameter is `ref String`. Legacy is frozen, so
all this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. Sixty-four
random expressions of 2,400 numbers, up to 9,995 characters against
LeetCode's 10,000, are built once, drawn as in the harness except that
at each operator the generator takes the first, from a random start,
that keeps every value valid; each of 6,000 rounds evaluates the next of
them and folds its value into a checksum. Every implementation prints
`6000 expressions of up to 9995 characters: checksum 848496126`, the
Kāra program under `karac __mir-run` included (in 134 s). The Kāra arm
copies the expression's bytes into a `Vec` for its cursor once a round;
C, Rust, Go and Python read the string in place.

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and two of Python (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.43 to 0.52 s |
| Rust (`rustc -O`) | 0.45 to 0.51 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.51 to 0.60 s |
| Go | 0.59 to 0.73 s |
| Python | 17.7 to 19.1 s |
| Kāra (`karac build --mir`) | 0.69 to 0.77 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend, the one this kata measures now that legacy is
frozen. That edit is by hand, on top of the `scripts/new-bench.sh`
output. Under `karac __mir-llvm-run` the program prints the same line in
3.1 s, compile included; that JITs the MIR's IR without optimization
passes, so it is not a benchmark.

So at the medians of the interleaved runs the v2 build takes 0.71 s,
against C's 0.49, Rust's 0.46 (0.54 under overflow checks) and Go's
0.63, and Python takes 18 s. Under valgrind's cachegrind v2 runs
3.1 billion instructions and 456 million branches, Rust 1.7 billion and
288 million, and C 1.7 billion and 305 million; all three mispredict
11 to 14 percent of their branches. The legacy build of the copy ran
14.9 to 15.4 s, a median of 15.1 s in the interleaved runs, 21 times
v2; legacy is frozen, so the cause was not looked for. New katas'
benches are outside M2's frozen set in any case. The comparison with C
and Rust waits until after M4.

## Compiler findings

Nothing new.
