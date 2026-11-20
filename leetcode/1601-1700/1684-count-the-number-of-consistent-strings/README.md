# 1684. Count the Number of Consistent Strings

You are given a string `allowed` consisting of **distinct** characters
and an array of strings `words`. A string is **consistent** if all
characters in the string appear in the string `allowed`.

Return *the number of **consistent** strings in the array* `words`.

```
allowed = "ab", words = ["ad","bd","aaab","baa","badab"]                ->  2
allowed = "abc", words = ["a","b","c","ab","ac","bc","abc"]             ->  7
allowed = "cad", words = ["cc","acd","b","ba","bac","bad","ac","d"]     ->  4
```

**Constraints:** `1 <= words.length <= 10^4`; `1 <= allowed.length <= 26`;
`1 <= words[i].length <= 10`; the characters in `allowed` are distinct;
`words[i]` and `allowed` contain only lowercase English letters.

## Approaches

| file | mechanism |
|---|---|
| `consistent.kara` ★ | each allowed letter marks its place in a fixed array of 26 (`[false; 26]`); a word is consistent when every one of its bytes finds its mark. O(total length) |
| `consistent_set.kara` | a `Set[char]` of the allowed letters, collected from `chars()`; the words whose every letter is in it, counted by `filter`. O(total length) expected |
| `consistent_mask.kara` | every word's letters folded into a bit mask, and the word consistent when its mask has no bit outside the allowed letters' (`mask & ~allowed == 0`). O(total length) |
| `consistent_solution.kara` | a Rust solution as LeetCode's Rust users write it, a `0u32` mask of the allowed letters and a `filter` over `bytes()`, carried to Kāra by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 8 lines: LeetCode's three examples, every
letter allowed, and one letter; then the consistent words summed and a
checksum for 3000 random problems of up to 10 words from 4 letters, 300
of up to 1000 from 10, and 10 of up to `10^4` from all 26, each letter
allowed half the time. `consistent.py` mirrors the ★ arm and its output
is byte-identical.

```
2
7
4
3
3
3000 problems of up to 10 words from 4 letters: 2978 consistent, checksum 252278505
300 problems of up to 1000 words from 10 letters: 17530 consistent, checksum 619199862
10 problems of up to 10000 words from 26 letters: 4294 consistent, checksum 230886186
```

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: a word is consistent when every one of its characters is
found among `allowed`'s, searched one by one. It checks 3000 random
problems of 1 to 12 words of 1 to 6 letters; the allowed letters are
each of the first 1 to 6 kept half the time, shuffled, and the words are
drawn from those letters and one more. Every case is drawn before any
arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the words split in two at a random place give two answers that add up to it |
| P3 | every word reversed, and the allowed letters reversed, give the same answer |
| P4 | the allowed letters added as a word, and they with a `z`, add exactly one |
| P5 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 372698254, 60000 checks
over 4 arms: 0 failures` under every lane in Verification, and a Python
reading of the statement, `set(word) <= set(allowed)`, gives the same
checksum. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. P2 fails for no mutant: every edit
still judges each word on its own, so the halves always add up. M2 and
M7 are one mistake written two ways, a word with any allowed letter
counted, and fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: each allowed letter marks the next one | P1 1722, P4 3000, P5 1722 |
| M2 | ★: `any` for `all` | P1 2808, P4 3000, P5 2808 |
| M3 | ★: the first allowed letter not marked | P1 1329, P3 679, P4 3000, P5 1329 |
| M4 | set: a word's first letter not checked | P1 1904, P3 1375, P5 1904 |
| M5 | set: only the first two allowed letters kept | P1 453, P3 388, P4 825, P5 453 |
| M6 | mask: the bits folded with `^`, so a letter twice cancels | P1 1666, P5 1666 |
| M7 | mask: a word sharing any letter with the mask | P1 2808, P4 3000, P5 2808 |
| M8 | mask: the allowed letters a subset of the word's | P1 2445, P4 3000, P5 2445 |
| M9 | solution: only the last allowed letter in the mask | P1 844, P3 546, P4 1536, P5 844 |
| M10 | solution: each letter looked up one bit higher | P1 1544, P4 3000, P5 1544 |

## Benchmarks

The bench draws 100 random problems of `10^4` words, LeetCode's largest,
of 1 to 10 letters, each letter allowed seven times in eight, all of them
first, then answers each 20 times by the ★ arm in all five languages.
Every implementation prints `100 problems of 10000 words, 20 rounds:
11048780 consistent, checksum 18845973`. The C build also runs clean
under gcc's AddressSanitizer and UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `9b0b5eb92c` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.229 s |
| Go | 0.316 s |
| Rust (`rustc -O`) | 0.322 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.330 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.351 s |
| Kāra (`karac build`) | 0.358 s |
| Python | 7.2 s |

The sequential Kāra build takes 1.09x Rust's time and 1.06x that of Rust
with overflow checks on, the equal-safety comparison (BENCHMARKS.md). C
is the fastest here at 0.229 s.

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here:
its user time is not above its real time (0.339 s and 0.376 s on one
run).

## Verification

All four arms print the same output as `consistent.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `9b0b5eb92c`.

## Writing it

The set arm checked clean as first written. The ★ arm's first draft
asked `word.bytes().all(..)`, as Rust's byte iterator takes it; Kāra's
`bytes()` is a slice, and an adaptor on it wants an explicit `.iter()`
(E0236), which `karac fix` wrote. The same fix put `.iter()` before the
mask arm's `fold`, and the ★ arm's `(b - b'a') as i64`, a byte that
widens by itself, lost its cast. The mask arm wrote Rust's `!allowed_mask`;
the refusal (E0001) names `not` for a bool and `~` for an integer, and
`karac fix` wrote `~allowed_mask`. The harness's `answer as i64` was
dropped the same way in every arm.

The Rust solution took one `karac fix` of 5 edits: `struct Solution {}`
added, `Vec<String>` written `Vec[String]`, `.iter()` put after
`w.bytes()`, and the harness's cast dropped; the `0u32` mask and the
`b'a'` byte literals carried over as written.

`arm_name` in the differential indexes a list of string literals for a
`Str`, as #1662's does (B-2026-11-19-131).
