# 556. Next Greater Element III

Given a positive integer `n`, find the smallest integer which has
exactly the same digits existing in the integer `n` and is greater in
value than `n`. If no such positive integer exists, return `-1`. Note
that the returned integer should fit in 32-bit integer; if there is a
valid answer but it does not fit in 32-bit integer, return `-1`.

```
n = 12  ->  21
n = 21  ->  -1
```

**Constraints:** `1 <= n <= 2^31 - 1`.

## Approaches

Every arm is `fn next_greater_element(n: i64) -> i64`. The answer keeps
as long a prefix of n as it can: it raises the rightmost digit that has
a larger digit somewhere to its right, to the smallest such digit, and
puts the rest in rising order. If the digits only fall from left to
right there is no such digit and the answer is -1, and so is any answer
above 2^31 - 1.

| file | mechanism |
|---|---|
| `next_greater_element_iii.kara` ★ | the next permutation on a `Vec` of digits peeled off with `%` and `/`: the first digit from the right below its neighbour, swapped with the last larger digit, the rest reversed; O(digits) |
| `next_greater_element_iii_text.kara` | the same steps on `n.to_string()` as a `Vec[char]`, collected back into a `String` and read with `i64.parse` |
| `next_greater_element_iii_counts.kara` | no swaps: digits peeled off from the right into counts until one has a larger digit counted, then the number rebuilt from the counts in rising order |
| `next_greater_element_iii_scan.kara` | for every place from the right, the smallest larger digit to its right tried in it and the rest sorted after it, the first place that works kept; O(digits^3 log digits) |
| `differential.kara` | the four arms against the definition, five properties |

Every arm prints the same 13 lines: twelve numbers at the edges (the
examples, one digit, equal digits, answers just under and just over
2^31 - 1, and 2^31 - 1 itself) and a count and checksum over 300 random
numbers. `next_greater_element_iii.py` mirrors the ★ arm and its output
is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
the statement read literally in two ways: up to 7 digits, every order of
the digits, the smallest above n that fits in 32 bits; near 2^31, every
number from n + 1 up to 2^31 - 1 tried in turn, the first with the same
digits. Each arm is held to the properties below on 1,000 random
numbers: from 1 to 1,000, from 1 to 10^7, or within 20,000 of 2^31 -
1, in turn.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | the answer is -1, or larger than n and within 32 bits |
| P3 | the answer has the same digits as n |
| P4 | below 10^9, the answer is -1 exactly when n's digits fall from left to right |
| P5 | the answer's own next is larger again, or -1 |

It prints `1000 cases, 4 arms, 20000 checks, 0 failures` under `karac
__mir-run` and `karac __mir-llvm-run`, and runs clean under `karac
__mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and four that do not, each run under `karac __mir-run`. All
eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the digits after the swap left as they were | P1 391 |
| M2 | ★: the swap partner may equal the digit | P1 71, P2 71, P5 76 |
| M3 | text: no 32-bit check | P1 29, P2 29 |
| M4 | text: the swapped digit reversed with the rest | P1 904, P2 904, P3 13, P5 904 |
| M5 | counts: the raised digit not put back | P1 904, P2 904, P3 904, P5 781 |
| M6 | counts: the raised digit may stay the same | P1 213, P2 213, P4 39, P5 218 |
| M7 | scan: the largest larger digit chosen | P1 175 |
| M8 | scan: the rest reversed, not sorted | P1 250 |
| E1 | ★: the rest sorted, not reversed | 0 |
| E2 | text: the 32-bit check written `>= 2^31` | 0 |
| E3 | counts: `up < 10` written `up <= 9` | 0 |
| E4 | scan: a later equal digit chosen on a tie | 0 |

M1, M7 and M8 give a larger number with the right digits that is not the
smallest, so only P1 sees them. M3 is wrong only above 2^31 - 1, which
29 of the cases near it reach. M2 and M6 can swap a digit for an equal
one, giving n itself or less, which P2 sees; M4 reverses the raised
digit back down, giving a smaller number almost always. P3 sees M5, the
one mutant that loses a digit, and M4 where it turns a leading digit
into a zero. E1 is safe because the digits after the swap are falling,
so reversing them is sorting them; E4 because two equal digits are
interchangeable.

## Verification

Every arm prints the same output as `next_greater_element_iii.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and runs clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. `karac check`
passes on every arm, the differential and the bench program.

The frozen legacy backends: the text and counts arms print the same
output under `karac run --interp`, `karac run` and `karac build`, and
under `KARAC_AUTO_PAR=1 karac build`. The ★ and scan arms, the
differential and the bench program stop at type checking under all three
on `*v` over a `Vec[i64]`'s `iter()` ("unary '*' requires 'ref T' ...
found 'i64'"). Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It builds 500,000 random numbers once,
up to 1,000, 10^7 or 2^31 - 1 in turn; then 20 times over every number
is answered, with a fresh `Vec` of digits each time. Every
implementation prints `500000 numbers, 20 rounds each: 9044780 have a
next, checksum 387455072`, the Kāra program under `karac __mir-run`
included (154 s).

Rust and Go push the digits into a fresh vector as the Kāra arm does,
and C into a fresh `malloc`'d buffer that grows as it fills. Spot
timings on a shared 4-core container, three runs each (two for Python;
`bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.67 to 0.68 s |
| Rust (`rustc -O`) | 0.86 to 0.91 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.89 to 0.98 s |
| Go | 1.53 to 1.68 s |
| Python | 12.3 to 12.7 s |
| Kāra (`karac build --mir`) | 0.62 to 0.66 s |

The legacy `karac build` refuses this program (see Verification). So
`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend; that edit is by hand, on top of the
`scripts/new-bench.sh` output. The `--mir` row is timed at kara
`af2123abc5`. Under `karac __mir-llvm-run` the program prints the same
line in 3.2 s, compile included; that JITs the MIR's IR without
optimization passes, so it is not a benchmark. The Kāra row is level
with C's and a little ahead of Rust's.

## Compiler findings

None new. Nothing was filed from this kata; the legacy failures above
are not filed because legacy is frozen.
