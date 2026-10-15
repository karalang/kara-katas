# 680. Valid Palindrome II

Given a string `s`, return whether it can be made a palindrome by
deleting at most one character from it.

```
"aba"   ->  true
"abca"  ->  true    (delete the "c")
"abc"   ->  false
```

**Constraints:** 1 <= `s.length` <= 10^5; `s` holds lowercase English
letters.

## Approaches

Every arm is `fn valid_palindrome(s: String) -> bool`, reading the
string's bytes.

| file | mechanism |
|---|---|
| `valid_palindrome_ii.kara` ★ | walk inward from both ends; at the first pair that differs, the string is valid exactly when the run between them reads the same with its left end or its right end left out |
| `valid_palindrome_ii_budget.kara` | the same walk for any number of deletions: at a mismatch, spend one on either end and recurse, failing when the budget is spent; here the budget is 1 |
| `valid_palindrome_ii_banded.kara` | the insertions and deletions turning the string into its reverse number twice what its longest palindromic subsequence is short of n, so the string is valid when that distance is at most 2; a table of the five cells nearest the diagonal |
| `valid_palindrome_ii_hashes.kara` | polynomial hashes of the prefixes of the string and of its reverse give, for each position left out, the hash of the rest and of the rest reversed; a match is checked byte by byte |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 17 lines: the three LeetCode examples; ten
corners, among them `"eeccccbebaeeabebccceea"`, whose first mismatch can
be fixed on neither side, and a 100-letter LeetCode test; how many of
the 29,523 strings over `abc` of length 1 to 9 are valid, by length; six
palindromes of 100,000 letters over 2 and 26 letters with none, one or
two letters inserted; and 3,000 random strings, half of them near
palindromes, with a checksum and whether each answers the same reversed.
`valid_palindrome_ii.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition.
The definition is written apart from all four arms: the string, or the
string with one of its characters removed, equals its own reverse, built
as a new `String` for every position. 2,000 strings of 1 to 30 letters
over one to three letters are checked against it, half of them random
and half palindromes with up to two letters inserted, since a random
string is rarely valid.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | the reversed string answers the same |
| P3 | a palindrome with one letter inserted anywhere is valid |
| P4 | the same letter added at both ends changes nothing |

It prints `2000 strings (1355 valid by the definition), 4 arms,
32000 checks, 0 failures` under `karac __mir-run` and `karac
__mir-llvm-run`, and runs clean under `karac __mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac __mir-run`.
All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: only the left end left out at a mismatch | P1 125, P2 276, P3 692 |
| M2 | ★: the last pair of a run never compared | P1 43 |
| M3 | budget: two deletions allowed | P1 226 |
| M4 | budget: one deletion spent on both ends | P1 130, P2 171, P3 359 |
| M5 | banded: a distance of 2 refused | P1 337, P3 1625 |
| M6 | banded: the string compared with itself, not its reverse | P1 645 |
| M7 | hashes: the last position never left out | P1 29, P2 65, P3 126, P4 29 |
| M8 | hashes: the check skips the left out position on the left only | P1 125, P2 276, P3 692 |
| E1 | ★: the innermost pair of the first walk never compared | 0 |
| E2 | budget: the right branch given a budget of 0, not budget - 1 | 0 |
| E3 | banded: cells capped at 4, not 3 | 0 |
| E4 | hashes: base 137, not 131 | 0 |

P1 kills all eight. P2 and P3 see the four that lose a deletion on one
side, M1, M4, M7 and M8, since the reversed string or a letter inserted
on that side needs it; P3 also sees M5, which refuses every deletion.
P4 sees only M7: a letter added at both ends moves the last position.
M2, M3 and M6 accept strings they should refuse, which none of P2 to
P4 can see, since each of those expects a valid answer or the same
answer twice. M1 and M8 fail exactly the same checks, which suggests the
hash arm's check that skips a position only on the left accepts the same
deletions as trying only the left end; that is inferred from the counts,
not shown. The four survivors change no answer. When the walk's last two
bytes are next to each other, leaving out either makes the rest a
palindrome, so never comparing them is harmless. The budget is 1, so
`budget - 1` is 0. The table only has to tell a distance of 2 from more,
so any cap above 2 works. And every hash match is checked byte by byte,
so the base changes only which candidates get checked.

## Verification

Every arm prints the same output as `valid_palindrome_ii.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and runs clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints its line under all three. `karac check` passes all four arms, the
differential and the bench program. All with the compiler at kara
`5e4d49c205` for both the debug build and the release build that runs
`check` and `__mir-run`, with runtime archives newer than the last
`runtime/src` change.

The frozen legacy backends refuse every arm at type checking, at
`cs.push(*c)` in the harness, since legacy gives the items of
`half.iter()` by value where v2 gives references. The legacy `karac
build` refuses the differential in codegen, where `Iterator.rev()` is
not supported for `s.chars().rev().collect()`. Legacy is frozen, so this
is noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It builds 300 strings of about
20,000 letters once, each a palindrome over 2, 3 or 26 letters with
none, one or two letters inserted at random places, then checks every
one of them in 100 rounds, in an order that changes each round, counting
the valid ones and putting each answer into a checksum. Every
implementation prints `30000 strings checked: 20200 valid, checksum
14079126`, the Kāra program under `karac __mir-run` included (in 221 s).

Each implementation is the same two-pointer walk over bytes, on strings
built once at the start. Spot timings on a shared 4-core container, six
runs each, three of them interleaved (two for Python; `bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.16 to 0.28 s |
| Rust (`rustc -O`) | 0.22 to 0.35 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.22 to 0.36 s |
| Go | 0.24 to 0.32 s |
| Python | 17.3 to 17.8 s |
| Kāra (`karac build --mir`) | 0.23 to 0.36 s |
| Kāra, legacy (`karac build`, a copy) | 0.45 to 0.60 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend, since the legacy `karac build` refuses the bench
program at type checking: `valid_palindrome(strings[at])` moves an
element out of `strings` under legacy, where a bare parameter is owned,
but v2 borrows it. That edit is by hand, on top of the
`scripts/new-bench.sh` output. A copy outside the kata whose parameter
is `ref String` builds under legacy, and its row is above. Under `karac
__mir-llvm-run` the program prints the same line in 2.6 s, compile
included; that JITs the MIR's IR without optimization passes, so it is
not a benchmark.

So the v2 build is level with C, Rust and Go here, and about twice as
fast as legacy. Every compiled row runs the same byte loop, which seems
to set the time; that is inferred from the rows being level, not
profiled. Why legacy is slower was not looked into, since legacy is
frozen. The comparison with C and Rust waits until after M4.

## Compiler findings

None new. All four arms, the differential and the bench program pass
`karac check` and run the same on both v2 backends. The bench program
binds `cs.iter().collect()` to a `let` with a `String` annotation before
pushing it, because `strings.push(cs.iter().collect())` is refused with
"expected 'String', found 'Vec[char]'": that is B-2026-10-12-33, open.
