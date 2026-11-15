# 1163. Last Substring in Lexicographical Order

Given a string `s`, return the last substring of `s` in lexicographical
order.

```
s = "abab"      ->  "bab"
s = "leetcode"  ->  "tcode"
```

**Constraints:** `1 <= s.length <= 4 * 10^5`; `s` contains only
lowercase English letters.

The arms are `fn last_substring(s: Str) -> String`.

## Approaches

A substring is never larger than the suffix it begins, so the answer is
the largest suffix; the arms differ in how they find it without
comparing every pair of suffixes in full.

| file | mechanism |
|---|---|
| `last_substring.kara` ★ | two pointers over `s.bytes()`: `i` the best start so far, `j` its challenger, compared `k` letters in; the loser skips past everything the comparison read, since every start inside it loses to a start the winner already beat. O(n) |
| `last_substring_period.kara` | the maximal suffix as the Two-Way string matcher computes it (Crochemore and Perrin): the start before the best suffix, a candidate, an offset and the best suffix's period; a smaller letter extends the period, an equal one walks it, a larger one starts a new best. O(n) |
| `last_substring_candidates.kara` | candidates: every place the largest letter stands; each round keeps the survivors holding the largest next letter and drops a survivor the one before it has run into. O(n log n) |
| `last_substring_hash.kara` | hashing: the best start meets each later start of the largest letter, the two suffixes' longest common prefix found by a binary search over two prefix hashes (modulo 10^9 + 7 and 10^9 + 9), and the letter after it decides. O(n log n) |
| `last_substring_solution.kara` | a Rust solution as LeetCode's Rust users write it (`impl Solution`, `s.as_bytes()`, `let (mut i, mut j, mut k)`, a `continue` on a match, `std::cmp::max`, the answer rebuilt by `String::from_utf8(s[i..].to_vec())`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 14 lines: LeetCode's examples (`"bab"`,
`"tcode"`); one letter; one letter repeated (`"zzz"`); the largest letter
last (`"aaab"`: `"b"`); a period of three (`"abcabcabc"`: `"cabcabc"`);
two runs of the largest letter, the longer one later (`"zazzab"`:
`"zzab"`); a prefix tie the longer suffix wins (`"zyzyzyz"`, all of it);
the largest letter first (`"cbabc"`, all of it). Then 2000 random strings
of 1 to 30 letters over the first 1 to 4 letters or all 26 (`2000 random
strings: starts 10390, checksum 918827991`), and four of 4 * 10^5
letters, the constraints' most: one letter repeated (all of it), a period
of two (from 1), random over three letters, and every letter `a` but the
last (the last). `last_substring.py` mirrors the ★ arm and its output is
byte-identical; a Python reading that takes the largest of every
substring gives the same first 10 lines.

The Mend loop: the ★, period and candidates arms check clean as written.
The hashing arm takes one fix, `let (mut lo, mut hi)` to `let mut (lo,
hi)`. The Rust arm takes three rounds (8, 1 and 1 edits): the tuple of
`let mut` bindings to `let mut (i, j, k)`, `std::cmp::max` to `max`,
`String::from_utf8` to `String.from_utf8`, `&str` to `Str`, `Solution::`
to `Solution.`; then `struct Solution {}`; then `s.as_bytes()` to
`s.bytes()`. The `continue`, the slice `s[i..]` and its `to_vec()` are
kept. Its output matches on the first run.

Writing the differential found a gap: `String.from_utf8(s.bytes().iter()
.map(...).collect())`, Rust's spelling, was refused, because Kāra's
`from_utf8` takes a `Slice[u8]` and the `collect()` took that slot's
type as its target, which nothing gathers into. A `collect()` passed
where a call takes a `Slice[T]` now gathers a `Vec[T]`, which the call
borrows as it borrows any `Vec`. That is kara B-2026-11-15-21, found the
same day by kata 1585 and fixed at `bae463436e`.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: for up to 12 letters, every substring, the largest kept; past
that, every suffix. It checks 2000 strings in four kinds of 500, over
letters from `b`, so that `a` is below every letter and `z` above: 1 to
10 letters over 1 to 3; 1 to 40 over 1 to 4; a block of 1 to 5 letters
over 2 repeated to up to 120, a quarter with one letter changed; and 50
to 600 over 2 to 13. Every random choice the properties make is drawn
before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal one |
| P2 | `a` appended, a letter below every other, joins the answer |
| P3 | `z` prepended, a letter above every other, makes the whole string the answer |
| P4 | the letters renamed by a drawn increasing map keep where the answer starts |
| P5 | the string cut at a drawn place at or before the answer's start keeps the answer |
| P6 | the answer's own answer is itself |

