# 640. Solve the Equation

Solve an equation in x that uses only `+`, `-`, whole numbers and terms
in x, each with a coefficient or none (`x` is 1x). Return `x=#value`
when there is one solution, `No solution` when there is none and
`Infinite solutions` when every x works. When there is one solution it
is a whole number.

```
"x+5-3+x=6+x-2"  ->  "x=2"
"x=x"            ->  "Infinite solutions"
"2x=x"           ->  "x=0"
```

**Constraints:** 3 to 1,000 characters with exactly one `=`; every
number from 0 to 100, with no leading zeros.

## Approaches

Every arm is `fn solve_equation(equation: String) -> String`. However it
reads the terms, each arm reduces the equation to a x + b = c x + d, or
equally (a - c) x = d - b: when a = c there is no solution unless b = d,
and then every x is one; otherwise x = (d - b) / (a - c), which divides
exactly. Every arm reads a bare `x` as 1x and `0x` as 0x.

| file | mechanism |
|---|---|
| `solve_the_equation.kara` ★ | each side's bytes scanned once, term by term (a sign, digits, maybe an `x`), into its x count and constant; O(length) |
| `solve_the_equation_once.kara` | one walk over the whole equation with a single x count and constant, every term after the `=` turned over; O(length) |
| `solve_the_equation_split.kara` | every `-` written `+-`, then `split("+")` lists each side's terms with their signs, and `i64.parse` reads each, a trailing `x` taken off; O(length) |
| `solve_the_equation_terms.kara` | a first pass cutting the equation into a `Vec` of terms (a signed number, whether it holds x, which side), then a second adding them up; O(length) |
| `differential.kara` | the four arms against the definition, five properties |

Every arm prints the same 15 lines: the three LeetCode examples; ten
more (no solution; x on the right only; `0x` against a constant; a minus
at the start of each side; constants only, equal and not; a negative
answer; numbers of three digits; `0x` on both sides; and x terms that
cancel); a count of the solved, unsolvable and always-true equations
among 300 random ones of 1 to 6 terms a side with numbers from 0 to
12, and the sum of their solutions; and the answer for a random equation
of 935 characters. The random equations get a constant taken off the
right side so that any single solution is whole, as the problem
promises. `solve_the_equation.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition:
the equation is built from known coefficients, and every whole x from
-300 to 300 is tried in a x + b = c x + d; none working means no
solution, more than one means every x, and otherwise the one that works
is the answer. Each of 1,000 cases has 1 to 4 terms a side with numbers
from 0 to 12, and a constant taken off the right side whenever a - c is
not 0, so that a solution is whole.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | swapping the sides gives the same answer |
| P3 | so does the same term, a constant or a multiple of x, added to both sides |
| P4 | so does every bare `x` written `1x` |
| P5 | so does every sign on both sides turned over |

It prints `1000 cases (922 with one solution), 4 arms, 20000 checks,
0 failures` under `karac __mir-run` and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac
__mir-llvm-run`. All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a number's digits read in base 100 | P1 297 |
| M2 | ★: a bare x read as 0x | P1 56, P4 56 |
| M3 | once: the right side's terms not turned over | P1 590, P3 490 |
| M4 | once: the answer's sign lost | P1 443 |
| M5 | split: every minus read as a plus | P1 574 |
| M6 | split: -x read as x | P1 34, P4 34, P5 59 |
| M7 | terms: 0x read as 1x | P1 73 |
| M8 | terms: the right side's terms not turned over | P1 590, P3 490 |
| E1 | once: a sign reset to 1 after an x term, not 0 | 0 |
| E2 | ★: a constant added only when it has digits | 0 |
| E3 | split: a term holding x, not ending in it | 0 |
| E4 | terms: a bare x also needing a value of 0 | 0 |

P1 kills all eight. P2 sees none: every mutant misreads a term the same
way on either side, or turns over the right side's terms wherever they
are, so swapping the sides swaps an error for its mirror image and the
answer stays the same. P3 sees the two that do not turn over the right
side, M3 and M8, since a term added to both sides then counts twice
instead of cancelling. P4 sees the two that misread a bare x, M2 and
M6, which `1x` corrects. P5 sees M6 alone, since turning the signs over
makes some -x into x and some x into -x, which M6 reads differently. The
four survivors cannot change an answer: an x term leaves a value of
0 behind, so the sign it resets is only ever multiplied by 0; a constant
with no digits is 0; an `x` only ever ends a term; and a term with no
digits has a value of 0.

## Verification

Every arm prints the same output as `solve_the_equation.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints its line under all three. `karac check` passes every arm, the
differential and the bench program. All at kara `d6111aa22a` for the
debug build, with the runtime archives rebuilt from that tree, and
`14acd67779` for the release build that runs `check` and `__mir-run`.

The frozen legacy backends refuse every arm and the differential at
type checking. The ★, once and terms arms hand `seed`, already a
`mut ref` parameter, on to `next_random(mut seed)` with the `mut` marker
design.md asks for, and legacy rejects that marker. The split arm and
the differential also stop because their parameters are still owned
under legacy, so handing `sides[0]` to `side` moves an element out of a
`Vec`. With the markers left out, as an earlier version of this kata
did, `karac run --interp` printed the same output for the three arms and
`karac run` and `karac build` panicked in code generation
(`src/codegen/assoc_call.rs:2826`, an integer where a struct was
expected, the same panic kata 639 meets). Legacy is frozen, so these are
noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It makes 20 equations once, each of
125 terms a side with numbers from 0 to 99, 820 to 873 characters, with
a constant taken off the right side so that each has a whole solution;
then 200,000 rounds each solve one of them, picked by the round,
counting the solutions and adding them up. Every implementation prints
`20 equations, 200000 rounds: 200000 solved, x adding to -230000`, the
Kāra program under `karac __mir-run` included (in 220 s).

Each implementation scans each side's bytes once and builds its answer
as a new string: Rust with `format!`, C with `snprintf` into a caller's
buffer, after a `strlen` to find the end, Go with `strconv.FormatInt`
and Python with an f-string. Spot timings on a shared 4-core container,
three runs each (two for Python; `bench.sh` timings need a quiet
machine), each including making the equations:

| | time |
|---|---|
| C (`clang -O3`) | 0.41 to 0.43 s |
| Rust (`rustc -O`) | 0.25 to 0.31 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.55 to 0.59 s |
| Go | 0.48 to 0.59 s |
| Python | 21.5 to 22.3 s |
| Kāra (`karac build --mir`) | 0.33 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, since the legacy `karac build` refuses the bench
program: handing `equations[round % 20]` to `solve_equation` moves an
element out of a `Vec` while parameters are owned, and it rejects the
`mut` markers above. That edit is by hand, on top of the
`scripts/new-bench.sh` output. A copy outside the kata that adds
`.clone()` to the argument and leaves out the markers, copying an
equation every round, builds under legacy and takes 0.63 to 0.67 s.
Under `karac __mir-llvm-run` the program prints the same line in 3.0 s,
compile included; that JITs the MIR's IR without optimization passes, so
it is not a benchmark.

The Kāra build, with its overflow checks on, sits between Rust without
them and Rust with them, and ahead of C, Go and Python. That Rust's
checked build takes twice its unchecked one is measured; why the checks
cost Rust more than Kāra here is not examined.

## Compiler findings

None. The legacy failures above are not filed because legacy is frozen.
