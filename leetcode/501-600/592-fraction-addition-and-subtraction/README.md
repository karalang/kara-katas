# 592. Fraction Addition and Subtraction

Given a string `expression` representing an expression of fraction
addition and subtraction, return the calculation result in string
format. The final result should be an irreducible fraction. If your
final result is an integer, change it to the format of a fraction that
has a denominator `1`. So in this case, `2` should be converted to
`2/1`.

```
expression = "-1/2+1/2"      ->  "0/1"
expression = "-1/2+1/2+1/3"  ->  "1/3"
expression = "1/3-1/2"       ->  "-1/6"
```

**Constraints:** the input string only contains `'0'` to `'9'`, `'/'`,
`'+'` and `'-'`, and so does the output; each fraction (input and
output) has the format `±numerator/denominator`, and if the first input
fraction or the output is positive, then `'+'` will be omitted; the
input only contains valid irreducible fractions, where the numerator and
denominator of each fraction will always be in the range `[1, 10]`, and
if the denominator is `1`, the fraction is an integer; the number of
given fractions will be in the range `[1, 10]`; the numerator and
denominator of the final result are guaranteed to be valid and in the
range of a 32-bit int.

## Approaches

Every arm is `fn fraction_addition(expression: Str) -> String`.

| file | mechanism |
|---|---|
| `fraction_addition.kara` ★ | a running sum: each fraction read as a sign, digits, `/` and digits from the expression's `Vec[char]`, added over the least common multiple of the two denominators, and the sum reduced by the greatest common divisor every time; O(n) |
| `fraction_addition_common.kara` | one common denominator: every denominator is from 1 to 10, so each divides 2520, and a/b is 2520/b * a over 2520; the numerators are added as the characters go by and the sum reduced once at the end; O(n) |
| `fraction_addition_split.kara` | cut, then add: the expression cut before every sign but the first into `Str` pieces, each parsed with `i64.parse` either side of its `/`, then added over the product of the denominators and reduced; O(n) |
| `fraction_addition_rational.kara` | a `Fraction` type that keeps itself in lowest terms, with `impl Add` for it, so the sum is the fractions folded with `+` |
| `differential.kara` | the four arms against the definition, five properties |

Every arm prints the same 13 lines: the three examples above, nine cases
at the edges (one fraction; whole numbers; ten fractions of 10 and of
-10, the largest sums; every denominator from 1 to 10, added and
alternated; terms that reduce only together; a sum of 0), and a count
and checksum over 1,000 random expressions of 1 to 10 fractions.
`fraction_addition.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
which reads no text: the harness draws each case as three lists, the
signs, numerators and denominators, and writes the expression from them.
The definition puts every fraction over the product of all the
denominators, adds the numerators, and divides both by their greatest
common divisor, found by subtraction. Each of 1,000 cases has 1 to
8 irreducible fractions, so that P3 stays inside the problem's 10; every
fourth draws them from 1/1, 1/2, 1/3, 2/1 and 2/3, so that terms repeat.
4 of the sums are 0 and 58 more are whole.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | the answer is in lowest terms: a denominator of at least 1 sharing no factor with the numerator, so 0 is only ever `0/1` |
| P3 | one more fraction added and then taken away changes nothing |
| P4 | the fractions in the opposite order give the same answer |
| P5 | every sign turned over turns the answer's over |

Both MIR backends stop at the differential's `Ok` and `Err` patterns on
`i64.parse`, as `karac check` does; see Compiler findings. A copy
outside this directory with `Some` and `None` for the patterns, the only
change, prints `1000 cases (4 zero, 58 other whole), 4 arms,
20000 checks, 0 failures` under `karac __mir-run` and `karac
__mir-llvm-run`, and runs clean under `karac __mir-llvm-asan`.

## Mutation testing

Twelve edits to a copy made before kara B-2026-10-14-30 was fixed, which
also had the rational arm's `add` as an ordinary method called as
`sum.add(...)`: two to each arm that change its answers and one to each
that does not, each run under `karac __mir-run`. All eight that change
answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a `-` read as `+` | P1 871, P3 1000, P5 1000 |
| M2 | ★: the sum never reduced | P1 291, P2 291, P3 283 |
| M3 | common: every sign after the first read as `-` | P1 738, P3 1000, P4 647, P5 871 |
| M4 | common: 1260 for the common denominator | P1 235 |
| M5 | split: the running numerator not scaled by the new denominator | P1 834, P3 840, P4 847 |
| M6 | split: the sum reduced by the divisor its numerator shares with the new denominator only | P1 291, P2 291, P3 283 |
| M7 | rational: denominators added, not multiplied | P1 995, P3 978, P4 840 |
| M8 | rational: the divisor's sign kept | P1 242, P2 242, P5 478 |
| E1 | ★: a digit's value by `to_digit` | 0 |
| E2 | common: the divisor taken as the gcd of 2520 and the sum | 0 |
| E3 | split: a cut wherever the piece so far is not empty | 0 |
| E4 | rational: the two products added the other way round | 0 |

P1 kills all eight. M4 is seen by nothing else: 1260 is every
denominator's multiple but 8's, so only expressions holding an eighth go
wrong, and in the same way whatever is added, removed or reordered.
P2 sees the three that leave a sum that can still be reduced: M2 and
M6, on 291 cases each, and M8, whose divisor can come out negative when
the numerator is, leaving `1/-2` where `-1/2` belongs. M1 fails P3 and
P5 on every case: with `-` read as `+`, a fraction taken away is added
again, and every sign turned over gives the same answer, not its
opposite. M3 reads every sign after the first as `-`, so writing the
fractions in the opposite order moves which one escapes, and P4 sees it
on 647. E2 is safe because the gcd here never depends on its order, and
E3 because `start` is 0 until the first cut and behind `i` after it.

## Verification

Every arm prints the same output as `fraction_addition.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. `karac check`
passes every arm and the bench program; it refuses the differential (see
Compiler findings). `karac check` and `karac __mir-run` at kara
`5ff30e5f1c`, the compiled MIR backend at `555c29b44e`; the rational arm
at `2d241d9b05`, after kara B-2026-10-14-30 was fixed.

