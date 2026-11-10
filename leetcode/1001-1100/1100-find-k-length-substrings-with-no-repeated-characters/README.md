# 1100. Find K-Length Substrings With No Repeated Characters

Given a string `s` and an integer `k`, return the number of substrings in
`s` of length `k` with no repeated characters.

```
s = "havefunonleetcode", k = 5  ->  6
s = "home",              k = 5  ->  0
```

The six in the first are `havef`, `avefu`, `vefun`, `efuno`, `etcod`
and `tcode`; the second has no substring of length 5.

**Constraints:** `1 <= s.length <= 10^4`; `s` consists of lowercase
English letters; `1 <= k <= 10^4`.

The arms are `fn num_k_len_substr_no_repeats(s: String, k: i64) -> i64`.
A substring is counted once for each place it starts: `abab` has two
substrings `ab` of length 2 at 0 and 2, and both count.

## Approaches

| file | mechanism |
|---|---|
| `num_k_len_substr_no_repeats.kara` ★ | a sliding window of `k` letters over `s.bytes()`, with a count of each letter in a `[0; 26]` array and of the letters that occur more than once: each step adds the letter coming in and takes away the one going out, and a window with no repeated letter counts. Over 26 letters nothing fits. O(n) |
| `num_k_len_substr_no_repeats_last.kara` | the last place each letter was seen, a `Vec.filled(26, -1)`: the run ending at `i` with no repeat starts just past the last copy of any letter in it, and every `i` whose run is at least `k` long ends one such substring. `chars().enumerate()`. O(n) |
| `num_k_len_substr_no_repeats_windows.kara` | the statement as iterator chains: `windows(k)` over the letters, each kept when a `Set[char]` of its letters is `k` large, then `count`. O(nk) |
| `num_k_len_substr_no_repeats_mask.kara` | a bit mask per start: the letters of the window are bits of a `u32`, and the scan from each start stops at the first letter already set. O(nk) |
| `num_k_len_substr_no_repeats_map.kara` | a sliding window over a `Map[char, i64]` of letter counts through `entry(..).or_insert(0)` and `get_mut`: a letter that leaves is removed at count zero, so the window has no repeat exactly when the map holds `k` letters. O(n) |
| `num_k_len_substr_no_repeats_solution.kara` | a Rust solution as LeetCode's Rust users write it (`impl Solution`, `s.as_bytes()`, `k as usize`, a window shrunk with `while cnt[c] > 1`), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 15 lines: the answers for LeetCode's two
examples and ten more (one letter, a run of one letter at `k` 1 and 2,
`abcabc` at 3 and 4, the 26 letters at 26 and with `a` again at 27,
`abab` at 2,
`leetcode` whole, and the alphabet backwards with `z` again), then over
2000 random texts of 1 to 200 letters the substrings found (`26923
substrings, checksum 568100580`), and 10^4 letters, LeetCode's longest,
at every `k` from 1 to 27 and at `k` = 10^4.
`num_k_len_substr_no_repeats.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every start with `k` letters after it, each pair of those
letters compared. It checks 2000 problems in four kinds of 500: 1 to 60
letters from the first 1 to 26, `k` from 1 to 30; the 26 letters
shuffled and cut to 1 to 26 of them, `k` within two of that length;
1 to 30 letters from two or three, `k` from 1 to 4; and 100 to 160
letters from all 26, `k` from 5 to 15. Every random choice is drawn
before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal count |
| P2 | at most one substring per start, none longer than 26 letters, and at `k` = 1 every letter counts |
| P3 | the text backwards gives the same answer |
| P4 | every letter renamed by a step coprime to 26 (`a` + i to `a` + i·step mod 26) gives the same answer |
| P5 | the text twice over gives each copy's substrings and at most `k` - 1 more across the join |
| P6 | one letter longer, the count drops by the starts whose longest run with no repeat is exactly `k` |

All 72,000 checks pass on every arm: `2000 problems: checksum
269077245, 72000 checks over 6 arms: 0 failures`. A Python reading of
the same problems gives the same checksum.

P1 counts every substring, and P6 the runs from each start, both
literally; P2's `k` = 1 is the text's length. P3, P4 and P5 compare the
arm only with itself.

## Mutation testing

Thirty edits to the differential, five to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`, each failing the same way
under both. All thirty are caught. Fifteen are kept, no two failing the
same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a third copy counted as another repeat | P1 552, P3 436, P5 381, P6 682 |
| M2 | ★: a repeat cleared only when its letter is gone | P1 1161, P2 1954, P3 723, P5 1194, P6 1136 |
| M3 | ★: the window one letter too long | P1 750, P2 1348, P3 584, P5 689, P6 644 |
| M4 | ★: windows shorter than `k` counted | P1 1442, P2 297, P3 711, P5 989, P6 695 |
| M5 | last: the run may start further back | P1 977, P2 16, P3 593, P6 920 |
| M6 | last: only a run of exactly `k` counted | P1 856, P2 1923, P5 317, P6 856 |
| M7 | last: every letter seen at 0 | P1 689, P2 2000, P3 228, P5 544, P6 294 |
| M8 | last: a run one longer needed | P1 1130, P2 2000, P5 317, P6 809 |
| M9 | windows: one repeat allowed | P1 903, P6 1010 |
| M10 | windows: the whole text never counted | P1 113, P2 46, P5 113, P6 211 |
| M11 | mask: letters 16 apart share a bit | P1 674, P4 363, P6 635 |
| M12 | mask: 26 different letters never counted | P1 5, P6 10 |
| M13 | map: a letter that leaves never removed | P1 1131, P2 1923, P3 555, P5 1111, P6 1101 |
| M14 | map: a letter that leaves taken out twice | stops: `unwrap()` on `None` |
| M15 | solution: the window shrunk one letter at a repeat | P1 866, P3 229, P6 928 |

