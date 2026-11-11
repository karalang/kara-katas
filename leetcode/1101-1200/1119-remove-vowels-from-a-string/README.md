# 1119. Remove Vowels from a String

Given a string `s`, remove the vowels `'a'`, `'e'`, `'i'`, `'o'`, and
`'u'` from it, and return the new string.

```
s = "leetcodeisacommunityforcoders"  ->  "ltcdscmmntyfrcdrs"
s = "aeiou"                          ->  ""
```

**Constraints:** `1 <= s.length <= 1000`; `s` consists of only lowercase
English letters.

The arms are `fn remove_vowels(s: String) -> String`.

## Approaches

| file | mechanism |
|---|---|
| `remove_vowels.kara` ★ | the characters filtered by a `match` that names the five vowels, collected into a new `String`. O(n) |
| `remove_vowels_push.kara` | a loop over the characters, each pushed onto a `String` made with room for all of them unless `"aeiou"` holds it. O(n) |
| `remove_vowels_replace.kara` | each vowel replaced by nothing in turn, five passes over the text, each making a new `String`. O(n) |
| `remove_vowels_mask.kara` | the five vowels as bits of one `u32`, each byte's bit read at its distance from `b'a'`, and the bytes kept read back with `String.from_utf8`. O(n) |
| `remove_vowels_retain.kara` | the text copied and the vowels dropped from the copy in place with `retain`, as Rust's `String::retain` does. O(n) |
| `remove_vowels_solution.kara` | a Rust solution as LeetCode's Rust users write it (`impl Solution`, a filter on `!"aeiou".contains(*c)`), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 10 lines: the answers for LeetCode's two
examples and seven more (one consonant, one vowel, every letter once, a
vowel at each end, vowels only between, a repeated vowel, and no vowel
at all), then over 2000 random texts of up to 1000 letters, a vowel one
time in two to one time in six, the letters kept and a checksum (`2000
random texts: 705846 letters kept, checksum 397210105`).
`remove_vowels.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: while a vowel is left, the first one is cut out, the text
before it and after it kept as they are. It checks 2000 problems in
four kinds of 500: up to 30 letters, a vowel one time in two to one time
in six; one to three letters, a vowel one time in two; up to 20 letters
all vowels or all consonants; and up to 30 letters in runs, each run one
letter repeated. Every random choice is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal one |
| P2 | by a second reading, what is kept: the answer holds no vowel, its letters are found in the text in order, and it is as long as the text less its vowels |
| P3 | the text cut in two at a random place, each part answered, gives the answer joined |
| P4 | the text reversed gives the answer reversed |
| P5 | the consonants renamed by a random permutation, before or after, give the same |
| P6 | vowels put in at random places change nothing, and the answer answered again is itself |

All 72,000 checks pass on every arm: `2000 problems: checksum 28402089,
72000 checks over 6 arms: 0 failures`. A Python reading of the same
problems, removing the vowels with `str.translate`, gives the same
checksum.

## Mutation testing

Thirty edits to the differential, five to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`, each failing the same way
under both. All thirty are caught. Fifteen are kept, no two failing the
same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: `u` kept | P1 679, P2 679, P6 1291 |
| M2 | ★: the first kept letter lost | P1 1599, P2 1599, P3 1050, P4 1315, P6 1321 |
| M3 | ★: the answer reversed | P1 1311, P2 1311, P3 1049, P6 1311 |
| M4 | push: every kept letter doubled | P1 1599, P2 1599, P6 1599 |
| M5 | push: only the first half of the text read | P1 1268, P2 1268, P3 1025, P4 1314, P6 1221 |
| M6 | push: `a` kept | P1 734, P2 734, P6 1272 |
| M7 | replace: each vowel left as `_` | P1 1490, P2 1490, P6 1861 |
| M8 | replace: each vowel taken from the text, not the answer so far | P1 1391, P2 1391, P6 1791 |
| M9 | replace: `a` and `e` dropped only together | P1 1032, P2 1032, P3 10, P4 153, P6 1548 |
| M10 | mask: `v`'s bit for `u`'s | P1 1005, P2 1005, P5 755, P6 1291 |
| M11 | mask: the letter after each vowel in the alphabet dropped too | P1 1085, P2 1085, P5 1253 |
| M12 | retain: `w` for `u` | P1 989, P2 989, P5 714, P6 1291 |
| M13 | retain: `e` and `i` kept | P1 1045, P2 1045, P6 1555 |
| M14 | solution: the answer cut at 20 letters | P1 494, P2 494, P3 450, P4 494 |
| M15 | solution: an `x` after every answer | P1 2000, P2 2000, P3 2000, P4 1586, P5 1897, P6 2000 |

