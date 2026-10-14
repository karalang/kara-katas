# 567. Permutation in String

Given two strings `s1` and `s2`, return `true` if `s2` contains a
permutation of `s1`, or `false` otherwise. In other words, return `true`
if one of `s1`'s permutations is the substring of `s2`.

```
s1 = "ab", s2 = "eidbaooo"  ->  true   ("ba" is a permutation of "ab")
s1 = "ab", s2 = "eidboaoo"  ->  false
```

**Constraints:** `1 <= s1.length, s2.length <= 10^4`; `s1` and
`s2` consist of lowercase English letters.

## Approaches

Every arm is `fn check_inclusion(s1: String, s2: String) -> bool`.

| file | mechanism |
|---|---|
| `check_inclusion.kara` ★ | a window as long as s1 slides along s2, keeping for each letter how many more s1 needs than the window has, and `missing`, the sum of the positive ones; each step changes two counts, and the window matches when `missing` is 0; O(\|s1\| + \|s2\|) |
| `check_inclusion_compare.kara` | the window's 26 letter counts kept in a `Vec` and compared with s1's, `window == want`, at every step |
| `check_inclusion_map.kara` | one `Map[char, i64]` of the window's counts less s1's, a letter removed when its count comes back to 0; the window matches when the map is empty |
| `check_inclusion_shrink.kara` | over `bytes()`: the window grows by one letter on the right and gives up letters on the left until no letter is over s1's count; it matches when it is as long as s1 |
| `differential.kara` | the four arms against the definition, five properties |

Every arm prints the same 14 lines: eleven pairs at the edges (the two
examples, s1 longer than s2, a match after a false start, one letter
there and not, repeated letters whose counts must match, and matches at
the very start and the very end of s2), a count and checksum over
300 random pairs over `a`, `b` and `c`, and the problem's largest, s1 of
5,000 random letters and s2 of 10,000 that ends in s1 reversed, then the
same with its last letter changed to the one s1 has fewest of.
`check_inclusion.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
the statement read literally: for every place in s2, the letters from
there as long as s1, each one struck out of a copy of s1 in turn; a
place where every letter finds one to strike is a match. Each arm is
held to the properties below on 1,000 random pairs, s1 of 1 to 5 letters
and s2 of 1 to 25, over the first 2 to 4 letters of the alphabet.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | false when s1 is longer than s2; true when s2 contains s1 itself |
| P3 | renaming the letters the same way in both strings changes nothing |
| P4 | reversing both strings changes nothing |
| P5 | s1's letters shuffled and put into s2 at a random place are found |

It prints `1000 cases, 4 arms, 20000 checks, 0 failures` under `karac
__mir-run` and `karac __mir-llvm-run`, and runs clean under `karac
__mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac
__mir-llvm-run`. All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a letter leaving never counted missing again | P1 190 |
| M2 | ★: a letter not needed counted as found | P1 274, P4 4 |
| M3 | compare: the window never gives letters up | P1 415, P2 286, P4 243, P5 684 |
| M4 | compare: the window one letter too long | P1 415, P2 286, P4 243, P5 684 |
| M5 | map: a count back at 0 kept | P1 606, P2 444, P5 1000 |
| M6 | map: the leaving letter added, not taken away | P1 415, P2 286, P4 243, P5 684 |
| M7 | shrink: one letter given up at most | P1 203, P4 4 |
| M8 | shrink: a window one letter short accepted | P1 206, P2 17 |
| E1 | ★: the match tested with `<= 0` | 0 |
| E2 | compare: the counts compared the other way round | 0 |
| E3 | map: emptiness tested by length | 0 |
| E4 | shrink: the window's length written another way | 0 |

M3, M4 and M6 fail identically, since each can match only the first
window: M3's and M6's windows never lose a letter, so after s1's length
they hold too many, and M4's is one letter too long from then on. Each
answers true only when s2's first letters are a permutation of s1, so
P5 fails whenever the shuffle is put in later. M5 never empties its map
once a letter has come and gone, so it answers false on every case where
the answer is true, and P5 fails on all 1,000. M1 and M2 let `missing`
fall faster than it should, so the ★ arm answers true on some windows
that do not match; only P1 sees M1, and only P1 and, four times, P4 see
M2. P3 sees none of the mutants: every arm treats the 26 letters alike,
so a renaming changes no answer, right or wrong. E1 is safe because
`missing` never goes below 0.

## Verification

The four arms print the same output as `check_inclusion.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and run
clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. `karac check`
passes on every arm, the differential and the bench program.

