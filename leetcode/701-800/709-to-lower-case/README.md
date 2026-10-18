# 709. To Lower Case

Given a string `s`, return the string after replacing every uppercase
letter with the same lowercase letter.

```
s = "Hello"   ->  "hello"
s = "here"    ->  "here"
s = "LOVELY"  ->  "lovely"
```

**Constraints:** 1 <= `s.length` <= 100; `s` consists of printable ASCII
characters.

## Approaches

Every arm is one pass over the string, O(n): 'A' to 'Z' become 'a' to
'z', 32 code points higher, and every other character is copied as it
is.

| file | mechanism |
|---|---|
| `to_lower_case.kara` ★ | walk the characters, pushing each onto a new `String`, an uppercase letter moved up by 32 |
| `to_lower_case_bytes.kara` | copy the bytes into a `Vec[u8]`, set bit 5 (`0x20`) on each uppercase letter in place, and read them back with `String.from_utf8`; every byte stays below 128, so they are still valid UTF-8 |
| `to_lower_case_table.kara` | a table of what each of the 128 ASCII bytes becomes, built once; each byte is then one lookup, with no comparison |
| `to_lower_case_stdlib.kara` | `String.to_lowercase`, which lowers by Unicode's rules; for printable ASCII that is exactly the same mapping, and the library has no ASCII-only form |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 8 lines: the three LeetCode examples; a
one-letter string; the characters on either side of 'A' to 'Z' and 'a'
to 'z'; every printable character in order; one random string of
100 characters; and 1,000 random strings of 1 to 100 characters, with
how many changed and a checksum. `to_lower_case.py` mirrors the ★ arm
and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition.
The definition is written apart from all four arms and does no
arithmetic on characters: it looks each character up in the uppercase
alphabet, written out as a string, and replaces it with the character at
the same place in the lowercase one. 3,000 cases are checked, each two
random printable strings of 0 to 100 characters.

| | property |
|---|---|
| P1 | the string is the definition's |
| P2 | lowering the result again changes nothing |
| P3 | the result has the same length, and every character that is not an uppercase letter is where it was |
| P4 | lowering two strings joined is joining the two lowered |

It prints `3000 strings (40846 uppercase letters), 4 arms, 48000 checks,
0 failures` under `karac __mir-run` and `karac __mir-llvm-run`, and the
same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Eleven edits to the differential, two or three to each arm, each run
under `karac __mir-run`. All eleven are killed. Three more edits, E1 to
E3, change nothing that can be seen, and the differential rightly
reports no failure for them.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: 'Z' left as it is | P1 1149 |
| M2 | ★: '@' lowered too, to the backquote | P1 1087, P3 1087 |
| M3 | ★: each letter moved 31, not 32 | P1 2900 |
| M4 | bytes: '[' lowered too, to '{' | P1 1140, P3 1140 |
| M5 | bytes: bit 4 set, not bit 5 | P1 2900 |
| M6 | bytes: 'A' left as it is | P1 1114 |
| M7 | table: 25 letters mapped, 'Z' left out | P1 1149 |
| M8 | table: each mapping one byte early | P1 2902, P3 1087 |
| M9 | table: each letter mapped one too low | P1 2900 |
| M10 | stdlib: uppercase, not lowercase | P1 2954, P3 2906 |
| M11 | stdlib: the string copied unchanged | P1 2900 |
| E1 | bytes: bit 5 flipped rather than set | 0 |
| E2 | ★: the range test as c.is_ascii_uppercase() | 0 |
| E3 | table: built over all 256 bytes, not 128 | 0 |

P1 kills all eleven. P3 also kills the four that change a character that
is not an uppercase letter, M2, M4, M8 and M10. P2 and P4 kill nothing:
every mutant is still a map from one character to one character, so it
agrees with itself on a joined string, and every mutant here leaves its
own output alone, so a second pass changes nothing. E1 flips bit
5 rather than setting it, which on an uppercase letter, where it is
clear, is the same; E2 tests the range with `is_ascii_uppercase`, the
same range; E3 builds the table over all 256 bytes, of which only the
first 128 can occur.

## Verification

Every arm prints the same output as `to_lower_case.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. All with the compiler
at kara `2bfc20c2ad` for the debug build and `fe20f8fdb9` for the
release build that runs `check` and `__mir-run`; the two compiler
commits between them, `082e3de2d8` (`\xHH` escapes) and `6f256df19a` (a
generic function passed as a value), touch nothing these programs use,
and no `runtime/src` change has landed since the runtime archives were
built.

The sanitizer lane cannot see a leak (kara B-2026-10-18-31), so the leak
check ran the differential's lane executable with the preloaded shim
from kata 708, which refuses the lane's hand-made stack so that
LeakSanitizer sees `main`: it prints its line and reports no leak. The
differential calls all four arms 12,000 times each. The arms' own lane
executables finish before they can be copied out, so they were not
checked this way.

The frozen legacy backends refuse all four arms and the differential at
type checking, at `next_random(mut seed)` inside `random_string`, whose
`seed` is already a `mut ref`: legacy wants the marker dropped, where
design.md § Call-site `mut` markers now requires it on every such
argument (kara B-2026-10-14-25). They refuse the bench program at
`to_lower_case(strings[i])`, an element passed to a borrowing parameter,
which legacy reads as a move out of the `Vec`. Legacy is frozen, so this
is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages: a new string,
each character pushed onto it. C has no growable string and writes into
a buffer of the input's length, the natural C. It makes 10,000 random
printable strings of 100 characters once. Each of 50 rounds lowers every
string into a kept result, which replaces the one from the round before,
and adds one byte of it, whose place moves with the round and the
string; the last round's results are then summed in full, so no result
can go unbuilt. Every implementation prints `50 rounds of 10000 strings
of 100 characters: sum 131658517`, the Kāra program under `karac
__mir-run` included (in 76 s).

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and two of Python (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.00 to 0.01 s |
| Rust (`rustc -O`) | 0.28 to 0.33 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.28 to 0.31 s |
| Go | 0.43 to 0.51 s |
| Python | 3.4 to 3.8 s |
| Kāra (`karac build --mir`) | 0.35 to 0.38 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend; the legacy `karac build` refuses it (above). That
edit is by hand, on top of the `scripts/new-bench.sh` output. Under
`karac __mir-llvm-run` the program prints the same line in 2.3 s,
compile included; that JITs the MIR's IR without optimization passes, so
it is not a benchmark.

C is not doing less work than it says. Under valgrind's cachegrind it
runs 143 million instructions to Rust's 2,046 million and v2's
2,404 million, under 3 for each of the 50 million characters: knowing
the length up front, clang lowers each buffer 16 bytes at a time, and
with vectorizing turned off it still takes 0.03 s. Rust and Kāra decode
each character from UTF-8 and push it onto a string that grows, about
40 instructions a character; v2 runs 17% more instructions than Rust and
takes about 30% longer. The comparison with C and Rust waits until after
M4.

## Compiler findings

None new. The v2 checker accepts this program's `next_random(mut seed)`
with the marker left off as well, which design.md § Call-site `mut`
markers makes an error; that is kara B-2026-10-14-35, already open.