On the frozen legacy backends, `karac run --interp` prints the same
output for the ★, common and split arms. `karac run` and `karac build`
build none of them: the ★ arm stops in codegen at
`expression.chars().collect()` ("no handler for method 'len' on variable
'expression'"), the common arm's `for c in expression.chars()` panics
the compiler's for-loop lowering, and the split arm's `for (i, c) in
expression.chars().enumerate()` is "not yet lowered". The rational arm
and the differential are still refused at resolve, since the fix for
B-2026-10-14-30 is on v2 only, and `karac build` refuses the bench
program at type checking, reading `expressions[..]` as a move out of an
index (E_INDEX_MOVE_NON_COPY). Legacy is frozen, so this is noted, not
filed.

## Benchmarks

The bench program uses the ★ arm. It makes 1,000 random expressions of
10 fractions, the problem's most, once, and then 1,000 times over adds
every one up, folding the characters of each answer into a checksum.
Every implementation prints `1000 expressions, 1000 rounds:
532000 negative, checksum 264094699`, the Kāra program under `karac
__mir-run` included (118 s).

Each implementation is the same scan, each answer a fresh string. Rust
collects the expression into a `Vec<char>` and Go into a `[]rune`, as
the Kāra arm collects a `Vec[char]`; C reads the expression's bytes
where they are and writes the answer into a buffer the caller gives,
with `snprintf`; Python spells out Kāra's truncating `/` and `%`. Spot
timings on a shared 4-core container, three runs each (two for Python;
`bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.84 to 0.86 s |
| Rust (`rustc -O`) | 0.93 to 1.10 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.09 to 1.10 s |
| Go | 1.24 to 1.34 s |
| Python | 21.8 to 23.3 s |
| Kāra (`karac build --mir`) | 1.38 to 1.52 s |

So `bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend; that edit is by hand, on top of the
`scripts/new-bench.sh` output. The `--mir` row is timed at kara
`555c29b44e`. Under `karac __mir-llvm-run` the program prints the same
line in 8.4 s, compile included; that JITs the MIR's IR without
optimization passes, so it is not a benchmark.

The Kāra row is about 1.4 times Rust's. A callgrind profile of the same
program at 50 rounds puts 18% of its instructions in `karac_mir_char`,
the runtime function the compiled backend calls for `is_ascii_digit`:
one call for every digit read and one for the character after, about two
million in those 50 rounds, each finding the method by comparing its
name; kara B-2026-10-13-31 (open) already records this for
`is_ascii_uppercase`, with the remedy of testing the ASCII ranges in
line. Another 13% is `malloc` and `free`, for the `Vec[char]` and the
answer string of every call, which the Rust program makes too. That the
char calls are where most of the gap comes from is read from the
profile; it is not measured by changing the program.

## Compiler findings

**kara B-2026-10-14-30** (found by this kata; fixed in `d02338bc95`). A
user type could not implement `Add`: the rational arm's `impl Add for
Fraction`, which design.md § Operator traits allows, was refused at name
resolution by `karac check` and both MIR backends, with "operator traits
are stdlib-only". It builds and runs on v2 now; legacy, frozen, still
refuses it.

**kara B-2026-10-12-6** (open). The differential's `lowest_terms`
matches `i64.parse` with `Ok` and `Err`, as library/core-types.md §
Parsing gives `fn parse(s: Str) -> Result[Self, ParseError]`; the
compiler still returns an `Option`, so `karac check` and `karac
__mir-run` refuse those four patterns. The
arms call `i64.parse(...).unwrap()`, which is spelled the same either
way.
