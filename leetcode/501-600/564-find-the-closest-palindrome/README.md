# 564. Find the Closest Palindrome

Given a string `n` representing an integer, return the closest integer
(not including itself) which is a palindrome. If there is a tie, return
the smaller one. The closest is defined as the absolute difference
minimized between two integers.

```
n = "123"  ->  "121"
n = "1"    ->  "0"     (0 and 2 are both 1 away; the smaller wins)
```

**Constraints:** `1 <= n.length <= 18`; `n` consists of only digits and
has no leading zeros; `n` represents an integer in the range
`[1, 10^18 - 1]`.

## Approaches

Every arm is `fn nearest_palindromic(n: String) -> String`.

| file | mechanism |
|---|---|
| `nearest_palindromic.kara` ★ | five candidates: n's first half, and that half one smaller and one larger, each mirrored into a palindrome of n's length; and 99...9 one digit shorter and 10...01 one digit longer. The nearest that is not n wins, the smaller on a tie; O(digits) |
| `nearest_palindromic_digits.kara` | the same five candidates in arithmetic: the half is n divided by a power of ten and mirrored by peeling digits off with `%` and `/`, each candidate offered to a closure that keeps the best; a neighbouring half that has lost or gained a digit is skipped |
| `nearest_palindromic_sides.kara` | the nearest palindrome above n and the nearest below found separately from n's own mirrored half, the next half up or down, or 10...01 and 99...9 when that half changes length; the nearer of the two, the one below on a tie |
| `nearest_palindromic_sorted.kara` | the five candidates built as text, each read with `if let Ok(c) = i64.parse(t)` and paired with its distance from n; the pairs sorted, the first that is not n taken |
| `differential.kara` | the four arms against the definition, five properties |

