# 471. Encode String with Shortest Length

Given a string `s`, encode the string such that its encoded length is
the shortest.

The encoding rule is: `k[encoded_string]`, where the `encoded_string`
inside the square brackets is being repeated exactly `k` times. `k`
should be a positive integer.

If an encoding process does not make the string shorter, then do not
encode it. If there are several solutions, return any of them.

```
s = "aaa"         ->  "aaa"
s = "aaaaa"       ->  "5[a]"
s = "aaaaaaaaaa"  ->  "10[a]"    ("a9[a]" and "9[a]a" are as short)
```

**Constraints:** `1 <= s.length <= 150`; `s` consists of only lowercase
English letters.

## Approaches

Every arm is `fn encode(s: String) -> String`, and borrows the string.
All four rest on one recurrence: a shortest encoding of a string `t` is
`t` itself, shortest encodings of the two sides of some cut put side by
side, or `k[e]` where `t` is `k` copies of a unit and `e` is a shortest
encoding of the unit. A choice replaces the one before it only when it
is strictly shorter, so nothing is encoded unless that makes it
shorter, at any depth.

| file | mechanism |
|---|---|
| `encode_string.kara` ★ | bottom up by length, keeping the encodings themselves; the shortest unit of `t` is where `t` first appears in `t + t` after position 0 (`find`), and the shortest unit is enough, since every unit is copies of it. O(n³) |
| `encode_string_memo.kara` | top down, each piece worked out when first asked for and kept in a `Map` keyed by its start and end; every unit length that divides the length and leaves the piece equal to itself shifted by it is tried, compared as slices. O(n³) |
| `encode_string_lengths.kara` | lengths first: a table of shortest lengths and of how each is made (the letters, a cut, or a unit), units checked letter by letter, filled from the last start back; then the one encoding is written out by following the choices down. O(n³) |
| `encode_string_kmp.kara` | shortest units from the prefix function: for each start, KMP's failure table of the rest of the string gives each piece's longest border `b`, and `len - b` is a unit when it divides `len`; the encodings are kept in one flat table. O(n³) |
| `differential.kara` | the four arms on 1,500 random strings, five properties |

The arms may return different encodings of the same length (for 10
`a`s, `10[a]` or `a9[a]`), so the harness prints what every correct
arm agrees on. Every arm prints the same 15 lines: for the three
LeetCode examples, two more from the problem's first version
(`aabcaabcd` and `abbbabbbcabbbabbbc`, which nest), one letter, four
`a`s (no shorter), `ababab`, six different letters, 38 `a`s and a `b`,
150 `a`s, `abc` 50 times, 25 different letters 6 times, and `ab` 74
times then `a` (whose unit starts at the second letter), the length of
the encoding, whether it decodes back to the string, and whether it is
the string unchanged; then, for 300 random strings over 1, 2 or 3
letters (pieces of letters and nested copies, cut to 1 to 60 letters),
the total length, how many are left unchanged, whether all decode back,
and a checksum of the lengths in order. `encode_string.py` mirrors the
★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and runs them on
1,500 random strings over 1 to 3 letters, built as in the harness: a
third cut to up to 24 letters, a third to up to 8, and a third to up to
8 and then followed by a run of 8 to 12 `a`s and up to 8 more letters,
where a count goes from one digit to two.

| | property |
|---|---|
| P1 | the encoding decodes back to the string, and is the string itself unless it is shorter |
| P2 | its length is the reference's: the recurrence written straight from the grammar, with units checked by `repeat` and lengths remembered by the string itself |
| P3 | up to 4 letters of the string, written `k` times (2 to 12), encode no longer than `k[e]` for the arm's encoding `e` of those letters |
| P4 | the string encodes no longer than its two sides of a cut, each encoded |
| P5 | renaming the letters by a turn of the alphabet, and reversing the string, keep the length |

It prints `1500 cases, 4 arms, 30000 checks, 0 failures` under
`karac __mir-run`, and a count for each property when anything fails.
The reversal is made by reversing a `Vec[char]`, because
`s.chars().rev()` is refused on the MIR backends (B-2026-10-12-35);
switch to it once that is fixed.

## Mutation testing

