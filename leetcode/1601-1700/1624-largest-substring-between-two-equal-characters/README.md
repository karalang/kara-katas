# 1624. Largest Substring Between Two Equal Characters

Given a string `s`, return *the length of the longest substring between
two equal characters, excluding the two characters.* If there is no such
substring return `-1`.

A **substring** is a contiguous sequence of characters within a string.

```
s = "aa"     ->  0
s = "abca"   ->  2
s = "cbzxy"  ->  -1
```

**Constraints:** `1 <= s.length <= 300`; `s` contains only lowercase
English letters.

## Approaches

| file | mechanism |
|---|---|
| `gap.kara` ★ | one pass: the first index of each letter in a `[-1; 26]` table, and at every later sight of it the gap back to that first index. The first sight gives the longest gap for every later one. O(n) |
| `gap_pairs.kara` | every pair `i < j` with `s[i] == s[j]`, the gap `j - i - 1`, the largest kept. O(n^2) |
| `gap_ends.kara` | a `Map[char, (i64, i64)]` from each letter to its first and last index, then the widest gap over its values. A letter seen once gives `-1`, so the answer is the maximum with no special case. The map is folded to a maximum, so its walk order never shows. O(n) |
| `gap_solution.kara` | LeetCode's Rust template: the last index of each byte first, then one pass from the left with the gap to each byte's last sight. Carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's three examples, one letter
alone, the alphabet with its first letter again (25), and a letter at
both ends of 300 (298); then the strings with no pair and a checksum of
every answer for 3000 random strings of up to 8 letters from 3, 3000 of
up to 30 from 26, and 300 of up to 300 from 26. `gap.py` mirrors the ★
arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: the substrings from the longest down, by slices of the
string, the first whose two neighbours are one letter. It checks 3000
random strings of 1 to 40 letters, every third from two letters, so
pairs are dense, the rest from 3 to 26. Every random choice is drawn
before any arm answers. The interpreter takes about 4 s.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the string reversed has the same answer |
| P3 | the letters mirrored (`a <-> z`, `b <-> y`, ..) leave the answer |
| P4 | the string with its first letter written again at the end answers `n - 1`, the whole of it |
| P5 | the answer is in `-1..=n - 2`, and `-1` exactly when no letter repeats |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 305398281, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. M4 and M8, which lose only the gap of
0 between two neighbours, are the rarest: 91 strings in 3000.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the first index moved up at each sight, so only neighbouring pairs count | P1 2015, P4 2266, P6 2015 |
| M2 | ★: the gap counts one of its ends | P1 2727, P4 3000, P5 674, P6 2727 |
| M3 | ★: the answer starts at 0, not -1 | P1 273, P5 273, P6 273 |
| M4 | pairs: `j` starts two past `i` | P1 91, P4 80, P5 91, P6 91 |
| M5 | pairs: `i` starts at 1 | P1 1193, P2 1414, P4 3000, P5 82, P6 1193 |
| M6 | ends: a letter's first index moved up to its previous sight | P1 2015, P2 1332, P4 2266, P6 2015 |
| M7 | ends: the narrowest gap, not the widest | P1 2553, P4 2892, P5 1525, P6 2553 |
| M8 | template: a gap counted only past `i + 1` | P1 91, P4 80, P5 91, P6 91 |
| M9 | template: each byte's first index kept, not its last | P1 2482, P2 2070, P4 2266, P5 461, P6 2482 |
| M10 | template: the last gap kept, not the largest | P1 2484, P2 1547, P4 2727, P6 2484 |

## Benchmarks

The bench draws 100000 random strings of 1 to 300 letters, all of them
first, then each one's answer by the ★ arm in all five languages. Kāra,
Rust and Go walk the characters (`chars()`, `range`); C walks the bytes,
which are the characters here. Every implementation prints `100000
random strings: answers sum to 14315974, checksum 567335135`. The C build
also runs clean under gcc's AddressSanitizer and
UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `eb32a1ff0` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.073 s |
| Rust (`rustc -O`) | 0.082 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.085 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.085 s |
| Kāra (`karac build`) | 0.088 s |
| Go | 0.187 s |
| Python | 4.0 s |

Kāra is level with Rust with overflow checks, a tenth behind C. Most of
the time in every language is drawing the 15 million letters; the
answers themselves are one table lookup per letter.

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time is not above its real time (0.073 s and 0.085 s on one run).

## Verification

All four arms print the same output as `gap.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them, the differential and the bench. `karac check` reports nothing on
any of them, and `karac fix` has nothing left to change. Checked at kara
`eb32a1ff0`.

## Writing it

The three arms of my own checked clean as first written. The harness
first wrote a letter as `('a' as u8 + r as u8) as char`; a `char` does not
cast straight to `u8`, and `karac fix` wrote the byte literal `b'a'`. It
also dropped a `.to_string()` on a string literal, which is already a
`String`. In the differential, the mirrored letter took `c as u32 as u8`,
the cast the diagnostic names for a `char` variable.

LeetCode's Rust template takes one `karac fix` of 8 edits:
`struct Solution;` to `struct Solution {}`, `s.as_bytes()` to `s.bytes()`,
`[0usize; 26]` to `[0; 26]`, both `&b` patterns to `b`, both
`(b - b'a') as usize` indexes to `b - b'a'`, and `Solution::` to
`Solution.`. It then checks and agrees with no hand edit. No compiler gap
was met.