All 60,000 checks pass on every arm: `2000 strings: checksum 416595250,
60000 checks over 5 arms: 0 failures`, in 14 s under `karac __mir-run`.
A Python reading of the same draws, with the mirror against the literal
reading, gives the same checksum.

## Mutation testing

Seventeen edits to the differential, three or four to each arm, each run
under `karac __mir-run` and `karac __mir-llvm-run` with
`KARAC_HASH_SEED=1`, each failing the same way under both. Fourteen are
caught and three are equivalent:

- the ★ arm's winner placed at `max(i + k, j)` rather than `max(i + k +
  1, j)` (T4): every start before `i + k` is still ruled out, and taking
  one more start back into the search only gives up part of a skip;
- the candidates arm dropping a survivor that starts just past the
  previous survivor's reach (C1): if that start's suffix were the
  largest, the previous survivor's suffix, the same `k + 1` letters
  followed by it, would be larger still;
- the hashing arm never trying the last place (H3): a suffix of one
  letter is a prefix of every other suffix starting with that letter, so
  it wins only when it is the only one, and then it is where the search
  starts.

| # | mutation | failures by property |
|---|---|---|
| T1 | ★: the challenger skips one start too many | P1 527, P5 259 |
| T2 | ★: the comparison turned around | P1 1486, P2 2000, P3 2000, P5 436 |
| T3 | ★: the last letter never compared | P1 63, P2 63, P5 44 |
| E1 | period: an equal letter read as smaller | P1 866, P5 731 |
| E2 | period: the period one too long | P1 15, P5 19 |
| E3 | period: the next candidate one place late | P1 82, P5 63, P6 47 |
| C2 | candidates: the smallest letter's places | P1 1486, P2 2000, P3 2000, P5 302 |
| C3 | candidates: every other letter compared | P1 441, P5 145 |
| H1 | hash: every power one too large | P1 866, P5 731 |
| H2 | hash: a negative remainder left as it is | P1 417, P2 12, P4 18, P5 496, P6 40 |
| X1 | solution: the winner placed one start late | P1 998, P5 310 |
| X2 | solution: the next challenger one start late | P1 48, P5 40, P6 25 |
| X3 | solution: the last letter never compared | P1 63, P2 63, P5 44 |
| X4 | solution: the second place never challenges | P1 165, P5 214 |

P1 and P5 catch all fourteen, P2 five, P6 three, P3 two and P4 one. The
cut (P5) is the strongest of the properties: a start that an arm skips
wrongly is often the first place of a cut string. The two edits that
look for the smallest answer (T2, C2) fail every `a` appended and every
`z` prepended. Only the negative remainders (H2) break the renaming,
since their collisions depend on the letters' codes.

## Benchmarks

`bench/` times the ★ arm against the same two pointers in C, Rust, Go and
Python, each copying the answer out as a new string. 8 strings of 4 *
10^5 letters, the constraints' most, are built once, two of each kind:
random over all 26 letters, random over two, a random block of seven
letters repeated with one letter in a thousand changed, and `y` and `z`
with nine in ten of them `z`. Each of 150 rounds solves every string from
a random place in its first half. Every program prints `150 rounds over
8 strings of 4 * 10^5 letters: total 305345550, checksum 800541146`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `f5f9065de8`
on LLVM 22. karac builds for the x86-64-v3 baseline, so the C and
overflow-checked Rust programs are also built at `-march=x86-64-v3`:

| | time | median |
|---|---|---|
| C (`clang -O3 -march=x86-64-v3`) | 0.560 to 0.595 s | 0.575 s |
| C (`clang -O3`) | 0.562 to 0.621 s | 0.588 s |
| Rust (`rustc -O`) | 0.586 to 0.668 s | 0.613 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.796 to 0.831 s | 0.811 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.791 to 0.875 s | 0.816 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.891 to 0.977 s | 0.907 s |
| Kāra (`karac build`) | 0.894 to 0.940 s | 0.917 s |
| Go | 0.916 to 1.055 s | 0.986 s |
| Python | 47.8 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane; a plain `karac build` gives the same binary, byte
for byte, so the two Kāra rows are one program timed twice. Kāra takes
about 1.11x overflow-checked Rust's time, the equal-safety comparison,
and about 1.5x unchecked Rust's and C's: the loop is two byte loads, a
compare and index arithmetic, so the checks on `i + k` and `j + k` are a
large share of it. Python takes about 53x Kāra's time.
