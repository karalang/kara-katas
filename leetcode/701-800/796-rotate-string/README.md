# 796. Rotate String

Given two strings `s` and `goal`, return true when some number of shifts
turns `s` into `goal`. A shift moves the first letter of `s` to the end.

```
s = "abcde", goal = "cdeab"  ->  true
s = "abcde", goal = "abced"  ->  false
```

**Constraints:** both strings have 1 to 100 lowercase English letters.

## Approaches

| file | mechanism |
|---|---|
| `rotate_string.kara` ★ | every rotation of `s` is a piece of `s + s`, so `goal` is one when it is as long as `s` and `s + s` contains it; O(n²) for the library's search at worst |
| `rotate_string_shifts.kara` | try each shift `k`, comparing `goal[i]` with `s[(i + k) % n]` until a letter differs; O(n²) |
| `rotate_string_kmp.kara` | search for `goal` in `s + s` with the Knuth-Morris-Pratt failure table, so a mismatch falls back without reading `s + s` again; O(n) |
| `rotate_string_hash.kara` | hash `goal` and each window of `s + s` as numbers in base 131 modulo 10^9 + 7, moving the window a letter at a time, and compare a window letter by letter when its hash is `goal`'s, so a collision cannot give a wrong answer; O(n) expected |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 8 lines: LeetCode's two examples; one letter
against itself; a goal shorter than `s`; `abab` and `baba`, a rotation
that is also `s` read from its second letter; a string against itself;
two strings with the same letters in different numbers; and 300 random
cases, 1 to 100 letters from the first 1 to 4 of the alphabet, a third
rotations, a third rotations with one letter changed and a third any
string as long, with the rotations in all and a checksum.
`rotate_string.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition:
`s` with its first `k` letters moved to the end, for every `k`, compared
with `goal`. Its 1,600 cases come in four kinds of 400, with 1 to 3
letters: `goal` a rotation of `s`; a rotation with one letter changed;
any string as long as `s`; and `s` a piece of 1 to 4 letters written up
to six times, so that many of its rotations are the same, with `goal` a
rotation of it, changed in one letter half the time.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | `s` is a rotation of `goal` just when `goal` is one of `s` |
| P3 | turning `goal` any number of places keeps the answer |
| P4 | any rotation of `s` is one, and a `goal` one letter longer is not |

It prints `1600 cases (735 rotations), 4 arms, 25600 checks, 0 failures`
under `karac __mir-run` and `karac __mir-llvm-run`, and the same under
`karac __mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: no check that goal is as long as s | P4 511 |
| M2 | ★: goal looked for in s, not s written twice | P1 272, P3 84, P4 782 |
| M3 | ★: goal looked for only at the start | P1 272, P3 84, P4 782 |
| M4 | shifts: the last shift not tried | P1 63, P2 54, P3 55, P4 152 |
| M5 | shifts: a shift failing where the letters agree | P1 775, P4 1454 |
| M6 | shifts: a mismatch not recorded | P1 865 |
| M7 | KMP: the failure table built falling back to the start | P1 1, P2 1, P3 1, P4 1 |
| M8 | KMP: s searched once, not twice | P1 272, P3 84, P4 782 |
| M9 | KMP: a mismatch in the search falling back to the start | P1 50, P2 76, P3 73, P4 152 |
| M10 | hash: the letter coming into the window left out | P1 272, P3 84, P4 782 |
| M11 | hash: the first letter's weight one power too high | P1 272, P3 84, P4 782 |
| M12 | hash: the wrong letter taken out of the window | P1 258, P2 39, P3 102, P4 728 |

P1 and P4 kill eleven each, between them all twelve. A ★ arm that does
not check the lengths is seen by P4 alone, as a goal one letter longer
is the only case it gets wrong, and a shifts arm that never records a
mismatch, so taking the first shift every time, by P1 alone, since a
rotation of `s` is a rotation whatever it answers. P3 kills nine and P2
four, the shifts and KMP arms' wrong fall-backs and the hash arm's wrong
letter taken out among them, which go wrong for some rotations and not
for others. The KMP failure table that falls back to the start rather
than to the next shorter border is killed by a single failure in each
property: it goes wrong only when the search meets a border that has a
border of its own, which few strings of up to 30 letters give it.

## Verification