P1 and P2 catch all fifteen, P6 thirteen, P3 six, P4 five and P5 four.
P6 sees every edit that keeps a vowel or leaves something in its place,
since the vowels put in then show, and every edit whose answer changes
when it is answered again (M2 to M5, M15); it misses the two that wrong
only consonants, `b`, `f`, `j`, `p` and `v` dropped (M11) and the answer
cut at 20 letters (M14). P5 is the other side: it sees only the edits
that treat a consonant wrongly (M10 to M12, and M15's `x`), since
renaming the consonants commutes with any rule about vowels. P3 and P4
see the edits that depend on where the text starts, ends or is cut: the
first kept letter lost (M2), half the text read (M5), `ae` dropped only
together (M9), whose pair a cut or a reversal splits, and M14 and M15.
The ★ arm reversing its answer (M3) passes P4, since reversing the text
and then the answer gives the right answer back, and fails P3, where the
two halves come back in the wrong order.

Of the fifteen not kept, four fail as a kept edit: the push and replace
arms keeping `u` as M1, and the mask and retain arms keeping `a` as M6.
Six more fail alike in two or more arms: only the vowels kept (★, mask,
retain and solution), and `z` taken as a vowel (replace and retain).
The other five fail in ways of their own but were not needed: the ★ arm
taking `y` as a vowel, the push arm keeping `o`, the mask arm reading
`j`'s bit for `i`'s, and the solution arm keeping `i` and taking `x`,
`y` and `z` as vowels.

## Verification

Every arm prints the same output as `remove_vowels.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing
on any file, and `karac fix` has nothing to apply.

The kata found one gap, now fixed: `String` had no `retain`, though
`Vec`, `VecDeque`, `Map` and `Set` have one, and the retain arm's
`out.retain(|c| not is_vowel(c))` was refused as `no method 'retain' on
type 'String'` (B-2026-11-11-39). The ★, replace, mask and retain arms were
written as Kāra, the solution arm as Rust writes it; the push arm took a
habit from Rust. `karac fix` carried the solution arm to a clean check
in four rounds: `!` to `not`, `Solution::` to `Solution.` and `struct
Solution {}` declared, `*c` to `c` for a closure parameter that is a
`char`, and `"aeiou".contains(c)` to `"aeiou".contains(c.to_string())`,
since a `Str`'s `contains` takes a `Str`. The push arm's
`"aeiou".contains(c)` took the same fix, and the mask arm's
`s.bytes().filter(..)` became `s.bytes().iter().filter(..)`, as
`bytes()` is a `Vec[u8]`. The `c.to_string()` allocates a string per
character, which B-2026-11-10-25 tracks as a cost.

## Benchmarks

The bench builds 64 texts of 1000 random letters once, LeetCode's
longest. Each of 2000 rounds changes one letter in every text, makes it
a `String` and removes its vowels with the ★ arm: 128,000 calls. Every
implementation prints `2000 rounds over 64 texts of 1000 letters:
103378585 letters kept, checksum 809420667`. Each text and each answer
is its own heap string in every language: C `malloc`s a copy of the text
and the answer for each call and frees both.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `3402c1954a`
on LLVM 22. karac builds for the x86-64-v3 baseline, so the C and
overflow-checked Rust programs are also built at `-march=x86-64-v3`:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.339 to 0.354 s | 0.346 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.376 to 0.423 s | 0.383 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.692 to 0.716 s | 0.705 s |
| Kāra (`karac build`) | 0.689 to 0.824 s | 0.709 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.684 to 0.825 s | 0.716 s |
| Rust (`rustc -O`) | 0.761 to 0.860 s | 0.779 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.809 to 0.868 s | 0.838 s |
| Go | 1.478 to 1.623 s | 1.537 s |
| Python | 5.724 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Kāra is level with overflow-checked Rust, a little ahead of
plain Rust, and about 2.2x faster than Go, whose `strings.Builder`
grows as it goes. C takes about half Kāra's time: it copies bytes into
an answer allocated at the text's length, where Kāra and Rust walk the
text by `char` and collect into a `String`; the gap was not traced
further. Python takes about 8x
Kāra's time.
