# 639. Decode Ways II

A message of letters A to Z was encoded as numbers, A as 1 up to Z as
26, written one after another. Given the encoded string, which may also
hold `*`, standing for any digit from 1 to 9, return the number of ways
to decode it, modulo 10^9 + 7. A decoding splits the string into letters
of one or two characters; a letter cannot begin with 0, so `06` is not
F.

```
s = "*"   ->  9     (A to I)
s = "1*"  ->  18    (A then A to I, or K to S)
s = "2*"  ->  15    (B then A to I, or U to Z)
```

**Constraints:** 1 to 10^5 characters, each a digit or `*`.

## Approaches

Every arm is `fn num_decodings(s: String) -> i64` over the string's
bytes. A decoding of a prefix ends in a letter read from its last
character or from its last two, so every arm adds the ways the prefix
one shorter can be followed by one letter to the ways the prefix two
shorter can be followed by a two-character one. A `*` alone is
9 letters; `**` is 15 two-character ones (11 to 19 and 21 to 26), `*`
then a digit is 2 up to 6 and 1 above, `1*` is 9 and `2*` is 6. Counts
are reduced modulo 10^9 + 7 at every step, so no product exceeds 15 x
(10^9 + 7).

| file | mechanism |
|---|---|
| `decode_ways_ii.kara` ★ | the counts for the last two prefixes, rolled forward one character at a time; O(n) time, O(1) space |
| `decode_ways_ii_table.kara` | a `Vec` of the count for every prefix, the empty one counting 1; O(n) time and space |
| `decode_ways_ii_states.kara` | counts of partial decodings by what they leave open: nothing, a pending 1 or a pending 2 that the next character may close into a letter; O(n) time, O(1) space |
| `decode_ways_ii_backward.kara` | the count for every suffix, filled from the end, each the ways to start with a one- or two-character letter; O(n) time and space |
| `differential.kara` | the four arms against the definition, five properties |

Every arm prints the same 18 lines: the three LeetCode examples; twelve
more (a lone 0; a 0 after 1, after 2, after 3 and after a star; a star
after a 0; two stars; a star then 7; 27 and 26; a star, a 0 and a star;
and 1s and stars by turns ending in a 0); the total and a checksum of
the counts for 300 random strings of 1 to 30 characters, with up to
59 in 100 stars and up to 19 in 100 zeros among the digits; and the
counts for 100,000 stars and for 100,000 characters mixing stars with
the digits 1 to 9. `decode_ways_ii.py` mirrors the ★ arm and its output
is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition: a
decoding from a position is any letter from 1 to 26 that the next one or
two characters can spell, a `*` standing for any of 1 to 9, followed by
a decoding of the rest; every letter is tried and nothing is remembered.
Each of 1,000 cases draws 1 to 8 characters from `**1122203456789`, so
1s, 2s, 0s and stars come often, with at most two stars, which keeps the
definition's search small.

| | property |
|---|---|
| P1 | the count is the definition's |
| P2 | a star counts as the sum over the nine digits that can take its place |
| P3 | nothing is read across a 3, so the count for s, 3, t is the count for s and 3 times the count for t |
| P4 | a 5 then a 0, put in anywhere, leaves no decoding |
| P5 | the digits 3 to 6 are alike and so are 7 to 9: turning 3 to 4, 4 to 5, 5 to 6, 6 to 3 and 7 to 8, 8 to 9, 9 to 7 changes nothing |

It prints `1000 cases (840 decodable), 4 arms, 20000 checks, 0 failures`
under `karac __mir-run` and `karac __mir-llvm-run`, and runs clean under
`karac __mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac
__mir-llvm-run`. All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: two stars spell 17 letters, not 15 | P1 25, P2 25 |
| M2 | ★: the count two back stuck at 1 | P1 349, P2 191, P3 545, P4 339 |
| M3 | table: a star then 7 read as two letters | P1 17, P2 13, P5 41 |
| M4 | table: the first two characters never read together | P1 308, P3 265 |
| M5 | states: a pending 2 closed by every star | P1 83, P2 52 |
| M6 | states: 0 a letter and 9 not | P1 416, P2 348, P4 779, P5 396 |
| M7 | backward: 1 then a star spells 11 to 18 only | P1 42, P2 56 |
| M8 | backward: a pair followed by the rest from one on | P1 345, P2 81 |
| E1 | ★: each product reduced before the sum | 0 |
| E2 | table: one entry more than needed | 0 |
| E3 | states: a star's nine factored out | 0 |
| E4 | backward: one entry fewer | 0 |