Every arm prints the same output as `rotate_string.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The debug build that
runs `__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` and the
release build that runs `check` and `__mir-run` are both at kara
`5dee7bbc7c`, whose last compiler change is `e392d00704`. The runtime
archives were built after the last runtime change, `216d20e28a`.

Since kara `3c8e763161` (B-2026-10-18-31) the sanitizer lane sees leaks
itself. The leak check also copied each arm's and the differential's
lane executable as it was linked and ran it with the preloaded shim from
kata 708, which refuses the lane's hand-made stack so that LeakSanitizer
sees `main`: all five print their output and report no leak.

The frozen legacy interpreter (`karac run --interp`) prints the same
output for all four arms unchanged. The legacy JIT (`karac run`) and
`karac build` refuse them, having no `len` or `bytes` on a `Str`
parameter; copies with the parameters written `ref String` print the
same output under the legacy interpreter, the legacy JIT, `karac build`
and an auto-par build. Legacy's checker refuses the differential, for
comparing a `String` with a `Str` and for the `chars.iter().collect()`
at the end of the inner branch, which it takes as a `Vec[char]`. A copy
with `ref String` parameters and the collect bound to a `String` first
builds, but under the legacy JIT, `karac build` and an auto-par build it
aborts on a double free before printing; the legacy interpreter runs it
and prints `1600 cases (761 rotations), 4 arms, 25600 checks, 0
failures`, as it draws different random cases. Legacy also refuses the
bench program's `len` on a `Str`; a copy with `ref String` parameters
builds and prints the same line, and the bench timing below is of it.
Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. 4,096 pairs of
100-letter strings, LeetCode's longest, over the first 1 to 4 letters of
the alphabet are made once: a third with `goal` a rotation of `s`, a
third a rotation with one letter changed, and a third any string of the
same letters. Each of 1,500,000 rounds asks whether the next `goal` is a
rotation of its `s`, building `s + s` and searching it with the
language's own substring search (`strstr` in C, `str::contains` in Rust,
`strings.Contains` in Go, `in` in Python). Every implementation prints
`1500000 pairs: 745273 rotations, checksum 652750545`, the Kāra program
under `karac __mir-run` included (in 9.0 s).

The bench measures one small allocation and one substring search a
round, so it is a bench of each library's search on short, repetitive
strings. Spot timings on a shared 4-core container, eight runs of each
compiled program, five of them interleaved, and two of Python
(`bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.19 to 0.25 s |
| Rust (`rustc -O`) | 2.15 to 2.51 s |
| Rust (`rustc -O -C overflow-checks=on`) | 2.18 to 2.41 s |
| Go | 0.66 to 0.75 s |
| Python | 1.74 to 1.99 s |
| Kāra (`karac build --mir`) | 1.99 to 2.15 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, since the legacy `karac build` refuses it (see
Verification); that edit is by hand, on top of the
`scripts/new-bench.sh` output. Under `karac __mir-llvm-run` the program
prints the same line in 6.0 s, compile included; that JITs the MIR's IR
without optimization passes, so it is not a benchmark.

At the medians of the interleaved runs the v2 build takes 2.03 s,
against C's 0.20, Rust's 2.23 (2.27 under overflow checks) and Go's
0.70. v2's `String.contains` is Rust's `str::contains`, and the two run
alike: under valgrind's cachegrind v2 runs 7.86 billion instructions
with 155 million branches mispredicted, Rust 10.0 billion with 158
million, and C 1.94 billion with 33.5 million. The two-way search Rust
uses is linear at worst, but on a 100-letter needle in a 200-letter
haystack over a few letters its setup and its branches cost more than
they save. The legacy build of the copy, whose `contains` tries each
start with `memcmp`, ran 0.41 to 0.51 s, a median of 0.44 s in the
interleaved runs, with 3.00 billion instructions and 2.65 million
mispredicts, so v2 takes 4.6 times legacy; that is filed as
B-2026-10-19-26. The comparison with C and Rust waits until after M4.

## Compiler findings

- **B-2026-10-19-25.** On the MIR backends a bare `collect()` at the
  end of one branch of an un-annotated `let goal = if .. { .. } else {
  .. }` does not lower when its target type comes only from the other
  branch; `karac check` passes it. The differential's `goal` binding is
  written `let goal: String` until it is fixed, with a comment citing
  the row.
- **B-2026-10-19-26.** `String.contains` on the v2 compiled backend is
  Rust's `str::contains`, whose two-way search sets itself up on every
  call; on the bench's 100-letter needles in 200-letter haystacks that
  makes the bench 4.6 times the legacy build, which scans with `memcmp`
  at each start. See Benchmarks.
