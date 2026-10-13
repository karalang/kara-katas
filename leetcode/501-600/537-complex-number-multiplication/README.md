# 537. Complex Number Multiplication

A complex number can be written as a string `"real+imaginaryi"`, where
`real` and `imaginary` are integers in `[-100, 100]` and `i^2 = -1`.
Given two complex numbers `num1` and `num2` as strings, return their
product as a string in the same form.

```
num1 = "1+1i",  num2 = "1+1i"   ->  "0+2i"
num1 = "1+-1i", num2 = "1+-1i"  ->  "0+-2i"
```

**Constraints:** `num1` and `num2` are valid complex numbers.

## Approaches

Every arm is `fn complex_number_multiply(num1: Str, num2: Str) ->
String`. The answer is `(a + bi)(c + di) = (ac - bd) + (ad + bc)i`,
written with a `+` between the parts even when the imaginary part is
negative.

| file | reading the numbers | the product |
|---|---|---|
| `complex_number_multiply.kara` ★ | `split("+")`, the `i` dropped, each part parsed | the schoolbook four products |
| `complex_number_multiply_scan.kara` | one pass over the bytes: a sign, digits, the `+`, a sign, digits | the schoolbook four products |
| `complex_number_multiply_gauss.kara` | `find("+")` and two slices | Gauss's three products: `k1 = c(a + b)`, `k2 = a(d - c)`, `k3 = b(c + d)`, then `k1 - k3` and `k1 + k2` |
| `complex_number_multiply_matrix.kara` | `find("+")` and two slices | `a + bi` as the matrix `[[a, -b], [b, a]]`; the matrices multiplied and the answer read off the first column |
| `differential.kara` | the four arms against the definition, five properties | |

The ★ arm collects `num.split("+")` into a `Vec[Str]`, as
`docs/library/strings.md` writes it. `karac` refuses that: its `split`
still returns an eager `Vec[String]` (kara B-2026-10-12-7, open). The
arm and the differential keep the spec's spelling. A copy that takes
`num.split("+")` as the `Vec[String]` it is was checked as described
under Verification.

Every arm prints the same 13 lines: eleven products (the two examples,
`i` times `i`, times 1 and -1, times 0, a number by its conjugate, the
corners of the range and mixed signs), then for 3,000 random pairs,
one in ten a number and its conjugate, how many products are real and
a checksum over the products as written, and last a checksum over
every number with both parts in range times `-37+59i`, 40,401 of
them. `complex_number_multiply.py` mirrors the ★ arm and its
output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition:
the four products of the parts, each times the power of `i` it
carries, summed part by part. Each arm is held to the properties below
on 2,000 random pairs whose parts run from -100 to 100, or one time in
four from -10^4 to 10^4 (as large as the product of two numbers in
range, so that P4 multiplies products), and a third number in range.

| | property |
|---|---|
| P1 | the product is the definition's |
| P2 | the numbers the other way round give the same product |
| P3 | times `1+0i` is the number, and times `0+1i` turns it a quarter: `a+bi` to `-b+ai` |
| P4 | `(x y) z = x (y z)` |
| P5 | a number times its conjugate is the square of its size, `a^2+b^2` and `0i` |

It prints `2000 cases, 4 arms, 40000 checks, 0 failures` under `karac
__mir-run` on the copy of the ★ arm that takes the `Vec[String]`.

## Mutation testing

Twelve edits to the copy of `differential.kara` that takes the
`Vec[String]`, two to each arm that change its answers, and four that
do not, each run under `karac __mir-run`. All eight that change
answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: `i` times `i` taken as 1 | P1 1992, P3 1998, P5 1998 |
| M2 | ★: the imaginary part as `ad - bc` | P1 1986, P2 1999, P3 1998, P4 1998, P5 1991 |
| M3 | scan: the sign never applied | P1 1738, P3 1544, P4 1305, P5 1998 |
| M4 | scan: the second number's `+` not stepped over | P1 1994, P2 1999, P3 2000, P5 1998 |
| M5 | gauss: `k2 = a(d + c)` | P1 1981, P3 1993, P4 2000, P5 1993 |
| M6 | gauss: the real part `k1 + k3` | P1 1994, P2 1999, P3 1998, P4 1998, P5 1995 |
| M7 | matrix: `a + bi` as `[[a, b], [b, a]]` | P1 1992, P3 1998, P5 1998 |
| M8 | matrix: the imaginary part read off the first row | P1 2000, P3 2000, P4 2000 |
| E1 | ★: each product written the other way round | 0 |
| E2 | scan: digits read up to the `+` or the `i` | 0 |
| E3 | gauss: the real part as `ac - bd` | 0 |
| E4 | matrix: the real part read off the second column | 0 |