P1 kills all eight. P2 sees all but M4: putting each digit in a star's
place exercises the very rules the star must agree with, while M4's
fault, at the first two characters, hits a star and its digits alike.
P3 sees the two that misplace a count rather than a letter, M2 and
M4, which break how a count for one part multiplies with another.
P4 sees M2, whose stale count two back brings a count to life after the
dead end, and M6, which reads the 0 as a letter. P5 sees M3, which
treats 7 unlike 8 and 9 after a star, and M6, which treats 9 unlike
7 and 8. The four survivors cannot change an answer: reducing each
product before the sum gives the same residue; a table one entry longer
leaves the extra entry unread; `9 * done + 9 * one` is `9 * (done +
one)`; and the backward table reads `rest[i + 2]` only when i + 1 < n,
so its last entry is never read.

## Verification

Every arm prints the same output as `decode_ways_ii.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints its line under all three. `karac check` passes every arm, the
differential and the bench program. All at kara `d6111aa22a` for the
debug build, with the runtime archives rebuilt from that tree, and
`14acd67779` for the release build that runs `check` and `__mir-run`.

The frozen legacy backends refuse every arm and the differential at
type checking. The ★, table and backward arms hand `seed`, already a
`mut ref` parameter, on to `next_random(mut seed)` with the `mut` marker
design.md asks for, and legacy rejects that marker; the states arm and
the differential stop earlier, because legacy types the items of
`bytes().iter()` by value, so `*c` is an error. With the markers left
out, as an earlier version of this kata did, `karac run --interp`
printed the same output for the three arms and `karac run` and `karac
build` panicked in code generation (`src/codegen/assoc_call.rs:2826`, an
integer where a struct was expected). Legacy is frozen, so these are
noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It makes 20 strings of
100,000 characters, the problem's most, once: each character a star with
chance 3 in 10 and otherwise a digit from 1 to 9, turned into a 0 with
chance 1 in 100 when it follows a 1, a 2 or a star, so that no string
has a dead end. Then 600 rounds each count the decodings of one of them,
picked by the round, adding up the counts and a checksum. Every
implementation prints `20 strings of 100000 characters, 600 rounds:
total 549013858, checksum 789154533`, the Kāra program under `karac
__mir-run` included (in 87 s).

Each implementation walks the string's bytes once, keeping the counts
for the last two prefixes: Rust and Go over a `String` and `string`, C
over a fixed array of bytes, and Python over `bytes`. Spot timings on a
shared 4-core container, three runs each (two for Python; `bench.sh`
timings need a quiet machine), each including making the strings:

| | time |
|---|---|
| C (`clang -O3`) | 0.39 s |
| Rust (`rustc -O`) | 0.40 to 0.44 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.39 to 0.46 s |
| Go | 0.57 to 0.64 s |
| Python | 13.1 to 13.4 s |
| Kāra (`karac build --mir`) | 0.39 to 0.42 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, since the legacy `karac build` refuses the bench
program: handing `texts[round % 20]` to `num_decodings` moves an element
out of a `Vec` while parameters are owned, and it rejects the `mut`
markers above. That edit is by hand, on top of the
`scripts/new-bench.sh` output. A copy outside the kata that adds
`.clone()` to the argument and leaves out the markers, copying a string
of 100,000 bytes every round, builds under legacy and takes 0.40 to 0.42
s. Under `karac __mir-llvm-run` the program prints the same line in 2.3
s, compile included; that JITs the MIR's IR without optimization passes,
so it is not a benchmark.

The Kāra build runs level with C and Rust and ahead of Go: each
character costs a few compares and one division for the modulus, in
every language.

## Compiler findings

None. The legacy failures above are not filed because legacy is frozen.
