# 770. Basic Calculator IV

Given an expression of integers, lowercase variables, `+`, `-`, `*` and
brackets, and values for some of the variables, return the simplified
polynomial as a list of terms. Each term is its coefficient and then its
variables in sorted order, joined by `*`, like `"-2*a*a*b"`. Terms come
in order of degree, highest first, ties broken by their variables in
dictionary order, with the constant last; terms whose coefficient is
0 are left out.

```
"e + 8 - a + 5", e = 1            ->  ["-1*a", "14"]
"(e + 8) * (e - 8)", no values    ->  ["1*e*e", "-64"]
```

**Constraints:** the expression has from 1 to 250 characters, its tokens
separated by single spaces; at most 100 variables are given values, each
from -100 to 100.

## Approaches

All four arms read the expression with the usual precedence and multiply
out every product; they differ in how they parse and in how they hold a
polynomial.

| file | mechanism |
|---|---|
| `basic_calculator_iv.kara` ★ | recursive descent, one method per level of precedence; a polynomial is a `Map` from a term's sorted, `*`-joined variables to its coefficient |
| `basic_calculator_iv_postfix.kara` | Dijkstra's shunting-yard into postfix order, then a stack of polynomials, kept in the same kind of `Map` |
| `basic_calculator_iv_tree.kara` | precedence climbing into a tree of `shared enum` nodes, then a recursive evaluation; a polynomial is a list of terms sorted by their variables, merged for a sum and sorted and combined for a product |
| `basic_calculator_iv_stacks.kara` | two stacks, operands and operators, evaluated as the tokens arrive; an operand is a plain list of terms never merged until the end, where equal terms are added up |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 9 lines: LeetCode's three examples; `7 -
7`, which is empty; two products of the same variables in different
orders; a long product of differences whose answer has 22 terms; terms
that cancel; a variable multiplied by 0 and another given a value; then
300 random expressions of up to 12 leaves over a to d, x and y, x
sometimes given a value, with the answers' total length in terms and a
checksum of their characters. `basic_calculator_iv.py` mirrors the ★ arm
and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition:
the answer, read back as a polynomial, has the expression's own value at
every point. It evaluates both modulo the prime 1,000,000,007 at five
random points, with the given variables at their values; two different
polynomials of degree d agree at a random point with probability at most
d in 10^9. Of the 1,800 random expressions, 1,500 have up to 8 leaves
and 300 up to 20, with x and y each given a value half the time, and a
second expression of up to 6 leaves for P4.

| | property |
|---|---|
| P1 | the answer has the expression's value at five random points, modulo a prime |
| P2 | the answer is in LeetCode's form: no zero coefficient, each term's variables sorted, the terms in order with none repeated |
| P3 | `E - (E)` has an empty answer |
| P4 | `(E) + (F)` and `(F) + (E)` have the same answer, and so do `(E) * (F)` and `(F) * (E)` |

It prints `1800 expressions (4771 terms), 4 arms, 28800 checks,
0 failures` under `karac __mir-run` and `karac __mir-llvm-run`, and the
same under `karac __mir-llvm-asan` with no error; the total is the ★
arm's.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: minus read as plus | P1 1157, P3 1766 |
| M2 | ★: a product's variables never sorted | P2 341, P4 1302 |
| M3 | ★: terms with coefficient 0 kept | P2 330, P3 1800 |
| M4 | postfix: * binding no tighter than + and - | P1 629 |
| M5 | postfix: operators of equal binding grouped from the right | P1 656, P3 424 |
| M6 | postfix: terms ordered by their variables alone | P2 1062 |
| M7 | tree: operators of equal binding grouped from the right | P1 656, P3 424 |
| M8 | tree: a term only on the right of a minus not negated | P1 974 |
| M9 | tree: equal terms not added but replaced | P1 9 |
| M10 | two stacks: the right side of a minus kept positive | P1 1157, P3 1766 |
| M11 | two stacks: a product's variables never sorted | P2 341, P4 1302 |
| M12 | two stacks: terms of the same degree added together | P1 885 |

P1 kills the eight edits that change a value; P2 sees the four that only
break LeetCode's form: M2 and M11 leave a product's variables unsorted,
M3 keeps zero coefficients and M6 orders terms by their variables alone.
M2 and M11 are also seen by P4, since unsorted variables make the order
of a product's sides matter, and M3 by P3, whose `E - (E)` leaves zero
terms behind. P3 sees the edits that get a minus wrong, M1 and M10, and
the right-grouped minus of M5 and M7. M4 binds `*` as loosely as `+`,
which P1 sees but P3 cannot, since `E` and `(E)` are then misread the
same way. M9 adds equal terms by replacing one with the other, which
matters only when a product makes the same term twice, as `(a + b) * (a
+ b)` does; P1 caught it 9 times. No first choice survived.

## Verification

Every arm prints the same output as `basic_calculator_iv.py` under
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

The frozen legacy backends refuse all four arms, the differential and
the bench, at spellings v2 and `karac check` accept: `*value` on a
`Map.get` result, which legacy gives by value; a borrowed `String`
passed as a bare argument, which legacy treats as a move out of an
index; and `count` and `map` straight on `split`, which legacy returns
as a `Vec`. A copy of the bench changed for legacy then stopped at
`is_ascii_alphanumeric`, which legacy codegen has no handler for, and
with that written as character comparisons the legacy build aborts at
once with `free(): double free detected`. So there is no legacy timing.
Legacy is frozen, so all this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. Sixty-four
random expressions of 40 leaves, up to 195 characters against LeetCode's
250, are built once, drawn as in the harness; each of 20,000 rounds
simplifies the next of them, with x given a value from -3 to 3, and
folds the answer's characters into a checksum. Every implementation
prints `20000 expressions of up to 195 characters: 317871 terms in all,
checksum 907450851`, the Kāra program under `karac __mir-run` included
(in 50 s). Kāra's `Map`, Rust's `HashMap` and Python's dict all hash
strings with SipHash-1-3; Go uses its own map hash and C a small
open-addressing table with FNV-1a.

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and two of Python (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.53 to 0.63 s |
| Rust (`rustc -O`) | 0.60 to 0.67 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.60 to 0.70 s |
| Go | 0.83 to 0.95 s |
| Python | 1.71 to 1.78 s |
| Kāra (`karac build --mir`) | 1.06 to 1.18 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend, the one this kata measures now that legacy is
frozen. That edit is by hand, on top of the `scripts/new-bench.sh`
output. Under `karac __mir-llvm-run` the program prints the same line in
8.0 s, compile included; that JITs the MIR's IR without optimization
passes, so it is not a benchmark.

So at the medians of the interleaved runs the v2 build takes 1.07 s,
against C's 0.56, Rust's 0.65 (0.64 under overflow checks) and Go's
0.83, and Python takes 1.75 s, only 1.6 times v2. Under valgrind's
cachegrind v2 runs 9.1 billion instructions, Rust 5.0 billion and C
3.6 billion. The work is splitting, sorting and joining short strings
and hashing them into maps, where Python's string and dict code is
compiled C. With no legacy build there is no M2 ratio; new katas'
benches are outside M2's frozen set in any case. The comparison with C
and Rust waits until after M4.

## Compiler findings

Nothing new. The tree arm first read an integer leaf as `Expr.Num(n) =>
normal([(String.new(), *n)])`. A `shared enum` payload is bound as a
reference (core-semantics.md §4.6), so `*n` is right, and `karac check`
accepts it, but every v2 surface binds it by value and refuses the `*`:
that is kara B-2026-10-18-30, open, which kata 707 found first. The arm
reads it as `n`, which §5.10 makes equally right for a `Copy` payload.
