# 459. Repeated Substring Pattern

Given a string `s`, check if it can be constructed by taking a
substring of it and appending multiple copies of the substring
together.

```
s = "abab"          ->  true    ("ab" twice)
s = "aba"           ->  false
s = "abcabcabcabc"  ->  true    ("abc" four times, or "abcabc" twice)
```

**Constraints:** `1 <= s.length <= 10^4`; `s` consists of lowercase
English letters.

## Approaches

Every arm is `fn repeated_substring_pattern(s: String) -> bool`.

| file | mechanism |
|---|---|
| `repeated_substring.kara` ★ | for each proper divisor `d` of the length, check that every letter equals the one `d` before it. O(n · number of divisors) |
| `repeated_substring_doubled.kara` | `s` is a repeated unit exactly when it equals one of its proper rotations, and those are the windows of `s + s` without its first and last letters; look for `s` there with `contains` |
| `repeated_substring_prefix.kara` | the prefix function (KMP's failure table): with `p` the longest proper border of `s`, `n - p` is its shortest period, which must divide `n`. O(n) |
| `repeated_substring_rotate.kara` | for each proper divisor `d`, compare the slices `s[d..]` and `s[..n - d]` whole. O(n · number of divisors) |
| `differential.kara` | the four arms on 1,500 random cases, five properties |

Every arm prints the same 11 lines: the three LeetCode examples, one
letter, two equal letters, two different letters, a string with a
border but no period that divides it (`aabaaba`), a unit that is a
string with a border of its own (`abaab` twice), a near miss in the
last letter, 29 `z`s and a `y`, and for 300 random strings (half a unit
of 1 to 10 letters written 1 to 20 times, a third of those with one
letter changed, and half random strings of 1 to 200 letters, over 1,
2, 3 or 26 letters) how many repeat a substring and a checksum.
`repeated_substring.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and runs them on
1,500 random cases.

| | property |
|---|---|
| P1 | on 1 to 8 letters over 1 or 2 letters, the answer is brute force's: for each unit length that divides `n`, write the first that many letters `n / d` times with `repeat` and compare |
| P2 | a unit of 1 to 30 letters written 2 to 5 times gives `true` |
| P3 | rotating a string keeps the answer |
| P4 | reversing a string keeps the answer |
| P5 | a string ending in a letter found nowhere else in it gives `false` |

It prints `1500 cases, 4 arms, 30000 checks, 0 failures` under
`karac __mir-run`, and a count for each property when anything fails.

## Mutation testing

Eight edits to `differential.kara`, two to each arm, each run under
`karac __mir-run`. All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a unit of half the string is not tried | P1 291, P2 274 |
| M2 | ★: a unit length need not divide `n` | P1 16, P3 4 |
| M3 | doubled: only the rotation by one letter is tried | P1 23, P2 1051 |
| M4 | doubled: the last letter is not matched | P1 727, P5 1500 |
| M5 | prefix: any border counts | P1 282, P3 202 |
| M6 | prefix: a mismatch falls back to nothing | P1 1, P2 138, P3 75, P4 71 |
| M7 | rotate: only the second copy is compared | P1 254, P3 222, P4 210, P5 736 |
| M8 | rotate: a unit of one letter is not tried | P1 460, P2 31 |

P1, the only property with an independent answer, sees all eight. M2
is the faintest: it errs only on a string with a period that does not
divide its length and no period that does, and those are rare among
random strings. M6 is nearly invisible to P1, whose strings of up to 8
letters rarely need the prefix function's fallback, but P2 to P4 use
units of up to 30 letters, where it is needed. P5 sees only the
mutants that answer `true` too readily.

## Verification

All four arms print the same output as `repeated_substring.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`.
The differential prints `30000 checks, 0 failures` on both. The four
arms and the differential also run clean under `karac __mir-llvm-asan`
(AddressSanitizer and LeakSanitizer): output identical, no error, no
leak.

`karac check` passes the differential but refuses the four arms, on the
harness's `s = cs.iter().collect();`, which changes one letter of a
random string: check does not take `collect`'s target type from an
assignment (B-2026-10-12-33, below). The arms keep that line.

On the frozen legacy backends every arm stops on the same line, which
the legacy front end shares with check. The differential fails
legacy's ownership check, which moves `s` into a call that v2 borrows.
Legacy `karac build` also rejects the bench program (see Benchmarks).
Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It builds 10 strings of 100,000
letters once, each a random unit written over and over (units of 1, 5,
32, 100, 625, 1,000, 3,125, 5,000, 20,000 and 50,000 letters). Each of
40 rounds, for every string, changes one letter in its second half half
the time, checks the string, and puts it back. A check of an untouched
string stops at the unit's length; one of a changed string tries every
divisor that is a multiple of the unit, each up to the changed letter.
Every implementation prints `40 rounds on 10 strings of 100000: 204
repeat a substring, checksum 949457219`, the Kāra program under
`karac __mir-run` included (in 97 s).

The legacy `karac build` rejects the bench program (its front end
refuses `all[a] = cs.iter().collect();`, B-2026-10-12-33), so `bench.sh`
builds the Kāra program with `karac build --mir`, the v2 compiled
backend. That edit is by hand, on top of the `scripts/new-bench.sh`
output.

The mirrors keep the ★ arm's structure: the check copies the letters
into an array of chars, and the punch keeps a copy of the string,
rebuilds it from its chars with one letter changed, and restores the
copy. The C mirror changes the letter in place. Spot timings on a
shared 4-core container, three runs each (two for Python; `bench.sh`
timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.09 to 0.12 s |
| Rust (`rustc -O`) | 0.15 to 0.17 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.18 to 0.19 s |
| Go | 0.41 to 0.53 s |
| Python | 5.9 to 6.2 s |
| Kāra (`karac build --mir`) | 0.60 to 0.63 s |

Kāra spends its time about evenly on the punch (0.23 s without the
check) and the check (0.29 s without the punch), and in both most of
it is `chars().collect()`: on the v2 compiled backend every `push` is a
call into the runtime that copies the element with `memcpy`, and every
char is decoded by another call (B-2026-10-12-36, below). Under
`karac __mir-llvm-run` the program prints the same line in 6.3 s,
compile included; that JITs the MIR's IR without optimization passes,
so it is not a benchmark.

## Compiler findings

- **B-2026-10-12-33** (`karac check`, open): `s = cs.iter().collect();`
  into an existing `String` is refused with "expected 'String', found
  'Vec[char]'", as are `w.name = ...` and `v.push(cs.iter().collect())`;
  check takes `collect`'s target from a `let` annotation or a return
  type only. The MIR backends run the assignment. Every arm's harness
  and the bench keep the assignment; `let t: String =
  cs.iter().collect(); s = t;` would pass.
- **B-2026-10-12-34** (MIR, open): `v.push(cs.iter().collect())` with
  `v: Vec[String]` fails to build on the MIR backends ("the method call
  `.collect` with no resolved callee is not lowered yet"). Found while
  measuring B-2026-10-12-33; the kata does not use the form.
- **B-2026-10-12-35** (library spec, fixed in kara `a9bce361cd`):
  `s.chars().rev()` was refused on the MIR backends, whose `chars()`
  followed the spec in not being double-ended, while `karac check`
  accepted it. `chars()` is now double-ended in the spec and on both
  MIR backends, and the differential's P4 is back to
  `let reversed: String = s.chars().rev().collect();` (it reversed a
  `Vec[char]` until then).
- **B-2026-10-12-36** (MIR compiled backend, open, performance):
  `Vec.push` is an out-of-line runtime call with a `memcpy` per element.
  A loop pushing 1,000,000 numbers 40 times takes 0.19 s under
  `karac build --mir`, 0.04 s for Rust; `s.chars().collect()` of
  1,000,000 letters 40 times takes 0.28 s against Rust's 0.05 s. The
  output is correct; only the time is off.
