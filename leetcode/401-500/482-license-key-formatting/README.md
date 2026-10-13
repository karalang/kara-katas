# 482. License Key Formatting

You are given a license key represented as a string `s` that consists
of only alphanumeric characters and dashes. The string is separated
into `n + 1` groups by `n` dashes. You are also given an integer `k`.

We want to reformat the string `s` such that each group contains
exactly `k` characters, except for the first group, which could be
shorter than `k` but still must contain at least one character.
Furthermore, there must be a dash inserted between two groups, and you
should convert all lowercase letters to uppercase.

Return the reformatted license key.

```
s = "5F3Z-2e-9-w", k = 4  ->  "5F3Z-2E9W"
s = "2-5g-3-J",    k = 2  ->  "2-5G-3J"
```

**Constraints:** `1 <= s.length <= 10^5`; `s` consists of English
letters, digits and dashes; `1 <= k <= 10^4`.

## Approaches

Every arm is `fn license_key_formatting(s: String, k: i64) -> String`,
and borrows the string. The groups are fixed from the end: the last `k`
characters kept are one group, the `k` before them another, and the
first group holds what is left.

| file | mechanism |
|---|---|
| `license_key_formatting.kara` ★ | back to front over `s.chars().rev()`: dashes skipped, every character uppercased with `to_ascii_uppercase`, a dash put in before each `k`-th one after the first, and the `Vec[char]` reversed at the end |
| `license_key_formatting_front.kara` | front to back, after counting the characters that are not dashes: the first group holds that count modulo `k`, or `k` when it is 0, and a dash goes in each time a group is full |
| `license_key_formatting_pieces.kara` | whole-string operations: `replace("-", "")`, `to_uppercase()`, then slices `clean[start..end]` for the first group and the `k`-long ones after it, joined with `join("-")` |
| `license_key_formatting_collect.kara` | one iterator chain (`filter`, `map`, `collect`) into a `Vec[char]`; a dash goes before position `i` exactly when `i > 0` and the characters from `i` to the end, `n - i`, are a multiple of `k` |
| `differential.kara` | the four arms on 1,500 random strings, four properties |

Every arm prints the same 10 lines: the two LeetCode examples, a string
of dashes only (the key is empty), one character, `k` longer than the
string, `k = 1`, dashes at both ends and doubled, a first group of one,
a string in both cases, and for 300 random strings (1 to 40 characters,
a dash one time in four, otherwise a letter of either case or a digit,
with `k` from 1 to 8) the number of characters and dashes in the keys
and a checksum of them. `license_key_formatting.py` mirrors the ★ arm
and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and runs them on
1,500 random strings of 0 to 30 characters (a dash one time in three)
with `k` from 1 to 7.

| | property |
|---|---|
| P1 | the key passes the definition: without its dashes it is the string's characters without dashes, uppercased, and its groups are `k` long except the first, which holds 1 to `k`. Only one string passes, so this is a full oracle |
| P2 | one more dash in the string, at a random place, gives the same key |
| P3 | the string with its letters' case swapped gives the same key |
| P4 | `k` more characters at the end give them, uppercased, as one more group at the end of the key |

It prints `1500 cases, 4 arms, 24000 checks, 0 failures` under
`karac __mir-run`, in 1.9 s, and a count for each property when
anything fails.

A first draft of P4 put the `k` characters in front and expected one
more group in front of the key. That is wrong, not the arms: groups are
counted from the end, so characters added in front join the first
group and only split off when it overflows. All four arms failed it
alike, which is what gave the harness away.

## Mutation testing

Eight edits to `differential.kara`, two to each arm, each run under
`karac __mir-run`. All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a group after a dash restarts its count at 1, not 0 | P1 930, P4 1227 |
| M2 | ★: the characters are not uppercased | P1 1326, P3 1404, P4 1500 |
| M3 | front: the dashes are counted too | P1 782, P2 1079, P4 879 |
| M4 | front: a first group of 0 is not made `k` | P1 521, P4 72 |
| M5 | pieces: the groups are cut from the front | the run stops: a slice past the end |
| M6 | pieces: the last piece is left out | P1 1428, P4 1473 |
| M7 | collect: a dash may go before the first character | P1 521, P4 72 |
| M8 | collect: the dashes are kept | P1 1355, P2 1500 |