Every arm prints the same 19 lines: 17 numbers at the edges (the two
examples, the numbers either side of 10, 100 and 1000, where the answer
can change length and 10 and 1000 are ties, halves that carry or borrow,
and the problem's largest numbers), a checksum over every number from
1 to 3,000, and a count and checksum over 300 random numbers of 1 to
18 digits, plain, palindromes, or a power of ten moved by up to 3, in
turn. `nearest_palindromic.py` mirrors the ★ arm and its output is
byte-identical.

The sorted arm does not build today; see Compiler findings. It is kept
as written. A copy outside this directory that reads the text with `if
let Some(c) = i64.parse(t)`, the only change, prints the same output.

## Differential

`differential.kara` holds copies of the four arms and the definition,
the statement read literally: try the numbers 1 away from n, then
2 away, and so on, the smaller of each pair first, until one is a
palindrome. Each arm is held to the properties below on 1,000 random
numbers of 1 to 6 digits: plain, a palindrome, or within 3 of a power of
ten, in turn.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | the answer is a palindrome, is not n, and has no leading zeros |
| P3 | the answer is at most one digit longer or shorter than n |
| P4 | no palindrome other than n is nearer to n |
| P5 | on a tie the smaller is taken |

Since the sorted arm does not build, the differential does not either:
`karac check` and the MIR backends stop at its copy of that arm. The
copy outside this directory with `Some(c)` in that one place prints
`1000 cases, 4 arms, 20000 checks, 0 failures` under `karac __mir-run`
and `karac __mir-llvm-run`, and runs clean under `karac
__mir-llvm-asan`.

## Mutation testing

Twelve edits to the workaround copy of the differential, two to each arm
that change its answers and one to each that does not, each run under
`karac __mir-llvm-run`. All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a tie settled by the larger | P1 471, P2 18, P5 471 |
| M2 | ★: the 99...9 candidate dropped | P1 67, P4 40, P5 27 |
| M3 | digits: an odd length's middle digit mirrored too | P1 251, P2 249, P4 87, P5 3 |
| M4 | digits: n itself allowed as the answer | P1 549, P2 549 |
| M5 | sides: a tie settled by the one above | P1 453, P5 453 |
| M6 | sides: the case for 10 to 19 below dropped | P1 29, P4 19, P5 10 |
| M7 | sorted: the candidates not sorted | P1 903, P4 903, P5 77 |
| M8 | sorted: one digit too many skipped from the back | P1 676, P4 676, P5 4 |
| E1 | ★: the distance taken the other way round | 0 |
| E2 | digits: digits counted until the rest is 0, not above 0 | 0 |
| E3 | sides: the tie comparison written the other way round | 0 |
| E4 | sorted: n skipped by its difference being 0 | 0 |

Ties are common: a palindrome n usually has its neighbours at the same
distance either side, 12221 and 12421 around 12321, so M1 and M5 fail on
almost half the cases, and only on P1 and P5. The 18 P2 failures under
M1 are the cases with n = 9: the ★ arm's half one larger, 10, mirrors to
10, not a palindrome, and it ties with 8 and loses only on the tie rule.
M4 answers n itself whenever n is a palindrome. M8's three mirrored
texts come out a digit short and far from n, so the arm falls back to
99...9 or 10...01: wrong, but a palindrome of a nearby length, which
P2 and P3 accept. P3 sees none of the mutants, since every one still
picks among candidates within a digit of n's length. E2 is safe because
the digits arm counts only halves of 0 or more.

## Verification

The ★, digits and sides arms print the same output as
`nearest_palindromic.py` under `karac __mir-run` (the v2 MIR
interpreter) and `karac __mir-llvm-run`, and run clean under `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer): output identical,
no error, no leak. `karac check` passes on those three and the bench
program; it refuses the sorted arm and the differential
(B-2026-10-12-6). The workaround copy of the sorted arm prints the same
output on the three MIR lanes.

The frozen legacy backends: `karac run --interp` prints the right output
for the ★, digits and sides arms. `karac run` and `karac build` fail on
those three in code generation, on the harness's `n.to_string()` where
`n` is a `Str` ("no handler for method 'to_string' on variable 'n'").
The sorted arm and the differential stop at type checking, as on every
backend. Legacy refuses the bench program too (see Benchmarks). Legacy
is frozen, so these are noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It makes 10,000 random numbers of 1 to
18 digits once, as the test harness does; then 300 times over every
number is answered and the answer read back into the checksum. Every
implementation prints `10000 numbers, 300 rounds: checksum
807375207`, the Kāra program under `karac __mir-run` included (109 s).

Rust, Go and Python follow the arm: each candidate's half is written out
with the language's own integer formatting, mirrored and parsed back. C
does the same with `snprintf` and `strtoll` into `malloc`'d strings, and
returns a fresh string, as the Kāra arm returns a fresh `String`. Spot
timings on a shared 4-core container, three runs each (two for Python;
`bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 1.38 to 1.59 s |
| Rust (`rustc -O`) | 1.56 to 1.81 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.49 to 1.55 s |
| Go | 1.38 to 1.42 s |
| Python | 10.3 to 11.7 s |
| Kāra (`karac build --mir`) | 3.26 to 3.83 s |

The legacy `karac build` refuses this program, since it moves
`numbers[(round * 7 + g) % count]` out of the index where v2 borrows it.
So `bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend; that edit is by hand, on top of the
`scripts/new-bench.sh` output. The `--mir` row is timed at kara
`a87257d083`. Under `karac __mir-llvm-run` the program prints the same
line in 23.4 s, compile included; that JITs the MIR's IR without
optimization passes, so it is not a benchmark.

The Kāra row is about twice Rust's, and about half of the gap is the
round trip from number to text and back that each candidate makes.
Measured alone with `karac build --mir` against `rustc -O`, 15 million
`x.to_string()` of a 15-digit number take 1.02 s against 0.41 s, and
15 million `i64.parse` of short texts 0.68 s against 0.23 s. Each answer
here does six parses and four `to_string` calls, which comes to about
1 s more than Rust over the 3 million answers. On the compiled MIR
backend `to_string` goes through the f-string buffer, three allocations
for one number (kara B-2026-10-13-20), and `i64.parse` copies its text
into a fresh heap `String` and parses an `i128` (B-2026-10-13-34).

## Compiler findings

None new. The sorted arm meets kara B-2026-10-12-6 (open): the spec
gives every number type `parse(s: Str) -> Result[Self, ParseError]`, but
the compiler still returns `Option[Self]`, so the arm's `if let Ok(c) =
i64.parse(t)` is refused by `karac check` and both MIR backends with
"pattern `Ok(..)` is an enum-variant pattern, but the scrutinee has type
`Option[i64]`". The arm keeps the spec's spelling. The legacy failures
above are not filed because legacy is frozen.