Eight edits to `differential.kara`, two to each arm, each run under
`karac __mir-run`. All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a unit is used when it is no shorter | P1 45 |
| M2 | ★: the last cut is not tried | P2 49, P4 4, P5 123 |
| M3 | memo: a unit length need not divide the length | P1 203, P2 161, P5 43 |
| M4 | memo: no cut after the first letter | P2 87, P4 10, P5 123 |
| M5 | lengths: a unit is checked against its second copy only | P1 480, P2 477, P5 343 |
| M6 | lengths: every count costs one digit in the length table | P2 2, P5 2 |
| M7 | kmp: a mismatch falls back to nothing | P2 3, P3 47, P5 4 |
| M8 | kmp: the shortest period counts as a unit even when it does not divide the length | P1 203, P2 161, P5 43 |

M1 changes no length, so only P1's rule that a string no encoding can
shorten comes back unchanged sees it (`aaaa` becomes `4[a]`). M3 and M8
are the same mistake in two arms and fail the same cases. M7 is nearly
invisible on the case strings, where borders are short and the
fallback is rarely needed; P3's strings of 2 to 12 copies are where it
shows.

M6 is the faint one, and it survived the first version of the
differential, whose strings were all random pieces of up to 24
letters. Its table thinks a count of 10 or more costs one letter less
than it does, which changes the answer only where an encoding with
such a count ties, in the table's eyes, with a shorter one without it:
`cacacaaaaaaaaaacbbbbb` is `3[ca]9[a]c5[b]` (15 letters), and the
mutant's `cacac10[a]c5[b]` is 16. Random pieces almost never make one.
Measured on strings of 150 letters built as in the bench, it changes
the length of 4 of 400; on random strings of up to 60 letters, about
one in 1,400. The third kind of case, with a run of 8 to 12 `a`s where
a count goes from one digit to two, was added for it, and now kills it
on 2 strings in P2 and the same 2 in P5. A first M6, which cut the
right side of a cut one letter late, was killed only by a panic (an
index out of bounds) and was replaced.

## Verification

All four arms print the same output as `encode_string.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and `karac check` passes on every file, the bench program included. The
differential prints `30000 checks, 0 failures` on both. The four arms
and the differential also run clean under `karac __mir-llvm-asan`
(AddressSanitizer and LeakSanitizer): output identical, no error, no
leak.

Nothing here runs on the frozen legacy backends. `karac run --interp`
has no `String.as_str` or `String.find`, and LLJIT stops on `as_str` in
its code generator. Legacy `karac build` reads a bare parameter as
owned, so it rejects passing the same string or `Vec` to two calls
(`value 'cs' moved here, used again here`); on the differential it
rejects `*known` on what `Map.get` returns, and on the bench program
the move of `strings[i]` out of its index. Legacy is frozen, so this
is noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It builds 400 strings of 150 letters
(the problem's largest) over 2 or 3 letters once, from random pieces
and nested copies as in the harness, and encodes each. Every
implementation prints `400 strings of 150 letters: 11008 letters
encoded, checksum 978521168`, the Kāra program under `karac __mir-run`
included (in 230 s).

The legacy `karac build` rejects the bench program (it moves
`strings[i]` out of the index, where v2 borrows it), so `bench.sh`
builds the Kāra program with `karac build --mir`, the v2 compiled
backend. That edit is by hand, on top of the `scripts/new-bench.sh`
output.

Every mirror keeps each piece's encoding as its own string, finds the
shortest unit by searching `t + t` from its second letter with the
language's own substring search (`strstr` in C), and builds a new
string only when a choice is strictly shorter. Spot timings on a
shared 4-core container, three runs each (two for Python; `bench.sh`
timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.70 to 0.90 s |
| Rust (`rustc -O`) | 2.85 to 3.34 s |
| Rust (`rustc -O -C overflow-checks=on`) | 2.80 to 3.15 s |
| Go | 1.79 to 2.06 s |
| Python | 21.1 to 21.3 s |
| Kāra (`karac build --mir`) | 3.78 to 4.16 s |

The `--mir` row is timed at kara `a47100457f`. Most of the time goes
to the 4.5 million substring searches and the strings built for them,
so the spread is likely the libraries' searches and allocators rather
than the DP. Under `karac __mir-llvm-run` the program prints the same
line in 14 s, compile included; that JITs the MIR's IR without
optimization passes, so it is not a benchmark.

## Compiler findings

No new findings. The differential works around B-2026-10-12-35 (see
above).
