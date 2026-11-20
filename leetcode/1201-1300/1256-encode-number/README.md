# 1256. Encode Number

Given a non-negative integer `num`, Return its *encoding* string.

The encoding is done by converting the integer to a string using a
secret function that you should deduce from the following table:

| n | f(n) |
|---|---|
| 0 | "" |
| 1 | "0" |
| 2 | "1" |
| 3 | "00" |
| 4 | "01" |
| 5 | "10" |
| 6 | "11" |
| 7 | "000" |

```
num = 23   ->  "1000"
num = 107  ->  "101100"
```

**Constraints:** `0 <= num <= 10^9`.

The arms are `fn encode(num: i64) -> String`.

## Approaches

The table lists every string of 0s and 1s, the shorter first and those
of one length counting up in binary, so `num`'s string is `num + 1` in
binary with its leading 1 taken off.

| file | mechanism |
|---|---|
| `encode_number.kara` ★ | `num + 1`'s binary digits found by halving into a `Vec[char]`, its leading 1 left out by stopping at 1, and the digits collected in reverse |
| `encode_number_format.kara` | by formatting: `f"{num + 1:b}"`, and the slice after its first digit |
| `encode_number_length.kara` | by length: the largest `k` with `2^k - 1 <= num` is the string's length, and the string is `num - (2^k - 1)` in exactly `k` digits, high bit first, with shifts |
| `encode_number_bijective.kara` | as bijective numbering: one taken off before every halving, so no `+ 1` at all, each digit put at the front of a `Vec[char]` with `insert(0, ..)` |
| `encode_number_solution.kara` | a Rust solution as LeetCode's Rust users write it (`format!("{:b}", num as i64 + 1)[1..].to_string()`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 3 lines: LeetCode's two examples with the
table's first eight strings; the digits and a checksum of them for 1000
random numbers from 0 to 10^9 and the numbers 0 to 99999 (`1496681
digits, checksum 498502900`); and the strings of 10^9, 2^30 - 2 (thirty
1s less one) and 2^30 - 1 (thirty 0s). `encode_number.py` mirrors the ★
arm, and its output is byte-identical. Every arm gives the same output
under `karac run` and `karac build`, and under the AddressSanitizer
build.

The Mend loop: the ★, formatting and length arms checked clean as first
written. The bijective arm was first written with Rust's
`s.insert(0, c)` on a `String`, which Kāra does not edit by position;
the diagnostic (E0236) names the route, a `Vec[char]` whose `insert`
does, collected into the `String` at the end, and the arm is written
that way. The solution arm takes one round of fixes, 2 edits by `karac
fix`'s count: `struct Solution;` to `struct Solution {}`, and
`format!("{:b}", num as i64 + 1)` to the f-string `f"{num as i64 +
1:b}"`, which keeps its `[1..]` slice. All five check clean.

## Gaps

None found: every arm, as written, checks after its fixes, and runs and
builds alike. Two Rust habits in the harness and the bench met
diagnostics that name the route: `s.as_bytes()`, which `karac fix`
rewrites to `s.bytes()`, and `s.get(1..)` on a `String`, which reads
only "no method 'get' on type 'String'" and is taken up in the compiler
with Kāra's `s[a..b]` and `substring` named.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the table's strings in its order, each made from the one
before by adding one to its last digit and carrying, a string of 1s
followed by the 0s one longer, the first 10002 of them. 2000 cases, half
from 0 to 4999, read from that table, and half from 0 to 10^9, where the
table does not reach.

| | property |
|---|---|
| P1 | the statement read literally (for the numbers below 5000) |
| P2 | as many digits as halvings take `num + 1` to 1 |
| P3 | the strings of `2 num + 1` and `2 num + 2` are `num`'s with a 0 and a 1 added |
| P4 | before the string of `num + 1`: shorter, or as long and smaller |
| P5 | a 1 put in front and read in binary gives `num + 1` |
| P6 | the ★ arm's string |

All 60,000 checks pass on every arm: `2000 numbers: checksum 85408230,
60000 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and the AddressSanitizer build. Python, with `bin`,
gives the same checksum.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac run`, each failing the same way under both.

| # | mutation | failures by property |
|---|---|---|
| S1 | ★: the leading 1 kept | P1 1000, P2 2000, P5 2000, P6 8000 |
| S2 | ★: the digits not reversed | P1 956, P3 1999, P4 991, P5 1955, P6 7820 |
| F1 | formatting: the slice from the first digit | P1 1000, P2 2000, P5 2000, P6 2000 |
| F2 | formatting: `num` written in place of `num + 1` | P1 999, P2 4, P3 2000, P4 1, P5 1999, P6 1999 |
| N1 | length: `<` in place of `<=` in finding the length | P1 4, P2 4, P3 5, P4 1, P5 4, P6 4 |
| N2 | length: `2^k` taken off in place of `2^k - 1` | P1 999, P3 2000, P4 4, P5 1999, P6 1999 |
| J1 | bijective: no one taken off before halving | P1 999, P2 1995, P3 2000, P5 1999, P6 1999 |
| J2 | bijective: the two digits swapped | P1 999, P3 2000, P4 1999, P5 1999, P6 1999 |
| L1 | solution: `num + 2` | P1 1000, P2 1, P3 2000, P5 2000, P6 2000 |
| L2 | solution: `:o`, octal, in place of `:b` | P1 999, P2 1999, P3 1998, P4 8, P5 1999, P6 1999 |

All ten are caught, every one by P1, the statement read literally, and
by P6, which fails on the other four arms too when the ★ arm is the one
mutated (S1, S2), and by P5, reading the string back. N1 is the
narrowest: it goes wrong only when `num` is one less than a power of
two, the first string of each length, and 4 of the 1000 small cases are
such numbers; every property catches it there. P2, the length, misses
the three that keep the length and get the digits wrong (S2, N2, J2),
and catches F2 and L1 only where `num + 1` and their number cross a
power of two apart. P3, the strings of `2 num + 1` and `2 num + 2`, catches
all but the two that keep the leading 1 (S1, F1), which add their digit
just as well. P4, the order, catches the ones that scramble the order
within a length (S2, J2) and, rarely, those off by one at a power of two.

## Benchmarks

`bench/` runs the same workload in Kāra, C, Rust, Go and Python: the ★
arm (`num + 1` in binary with its leading 1 taken off, the digits found
by halving) on 200000 random numbers from 0 to 10^9 drawn once, each
encoded 20 times; every string's length and middle digit folded into a
checksum. Every program prints `20 rounds of 200000 numbers: checksum
301169842`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `684b860a50`
on LLVM 22. A plain `karac build` targets x86-64-v2, so the C and
overflow-checked Rust programs are also built at x86-64-v3 for
comparison:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 0.518 to 0.564 s | 0.543 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.536 to 0.666 s | 0.550 s |
| Rust (`rustc -O`) | 0.879 to 1.016 s | 0.922 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.858 to 1.076 s | 0.911 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.915 to 1.074 s | 0.945 s |
| C (`clang -O3`) | 0.211 to 0.335 s | 0.228 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.221 to 0.249 s | 0.228 s |
| Go | 0.938 to 1.025 s | 0.959 s |
| Python | 12.59 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Rust with overflow checks on takes about 1.7x Kāra's time. Kāra
takes about 2.4x C's time (0.550 s against 0.228 s); Go takes about 1.7x
Kāra's time. Python takes about 23x Kāra's time. No profile was taken.