M1 and M7 are one mistake in two arms: both multiply as if `i^2` were
1, which keeps the product commutative and associative, so only P1, P3
and P5 see it, in the same cases. M8 reads `-(ad + bc)` for the
imaginary part: the negated product of two numbers is still
commutative, and a number times its conjugate has no imaginary part to
negate, so P2 and P5 miss it. M4 reads the second number's imaginary
part as 0, which no longer commutes. E2 changes nothing because a part
ends at the `+` or the `i` anyway, E3 writes out what `k1 - k3` comes
to, and E4 reads the matrix's other copy of the real part.

## Verification

Every alternative arm prints the same output as
`complex_number_multiply.py` under `karac __mir-run` (the v2 MIR
interpreter) and `karac __mir-llvm-run`, and runs clean under `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer): output identical,
no error, no leak. The ★ arm, the differential and the bench program are
refused by every `karac` command, `check` included, at the `collect` of
`split` (B-2026-10-12-7). Their copies that take `num.split("+")` as a
`Vec[String]` (the one line changed) pass the same three runs: the ★
copy's output is byte-identical to the mirror's, the differential copy
prints `40000 checks, 0 failures`, and the bench copy prints the
mirrors' line.

The frozen legacy backends refuse every file at type checking. The ★
arm, the differential and the bench program stop at the same `split`.
The other three arms stop at the checksum's `*b`, "unary '*' requires
'ref T' ... found 'u8'": legacy types the items of a `Vec`'s `iter()` by
value. Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It makes 2,000 random numbers with
both parts from -100 to 100 once; then in each of 2,500 rounds it
multiplies every number by another, picked by the round. Every
implementation prints `2000 numbers, 2500 rounds: 1205 real, length
53383699`, and so does the Kāra copy described below, under `karac
__mir-run` too (in 57 s).

No Kāra build of the bench program as written exists yet: every
`karac` command refuses its `split` (B-2026-10-12-7, above), and the
legacy `karac build` refuses it as well (see Verification). So
`bench.sh` builds it with `karac build --mir`, the v2 compiled backend,
and will time it once the row is fixed; that edit is by hand, on top
of the `scripts/new-bench.sh` output.

Every mirror splits each number at its `+` and writes the product into
a fresh string. Rust collects `split('+')` into a `Vec<&str>`, as the
★ arm would; Go uses `strings.Split` and `fmt.Sprintf`; C reads the two
parts with `strtoll` and writes the product with `snprintf` into a
fresh `malloc`'d string. Spot timings on a shared 4-core container,
three runs each (two for Python; `bench.sh` timings need a quiet
machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.97 to 0.98 s |
| Rust (`rustc -O`) | 1.05 to 1.11 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.10 to 1.17 s |
| Go | 1.83 to 2.09 s |
| Python | 6.2 to 6.3 s |
| Kāra (`karac build --mir`), the `Vec[String]` copy | 2.56 to 2.61 s |

The Kāra row times the copy, at kara `2649217dc8`, and is not quite
the ★ arm's cost: the copy's `split` makes a `String` of each part,
two allocations per number that a `split` of views would not make.
Under `karac __mir-llvm-run` the copy prints the same line in 17.5 s,
compile included; that JITs the MIR's IR without optimization passes,
so it is not a benchmark.

## Compiler findings

kara B-2026-10-12-7 (open), filed from kata 388 and met again here:
`split` returns an eager `Vec[String]` of copies, where
`docs/library/strings.md` gives it `impl Iterator[Item = Str]` of
views, so the spec's own `num.split("+").collect()` into a `Vec[Str]`
is refused ("no method 'collect' on type 'Vec'"). It blocks the ★ arm,
the differential and the bench program under every `karac` command;
the copies that take the `Vec[String]` run right. Nothing new filed.