The frozen legacy backends refuse every arm, the differential and the
bench program under `karac run --interp`, `karac run` and `karac build`,
at type checking. Each arm reads its letters through `iter()` as `*c`
(the shrink arm `*x`, over `bytes()`), and legacy gives the element as a
`char` or `u8` where v2 gives a reference: "unary '*' requires 'ref T',
'mut ref T', or a raw pointer, found 'char'". Legacy is frozen, so this
is noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It makes 100 random pairs once: s1 of
5 to 200 letters and s2 of 10,000 (the problem's most), both over the
first 3 to 26 letters of the alphabet, and every other s2 with s1's
letters, shuffled, put in at a random place. Then 300 times over every
pair is answered. Every implementation prints `100 pairs, 300 rounds:
15900 found, checksum 697485292`, the Kāra program under `karac
__mir-run` included (357 s).

Rust, Go and Python collect each string into an array of chars on every
call, as the Kāra arm does, and C copies each into a fresh array of code
points. Spot timings on a shared 4-core container, three runs each (two
for Python; `bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.27 to 0.29 s |
| Rust (`rustc -O`) | 0.54 to 0.56 s |
| Rust (`rustc -O -C overflow-checks=on`) | 2.50 to 2.61 s |
| Go | 1.22 to 1.33 s |
| Python | 48.8 to 50.1 s |
| Kāra (`karac build --mir`) | 4.10 to 4.18 s |

The legacy `karac build` refuses this program on the same `*c`. So
`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend; that edit is by hand, on top of the
`scripts/new-bench.sh` output. The `--mir` row is timed at kara
`c0de09ec65`. Under `karac __mir-llvm-run` the program prints the same
line in 7.1 s, compile included; that JITs the MIR's IR without
optimization passes, so it is not a benchmark.

The Kāra row is seven to eight times Rust's, but 1.6 times Rust's with
overflow checks on, and most of the gap is those checks. Measured alone,
the window loop over one 10,000-letter text of random letters from all
26, run 30,000 times, takes 2.39 to 2.48 s with `karac build --mir`,
0.64 to 0.69 s with `rustc -O` and 1.95 to 1.96 s with `rustc -O -C
overflow-checks=on`. `rustc -O` turns the `missing -= 1` and `missing +=
1` under their `if`s into arithmetic with no branch (`setg` and `sub`,
`cmp` and `adc` in its assembly). With overflow checks each becomes a
branch, and on random letters those branches are hard to predict; the
Kāra build's assembly branches there the same way. On a text whose
letters repeat in a fixed pattern, where the branches predict well, the
same loop takes 1.07 to 1.15 s against Rust's 1.08 to 1.12. The rest is
not measured in full: each call collects both `String`s into a
`Vec[char]`, and collecting 10,000 chars took about three times Rust's
time when measured alone (1.08 s against 0.36 s for 30,000 collects).

## Compiler findings

One filed, found while measuring the bench rather than in the kata:
**B-2026-10-14-19**, fixed in kara `2260a980ea`. A `collect()` written
as an element of a tuple literal, as in
`pairs.push((s.chars().collect(), 1))` or `let t: (Vec[char], i64) =
(s.chars().collect(), 1);`, did not build on either MIR backend ("an
expression whose type does not lower", `UnsolvedParam("C")`), though
`karac check` passed it. Both now build and print the expected values
under `karac __mir-run` and `karac __mir-llvm-run`, rechecked at kara
`555c29b44e`. The bench keeps each pair as two `String`s, as the problem
gives them, so it never met this; the probe that did collected outside
the tuple. The legacy failures above are not filed because legacy is
frozen.