M4 and M7 are the same fault reached two ways, a leading dash when the
character count is a multiple of `k`, and fail exactly the same checks.
P3 sees only M2, the one mutant that touches case; P2 sees only the two
that let a dash count (M3, M8). M5's last slice runs past the end of
the string and the run stops there; on both MIR backends the report is
`runtime error: explicit panic`, which is B-2026-10-13-13 below.

## Verification

All four arms print the same output as `license_key_formatting.py`
under `karac __mir-run` (the v2 MIR interpreter) and
`karac __mir-llvm-run`, and `karac check` passes on every file, the
bench program included. The differential prints `24000 checks, 0
failures` on both. The four arms and the differential also run clean
under `karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer):
output identical, no error, no leak.

On the frozen legacy backends, `karac run --interp` prints the same
output on every arm, and LLJIT, legacy `karac build` and a
`KARAC_AUTO_PAR=1` build agree on the front, pieces and collect arms.
They refuse the ★ arm and its bench program: "`Iterator.rev()` is not
yet supported under `karac build`/`karac run` (codegen) for this chain
shape", on `s.chars().rev()`, as on kata 479. The differential stops
on the legacy interpreter at `back.as_str()` ("method 'as_str' not
found on type 'String'"), and legacy `karac build` refuses it ("value
's' moved here, used again here"), since it reads the string after
lending it to an arm. Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It builds one string of 100,000
characters (the problem's most; a dash one time in four) once, then
formats it for every `k` from 1 to 500. Every implementation prints `k
= 1 to 500 on 100000 characters: keys add up to 37980327 characters,
checksum 570959870`, the Kāra program under `karac __mir-run` included
(in 107 s).

Every mirror walks the string back to front into a growable buffer of
characters and reverses it: Rust `chars().rev()` into a `Vec<char>`, Go
a `[]rune` (the string converted to runes first, as Kāra and Rust
decode UTF-8), Python a list and `"".join`, and C a byte buffer. Python
uppercases with `str.upper()`, which is Unicode, where the others use
the ASCII mapping; on this alphabet the two agree. Spot timings on a
shared 4-core container, three runs each (two for Python; `bench.sh`
timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.18 to 0.19 s |
| Rust (`rustc -O`) | 0.25 to 0.27 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.27 to 0.30 s |
| Go | 0.74 to 0.83 s |
| Python | 3.6 s |
| Kāra (`karac build --mir`) | 0.68 to 0.73 s |

The legacy `karac build` refuses this program (see Verification), so
`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend. That edit is by hand, on top of the
`scripts/new-bench.sh` output. The `--mir` row is timed at kara
`b0b1557b39`. Under `karac __mir-llvm-run` the program prints the same
line in 8.2 s, compile included; that JITs the MIR's IR without
optimization passes, so it is not a benchmark.

## Compiler findings

- **B-2026-10-13-12** (open): `char.is_ascii_lowercase()`,
  `is_ascii_uppercase()` and `is_ascii_alphanumeric()` are refused by
  `karac check`, the legacy interpreter and both MIR backends ("no
  method 'is_ascii_lowercase' on type 'char'"), while
  `is_ascii_digit`, `is_ascii_alphabetic`, `is_lowercase` and
  `to_ascii_uppercase` are accepted. The differential's case swap was
  first written `if c.is_ascii_lowercase() { .. }`; it writes
  `c.is_lowercase()`, the same test on its ASCII alphabet.
- **B-2026-10-13-13** (open): on both MIR backends a string slice that
  runs past the end, or cuts a code point, stops with `runtime error:
  explicit panic`, the report a `panic(..)` call gets, where legacy
  names the bounds. Met in mutant M5; the arms never slice out of
  range.