Of the fourteen that run to the end, P1 and P6 catch all fourteen, P2
and P5 nine, P3 eight and P4 one. P4 sees only the mask arm sharing a
bit between letters 16 apart (M11), the one edit that depends on which
letters the text uses; renaming them by a step coprime to 26 moves
which pairs share a bit, and nothing else sees it but P1 and P6. P3, P4
and P5, which compare the arm only with itself, catch twelve. They miss
one repeat allowed (M9), which counts the same windows read backwards,
renamed or twice over, and 26 different letters never counted (M12),
which only a window of the whole alphabet meets: five problems in 2000,
and ten more under P6, which asks every problem at `k` + 1.

Of the fifteen not kept, five fail exactly as a kept edit: M6 is also
the solution arm not moving the window on after a count; M7 is also the
windows arm never counting the first window, since a letter seen at 0
pushes every run's start past 0; M8 is also the solution arm counting
windows of `k` + 1; M12 is also the solution arm with the same bound;
and M13 is also the map arm counting a letter coming in twice. The other
ten fail in ways of their own but were not needed: the ★ arm counting a
repeat twice, the last arm seeing a letter one place on, the windows
arm dropping the first letter of each window and every `a`, the mask
arm never trying the last window, remembering only the letter before
and ignoring the first letter of each window, the map arm allowing one
repeat and taking out the wrong letter, and the solution arm never
counting a letter twice.

## Verification

Every arm prints the same output as `num_k_len_substr_no_repeats.py`
under `karac __mir-run` (the v2 MIR interpreter), `karac
__mir-llvm-run`, and `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer) with no error. `karac run` and a `karac build` binary
print the same output for every arm and the differential. `karac check
--output=json` reports nothing on any file, and `karac fix` has nothing
to apply.

The kata found no compiler gap. `karac fix` carried every Rust spelling
tried across:

- The windows arm was written `.windows(k).filter(|w|
  w.iter().collect::<Set<char>>().len() == k)`. Kāra has no turbofish,
  and since that `collect` is the receiver of `len()`, nothing gives its
  type, so the refusal advises binding a typed `let` and offers no edit;
  the closure was rewritten by hand to `let letters: Set[char] =
  w.iter().collect();`. `windows(k)` is a `Vec`, and `karac fix` then
  added `.iter()` before `filter`.
- The last arm's `c as u8` on a `char` became `c as u32 as u8`, and the
  map arm's `get_mut(&out)` and `remove(&out)` lost the `&`.
- The Rust solution reaches a clean check in three rounds: `||` to `or`,
  then `struct Solution {}`, then `as_bytes()` to `bytes()` and `usize`
  to `i64`.

## Benchmarks

The bench builds 64 texts of 10^4 letters once, LeetCode's longest, over
the first 8 to 26 letters. Each of 10 rounds changes one letter in every
text, joins it into a fresh string and counts its substrings for 4
values of `k` from 1 to 30 with the ★ arm, each count on its own copy:
2560 calls over 25.6 million letters. Every implementation prints `10
rounds over 64 texts of 10^4 letters: 4010375 substrings, checksum
96494179`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `33ef2a7ad2`
on LLVM 22. karac builds for the x86-64-v3 baseline, so the C and
overflow-checked Rust programs are also built at `-march=x86-64-v3`:

| | time | median |
|---|---|---|
| C (`clang -O3 -march=x86-64-v3`) | 0.040 to 0.067 s | 0.043 s |
| C (`clang -O3`) | 0.042 to 0.081 s | 0.044 s |
| Rust (`rustc -O`) | 0.055 to 0.102 s | 0.058 s |
| Go | 0.069 to 0.096 s | 0.077 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.217 to 0.248 s | 0.227 s |
| Kāra (`karac build`) | 0.224 to 0.279 s | 0.231 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.223 to 0.257 s | 0.232 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.226 to 0.258 s | 0.239 s |
| Python | 5.070 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Kāra takes about 5.4x C's time and ties overflow-checked Rust.
With the checks off, Rust drops from 0.234 s to 0.058 s, so the gap is
the overflow checking of the window's counters, which Kāra does by
default and `rustc -O` does not. Python takes about 21x Kāra's time.
